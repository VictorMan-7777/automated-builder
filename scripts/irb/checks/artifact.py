"""checks/artifact.py — T1-ARTI-001..010 implementations.

R1 revision:
- ARTI-001..004: Code-level lifecycle invariants (source file + symbol existence).
- ARTI-005..006: Test-level lifecycle invariants derived from cached BUILD-002
  pytest output (TWEAK 1 — no separate pytest invocations).
- ARTI-007..010: Advisory runtime presence checks (non-blocking).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus
from scripts.irb.checks.build import PYTEST_CACHE_KEY


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


# ── Code lifecycle checks (ARTI-001..004) ────────────────────────────────────

def _check_source_present(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """Verify source file exists and contains required symbols."""
    evidence_path = check_def.get("evidence_path", "")
    required_symbols = check_def.get("required_symbols", [])
    file_path = target / evidence_path

    if not file_path.exists():
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=f"file={evidence_path}; exists=False",
            failure_reason=f"Source file not found: {evidence_path}",
        )

    content = file_path.read_text(encoding="utf-8")
    missing_symbols = [s for s in required_symbols if s not in content]
    passed = not missing_symbols
    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=(
            f"file={evidence_path}; "
            f"symbols_required={required_symbols}; "
            f"symbols_missing={missing_symbols}"
        ),
        failure_reason=(
            None if passed else f"Symbols not found in source: {missing_symbols}"
        ),
    )


# ── Test lifecycle checks (ARTI-005..006, derived from cache) ─────────────────

def _check_lifecycle_tests_from_cache(
    check_def: dict, target: Path, cache: dict
) -> CheckResult:
    """TWEAK 1: Derive lifecycle test evidence from the cached BUILD-002 run.

    Filters verbose pytest output lines for the specified test path.
    No separate pytest invocation — evidence comes from the single full run.
    """
    test_path_filter = check_def.get("evidence_test_path", "")
    cached = cache.get(PYTEST_CACHE_KEY)

    if cached is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=(
                "BUILD-002 pytest cache empty; cannot derive lifecycle test evidence"
            ),
            failure_reason="No cached pytest output (BUILD-002 must pass first)",
        )

    stdout = cached.get("stdout", "")
    all_lines = stdout.splitlines()

    # Filter lines that reference this test path (verbose pytest output)
    relevant_lines = [ln for ln in all_lines if test_path_filter in ln]

    if not relevant_lines:
        tail = "; ".join(all_lines[-5:]) if all_lines else "(empty)"
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=(
                f"test_path={test_path_filter!r}; "
                f"searched_lines={len(all_lines)}; matched=0; "
                f"tail={tail!r}"
            ),
            failure_reason=(
                f"No pytest output found for test path: {test_path_filter}"
            ),
        )

    passed_lines = [ln for ln in relevant_lines if " PASSED" in ln]
    failed_lines = [ln for ln in relevant_lines if " FAILED" in ln or " ERROR" in ln]
    passed_count = len(passed_lines)
    failed_count = len(failed_lines)

    if failed_count > 0:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=(
                f"test_path={test_path_filter}; "
                f"passed={passed_count}; failed={failed_count}; "
                f"failures={failed_lines[:3]}"
            ),
            failure_reason=f"{failed_count} test(s) failed in {test_path_filter}",
        )

    if passed_count == 0:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=True,
            evidence_summary=(
                f"test_path={test_path_filter}; "
                f"matched_lines={len(relevant_lines)}; "
                f"no PASSED lines; sample={relevant_lines[:3]}"
            ),
            failure_reason=(
                f"No PASSED tests in cached output for {test_path_filter}"
            ),
        )

    # Extract sample test names for evidence
    sample_names = []
    for ln in passed_lines[:5]:
        # pytest -v line format: "tests/grounding_store/test_foo.py::test_bar PASSED"
        parts = ln.strip().split(" ")
        if parts:
            sample_names.append(parts[0].split("::")[-1])

    return _make(
        check_def,
        status=CheckStatus.PASS,
        evidence_collected=True,
        evidence_summary=(
            f"test_path={test_path_filter}; "
            f"passed={passed_count}; failed={failed_count}; "
            f"sample_tests={sample_names}; "
            f"source=BUILD-002-cache"
        ),
        failure_reason=None,
    )


# ── Advisory runtime presence checks (ARTI-007..010) ─────────────────────────

def _check_advisory_path_exists(
    check_def: dict, target: Path, cache: dict
) -> CheckResult:
    evidence_path = check_def.get("evidence_path", "")
    p = target / evidence_path
    exists = p.exists()
    return _make(
        check_def,
        status=CheckStatus.PASS if exists else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=f"path={evidence_path}; exists={exists}",
        failure_reason=(
            None if exists else
            f"Runtime path not found: {evidence_path} (expected on clean clone)"
        ),
    )


def _check_advisory_file_count(
    check_def: dict, target: Path, cache: dict
) -> CheckResult:
    evidence_path = check_def.get("evidence_path", "")
    file_pattern = check_def.get("file_pattern", "*.json")
    p = target / evidence_path
    if not p.exists():
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=f"path={evidence_path}; dir_exists=False",
            failure_reason=f"Directory not found: {evidence_path}",
        )
    files = sorted(p.glob(file_pattern))
    count = len(files)
    passed = count >= 1
    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=(
            f"path={evidence_path}; pattern={file_pattern}; count={count}"
        ),
        failure_reason=(
            None if passed else
            f"0 files matching {file_pattern!r} in {evidence_path}"
        ),
    )


# ── Dispatch ──────────────────────────────────────────────────────────────────

_CODE_LIFECYCLE = {"T1-ARTI-001", "T1-ARTI-002", "T1-ARTI-003", "T1-ARTI-004"}
_TEST_LIFECYCLE = {"T1-ARTI-005", "T1-ARTI-006"}
_ADV_PATH = {"T1-ARTI-007", "T1-ARTI-009"}
_ADV_COUNT = {"T1-ARTI-008", "T1-ARTI-010"}


def run_check(check_def: dict, target: Path, cache: dict) -> CheckResult:
    cid = check_def["id"]
    if cid in _CODE_LIFECYCLE:
        return _check_source_present(check_def, target, cache)
    elif cid in _TEST_LIFECYCLE:
        return _check_lifecycle_tests_from_cache(check_def, target, cache)
    elif cid in _ADV_PATH:
        return _check_advisory_path_exists(check_def, target, cache)
    elif cid in _ADV_COUNT:
        return _check_advisory_file_count(check_def, target, cache)
    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown artifact check id: {cid}",
        )
