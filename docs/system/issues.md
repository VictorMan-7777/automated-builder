# Issue Numbering and Severity Scheme

**Version**: 1.7
**Last Updated**: 2026-02-10

---

## Issue Identifiers

Issue identifiers use the format:

```
Issue-###
```

Where `###` is a zero-padded three-digit number (e.g., `001`, `012`, `100`).

**Exclusivity rule.** The `Issue-###` format is the only permitted issue
identification scheme. Letter-based identifiers (e.g., "Issue A", "Fix B"),
unnamed labels, or ad-hoc enumeration (e.g., "the first issue") are not valid
issue identifiers. This rule applies to all contexts where issues are
identified, including inventories, diagnostics, proposals, summaries, and
verification artifacts.

---

## Severity Markers

Severity is indicated by appending a single-letter suffix to the identifier:

| Severity | Suffix | Example |
|----------|--------|---------|
| CRITICAL | C | Issue-007C |
| HIGH | H | Issue-012H |
| MEDIUM | *(none)* | Issue-021 |
| LOW | *(none)* | Issue-034 |

Only CRITICAL and HIGH receive a suffix marker. MEDIUM and LOW issues use the
bare identifier with no suffix.

---

## Where Issue Identifiers MUST Appear

Issue identifiers MUST be included in the following output artifact types:

- Proposal output artifacts
- Implementation documentation output artifacts
- Summary output artifacts

---

## Where Issue Identifiers MUST NOT Appear

Issue identifiers MUST NOT appear in:

- Output filenames (other than proposal, implementation, or summary artifacts)
- System or governance file bodies
- Implementation file contents

---

## Changelog Entry Format

If a system file contains a changelog section, each changelog entry that
corresponds to an issue MUST include:

1. Date changed
2. Description
3. Inventory file reference
4. Issue identifier

**Format:**

```
Date — Description — Inventory file — Issue-###(C|H)?
```

**Examples:**

```
2026-02-09 — Fix system iterator definition — 2026-02-09__02__system__fix-a-system-iterator-definition.md — Issue-001C
2026-02-09 — Expand governance lock list — 2026-02-09__06__system__fix-c-governance-lock-list-expansion.md — Issue-003H
2026-02-09 — Clarify commit convention — 2026-02-09__12__system__pass-1-deferred-items-register.md — Issue-015
```

---

## Issue Resolution Loop

Issues are resolved through a repeating loop. Each issue passes through
proposal, approval, and execution before the next issue begins:

```
Inventory
→ Proposal → STOP (await human review)
→ Approval (execution trigger)
  → Change
  → Summary
→ repeat for next issue
→ Deferred / Unapproved + Verification
→ STOP
```

### Termination Conditions

The loop continues until one of the following is true:

1. The inventory is fully resolved (every issue has a completed summary), OR
2. Human intervention explicitly indicates all required issues are resolved.

### End-of-Loop Artifacts

At loop end, both of the following apply:

1. **Deferred / Unapproved register.** If any issues were deferred or
   unapproved during the loop, a Deferred / Unapproved register artifact
   is created and committed.
2. **Verification artifact.** A Verification artifact is always created
   and committed, regardless of whether any issues were deferred.

### Post-Verification Constraint

No new proposals may be started after the Verification artifact is created
without a new inventory.

---

## Loop Templates

### Proposal

The Proposal step produces a proposal output artifact for a single issue.

**Behavior:**

1. If the inventory artifact is uncommitted, commit it first.
2. Produce the proposal output artifact.
3. Do NOT implement any changes.
4. Do NOT commit the proposal artifact.

The proposal artifact remains uncommitted so the human can review it before
approval. The approval step determines what happens next.

---

### Approval

Approval is the execution trigger for an issue. Proposal artifacts are draft
and MUST NOT be committed; only approved artifacts are committed. The human
responds to a proposal with one of the following instructions.

**Proposal artifact prerequisite.** Approval MUST reference a proposal
artifact. If the proposal artifact is present in the current session context,
the reference is implicit. If the proposal artifact is not present in the
current session context, the approval instruction MUST include the proposal
artifact filename or path. If the proposal artifact reference is missing,
STOP and request it from the human.

**Approved / Approved with updates:**

```
Approved
```

or

```
Approved with <updates>
```

When the instruction is "Approved" or "Approved with \<updates\>", Claude
executes the following sequence without pausing:

1. Apply the specified updates to the proposal, if any.
2. Rename the proposal artifact from `*-proposal.md` to `*-approved.md`.
3. Commit the approved artifact.
4. Implement the approved change.
5. Commit the implementation.
6. Create the implementation summary artifact.
7. Commit the summary.

No secondary approval is implied. Verification is NEVER part of approval
and is always a separate prompt.

**Not approved / Update proposal:**

```
Update the proposal…
```

or

```
Redo the proposal…
```

An explicit instruction to update or redo the proposal keeps the proposal
unapproved and in draft. Claude revises the proposal artifact per the
instruction. The proposal remains uncommitted and awaits a subsequent
approval instruction.

**Artifact requirement.** All approvals MUST be saved as approved artifacts
(the renamed `*-approved.md` file). The approved artifact is the
authoritative record of what was approved.

**Approved artifact immutability.** Once an approved artifact is committed,
it MUST NOT be modified. The committed artifact is the permanent record of
what was authorized.

---

### Deferred / Unapproved + Verification

This template runs once at loop end, after all issues have been resolved,
deferred, or left unapproved.

**Behavior:**

1. If any issues were deferred or unapproved, produce a Deferred / Unapproved
   register artifact.
2. Produce a Verification artifact.
3. Commit both artifacts (or the Verification artifact alone if no issues
   were deferred or unapproved).
4. Stop.

**Deferred-item disposition in `pending-items.md`:**

When an item is deferred during issue resolution or verification:

1. Do NOT move the item to a separate Deferred section or list.
2. Keep the item in **Pending** in `docs/system/pending-items.md`.
3. Append exactly one deferred marker line inside the item block, using one
   of these forms:
   - `Deferred: <reason>`
   - `Deferred until: <condition>`
4. Deferred items remain part of the canonical backlog. Derived views
   (e.g., an active-pending filter) may exclude deferred items, but the
   Verification step must not.

**Example — pending item with deferred marker:**

```markdown
### P-042 — Example deferred item
- Source: Issue loop
- Captured: 2026-02-10
- Summary:
  Description of the pending item.
Deferred until: <condition>
```

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.7 | 2026-02-10 | Correct loop diagram to show pause-for-review and execution-trigger semantics; add approved artifact immutability rule |
| 1.6 | 2026-02-10 | Add deferred-item disposition rules and example to verification template |
| 1.5 | 2026-02-10 | Add proposal artifact prerequisite to approval template |
| 1.4 | 2026-02-10 | Rewrite approval template: encode execution sequence, distinguish approved/not-approved paths, add artifact requirement |
| 1.3 | 2026-02-09 | Add exclusivity rule: numeric Issue-### identifiers only, no letter-based identifiers |
| 1.2 | 2026-02-09 | Add loop templates (proposal, approval, deferred/verification) |
| 1.1 | 2026-02-09 | Add issue resolution loop and termination rules |
| 1.0 | 2026-02-09 | Initial issue numbering and severity scheme |
