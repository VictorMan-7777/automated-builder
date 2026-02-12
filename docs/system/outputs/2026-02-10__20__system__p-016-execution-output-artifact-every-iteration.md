# P-016 Execution — Enforce Output Artifact After Every Claude Iteration

**Date**: 2026-02-10
**Context**: system
**Pending Item**: P-016

---

## Summary

Implemented P-016 by replacing the conditional (artifact-type-gated) output
requirement with an unconditional rule: every Claude iteration must produce
an output artifact saved to `docs/system/outputs/`.

The previous rule required output artifacts only when a session produced a
"reviewable artifact" (plan, audit, decision, governance guidance, build
report, review, interruption report, or gap report). Sessions performing
substantive work outside those categories could complete without saving any
output, causing untracked changes and lost work.

The new rule eliminates the artifact-type gate entirely. The obligation is
unconditional — triggered by the existence of a Claude iteration, not by
what kind of artifact it produced.

---

## Changes Applied

### 1. `docs/system/access.md`

**Output requirement rule** (lines 76–80):
- Before: "Any session that produces a reviewable artifact — defined as [type list] — must write that artifact..."
- After: "Every Claude iteration must produce an output artifact... This obligation is unconditional — it is not gated by artifact type, length, or session mode."

**Output compliance clause** (lines 82–85):
- Before: "A qualifying session — one that produced any reviewable artifact — may not be considered complete..."
- After: "A session may not be considered complete until its output artifact exists..."

Preserved: interrupted-session exception, iterator rule, restriction list.

### 2. `docs/system/initial-prompt.md` (v1.1 → v1.2)

**OUTPUT REQUIREMENT RULE** (authority header):
- Before: "Any session that produces a reviewable artifact (plan, audit, decision, or governance guidance) MUST write that artifact..."
- After: "Every Claude iteration MUST produce an output artifact... This obligation is unconditional..."

**OUTPUT COMPLIANCE CLAUSE** (authority header):
- Before: "...if the session produced any reviewable artifact (plan, audit, decision, governance guidance, build report, or review)."
- After: Conditional removed. Clause now reads: "This session will not be considered complete until an output artifact has been created..."

### 3. `docs/system/prompt-template.md` (v1.1 → v1.2)

**Output Compliance (All Modes)** standard instruction block:
- Before: "All prompts that produce reviewable artifacts... MUST include this instruction block"
- After: "All prompts MUST include this instruction block. Every Claude iteration must produce an output artifact — this obligation is unconditional."
- Instruction block text updated to match unconditional rule.

---

## Files NOT Modified

| File | Reason |
|------|--------|
| `prompts/planner/run-planner.md` | Already enforces output every iteration |
| `prompts/builder/run-builder.md` | Already enforces output every iteration |
| `docs/system/issue-resolution.md` | Not a target; verification template excluded per instructions |
| `docs/system/pending-items.md` | P-016 remains in Pending per instructions |

---

## Enforcement Mechanism (Unchanged Structure)

The three-layer enforcement model is preserved:

| Layer | File | Mechanism |
|-------|------|-----------|
| Root authority | `initial-prompt.md` | OUTPUT COMPLIANCE CLAUSE — session-level stop condition |
| Template guidance | `prompt-template.md` | OUTPUT COMPLIANCE block — prompt-level instruction |
| Role-specific checklists | `run-planner.md`, `run-builder.md` | Mandatory checklist items |

The only change is the trigger condition: from "if reviewable artifact produced" to "unconditional."

---

## Verification Criteria

1. All three governance files contain the unconditional rule.
2. The compliance clause applies to every session (no artifact-type gate).
3. Existing enforcement mechanisms preserved.
4. Interrupted-session exception in `access.md` preserved.
5. No unrelated changes introduced.
6. This execution output artifact produced.
7. P-016 remains in Pending.
