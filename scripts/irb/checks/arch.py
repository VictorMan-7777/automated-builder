"""checks/arch.py — T1-ARCH-001..004 implementations.

R4: T1-ARCH-004 uses precise import + instantiation regex patterns,
    excluding comment lines, to avoid false positives.
"""
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
        blocking=check_def.get("blocking", True),
        evidence_collected=evidence_collected,
        evidence_summary=evidence_summary,
        failure_reason=failure_reason,
    )


def run_check(check_def: dict, target: Path, cache: dict) -> CheckResult:
    cid = check_def["id"]

    if cid == "T1-ARCH-001":
        src = target / "src"
        exists = src.is_dir()
        return _make(
            check_def,
            status=CheckStatus.PASS if exists else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=f"path=src/; is_dir={exists}",
            failure_reason=None if exists else "src/ directory not found",
        )

    elif cid == "T1-ARCH-002":
        src = target / "src"
        if not src.is_dir():
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=False,
                evidence_summary="src/ does not exist; cannot list",
                failure_reason="src/ directory absent",
            )
        required = check_def.get("required_entries", [])
        present = {p.name for p in src.iterdir() if p.is_dir()}
        missing = [m for m in required if m not in present]
        found = [r for r in required if r in present]
        passed = not missing
        return _make(
            check_def,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=(
                f"required={len(required)}; found={len(found)}; missing={missing}"
            ),
            failure_reason=None if passed else f"Missing src modules: {missing}",
        )

    elif cid == "T1-ARCH-003":
        p = target / "src" / "api" / "generation_pipeline.py"
        exists = p.exists()
        return _make(
            check_def,
            status=CheckStatus.PASS if exists else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=f"path=src/api/generation_pipeline.py; exists={exists}",
            failure_reason=None if exists else "generation_pipeline.py not found",
        )

    elif cid == "T1-ARCH-004":
        # R4: precise hard-halt — checks import statements and instantiation
        # calls only; excludes comment lines.
        evidence_file = check_def.get("evidence_file", "src/api/generation_pipeline.py")
        p = target / evidence_file
        if not p.exists():
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=False,
                evidence_summary=f"evidence_file={evidence_file}; not found",
                failure_reason=f"Evidence file not found: {evidence_file}",
            )

        content = p.read_text(encoding="utf-8")
        all_lines = content.splitlines()

        # Strip comment lines (lines whose first non-whitespace char is #)
        exclude_comments = check_def.get("exclude_comment_lines", True)
        if exclude_comments:
            non_comment_lines = [
                ln for ln in all_lines if not ln.lstrip().startswith("#")
            ]
        else:
            non_comment_lines = all_lines
        non_comment_content = "\n".join(non_comment_lines)

        forbidden_patterns = check_def.get("forbidden_patterns", [])
        violations = []
        for pat_def in forbidden_patterns:
            regex = pat_def["regex"]
            matches = re.findall(regex, non_comment_content, re.MULTILINE)
            if matches:
                violations.append({
                    "pattern": pat_def["name"],
                    "match_count": len(matches),
                    "first_match": str(matches[0])[:80],
                })

        passed = not violations
        evidence_summary = (
            f"file={evidence_file}; total_lines={len(all_lines)}; "
            f"non_comment_lines={len(non_comment_lines)}; "
            f"patterns_checked={len(forbidden_patterns)}; "
            f"violations={len(violations)}"
        )
        return _make(
            check_def,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=evidence_summary,
            failure_reason=(
                None if passed else
                f"Hard-halt violated: {[v['pattern'] for v in violations]}"
            ),
        )

    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown arch check id: {cid}",
        )
