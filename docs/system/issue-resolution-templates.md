# Issue Resolution Workflow — Templates

Version: 3.0
Last Updated: 2026-02-17

This document contains the procedural templates for the issue resolution workflow. For normative rules and definitions, see [issue-resolution-rules.md](issue-resolution-rules.md).

------------------------------------------------------------

Proposal Template

Scope: Produces a proposal output artifact for a single issue.

Prompt Format:

```
<TASK TITLE LINE — REQUIRED>
You are in BOUNDED mode. No scope expansion.
```

Examples:

Regular issue proposal:
```
Issue-012 Proposal — Add git pre-commit hook
You are in BOUNDED mode. No scope expansion.
```

Inventory-flagged proposal:
```
Issue-007 Proposal — Refactor authentication module (P-084)
You are in BOUNDED mode. No scope expansion.
```

Behavior:

1. If the inventory artifact is uncommitted, commit it first.
2. Produce the proposal output artifact.
3. Execute Proposal Self-Review.
4. Do NOT implement any changes.
5. Do NOT commit the proposal artifact.

The proposal artifact remains uncommitted so the human can review it before approval.

Proposal Self-Review

After generating the proposal artifact, the system MUST immediately review the proposal against:

Required checklist:
- Required sections present (as defined by issue type)
- Acceptance criteria present and testable
- Dependencies explicitly listed (including deferrals)
- No scope expansion beyond inventory authority (if inventory)
- Proposal aligns with governing inventory-approved artifact (if inventory)

Iteration counter:
- Start at iteration 1.
- Maximum 5 iterations per Issue.

If the proposal fails self-review:
- Generate a revised proposal artifact (increment iteration counter).
- Repeat self-review.
- If iteration counter reaches 5 and proposal still fails, HALT with:
  - "Proposal self-review failed after 5 iterations"
  - A concise list of missing/contradictory requirements
  - No implementation performed.

If the proposal passes self-review:
- Proceed to STOP for human review.

STOP.

Transition Binding Rule:

When the human responds "Approved" or "Approved with <updates>", immediately execute the relevant Approval Template below (Regular P-### or Inventory, depending on the issue type). Do NOT pause or request further instruction.

------------------------------------------------------------

Approval Template (Regular P-###)

Scope: Execution trigger for an issue (non-inventory).

Prompt Format:

```
<TASK TITLE LINE — REQUIRED>
You are in BOUNDED mode. No scope expansion.
```

Examples:

Regular issue approval:
```
Issue-012 Approval — Add git pre-commit hook
You are in BOUNDED mode. No scope expansion.
```

Inventory-flagged issue approval:
```
Issue-007 Approval — Refactor authentication module (P-084)
You are in BOUNDED mode. No scope expansion.
```

Proposal artifact prerequisite: Approval MUST reference a proposal artifact. If the proposal artifact is not present in the current session context, the approval instruction MUST include the proposal artifact filename or path. If missing, STOP and request it from the human.

Human response:

```
Approved
```

or

```
Approved with <updates>
```

Execution sequence (no pauses):

1. Apply the specified updates to the proposal, if any.
2. Rename the proposal artifact from *-proposal.md to *-approved.md.
3. Commit the approved artifact.
4. Implement the approved change.
5. Commit the implementation.
6. Create the implementation summary artifact.
7. Commit the summary.

Alternative responses:

```
Update the proposal...
```

or

```
Redo the proposal...
```

An explicit instruction to update or redo keeps the proposal unapproved and in draft. Revise the proposal artifact per the instruction. The proposal remains uncommitted and awaits a subsequent approval instruction.

------------------------------------------------------------

Inventory Approval Template

Scope: Execution trigger for an inventory item (P-### with inventory flag).

Prompt Format:

```
<TASK TITLE LINE — REQUIRED>
You are in BOUNDED mode. No scope expansion.
```

Example:

```
P-084 Inventory Approval — System Builder MVP
You are in BOUNDED mode. No scope expansion.
```

Human response:

```
Approved
```

or

```
Approved with <updates>
```

Execution sequence (no pauses):

1. Apply any approved updates to the proposal.
2. Rename the typed proposal artifact using the parallel naming rule:

   ```
   *-<type>-proposal.md → *-<type>-approved.md
   ```

   Example:

   ```
   p-084-inventory-proposal.md → p-084-inventory-approved.md
   ```

3. Commit the approved inventory artifact.
4. Update pending-items.md for the same P-### to reflect the approved inventory scope in descriptive form (P-### style).
   - Do NOT add any "approved" marker to the P-### item.
   - This is a scope sync only.
5. Commit the updated pending-items.md in a separate commit.
6. Ask the user:

   ```
   Which Issue-### next?
   ```

7. Do NOT mark P-### complete at this stage.

The P-### item remains in Pending until Inventory Verification — Stage 2 PASS authorizes completion.

------------------------------------------------------------

Inventory Verification — Stage 1 (Issue Completion Verification)

Scope: Confirms all Issue-### items spawned by the inventory-approved artifact are completed.

Prompt Format:

```
<TASK TITLE LINE — REQUIRED>
You are in BOUNDED mode. No scope expansion.
```

Example:

```
Inventory Verification Stage-1 — P-084 (System Builder)
You are in BOUNDED mode. No scope expansion.
```

Verification Discovery Safeguards

- Issues are evaluated as a SET.
- Artifact detection is filesystem-based.
- Flexible summary filename matching.
- No consolidation assumptions without artifact reference.
- Diagnostic output MUST list explicit FOUND/NOT FOUND evidence for each Issue.

Trigger: After an Issue-### within the inventory is completed (implementation and summary committed), ask:

```
Next Issue-###? OR Validation?
```

When the user selects Validation, proceed with Stage 1.

Inputs:

1. The approved inventory artifact (*-inventory-approved.md).
2. Summary artifacts for all implemented Issue-### items.
3. Deferred register (if any).

Checks:

1. List all Issue-### items defined in the approved inventory artifact.
2. For each Issue-###, verify it has either:
   - A committed implementation summary artifact, OR
   - An entry in the deferred register.
3. For each missing Issue-###, identify whether it is required to satisfy P-### requirements.

Required Output Structure:

The Stage-1 artifact MUST include:

1. A verdict header section:
   ```
   Verdict: PASS
   ```
   or
   ```
   Verdict: FAIL
   ```

2. An explicit Issue coverage table listing every Issue-### from the inventory-approved artifact.

3. Explicit evidence references for each Issue (FOUND: approved artifact + implementation summary, or explicit deferral reference).

Verdict:

- PASS: All Issue-### items are accounted for (implemented or deferred).
- FAIL: One or more Issue-### items are missing.

On FAIL:

Create new pending items in pending-items.md for all incomplete Issue-### items.

CRITICAL: Stage 1 does NOT authorize moving P-### to Completed. Proceed to Stage 2.

------------------------------------------------------------

Inventory Verification — Stage 2 (Pending Scope Verification)

Scope: Confirms that executed work resolves the descriptive scope of the P-### item in pending-items.md.

Prompt Format:

```
<TASK TITLE LINE — REQUIRED>
You are in BOUNDED mode. No scope expansion.
```

Example:

```
Inventory Verification Stage-2 — P-084 (System Builder)
You are in BOUNDED mode. No scope expansion.
```

Stage-1 Dependency Gate:

Stage-2 MUST locate the Stage-1 PASS artifact using windowed discovery:
1. Locate the most recent Stage-1 verification artifact for this P-### in docs/system/outputs/.
2. If it contains "Verdict: PASS", use it as the Stage-1 PASS artifact.
3. If it does NOT contain "Verdict: PASS", search only newer artifacts (created after that artifact) for a Stage-1 artifact with "Verdict: PASS".
4. Select the newest Stage-1 artifact that satisfies "Verdict: PASS".
5. If no PASS artifact exists in the search window, Stage-2 MUST fail immediately.

Stage-2 MUST explicitly cite the Stage-1 PASS artifact filename in the output.
Stage-2 MUST fail if the cited Stage-1 artifact does not contain "Verdict: PASS".

Required Inputs:

Stage-2 MUST explicitly use:
1. inventory-approved artifact (primary authority)
2. P-### entry in pending-items.md (secondary authority; descriptive scope only)
3. all Issue implementation summaries relevant to the inventory item
4. deferred register (if present; if absent, state "none")
5. The Stage-1 PASS artifact (mandatory prerequisite)

Required Output Structure:

The Stage-2 artifact MUST include:

1. A Stage-1 reference field:
   ```
   Stage-1 Reference: <filename>
   ```

2. An Inventory reference field:
   ```
   Inventory Reference: <filename>
   ```

3. A verdict section:
   ```
   Verdict: PASS
   ```
   or
   ```
   Verdict: FAIL
   ```

4. Evidence-based PASS/FAIL results for:
   - Descriptive scope validation
   - Deferred dependency check

Checks:

1. Stage-1 Dependency Check (mandatory first check):
   - Verify that a Stage-1 PASS artifact exists and is explicitly referenced.
   - If Stage-1 PASS artifact does not exist, FAIL immediately.
   - If the cited Stage-1 artifact does not contain "Verdict: PASS", FAIL immediately.

2. Deferred Dependency Check (evidence-based):
   - List all deferred Issue-### items from the deferred register.
   - For each deferred Issue-### item:
     - Evaluate whether it is required to satisfy the descriptive requirements of the P-### item.
     - Document the evaluation evidence.
   - If a deferred Issue-### is required to meet P-### requirements, Stage 2 MUST fail.

3. Descriptive Scope Validation (evidence-based):
   - Validate that the final system state satisfies the descriptive requirements in the P-### entry.
   - Document the validation evidence.

Verdict:

- PASS: Stage-1 PASS artifact exists and is referenced, all required work is complete, and the P-### descriptive scope is fully satisfied.
- FAIL: Stage-1 PASS artifact missing or does not contain "Verdict: PASS", OR deferred Issue-### items are required for P-###, OR the P-### descriptive scope is not satisfied.

On PASS:

Move the P-### item from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`.

On FAIL:

The P-### item remains in Pending. The artifact must state what remediation is required.

Completion authority: Stage 2 PASS is the ONLY authority that moves an inventory P-### from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`. The commit that moves P-### must occur only after Stage-2 PASS artifact is written.

Deferred handling: Create NEW pending items in pending-items.md from deferred Issue-### items that are NOT required to satisfy P-### requirements.

------------------------------------------------------------

Verification Template

Scope: Runs once at loop end, after all issues have been resolved, deferred, or left unapproved.

Prompt Format:

```
<TASK TITLE LINE — REQUIRED>
You are in BOUNDED mode. No scope expansion.
```

Example:

```
Verification — P-084 (System Builder)
You are in BOUNDED mode. No scope expansion.
```

Behavior:

1. If any issues were deferred or unapproved, produce a Deferred/Unapproved register artifact.
2. Produce a Verification artifact.
3. Commit both artifacts (or the Verification artifact alone if no issues were deferred or unapproved).
4. Stop.

Required content:

1. Pending-item context (when the change targets a P-### item):
   - Pending item ID (P-###).
   - Intent and scope (from the item's Summary in pending-items.md).
   - Acceptance criteria: what constitutes "done" for this item.
2. Checks: Specific checks confirming the change was applied correctly and completely.
3. Verdict: PASS or FAIL with justification.
4. Completion authority: Verification — not approval — authorizes moving a P-### item from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`. When the verdict is PASS and all acceptance criteria are met, the artifact must explicitly state that completion is authorized. When the verdict is FAIL, the item remains in Pending and the artifact must state what remediation is required.

Backlog hygiene: When verification authorizes completion of a P-### item, move that item from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md` and commit the change as part of the verification commit. The completion date is the date of the verification artifact.
