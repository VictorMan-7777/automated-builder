# System Builder MVP — Iteration 2: Contract Alignment & External Project Application Protocol

**Output**: 2026-02-07__08__planner
**Type**: Planning artifact
**Status**: Draft — awaiting human review
**Predecessor**: 2026-02-07__07__planner__system-builder-mvp-plan.md (Iteration 1)

---

## Central Question

> "How does the System Builder safely and predictably operate on a real project repo
> without violating governance, authority boundaries, or provenance?"

This document answers that question by reconciling Iteration 1's contracts with
the concrete reality of an external project repository (the devotional-project-test
repo, as restructured per commit `d694fa5`).

---

## 1. Input Contract Alignment

### 1.1 Problem Statement

Iteration 1 defined inputs using automated-builder-internal paths:

| Iteration 1 Path | Purpose |
|-------------------|---------|
| `docs/projects/<slug>/phases/NNN-*.md` | Phase plans |
| `docs/projects/<slug>/index.md` | Project index |
| `docs/projects/<slug>/prd.md` | PRD |
| `docs/projects/<slug>/roadmap.md` | Roadmap |

The devotional project now exists as a **separate repo** with a different
directory structure (per the reorganization plan in `__06__`):

| Project Repo Path | Purpose |
|--------------------|---------|
| `plans/NNN-*.md` | Phase plans |
| `docs/index.md` | Project index |
| `docs/prd.md` | PRD |
| `docs/roadmap.md` | Roadmap |
| `audits/` | Quality reviews |
| `artifacts/` | Session outputs |

These paths do not match. The builder cannot assume a single path convention.

### 1.2 Resolution: Project Manifest

The builder requires a **project manifest** — a small contract file at a known
location in every target project repo that declares where the builder should
look for inputs.

**File**: `builder-manifest.yaml` (project repo root)

```yaml
# builder-manifest.yaml — System Builder input contract
# This file tells the builder where to find required artifacts.

version: 1
project:
  slug: devotional-generator
  name: "Devotional Generator"

paths:
  index: docs/index.md
  prd: docs/prd.md
  roadmap: docs/roadmap.md
  phases: plans/
  audits: audits/
  artifacts: artifacts/

approval:
  mechanism: marker   # one of: marker | registry
  marker: "<!-- STATUS: APPROVED -->"
```

**Rules**:
- `builder-manifest.yaml` MUST exist before any build session.
- The builder reads this file first, before any other file in the project repo.
- All paths in the manifest are relative to the project repo root.
- If the manifest is missing or malformed, the build session halts immediately.
- The manifest is a **read-only input** to the builder — the builder never
  modifies it.

**Why a manifest instead of convention?** Convention works when all projects
live inside the builder repo. External repos have their own structures. The
manifest decouples the builder's expectations from any single directory layout,
while keeping the contract explicit and auditable.

### 1.3 Supported Directory Structures

The manifest must map to these logical concepts:

| Logical Input | Required? | Description |
|---------------|-----------|-------------|
| `index` | Yes | Project navigation hub |
| `prd` | Yes | Product requirements |
| `roadmap` | Yes | Phase sequence and status |
| `phases` | Yes | Directory containing phase plans |
| `audits` | No | Quality reviews (read-only reference) |
| `artifacts` | No | Session outputs (read-only reference) |

The builder validates that all required paths resolve to existing files or
directories. Optional paths are logged but do not block execution.

### 1.4 What Constitutes an "Approved Plan"

Iteration 1 referenced a `<!-- STATUS: APPROVED -->` HTML comment marker in
phase plan files but the existing phase plans (e.g., `001-data-model-inputs.md`)
do not contain this marker.

**Decision**: The approval mechanism is declared in the manifest.

**Mechanism: `marker`** (default for MVP)
- Phase plan file must contain the exact string declared in `approval.marker`.
- The builder scans the file for this string before executing.
- If not found, the build halts with: "Phase plan NNN is not approved."

**Mechanism: `registry`** (deferred — not MVP)
- A separate file (e.g., `approvals.yaml`) would track approval decisions
  per phase, with timestamps and approver identity.
- This is more robust but adds complexity. Deferred to post-MVP.

**Practical implication**: Before the first build session, a human must add
`<!-- STATUS: APPROVED -->` to the target phase plan file. This is a deliberate
human gate — the marker is placed by the human reviewer after Gatekeeper
approval, not by the builder or planner.

### 1.5 Updated Inputs Contract (supersedes Iteration 1 §2)

| Input | Source | Location | Validation |
|-------|--------|----------|------------|
| Project manifest | Project repo | `builder-manifest.yaml` (root) | Exists, valid YAML, version = 1 |
| Approved phase plan | Project repo | `{manifest.paths.phases}/NNN-*.md` | File exists, approval marker present |
| Project index | Project repo | `{manifest.paths.index}` | File exists, readable |
| PRD | Project repo | `{manifest.paths.prd}` | File exists, readable |
| Roadmap | Project repo | `{manifest.paths.roadmap}` | File exists, readable |
| Session authority header | Prompt preamble | (inline) | `mode = repo-rw`, project repo path declared |

All inputs are **read-validated** before execution begins. If any validation
fails, the session halts with a specific error message naming the missing or
invalid input.

---

## 2. External Repo Application Protocol

### 2.1 How the Builder Reads from an External Repo

The builder session operates with filesystem access to the project repo.
The session authority header must declare the project repo path as the
working root:

```text
SESSION AUTHORITY HEADER — IMMUTABLE FOR THIS SESSION

1. ACCESS MODE DECLARATION
   mode = repo-rw
   working_root = ~/dev/claude-projects/projects/devotional-project-test
```

**Read sequence**:
1. Read `builder-manifest.yaml` from `working_root`
2. Resolve all manifest paths relative to `working_root`
3. Read and validate each required input
4. Read the target phase plan
5. Verify approval marker
6. Parse commit points from the phase plan

The builder **also** reads from the automated-builder repo (its own repo) for:
- System governance docs (authority rules, git policy)
- Build report template
- Builder prompts and system prompts

This means the builder session needs visibility into **two** repos:
the builder repo (for its own instructions) and the project repo (for
the build target). This is handled by the session prompt providing paths
to both.

### 2.2 Input Validation Before Acting

The builder performs a **pre-build validation gate** before executing any
step. This gate is pass/fail with no partial execution:

**Pre-Build Validation Checklist** (updated from Iteration 1):

| # | Check | Source | Fail Action |
|---|-------|--------|-------------|
| 1 | `builder-manifest.yaml` exists and is valid | Project repo root | Halt: "No builder manifest found" |
| 2 | All required manifest paths resolve | Project repo | Halt: "Missing: {path}" |
| 3 | Phase plan file exists | `{phases}/NNN-*.md` | Halt: "Phase plan not found" |
| 4 | Approval marker present in phase plan | Phase plan file | Halt: "Phase NNN not approved" |
| 5 | All commit points parseable (CP1, CP2, ...) | Phase plan file | Halt: "Cannot parse commit points" |
| 6 | Each CP has: files-to-stage, commit command, verification, rollback | Phase plan file | Halt: "CP{N} incomplete" |
| 7 | Prerequisites satisfied (prior phases complete) | Roadmap | Halt: "Prerequisite phase(s) not complete" |
| 8 | Working directory clean | `git status` | Halt: "Uncommitted changes detected" |
| 9 | Branch matches expected build branch | `git branch` | Halt: "Wrong branch" |
| 10 | Session authority = `repo-rw` | Prompt header | Halt: "Insufficient authority" |

All 10 checks must pass. On first failure, execution halts with the
specific error. No partial checks, no "warnings."

### 2.3 Dry-Run vs Apply Modes

**Dry-run mode** (`--dry-run`):
- Performs all pre-build validation (checks 1-10).
- Walks through each commit point and reports what **would** happen.
- Does NOT execute any git commands, create any files, or modify any state.
- Output: A dry-run report written to `docs/system/outputs/` in the
  **builder repo** (not the project repo).
- Authority required: `planning-only` is sufficient for dry-run.

**Apply mode** (default):
- Performs all pre-build validation.
- Executes each commit point sequentially.
- Commits, verifies, and reports after each CP.
- Output: Build report to builder repo `docs/system/outputs/`, plus
  commits and roadmap updates in the project repo.
- Authority required: `repo-rw`.

**Why dry-run matters**: It allows validation of the entire pipeline
(manifest, phase plan, commit points) without touching the project repo.
Iteration 1's "Task 6: Dry-Run Validation" depends on this mode existing.

### 2.4 What the Builder MUST NOT Do Without Additional Authority

The following actions are **unconditionally prohibited** during a build
session, even with `repo-rw` authority:

| Prohibited Action | Reason |
|-------------------|--------|
| Modify the builder-manifest.yaml | Input contract is read-only |
| Modify governance docs in builder repo | Builder operates under governance, not on it |
| Modify files outside the phase plan's declared scope | Plan fidelity — no undeclared changes |
| Delete files not specified in the phase plan | Destructive action requires explicit plan authority |
| Create files not specified in the phase plan | Scope discipline — no surprise artifacts |
| Modify the phase plan itself | The plan is the authority; the builder is the executor |
| Push to remote | Requires explicit human instruction per session |
| Modify git hooks, CI/CD, or automation | Prohibited per git.md |
| Operate on a second project repo | MVP is single-project only |
| Merge branches | Requires explicit human instruction |
| Amend, squash, or rebase commits | Prohibited per git.md unless explicitly requested |

If the builder encounters a situation where one of these actions seems
necessary, it must halt and escalate to the human with a specific
description of what it needs and why.

---

## 3. Outputs + Provenance Rules

### 3.1 Where Builder Outputs Live

Builder outputs are split across two repos by purpose:

| Output | Lives In | Path | Reason |
|--------|----------|------|--------|
| Build report | Builder repo | `docs/system/outputs/YYYY-MM-DD__NN__builder__*.md` | System-level record; permanent audit trail in builder |
| Gatekeeper checklist | Builder repo | (included in build report) | Same as above |
| Git commits | Project repo | (committed to working branch) | Build artifacts belong to the project |
| Roadmap update | Project repo | `{manifest.paths.roadmap}` | Phase status is project state |
| Error report | Builder repo | `docs/system/outputs/YYYY-MM-DD__NN__builder__*.md` | Failure records belong to builder system |

**Rule**: The builder writes **new files** to the project repo only as
specified in the phase plan's commit points. All system/meta outputs
(reports, checklists, errors) go to the builder repo.

**Rationale**: The project repo should contain only project artifacts.
Build orchestration metadata (reports, decisions, errors) is a property
of the builder system, not the project. This also avoids polluting the
project repo's git history with builder infrastructure commits.

### 3.2 How Outputs Reference the Target Project

Build reports must establish provenance by including:

```markdown
## Build Context

| Field | Value |
|-------|-------|
| Project | {manifest.project.slug} |
| Project Repo | {working_root} |
| Phase | {phase_id} |
| Phase Plan | {manifest.paths.phases}/{phase_file} |
| Builder Repo | ~/dev/claude-projects/projects/automated-builder |
| Builder Session | {session_id or date} |
| Manifest Version | {manifest.version} |
```

This creates a bidirectional link:
- **Builder repo → Project repo**: Build report names the project, phase, and
  exact file paths used.
- **Project repo → Builder repo**: Commit messages in the project repo
  reference the build session (e.g., `Built by System Builder session
  2026-02-07__08`).

### 3.3 Provenance Chain

For any artifact produced during a build, the provenance chain is:

```
PRD (what) → Roadmap (sequence) → Phase Plan (how) → Build Report (did) → Git Commits (proof)
     ↑                ↑                  ↑                   ↑                    ↑
  project repo   project repo      project repo         builder repo         project repo
```

Every link in this chain is traceable:
- PRD defines requirements.
- Roadmap sequences phases.
- Phase plan specifies commit points.
- Build report records execution (commits made, verifications passed/failed).
- Git commits in the project repo are the proof of work.

No artifact exists without a traceable origin in this chain.

---

## 4. Failure Modes & Guardrails

### 4.1 Enumerated Failure Cases

#### F1: Missing Phase Plan

**Trigger**: `{manifest.paths.phases}/NNN-*.md` does not exist.
**Builder action**: Halt at pre-build validation, check #3.
**Human action**: Create or correct the phase plan, or update the manifest path.
**Recovery**: Fix the issue, re-run the build session.

#### F2: Phase Plan Not Approved

**Trigger**: Phase plan file exists but approval marker is absent.
**Builder action**: Halt at pre-build validation, check #4.
**Message**: "Phase NNN is not approved. Add `<!-- STATUS: APPROVED -->` after
Gatekeeper review."
**Human action**: Complete the review process, add the marker.
**Recovery**: Re-run the build session.

#### F3: Missing Manifest

**Trigger**: `builder-manifest.yaml` does not exist in project repo root.
**Builder action**: Halt at pre-build validation, check #1.
**Message**: "No builder-manifest.yaml found at {working_root}. Cannot proceed."
**Human action**: Create the manifest file.
**Recovery**: Re-run the build session.

#### F4: Malformed Manifest

**Trigger**: Manifest exists but is not valid YAML or missing required fields.
**Builder action**: Halt at pre-build validation, check #1.
**Message**: "builder-manifest.yaml is invalid: {specific error}."
**Human action**: Fix the manifest.
**Recovery**: Re-run the build session.

#### F5: Prerequisite Phase Not Complete

**Trigger**: Roadmap shows a prior phase as incomplete.
**Builder action**: Halt at pre-build validation, check #7.
**Message**: "Phase {current} depends on Phase {prior}, which is not marked
complete in the roadmap."
**Human action**: Complete the prerequisite phase first, or update dependencies.
**Recovery**: Complete prerequisites, re-run.

#### F6: Commit Point Verification Failure

**Trigger**: After executing a CP, the verification steps fail.
**Builder action**:
1. Halt execution immediately.
2. Rollback the failed CP using its declared rollback procedure.
3. Write an error report to `docs/system/outputs/`.
4. Report to human: what failed, what was rolled back, what CP was last successful.
**Human action**: Investigate failure, revise the phase plan or fix the issue.
**Recovery**: Resume from the last successful CP in a new session.

#### F7: Conflicting Approvals

**Trigger**: Phase plan contains approval marker but the roadmap shows
the phase as "superseded" or a newer version of the phase plan exists.
**Builder action**: Halt at pre-build validation.
**Message**: "Phase NNN has conflicting status: approved in plan file but
{status} in roadmap."
**Human action**: Reconcile the conflict.
**Recovery**: Update roadmap or phase plan to be consistent, re-run.

#### F8: Audit Constraints Blocking Execution

**Trigger**: An audit in `{manifest.paths.audits}` flags a blocking issue
for the target phase.
**Builder action**: The builder does NOT read audits proactively (audits are
reference material, not builder inputs). However, if the phase plan references
an audit as a dependency or the roadmap includes an audit gate, the builder
checks the referenced audit.
**Practical resolution**: Audit constraints are enforced by the Gatekeeper
before the approval marker is placed. If the marker is present, the audit
was already satisfied. This is a governance process, not a builder mechanism.

#### F9: Uncommitted Changes in Project Repo

**Trigger**: `git status` shows dirty working directory.
**Builder action**: Halt at pre-build validation, check #8.
**Message**: "Working directory is not clean. Stash or commit changes before
running a build session."
**Human action**: Commit or stash the changes.
**Recovery**: Re-run.

#### F10: Stub Detection Failure

**Trigger**: After phase completion, stub detection finds TODO comments,
empty implementations, or placeholder content in newly created files.
**Builder action**:
1. Add findings to the build report.
2. Mark the build report recommendation as REVISE (not APPROVE).
3. Escalate to human — stubs indicate incomplete work.
**Human action**: Complete the stubbed content or revise the phase plan.
**Recovery**: New build session to address stubs.

### 4.2 Required Stop Conditions

The builder MUST stop and escalate when:

1. **Any pre-build validation check fails** — no partial execution.
2. **Any CP verification step fails** — rollback that CP, report.
3. **Plan ambiguity discovered** — cannot infer intent, must ask.
4. **Scope expansion needed** — plan is insufficient, cannot add steps.
5. **Unrecoverable error** — full phase rollback, error report.
6. **Builder encounters a prohibited action** — see §2.4.

The builder MUST NOT:
- Retry failed operations silently.
- Skip a failing check to continue.
- Interpret a warning as permission to proceed.
- Auto-fix issues in the phase plan.

### 4.3 Human Review Points

| Review Point | When | What the Human Sees |
|-------------|------|---------------------|
| Pre-build manifest review | Before first build on a new project | `builder-manifest.yaml` — confirm paths are correct |
| Phase plan approval | Before each phase build | Phase plan with approval marker request |
| CP failure escalation | On any CP failure | Error report with rollback status |
| Phase completion review | After all CPs in a phase | Build report with Gatekeeper checklist |
| Dry-run report review | After dry-run mode | What would happen, before it actually does |

---

## 5. GSD Concept Reconciliation (Iteration 2 Pass)

Iteration 1 evaluated seven GSD concepts. Iteration 2 re-evaluates in light
of the external project repo reality.

### 5.1 Multi-Agent Orchestration — REJECT (unchanged)

**Iteration 1 decision**: Reject for MVP.
**Iteration 2 status**: **Still rejected.** The external repo protocol adds
complexity (manifest parsing, cross-repo reads) that makes multi-agent
coordination even less appropriate for MVP. One agent, one repo, one phase.

### 5.2 Command Patterns for Session Invocation — ADOPT (refined)

**Iteration 1 decision**: Adopt. Create `run-builder.md` prompt template.
**Iteration 2 refinement**: The `run-builder.md` prompt must now include:
- Project repo path (working_root) as a required parameter
- Manifest validation as the first step (before plan validation)
- Explicit dry-run vs apply mode selection
- Two-repo context setup (builder repo for governance, project repo for target)

**Updated scope for Task 1** (from Iteration 1 §6):
```
run-builder.md must gather:
  1. Project repo path (absolute)
  2. Phase ID (NNN)
  3. Mode (dry-run | apply)
  4. Authority declaration (must be repo-rw for apply, planning-only for dry-run)

And must perform:
  1. Read builder-manifest.yaml from project repo
  2. Validate manifest
  3. Resolve all paths
  4. Run pre-build validation checklist (10 checks)
  5. Execute or simulate (based on mode)
```

### 5.3 Wave Parallelization — REJECT (unchanged)

**Iteration 1 decision**: Reject for MVP.
**Iteration 2 status**: **Still rejected.** No new information changes this.

### 5.4 Checkpoint Types — ADOPT (refined from "adapt")

**Iteration 1 decision**: Adapt. Three CP types: verification, decision, action.
**Iteration 2 update**: **Promote to ADOPT.** The external repo context makes
CP typing more important, not less. When the builder operates on a separate
project repo, the distinction between "I can verify this myself" and "I need
a human to decide/act" becomes critical because:
- The builder has limited context about the project's external dependencies.
- Decision CPs may involve information outside the repo (e.g., KDP account setup).
- Action CPs may require credentials or access the builder cannot have.

**No design change** — the three types and their builder behaviors remain as
defined in Iteration 1 §5.4. The promotion from "adapt" to "adopt" reflects
increased confidence, not a scope change.

### 5.5 State Management — ADAPT (unchanged)

**Iteration 1 decision**: Adapt. Use build reports for resumption, not STATE.md.
**Iteration 2 status**: **Still adapted.** Build reports in the builder repo's
`docs/system/outputs/` provide the resumption artifact. The cross-repo context
actually validates this decision: state lives in the builder repo (where
orchestration happens), not in the project repo (which should only contain
project artifacts).

### 5.6 Stub Detection — ADOPT (unchanged)

**Iteration 1 decision**: Adopt. Stub detection as a verification step.
**Iteration 2 status**: **Still adopted.** No change needed. The verification
runs against newly created files in the project repo, which works regardless
of where those files live.

### 5.7 Atomic Per-Task Commits — REJECT (already present, unchanged)

**Iteration 1 decision**: Reject (already present via CP system).
**Iteration 2 status**: **Still rejected (already present).** No change.

### 5.8 Iteration 2 Summary Table

| # | GSD Concept | Iter 1 | Iter 2 | Change |
|---|-------------|--------|--------|--------|
| 5.1 | Multi-agent orchestration | Reject | Reject | None |
| 5.2 | Command patterns | Adopt | Adopt | Refined: manifest + two-repo + mode |
| 5.3 | Wave parallelization | Reject | Reject | None |
| 5.4 | Checkpoint types | Adapt | **Adopt** | Promoted: cross-repo makes typing more important |
| 5.5 | State management | Adapt | Adapt | None — build reports confirmed as correct location |
| 5.6 | Stub detection | Adopt | Adopt | None |
| 5.7 | Atomic commits | Reject (present) | Reject (present) | None |

---

## 6. Implementation Readiness Check

### 6.1 What Is Now Locked (after Iteration 2)

These decisions are final and will not be revisited before implementation:

| Decision | Reference |
|----------|-----------|
| Builder reads from external project repos via `builder-manifest.yaml` | §1.2 |
| Manifest is a YAML file at project repo root, version 1 | §1.2 |
| Approval mechanism for MVP is HTML comment marker in phase plan | §1.4 |
| Pre-build validation is 10 checks, all-or-nothing | §2.2 |
| Dry-run and apply are the two execution modes | §2.3 |
| Prohibited actions list for build sessions | §2.4 |
| Builder system outputs go to builder repo, project artifacts go to project repo | §3.1 |
| Build reports include cross-repo provenance fields | §3.2 |
| 10 enumerated failure cases with specific stop-and-escalate behavior | §4.1 |
| CP types are: verification, decision, action (promoted to ADOPT) | §5.4 |
| Build reports serve as resumption artifacts (no STATE.md) | §5.5 |

### 6.2 What Remains Explicitly Deferred

| Deferred Item | Why | Revisit When |
|---------------|-----|--------------|
| Registry-based approval mechanism | MVP uses marker; registry adds complexity | Post-MVP, when multiple approvers or audit trails needed |
| Multi-project builds | MVP is single-project | When a second project needs building |
| Parallel execution / waves | MVP is sequential | When build sessions routinely contain independent work |
| Multi-agent orchestration | MVP is single session | When cost/speed optimization is a priority |
| Automated manifest generation | MVP manifest is human-created | When onboarding friction becomes a problem |
| Builder self-test suite | No code exists yet to test | After first successful build session |
| `approvals.yaml` registry | Marker-based approval is sufficient for MVP | When Gatekeeper needs structured approval records |

### 6.3 Pre-Implementation Checklist

Before Task 1 can begin, these conditions must be true:

- [ ] This Iteration 2 artifact is reviewed and accepted by human.
- [ ] The devotional-project-test repo has been initialized as a git repo
      (per the reorg plan in `__06__`).
- [ ] A `builder-manifest.yaml` file exists in the devotional-project-test repo.
      (This is a human action — the builder does not create its own manifest.)
- [ ] At least one phase plan has the `<!-- STATUS: APPROVED -->` marker.
      (Requires Gatekeeper review of Phase 001.)

**Note**: Items 2-4 can happen in parallel with implementation Tasks 1-5 from
Iteration 1, since those tasks produce builder infrastructure (prompts, docs)
that don't touch the project repo. Task 6 (dry-run validation) requires all
four conditions to be met.

### 6.4 Exact Next Commands (Updated from Iteration 1)

These commands start implementation. **Do not run them now.**

#### Command 1: Implement Task 1 (run-builder.md) — UPDATED

```text
Session Access Declaration:
mode = bootstrap-file
target = prompts/builder/run-builder.md

Task: Create the run-builder.md prompt template per:
- System Builder MVP plan (docs/system/outputs/2026-02-07__07__planner__system-builder-mvp-plan.md), Task 1
- Iteration 2 contracts (docs/system/outputs/2026-02-07__08__planner__system-builder-iteration-2-contracts.md), §2

Key additions from Iteration 2:
- Include builder-manifest.yaml reading as first step
- Include dry-run vs apply mode parameter
- Include project repo path as required input
- Include 10-check pre-build validation (not 6)
- Reference two-repo context (builder repo + project repo)

Use run-planner.md as structural reference. Do not import GSD content.
```

#### Command 2: Implement Task 2 (builder.md update) — UNCHANGED

```text
Session Access Declaration:
mode = bootstrap-file
target = builder.md

Task: Add checkpoint type taxonomy (verification / decision / action) to
builder.md per the System Builder MVP plan, Task 2.
```

#### Command 3: Implement Tasks 3-5 (multi-file updates) — UNCHANGED

```text
Session Access Declaration:
mode = repo-rw

Task: Update builder-base.md, create build-report-template.md, and update
planning.md per the System Builder MVP plan, Tasks 3-5. Commit each update
as a separate CP.

Note: build-report-template.md must include the cross-repo provenance fields
defined in Iteration 2 §3.2.
```

#### Command 4: Implement Task 6 (dry-run validation) — UPDATED

```text
Session Access Declaration:
mode = planning-only

Task: Dry-run the run-builder.md prompt against the devotional-project-test
Phase 001 plan. Use dry-run mode as defined in Iteration 2 §2.3.

Prerequisites (must be true before running):
- devotional-project-test is a git repo
- builder-manifest.yaml exists in devotional-project-test
- Phase 001 has <!-- STATUS: APPROVED --> marker

Produce a validation report to docs/system/outputs/.
```

---

## 7. Authority Request

This Iteration 2 artifact is complete. It reconciles the System Builder MVP's
contracts with the concrete reality of an external project repository.

To proceed to implementation, I need:

1. **Human review** of this artifact.
2. **Explicit authorization**: Authorize implementation of System Builder MVP? (Yes / No)

I will not proceed without both.
