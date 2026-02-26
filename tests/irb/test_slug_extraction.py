"""tests/irb/test_slug_extraction.py — Unit tests for get_project_slug() and helpers."""
from __future__ import annotations

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure automated-builder root is on sys.path so scripts.irb imports resolve.
_AB_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_AB_ROOT) not in sys.path:
    sys.path.insert(0, str(_AB_ROOT))

from scripts.irb.reporter import _parse_project_name_regex, get_project_slug


# ── _parse_project_name_regex helper ─────────────────────────────────────────

class TestParseProjectNameRegex:
    def test_double_quoted_name(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "my-project"\n', encoding="utf-8"
        )
        text = (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
        assert _parse_project_name_regex(text) == "my-project"

    def test_single_quoted_name(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            "[project]\nname = 'my-project'\n", encoding="utf-8"
        )
        text = (tmp_path / "pyproject.toml").read_text(encoding="utf-8")
        assert _parse_project_name_regex(text) == "my-project"

    def test_comment_lines_ignored(self, tmp_path):
        content = (
            "[project]\n"
            "# name = 'not-this'\n"
            'name = "real-name"\n'
        )
        assert _parse_project_name_regex(content) == "real-name"

    def test_stops_at_next_section(self, tmp_path):
        content = (
            "[project]\n"
            'name = "first-project"\n'
            "[tool.something]\n"
            'name = "second-project"\n'
        )
        assert _parse_project_name_regex(content) == "first-project"

    def test_no_project_section_returns_none(self):
        content = "[build-system]\nrequires = []\n"
        assert _parse_project_name_regex(content) is None

    def test_project_section_missing_name_returns_none(self):
        content = "[project]\nversion = '1.0'\n"
        assert _parse_project_name_regex(content) is None

    def test_inline_comment_after_name(self):
        content = '[project]\nname = "pkg" # inline comment\n'
        assert _parse_project_name_regex(content) == "pkg"


# ── get_project_slug — tier 1: tomllib (Python 3.11+ only) ───────────────────

@pytest.mark.skipif(sys.version_info < (3, 11), reason="tomllib stdlib requires Python 3.11+")
class TestGetProjectSlugTomllib:
    def test_reads_name_via_tomllib(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "devotional-generator"\n', encoding="utf-8"
        )
        slug, source = get_project_slug(tmp_path)
        assert slug == "devotional-generator"
        assert source == "tomllib"


# ── get_project_slug — tier 2: tomli backport ────────────────────────────────

class TestGetProjectSlugTomli:
    def test_reads_name_via_tomli_when_tomllib_absent(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "devotional-generator"\n', encoding="utf-8"
        )
        # Fake tomli module
        fake_tomli = types.ModuleType("tomli")
        fake_tomli.load = lambda fh: {"project": {"name": "devotional-generator"}}

        with patch.dict(sys.modules, {"tomllib": None, "tomli": fake_tomli}):
            slug, source = get_project_slug(tmp_path)

        assert slug == "devotional-generator"
        assert source == "tomli"


# ── get_project_slug — tier 3: regex fallback ────────────────────────────────

class TestGetProjectSlugFallbackRegex:
    def test_regex_fallback_when_no_toml_lib(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "my-lib"\n', encoding="utf-8"
        )
        # Block both tomllib and tomli
        with patch.dict(sys.modules, {"tomllib": None, "tomli": None}):
            slug, source = get_project_slug(tmp_path)

        assert slug == "my-lib"
        assert source == "fallback_regex"

    def test_regex_fallback_single_quotes(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            "[project]\nname = 'single-quote-pkg'\n", encoding="utf-8"
        )
        with patch.dict(sys.modules, {"tomllib": None, "tomli": None}):
            slug, source = get_project_slug(tmp_path)

        assert slug == "single-quote-pkg"
        assert source == "fallback_regex"


# ── get_project_slug — tier 4: basename fallback ─────────────────────────────

class TestGetProjectSlugBasenameFallback:
    def test_basename_when_pyproject_missing(self, tmp_path):
        # No pyproject.toml in tmp_path
        with patch.dict(sys.modules, {"tomllib": None, "tomli": None}):
            slug, source = get_project_slug(tmp_path)

        assert slug == tmp_path.name
        assert source == "basename_fallback"

    def test_basename_when_project_name_key_absent(self, tmp_path):
        (tmp_path / "pyproject.toml").write_text(
            "[build-system]\nrequires = []\n", encoding="utf-8"
        )
        with patch.dict(sys.modules, {"tomllib": None, "tomli": None}):
            slug, source = get_project_slug(tmp_path)

        assert slug == tmp_path.name
        assert source == "basename_fallback"
