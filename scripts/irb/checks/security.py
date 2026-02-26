"""checks/security.py — T15-SEC-001..002 implementations."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus
from scripts.irb.checks.hygiene import git_ls_files, _is_binary, _file_list_hash

MAX_SIZE = 2 * 1024 * 1024  # 2 MB


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


def _check_sec_001(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-SEC-001: no tracked file contains a PEM private key header marker."""
    spec_config = cache.get("spec_config", {})
    markers = spec_config.get("forbid_tracked_secret_markers", [])

    files = cache.get("T15:tracked_files") or git_ls_files(target)
    if files is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="git ls-files failed",
            failure_reason="Could not retrieve tracked file list",
        )

    file_hash = _file_list_hash(files)
    skipped_size = 0
    skipped_binary = 0
    match_count = 0
    found_markers: list[str] = []
    sample_files: list[str] = []

    for rel in files:
        abs_path = target / rel
        try:
            stat = abs_path.stat()
        except Exception:
            continue
        if stat.st_size > MAX_SIZE:
            skipped_size += 1
            continue
        if _is_binary(abs_path):
            skipped_binary += 1
            continue
        try:
            text = abs_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for marker in markers:
            if marker in text:
                match_count += 1
                if marker not in found_markers:
                    found_markers.append(marker)
                if rel not in sample_files and len(sample_files) < 5:
                    sample_files.append(rel)

    passed = match_count == 0
    summary = (
        f"tracked_files={len(files)}; file_list_hash={file_hash}; "
        f"markers_checked={len(markers)}; match_count={match_count}; "
        f"skipped_size={skipped_size}; skipped_binary={skipped_binary}"
    )
    if found_markers:
        summary += f"; found_markers={found_markers}; sample_files={sample_files}"

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"Private key marker(s) found in {len(sample_files)} tracked file(s): {sample_files}"
        ),
    )


def _check_sec_002(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-SEC-002: no tracked file contains a secret-like token regex match."""
    spec_config = cache.get("spec_config", {})
    regex_patterns = spec_config.get("forbid_tracked_secret_regexes", [])

    if not regex_patterns:
        return _make(
            check_def,
            status=CheckStatus.PASS,
            evidence_collected=True,
            evidence_summary="no regex patterns configured; nothing to scan",
        )

    try:
        compiled = [(p, re.compile(p)) for p in regex_patterns]
    except re.error as exc:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary=f"regex compile error: {exc}",
            failure_reason=str(exc),
        )

    files = cache.get("T15:tracked_files") or git_ls_files(target)
    if files is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="git ls-files failed",
            failure_reason="Could not retrieve tracked file list",
        )

    file_hash = _file_list_hash(files)
    skipped_size = 0
    skipped_binary = 0
    match_count = 0
    ignored_count = 0
    samples: list[str] = []

    FALSE_POSITIVE_MARKERS = ("<redacted>", "example", "fake")

    for rel in files:
        abs_path = target / rel
        try:
            stat = abs_path.stat()
        except Exception:
            continue
        if stat.st_size > MAX_SIZE:
            skipped_size += 1
            continue
        if _is_binary(abs_path):
            skipped_binary += 1
            continue
        try:
            text = abs_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            line_lower = line.lower()
            for pattern_str, pattern_re in compiled:
                if pattern_re.search(line):
                    # False-positive suppression
                    if any(fp in line_lower for fp in FALSE_POSITIVE_MARKERS):
                        ignored_count += 1
                        continue
                    match_count += 1
                    if len(samples) < 5:
                        samples.append(f"{rel}:{line_no} (pattern={pattern_str!r})")

    passed = match_count == 0
    summary = (
        f"tracked_files={len(files)}; file_list_hash={file_hash}; "
        f"patterns_checked={len(regex_patterns)}; match_count={match_count}; "
        f"ignored_count={ignored_count}; "
        f"skipped_size={skipped_size}; skipped_binary={skipped_binary}"
    )
    if samples:
        summary += f"; samples={samples}"

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"{match_count} secret-like token(s) detected: {samples[:3]}"
        ),
    )


def run_check(check_def: dict, target: Path, cache: dict) -> CheckResult:
    cid = check_def["id"]
    if cid == "T15-SEC-001":
        return _check_sec_001(check_def, target, cache)
    elif cid == "T15-SEC-002":
        return _check_sec_002(check_def, target, cache)
    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown security check id: {cid}",
        )
