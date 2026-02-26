#!/usr/bin/env python3
"""runner.py — IRB CLI entry point.

Usage:
    python3 scripts/irb/runner.py review --tier 1 --target /path/to/repo
    scripts/irb/builder review --tier 1 --target /path/to/repo

Exit codes:
    0  CERTIFIED  — all blocking checks pass
    1  FAILED     — one or more blocking checks fail
    2  ERROR      — runner crashed before producing a report
"""
from __future__ import annotations

import sys
from pathlib import Path

# Add automated-builder root to sys.path so 'scripts.irb.*' imports resolve.
# scripts/irb/runner.py → scripts/irb/ → scripts/ → automated-builder/
_AB_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_AB_ROOT) not in sys.path:
    sys.path.insert(0, str(_AB_ROOT))

import argparse
import datetime
import json
import shlex

EXIT_CERTIFIED = 0
EXIT_FAILED = 1
EXIT_ERROR = 2


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="irb-runner",
        description="IRB certification runner",
    )
    sub = parser.add_subparsers(dest="command")

    review_cmd = sub.add_parser("review", help="Run a certification tier review")
    review_cmd.add_argument(
        "--tier", type=int, required=True, help="Tier number (e.g. 1)"
    )
    review_cmd.add_argument(
        "--target", required=True, help="Absolute path to the target repository"
    )
    review_cmd.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for reports. Default: outputs/reviews/ in automated-builder",
    )
    review_cmd.add_argument(
        "--spec",
        default=None,
        help="Path to spec YAML. Default: specs/irb/tier-<N>-spec.yaml",
    )
    review_cmd.add_argument(
        "--python",
        dest="python_exe",
        default=None,
        help="Python interpreter for running tests. Default: sys.executable",
    )
    review_cmd.add_argument(
        "--pytest-args",
        default="",
        help="Extra arguments passed to pytest (space-separated string)",
    )

    args = parser.parse_args()

    if args.command != "review":
        parser.print_help()
        return EXIT_ERROR

    target = Path(args.target).resolve()
    if not target.exists():
        print(f"ERROR: target path does not exist: {target}", file=sys.stderr)
        return EXIT_ERROR
    if not target.is_dir():
        print(f"ERROR: target path is not a directory: {target}", file=sys.stderr)
        return EXIT_ERROR

    spec_path = (
        Path(args.spec).resolve()
        if args.spec
        else _AB_ROOT / "specs" / "irb" / f"tier-{args.tier}-spec.yaml"
    )
    if not spec_path.exists():
        print(f"ERROR: spec not found: {spec_path}", file=sys.stderr)
        return EXIT_ERROR
    if not spec_path.is_file():
        print(f"ERROR: spec path is not a file: {spec_path}", file=sys.stderr)
        return EXIT_ERROR

    output_dir = (
        Path(args.output_dir).resolve()
        if args.output_dir
        else _AB_ROOT / "outputs" / "reviews"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    python_exe = args.python_exe or sys.executable
    pytest_extra_args = shlex.split(args.pytest_args) if args.pytest_args else []

    try:
        return _run(target, spec_path, output_dir, args.tier, python_exe, pytest_extra_args)
    except Exception as exc:
        import traceback
        print(f"ERROR: runner crashed: {exc}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        return EXIT_ERROR


def _run(
    target: Path,
    spec_path: Path,
    output_dir: Path,
    tier: int,
    python_exe: str,
    pytest_extra_args: list[str],
) -> int:
    from scripts.irb.loader import load_spec
    from scripts.irb.executor import run_all_checks, determine_outcome
    from scripts.irb.evidence import CheckStatus, Outcome, RunReport, RunSummary
    from scripts.irb.reporter import (
        get_project_slug,
        compute_report_filename,
        build_md_report,
        build_json_report,
    )

    spec = load_spec(spec_path)
    spec_config = spec.get("config", {})

    cache: dict = {
        "python_exe": python_exe,
        "pytest_extra_args": pytest_extra_args,
        "spec_config": spec_config,
    }

    results = run_all_checks(spec, target, cache)
    outcome = determine_outcome(results)

    now_utc = datetime.datetime.utcnow()
    runner_date = now_utc.strftime("%Y-%m-%d")
    runner_timestamp = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    git_sha = cache.get("git_sha", "")
    git_sha_8 = git_sha[:8] if git_sha else "00000000"
    project_slug, slug_source = get_project_slug(target)

    total = len(results)
    passed = sum(1 for r in results if r.status == CheckStatus.PASS)
    failed = sum(1 for r in results if r.status == CheckStatus.FAIL)
    skipped = sum(1 for r in results if r.status == CheckStatus.SKIP)
    blocking_failed = sum(
        1 for r in results if r.status == CheckStatus.FAIL and r.blocking
    )

    report = RunReport(
        report_version="1.0.0",
        spec_id=spec["spec_id"],
        spec_version=spec["spec_version"],
        target_project=project_slug,
        target_git_sha=git_sha,
        target_git_sha_8=git_sha_8,
        runner_timestamp=runner_timestamp,
        runner_date=runner_date,
        outcome=outcome,
        summary=RunSummary(
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            blocking_failed=blocking_failed,
        ),
        checks=results,
        slug_source=slug_source,
    )

    md_fn, json_fn = compute_report_filename(project_slug, tier, git_sha_8, runner_date)
    md_path = output_dir / md_fn
    json_path = output_dir / json_fn

    md_path.write_text(build_md_report(report, tier, target, _AB_ROOT), encoding="utf-8")
    json_path.write_text(
        json.dumps(build_json_report(report, target, _AB_ROOT), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    report.output_md_path = md_path
    report.output_json_path = json_path

    print(f"\nIRB Tier-{tier} complete")
    print(f"Outcome:         {outcome.value}")
    print(f"Total checks:    {total}")
    print(f"Passed:          {passed}")
    print(f"Failed:          {failed}")
    print(f"Skipped:         {skipped}")
    print(f"Blocking failed: {blocking_failed}")
    print(f"\nReport (MD):   {md_path}")
    print(f"Report (JSON): {json_path}")

    return EXIT_CERTIFIED if outcome == Outcome.CERTIFIED else EXIT_FAILED


if __name__ == "__main__":
    sys.exit(main())
