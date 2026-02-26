"""checks/build.py — T1-BUILD-001..004 implementations.

R2: T1-BUILD-001 is non-blocking; records interpreter info.
    All pytest invocations use cache["python_exe"] (default sys.executable).
R3: Minimum test count threshold read from cache["spec_config"].
TWEAK 1: BUILD-002 runs pytest -v --tb=short; output cached for ARTI-005/006.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus

PYTEST_CACHE_KEY = "T1-BUILD-002:pytest_result"


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
    python_exe = cache.get("python_exe", sys.executable)

    if cid == "T1-BUILD-001":
        # R2: non-blocking; records interpreter path + version; checks pytest available.
        version_info = (
            f"{sys.version_info.major}.{sys.version_info.minor}"
            f".{sys.version_info.micro}"
        )
        try:
            proc = subprocess.run(
                [python_exe, "-m", "pytest", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            pytest_available = proc.returncode == 0
            pytest_ver = proc.stdout.strip().split("\n")[0] if proc.stdout else "unknown"
        except Exception as exc:
            pytest_available = False
            pytest_ver = str(exc)

        evidence = (
            f"python_exe={python_exe}; python_version={version_info}; "
            f"pytest_available={pytest_available}; pytest_version={pytest_ver!r}"
        )
        return _make(
            check_def,
            status=CheckStatus.PASS if pytest_available else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=evidence,
            failure_reason=(
                None if pytest_available else
                f"pytest not importable via {python_exe}: {pytest_ver}"
            ),
        )

    elif cid == "T1-BUILD-002":
        # TWEAK 1: run with -v --tb=short so output has per-test PASSED/FAILED lines.
        # This single run is cached for BUILD-003, BUILD-004, ARTI-005, ARTI-006.
        extra_args = cache.get("pytest_extra_args", [])
        cmd = [python_exe, "-m", "pytest", "tests/", "-v", "--tb=short"] + extra_args
        timeout = check_def.get("timeout_seconds", 300)
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(target),
                timeout=timeout,
            )
            cache[PYTEST_CACHE_KEY] = {
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "cmd": " ".join(cmd[:4]) + "...",
            }
            passed = proc.returncode == 0
            stdout_lines = len(proc.stdout.splitlines())
            evidence = (
                f"exit_code={proc.returncode}; stdout_lines={stdout_lines}; "
                f"cmd={' '.join(cmd[:4])}..."
            )
            return _make(
                check_def,
                status=CheckStatus.PASS if passed else CheckStatus.FAIL,
                evidence_collected=True,
                evidence_summary=evidence,
                failure_reason=None if passed else f"pytest exited {proc.returncode}",
            )
        except subprocess.TimeoutExpired:
            cache[PYTEST_CACHE_KEY] = None
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=False,
                evidence_summary=f"pytest timed out after {timeout}s",
                failure_reason=f"pytest timed out ({timeout}s)",
            )
        except Exception as exc:
            cache[PYTEST_CACHE_KEY] = None
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=False,
                evidence_summary=f"subprocess failed: {exc}",
                failure_reason=str(exc),
            )

    elif cid == "T1-BUILD-003":
        # R3: minimum from spec config (not hardcoded).
        cached = cache.get(PYTEST_CACHE_KEY)
        if cached is None:
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=False,
                evidence_summary="pytest cache empty — BUILD-002 did not run or failed",
                failure_reason="No cached pytest output",
            )
        stdout = cached.get("stdout", "")
        match = re.search(r"(\d+) passed", stdout)
        if match is None:
            # Parse failed — include excerpt for diagnostics
            lines = stdout.splitlines()
            summary_lines = [
                ln for ln in lines
                if any(kw in ln for kw in ("passed", "failed", "error", "warning"))
            ]
            excerpt = "; ".join(summary_lines[-5:]) if summary_lines else stdout[-300:]
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=True,
                evidence_summary=f"parse_failed=True; excerpt={excerpt!r}",
                failure_reason="Could not parse 'N passed' from pytest output",
            )
        count = int(match.group(1))
        spec_config = cache.get("spec_config", {})
        minimum = spec_config.get("minimum_passed_tests", 549)
        passed = count >= minimum
        return _make(
            check_def,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=f"parsed_count={count}; minimum={minimum}; sufficient={passed}",
            failure_reason=(
                None if passed else f"Only {count} tests passed; minimum is {minimum}"
            ),
        )

    elif cid == "T1-BUILD-004":
        cached = cache.get(PYTEST_CACHE_KEY)
        if cached is None:
            return _make(
                check_def,
                status=CheckStatus.FAIL,
                evidence_collected=False,
                evidence_summary="pytest cache empty",
                failure_reason="No cached pytest output",
            )
        stdout = cached.get("stdout", "")
        fail_match = re.search(r"(\d+) failed", stdout)
        error_match = re.search(r"(\d+) error", stdout)
        failed_count = int(fail_match.group(1)) if fail_match else 0
        error_count = int(error_match.group(1)) if error_match else 0
        passed = failed_count == 0 and error_count == 0
        return _make(
            check_def,
            status=CheckStatus.PASS if passed else CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=f"failed={failed_count}; errors={error_count}",
            failure_reason=(
                None if passed else
                f"pytest reported {failed_count} failures, {error_count} errors"
            ),
        )

    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown build check id: {cid}",
        )
