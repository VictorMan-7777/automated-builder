"""checks/quality.py — T15-QA-001..003 implementations (all advisory)."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus


def _make(
    check_def: dict,
    status: CheckStatus,
    evidence_collected: bool,
    evidence_summary: str,
    failure_reason: Optional[str] = None,
) -> CheckResult:
    return CheckResult(
        id=check_def["id"],
        name=check_def["name"],
        category=check_def["category"],
        status=status,
        blocking=check_def.get("blocking", False),
        evidence_collected=evidence_collected,
        evidence_summary=evidence_summary,
        failure_reason=failure_reason,
    )


def _check_qa_001(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-QA-001: docs/irb/*.md must not have bare fenced code blocks (MD040)."""
    # Uses automated-builder docs, not target repo
    from pathlib import Path as _Path
    import sys
    _AB_ROOT = _Path(__file__).resolve().parent.parent.parent.parent
    docs_dir = _AB_ROOT / "docs" / "irb"

    if not docs_dir.is_dir():
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=f"docs/irb/ not found at {docs_dir}",
            failure_reason="docs/irb/ directory missing",
        )

    md_files = sorted(docs_dir.glob("*.md"))
    if not md_files:
        return _make(
            check_def,
            status=CheckStatus.PASS,
            evidence_collected=True,
            evidence_summary="no .md files in docs/irb/",
        )

    # MD040: flag opening fence lines with no language tag.
    # Closing fences (``` with no tag) are not violations — track fence state.
    fence_re = re.compile(r"^(```+)(.*)")
    occurrences: list[str] = []

    for md_path in md_files:
        try:
            lines = md_path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        in_fence = False
        for line_no, line in enumerate(lines, 1):
            m = fence_re.match(line)
            if m:
                lang = m.group(2).strip()
                if not in_fence:
                    # Opening fence — flag if no language tag
                    in_fence = True
                    if not lang and len(occurrences) < 10:
                        occurrences.append(f"docs/irb/{md_path.name}:{line_no}")
                else:
                    # Closing fence — reset state, never flag
                    in_fence = False

    passed = len(occurrences) == 0
    summary = (
        f"md_files_scanned={len(md_files)}; "
        f"bare_fence_occurrences={len(occurrences)}"
    )
    if occurrences:
        summary += f"; locations={occurrences}"

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"{len(occurrences)} bare ``` fence(s) found in docs/irb/*.md"
        ),
    )


def _check_qa_002(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-QA-002: docs/irb/*.md must not contain machine-local absolute paths."""
    from pathlib import Path as _Path
    _AB_ROOT = _Path(__file__).resolve().parent.parent.parent.parent
    docs_dir = _AB_ROOT / "docs" / "irb"

    if not docs_dir.is_dir():
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=f"docs/irb/ not found at {docs_dir}",
            failure_reason="docs/irb/ directory missing",
        )

    FORBIDDEN = ["/Users/", "C:\\Users\\"]
    md_files = sorted(docs_dir.glob("*.md"))
    occurrences: list[str] = []

    for md_path in md_files:
        try:
            lines = md_path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for line_no, line in enumerate(lines, 1):
            for sub in FORBIDDEN:
                if sub in line:
                    if len(occurrences) < 10:
                        occurrences.append(f"docs/irb/{md_path.name}:{line_no}")

    passed = len(occurrences) == 0
    summary = (
        f"md_files_scanned={len(md_files)}; "
        f"forbidden_count={len(FORBIDDEN)}; "
        f"occurrences={len(occurrences)}"
    )
    if occurrences:
        summary += f"; locations={occurrences}"

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"Machine-local path substring found in docs/irb/*.md: {occurrences}"
        ),
    )


def _check_qa_003(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-QA-003: reporter.py contains _sanitize_paths + build functions accept path args."""
    from pathlib import Path as _Path
    _AB_ROOT = _Path(__file__).resolve().parent.parent.parent.parent
    reporter_path = _AB_ROOT / "scripts" / "irb" / "reporter.py"

    if not reporter_path.is_file():
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="scripts/irb/reporter.py not found",
            failure_reason="reporter.py missing",
        )

    try:
        content = reporter_path.read_text(encoding="utf-8")
    except Exception as exc:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=f"could not read reporter.py: {exc}",
            failure_reason=str(exc),
        )

    REQUIRED_TOKENS = [
        "_sanitize_paths",
        "build_md_report",
        "build_json_report",
        "builder_root",
    ]
    missing = [t for t in REQUIRED_TOKENS if t not in content]
    passed = len(missing) == 0

    summary = (
        f"required_tokens={REQUIRED_TOKENS}; "
        f"missing={missing}; "
        f"reporter_size_bytes={len(content.encode())}"
    )

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"reporter.py missing required redaction tokens: {missing}"
        ),
    )


def run_check(check_def: dict, target: Path, cache: dict) -> CheckResult:
    cid = check_def["id"]
    if cid == "T15-QA-001":
        return _check_qa_001(check_def, target, cache)
    elif cid == "T15-QA-002":
        return _check_qa_002(check_def, target, cache)
    elif cid == "T15-QA-003":
        return _check_qa_003(check_def, target, cache)
    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown quality check id: {cid}",
        )
