"""reporter.py — MD and JSON report builders."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Tuple

from scripts.irb.evidence import CheckStatus, RunReport


def _sanitize_paths(text: str, target: Path, builder_root: Path) -> str:
    """Replace machine-local absolute paths with portable tokens.

    Replacements applied in order (most-specific first):
    - Full target repo path → $TARGET_ROOT
    - Full builder repo path → $BUILDER_ROOT
    - Any remaining /Users/<name>/ segment → /Users/<redacted>/
    """
    if not text:
        return text
    text = text.replace(str(target), "$TARGET_ROOT")
    text = text.replace(str(builder_root), "$BUILDER_ROOT")
    text = re.sub(r"/Users/[^/]+/", "/Users/<redacted>/", text)
    return text


def _table_reason(text: str) -> str:
    """Return a short, table-safe failure reason (max 70 chars, pipes escaped).

    Truncates cleanly — never ends mid-list — and appends "…" if clipped.
    """
    if not text:
        return ""
    one_line = text.replace("|", "\\|").replace("\n", " ").strip()
    if len(one_line) <= 70:
        return one_line
    trunc = one_line[:67].rstrip("[,( ")
    return trunc + "…"


def _failure_detail_lines(text: str) -> list[str]:
    """Format a failure reason for the Evidence Detail section.

    Long failure reasons that contain list literals are wrapped in a fenced
    ``text`` block so they render clearly instead of as a single long line.
    """
    if "[" in text and "]" in text and len(text) > 60:
        return ["- Failure (full list):", "```text", text, "```"]
    return [f"- Failure: {text}"]


def _parse_project_name_regex(toml_text: str) -> str | None:
    """Tiny deterministic TOML parser: extract [project] name without tomllib.

    Rules:
    - Find a line matching ``[project]`` (as a section header, nothing else on line).
    - Within that section, find ``name = "..."`` or ``name = '...'`` (double or single quotes).
    - Stop scanning when the next ``[<something>]`` section begins.
    - Comment lines (stripped starting with ``#``) are ignored.
    - Return the extracted name string, or None if not found.
    """
    import re

    in_project_section = False
    section_re = re.compile(r"^\s*\[([^\]]+)\]\s*$")
    name_re = re.compile(r"""^\s*name\s*=\s*["']([^"']+)["']\s*(?:#.*)?$""")

    for raw_line in toml_text.splitlines():
        line = raw_line.strip()
        if line.startswith("#"):
            continue
        section_m = section_re.match(raw_line)
        if section_m:
            section_name = section_m.group(1).strip()
            if section_name == "project":
                in_project_section = True
            elif in_project_section:
                # Entered a new section after [project] — stop
                break
            continue
        if in_project_section:
            name_m = name_re.match(raw_line)
            if name_m:
                return name_m.group(1)

    return None


def get_project_slug(target: Path) -> tuple[str, str]:
    """Return (project_slug, slug_source) using a four-tier fallback chain.

    Tiers:
    1. stdlib ``tomllib`` (Python 3.11+)
    2. ``tomli`` backport (optional install)
    3. Inline regex parser (no external deps)
    4. ``target.name`` directory basename
    """
    pyproject = target / "pyproject.toml"

    # Tier 1: stdlib tomllib (Python 3.11+)
    try:
        import tomllib  # type: ignore[import]
        with open(pyproject, "rb") as fh:
            data = tomllib.load(fh)
        name = data["project"]["name"]
        return name, "tomllib"
    except (ImportError, ModuleNotFoundError):
        pass  # Python < 3.11 — try next tier
    except Exception:
        pass  # file missing, parse error, no [project].name — fall through

    # Tier 2: tomli backport
    try:
        import tomli  # type: ignore[import]
        with open(pyproject, "rb") as fh:
            data = tomli.load(fh)
        name = data["project"]["name"]
        return name, "tomli"
    except (ImportError, ModuleNotFoundError):
        pass
    except Exception:
        pass

    # Tier 3: inline regex parser
    try:
        text = pyproject.read_text(encoding="utf-8")
        name = _parse_project_name_regex(text)
        if name:
            return name, "fallback_regex"
    except Exception:
        pass

    # Tier 4: basename fallback
    return target.name, "basename_fallback"


def compute_report_filename(
    project_slug: str,
    tier: int,
    git_sha_8: str,
    runner_date: str,
) -> Tuple[str, str]:
    """Return (md_filename, json_filename).

    Format: YYYY-MM-DD__<project-slug>__tier-<N>__<git-sha-8>.(md|json)
    """
    base = f"{runner_date}__{project_slug}__tier-{tier}__{git_sha_8}"
    return f"{base}.md", f"{base}.json"


def build_json_report(report: RunReport, target: Path, builder_root: Path) -> dict:
    def _s(text: str | None) -> str | None:
        return _sanitize_paths(text, target, builder_root) if text else text

    return {
        "report_version": report.report_version,
        "spec_id": report.spec_id,
        "spec_version": report.spec_version,
        "target_project": report.target_project,
        "target_git_sha": report.target_git_sha,
        "runner_timestamp": report.runner_timestamp,
        "slug_source": report.slug_source,
        "outcome": report.outcome.value,
        "summary": {
            "total": report.summary.total,
            "passed": report.summary.passed,
            "failed": report.summary.failed,
            "skipped": report.summary.skipped,
            "blocking_failed": report.summary.blocking_failed,
        },
        "checks": [
            {
                "id": r.id,
                "name": r.name,
                "category": r.category,
                "status": r.status.value,
                "blocking": r.blocking,
                "evidence_collected": r.evidence_collected,
                "evidence_summary": _s(r.evidence_summary),
                "failure_reason": _s(r.failure_reason),
            }
            for r in report.checks
        ],
    }


def build_md_report(report: RunReport, tier: int, target: Path, builder_root: Path) -> str:
    lines = [
        f"# IRB Tier-{tier} Certification Report",
        "",
        f"**Outcome:** `{report.outcome.value}`  ",
        f"**Project:** {report.target_project}  ",
        f"**Git SHA:** `{report.target_git_sha_8}`  ",
        f"**Timestamp:** {report.runner_timestamp}  ",
        f"**Spec:** {report.spec_id} v{report.spec_version}  ",
        f"**Slug source:** {report.slug_source}  ",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|-------|",
        f"| Total checks | {report.summary.total} |",
        f"| Passed | {report.summary.passed} |",
        f"| Failed | {report.summary.failed} |",
        f"| Skipped | {report.summary.skipped} |",
        f"| Blocking failed | {report.summary.blocking_failed} |",
        "",
        "## Check Results",
        "",
        "| ID | Name | Status | Blocking | Evidence | Failure Reason |",
        "|----|------|--------|----------|----------|----------------|",
    ]

    def _s(text: str) -> str:
        return _sanitize_paths(text, target, builder_root)

    for r in report.checks:
        if r.status == CheckStatus.PASS:
            status_cell = r.status.value
        else:
            status_cell = f"**{r.status.value}**"
        ev_cell = "yes" if r.evidence_collected else "**NO**"
        reason = _table_reason(_s(r.failure_reason or ""))
        lines.append(
            f"| {r.id} | {r.name} | {status_cell} | "
            f"{'yes' if r.blocking else 'no'} | {ev_cell} | {reason} |"
        )

    lines += ["", "## Evidence Detail", ""]
    current_cat = None
    for r in report.checks:
        if r.category != current_cat:
            lines.append(f"### {r.category.upper()}")
            lines.append("")
            current_cat = r.category
        lines += [
            f"**{r.id}** — {r.name}",
            f"- Status: {r.status.value}",
            f"- Blocking: {r.blocking}",
            f"- Evidence collected: {r.evidence_collected}",
            f"- Evidence: {_s(r.evidence_summary)}",
        ]
        if r.failure_reason:
            lines.extend(_failure_detail_lines(_s(r.failure_reason)))
        lines.append("")

    return "\n".join(lines)
