# Phase 007 — CP1 Build Report: Artifact Integrity Layer

**Document**: `2026-02-24__25__builder__phase-007-cp1-build-report.md`
**Date**: 2026-02-24
**Phase**: 007 — Artifact Integrity Layer (GroundingMap Lifecycle Hardening)
**Commit Point**: CP1 — id_policy + harness + storage convention hardening
**Commit**: `25c2cfc`
**Status**: COMPLETE

---

## Deliverables

### New modules

| File | Description |
|------|-------------|
| `src/grounding_store/id_policy.py` | `create_grounding_map_id()` — deterministic `"gm_<8-hex>"` id policy |
| `src/grounding_store/harness.py` | `validate_grounding_map_artifact()` — out-of-band validation harness |

### Updated module

| File | Changes |
|------|---------|
| `src/grounding_store/store.py` | `_DEFAULT_ROOT` anchored via `__file__`; `_SUBDIR` removed; `root_dir` is now the direct storage directory |

### New test files

| File | Tests |
|------|-------|
| `tests/grounding_store/test_id_policy.py` | 10 |
| `tests/grounding_store/test_harness.py` | 12 |
| `tests/grounding_store/test_storage_convention.py` | 12 |
| **CP1 total** | **34** |

---

## Design Decisions Recorded

### ID Policy (`id_policy.py`)

**Formula**: `f"gm_{hashlib.sha256(exposition_id.encode('utf-8')).hexdigest()[:8]}"`

**Output format**: `"gm_<8 lowercase hex chars>"` — 11 chars total.

**Properties**: deterministic, content-addressed, no time/random dependency, collision-resistant
for expected catalog sizes (2^32 = ~4 billion ids from 8-hex prefix).

**Forward-looking only**: existing GroundingMaps with random UUID ids (from `GroundingMapBuilder`)
are not retrofitted. `id_policy.py` is available for future use when real exposition_ids exist.

### Harness (`harness.py`)

**Design**: calls into existing `validate_exposition()` — no new validation rules. Uses a
deterministic 500-word stub `ExpositionSection` (`"grace"` × 500) that passes WORD_COUNT and
VOICE checks so the grounding check executes cleanly. Filters returned assessments to
`EXPOSITION_GROUNDING_MAP` only.

**Error surface**:
- `KeyError` if `grounding_map_id` not in store (from `store.load()`)
- `pydantic.ValidationError` if stored JSON fails model constraints (from `GroundingMap.model_validate()`)
- No swallowing of exceptions; errors surface to caller.

**Store immutability**: harness performs read-only operations; `save()` is never called. Verified
by `test_no_extra_files_created_in_store`.

### Storage Convention (`store.py` update)

**Before**: `_DEFAULT_ROOT = Path("data")` (CWD-relative); files at `data/grounding-maps/<id>.json`.

**After**: `_DEFAULT_ROOT = Path(__file__).parent.parent.parent / "data" / "artifacts" / "grounding_maps"` (absolute, `__file__`-anchored); files at `data/artifacts/grounding_maps/<id>.json`.

**Backward compatibility**: all existing Phase 006 tests inject `tmp_path` — unaffected by
default path change or `_SUBDIR` removal. 16 Phase 006 tests continue to pass.

**Note on `test_total_length_is_11`**: test corrected from 12 to 11 chars (`"gm_" = 3` + `8` hex chars = `11`). A test specification error, not an implementation error.

**Note on `test_default_store_dir_equals_default_root`**: monkeypatch approach discarded because
Python binds default argument values at class definition time, not at call time. Test now uses
`GroundingMapStore()._dir == _DEFAULT_ROOT` directly (creates canonical directory; intended
production side effect).

---

## All 10 Required Behaviours Verified

| # | Required Behaviour | Test |
|---|---------------------|------|
| 1 | Deterministic for same exposition_id | `TestDeterminism::test_same_input_returns_same_id` |
| 2 | Distinct for different exposition_ids | `TestDistinctness::test_different_ids_for_different_inputs` |
| 3 | Correct prefix and length | `TestFormat::test_full_format_matches_pattern` |
| 4 | Valid stored map → harness returns assessments | `TestValidStoredMap::test_valid_map_assessment_passes` |
| 5 | Missing id → KeyError | `TestMissingId::test_missing_id_raises_key_error` |
| 6 | Corrupted JSON → ValidationError | `TestCorruptedMap::test_corrupted_json_raises_validation_error` |
| 7 | Harness does not mutate store | `TestHarnessDoesNotMutateStore::test_no_extra_files_created_in_store` |
| 8 | DEFAULT_ROOT matches canonical structure | `TestDefaultRootStructure::test_canonical_tail_matches_exactly` |
| 9 | Default constructor uses canonical path | `TestCanonicalPathUsed::test_default_store_dir_equals_default_root` |
| 10 | Directory auto-created on construction | `TestDirectoryAutoCreated::test_nested_path_created_on_init` |

---

## Gate Results

| Gate | Result |
|------|--------|
| `pytest tests/grounding_store/ -v` (50 tests) | PASS |
| `pytest tests/ -q` (480 Python tests) | PASS |

---

## Cumulative Test Count After Phase 007 CP1

| Suite | Count |
|-------|-------|
| Python (prior — end of Phase 006 CP1) | 446 |
| Python (Phase 007 CP1) | +34 |
| Python total | 480 |
| TypeScript | 73 |
| **Grand Total** | **553** |

---

## Phase 007 CP1 HALT

**Do not wire GroundingMapStore or harness into `generate_devotional()`, implement
`RealSectionGenerator`, add scoring/evaluation, or begin Phase 008 without explicit operator
instruction.**
