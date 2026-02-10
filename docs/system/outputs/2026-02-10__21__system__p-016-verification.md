# P-016 Verification — Enforce Output Artifact After Every Claude Iteration

**Date**: 2026-02-10
**Context**: system
**Pending Item**: P-016
**Verification type**: One-off process/governance verification (non-inventory)

---

## Overall Verdict: FAIL

P-016 partially achieves its stated goal. The core governance files were updated
correctly, but a significant enforcement gap exists: the outputs directory's own
governing document (`docs/system/outputs/README.md`) was not updated and still
contains the old conditional rule, directly contradicting the new unconditional
rule. Additionally, no approval artifact exists in the artifact trail.

---

## Check 1 — Was P-016 explicitly approved before execution?

**Result: UNVERIFIABLE (gap)**

No proposal artifact and no approval artifact exist for P-016. The only
P-016-related output artifact is the execution summary
(`2026-02-10__20__system__p-016-execution-output-artifact-every-iteration.md`).

Evidence examined:
- Glob search for `*p-016*approv*` and `*p-016*proposal*`: no matches.
- Git log shows a single commit (`09799f2`) containing all changes and the
  execution output simultaneously — no prior proposal or approval commit.
- `pending-items.md` Rule 6 states: "Pending items are capture-only and do not
  trigger work unless explicitly promoted."

The approval may have occurred in chat (the commit is co-authored by
Claude Opus 4.6 and the human), but no artifact trail exists to verify it.
The system's plan-first methodology (CLAUDE.md) requires Plan → Review →
Implement → Verify, and no plan or review artifact is present.

---

## Check 2 — Exact governance rule text added

**Result: PASS**

The following unconditional rule text was added to three governance files:

### `docs/system/access.md` (lines 76–80)

> Every Claude iteration must produce an output artifact saved to
> `docs/system/outputs/`. This obligation is unconditional — it is not gated
> by artifact type, length, or session mode.

### `docs/system/initial-prompt.md` (lines 67–70, inside authority header)

> OUTPUT REQUIREMENT RULE: Every Claude iteration MUST produce an output
> artifact saved to docs/system/outputs/. This obligation is unconditional —
> it is not gated by artifact type, length, or session mode.

### `docs/system/prompt-template.md` (lines 176–177)

> All prompts MUST include this instruction block. Every Claude iteration must
> produce an output artifact — this obligation is unconditional.

All three files contain consistent, aligned rule text establishing the
unconditional obligation.

---

## Check 3 — Enforcement scope is broader than pre-existing rules

**Result: PASS**

The diff (commit `09799f2`) confirms the old rule was conditional:

| File | Old trigger | New trigger |
|------|-------------|-------------|
| `access.md` | "Any session that produces a reviewable artifact — defined as [8-type list]" | "Every Claude iteration" (unconditional) |
| `initial-prompt.md` | "Any session that produces a reviewable artifact (plan, audit, decision, or governance guidance)" | "Every Claude iteration" (unconditional) |
| `prompt-template.md` | "All prompts that produce reviewable artifacts" | "All prompts" (unconditional) |
| Compliance clause (`access.md`) | "A qualifying session — one that produced any reviewable artifact" | "A session" (no qualification) |
| Compliance clause (`initial-prompt.md`) | "if the session produced any reviewable artifact (plan, audit, decision, governance guidance, build report, or review)" | Conditional removed entirely |

The new scope is strictly broader. Every session is now covered, not just those
producing specific artifact types.

---

## Check 4 — Execution produced required artifacts

**Result: PARTIAL FAIL**

| Artifact | Expected | Found |
|----------|----------|-------|
| Proposal artifact | Yes (plan-first methodology) | **Not found** |
| Approval artifact | Yes (explicit promotion required) | **Not found** |
| Execution output artifact | Yes | Found: `2026-02-10__20__system__p-016-execution-output-artifact-every-iteration.md` |
| Implementation commit | Yes | Found: `09799f2` |

The execution output artifact exists and is well-structured. However, the
proposal and approval artifacts are absent, leaving the authorization chain
unverifiable from the artifact trail alone.

---

## Check 5 — Rule is enforceable (not advisory)

**Result: PASS**

The rule uses mandatory enforcement language across all three files:

| Enforcement mechanism | Evidence |
|-----------------------|----------|
| Mandatory verb | "must produce" / "MUST produce" |
| Stop condition | "may not be considered complete until" / "MAY NOT stop" |
| Failure consequence | "Failure to do so is a session failure" |
| Authority level | Inside immutable session authority header |
| Propagation | prompt-template.md requires all prompts include the block |

The rule is enforceable, not advisory or descriptive. It creates a binding
obligation with a defined failure state.

---

## Check 6 — Gaps, ambiguities, and partial enforcement

### Gap 1 (CRITICAL): `docs/system/outputs/README.md` not updated

The outputs directory's governing document still contains the **old conditional
rule** (lines 20–34):

> Claude MUST save output to a file in this directory when the session produces
> a **reviewable artifact**. Length is not a factor; the obligation is triggered
> by artifact type, not size.

This directly contradicts the new unconditional rule in `access.md`,
`initial-prompt.md`, and `prompt-template.md`. The README also retains a
"When NOT to Save" section (lines 38–44) listing exemptions (interactive Q&A,
error messages, quick status updates) that conflict with the unconditional
obligation.

The P-016 execution output acknowledges this file under "Files NOT Modified"
but does not list `README.md` — it only lists `run-planner.md`, `run-builder.md`,
`issues.md`, and `pending-items.md`. The README.md omission appears unintentional.

### Gap 2 (MEDIUM): No approval artifact trail

As detailed in Check 1, no proposal or approval artifact exists. This makes the
authorization unverifiable from artifacts alone and departs from the plan-first
methodology (Plan → Review → Implement → Verify) defined in CLAUDE.md.

### Gap 3 (LOW): Version numbering order in document history

Both `initial-prompt.md` and `prompt-template.md` list version 1.2 above
version 1.1 in their document history tables, creating a non-chronological
display order. This is cosmetic but could cause confusion.

### Gap 4 (LOW): "Iteration" not formally defined in rule text

The rule uses "every Claude iteration" but the term "iteration" is not defined
in the rule text itself. Context suggests it means "a Claude session/conversation
where work is performed," and the system iterator documentation provides related
naming conventions, but an explicit definition within the rule would strengthen
enforceability.

---

## Remediation Required

### Must-fix (to achieve PASS)

1. **Update `docs/system/outputs/README.md`** — Replace the conditional
   "Output Capture Rule" (lines 20–44) with the unconditional rule consistent
   with `access.md`, `initial-prompt.md`, and `prompt-template.md`. Remove or
   reconcile the "When NOT to Save" exemption list.

### Should-fix

2. **Create a retroactive approval record** — Document the authorization for
   P-016 (even if approval occurred in chat) to close the artifact trail gap.
   This could be a brief approval artifact noting chat-based authorization.

3. **Fix document history ordering** — In `initial-prompt.md` and
   `prompt-template.md`, reorder the version history table so entries appear in
   chronological order (1.0 → 1.1 → 1.2).

### Consider

4. **Define "iteration"** — Add a brief definition of "Claude iteration" to the
   rule text or reference an existing definition to prevent future ambiguity.

---

## Files Examined

| File | Purpose |
|------|---------|
| `docs/system/pending-items.md` | P-016 definition and status |
| `docs/system/outputs/2026-02-10__20__system__p-016-execution-output-artifact-every-iteration.md` | Execution output |
| `docs/system/access.md` | Updated governance rule (verified) |
| `docs/system/initial-prompt.md` | Updated authority header (verified) |
| `docs/system/prompt-template.md` | Updated prompt template (verified) |
| `docs/system/outputs/README.md` | Outputs directory governance (**not updated — gap**) |
| `docs/system/issues.md` | Loop templates and approval semantics |
| `docs/system/outputs/2026-02-10__18__system__continue-repo-scan-summary.md` | Pre-execution scan |
| `docs/system/outputs/2026-02-10__19__system__output-artifact-repo-scan.md` | Pre-execution scan |
| Git commit `09799f2` | P-016 implementation commit |

---

## Pending Item Status

P-016 remains in **Pending** in `docs/system/pending-items.md`. No status
changes were made per verification instructions.
