"""checks/hygiene.py — T15-HYG-001..003 implementations.

Shared utility: git_ls_files(target) → list of posix-relative tracked paths.
"""
from __future__ import annotations

import fnmatch
import hashlib
import re
import subprocess
from pathlib import Path
from typing import Optional

from scripts.irb.evidence import CheckResult, CheckStatus


# ── Shared utilities ──────────────────────────────────────────────────────────

def git_ls_files(target: Path) -> Optional[list[str]]:
    """Return NUL-delimited tracked file list as relative posix paths, or None on error."""
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"],
            capture_output=True,
            cwd=str(target),
            timeout=30,
        )
        if proc.returncode != 0:
            return None
        raw = proc.stdout.decode("utf-8", errors="replace")
        files = [f for f in raw.split("\0") if f]
        return files
    except Exception:
        return None


def git_ls_files_matching_globs(files: list[str], globs: list[str]) -> list[str]:
    """Return subset of files matching any of the given glob patterns (fnmatch)."""
    matched = []
    for f in files:
        if any(fnmatch.fnmatch(f, g) for g in globs):
            matched.append(f)
    return matched


def _file_list_hash(files: list[str]) -> str:
    """SHA-256 of the sorted, newline-joined file list (stable across runs)."""
    content = "\n".join(sorted(files))
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _is_binary(path: Path) -> bool:
    """True if the first 4 KB contains a NUL byte (heuristic binary check)."""
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(4096)
        return b"\x00" in chunk
    except Exception:
        return False


def _redact_paths(snippet: str) -> str:
    """Replace /Users/<name>/ with /Users/<redacted>/ in a snippet."""
    return re.sub(r"/Users/[^/\s]+/", "/Users/<redacted>/", snippet)


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


# ── Check implementations ─────────────────────────────────────────────────────

def _check_hyg_001(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-HYG-001: no tracked file contains a home-path substring."""
    spec_config = cache.get("spec_config", {})
    forbidden_substrings = spec_config.get("forbid_tracked_path_substrings", ["/Users/", "C:\\Users\\"])

    files = git_ls_files(target)
    if files is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="git ls-files failed",
            failure_reason="Could not retrieve tracked file list",
        )

    # Cache file list for other checks
    cache["T15:tracked_files"] = files
    file_hash = _file_list_hash(files)

    MAX_SIZE = 2 * 1024 * 1024  # 2 MB
    skipped_size = 0
    skipped_binary = 0
    match_count = 0
    samples: list[str] = []

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
            for sub in forbidden_substrings:
                if sub in line:
                    match_count += 1
                    if len(samples) < 5:
                        redacted = _redact_paths(line.strip()[:120])
                        samples.append(f"{rel}:{line_no}:{redacted}")

    passed = match_count == 0
    summary = (
        f"tracked_files={len(files)}; file_list_hash={file_hash}; "
        f"forbidden_substrings={forbidden_substrings}; "
        f"match_count={match_count}; "
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
            f"{match_count} occurrence(s) of forbidden path substrings in tracked files"
        ),
    )


def _check_hyg_002(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-HYG-002: all tracked outputs/ files match the allowlist."""
    spec_config = cache.get("spec_config", {})
    allow_globs = spec_config.get(
        "allow_tracked_outputs_globs",
        ["outputs/reviews/.gitkeep", "outputs/reviews/*.md", "outputs/reviews/*.json"],
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

    outputs_files = [f for f in files if f.startswith("outputs/")]
    allowed = git_ls_files_matching_globs(outputs_files, allow_globs)
    disallowed = [f for f in outputs_files if f not in allowed]

    passed = len(disallowed) == 0
    capped = disallowed[:20]
    overflow = len(disallowed) - 20 if len(disallowed) > 20 else 0
    disallowed_str = str(capped) + (f" +{overflow} more" if overflow else "")

    summary = (
        f"outputs_tracked={len(outputs_files)}; "
        f"allowed={len(allowed)}; disallowed={len(disallowed)}; "
        f"allow_globs={allow_globs}"
    )
    if disallowed:
        summary += f"; disallowed_files={disallowed_str}"

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"{len(disallowed)} tracked outputs/ file(s) not in allowlist: {capped}"
        ),
    )


def _check_hyg_003(check_def: dict, target: Path, cache: dict) -> CheckResult:
    """T15-HYG-003: no local-state files are tracked."""
    LOCAL_STATE_GLOBS = [
        ".claude/settings.local.json",
        ".DS_Store",
        "node_modules/**",
        "node_modules/*",
        ".pytest_cache/**",
        ".pytest_cache/*",
        "__pycache__/**",
        "__pycache__/*",
    ]

    files = cache.get("T15:tracked_files") or git_ls_files(target)
    if files is None:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="git ls-files failed",
            failure_reason="Could not retrieve tracked file list",
        )

    # Also match nested paths: any component matching the denylist patterns
    def _is_local_state(f: str) -> bool:
        parts = f.replace("\\", "/").split("/")
        # Exact match
        if any(fnmatch.fnmatch(f, g) for g in LOCAL_STATE_GLOBS):
            return True
        # Prefix match: node_modules, .pytest_cache, __pycache__ anywhere in path
        for i, part in enumerate(parts):
            prefix = "/".join(parts[:i + 1])
            if any(fnmatch.fnmatch(prefix, g.rstrip("/*")) for g in LOCAL_STATE_GLOBS):
                return True
        return False

    offending = [f for f in files if _is_local_state(f)]
    passed = len(offending) == 0

    summary = (
        f"tracked_files={len(files)}; "
        f"local_state_denylist_globs={LOCAL_STATE_GLOBS}; "
        f"offending_count={len(offending)}"
    )
    if offending:
        summary += f"; offending={offending[:20]}"

    return _make(
        check_def,
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        evidence_collected=True,
        evidence_summary=summary,
        failure_reason=(
            None if passed else
            f"{len(offending)} local-state file(s) are tracked: {offending[:5]}"
        ),
    )


# ── Dispatch ──────────────────────────────────────────────────────────────────

def run_check(check_def: dict, target: Path, cache: dict) -> CheckResult:
    cid = check_def["id"]
    if cid == "T15-HYG-001":
        return _check_hyg_001(check_def, target, cache)
    elif cid == "T15-HYG-002":
        return _check_hyg_002(check_def, target, cache)
    elif cid == "T15-HYG-003":
        return _check_hyg_003(check_def, target, cache)
    else:
        return _make(
            check_def,
            status=CheckStatus.FAIL,
            evidence_collected=False,
            evidence_summary="unknown check id",
            failure_reason=f"Unknown hygiene check id: {cid}",
        )
