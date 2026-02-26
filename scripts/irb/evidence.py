"""evidence.py — Core data types for IRB v1 runner."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional


class CheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"


class Outcome(str, Enum):
    CERTIFIED = "CERTIFIED"
    FAILED = "FAILED"
    ERROR = "ERROR"


@dataclass
class CheckResult:
    id: str
    name: str
    category: str
    status: CheckStatus
    blocking: bool
    evidence_collected: bool
    evidence_summary: str
    failure_reason: Optional[str]


@dataclass
class RunSummary:
    total: int
    passed: int
    failed: int
    skipped: int
    blocking_failed: int


@dataclass
class RunReport:
    report_version: str
    spec_id: str
    spec_version: str
    target_project: str
    target_git_sha: str
    target_git_sha_8: str
    runner_timestamp: str
    runner_date: str
    outcome: Outcome
    summary: RunSummary
    checks: List[CheckResult]
    slug_source: str = "basename_fallback"
    output_md_path: Optional[Path] = None
    output_json_path: Optional[Path] = None
