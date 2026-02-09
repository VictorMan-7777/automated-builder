# Approval Decision — access.md Governance Updates

**Date:** 2026-02-09
**Status:** APPROVED
**Scope:** Minimal changes to `docs/system/access.md` to reflect Fixes A–E
**Authority:** Human approval (Objective 2a)
**Prerequisites:** Architecture Review Pass 1 VERIFIED COMPLETE (all 5 fixes passed)

---

## Context

Fixes A–E are authoritative and verified:

| Fix | Description | Commit |
|-----|-------------|--------|
| Fix A | Define system iterator protocol | `b677369` |
| Fix B | Resolve sequence number scoping contradiction | `7b66714` |
| Fix C | Expand default governance file list | `586d740` |
| Fix D | Resolve planner command prohibition vs checkpoint requirements | `539df5b` |
| Fix E | Formalize interrupted-session artifact path | `25a30e7` |

Verification: `2026-02-09__13__system__pass-1-verification.md` — 5/5 PASS, 0 contradictions.

A change proposal was produced identifying 5 minimal updates to `access.md`.
The proposal was reviewed and approved by the human operator.

---

## Approved Change List

### Change 1 — Preamble: Governance-lock acknowledgment

**Location:** After line 9 (before the `---` at line 13)

**Action:** Add the following line:

> This file is governance-locked by default under CP-2 (see `docs/implementation/system/checkpoint-taxonomy.md`). Sessions read this file for integrity baselining; this does not constitute behavioral use.

**Fix reference:** Fix C — `access.md` added to CP-2 default governance lock list (taxonomy line 108).

---

### Change 2 — Output requirement rule: Expand artifact types

**Location:** Lines 74–77

**Action:** Replace the artifact type enumeration. Add "interruption report" and "gap report" to the list.

**Current:**
> "...defined as a plan, audit, decision, governance guidance document, build report, or review..."

**Approved replacement:**
> "...defined as a plan, audit, decision, governance guidance document, build report, review, interruption report, or gap report..."

**Fix reference:** Fix E — Section 3.4 of checkpoint taxonomy introduces interruption reports (Section 3.4.1) and gap reports (Section 3.4.2).

---

### Change 3 — Output compliance clause: Interrupted session qualification

**Location:** After line 82 (before "This is enforced by...")

**Action:** Add the following paragraph:

> For interrupted sessions — sessions that terminate before CP-9 records a PASS — the output obligation is satisfied via the exception path defined in the checkpoint taxonomy (Section 3.4). An interrupted session that produces an interruption artifact via CP-7 out-of-order satisfies this clause. Post-termination recovery artifacts are governed by Section 3.4.2 of the checkpoint taxonomy and are not subject to in-session confirmation.

**Fix reference:** Fix E — Section 3.4.1 (in-session exception path) and Section 3.4.2 (post-termination recovery).

---

### Change 4 — System iterator cross-reference

**Location:** Line 88

**Action:** Add parenthetical cross-reference to the system iterator definition.

**Current:**
> "Output filenames are managed by the system iterator and must not be chosen or suggested by the assistant."

**Approved replacement:**
> "Output filenames are managed by the system iterator (defined in `docs/system/outputs/README.md`) and must not be chosen or suggested by the assistant."

**Fix reference:** Fix A — System iterator formally defined in `outputs/README.md` lines 160–184.

---

### Change 5 — Authority Boundary: Add checkpoint taxonomy reference

**Location:** Lines 98–101

**Action:** Replace the authority boundary section text.

**Current:**
> "Access mode behavior is enforced by the session authority header.
> This document must not be used to infer permissions or justify actions
> outside the declared session mode."

**Approved replacement:**
> "Access mode behavior is enforced by the session authority header
> (`docs/system/initial-prompt.md`). The session lifecycle — including
> checkpoint ordering, governance locking, artifact production, and commit
> validation — is governed by the checkpoint taxonomy
> (`docs/implementation/system/checkpoint-taxonomy.md`).
>
> This document must not be used to infer permissions or justify actions
> outside the declared session mode."

**Fix reference:** Fixes A–E collectively — the checkpoint taxonomy is now the verified execution contract. CP-7 enforces output rules, CP-2 enforces governance locking, Section 3.4 handles interrupted sessions.

---

## Boundaries

- These 5 changes are the complete approved scope. No other changes to `access.md`.
- No new rules introduced. All changes reference existing, verified fixes.
- No duplication of checkpoint taxonomy content (references only).
- `initial-prompt.md` session authority header is out of scope for this change (may require parallel evaluation separately).
