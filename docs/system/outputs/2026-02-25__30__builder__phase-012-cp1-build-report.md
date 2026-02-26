# Build Report — Phase 012 CP1
**File:** `2026-02-25__30__builder__phase-012-cp1-build-report.md`
**Date:** 2026-02-26
**Phase:** 012 CP1 — Controlled LLM Exposition Generator
**Repo:** `devotional-generator-system-a`
**Commit:** `52a3869`
**Branch:** `main`
**Builder:** Claude Code / Sonnet 4.6

---

## Objective

Introduce LLM-backed exposition text generation while keeping all existing artifact infrastructure unchanged. Prayer generation remains deterministic. The orchestrator and audit layers required no modification — the new generator slots into the established grounding lifecycle by producing a truthy `grounding_map_id` that activates existing auto-resolution seams.

---

## Authorization

- Phase 012 CP1 authorized by operator instruction after:
  - Gatekeeper plan revision (removed `runtime_checkable`, enforced keyword `root_dir=`, structured FakeLLM output)
  - Gatekeeper Preflight Seam Integrity Audit (all sections A–E returned INFO only; no BLOCKER/WARNING)
  - `SAFE TO PROCEED` verdict confirmed

---

## Files Created

| File | Purpose |
|------|---------|
| `src/llm/__init__.py` | Module marker |
| `src/llm/interfaces.py` | `LLMClient` Protocol (no `runtime_checkable`) |
| `src/generation/llm_exposition_generator.py` | `LLMExpositionGenerator` — single-call LLM exposition with RAG grounding |
| `tests/generation/test_llm_exposition_generator.py` | 10 deterministic tests; `FakeLLMClient` stub; no network |

---

## Files NOT Modified

- `src/api/generation_pipeline.py` — pipeline unchanged; `generate_devotional()` still uses `MockSectionGenerator`
- `src/generation/generators.py` — unchanged
- All validation, store, model, and audit files — unchanged

---

## Implementation Notes

### LLMClient Protocol (`src/llm/interfaces.py`)
```python
from typing import Protocol

class LLMClient(Protocol):
    def generate(self, prompt: str) -> str: ...
```
No `runtime_checkable`. No concrete network implementation. Tests inject `FakeLLMClient`.

### LLMExpositionGenerator (`src/generation/llm_exposition_generator.py`)
- Constructor: `__init__(llm, rag=None, store=None)` — all dependencies injectable
- Method: `generate_exposition(exposition_id, topic, passage_reference) -> ExpositionSection`
- Step order: RAG retrieval → shortage fallback → GroundingMap build + persist → prompt build → single LLM call → ExpositionSection
- Store resolution: `GroundingMapStore(root_dir=GroundingMapStore.DEFAULT_ROOT)` at call-time when no store injected — monkeypatchable in tests
- RAG slot assignment: para1 and para4 reuse first available excerpt; para2 = context set; para3 = theological set
- Shortage fallback: synthetic `RetrievedExcerpt(source_title="RAG_SHORTAGE")` ensures GroundingMapBuilder always receives 4 non-empty slots
- GroundingMap id: `create_grounding_map_id(exposition_id)` — deterministic SHA-256, same id_policy as Phase 011
- `grounding_map_id` on returned `ExpositionSection` is always truthy
- `prayer_trace_map_id` not touched — remains `""` from MockSectionGenerator base

### Prompt (`_build_prompt`)
- Includes: `TOPIC`, `PASSAGE`, grounding instruction, up to 3 verbatim excerpt blocks from each RAG set (skipping RAG_SHORTAGE entries), required 4-paragraph structure (`declaration / context / theological / bridge`), target word count (500–650), voice rule (no "you"/"your")

### Test design (`FakeLLMClient`)
- Returns 4-paragraph fixed text, ~548 words, no "you"/"your"
- Passes: `EXPOSITION_WORD_COUNT`, `EXPOSITION_VOICE`, doctrinal guardrails
- `call_count` tracks invocation count

---

## Lifecycle Proof

```
LLMExpositionGenerator.generate_exposition()
  → ExpositionRAG.retrieve_for_paragraph() × 2          [deterministic seed data]
  → GroundingMapBuilder.build()                          [4-entry GroundingMap]
  → gm.model_copy(update={"id": create_grounding_map_id(exposition_id)})
  → GroundingMapStore(root_dir=GroundingMapStore.DEFAULT_ROOT).save(gm)
  → _build_prompt() + llm.generate()                    [single call]
  → ExpositionSection(grounding_map_id=<truthy>)

validate_daily_devotional(day)
  → sees truthy grounding_map_id
  → GroundingMapStore(root_dir=GroundingMapStore.DEFAULT_ROOT).load(id)  [auto-resolution]
  → validate_exposition(section, grounding_map=gm)
  → EXPOSITION_GROUNDING_MAP: pass

audit_devotionals([day])
  → _audit_grounding(grounding_map_id)
  → GroundingMapStore(root_dir=GroundingMapStore.DEFAULT_ROOT)  [same DEFAULT_ROOT]
  → grounding_status = "pass"
  → prayer_trace_status = "absent"  [prayer_trace_map_id = ""]
```

---

## Test Results

```
.venv/bin/pytest tests/ -q
527 passed in 33.62s
```

| Suite | Before | After | Delta |
|-------|--------|-------|-------|
| Python | 517 | 527 | +10 |
| TypeScript | 73 | 73 | 0 |
| **Total** | **590** | **600** | **+10** |

### New tests (10)

| Class | Test | Validates |
|-------|------|-----------|
| `TestGroundingMapPersisted` | `test_grounding_map_id_matches_id_policy` | id = SHA-256 of exposition_id |
| `TestGroundingMapPersisted` | `test_grounding_map_file_exists_in_store` | artifact persisted before return |
| `TestGroundingMapPersisted` | `test_grounding_map_has_four_entries` | exactly 4 GroundingMapEntry objects |
| `TestOrchestratorAutoResolution` | `test_prayer_trace_map_id_is_falsy` | prayer unchanged |
| `TestOrchestratorAutoResolution` | `test_exposition_grounding_map_check_present` | check_id emitted |
| `TestOrchestratorAutoResolution` | `test_exposition_grounding_map_check_passes` | result == "pass" |
| `TestAuditResult` | `test_grounding_status_pass` | audit sees pass |
| `TestAuditResult` | `test_prayer_trace_status_absent` | audit sees absent |
| `TestLLMCallCount` | `test_llm_called_exactly_once` | single call per invocation |
| `TestLLMCallCount` | `test_second_call_increments_count` | each call is independent |

---

## Invariants Confirmed

- `grounding_map_id=""` (falsy) remains the placeholder for no-artifact; only `LLMExpositionGenerator` sets truthy ids — never `MockSectionGenerator` or fixtures
- `GroundingMapStore.DEFAULT_ROOT` (class attribute) read at call-time — monkeypatching works correctly
- `_DEFAULT_ROOT` (module constant) is NOT the monkeypatch target — confirmed by `test_storage_convention.py` contract
- `generate_devotional()` pipeline untouched — `MockSectionGenerator` remains the default
- `prayer_trace_map_id` remains `""` throughout Phase 012 — no PrayerTraceMapBuilder wired

---

## Hard Halt Conditions (still active)

- Do NOT wire `LLMExpositionGenerator` into `generate_devotional()`
- Do NOT wire `DeterministicRealSectionGenerator` into `generate_devotional()`
- Do NOT implement `RealSectionGenerator` with LLM for prayer
- Do NOT add `PrayerTraceMapBuilder`
- Do NOT begin Phase 013 or any new architectural layer
- Await explicit operator authorization before any new phase

---

## Status

**HALT — Phase 012 CP1 complete.**
Awaiting operator instruction for Phase 013.
