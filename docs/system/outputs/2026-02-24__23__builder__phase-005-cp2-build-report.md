# Phase 005 — CP2 Build Report: RAG Infrastructure — ExpositionRAG + GroundingMapBuilder

**Document**: `2026-02-24__23__builder__phase-005-cp2-build-report.md`
**Date**: 2026-02-24
**Phase**: 005 — RAG Infrastructure
**Commit Point**: CP2 — ExpositionRAG + GroundingMapBuilder + Seed Excerpts + Unit Tests
**Commit**: `366662e`
**Status**: COMPLETE

---

## Deliverables

### New modules: `src/rag/exposition.py`, `src/rag/grounding.py`

| File | Description |
|------|-------------|
| `src/rag/exposition.py` | `ExpositionRAG` — concrete `ExpositionRAGInterface` implementation |
| `src/rag/grounding.py` | `GroundingMapBuilder` — assembles `GroundingMap` from per-paragraph excerpt lists |

### New data: `data/excerpts/seed-excerpts.json`

8 public-domain excerpts — **Matthew Henry, "Commentary on the Whole Bible"** (1706).
4 entries tagged `"paragraph_type": "context"` (historical/contextual commentary).
4 entries tagged `"paragraph_type": "theological"` (doctrinal commentary).
All entries: `source_type: "commentary"`, `author: "Matthew Henry"`.

### New test files

| File | Tests |
|------|-------|
| `tests/rag/test_exposition.py` | 12 |
| `tests/rag/test_grounding.py` | 15 |
| **CP2 total** | **27** |

---

## Design Decisions Recorded

**`ExpositionRAGInterface` structural compliance**: `ExpositionRAG` satisfies the Protocol via
structural subtyping. Confirmed in tests via `rag: ExpositionRAGInterface = ExpositionRAG()`.

**Filter logic — two-stage**:
1. Primary: `paragraph_type == requested AND source_type in source_types`
2. Fallback (when primary yields no results): `source_type in source_types` (ignores paragraph_type)

This ensures callers using non-standard paragraph_type labels (e.g. "declaration", "bridge") still
receive excerpts rather than an empty list, as long as source_types are valid.

**`source_types=[]` returns `[]` immediately** — short-circuits before any filtering. Guards
against callers passing an empty list without signalling an error.

**Determinism**: results returned in seed-file insertion order within each filtered set. No sorting
or randomisation applied.

**`paragraph_type` as metadata only**: The seed JSON schema includes `"paragraph_type"` for
filtering, but `RetrievedExcerpt` (from `src/interfaces/rag.py`) does not expose it. The field is
used internally during construction and stripped when building `RetrievedExcerpt` objects.

**GroundingMapBuilder — early ValueError**: Raises `ValueError` when any paragraph (1–4) is absent
from `paragraph_excerpts` or has an empty list, before Pydantic's `field_validator` is reached.
This produces a clearer error message than Pydantic's generic `ValidationError`.

**`sources_retrieved` deduplication**: Insertion-order deduplication via `seen: set`. Two excerpts
from the same `source_title` produce a single entry in `sources_retrieved`.

**`excerpts_used` truncation**: `e.text[:80]` used as excerpt identifier. Keeps
`GroundingMapEntry.excerpts_used` values concise while remaining human-readable.

**`how_retrieval_informed_paragraph`**: `f"Retrieved {N} excerpt(s) from {M} source(s)."` —
machine-readable, deterministic, satisfies the non-empty requirement of `GroundingMapEntry`.

**No pipeline wiring**: `generate_devotional()` unchanged. `MockSectionGenerator` unchanged.
No `RealSectionGenerator`. No `generate_devotional()` signature changes.

---

## Test Results (CP2)

| Suite | New Tests | Result |
|-------|-----------|--------|
| `tests/rag/test_exposition.py` | 12 | PASS |
| `tests/rag/test_grounding.py` | 15 | PASS |
| **CP2 total** | **27** | **ALL PASS** |

---

## CP2 Gate Results

| Gate | Result |
|------|--------|
| `pytest tests/rag/ -v` (46 tests) | PASS |
| `pytest tests/ -q` (430 Python tests) | PASS |

---

## Cumulative Test Count After CP2

| Suite | Count |
|-------|-------|
| Python (prior — end of Phase 005 CP1) | 403 |
| Python (Phase 005 CP2) | +27 |
| Python total | 430 |
| TypeScript | 73 |
| **Grand Total** | **503** |

---

## Phase 005 Complete — HALT

Phase 005 (RAG Infrastructure) is complete:
- `QuoteCatalog` (CP1) — concrete `QuoteRAGInterface`; 12 Oswald Chambers quotes ✓
- `ExpositionRAG` (CP2) — concrete `ExpositionRAGInterface`; 8 Matthew Henry excerpts ✓
- `GroundingMapBuilder` (CP2) — `GroundingMap` constructor from per-paragraph excerpts ✓
- 46 total RAG unit tests — all pass ✓

**Do not wire into `generate_devotional()`, create `RealSectionGenerator`, add scoring/evaluation, or proceed to any new architectural layer without explicit operator instruction.**
