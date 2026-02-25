# Phase 011 — CP1 Build Report: Deterministic Real Section Generator + Artifact Lifecycle Proof

**Document**: `2026-02-25__29__builder__phase-011-cp1-build-report.md`
**Date**: 2026-02-25
**Phase**: 011 — Deterministic Real Section Generator (No LLM)
**Commit Point**: CP1 — DeterministicRealSectionGenerator + artifact lifecycle proof
**Commit**: `049d908`
**Status**: COMPLETE

---

## Deliverables

### New modules

| File | Description |
|------|-------------|
| `src/generation/real_section_generator.py` | `DeterministicRealSectionGenerator` — no-LLM generator using ExpositionRAG + GroundingMapBuilder + GroundingMapStore |

### New test files

| File | Tests |
|------|-------|
| `tests/generation/__init__.py` | Empty package marker |
| `tests/generation/test_deterministic_real_section_generator.py` | 8 |

---

## Design Decisions Recorded

### DeterministicRealSectionGenerator

```python
class DeterministicRealSectionGenerator:
    def generate_day(
        self,
        topic: str,
        day_number: int,
        attempt_number: int = 1,
    ) -> DailyDevotional: ...
```

Conforms to `SectionGeneratorInterface` (structural Protocol). No `DEFAULT_STORE_ROOT`
class attribute needed — generator delegates to `GroundingMapStore.DEFAULT_ROOT` directly
at call-time, so tests monkeypatching `GroundingMapStore.DEFAULT_ROOT` redirect all layers
(generator, orchestrator, audit) simultaneously via a single patch.

### Grounding slot assignment

| Paragraph | Slot | Source |
|-----------|------|--------|
| 1 (declaration) | `first_excerpt` | First item of `excerpts_2 + excerpts_3` |
| 2 (context) | `excerpts_2` | `ExpositionRAG.retrieve_for_paragraph(paragraph_type="context", ...)` |
| 3 (theological) | `excerpts_3` | `ExpositionRAG.retrieve_for_paragraph(paragraph_type="theological", ...)` |
| 4 (bridge) | `first_excerpt` | Same as paragraph 1 |

### Deterministic id assignment

`exposition_id = f"expo-{topic}-day{day_number}"` → `create_grounding_map_id(exposition_id)` → `"gm_<8hex>"`.

`GroundingMapBuilder.build()` generates a UUID internally; the UUID is immediately
discarded via `gm.model_copy(update={"id": grounding_map_id})` to enforce the
deterministic id policy.

### Side-effect contract

`store.save(gm)` is called on every `generate_day()` invocation. Because the id is
deterministic, repeated calls for the same `(topic, day_number)` overwrite the same
file (idempotent). No new file accumulates.

### Exposition text

Reuses the same 550-word neutral theological word block (`"grace mercy faith..."`)
used by `MockSectionGenerator`. This satisfies `EXPOSITION_WORD_COUNT` (500–700)
and `EXPOSITION_VOICE` (no second-person). The "real" aspect of this generator is
the GroundingMap artifact, not the text.

---

## Lifecycle Proof — All 3 Required Behaviours Verified

| Test Class | Required Behaviour | Tests |
|------------|--------------------|-------|
| `TestArtifactCreated` | Generator creates and saves GroundingMap with 4 entries; id is truthy and deterministic | `test_creates_and_saves_grounding_map`, `test_grounding_map_has_four_entries`, `test_grounding_map_id_is_deterministic`, `test_different_inputs_produce_different_ids` |
| `TestOrchestratorIntegration` | `validate_daily_devotional(day)` auto-resolves artifact → EXPOSITION_GROUNDING_MAP present and passes | `test_exposition_grounding_map_check_present`, `test_exposition_grounding_map_check_passes` |
| `TestAuditIntegration` | `audit_devotionals([day])` → `grounding_status="pass"`, `prayer_trace_status="absent"` | `test_grounding_status_pass`, `test_prayer_trace_status_absent` |

---

## Gate Results

| Gate | Result |
|------|--------|
| `pytest tests/generation/ -v` (8 tests) | PASS |
| `pytest tests/ -q` (517 tests) | PASS |

---

## Cumulative Test Count After Phase 011 CP1

| Suite | Count |
|-------|-------|
| Python (prior — end of Phase 010 CP1) | 509 |
| Python (Phase 011 CP1) | +8 |
| Python total | 517 |
| TypeScript | 73 |
| **Grand Total** | **590** |

---

## Phase 011 CP1 HALT

**Do not wire `DeterministicRealSectionGenerator` into `generate_devotional()`,
implement `RealSectionGenerator` with LLM calls, add `PrayerTraceMapBuilder`,
or begin Phase 012 without explicit operator instruction.**
