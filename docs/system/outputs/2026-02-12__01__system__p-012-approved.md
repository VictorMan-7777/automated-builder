# P-012 Proposal — Automated Builder Completion Definition and Guardrails

**Pending item**: P-012 — Automated builder — completion definition and guardrails
**Target file**: `builder.md`
**Baseline version**: 1.1
**Proposed version**: 1.2

---

## Context

`builder.md` defines the builder's operational requirements (commit cadence,
rollback, verification, scope control) but does not define when the builder
is **complete** or what architectural invariants must never be broken during
or after completion.

P-012 captures a detailed Definition of Done (6 criteria) and a set of
Minimal Architecture Guardrails (6 must-not-break invariants), plus explicit
non-goals. These are already fully specified in `docs/system/pending-items.md`
under P-012 and need to be codified in the authoritative builder document.

No document other than `builder.md` requires modification. The builder
system prompt (`prompts/builder/builder-base.md`) references `builder.md`
by directive and does not need changes — the new sections become effective
through the existing reference chain.

---

## Scope

Add three new sections to `builder.md`, placed after the existing
"Phase Completion" section and before the existing "Communication" section:

1. **Definition of Done — Builder Complete** — the 6 criteria that define
   when the builder is finished.
2. **Minimal Architecture Guardrails** — the 6 must-not-break invariants
   that apply during and after builder completion.
3. **Builder Completion Non-Goals** — what builder completion explicitly
   does not require.

Version bump `builder.md` from 1.1 to 1.2 with a changelog entry.

---

## Structural Changes

### New section: Definition of Done — Builder Complete

Inserted after "Phase Completion" (currently ending at line 231).

Content reproduces the 6 criteria from P-012 verbatim, reformatted into
`builder.md` style (section heading, numbered list with sub-bullets):

1. End-to-end execution loop exists
2. Write-safety & governance enforcement
3. Deterministic, reviewable changes
4. Audit trail + run record
5. Integrates with pending-items workflow
6. Failure behavior is safe

### New section: Minimal Architecture Guardrails

Inserted immediately after Definition of Done.

Content reproduces the 6 invariants from P-012 verbatim, reformatted:

1. Approved artifacts are immutable
2. Explicit write boundaries
3. Every run writes an audit record
4. Pending-items updates are explicit and attributable
5. Fail closed (no partial/ambiguous state)
6. Planner/builder role separation

### New section: Builder Completion Non-Goals

Inserted immediately after Minimal Architecture Guardrails.

Content reproduces the non-goals from P-012 verbatim:

- Does not require full verifier automation, downstream generator readiness,
  or performance optimization.

### Version and changelog

- Version: 1.1 → 1.2
- Last Updated: 2026-02-12
- Changelog entry: "Add Definition of Done, Minimal Architecture Guardrails, and Builder Completion Non-Goals (P-012)"

---

## Non-Goals of This Proposal

- Does not modify `docs/system/index.md`, `prompts/builder/builder-base.md`,
  or any other file.
- Does not introduce enforcement mechanisms, automation, or runtime checks.
- Does not create new pending items.
- Does not define how the builder will be implemented — only when it is
  considered complete and what invariants it must preserve.
- Does not add governance beyond what P-012 already specifies.

---

## Acceptance Criteria

1. `builder.md` contains a "Definition of Done — Builder Complete" section
   with all 6 criteria from P-012.
2. `builder.md` contains a "Minimal Architecture Guardrails" section with
   all 6 invariants from P-012.
3. `builder.md` contains a "Builder Completion Non-Goals" section matching
   P-012.
4. No content is added, removed, or reinterpreted beyond what P-012
   specifies.
5. Existing sections of `builder.md` are unmodified.
6. Version is bumped to 1.2 with a changelog entry.
7. No other files are modified.

---

## Notes / Assumptions

- The P-012 content in `pending-items.md` is the authoritative source. This
  proposal transfers that content into `builder.md` without reinterpretation.
- Section placement (after "Phase Completion", before "Communication") is
  chosen because completion criteria logically follow the definition of what
  a completed phase looks like, and precede operational concerns like
  status communication.
- The builder system prompt inherits these new sections through its existing
  `Read builder.md` directive — no prompt changes needed.
