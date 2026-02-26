"""executor.py — Check dispatch and orchestration.

TWEAK 2: Pre-run git status is captured before the check loop.
         Post-run git status is captured in a finally block so it
         always executes even if checks fail or raise.  Guard check
         runs after the finally block with both values available.
"""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus, Outcome


def _capture_git_status(target: Path) -> Optional[str]:
    """Run git status --porcelain. Returns stdout string, or None on error."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=str(target),
            timeout=15,
        )
        return proc.stdout
    except Exception:
        return None


def _make_skip(check_def: dict, reason: str) -> CheckResult:
    return CheckResult(
        id=check_def["id"],
        name=check_def["name"],
        category=check_def["category"],
        status=CheckStatus.SKIP,
        blocking=check_def.get("blocking", False),
        evidence_collected=False,
        evidence_summary="",
        failure_reason=reason,
    )


def _dispatch_check(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """Route to category check module. Catches and wraps unexpected exceptions."""
    category = check_def.get("category", "")
    try:
        if category == "repo":
            from scripts.irb.checks.repo import run_check
        elif category == "arch":
            from scripts.irb.checks.arch import run_check
        elif category == "build":
            from scripts.irb.checks.build import run_check
        elif category == "artifact":
            from scripts.irb.checks.artifact import run_check
        else:
            raise ValueError(f"Unknown category: {category!r}")
        return run_check(check_def, target, cache)
    except Exception as exc:
        return CheckResult(
            id=check_def["id"],
            name=check_def.get("name", check_def["id"]),
            category=category,
            status=CheckStatus.FAIL,
            blocking=check_def.get("blocking", False),
            evidence_collected=False,
            evidence_summary=f"dispatch raised exception: {type(exc).__name__}: {exc}",
            failure_reason=str(exc),
        )


def run_all_checks(spec: dict, target: Path, cache: dict) -> list[CheckResult]:
    """Execute all checks in spec order.

    Guard check always runs:
    - Pre-run git status captured before the loop.
    - Post-run git status captured in finally (TWEAK 2).
    - Guard check dispatched after finally so both statuses are available.
    """
    guard_defs = [c for c in spec["checks"] if c.get("category") == "guard"]
    regular_defs = [c for c in spec["checks"] if c.get("category") != "guard"]

    # TWEAK 2: Capture pre-run git status before any checks run
    cache["git_status_before"] = _capture_git_status(target)

    results: dict[str, CheckResult] = {}

    try:
        for check_def in regular_defs:
            cid = check_def["id"]
            dep = check_def.get("depends_on")
            if dep and dep in results and results[dep].status != CheckStatus.PASS:
                results[cid] = _make_skip(
                    check_def, f"dependency {dep!r} did not PASS"
                )
                continue
            results[cid] = _dispatch_check(check_def, target, cache)
    finally:
        # TWEAK 2: Always capture post-run git status
        cache["git_status_after"] = _capture_git_status(target)

    # Guard check(s) run after finally — both statuses are now in cache
    for guard_def in guard_defs:
        try:
            from scripts.irb.checks.guard import run_check as guard_run
            guard_result = guard_run(guard_def, target, cache)
        except Exception as exc:
            guard_result = CheckResult(
                id=guard_def["id"],
                name=guard_def.get("name", "repo_mutation_guard"),
                category="guard",
                status=CheckStatus.FAIL,
                blocking=guard_def.get("blocking", True),
                evidence_collected=False,
                evidence_summary=f"guard raised exception: {exc}",
                failure_reason=str(exc),
            )
        results[guard_def["id"]] = guard_result

    # Return in spec order; skip any check_id not in results (shouldn't happen)
    return [results[c["id"]] for c in spec["checks"] if c["id"] in results]


def determine_outcome(results: list[CheckResult]) -> Outcome:
    """CERTIFIED if no blocking check failed."""
    for r in results:
        if r.blocking and r.status == CheckStatus.FAIL:
            return Outcome.FAILED
    return Outcome.CERTIFIED
