# Issue Resolution Workflow — Templates

Version: 3.0
Last Updated: 2026-02-14

This document contains the procedural templates for the issue resolution workflow. For normative rules and definitions, see [issue-resolution-rules.md](issue-resolution-rules.md).

------------------------------------------------------------

Proposal Template

Scope: Produces a proposal output artifact for a single issue.

Behavior:

1. If the inventory artifact is uncommitted, commit it first.
2. Produce the proposal output artifact.
3. Do NOT implement any changes.
4. Do NOT commit the proposal artifact.

The proposal artifact remains uncommitted so the human can review it before approval.

------------------------------------------------------------

Approval Template (Regular P-###)

Scope: Execution trigger for an issue (non-inventory).

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

The P-### item remains in Pending until Inventory Validation authorizes completion.

------------------------------------------------------------

Inventory Validation Template

Scope: Validation for P-### items with an inventory flag.

Trigger: After an Issue-### within the inventory is completed (implementation and summary committed), ask:

```
Next Issue-###? OR Validation?
```

Validation sequence:

When the user selects Validation, the P-### descriptive scope is already synchronized with the approved inventory artifact. Proceed as follows:

1. Primary validation. Validate that implemented Issue-### work matches the approved inventory artifact.
2. Deferred analysis. For each deferred Issue-### item:
   - Evaluate whether it is required to satisfy the descriptive requirements of the P-### item.
   - If a deferred Issue-### is required to meet P-### requirements, validation MUST fail.
   - P-### cannot be marked Completed until all required Issue-### work is implemented.
3. Deferred handling. Create NEW pending items in pending-items.md from deferred Issue-### items that are NOT required to satisfy P-### requirements.
4. Secondary validation. Validate that the final system state satisfies the descriptive requirements in the P-### entry.
5. Completion authority. Only after both primary and secondary validation pass AND all required Issue-### work is implemented may the P-### item be marked Completed in pending-items.md.

Artifact requirement: The validation artifact follows the same content requirements as the standard Verification artifact (see Verification Template).

------------------------------------------------------------

Verification Template

Scope: Runs once at loop end, after all issues have been resolved, deferred, or left unapproved.

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
4. Completion authority: Verification — not approval — authorizes marking a P-### item as Completed. When the verdict is PASS and all acceptance criteria are met, the artifact must explicitly state that completion is authorized. When the verdict is FAIL, the item remains in Pending and the artifact must state what remediation is required.

Backlog hygiene: When verification authorizes completion of a P-### item, move that item from Pending to Completed in docs/system/pending-items.md and commit the change as part of the verification commit. The completion date is the date of the verification artifact.
