# Pending Items Archive

Archived pending items that no longer need to be referenced by the builder.

---

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

### P-002 — issue-resolution.md Requires Diff to Reflect Corrected Loop Semantics
- Source: Output File System Issue loop
- Captured: 2026-02-10
- Summary:
  issue-resolution.md does not currently reflect the clarified execution model:
  - proposals uncommitted
  - approval triggers execution
  - verification is separate
  - approved-with-updates semantics
- Notes:
    Requires a diff/update pass, not in scope of current Issue loop.

### P-012 — Automated builder — completion definition and guardrails
- Source: System architecture clarification
- Captured: 2026-02-10
- Completed: 2026-02-12
- Summary:
  Define the completion criteria and non-negotiable guardrails for finishing
  the automated builder, independent of any downstream generator.
- Notes:
    Completion authorized by PASS verification (`2026-02-12__03__system__p-012-verification.md`).
    Content codified in `builder.md` v1.2 — Definition of Done (6 criteria),
    Minimal Architecture Guardrails (6 invariants), and Builder Completion Non-Goals.

### P-015 — Verification template — add Pending item context (not inventory-only)
- Source: Verification workflow gap
- Captured: 2026-02-10
- Completed: 2026-02-10
- Summary:
  Update verification template to include Pending-item context fields (P-###, target file(s), proposal artifact, acceptance checks) so verification works for non-inventory changes as well.
- Notes:
    Verification template updated to include Pending-item context and shift completion authority to verification; dogfooded on P-016.

### P-016 — Enforce output artifact after every Claude iteration
- Source: Process enforcement gap
- Captured: 2026-02-10
- Completed: 2026-02-10
- Summary:
  Add/clarify system rule that every Claude iteration must produce an output artifact (saved under docs/system/outputs/) to prevent untracked changes and lost work.
- Notes:
    Completion authorized by PASS verification (`2026-02-10__23__system__p-016-re-verification.md`).
    Proposal/approval loop was not used; retroactive approval recorded (`2026-02-10__22__system__p-016-retroactive-approval.md`).

### P-037 — Determine required availability date for Mac Mini (special configuration)
- Source: Infrastructure planning for OpenClaw + local LLM development
- Captured: 2026-02-11
- Completed: 2026-02-12
- Summary:
  Identify when the Mac Mini (special configuration; ~2-week lead time)
  must be ordered to support local LLM experimentation, multi-agent
  OpenClaw testing, and overnight verification loops.
- Notes:
  Decision complete: selected a used Mac Studio instead of proceeding with a
  Mac Mini purchase path.

### P-061 — Survey online Bible study platforms (APIs, BYO integration, and low-cost alternatives)
- Status: Superseded
- Superseded by: P-031 (expanded scope)
- Notes:
  Scope merged into expanded P-031 to eliminate duplication and
  centralize Bible study platform integration analysis.

### P-083 — Relocate Planner output root to parent projects directory
- Source: System architecture / project organization
- Captured: 2026-02-12
- Completed: 2026-02-12
- Summary:
  Move Planner project planning docs and workflow artifacts from
  automated-builder to parent-level `../<slug>/`. Planning docs (index.md,
  prd.md, roadmap.md, iteration-log.md, phases/) write to `../<slug>/`.
  Workflow artifacts (proposals, approvals, verifications, implementation
  summaries) write to `../<slug>/docs/system/outputs/`. Automated-builder
  system artifacts remain in `docs/system/outputs/` inside automated-builder.
- Notes:
    Completion authorized by verification (this session).
    Proposal artifact: `2026-02-12__04__system__p-083-planner-output-root-approved.md`.
    Implementation summary: `2026-02-12__06__system__p-083-implementation-summary.md`.
    All six authoritative documents updated with correct paths and version bumps.

### P-084 — run-create-project — create project directory + bootstrap required system docs
- Source: Builder execution readiness for devotional-generator
- Captured: 2026-02-12
- Completed: 2026-02-16
- Project: Automated-builder
- Inventory: docs/system/outputs/2026-02-13__01__system__p-084-inventory-proposal-approved.md
- Summary:
  Implement `run-create-project` command to bootstrap new projects with all
  required system documentation. Command creates project directory structure,
  deploys 9 required files from canonical templates (project.yaml, index.md,
  prd.md, roadmap.md, iteration-log.md, builder-manifest.yaml, ai-process.md,
  and .gitkeep files), enforces governance protection rules, and validates
  17-point contract. Project becomes ready for planner/builder execution with
  zero manual setup. Prefix determination required by default; derivation
  available via explicit flag. Templates stored in automated-builder repository;
  project files deployed to sibling directory.
- Inventory Scope (11 Issue-### execution slices):
  - Issue-001: Create template directory and base templates (7 .tmpl files)
  - Issue-002: Implement command scaffolding with parameter parsing/normalization
  - Issue-003: Implement path resolution and sibling validation
  - Issue-004: Implement prefix determination (required by default, derivation opt-in)
  - Issue-005: Create project.yaml identity file FIRST
  - Issue-006: Deploy remaining files with placeholder substitution
  - Issue-007: Implement governance protection validation
  - Issue-008: Deploy project rules pack template
  - Issue-009: End-to-end validation (17 checks) and cleanup
  - Issue-010: Introduce inventory-proposal artifact type (governance)
  - Issue-011: Validate ai-process.md deployment and AI Process Contract
- Validation Requirements:
  - Primary: Confirm all 11 Issue-### items match approved inventory specification
  - Secondary: Confirm run-create-project produces valid project structure
  - All 17 validation checks pass (identity file, governance protection, path invariants)
  - Template deployment successful, no unresolved placeholders
  - Sibling relationship to automated-builder verified
- Notes:
  - Execution proceeds through issue-resolution loop (Issue-### proposal -> approval -> implementation -> summary)
  - Issue-### items are execution slices only (not inserted into pending-items.md)
  - P-084 completion requires successful two-stage validation
  - Completion authorized by two-stage inventory verification: Stage-1 PASS (all 11 Issue-### items match approved inventory), Stage-2 PASS (descriptive scope + system state validated)
  - Stage-1 artifact: `2026-02-16__27__system__p-084-stage1-verification-pass.md`
  - Stage-2 artifact: `2026-02-16__28__system__p-084-stage2-verification.md`


## Moved to Project Docs

## Superseded / Replaced

## Dropped / No Longer Needed
