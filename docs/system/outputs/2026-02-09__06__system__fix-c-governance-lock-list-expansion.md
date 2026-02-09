# Fix C Proposal — Pending Approval

**Date:** 2026-02-09
**Status:** Pending approval
**Source:** Architecture Review Pass 1 (`2026-02-09__01__system__architecture-review-pass-1.md`), Finding 1
**Severity:** HIGH
**Scope:** Single-file change to an APPROVED document (requires human-approved revision)

---

## Problem

CP-2 (GOVERNANCE-LOCK) in `docs/implementation/system/checkpoint-taxonomy.md` (lines 106-111) defines 4 default governance files that sessions must lock as read-only:

```
- docs/system/access.md
- docs/system/initial-prompt.md
- docs/system/prompt-template.md
- prompts/planner/run-planner.md
```

This list is incomplete. Six additional files carry governance authority — they define rules, constraints, or contracts that sessions operate *under* — but are not protected by the governance lock. A session could modify any of them and pass all checkpoint verifications.

| Unprotected file | Governance role | How it could be silently modified |
|------------------|----------------|-----------------------------------|
| `docs/system/identity.md` | Authority model, default posture, explicit prohibitions. Required prerequisite for both planner and builder. | A session could relax the "human in control" principle or remove an explicit prohibition. |
| `docs/system/git.md` | Single source of truth for all commit behavior. Enforced at CP-8. | A session could loosen commit boundary rules or permit mixed-concern commits. |
| `CLAUDE.md` | Repository naming conventions, directory structure, scope principles. | A session could change naming rules to permit conventions that conflict with output naming. |
| `docs/implementation/system/checkpoint-taxonomy.md` | The execution contract itself (APPROVED). | A session could weaken a HARD stop to SOFT, remove a checkpoint, or alter an invariant. |
| `prompts/builder/run-builder.md` | Builder invocation template. Asymmetry: `run-planner.md` IS locked, but `run-builder.md` is NOT. | A session could remove prohibited actions, weaken validation checks, or alter the escalation triggers. |
| `docs/system/index.md` | System entry point defining roles, workflow, and artifact locations. | A session could alter role boundaries or change where artifacts are stored. |

### Why this matters now

The builder is under construction. Builder sessions will operate under the checkpoint taxonomy. If the governance lock doesn't cover the files that define builder behavior (`run-builder.md`, `git.md`, the taxonomy itself), a builder session could — within the rules as written — modify its own constraints and still pass CP-2.

---

## Proposed Resolution

Expand the default governance file list in CP-2 to include all files that carry governance authority.

### Proposed new default list (10 files)

Current 4 (unchanged):
- `docs/system/access.md`
- `docs/system/initial-prompt.md`
- `docs/system/prompt-template.md`
- `prompts/planner/run-planner.md`

Added 6:
- `docs/system/identity.md`
- `docs/system/git.md`
- `docs/system/index.md`
- `CLAUDE.md`
- `docs/implementation/system/checkpoint-taxonomy.md`
- `prompts/builder/run-builder.md`

### Selection criterion

A file belongs in the default governance list if it defines rules, constraints, contracts, or authority boundaries that sessions operate *under* rather than *on*. Files that are the *subject* of session work (project artifacts, output artifacts) do not belong.

### What about `docs/system/outputs/README.md`?

This file defines the output naming convention and the System Iterator protocol. It is governance-adjacent. However, it was just modified by Fix A in this session — meaning it is sometimes the subject of legitimate system maintenance work. Including it in the lock list would prevent future maintenance sessions from updating output rules without overriding CP-2.

**Recommendation:** Exclude `docs/system/outputs/README.md` from the default list. It can be added to a session's governance lock via the "unless overridden by task instructions" mechanism when needed.

---

## Affected Files

**Primary change:**
- `docs/implementation/system/checkpoint-taxonomy.md` — Update the default governance file list in CP-2 (lines 106-111).

**Note:** This document has `<!-- STATUS: APPROVED -->` on line 1. Modification requires explicit human approval, which this proposal requests.

**No changes required to:**
- Any other file. The CP-2 definition is the single location where the default list is maintained. All other documents reference governance locking conceptually but do not enumerate the list.

---

## Rule-Level Change

In the CP-2 (GOVERNANCE-LOCK) section, replace the 4-item default governance file list with the 10-item list above. Add the selection criterion as a brief note so future maintainers understand the inclusion principle.

No other aspect of CP-2 changes — the verification criteria, pass/fail conditions, evidence requirements, and applicability remain identical.

---

## Acceptance Criteria

1. The default governance file list in CP-2 contains all 10 files enumerated above.
2. The selection criterion for inclusion is stated adjacent to the list.
3. No other section of the checkpoint taxonomy is modified.
4. The `<!-- STATUS: APPROVED -->` marker is preserved (the document remains approved after a human-approved revision).
5. Every file that defines rules sessions operate *under* is in the list or explicitly excluded with rationale.

---

## Proposed Commit Message

```
docs(implementation): expand CP-2 default governance file list
```

Single-purpose commit. One file modified (`docs/implementation/system/checkpoint-taxonomy.md`).
