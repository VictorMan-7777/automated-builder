# Issue Resolution Workflow — Rules

Version: 3.0
Last Updated: 2026-02-17

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

MODE CONSTRAINTS

Default Mode: Human (no automation constraints)

Constraint State: BOUNDED

Triggered by: "You are in BOUNDED mode. No scope expansion."

Note: Current prompts may use variant phrasing ("Constraint state: BOUNDED" with lowercase 's'). Both variants trigger BOUNDED state. Template phrasing reconciliation will be addressed in a future update.

Prohibitions:
- Scope expansion beyond prompt header artifact/phase identifier
- File modification outside docs/system/ is prohibited
- Within docs/system/, file modification outside the files explicitly listed in the active Issue-### scope (or explicitly listed target files in the governing prompt header) is prohibited
- Artifact write without template-required fields
- Commit before designated STOP checkpoint

Requirements:
- Adherence to governing inventory-approved artifact (if inventory)
- HALT on constraint violation: stop execution and report the specific violation

Automated Mode

Applies to: Inventory verification executed without human prompts between stages
Subject to: Automation Non-Interleaving Invariant (Inventory Verification Stage-2 Dependency Rules)

------------------------------------------------------------

APPROVAL LIFECYCLE EXECUTION CONTRACT

Applies to: All approval responses (Regular P-### and Inventory P-###).

Trigger: Human response of "Approved" or "Approved with <updates>" received
in response to a proposal artifact.

Upon trigger, the system MUST automatically execute the full approval
lifecycle without additional prompts:

1. Apply any approved corrections to the proposal artifact.
2. Produce the approved artifact per constitutional naming rules and
   artifact-state invariants (Issue-005).
3. Commit the approved artifact with constitutional commit message.
4. Execute post-approval sequencing:
   - For Inventory P-###: Pending-items.md scope sync (if required per
     Issue-005 guardrails), commit, then present the unified inventory gate:
     "Which issue proposal would you like next? (Or type 'Validation' to
     proceed to Inventory Verification.)"
   - For Regular Issue-###: Proceed immediately to implementation.
5. Continue execution until the next constitutional human gate:
   - Inventory: human responds to the unified inventory gate (selecting
     an Issue-### or Validation when all issues are Complete)
   - Regular Issue-###: human selects verification decision

Constitutional human gates (exhaustive list):
- "Which issue proposal would you like next? (Or type 'Validation' to
  proceed to Inventory Verification.)" prompt (Inventory loop; Validation
  is a selectable branch within this prompt and is the only valid
  recommendation when all issues are ✅ Complete)
- Verification decision (Regular loop)
- STOP checkpoints explicitly defined in governing templates

The system MUST NOT:
- Stop between the approval trigger and completion of the full execution
  lifecycle without having reached a constitutional human gate
- Require additional human prompts to initiate or continue approved
  execution before a constitutional gate is reached
- Pause between approval trigger and execution phase entry

Enforcement:

If execution stops after the approval trigger without reaching a
constitutional human gate:
- Classification: Constraint violation
- Required response: Report violation, identify last completed step,
  and resume execution from that step. If approved artifact was not
  yet written, revert to DRAFT state.

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
  - PASS → move P-### to pending-items-archive.md
→ Verification
→ STOP
```

Loop termination: The loop continues until (1) the inventory is fully resolved, OR (2) human intervention explicitly indicates all required issues are resolved.

Post-verification constraint: No new proposals may be started after the Verification artifact is created without a new inventory.

------------------------------------------------------------

RULES

Prompt Header Rule

The first line of every execution prompt MUST be a concise task description.

Purpose: Session dropdown title/indexing for later retrieval.

Requirements:

- ≤ 100 characters
- No multi-line text
- Must include the artifact/phase identifier when applicable (e.g., "Issue-009 Proposal", "Inventory Verification Stage-2 — P-084")
- Must not be "You are in BOUNDED mode…" (that becomes line 2).

Examples:

Regular Issue Proposal:
```
Issue-012 Proposal — Add git pre-commit hook
You are in BOUNDED mode. No scope expansion.
```

Inventory Verification Stage-1:
```
Inventory Verification Stage-1 — P-084
You are in BOUNDED mode. No scope expansion.
```

Inventory Verification Stage-2:
```
Inventory Verification Stage-2 — P-084 (System Builder)
You are in BOUNDED mode. No scope expansion.
```

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
   - Standard P-###: Verification PASS authorizes moving the P-### from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`.
   - Inventory P-###: Inventory Verification Stage 2 PASS authorizes moving the P-### from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`.
3. Deferred items remain in Pending. Append "Deferred: <reason>" or "Deferred until: <condition>" to the item block. Do NOT create a separate Deferred section.

Inventory-Specific Rules

1. Inventory approval syncs P-### scope immediately. Update the P-### descriptive scope in pending-items.md at approval (before Issue-### execution begins).
2. Issue-### Lifecycle Binding and Cross-Loop Isolation

   Issue-### items defined in the Inventory Proposal (required prior to approval):
   - Exist only inside the approved inventory artifact
   - MUST NOT move to pending-items.md
   - MUST NOT become P-### items
   - Are not independently archived
   - Are bound to the lifecycle of the governing Inventory P-###
   - Complete their lifecycle when the Inventory P-### reaches Stage-2 PASS

   Issue-### identifiers MUST NOT appear in pending-items.md except:
   - Descriptive references to completed work: "Resolved via Issue-012"
   - Dependency references in P-### blocks: "Depends on: Issue-009 completion"

   Enforcement (BOUNDED state):

   Before committing pending-items.md:
   - Verify no lines contain pattern "Issue-\d{3}[CH]?" in new P-### Summary blocks or as standalone items
   - If pattern found, HALT: "Loop isolation violation: Issue-### at line [N]"

   Before creating P-### from Issue-###:
   - HALT: "Lifecycle binding violation: Issue-### items cannot become P-### items"

   Before archiving Issue-### independently:
   - HALT: "Lifecycle binding violation: Issue-### items are not independently archived"
3. Validation assumes P-### already synchronized. Validators reference the approved inventory artifact directly.
4. Deferred analysis during Inventory Verification Stage 2. If a deferred Issue-### is required to satisfy P-### requirements, Stage 2 MUST fail.
5. Deferred handling creates new pending items. Non-blocking deferred Issue-### items become NEW P-### items in pending-items.md.
6. Two-phase verification for inventory items:
   - Stage 1 (Issue Completion Verification): Confirms all Issue-### spawned by the inventory-approved artifact are completed. Does NOT authorize P-### completion. If incomplete, create new pending items for missing steps.
   - Stage 2 (Pending Scope Verification): Confirms that executed work resolves the descriptive scope of the P-### in pending-items.md. PASS authorizes moving P-### from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`.

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

7. Newest Valid Artifact Selection Rule: When locating Stage-1 artifacts (or other verification prerequisites), the system MUST prefer the most recent artifact that satisfies the required condition (e.g., contains 'Verdict: PASS'). The system MUST NOT stop at the first matching filename if it fails the gate condition. If multiple candidates exist, select the newest candidate that satisfies the condition.

Proposal Self-Review Rule

After producing a proposal artifact, the system MUST immediately review the proposal against:
- The governing inventory-approved artifact (if inventory branch)
- The relevant issue template requirements (structure + required sections)
- The acceptance criteria listed in the proposal itself

If the proposal is missing required elements or contains contradictions, the system MUST generate a revised proposal (new output artifact) and repeat self-review.

Iteration limit:
- Maximum 5 proposal iterations per Issue.
- If the proposal still fails self-review after 5 iterations, HALT with:
  - "Proposal self-review failed after 5 iterations"
  - A concise list of missing/contradictory requirements
  - No implementation performed.

Human approval:
- Even after a proposal passes self-review, the system MUST STOP for human review and approval.
- Self-review does NOT authorize implementation.

Unified Inventory Gate — Input Handling

Non-Authoritative Intent Aliases

Applies to: Unified Inventory Gate and all proposal-entry points.

Purpose: Allow human-friendly phrasing at the inventory gate without
weakening deterministic authorization rules.

Intent phrases — examples of recognized non-authoritative approval expressions:
- "approve"
- "approve proposal 4"
- "ok approve"
- "let's approve 003"
- Similar informal expressions indicating approval intent

Intent phrases MUST NOT trigger any state change.

When intent is detected:

1. If a target Issue-### or Validation was included in the phrase, normalize
   it (e.g., "approve proposal 4" → Issue-004; leading zeros optional).
2. Respond with the exact deterministic command required:
   - If target is an Issue-###: reply `approved 004` (or `approved Issue-004`)
   - If no target and a recommendation is active: issue the confirmation
     prompt defined in the templates INPUT HANDLING block.
3. Await the literal deterministic token before proceeding. No state change
   occurs until the literal token is received.

Deterministic token authority:

Only the following tokens may trigger state transitions:
- `approved` (and `approved <target>` variants)
- `confirm`
- `confirm recreate Issue-###`
- `confirm inventory P-###`

No synonym expansion is permitted for state-changing tokens. "Approve", "ok",
"looks good", "yes", or other informal expressions are NOT deterministic tokens
and MUST NOT trigger state transitions.

Parse-layer constraint: Intent alias handling occurs at the parse layer only
and does not bypass lifecycle enforcement, BOUNDED state constraints, or any
other constitutional rules.

Duplicate Proposal Recreation Guard

Applies to: All proposal creation requests (Unified Inventory Gate and any
proposal-creation entry point).

Inventory Binding (precondition):

Before any proposal create, update, or recreate action for Issue-###:
1. Determine the governing Inventory P-### for the current session by
   locating the relevant APPROVED inventory artifact (e.g., the most
   recently approved *-inventory-approved.md for the active P-###).
2. All proposal existence checks and artifact scans MUST be scoped only
   to files explicitly associated with that governing Inventory P-###.
3. If the governing inventory cannot be determined unambiguously:
   HALT: "Inventory binding required — reply: confirm inventory P-###"
4. If the governing inventory IS determined, scans are bounded to its
   associated Issue-### set only. Cross-inventory matches are ignored.

If a request to create or draft a proposal for Issue-### is received and a
proposal artifact already exists for that Issue:

1. STOP immediately. Do not write or overwrite any file.
2. Present the following choice to the human:

   Option A (default-safe): Update the existing proposal in place.
   Option B (exception): Recreate the proposal from scratch — ONLY with
   explicit confirmation token: "confirm recreate Issue-###"

Confirmation token rules:
- Literal match only. No synonym expansion.
- Token format: "confirm recreate Issue-###" where ### matches the
  zero-padded Issue number.
- Without this exact token, the system MUST NOT regenerate, overwrite,
  or create a second proposal artifact.

Enforcement (BOUNDED state):

Before writing any new proposal artifact:
- Establish governing inventory per Inventory Binding precondition above.
  If unresolvable, HALT: "Inventory binding required — reply: confirm inventory P-###"
- Scan only the inventory-bound outputs set for the governing Inventory
  P-### (files explicitly associated with that inventory's Issue-### items).
  If no explicit association mechanism exists, default to HALT on ambiguity:
  HALT: "Inventory binding required — reply: confirm inventory P-###"
- Within the inventory-bound set, check for existing *__issue-###__proposal.md
  or *__issue-###__approved.md matching the requested Issue-###.
- If a proposal artifact is found, HALT creation and present Option A /
  Option B choice.
- If Option B is selected, require the confirmation token before
  proceeding.
- If confirmation token is absent or does not match literally,
  HALT: "Recreation token required: confirm recreate Issue-###"

Inventory Verification Stage-2 Dependency Rules

1. Stage-1 Dependency Rule: Inventory Stage-2 MUST:
   - Explicitly cite the Stage-1 PASS artifact filename.
   - Fail immediately if a Stage-1 PASS artifact does not exist.
   - Fail immediately if the cited Stage-1 artifact does not contain "Verdict: PASS".

2. Required Inputs Rule: Stage-2 MUST explicitly use:
   - inventory-approved artifact (primary authority)
   - P-### entry in pending-items.md (secondary authority; descriptive scope only)
   - all Issue implementation summaries relevant to the inventory item
   - deferred register (if present; if absent, state "none")

3. Machine-Verifiable Output Requirements Rule: Stage-2 output artifact MUST include:
   - "Stage-1 Reference: <filename>"
   - "Inventory Reference: <filename>"
   - "Verdict: PASS|FAIL"
   - Evidence-based PASS/FAIL results for:
     - Descriptive scope validation
     - Deferred dependency check

4. Completion Authority Binding Rule: A P-### Inventory item may only be moved from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md` if:
   - Stage-1 PASS artifact exists.
   - Stage-2 PASS artifact exists.
   - Stage-2 artifact explicitly references the Stage-1 PASS artifact.
   - The commit that moves P-### must occur only after Stage-2 PASS artifact is written.

5. Windowed Stage-1 PASS Discovery Rule: When locating the Stage-1 PASS artifact prerequisite for Stage-2:
   - Locate the most recent Stage-1 verification artifact for the inventory item (P-###).
   - If it contains "Verdict: PASS", use it.
   - If it does NOT contain "Verdict: PASS", search only newer artifacts (created after that artifact) for a Stage-1 artifact with "Verdict: PASS".
   - Select the newest Stage-1 artifact that satisfies "Verdict: PASS".
   - If no PASS artifact exists in the search window, Stage-2 MUST FAIL.

6. Automation Non-Interleaving Invariant (Mode: Automated only): When executing inventory verification in automated mode:
   - Automated inventory runs MUST NOT have other P-### or inventory verification artifacts interleaved between attempts for the same P-###.
   - If interleaving is detected (another P-### or verification artifact exists between consecutive attempts for the same P-###), HALT with: "Invariant violation: Interleaved artifacts detected for P-###. Manual review required."
   - This invariant applies only to automated execution. Human-guided execution is not subject to this constraint.

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
| 1.8 | 2026-02-10 | Add backlog hygiene rule: move completed P-### items to pending-items-archive during execution |
| 1.7 | 2026-02-10 | Correct loop diagram to show pause-for-review and execution-trigger semantics; add approved artifact immutability rule |
| 1.6 | 2026-02-10 | Add deferred-item disposition rules and example to verification template |
| 1.5 | 2026-02-10 | Add proposal artifact prerequisite to approval template |
| 1.4 | 2026-02-10 | Rewrite approval template: encode execution sequence, distinguish approved/not-approved paths, add artifact requirement |
| 1.3 | 2026-02-09 | Add exclusivity rule: numeric Issue-### identifiers only, no letter-based identifiers |
| 1.2 | 2026-02-09 | Add loop templates (proposal, approval, deferred/verification) |
| 1.1 | 2026-02-09 | Add issue resolution loop and termination rules |
| 1.0 | 2026-02-09 | Initial issue numbering and severity scheme |
