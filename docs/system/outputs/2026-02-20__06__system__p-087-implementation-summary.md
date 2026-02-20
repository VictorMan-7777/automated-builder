# P-087 — Implementation Summary

**Item**: P-087 — Pending Items "Current Status" Field (Session Reorientation Removal)
**Artifact Type**: Implementation Summary
**Date**: 2026-02-20
**Status**: IMPLEMENTED

---

## Changes Made

Five changes across four files per the approved proposal (iteration 3).

---

### Change 1 — `docs/system/pending-items.md` — Rule 12 (Current Status definition)

Rule 12 inserted in the `## Rules` block defining:
- The `- Current Status:` field requirement for all active P-### items
- Allowed values for Standard P-### and Inventory P-###
- Lifecycle-trigger update requirement
- Correction commit allowance for status drift

---

### Change 2 — `docs/system/pending-items.md` — Current Status backfill (all active items)

`- Current Status:` field inserted at the end of every active P-### block.

96 items updated using evidence-based initial status assignment:
- Evidence hierarchy applied in order: Deferred → implementation-summary → inventory stages → proposal artifacts → default
- Items with `- Deferred until:` received `Deferred — [condition]` matching existing text
- P-003, P-012, P-083: `Implementation complete — awaiting archive` (summary artifacts confirmed)
- P-015: `Implementation complete — awaiting archive [ambiguous — verify]` (verification artifact present; no standard summary artifact)
- P-079: `Awaiting inventory proposal` (Classification: Inventory; no inventory artifact found)
- P-087: `Proposal produced — awaiting approval [verify]` (approved artifact present; no summary at time of backfill)
- All remaining active items without artifacts: `Awaiting proposal`

---

### Change 3 — `docs/system/issue-resolution-templates.md` — Current Status trigger points (3a–3f)

Six trigger points added:

- **3a** (Regular Approval step 7): Standalone P-### items update Current Status to `Implementation complete — awaiting archive` batched into the step-7 summary commit
- **3b** (Proposal Template step 1): Inventory proposal artifact commit batches `Inventory proposal produced — awaiting approval` (applied in prior session)
- **3c** (Inventory Approval step 5): Made unconditional — pending-items.md always committed with `Inventory approved — awaiting Issue-### execution`; scope-sync and status update share the same commit
- **3d** (Stage-1 trigger): Standalone commit setting `Inventory Verification Stage 1 pending` when user selects Validation (constitutional human gate)
- **3e** (Stage-1 PASS): `Inventory Verification Stage 2 pending` batched into Stage-1 artifact commit on PASS; no update on FAIL
- **3f** (Regular Approval step 3): Inventory Issue-### approval commit batches `Issue loop in progress — Issue-[N]` for parent P-###

---

### Change 4 — `docs/system/issue-resolution-rules.md` — Current Status Update Authority rule

New normative rule inserted defining:
- Update authority at lifecycle trigger steps
- Out-of-band correction commit allowance for status drift
- Correction commit message format: `docs(system): Correct P-### Current Status — [reason]`
- Treatment of missing Current Status field

---

### Change 5 — `docs/system/issue-resolution.md` — Governance Entry Contract step 4

Step 4 expanded to reference `- Current Status:` as the canonical resume point for session reorientation, stating the next required action without prior chat context.

---

## Acceptance Criteria Verification

- [x] `docs/system/pending-items.md` Rule 12 defines Current Status field, allowed values by type, lifecycle-trigger requirement, and correction commit allowance
- [x] Every active P-### item has `- Current Status:` with an allowed value derived from artifact evidence per the initial status assignment procedure
- [x] Deferred items use `Deferred — [condition]` matching their existing `- Deferred until:` text
- [x] `docs/system/issue-resolution-templates.md` includes Current Status update instructions at all six trigger points (3a–3f)
- [x] All six trigger-point updates batch into the nearest required commit; only Stage-1 "Validation" human gate (3d) uses a standalone commit
- [x] `docs/system/issue-resolution-rules.md` includes the update authority rule from Change 4, including correction commit provision
- [x] `docs/system/issue-resolution.md` Governance Entry Contract step 4 references `- Current Status:` as canonical resume point (Change 5)
- [x] A fresh session reading a P-### entry can determine the next required action from Current Status alone, without prior chat context
- [x] No changes to lifecycle decision logic, approval gates, or validation mechanics
- [x] Inventory Verification Stage-2 still does not modify `docs/system/pending-items.md` (Current Status advances at Stage-1 PASS, not Stage-2)

---

## Commits

1. `0e16b24` — docs(system): P-087 Approved — Add Current Status field to pending items
2. `bdaf19f` — docs(system): P-087 Implementation — Add Current Status field to pending items and governance docs
