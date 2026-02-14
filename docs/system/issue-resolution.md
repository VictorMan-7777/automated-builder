# Issue Resolution Workflow

Version: 3.0
Last Updated: 2026-02-14

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
→ Inventory Validation
  - Validate against approved inventory artifact
  - Deferred analysis (fail if deferred required for P-###)
  - Deferred handling (non-blocking → new pending items)
  - Validate against P-### requirements
  - PASS → mark P-### complete
→ Verification
→ STOP
```

------------------------------------------------------------

For detailed rules, definitions, and examples, see [issue-resolution-rules.md](issue-resolution-rules.md).

For procedural templates, see [issue-resolution-templates.md](issue-resolution-templates.md).
