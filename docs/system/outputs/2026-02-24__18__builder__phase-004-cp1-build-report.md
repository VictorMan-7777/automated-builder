# Phase 004 — CP1 Build Report: Deterministic Validation Layer

**Document**: `2026-02-24__18__builder__phase-004-cp1-build-report.md`
**Date**: 2026-02-24
**Phase**: 004 — Deterministic Validation Layer
**Commit Point**: CP1 — Validator Implementations
**Commit**: `405fb6e`
**Status**: COMPLETE

---

## Deliverables

### New schema: `src/models/validation.py`

| Class | Description |
|-------|-------------|
| `ValidatorAssessment` | `check_id`, `result` ("pass"/"fail"), `reason_code`, `explanation`, `evidence` — no AC ID coupling |
| `RewriteSignal` | Enum: `AUTO_REWRITE` / `HUMAN_REVIEW` |
| `RewriteDecision` | `signal`, `failed_assessments` — signal only, no content modification |

### New validation modules: `src/validation/`

| File | FR | Checks |
|------|----|--------|
| `modernization.py` | FR-56 | Archaic pronoun/verb/shifted-meaning substitution; modern negation phrases (shall not, will not) protected before substitution and restored after |
| `exposition.py` | FR-74 | `EXPOSITION_WORD_COUNT` (computed from text, not stored field), `EXPOSITION_VOICE` (second-person prohibited), `EXPOSITION_GROUNDING_MAP` (optional) |
| `be_still.py` | FR-75 | `BE_STILL_PROMPT_COUNT` (3–5), `BE_STILL_SECOND_PERSON` (at least one prompt must contain you/your) |
| `action_steps.py` | FR-76 | `ACTION_STEPS_COUNT` (1–3), `ACTION_STEPS_CONNECTOR_PHRASE` (non-empty) |
| `prayer.py` | FR-77 | `PRAYER_WORD_COUNT` (computed from text), `PRAYER_TRINITY_ADDRESS`, `PRAYER_TRACE_MAP` (optional) |
| `doctrinal.py` | §10.1/10.2 | Pattern-based: `DOCTRINAL_PROSPERITY` (prosperity gospel patterns), `DOCTRINAL_WORKS_MERIT` (works-merit patterns) |
| `rewrite_router.py` | FR-78 | `route(assessments, attempt_number)` → `RewriteDecision`; attempt 1 → `AUTO_REWRITE`; attempt ≥2 → `HUMAN_REVIEW`; no content modification |

---

## Design Decisions Recorded

**Word count**: All word counts computed via `len(section.text.split())`. The stored `section.word_count` field is NOT used — validator recomputes from text to remain independent of caller-supplied metadata.

**Exposition voice check**: `EXPOSITION_VOICE` is a prohibition check — presence of "you/your" in exposition text is the failure condition (communal voice required; second-person prohibited).

**Be Still second-person check**: At least one prompt must contain explicit "you/your" (not all prompts required, accommodating imperative forms like "Sit quietly..." which are grammatically second-person but lack the explicit pronoun).

**Modernization protection order**: Archaic forms ("shalt not", "wilt not") pass through verb substitution (shalt→shall, wilt→will) — this IS the desired transformation. Only modern forms ("shall not", "will not", etc.) are protected. Fix applied after initial test run revealed "shalt" was being blocked from substitution by an over-eager protected list.

**GroundingMap / PrayerTraceMap**: Validator accepts optional maps. If None, the corresponding check is omitted from results entirely (not reported as "skip"). Callers decide whether to provide them.

---

## Errors Encountered and Fixed

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `"thou shalt not kill"` → `"you shalt not kill"` (not "you shall not kill") | `"shalt not"` in protected phrases list blocked `"shalt"` → `"shall"` verb substitution | Removed archaic forms from protected list; only modern forms protected |
| `test_three_entries_fails` no assertions | Test tried to construct `GroundingMap` with 3 entries; model-level validator raises before validator is called | Rewrote test to use `pytest.raises(Exception)` |

---

## Test Results (CP1)

| Suite | New Tests | Result |
|-------|-----------|--------|
| `test_modernization.py` | 20 | PASS |
| `test_exposition_validator.py` | 20 | PASS |
| `test_be_still_validator.py` | 11 | PASS |
| `test_action_steps_validator.py` | 9 | PASS |
| `test_prayer_validator.py` | 20 | PASS |
| `test_doctrinal.py` | 16 | PASS |
| `test_rewrite_router.py` | 9 | PASS |
| **CP1 total** | **105** | **ALL PASS** |

Boundary tests confirmed:
- Exposition: 499 words → fail; 500 → pass; 700 → pass; 701 → fail
- Prayer: 119 words → fail; 120 → pass; 200 → pass; 201 → fail
- "shall not" → "shall not" (not "may not") ✓
- "thou shalt not" → "you shall not" ✓

---

## Cumulative Test Count After CP1

| Suite | Count |
|-------|-------|
| Python (prior phases) | 230 |
| Python (CP1) | +105 |
| TypeScript | 73 |
| **Total** | **408** |
