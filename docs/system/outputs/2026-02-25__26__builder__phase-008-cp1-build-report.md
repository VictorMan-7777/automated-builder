# Phase 008 — CP1 Build Report: Controlled Grounding Activation

**Document**: `2026-02-25__26__builder__phase-008-cp1-build-report.md`
**Date**: 2026-02-25
**Phase**: 008 — Controlled Grounding Activation
**Commit Point**: CP1 — orchestrator resolution seam
**Commit**: `bb89c27`
**Status**: COMPLETE

---

## Deliverables

### Modified modules

| File | Changes |
|------|---------|
| `src/grounding_store/store.py` | Added `DEFAULT_ROOT: Path = _DEFAULT_ROOT` class attribute to `GroundingMapStore` for runtime-readable, monkeypatchable canonical path |
| `src/validation/orchestrator.py` | Added auto-resolution seam: loads `GroundingMap` from `GroundingMapStore(DEFAULT_ROOT)` when `grounding_map is None` and `exposition.grounding_map_id` is truthy; `KeyError` propagates on missing artifact |
| `src/generation/generators.py` | `grounding_map_id="gm-mock"` → `""` (both `MockSectionGenerator` and `FailFirstMockGenerator`) |
| `tests/fixtures/sample_devotional.py` | `grounding_map_id="gm-fixture-placeholder"` → `""` |
| `tests/validation/test_orchestrator.py` | `grounding_map_id="gm-test"` → `""` in `_day_with_exposition` helper |

### New test file

| File | Tests |
|------|-------|
| `tests/validation/test_grounding_activation.py` | 4 |

---

## Design Decisions Recorded

### Auto-Resolution Trigger

**Condition**: `if grounding_map is None and day.exposition.grounding_map_id:`

**Rationale**: Using `grounding_map is None` (not a sentinel) preserves the existing call convention. Callers that pass `grounding_map=loaded` explicitly are unaffected. Callers that pass `grounding_map=None` explicitly (e.g. `test_grounding_map_check_absent_when_not_provided`) are also unaffected — they must ensure `grounding_map_id=""` for the no-check behaviour to hold. The condition fires only when no map was provided AND a real id is set on the exposition.

### Placeholder id Cleanup

**Before**: `"gm-mock"`, `"gm-fixture-placeholder"`, `"gm-test"` — all truthy strings that would have accidentally triggered auto-resolution under the new rule.

**After**: `""` (empty string, always falsy) — semantically accurate: `MockSectionGenerator` and the test fixture don't have real grounding maps; the empty string signals this correctly.

**Backward compatibility**: All 480 pre-Phase-008 tests used these placeholder ids. Changing to `""` preserves every assertion since the `EXPOSITION_GROUNDING_MAP` check was always absent in those tests.

### `DEFAULT_ROOT` Class Attribute

**Before**: only `_DEFAULT_ROOT` module-level constant existed.

**After**: `GroundingMapStore.DEFAULT_ROOT = _DEFAULT_ROOT` class attribute added.

**Motivation**: The orchestrator instantiates `GroundingMapStore(root_dir=GroundingMapStore.DEFAULT_ROOT)`. This reads the class attribute **at call time**, not at import time, making `monkeypatch.setattr(GroundingMapStore, "DEFAULT_ROOT", tmp_path)` effective in tests. Module-level monkeypatching of `_DEFAULT_ROOT` is insufficient because Python binds default argument values at class-definition time.

### KeyError Propagation

No `try/except` added. `store.load()` raises `KeyError` when the artifact is absent; this propagates unmodified to the caller — confirmed by Test 3 (`TestIdPresentButMissing`).

---

## All 3 Required Behaviours Verified

| # | Required Behaviour | Test |
|---|--------------------|------|
| 1 | No id → no exception, check absent | `TestNoId::test_no_exception_when_grounding_map_id_is_empty` + `test_grounding_check_absent_when_no_id` |
| 2 | Id present and stored → check executes and passes | `TestIdPresentAndStored::test_grounding_check_executes_and_passes` |
| 3 | Id present but missing → KeyError propagates | `TestIdPresentButMissing::test_missing_artifact_raises_key_error` |

---

## Gate Results

| Gate | Result |
|------|--------|
| `pytest tests/ -q` (484 tests) | PASS |

---

## Cumulative Test Count After Phase 008 CP1

| Suite | Count |
|-------|-------|
| Python (prior — end of Phase 007 CP1) | 480 |
| Python (Phase 008 CP1) | +4 |
| Python total | 484 |
| TypeScript | 73 |
| **Grand Total** | **557** |

---

## Phase 008 CP1 HALT

**Do not wire RAG into `generate_devotional()`, implement `RealSectionGenerator`,
add scoring/evaluation, or begin Phase 009 without explicit operator instruction.**
