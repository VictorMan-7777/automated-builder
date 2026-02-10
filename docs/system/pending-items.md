# Pending Items

Items captured during active work loops.
No action is taken until explicitly promoted.

---

## Rules

1. Pending item IDs (`P-###`) are stable, never renumbered, and never reused.
2. This file contains exactly two item-state sections: **Pending** (open items) and **Completed** (finished items).
3. New pending items are assigned `max(existing P-###) + 1`.
4. Completed items are moved from Pending to Completed; they are never deleted.
5. A completed item MUST include a completion date line formatted exactly: `- Completed: YYYY-MM-DD`.
6. Pending items are capture-only and do not trigger work unless explicitly promoted.
7. This file is not an Issue tracker and does not start Issue loops.
8. If an instruction requires moving an item to Completed but the **Completed** section does not exist, STOP and report the error instead of partially applying changes.

---

## Pending

### P-002 — issues.md Requires Diff to Reflect Corrected Loop Semantics
- Source: Output File System Issue loop
- Captured: 2026-02-10
- Summary:
  issues.md does not currently reflect the clarified execution model:
  - proposals uncommitted
  - approval triggers execution
  - verification is separate
  - approved-with-updates semantics
- Notes:
    Requires a diff/update pass, not in scope of current Issue loop.

### P-003 — Add proposal-artifact reference requirement to Approval template in issues.md
- Source: Output File System inventory session
- Captured: 2026-02-10
- Summary:
  Update the Approval template to require an explicit proposal artifact
  reference when the proposal is not present in-session, mirroring the inventory
  artifact existence requirement. Do not add search/discovery logic.

### P-004 — Architecture review — next pass planning
- Source: System architecture clarification
- Captured: 2026-02-10
- Summary:
  Perform a full system architecture review AFTER the automated builder is complete.
  This review will assess the planner–builder–verification pipeline as a whole,
  validate architectural assumptions against the completed builder,
  and identify any refactors or systemic improvements before downstream generators
  (e.g., the devotional generator) are built.

### P-005 — Devotional generator — builder planning updates
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  Capture updates and refinements to the devotional generator builder
  plan, including newly identified features or adjustments to the existing
  builder design.

### P-012 — Automated builder — completion definition and guardrails
- Source: System architecture clarification
- Captured: 2026-02-10
- Summary:
  Define the completion criteria and non-negotiable guardrails for finishing
  the automated builder, independent of any downstream generator.

#### Definition of Done — Builder Complete
- The builder can take an approved, planner-produced work packet and execute it
    end-to-end safely, repeatably, and audibly—without manual patching of core
    artifacts.

1. End-to-end execution loop exists
    - Inputs: consumes planner output and governance rules.
    - Execution: applies only approved changes.
    - Outputs: produces audit/summaries and updates tracking files.

2. Write-safety & governance enforcement
    - Approved artifacts are never modified directly (refuse/abort).
    - Writes restricted to explicitly allowed paths.
    - All changes attributable to a builder run.

3. Deterministic, reviewable changes
    - Produces a reviewable diff/change summary.
    - Re-runs with same inputs are stable or differences are explained via
        captured inputs/versioning.

4. Audit trail + run record
    - Records inputs (planner output references / commit hash), files changed,
        checks performed, and outcome.

5. Integrates with pending-items workflow
    - Updates pending-items status explicitly on completion; no silent meaning
        changes.

6. Failure behavior is safe
    - Fails closed; leaves repo in diagnosable state.

#### Non-goals
  - Does not require full verifier automation, downstream generator readiness,
    or performance optimization.

#### Minimal Architecture Guardrails (Must-not-break invariants during builder completion)
1. Approved artifacts are immutable
    - Builder must never modify artifacts marked Approved; hard fail on
        violation; record PASS/FAIL in run output.

2. Explicit write boundaries
    - Builder may write only to explicitly approved target files for the current
        work packet and builder-owned output/audit paths; hard fail on any
        out-of-bounds write.

3. Every run writes an audit record
    - Success or failure, every run produces a run record: timestamp,
        inputs/work packet reference, files changed (or none), outcome, and
        failure reason.

4. Pending-items updates are explicit and attributable
    - Builder updates pending-items only when explicitly targeted; edits must be
        attributable to a specific builder run and limited to targeted items.

5. Fail closed (no partial/ambiguous state)
    - On any violation, stop safely; still write audit output and leave clear
        diagnostics.

6. Planner/builder role separation
    - Builder executes approved instructions only; does not invent new
        requirements or rewrite plans; run record references the planner output
        it executed.

### P-006 — Devotional generator — multi-volume series support (Vol 1–6)
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  Support a devotional series with 6 volumes (Vol 1 overview; Vol 2–6
  topic-specific), each 30 days (Mon–Sat). Generator completes Vol 1 and
  generates Vol 2–6 from a structured plan.

### P-007 — Devotional generator — series-level uniqueness (scripture + quotes)
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  Enforce series-wide uniqueness: no scriptures or quotes used in Volume 1 may
  appear in Volumes 2–6. Track used scriptures/quotes in a registry and
  validate before generation/export.

### P-008 — Devotional generator — one-time spreadsheet import (Vol 1 mapping)
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  One-time ingest of existing spreadsheet mapping (weeks 2–5 scripture + topics
  for Volume 1). Define import format, validation, and mapping into internal
  series plan model.

### P-009 — Devotional generator — one-time Scrivener import (existing draft)
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  One-time ingest of already-written content from Scrivener (Week 1 of Volume 1).
  Define export format and parsing, and mark imported days as locked so
  generator fills only missing days.

### P-010 — Devotional generator — workflow to finish Volume 1 then generate Vol 2–6
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  Workflow: import spreadsheet + Scrivener → generate remaining days in Volume 1
  → generate Volumes 2–6 → enforce series-level uniqueness throughout.

### P-011 — Devotional generator — per-volume KDP-ready export
- Source: Devotional generator planning
- Captured: 2026-02-10
- Summary:
  Export separate KDP-ready PDFs per volume with consistent formatting and
  volume-specific front/back matter; optionally support a series bundle export.

## Completed

### P-001 — Proposal / Approval commit semantics clarification
- Source: Output File System Issue loop
- Captured: 2026-02-09
- Completed: 2026-02-10
- Summary:
  Proposal artifacts should remain uncommitted until approval.
  Approval renames proposal to approved and triggers execution.
- Notes:
    Identified while resolving Issue-001H.

---
