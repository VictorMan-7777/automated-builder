# Issue Resolution Workflow — Rules

Version: 3.0
Last Updated: 2026-02-14

------------------------------------------------------------

PURPOSE

This document defines the issue resolution workflow for the automated-builder system. It specifies how issues are identified, proposed, approved, implemented, and verified.

For procedural templates, see [issue-resolution-templates.md](issue-resolution-templates.md).

------------------------------------------------------------

DEFINITIONS

Issue

An Issue is a discrete unit of work identified during system diagnosis or inventory analysis. Issues use the format Issue-### where ### is a zero-padded three-digit number (e.g., 001, 012, 100).

Severity markers:

| Severity | Suffix | Example |
|----------|--------|---------|
| CRITICAL | C | Issue-007C |
| HIGH | H | Issue-012H |
| MEDIUM | (none) | Issue-021 |
| LOW | (none) | Issue-034 |

Exclusivity rule: The Issue-### format is the only permitted issue identification scheme. Letter-based identifiers, unnamed labels, or ad-hoc enumeration are not valid.

P-item

A P-item is a pending work item tracked in docs/system/pending-items.md. P-items use the format P-### where ### is a zero-padded three-digit number.

Inventory Flag

An inventory flag is a marker on a P-### item indicating that the item requires an inventory-proposal artifact. When present, the item follows the Inventory loop instead of the Regular loop.

Proposal vs Approved

Proposal is a stage. Approved is a state.

- Proposal artifacts end in -proposal.md (uncommitted draft).
- Approved artifacts end in -approved.md (committed, immutable).

Parallel naming rule (typed artifacts):

Generic rule: *-proposal.md becomes *-approved.md (stage → state).

For typed artifacts, proposal is still just a stage:

```
*-<type>-proposal.md → *-<type>-approved.md
```

Example:

```
p-084-inventory-proposal.md → p-084-inventory-approved.md
```

NOT inventory-proposal-approved.md.

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
→ Inventory Verification — Stage 1 (Issue Completion Verification)
  - Confirm all Issue-### accounted for
  - Create new pending items if needed
→ Inventory Verification — Stage 2 (Pending Scope Verification)
  - Validate P-### descriptive scope satisfied
  - PASS → mark P-### complete
→ Verification
→ STOP
```

Loop termination: The loop continues until (1) the inventory is fully resolved, OR (2) human intervention explicitly indicates all required issues are resolved.

Post-verification constraint: No new proposals may be started after the Verification artifact is created without a new inventory.

------------------------------------------------------------

RULES

Issue Identifier Rules

1. Issue identifiers MUST appear in proposal, implementation, and summary output artifacts.
2. Issue identifiers MUST NOT appear in output filenames (except proposal, implementation, or summary artifacts), system/governance file bodies, or implementation file contents.
3. Changelog entries corresponding to an issue MUST include: date, description, inventory file reference, and Issue-### identifier.

Changelog format:

```
Date — Description — Inventory file — Issue-###(C|H)?
```

Output Formatting Rule

All direct human prompts (requests, required responses, or STOP conditions) MUST be:

1. Visually separated by at least one blank line above and below.
2. In a fenced code block OR on their own line with no trailing instructional text.

No instructional sentence may share a line with a human request.

This applies to: "Approved", "Update the proposal...", "Next Issue-###? OR Validation?", STOP instructions, and any required human input trigger.

Artifact Immutability Rule

Once an approved artifact is committed, it MUST NOT be modified. The committed artifact is the permanent record of what was authorized.

Backlog Hygiene Rules

1. Approval does NOT authorize completion. Items remain in Pending until verification authorizes completion.
2. Completion authority:
   - Standard P-###: Verification PASS authorizes moving the P-### from Pending → Completed.
   - Inventory P-###: Inventory Verification Stage 2 PASS authorizes moving the P-### from Pending → Completed.
3. Deferred items remain in Pending. Append "Deferred: <reason>" or "Deferred until: <condition>" to the item block. Do NOT create a separate Deferred section.

Inventory-Specific Rules

1. Inventory approval syncs P-### scope immediately. Update the P-### descriptive scope in pending-items.md at approval (before Issue-### execution begins).
2. Issue-### items are execution slices only. Do NOT insert Issue-### items into pending-items.md.
3. Validation assumes P-### already synchronized. Validators reference the approved inventory artifact directly.
4. Deferred analysis during Inventory Verification Stage 2. If a deferred Issue-### is required to satisfy P-### requirements, Stage 2 MUST fail.
5. Deferred handling creates new pending items. Non-blocking deferred Issue-### items become NEW P-### items in pending-items.md.
6. Two-phase verification for inventory items:
   - Stage 1 (Issue Completion Verification): Confirms all Issue-### spawned by the inventory-approved artifact are completed. Does NOT authorize P-### completion. If incomplete, create new pending items for missing steps.
   - Stage 2 (Pending Scope Verification): Confirms that executed work resolves the descriptive scope of the P-### in pending-items.md. PASS authorizes moving P-### from Pending → Completed.

Inventory Verification Stage-1 Hardening Rules

1. Set-Based Verification Rule: Inventory Stage-1 MUST treat Issue-### items as a SET. Numerical order and commit chronology are irrelevant. Verification is coverage-based only.

2. Filesystem-First Discovery Rule: Stage-1 artifact discovery MUST be based on filesystem presence. Cross-document references (including legacy filenames) are NON-authoritative. If multiple filename variants exist, prefer the canonical "*-approved.md" pattern.

3. Flexible Summary Detection Rule: Stage-1 MUST recognize the following as valid implementation summaries:
   - issue-###-implementation-summary.md
   - issue-###-summary.md
   - issue-###-implementation.md (if explicitly labeled as summary)

4. No Assumed Consolidation Rule: Stage-1 MUST NOT presume consolidation of Issues. Consolidation must be explicitly documented by artifact reference. Absent explicit consolidation evidence, each Issue must independently satisfy coverage requirements.

5. Stage-1 PASS Definition: Inventory Stage-1 is considered PASS only if:
   - A Stage-1 verification artifact exists in outputs.
   - The artifact explicitly states: "Verdict: PASS".
   - The artifact lists every Issue-### from the inventory-approved artifact.
   - Each Issue has explicit FOUND evidence (approved artifact + implementation summary) or explicit deferral reference.

   Absent these elements, Stage-1 is NOT PASS.

6. Machine-Verifiable Requirement: Stage-1 PASS must be determinable solely by reading the Stage-1 artifact. External inference or memory is not permitted.

Inventory Verification Stage-2 Dependency Rules

1. Stage-1 Dependency Rule: Inventory Stage-2 MUST:
   - Explicitly cite the Stage-1 PASS artifact filename.
   - Fail immediately if a Stage-1 PASS artifact does not exist.
   - Fail immediately if the cited Stage-1 artifact does not contain "Verdict: PASS".

2. Completion Gate Rule: A P-### Inventory item may only be moved from Pending → Completed if:
   - Stage-1 PASS artifact exists.
   - Stage-2 PASS artifact exists.
   - Stage-2 artifact explicitly references the Stage-1 PASS artifact.

Validation Lookup Rule

Tools and processes MUST reference the most recent inventory-proposal artifact for a given item ID:

1. Scan docs/system/outputs/ for files matching: *__system__<item-id>-inventory-approved.md
2. Select artifact with highest date (YYYY-MM-DD).
3. If multiple artifacts have same date, select highest sequence number (NN).
4. If no approved inventory found, HALT: "No approved inventory-proposal found for {item-id}".

------------------------------------------------------------

EXAMPLES

Regular P-### Naming

Proposal artifact:

```
2026-02-14__01__system__p-042-proposal.md
```

After approval:

```
2026-02-14__01__system__p-042-approved.md
```

Inventory P-### Naming

Inventory proposal artifact:

```
2026-02-13__01__system__p-084-inventory-proposal.md
```

After inventory approval (typed artifact rename):

```
2026-02-13__01__system__p-084-inventory-approved.md
```

------------------------------------------------------------

CHANGELOG

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2026-02-14 | Full rewrite: parallel typed artifact naming rule, separate Regular vs Inventory loop diagrams, human-readable rules/templates separation, visual spacing enforcement for human prompts |
| 2.0 | 2026-02-13 | Add Inventory branch rule, Inventory-specific approval behavior, and Inventory Validation section to support full-loop inventory items with inventory flag on P-### |
| 1.9 | 2026-02-10 | Add Pending-item context to verification template; shift completion authority from approval to verification (P-015) |
| 1.8 | 2026-02-10 | Add backlog hygiene rule: move completed P-### items to Completed during execution |
| 1.7 | 2026-02-10 | Correct loop diagram to show pause-for-review and execution-trigger semantics; add approved artifact immutability rule |
| 1.6 | 2026-02-10 | Add deferred-item disposition rules and example to verification template |
| 1.5 | 2026-02-10 | Add proposal artifact prerequisite to approval template |
| 1.4 | 2026-02-10 | Rewrite approval template: encode execution sequence, distinguish approved/not-approved paths, add artifact requirement |
| 1.3 | 2026-02-09 | Add exclusivity rule: numeric Issue-### identifiers only, no letter-based identifiers |
| 1.2 | 2026-02-09 | Add loop templates (proposal, approval, deferred/verification) |
| 1.1 | 2026-02-09 | Add issue resolution loop and termination rules |
| 1.0 | 2026-02-09 | Initial issue numbering and severity scheme |
