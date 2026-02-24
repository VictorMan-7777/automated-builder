# Phase 004.D — CP2 Build Report: Generation Orchestration Layer

**Document**: `2026-02-24__21__builder__phase-004d-cp2-build-report.md`
**Date**: 2026-02-24
**Phase**: 004.D — Generation Orchestration Layer (final sub-phase of Phase 4)
**Commit Point**: CP2 — Pipeline + Integration Tests
**Commit**: `9b094f9`
**Status**: COMPLETE

---

## Deliverables

### New entry point: `src/api/generation_pipeline.py`

```python
def generate_devotional(
    topic: str,
    num_days: int,
    scripture_reference: Optional[str] = None,
    output_mode: OutputMode = OutputMode.PERSONAL,
    generator: Optional[SectionGeneratorInterface] = None,
    registry: Optional[SeriesRegistry] = None,
    series_id: Optional[str] = None,
) -> PipelineResult:
```

Defaults: `generator` → `MockSectionGenerator()`; `registry` → `SeriesRegistry(db_path=Path(":memory:"))`.

Pipeline order per day (max 2 attempts):
1. `generator.generate_day(topic, day_number, attempt_number=attempt)`
2. `validate_daily_devotional(day, grounding_map=None, prayer_trace_map=None)`
3. Failures + attempt 1 → record `RewriteEvent(signal="auto_rewrite")`, retry with attempt 2
4. Failures + attempt 2 → record `RewriteEvent(signal="human_review")`, accept day
5. `registry.record_quote_use()` + `registry.record_scripture_use()` from accepted day

After loop: build `DevotionalBook` → `ExportGate.check_exportability()` → if exportable: `DocumentRenderer().render()` → `export_pdf(doc, output_mode.value)` → return `PipelineResult`.

### New test files

| File | Tests |
|------|-------|
| `tests/integration/__init__.py` | — |
| `tests/integration/test_pipeline.py` | 12 |

---

## Design Decisions Recorded

**OutputMode.value for export_pdf**: `DocumentRenderer.render()` receives the `OutputMode` enum; `export_pdf()` receives `output_mode.value` (the string literal `"personal"` or `"publish-ready"`). These are different call sites with different expected types.

**Subprocess avoidance in non-PDF tests**: Tests that don't assert on PDF bytes use `output_mode=OutputMode.PUBLISH_READY`. Since sections default to `SectionApprovalStatus.PENDING`, the export gate blocks and `export_pdf()` is never called. This makes those tests fast and deterministic regardless of `npx` availability.

**Module-scoped fixtures for PDF tests**: `personal_1_day` and `personal_3_day` are module-scoped; `export_pdf()` subprocess is invoked only twice for the entire integration test module regardless of how many tests use those fixtures.

**Retry loop termination**: `for attempt in range(1, 3)` (attempts 1 and 2). A `break` on success and explicit `if attempt == 2: accept day` on continued failure ensures the loop always terminates and `final_day` is always set.

**Registry scripture duplicates**: Multi-day generation using `MockSectionGenerator` reuses the same scripture reference across days (`Lamentations 3:22 / NASB`). `record_scripture_use()` is non-blocking on duplicates (returns `ScriptureUseResult.is_duplicate=True`); no exception raised.

---

## Test Results (CP2)

| Suite | New Tests | Result |
|-------|-----------|--------|
| `test_pipeline.py` | 12 | PASS |
| **CP2 total** | **12** | **ALL PASS** |

---

## CP2 Gate Results

| Gate | Result |
|------|--------|
| `pytest tests/pipeline/ tests/integration/ -v` (35 tests) | PASS |
| `pytest tests/ -q` (384 Python tests) | PASS |
| `pnpm test` (73 TypeScript tests) | PASS |
| `tsc --noEmit` | PASS (clean) |

---

## Cumulative Test Count After CP2

| Suite | Count |
|-------|-------|
| Python (prior — end of Phase 004) | 349 |
| Python (CP1) | +23 |
| Python (CP2) | +12 |
| Python total | 384 |
| TypeScript | 73 |
| **Grand Total** | **457** |

---

## Phase 004.D HALT

Phase 004.D is complete. The full generation orchestration layer is wired:
- Deterministic mock generation ✓
- Phase 004 validator loop with retry signals ✓
- Registry writes (quote + scripture) ✓
- Export gate (per-section PENDING check) ✓
- DocumentRenderer + PDF export ✓
- Full PipelineResult return ✓

**Do not proceed to real LLM generation, real RAG, scoring, or any new architectural layer without explicit operator instruction.**
