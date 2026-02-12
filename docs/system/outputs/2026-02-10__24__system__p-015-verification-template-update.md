# P-015 — Verification Template Update

**Date**: 2026-02-10
**Context**: system
**Pending Item**: P-015
**Target File**: `docs/system/issue-resolution.md` (v1.8 → v1.9)

---

## Summary

Updated the Verification template in `docs/system/issue-resolution.md` to:

1. Add Pending-item context fields so verification works for non-inventory
   changes (individual P-### items).
2. Shift completion authority from approval to verification.
3. Clarify that approval authorizes execution, verification authorizes
   completion.

---

## Changes Applied

### Change 1 — Backlog hygiene rule rewritten (Approval template)

**Before (v1.8):**

> **Backlog hygiene.** If the approved change completes a pending item
> identified as P-###, move that item from Pending to Completed in
> `docs/system/pending-items.md` during step 4. The move is committed as
> part of the implementation commit (step 5).

**After (v1.9):**

> **Backlog hygiene.** Approval authorizes execution of the approved change.
> It does not authorize marking a P-### item as Completed. Items targeted
> by the approved change remain in Pending until verification explicitly
> authorizes their completion.

**Rationale:** The v1.8 rule placed completion authority at the approval/
execution step, which meant items could be marked Completed before
verification confirmed the change was correct. This created a gap where
a FAIL verdict would need to undo a completion.

### Change 2 — Verification artifact required content (new subsection)

Added to the "Deferred / Unapproved + Verification" section:

1. **Pending-item context** — P-### ID, intent/scope, acceptance criteria.
2. **Checks** — Specific checks confirming correct and complete application.
3. **Verdict** — PASS or FAIL with justification.
4. **Completion authority** — Verification (not approval) authorizes marking
   a P-### item as Completed. PASS + acceptance criteria met = completion
   authorized. FAIL = item remains in Pending with remediation stated.

### Change 3 — Backlog hygiene at verification (new rule)

Added rule: when verification authorizes completion of a P-### item, move
it from Pending to Completed in `pending-items.md` as part of the
verification commit. Completion date = verification artifact date.

---

## Files Modified

| File | Change |
|------|--------|
| `docs/system/issue-resolution.md` | Backlog hygiene rewritten; verification content requirements added; version 1.8 → 1.9 |

## Files NOT Modified

| File | Reason |
|------|--------|
| `docs/system/pending-items.md` | No status changes per instructions |

---

## Pending Item Status

P-015 remains in **Pending**. Not marked complete per instructions.
