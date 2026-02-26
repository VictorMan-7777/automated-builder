"""checks/repo.py — T1-REPO-001..004 implementations."""
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus


def _run_git(args: list[str], cwd: Path) -> tuple[int, str, str]:
    """Run a git command. Returns (returncode, stdout, stderr)."""
    try:
        proc = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=15,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except FileNotFoundError:
        return -1, "", "git not found in PATH"
    except Exception as exc:
        return -2, "", str(exc)


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

    if cid == "T1-REPO-001":
        rc, out, err = _run_git(["rev-parse", "--is-inside-work-tree"], target)
        collected = rc >= 0
        passed = rc == 0
        return _make(
            check_def,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            evidence_collected=collected,
            evidence_summary=f"exit_code={rc}; stdout={out!r}",
            failure_reason=None if passed else f"git rev-parse returned {rc}: {err}",
        )

    elif cid == "T1-REPO-002":
        rc, out, err = _run_git(["log", "-1", "--format=%H"], target)
        collected = rc >= 0
        passed = rc == 0 and len(out) == 40
        # Cache git SHA for report filename
        if passed:
            cache["git_sha"] = out
        return _make(
            check_def,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            evidence_collected=collected,
            evidence_summary=f"sha={out[:8] if out else ''}...; len={len(out)}",
            failure_reason=None if passed else "HEAD SHA not readable or not 40 chars",
        )

    elif cid == "T1-REPO-003":
        p = target / "pyproject.toml"
        exists = p.exists()
        return _make(
            check_def,
            status=CheckStatus.PASS if exists else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=f"path=pyproject.toml; exists={exists}",
            failure_reason=None if exists else "pyproject.toml not found",
        )

    elif cid == "T1-REPO-004":
        rc, out, err = _run_git(["status", "--porcelain"], target)
        collected = rc >= 0
        clean = rc == 0 and out == ""
        n = len(out.splitlines()) if out else 0
        return _make(
            check_def,
            status=CheckStatus.PASS if clean else CheckStatus.FAIL,
            evidence_collected=collected,
            evidence_summary=f"dirty_files={n}",
            failure_reason=None if clean else f"Working tree dirty: {n} change(s)",
        )

    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown repo check id: {cid}",
        )
