# P-003 — Proposal: Add Proposal-Artifact Reference Requirement to Inventory Approval Template

**Item**: P-003 — Add proposal-artifact reference requirement to Approval template in issue-resolution-templates.md
**Artifact Type**: Proposal
**Date**: 2026-02-20
**Status**: APPROVED
**Iteration**: 1

---

## Scope

One targeted insertion to `docs/system/issue-resolution-templates.md`.

### Edit 1 — `docs/system/issue-resolution-templates.md`

Insert a "Proposal artifact prerequisite" block into the **Inventory Approval Template** section, between the closing code fence of the example prompt and the "Human response:" line.

**Location**: After the code block:

```
P-084 Inventory Approval — System Builder MVP
You are in BOUNDED mode. No scope expansion.
```

And before:

```
Human response:
```

**Content to insert** (one blank line above, one blank line below):

```
Proposal artifact prerequisite: Approval MUST reference a proposal artifact. If the proposal artifact is not present in the current session context, the approval instruction MUST include the proposal artifact filename or path. If missing, STOP and request it from the human.
```

**Rationale**: The Regular Approval Template already contains this prerequisite (immediately after its examples section). The Inventory Approval Template is missing the equivalent human-facing gate. The Inventory Approval Template's Enforcement (BOUNDED state) block does require "Source proposal artifact exists and is readable" as a write-time check — but that check fires after the approval prompt is processed, not before. The prerequisite block is the human-prompt-time gate: it tells the human what must be included in the approval instruction, and it tells the system to STOP and request it if absent. Without it, the Inventory Approval Template silently accepts an approval that lacks the proposal artifact reference, only detecting the gap later at write-time. This insertion closes that gap to match the Regular Approval Template's behaviour.

---

## Non-Goals

- No changes to the Regular Approval Template (already has the prerequisite)
- No search or discovery logic added (P-003 explicitly excludes this)
- No changes to `issue-resolution-rules.md`
- No changes to the Inventory Approval Template's Enforcement (BOUNDED state) block
- No other edits to `issue-resolution-templates.md`
- No new files created

---

## Acceptance Criteria

- [ ] `docs/system/issue-resolution-templates.md` — Inventory Approval Template contains a "Proposal artifact prerequisite" block
- [ ] The block text is identical to the prerequisite block in the Regular Approval Template
- [ ] The block appears after the closing code fence of the Inventory Approval Template example, and before "Human response:"
- [ ] No other content in the file is modified
- [ ] No new files created

---

## Dependencies

None.

---

## Change Log

| Version | Date | Trigger | Review Count | Summary | Reason | Sections Impacted |
|---|---|---|---|---|---|---|
| 1.0 | 2026-02-20 | Initial draft | 1 | Add prerequisite block to Inventory Approval Template between example and Human response | Inventory template missing human-prompt-time gate present in Regular template | Scope, Non-Goals, Acceptance Criteria |
