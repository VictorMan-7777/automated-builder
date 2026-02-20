# P-087 — Proposal: Add "Current Status" Field to Pending Items

**Item**: P-087 — Pending Items "Current Status" Field (Session Reorientation Removal)
**Artifact Type**: Proposal
**Date**: 2026-02-20
**Status**: APPROVED
**Iteration**: 3

---

## Scope

Five changes across four files. No workflow logic is altered; only status-surfacing fields and update instructions are added.

---

### Change 1 — `docs/system/pending-items.md` — Add Rule 12 (Current Status definition)

Insert a new rule as **Rule 12** in the `## Rules` block:

> 12. Every active P-### MUST include a `- Current Status:` field. The field MUST reflect the item's actual lifecycle state at all times. Allowed values are defined by item type (see table below). Current Status MUST be updated at the lifecycle trigger steps specified in `docs/system/issue-resolution-templates.md`. Out-of-band corrections are permitted only when Current Status has become factually inaccurate due to status drift (e.g., a lifecycle trigger completed without updating Current Status). Correction commits MUST use message `docs(system): Correct P-### Current Status — [reason]` and MUST state they are correcting status drift, not advancing lifecycle state. Current Status is descriptive and does not replace or duplicate the approval/validation mechanism.
>
> **Standard P-### allowed values:**
> | Value | Meaning |
> |---|---|
> | `Awaiting proposal` | Item captured; no proposal artifact written yet |
> | `Proposal produced — awaiting approval` | Proposal artifact written but not yet approved |
> | `Implementation complete — awaiting archive` | Summary artifact committed; pending archival |
> | `Deferred — [condition]` | Item explicitly deferred; condition stated |
>
> **Inventory P-### allowed values:**
> | Value | Meaning |
> |---|---|
> | `Awaiting inventory proposal` | Item captured; no inventory proposal artifact written yet |
> | `Inventory proposal produced — awaiting approval` | Inventory proposal artifact (*-inventory-proposal.md) committed but not yet approved |
> | `Inventory approved — awaiting Issue-### execution` | Approved; no issues started |
> | `Issue loop in progress — Issue-[N]` | Issue execution underway; N is the most recently started issue number |
> | `Inventory Verification Stage 1 pending` | All issues complete or deferred; Stage-1 not yet run |
> | `Inventory Verification Stage 2 pending` | Stage-1 PASS; Stage-2 not yet run |
> | `Deferred — [condition]` | Item explicitly deferred; condition stated |

---

### Change 2 — `docs/system/pending-items.md` — Add Current Status to all active items

For every active P-### item in the `## Pending Items` section, insert a `- Current Status:` line immediately after the last existing metadata line (e.g., after `- Notes:`, `- Dependencies:`, `- Acceptance Criteria:`, or `- Summary:` — whichever appears last).

Deferred items MUST use `- Current Status: Deferred — [condition]` with condition text matching the existing `- Deferred until:` line.

**Initial status assignment procedure** (one-time backfill only):

To assign Current Status for each existing active P-### item, evaluate committed artifact evidence in the order below. Apply the first matching condition. Derive status strictly from artifact state; do not infer or guess.

Evaluate in this order:

1. Item has a `- Deferred until:` line → `Deferred — [condition matching that text]`

2. *-implementation-summary.md committed in `docs/system/outputs/` for this P-### → `Implementation complete — awaiting archive`

3. *-inventory-approved.md committed for this P-###:
   a. AND a Stage-1 verification artifact (*-stage1-verification.md or equivalent) is committed for this P-### → `Inventory Verification Stage 2 pending`
   b. AND all Issue-### items declared in the approved artifact have committed summary artifacts (or deferred register entries), but no Stage-1 artifact yet → `Inventory Verification Stage 1 pending`
   c. AND at least one Issue-### summary artifact committed but not all → `Issue loop in progress — Issue-[N]` where N is the highest Issue-### number with a committed summary artifact
   d. AND no Issue-### summary artifacts exist → `Inventory approved — awaiting Issue-### execution`

4. *-inventory-proposal.md committed for this P-### (no approved version yet) → `Inventory proposal produced — awaiting approval`

5. *-approved.md committed in `docs/system/outputs/` for this P-### (no summary artifact) → `Proposal produced — awaiting approval` (approved artifact exists but summary is absent; implementation may be incomplete — flag inline with `[verify]`)

6. None of the above → `Awaiting proposal` (standard) or `Awaiting inventory proposal` (inventory-flagged, identifiable by the presence of Issue-### references in scope)

**Ambiguous case rule:** If artifact evidence is insufficient to determine state with confidence, assign the most conservative matching state and append `[ambiguous — verify]` inline. Do not guess. Document the specific evidence gap in a comment or note rather than advancing the status beyond what evidence supports.

---

### Change 3 — `docs/system/issue-resolution-templates.md` — Add Current Status update steps

Insert Current Status update instructions at the following lifecycle trigger points. Status updates are batched into the nearest constitutionally required commit at each trigger. A standalone commit is used only when no other commit occurs at that trigger point.

---

**3a — Regular Approval Template execution sequence (standalone P-### items)**

Applies when the P-### is a standalone item (not an Issue-### within an inventory). Amend step 7 to include the pending-items.md update in the same commit:

> 7. Update `- Current Status:` in pending-items.md for this P-### to `Implementation complete — awaiting archive`. Commit the summary artifact and the pending-items.md change together.

No separate step 8 is added.

---

**3b — Inventory Proposal Template — inventory artifact commit**

Applies when Proposal Template step 1 commits the *-inventory-proposal.md artifact. Add a sub-step to step 1:

> 1. If the inventory proposal artifact (*-inventory-proposal.md) is uncommitted, commit it first. Include the pending-items.md Current Status update (`Inventory proposal produced — awaiting approval`) in that same commit.
>
> If step 1 is skipped because the inventory proposal artifact was already committed in a prior session, the Current Status was set at that prior commit — no action needed in the current session.

The proposal output artifact produced in step 2 remains uncommitted (per the existing "Do NOT commit the proposal artifact" rule). No Current Status trigger is placed at step 2.

---

**3c — Inventory Approval Template — step 5 made unconditional**

Amend step 5 of the Inventory Approval Template so that it is unconditional:

> 5. Commit pending-items.md. This step is unconditional — pending-items.md MUST always be committed here, regardless of whether a scope-sync update occurred in step 4. The commit MUST include the Current Status update to `Inventory approved — awaiting Issue-### execution`. If step 4 produced a scope-sync update, include that change in the same commit.
>
> Commit message:
> - If scope-sync occurred (step 4 fired): `docs(system): Sync P-### scope and update Current Status — inventory approved`
> - If no scope-sync (step 4 was skipped): `docs(system): Update P-### Current Status — inventory approved`

Step 4 remains conditional (fires only if scope differs). Step 5 is unconditional.

---

**3d — Inventory Verification Stage-1 trigger**

In the Inventory Verification Stage-1 "Trigger" block, after "When the user selects Validation, proceed with Stage 1" and before the checks begin, insert:

> Update `- Current Status:` in pending-items.md for this P-### to `Inventory Verification Stage 1 pending`. Commit as a standalone commit with message: `docs(system): Update P-### Current Status — Stage-1 pending`
>
> This is a standalone commit. The user selecting "Validation" is a constitutional human gate; no other commit occurs at this trigger point.

---

**3e — Inventory Verification Stage-1 PASS**

When committing the Stage-1 artifact (PASS verdict), batch the Current Status update into the same commit:

> When Stage-1 verdict is PASS: include the pending-items.md Current Status update to `Inventory Verification Stage 2 pending` in the Stage-1 artifact commit. Do not create a separate commit for the status update.
>
> When Stage-1 verdict is FAIL: do not update Current Status. It remains `Inventory Verification Stage 1 pending`.

---

**3f — Issue loop in progress (Inventory)**

Remove the standalone commit from Inventory Approval Template step 6. Instead, batch the `Issue loop in progress` update into the Issue-N Approval Template step 3 commit:

In the Regular Approval Template, add a conditional sub-step to step 3:

> 3. Commit the approved artifact. If this Issue-### belongs to a parent inventory P-###: include the parent P-###'s pending-items.md Current Status update (`Issue loop in progress — Issue-[N]`, where N is this Issue number) in the same commit.

The Inventory Approval Template step 6 prompt ("Which Issue-### next?") is unchanged. No commit is made at step 6.

---

### Change 4 — `docs/system/issue-resolution-rules.md` — Add Current Status update authority rule

Insert the following as a new normative rule in `issue-resolution-rules.md` (in the section covering pending-items lifecycle or state management):

> **Current Status update authority:** The `- Current Status:` field in `docs/system/pending-items.md` MUST be updated at the lifecycle trigger steps defined in `docs/system/issue-resolution-templates.md`. Out-of-band corrections are permitted only when Current Status has become factually inaccurate due to status drift. Correction commits MUST use message format `docs(system): Correct P-### Current Status — [reason]` and MUST state they are correcting status drift, not advancing lifecycle state. If Current Status is absent from an active item, treat it as `Awaiting proposal` and note the missing field.

---

### Change 5 — `docs/system/issue-resolution.md` — Reference Current Status as canonical resume point

In the Governance Entry Contract, expand step 4 ("Locate the referenced Issue or P-### item") to add:

> After locating the P-### entry: read the `- Current Status:` field. This field is the canonical resume point for session reorientation. It states the next required action without relying on prior chat context.

---

## Non-Goals

- No changes to approval or validation logic
- No new lifecycle states or decision branches
- No changes to `docs/system/issue-resolution-rules.md` beyond the single rule addition in Change 4
- No changes to `docs/system/issue-resolution.md` beyond the single addition in Change 5
- No changes to `docs/system/pending-items-archive.md` (archived items do not carry Current Status)
- No changes to the Inventory Verification Stage-2 "MUST NOT modify pending-items.md" constraint — Current Status advances to `Inventory Verification Stage 2 pending` at Stage-1 PASS (batched with Stage-1 artifact commit), before Stage-2 runs

---

## Acceptance Criteria

- [ ] `docs/system/pending-items.md` Rule 12 defines the Current Status field, allowed values by item type, lifecycle-trigger update requirement, and correction commit allowance
- [ ] Every active P-### item in `docs/system/pending-items.md` has a `- Current Status:` line with an allowed value derived from artifact evidence per the initial status assignment procedure
- [ ] Deferred items use `Deferred — [condition]` matching their existing `- Deferred until:` text
- [ ] `docs/system/issue-resolution-templates.md` includes Current Status update instructions at all six trigger points defined in Change 3 (3a–3f)
- [ ] All six trigger-point updates batch the pending-items.md change into the nearest required commit; only the Stage-1 "Validation" human gate (3d) uses a standalone commit
- [ ] `docs/system/issue-resolution-rules.md` includes the update authority rule from Change 4, including the correction commit provision
- [ ] `docs/system/issue-resolution.md` Governance Entry Contract step 4 references `- Current Status:` as the canonical resume point (Change 5)
- [ ] A fresh session reading a P-### entry can determine the next required action from the Current Status field alone, without prior chat context
- [ ] No changes to lifecycle decision logic, approval gates, or validation mechanics
- [ ] Inventory Verification Stage-2 still does not modify `docs/system/pending-items.md` (Current Status advances at Stage-1 PASS, not Stage-2)

---

## Dependencies

- `docs/system/issue-resolution.md` — receives one sentence addition to the Governance Entry Contract (Change 5)
- `docs/system/issue-resolution-rules.md` — receives one addition (Change 4)
- `docs/system/issue-resolution-templates.md` — receives trigger-step additions (Change 3)
- P-086 depends on P-087: the Current Status field must exist in pending-items.md before P-086 (approval template pending-items sync) can reference it

---

## Change Log

| Version | Date | Trigger | Review Count | Summary | Reason | Sections Impacted |
|---|---|---|---|---|---|---|
| 1.0 | 2026-02-20 | Initial draft | 1 | Define Current Status field, add to all active items, add update steps to templates, add session reorientation rule | P-087 captured 2026-02-16; enables session resume without prior chat context | All sections |
| 2.0 | 2026-02-20 | Self-review fail — iteration 1 | 2 | Add Change 5 for docs/system/issue-resolution.md; correct Non-Goals to include it; update Acceptance Criteria; correct Dependencies | issue-resolution.md was listed in P-087 scope but incorrectly excluded in iteration 1 | Non-Goals, Acceptance Criteria, Dependencies, Change 5 |
| 3.0 | 2026-02-20 | Human review corrections | 3 | (1) Fix scope statement: five changes across four files. (2) Fix 3b commit semantics: batch into step-1 inventory artifact commit only; clarify proposal output stays uncommitted. (3) Batch all status updates into nearest required commit: 3a into step-7 commit; 3c makes step-5 unconditional; 3e batches Stage-2-pending into Stage-1 artifact commit; 3f moves trigger from Inventory Approval step 6 to Issue-N Approval step 3. (4) Replace absolute prohibition with correction commit allowance for status drift. (5) Add evidence-based initial status assignment procedure to Change 2. | Five corrections raised: scope accuracy, proposal commit semantics, commit noise, correction safety, initial status assignment | Scope, Change 1, Change 2, Change 3 (3a–3f), Change 4, Acceptance Criteria |
