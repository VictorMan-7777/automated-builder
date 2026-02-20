# Issue Resolution Workflow

Version: 3.0
Last Updated: 2026-02-17

---

## Governance Entry Contract (Mandatory First Read)

All governed operations MUST begin by reading this file.

For any request involving:
- Issues
- Inventory proposals
- Pending items
- Verification
- Approval
- Template changes
- P-### work

The agent MUST, in this order:

1. Read docs/system/issue-resolution.md
2. Read docs/system/issue-resolution-templates.md
3. Read docs/system/pending-items.md
4. Locate the referenced Issue or P-### item. After locating a P-### entry: read the `- Current Status:` field. This field is the canonical resume point for session reorientation — it states the next required action without relying on prior chat context.
5. Proceed under governed mechanics

Repository-wide exploration is NOT permitted before Step 1.

Failure to follow this order invalidates output authority.

---

------------------------------------------------------------

This document defines the issue resolution workflow for the automated-builder system. It specifies how issues are identified, proposed, approved, implemented, and verified.

The workflow is split into two companion documents:

- [issue-resolution-rules.md](issue-resolution-rules.md) — Definitions, loop diagrams, and normative rules
- [issue-resolution-templates.md](issue-resolution-templates.md) — Procedural templates (Proposal, Approval, Validation, Verification)

------------------------------------------------------------

LOOP OVERVIEW

The system uses two distinct loops depending on whether the P-### item has an inventory flag.

A. Regular P-### Loop (Non-Inventory)

```
Proposal
→ STOP (await human review)
→ Approval (execution trigger)
→ Change (implementation)
→ Summary
→ repeat per issue (if multi-issue)
→ Deferred/Unapproved + Verification
→ STOP
```

B. Inventory P-### Loop (Inventory-Flagged)

```
P-### Inventory Proposal
→ STOP (await human review)
→ Inventory Approval
  - Sync P-### scope in pending-items.md
  - Do NOT mark P-### complete
→ Loop Issue-### (multiple):
    Issue-### Proposal
    → STOP (await human review)
    → Approval
    → Change
    → Summary
    → Next Issue-### OR Validation?
→ Inventory Verification Stage 1
  - Confirm all Issue-### accounted for
  - Create new pending items if needed
→ Inventory Verification Stage 2
  - Validate P-### descriptive scope satisfied
  - PASS → move P-### to pending-items-archive.md
→ Verification
→ STOP
```

------------------------------------------------------------

For detailed rules, definitions, and examples, see [issue-resolution-rules.md](issue-resolution-rules.md).

For procedural templates, see [issue-resolution-templates.md](issue-resolution-templates.md).
