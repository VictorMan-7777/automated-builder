# Output Requirement Rule Change: Remove "Only If Long" Heuristic

**Type**: Governance Decision
**Date**: 2026-02-07
**Scope**: Output write policy in `access.md` and `initial-prompt.md`

---

## Decision

Replace the length-based heuristic ("save outputs only if long") with a clear,
deterministic rule:

> Outputs must be created for **any session producing a reviewable artifact**
> (plans, audits, decisions, governance guidance), **regardless of length**.

---

## Rationale

The previous heuristic — save to `docs/system/outputs/` only when output exceeds
comfortable chat readability — created ambiguity:

1. **Subjective threshold.** "Too long for chat" depends on context, screen size,
   and reader preference. Different sessions applied the rule inconsistently.
2. **Lost short artifacts.** Short but substantive outputs (e.g., a concise audit
   decision or a one-paragraph governance ruling) were not captured, even though
   they carry the same permanent-record value as longer artifacts.
3. **Auditability gap.** The governance trail is incomplete when some reviewable
   artifacts live only in ephemeral chat history.

The new rule eliminates length as the trigger and replaces it with artifact type,
which is unambiguous and aligns with the system's traceability goals.

---

## New Rule Text

Inserted into both `access.md` (Cross-Mode Permissions > Output Writes) and
`initial-prompt.md` (CROSS-MODE PROVISION: OUTPUT WRITES):

- Any session that produces a **reviewable artifact** — defined as a plan, audit,
  decision, or governance guidance document — **must** write that artifact to
  `docs/system/outputs/`.
- Length is not a factor; the obligation is triggered by artifact type, not size.

---

## Additional Clarifications Added

Both governance docs now also state:

1. **Canonical output directory.** `docs/system/outputs/` is the single canonical
   location for output artifacts.
2. **Separation of concerns.** Producing an output artifact is conceptually
   separate from applying doc changes. A session may do both only if its authority
   declaration permits both.
3. **Iterator-managed filenames.** The assistant must not choose or suggest output
   filenames. Filenames are assigned by the system's iterator process.

---

## What Counts as a "Reviewable Artifact"

The following are reviewable artifacts (this list is intentionally closed; do not
expand without a governance decision):

- **Plans** — iteration plans, phase plans, implementation plans
- **Audits** — compliance checks, rule audits, quote-sourcing audits
- **Decisions** — rule changes, scope rulings, governance clarifications
- **Governance guidance** — policy interpretations, process documentation

The following are **not** reviewable artifacts and remain governed by existing
rules:

- Interactive Q&A responses
- Error messages or debugging output
- Quick status updates
- File content displays

---

## Affected Files

| File | Change |
|------|--------|
| `docs/system/access.md` | Updated Output Writes section with new rule, canonical directory, iterator note |
| `docs/system/initial-prompt.md` | Updated CROSS-MODE PROVISION with new rule, canonical directory, iterator note |

No other files were modified in this session.

---

## Edge Cases

- **Sessions that produce only chat responses** (no reviewable artifact): No
  output file required. The new rule does not mandate outputs for every session,
  only for sessions producing reviewable artifacts.
- **Sessions with both doc changes and an artifact**: The output artifact and
  the doc changes are separate deliverables. Both are produced if authority
  permits.
- **Very short artifacts** (e.g., a single-paragraph decision): Must still be
  written to `docs/system/outputs/`. Length is explicitly irrelevant under the
  new rule.
