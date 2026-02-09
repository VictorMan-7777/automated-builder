# Fix A Proposal — Pending Approval

**Date:** 2026-02-09
**Status:** Pending approval
**Source:** Architecture Review Pass 1 (`2026-02-09__01__system__architecture-review-pass-1.md`), Finding 3
**Scope:** Single-file documentation fix

---

## Problem

The term "system iterator" appears in 5 governance documents as the authority for output filename generation:

| File | Line | Usage |
|------|------|-------|
| `docs/system/access.md` | 88 | "Output filenames are managed by the system iterator" |
| `docs/system/initial-prompt.md` | 77 | "Output filenames are managed by the system iterator" |
| `docs/implementation/system/checkpoint-taxonomy.md` | 251 | "Filename was supplied by the system iterator, not invented by the session" |
| `prompts/planner/run-planner.md` | 135 | "using the system iterator" |
| `prompts/builder/run-builder.md` | 151 | "the iterator controls naming" |

The naming convention rules exist in `docs/system/outputs/README.md` (lines 118-158) and are sufficient to deterministically compute a filename. But the term "system iterator" is never defined as "apply those rules." The result is an ambiguity: sessions cannot tell whether they are permitted to compute the filename themselves or must wait for an external authority. CP-7 (ARTIFACT-PRODUCE) checks that the "filename was supplied by the system iterator" — a check that is impossible to pass or fail when the iterator has no definition.

---

## Affected Files

**Primary change:**
- `docs/system/outputs/README.md` — Add a "System Iterator" definition section within or adjacent to the existing Naming Convention section (lines 114-158).

**No changes required to:**
- `docs/system/access.md` — References "the system iterator." Resolves once defined.
- `docs/system/initial-prompt.md` — Same.
- `docs/implementation/system/checkpoint-taxonomy.md` — Same. APPROVED document remains unmodified.
- `prompts/planner/run-planner.md` — Same.
- `prompts/builder/run-builder.md` — Same.

---

## Rule-Level Change

Add a definition to `docs/system/outputs/README.md` that establishes:

1. **The system iterator is the deterministic application of the naming convention rules already defined in `outputs/README.md`.** It is not a tool, not a human action, and not an external service.

2. **The algorithm:** Scan all existing files in `docs/system/outputs/`. For today's date (`YYYY-MM-DD`), find the highest existing `NN`. The next filename uses `NN+1` (zero-padded). If no files exist for today, `NN` = `01`. Context and description are determined by the session's role and task.

3. **Who executes it:** The session (assistant) applies the algorithm directly. No human confirmation of the filename is required. No external tool is invoked.

4. **What CP-7 verifies:** That the filename was produced by this algorithm (correct date, correct next `NN`, valid context, valid description format) — not that it was supplied by an external source.

This change defines an existing term. It does not alter the naming convention, the output compliance clause, or the checkpoint taxonomy. It closes the gap between "the rules exist" and "there is a named protocol that applies the rules."

---

## Acceptance Criteria

1. The term "system iterator" has an explicit definition in `docs/system/outputs/README.md`.
2. The definition is self-contained — a session reading only `outputs/README.md` can resolve the next filename without ambiguity.
3. The definition is consistent with the existing naming convention rules (no contradictions introduced).
4. All 5 documents that reference "the system iterator" resolve correctly against the new definition without requiring edits to those documents.
5. CP-7's verification criterion ("Filename sourced correctly — Filename was supplied by the system iterator, not invented by the session") becomes testable: the filename either follows the algorithm or it doesn't.

---

## Proposed Commit Message

```
docs(system): define system iterator protocol for output filenames
```

Single-purpose commit. One file modified (`docs/system/outputs/README.md`).
