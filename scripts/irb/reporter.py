"""reporter.py — MD and JSON report builders."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from scripts.irb.evidence import CheckStatus, RunReport


def get_project_slug(target: Path) -> str:
    """Read pyproject.toml project.name via stdlib tomllib. Falls back to dir basename."""
    try:
        import tomllib  # stdlib Python 3.11+
        with open(target / "pyproject.toml", "rb") as fh:
            data = tomllib.load(fh)
        return data["project"]["name"]
    except Exception:
        return target.name


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


def build_json_report(report: RunReport) -> dict:
    return {
        "report_version": report.report_version,
        "spec_id": report.spec_id,
        "spec_version": report.spec_version,
        "target_project": report.target_project,
        "target_git_sha": report.target_git_sha,
        "runner_timestamp": report.runner_timestamp,
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
                "evidence_summary": r.evidence_summary,
                "failure_reason": r.failure_reason,
            }
            for r in report.checks
        ],
    }


def build_md_report(report: RunReport, tier: int) -> str:
    lines = [
        f"# IRB Tier-{tier} Certification Report",
        "",
        f"**Outcome:** `{report.outcome.value}`  ",
        f"**Project:** {report.target_project}  ",
        f"**Git SHA:** `{report.target_git_sha_8}`  ",
        f"**Timestamp:** {report.runner_timestamp}  ",
        f"**Spec:** {report.spec_id} v{report.spec_version}  ",
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

    for r in report.checks:
        if r.status == CheckStatus.PASS:
            status_cell = r.status.value
        else:
            status_cell = f"**{r.status.value}**"
        ev_cell = "yes" if r.evidence_collected else "**NO**"
        reason = (r.failure_reason or "")[:100]
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
            f"- Evidence: {r.evidence_summary}",
        ]
        if r.failure_reason:
            lines.append(f"- Failure: {r.failure_reason}")
        lines.append("")

    return "\n".join(lines)
