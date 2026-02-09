# Architecture Review Pass 1 — Deferred / Unapproved Items Register

**Date:** 2026-02-09
**Source:** Architecture Review Pass 1 (`2026-02-09__01__system__architecture-review-pass-1.md`)
**Scope:** Items from Pass 1 that are explicitly labeled optional, deferrable, or low severity
**Status:** DEFERRED — Not required for Pass 1 completion

---

## Purpose

This register catalogs all items from Architecture Review Pass 1 that were
explicitly identified as optional, deferrable, or low severity. These items
were NOT part of the five required fixes (A–E) and are NOT required for
Pass 1 completion.

No new fixes are proposed. No governance rules are modified. This document
is a record only.

---

## Deferred Items

### Item 1 — Explicit Crosswalk Table (Taxonomy CPs vs Invocation Prompts)

**Source:** Pass 1, Section 6, Optional Improvement #1
**Related findings:** Finding 10 (MEDIUM), Finding 11
**Label:** Optional / Deferrable
**Status:** DEFERRED

Would create a mapping table between the 9 taxonomy checkpoints and the
step sequences in `run-planner.md` and `run-builder.md`. Makes the
"maps directly" claim in Section 6 (Compatibility Notes) of the taxonomy
independently verifiable.

Not required for Pass 1 completion.

---

### Item 2 — Add `audit` to Canonical Output Context List

**Source:** Pass 1, Section 6, Optional Improvement #2; Finding 5 (LOW)
**Label:** Optional / Deferrable / Low severity
**Status:** DEFERRED

Two existing output files use the context `audit`, which is not in the
canonical set (`planner | builder | gatekeeper | system`). Options: add
`audit` as a fifth canonical context, or re-categorize the two files.

Not required for Pass 1 completion.

---

### Item 3 — Fix `outputs/README.md` Compliance Section Old Naming Format

**Source:** Pass 1, Section 6, Optional Improvement #3; Finding 6 (LOW)
**Label:** Optional / Deferrable / Low severity
**Status:** DEFERRED

`outputs/README.md` line 371 references the pre-changelog naming format
(`YYYY-MM-DD-name.md`) instead of the canonical format
(`YYYY-MM-DD__NN__<context>__<description>.md`). The compliance section
is inconsistent with its own naming convention section.

Not required for Pass 1 completion.

---

### Item 4 — Changelog Entry for Checkpoint Taxonomy

**Source:** Pass 1, Section 6, Optional Improvement #4
**Label:** Optional / Deferrable
**Status:** DEFERRED

`docs/system/changelog.md` has no entry for the checkpoint taxonomy
addition (2026-02-07). Adding one would improve the system's own audit
trail.

Not required for Pass 1 completion.

---

### Item 5 — Clarify Single-Commit vs Multi-Commit Convention

**Source:** Pass 1, Section 6, Optional Improvement #5; Finding 12 (LOW)
**Label:** Optional / Deferrable / Low severity
**Status:** DEFERRED

The observed practice separates implementation artifacts from their output
records into distinct commits. `git.md` says "one logical change per commit"
without specifying whether the output artifact counts as the same logical
change or a separate one. Convention exists but is not codified.

Not required for Pass 1 completion.

---

### Item 6 — Consolidation of `run-planner.md` Duplicated Content

**Source:** Pass 1, Section 6, Optional Improvement #6
**Label:** Optional / Deferrable
**Status:** DEFERRED

`docs/system/run-planner.md` (system doc) and `prompts/planner/run-planner.md`
(invocation prompt) share overlapping content. The planner prompt references
the system doc as a prerequisite, but sections on output rules, iteration
procedure, and checklists appear in both. Creates maintenance overhead but
is not functionally broken.

Not required for Pass 1 completion.

---

## Summary

| # | Item | Severity | Label | Status |
|---|------|----------|-------|--------|
| 1 | Crosswalk table (CPs vs prompts) | — | Optional / Deferrable | DEFERRED |
| 2 | `audit` context canonicalization | LOW | Optional / Deferrable | DEFERRED |
| 3 | Compliance section old naming format | LOW | Optional / Deferrable | DEFERRED |
| 4 | Changelog entry for taxonomy | — | Optional / Deferrable | DEFERRED |
| 5 | Single vs multi-commit convention | LOW | Optional / Deferrable | DEFERRED |
| 6 | `run-planner.md` content consolidation | — | Optional / Deferrable | DEFERRED |

**Total deferred items:** 6
**Items required for Pass 1 completion:** 0

---

## Guardrail Statement

This register does not propose new fixes, recommend implementation, or
modify governance rules. It catalogs existing items from the Pass 1 review
that were explicitly labeled as optional or deferrable. Disposition of
these items is subject to future human instruction.
