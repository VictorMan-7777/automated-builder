# Implementation Summary — Backlog Hygiene Rule

**Target file**: `docs/system/issues.md`
**Version change**: 1.7 → 1.8

---

## Change Applied

Added a **Backlog hygiene** rule to the Approval template execution
sequence (after step 7, before the "No secondary approval" note):

> If the approved change completes a pending item identified as P-###,
> move that item from Pending to Completed in `docs/system/pending-items.md`
> during step 4. The move is committed as part of the implementation
> commit (step 5).

Version bumped to 1.8 with corresponding Document History entry.

---

## Verification Checklist

- [x] Rule placed inside Approval template, after execution sequence
- [x] No new concepts introduced (uses existing Pending/Completed sections)
- [x] No automation or discovery behavior added
- [x] Existing execution sequence (steps 1–7) unchanged
- [x] Other templates unchanged
- [x] Version bump and changelog entry present

---

## Commits

1. *(pending human approval)* — issues.md v1.7 → v1.8 + this summary
