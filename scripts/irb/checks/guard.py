"""checks/guard.py — T1-GUARD-001 repo mutation guard.

R5: Compares git status --porcelain captured before all checks
    (cache["git_status_before"]) vs. after all checks
    (cache["git_status_after"]).  The executor populates both via
    try/finally so the guard always has data to compare.
"""
from __future__ import annotations

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
    before = cache.get("git_status_before")
    after = cache.get("git_status_after")

    if before is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="git_status_before not captured",
            failure_reason="Pre-run git status was not captured",
        )
    if after is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="git_status_after not captured",
            failure_reason="Post-run git status was not captured",
        )

    no_delta = before == after
    # Trim for evidence summary (avoid huge diffs in the report)
    before_repr = repr(before[:200]) if before else "''"
    after_repr = repr(after[:200]) if after else "''"

    return _make(
        check_def,
        status=CheckStatus.PASS if no_delta else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=(
            f"no_delta={no_delta}; "
            f"before={before_repr}; "
            f"after={after_repr}"
        ),
        failure_reason=(
            None if no_delta else
            "Target repo was modified during check run"
        ),
    )
