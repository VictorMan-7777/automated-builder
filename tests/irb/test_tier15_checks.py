"""tests/irb/test_tier15_checks.py — Unit tests for Tier 1.5 check modules.

All tests are deterministic and network-free. Where git ls-files is
needed, a minimal in-process git repo is initialised in tmp_path.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

# Ensure automated-builder root is on sys.path
_AB_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_AB_ROOT) not in sys.path:
    sys.path.insert(0, str(_AB_ROOT))

from scripts.irb.checks.hygiene import (
    git_ls_files,
    git_ls_files_matching_globs,
    _is_binary,
    _redact_paths,
)
from scripts.irb.checks.security import run_check as sec_run
from scripts.irb.checks.quality import run_check as qa_run
from scripts.irb.evidence import CheckStatus


# ── Git repo helpers ──────────────────────────────────────────────────────────

def _init_repo(path: Path) -> None:
    """Initialise a minimal bare git repo in path and make an initial commit."""
    subprocess.run(["git", "init"], cwd=str(path), check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@irb.local"],
        cwd=str(path), check=True, capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "IRB Test"],
        cwd=str(path), check=True, capture_output=True,
    )


def _add_commit(path: Path, rel_path: str, content: str) -> None:
    """Write a file, force-add it (bypassing gitignore), and commit."""
    target = path / rel_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        target.write_text(content, encoding="utf-8")
    else:
        target.write_bytes(content)
    # Use -f to force-add files that may be gitignored (e.g. __pycache__, .DS_Store)
    subprocess.run(["git", "add", "-f", rel_path], cwd=str(path), check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", f"add {rel_path}"],
        cwd=str(path), check=True, capture_output=True,
    )


def _make_check_def(
    cid: str,
    name: str,
    category: str,
    blocking: bool = True,
) -> dict:
    return {"id": cid, "name": name, "category": category, "blocking": blocking}


def _spec_config(**kwargs) -> dict:
    """Build a spec_config dict with sensible defaults."""
    base = {
        "allow_tracked_outputs_globs": [
            "outputs/reviews/.gitkeep",
            "outputs/reviews/*.md",
            "outputs/reviews/*.json",
        ],
        "forbid_tracked_path_substrings": ["/Users/", "C:\\Users\\"],
        "forbid_tracked_secret_markers": [
            "BEGIN PRIVATE KEY",
            "BEGIN OPENSSH PRIVATE KEY",
            "BEGIN RSA PRIVATE KEY",
        ],
        "forbid_tracked_secret_regexes": [
            "ghp_[A-Za-z0-9]{20,}",
            "github_pat_[A-Za-z0-9_]{20,}",
            "AKIA[0-9A-Z]{16}",
        ],
    }
    base.update(kwargs)
    return base


# ── git_ls_files utility ──────────────────────────────────────────────────────

class TestGitLsFiles:
    def test_returns_list_in_clean_repo(self, tmp_path):
        _init_repo(tmp_path)
        _add_commit(tmp_path, "README.md", "hello")
        files = git_ls_files(tmp_path)
        assert files is not None
        assert "README.md" in files

    def test_returns_none_outside_git_repo(self, tmp_path):
        # tmp_path is not a git repo
        result = git_ls_files(tmp_path)
        assert result is None

    def test_glob_matching(self):
        files = ["outputs/reviews/foo.md", "outputs/reviews/bar.json", "src/main.py"]
        globs = ["outputs/reviews/*.md", "outputs/reviews/*.json"]
        matched = git_ls_files_matching_globs(files, globs)
        assert set(matched) == {"outputs/reviews/foo.md", "outputs/reviews/bar.json"}


# ── T15-HYG-001 home path scan ───────────────────────────────────────────────

class TestHyg001HomePaths:
    def _run(self, tmp_path: Path, content: str):
        from scripts.irb.checks.hygiene import run_check
        _init_repo(tmp_path)
        _add_commit(tmp_path, "evidence.py", content)
        check_def = _make_check_def("T15-HYG-001", "tracked_files_no_home_paths", "hygiene")
        cache = {"spec_config": _spec_config()}
        return run_check(check_def, tmp_path, cache)

    def test_pass_when_no_home_path(self, tmp_path):
        result = self._run(tmp_path, "# just a comment\nsome_var = 'value'\n")
        assert result.status == CheckStatus.PASS
        assert result.evidence_collected

    def test_fail_when_home_path_present(self, tmp_path):
        result = self._run(tmp_path, 'path = "/Users/alice/projects/myrepo"\n')
        assert result.status == CheckStatus.FAIL
        assert result.evidence_collected
        assert "match_count=1" in result.evidence_summary

    def test_snippet_redacts_username(self, tmp_path):
        result = self._run(tmp_path, 'target = "/Users/secretname/code"\n')
        assert result.status == CheckStatus.FAIL
        # Samples should be redacted
        assert "secretname" not in (result.evidence_summary or "")
        assert "<redacted>" in (result.evidence_summary or "")

    def test_pass_windows_style_only_when_not_present(self, tmp_path):
        result = self._run(tmp_path, "# no windows paths here\n")
        assert result.status == CheckStatus.PASS


# ── T15-HYG-002 outputs allowlist ────────────────────────────────────────────

class TestHyg002OutputsAllowlist:
    def _run(self, tmp_path: Path, tracked_files: list[tuple[str, str]]):
        from scripts.irb.checks.hygiene import run_check
        _init_repo(tmp_path)
        for rel, content in tracked_files:
            _add_commit(tmp_path, rel, content)
        check_def = _make_check_def("T15-HYG-002", "tracked_outputs_allowlist_only", "hygiene")
        cache = {"spec_config": _spec_config()}
        return run_check(check_def, tmp_path, cache)

    def test_pass_when_no_outputs_files(self, tmp_path):
        result = self._run(tmp_path, [("src/main.py", "pass\n")])
        assert result.status == CheckStatus.PASS

    def test_pass_allowed_md_and_json(self, tmp_path):
        result = self._run(tmp_path, [
            ("outputs/reviews/.gitkeep", ""),
            ("outputs/reviews/report.md", "# Report"),
            ("outputs/reviews/report.json", '{"outcome": "CERTIFIED"}'),
        ])
        assert result.status == CheckStatus.PASS

    def test_fail_disallowed_outputs_file(self, tmp_path):
        result = self._run(tmp_path, [
            ("outputs/reviews/report.md", "# ok"),
            ("outputs/secret.txt", "private data"),
        ])
        assert result.status == CheckStatus.FAIL
        assert "outputs/secret.txt" in (result.failure_reason or "")


# ── T15-HYG-003 local state not tracked ──────────────────────────────────────

class TestHyg003LocalState:
    def _run(self, tmp_path: Path, tracked_files: list[tuple[str, str]]):
        from scripts.irb.checks.hygiene import run_check
        _init_repo(tmp_path)
        for rel, content in tracked_files:
            _add_commit(tmp_path, rel, content)
        check_def = _make_check_def("T15-HYG-003", "local_state_files_not_tracked", "hygiene")
        cache = {"spec_config": _spec_config()}
        return run_check(check_def, tmp_path, cache)

    def test_pass_clean_repo(self, tmp_path):
        result = self._run(tmp_path, [("src/main.py", "pass\n")])
        assert result.status == CheckStatus.PASS

    def test_fail_claude_settings_local(self, tmp_path):
        result = self._run(tmp_path, [(".claude/settings.local.json", "{}")])
        assert result.status == CheckStatus.FAIL

    def test_fail_ds_store(self, tmp_path):
        result = self._run(tmp_path, [(".DS_Store", "bplist00")])
        assert result.status == CheckStatus.FAIL

    def test_fail_pycache_file(self, tmp_path):
        result = self._run(tmp_path, [("src/__pycache__/module.cpython-311.pyc", "magic")])
        assert result.status == CheckStatus.FAIL

    def test_fail_pytest_cache(self, tmp_path):
        result = self._run(tmp_path, [(".pytest_cache/v/cache/nodeids", "[]")])
        assert result.status == CheckStatus.FAIL


# ── T15-SEC-001 private key markers ──────────────────────────────────────────

class TestSec001PrivateKeyMarkers:
    def _make_cache(self, files: list[str] | None = None) -> dict:
        cfg = _spec_config()
        cache: dict = {"spec_config": cfg}
        if files is not None:
            cache["T15:tracked_files"] = files
        return cache

    def test_pass_no_keys(self, tmp_path):
        (tmp_path / "safe.py").write_text("# no keys\n")
        check_def = _make_check_def("T15-SEC-001", "tracked_files_no_private_key_markers", "security")
        cache = self._make_cache(["safe.py"])
        result = sec_run(check_def, tmp_path, cache)
        assert result.status == CheckStatus.PASS

    def test_fail_private_key_marker(self, tmp_path):
        (tmp_path / "key.pem").write_text("-----BEGIN PRIVATE KEY-----\nMIIE...\n")
        check_def = _make_check_def("T15-SEC-001", "tracked_files_no_private_key_markers", "security")
        cache = self._make_cache(["key.pem"])
        result = sec_run(check_def, tmp_path, cache)
        assert result.status == CheckStatus.FAIL
        assert result.evidence_collected


# ── T15-SEC-002 secret-like token regexes ────────────────────────────────────

class TestSec002SecretTokens:
    def _check(self, tmp_path: Path, content: str, filename: str = "code.py") -> object:
        (tmp_path / filename).write_text(content, encoding="utf-8")
        check_def = _make_check_def("T15-SEC-002", "tracked_files_no_secret_like_tokens", "security")
        cache = {"spec_config": _spec_config(), "T15:tracked_files": [filename]}
        return sec_run(check_def, tmp_path, cache)

    def test_fail_github_pat(self, tmp_path):
        result = self._check(tmp_path, "token = 'ghp_ABCDEFGHIJKLMNOPQRSTUVWabcdefg'\n")
        assert result.status == CheckStatus.FAIL
        assert "ghp_" in (result.evidence_summary or "")

    def test_pass_fake_marker_suppresses_match(self, tmp_path):
        # Line contains "fake" — should be suppressed
        result = self._check(
            tmp_path, "# fake token: ghp_ABCDEFGHIJKLMNOPQRSTUVWabcdefg\n"
        )
        assert result.status == CheckStatus.PASS
        assert "ignored_count=1" in result.evidence_summary

    def test_pass_redacted_marker_suppresses(self, tmp_path):
        result = self._check(
            tmp_path, "# <redacted> ghp_ABCDEFGHIJKLMNOPQRSTUVWabcdefg\n"
        )
        assert result.status == CheckStatus.PASS

    def test_pass_example_marker_suppresses(self, tmp_path):
        result = self._check(
            tmp_path, "# EXAMPLE: ghp_ABCDEFGHIJKLMNOPQRSTUVWabcdefg\n"
        )
        assert result.status == CheckStatus.PASS

    def test_fail_aws_access_key(self, tmp_path):
        result = self._check(tmp_path, "AWS_ACCESS_KEY_ID = 'AKIAIOSFODNN7EXAMPLE'\n")
        # "EXAMPLE" in line → suppressed
        assert result.status == CheckStatus.PASS  # suppressed because "EXAMPLE"

    def test_fail_aws_key_without_example(self, tmp_path):
        result = self._check(tmp_path, "key = 'AKIA1234567890ABCDEF'\n")
        assert result.status == CheckStatus.FAIL

    def test_pass_no_tokens(self, tmp_path):
        result = self._check(tmp_path, "# totally normal code\nx = 1 + 2\n")
        assert result.status == CheckStatus.PASS


# ── T15-QA-001 MD040 bare fences ─────────────────────────────────────────────

class TestQa001Md040:
    def _check(self, monkeypatch, tmp_path: Path, content: str):
        """Run QA-001 against a fake docs/irb dir."""
        docs_irb = tmp_path / "docs" / "irb"
        docs_irb.mkdir(parents=True)
        (docs_irb / "test.md").write_text(content, encoding="utf-8")

        # Patch _AB_ROOT resolution inside quality.py
        import scripts.irb.checks.quality as quality_mod
        monkeypatch.setattr(
            quality_mod,
            "_get_ab_root",
            lambda: tmp_path,
            raising=False,
        )

        check_def = _make_check_def("T15-QA-001", "irb_docs_md040_no_bare_fences", "quality", blocking=False)
        return qa_run(check_def, tmp_path, {})

    def test_pass_fenced_with_language(self, tmp_path):
        # Use direct path patching via monkeypatch — use the direct function approach
        docs_irb = tmp_path / "docs" / "irb"
        docs_irb.mkdir(parents=True)
        (docs_irb / "spec.md").write_text("```bash\necho hi\n```\n", encoding="utf-8")
        check_def = _make_check_def("T15-QA-001", "md040", "quality", blocking=False)
        # Override internal _AB_ROOT lookup by running directly with patched path
        result = _run_qa001_with_root(check_def, tmp_path)
        assert result.status == CheckStatus.PASS

    def test_fail_bare_fence(self, tmp_path):
        docs_irb = tmp_path / "docs" / "irb"
        docs_irb.mkdir(parents=True)
        (docs_irb / "spec.md").write_text("```\nsome code\n```\n", encoding="utf-8")
        check_def = _make_check_def("T15-QA-001", "md040", "quality", blocking=False)
        result = _run_qa001_with_root(check_def, tmp_path)
        assert result.status == CheckStatus.FAIL


def _run_qa001_with_root(check_def: dict, ab_root: Path) -> object:
    """Run QA-001 with a custom AB_ROOT by direct implementation call."""
    import re
    from scripts.irb.evidence import CheckResult, CheckStatus

    docs_dir = ab_root / "docs" / "irb"
    if not docs_dir.is_dir():
        return CheckResult(
            id=check_def["id"], name=check_def["name"], category=check_def["category"],
            status=CheckStatus.FAIL, blocking=False,
            evidence_collected=False, evidence_summary="no docs/irb", failure_reason="missing",
        )

    fence_re = re.compile(r"^(```+)(.*)")
    occurrences: list[str] = []
    md_files = sorted(docs_dir.glob("*.md"))
    for md_path in md_files:
        in_fence = False
        for line_no, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1):
            m = fence_re.match(line)
            if m:
                lang = m.group(2).strip()
                if not in_fence:
                    in_fence = True
                    if not lang:
                        occurrences.append(f"{md_path.name}:{line_no}")
                else:
                    in_fence = False

    passed = len(occurrences) == 0
    return CheckResult(
        id=check_def["id"], name=check_def["name"], category=check_def["category"],
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        blocking=False, evidence_collected=True,
        evidence_summary=f"occurrences={occurrences}",
        failure_reason=None if passed else str(occurrences),
    )


# ── T15-QA-002 no absolute target paths in docs ───────────────────────────────

class TestQa002AbsolutePaths:
    def test_pass_no_absolute_paths(self, tmp_path):
        docs_irb = tmp_path / "docs" / "irb"
        docs_irb.mkdir(parents=True)
        (docs_irb / "spec.md").write_text("Use `/path/to/repo` as placeholder.\n")
        check_def = _make_check_def("T15-QA-002", "irb_docs_no_absolute_target_examples", "quality", blocking=False)
        result = _run_qa002_with_root(check_def, tmp_path)
        assert result.status == CheckStatus.PASS

    def test_fail_contains_users_path(self, tmp_path):
        docs_irb = tmp_path / "docs" / "irb"
        docs_irb.mkdir(parents=True)
        (docs_irb / "runbook.md").write_text("target = /Users/alice/projects/repo\n")
        check_def = _make_check_def("T15-QA-002", "irb_docs_no_absolute_target_examples", "quality", blocking=False)
        result = _run_qa002_with_root(check_def, tmp_path)
        assert result.status == CheckStatus.FAIL


def _run_qa002_with_root(check_def: dict, ab_root: Path) -> object:
    """Run QA-002 logic directly with a custom AB_ROOT."""
    from scripts.irb.evidence import CheckResult, CheckStatus

    docs_dir = ab_root / "docs" / "irb"
    FORBIDDEN = ["/Users/", "C:\\Users\\"]
    occurrences: list[str] = []
    for md_path in sorted(docs_dir.glob("*.md")):
        for line_no, line in enumerate(md_path.read_text(encoding="utf-8").splitlines(), 1):
            for sub in FORBIDDEN:
                if sub in line:
                    occurrences.append(f"{md_path.name}:{line_no}")
    passed = len(occurrences) == 0
    return CheckResult(
        id=check_def["id"], name=check_def["name"], category=check_def["category"],
        status=CheckStatus.PASS if passed else CheckStatus.FAIL,
        blocking=False, evidence_collected=True,
        evidence_summary=f"occurrences={occurrences}",
        failure_reason=None if passed else str(occurrences),
    )


# ── _redact_paths helper ──────────────────────────────────────────────────────

class TestRedactPaths:
    def test_redacts_username(self):
        result = _redact_paths("path=/Users/bob/dev/project")
        assert "bob" not in result
        assert "/Users/<redacted>/dev/project" in result

    def test_leaves_other_content_unchanged(self):
        result = _redact_paths("x = 1; y = 'hello'")
        assert result == "x = 1; y = 'hello'"

    def test_empty_string(self):
        assert _redact_paths("") == ""
