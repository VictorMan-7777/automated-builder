# System Builder MVP — Plan

**Output**: 2026-02-07__07__planner
**Type**: Planning artifact
**Status**: Draft — awaiting human review

---

## 1. MVP Definition

### Purpose

The System Builder is the orchestration layer that turns an approved plan into
an executable build session. It bridges the gap between the Planner's output
(approved phase plans with commit points) and the Builder agent's execution
(creating artifacts, committing changes, verifying results).

Today, the Builder role is fully specified in `builder.md` and
`prompts/builder/builder-base.md`, but no system exists to:

- Start a build session from an approved plan
- Feed the Builder the right inputs in the right order
- Enforce authority boundaries during execution
- Capture build state for resumption after interruption
- Produce structured handoff artifacts for the Gatekeeper

The System Builder MVP fills exactly this gap — nothing more.

### Non-Goals

These are explicitly out of scope for the MVP:

- **No parallel execution.** One phase, one plan, one step at a time.
- **No subagent orchestration.** The Builder is a single Claude session, not
  a multi-agent swarm.
- **No model routing.** MVP uses whatever model the session is invoked with.
- **No automation hooks.** No CI/CD, no pre-commit hooks, no webhooks.
- **No cross-project builds.** One project at a time.
- **No self-healing.** On failure, stop and escalate — do not retry or
  auto-recover.
- **No GSD imports.** Reference only; no templates, commands, or code from GSD.

---

## 2. Inputs Contract

The System Builder consumes these artifacts. All must exist before a build
session starts.

### Required Inputs

| Input | Location | Description |
|-------|----------|-------------|
| Approved phase plan | `docs/projects/<slug>/phases/NNN-*.md` | Phase plan with Gatekeeper APPROVE status |
| Project index | `docs/projects/<slug>/index.md` | Navigation hub, project overview |
| PRD | `docs/projects/<slug>/prd.md` | Requirements and acceptance criteria |
| Roadmap | `docs/projects/<slug>/roadmap.md` | Phase sequence and dependencies |
| Session authority header | Prompt preamble | Must declare `mode = repo-rw` |

### Pre-Build Validation Checklist

Before the Builder begins, the System Builder verifies:

1. Phase plan file exists and contains `<!-- STATUS: APPROVED -->` marker
2. All commit points (CP1, CP2, ...) are present with files-to-stage,
   commit command, verification steps, and rollback instructions
3. Prerequisites section lists prior phases as complete (or phase has none)
4. Working directory is clean (`git status` shows no uncommitted changes)
5. Current branch matches the expected build branch
6. Session authority declares `mode = repo-rw`

If any check fails, the build session halts before execution begins.

---

## 3. Outputs Contract

The System Builder produces these artifacts during and after a build session.

### During Build

| Output | Location | Trigger |
|--------|----------|---------|
| Git commits | Repository | At each commit point (CP1, CP2, ...) |
| Status updates | Chat | After each step and commit point |

### On Phase Completion

| Output | Location | Description |
|--------|----------|-------------|
| Build report | `docs/system/outputs/` | Full record: commits, verification results, issues |
| Gatekeeper checklist | Included in build report | Completed checklist for review |
| Updated roadmap | `docs/projects/<slug>/roadmap.md` | Phase marked complete |

### On Failure

| Output | Location | Description |
|--------|----------|-------------|
| Error report | Chat + `docs/system/outputs/` | What failed, rollback status, what authority is needed |
| Rollback state | Repository | All partial changes reverted to last good commit |

---

## 4. Review Gates and Authority Boundaries

### Authority Model

The System Builder operates under the existing session authority header
(`initial-prompt.md`). Key constraints:

- **Mode**: `repo-rw` required — no silent escalation from narrower modes
- **Scope**: Restricted to the declared project's directories plus
  `docs/system/outputs/` for build reports
- **Plan fidelity**: Builder must not deviate from the approved plan; if the
  plan is insufficient, halt and escalate
- **Commit discipline**: Follow commit points exactly — no skipping, combining,
  or adding

### Review Gates

| Gate | When | Who Reviews | Pass Criteria |
|------|------|-------------|---------------|
| Pre-build validation | Before first step | System Builder (automated) | All checklist items pass |
| Per-commit verification | After each CP | Builder (self-check) | Verification steps from plan pass |
| Phase completion | After final CP | Gatekeeper | All acceptance criteria met, checklist complete |
| Failure escalation | On any error | Human | Explicit approval to retry, revise plan, or abort |

### Escalation Rules

1. Verification failure at any CP → halt, rollback that CP, report to human
2. Plan ambiguity discovered during execution → halt, document question, await
   human clarification
3. Scope expansion needed → halt, propose plan revision, await Gatekeeper
   re-approval
4. Unrecoverable error → halt, full phase rollback, error report to human

---

## 5. GSD Concept Mapping

Seven GSD concepts evaluated against the automated-builder context.

### 5.1 Specialized Agent Roles with Model Routing

**GSD pattern**: Orchestrator spawns subagents (planner, executor, verifier,
researcher, debugger) with different model tiers (Opus for planning, Sonnet
for execution, Haiku for read-only).

**Decision**: **Reject for MVP.**
The automated-builder already has clear role separation
(Planner/Builder/Gatekeeper) enforced by session authority. Multi-agent
orchestration within a single build session adds complexity without clear
benefit when builds are sequential. Model routing is a cost optimization that
matters at scale; MVP should prove the workflow first.

### 5.2 Command Patterns for Session Invocation

**GSD pattern**: Structured commands (`/gsd:plan-phase N`,
`/gsd:execute-phase N`) provide consistent entry points and make sessions
reproducible.

**Decision**: **Adopt.**
A `run-builder.md` prompt template (parallel to the existing `run-planner.md`)
gives the Builder a reproducible invocation contract. The prompt gathers
required inputs (project slug, phase ID, authority mode), validates
prerequisites, and sets execution context. This is the single most valuable
structural addition for MVP.

### 5.3 Phased Execution with Wave Parallelization

**GSD pattern**: Plans within a phase are grouped into "waves" that execute
in parallel, with dependencies resolved between waves.

**Decision**: **Reject for MVP.**
MVP builds one phase sequentially. Parallelization is a performance
optimization for later. The wave concept could be revisited when build sessions
routinely contain independent work streams, but that is not the current
reality.

### 5.4 Checkpoint Types (Human-Verify, Decision, Human-Action)

**GSD pattern**: Three distinct checkpoint types formalize what kind of human
involvement is needed — visual confirmation, architectural decision, or
manual action that cannot be automated.

**Decision**: **Adapt.**
The automated-builder's commit points (CPs) already serve as execution
checkpoints, but they conflate "verify the commit worked" with "human must
decide something." MVP should distinguish between:
- **Verification checkpoints** (automated): Did the commit succeed? Do files
  exist? — Builder handles these without stopping.
- **Decision checkpoints** (human): Plan says "choose X or Y" — halt and ask.
- **Action checkpoints** (human): Something the Builder cannot do (e.g.,
  configure an external service) — halt and wait.

This distinction should be expressed in phase plans, not in new system
machinery. The Planner tags each CP with its type; the Builder responds
accordingly.

### 5.5 State Management for Session Resumption

**GSD pattern**: `STATE.md` tracks current execution position, accumulated
decisions, and blockers, enabling context handoff between sessions.

**Decision**: **Adapt.**
Full state files add overhead for MVP. Instead, the build report (written to
`docs/system/outputs/` on completion or failure) serves as the resumption
artifact. It records: last successful CP, remaining steps, any blockers. A new
session reads the build report to pick up where the previous session stopped.
This is lighter than a dedicated state file and leverages the existing output
convention.

### 5.6 Stub Detection and Verification Patterns

**GSD pattern**: Automated checks for placeholder content — TODO comments,
empty implementations, hardcoded returns — to catch incomplete work before
it is declared done.

**Decision**: **Adopt.**
The existing builder verification steps are plan-specific ("run this command,
expect this output"). Adding a generic stub-detection pass after each phase
provides a safety net. MVP implementation: a short checklist in the build
report confirming no stub patterns were detected in newly created files. This
does not require new tooling — just a documented verification step in the
Builder prompt.

### 5.7 Atomic Per-Task Commits

**GSD pattern**: Each task produces exactly one commit immediately after
completion, enabling granular git bisect and blame.

**Decision**: **Reject (already present).**
The automated-builder's commit point (CP) system already enforces atomic
commits. Each CP = one logical unit = one commit. No change needed.

---

## 6. Phase 1 Task List — Planning Milestones

Phase 1 delivers the minimum system needed to run a build session from an
approved plan. All tasks below are planning/documentation tasks — no code.

### Task 1: Create `run-builder.md` Prompt Template

**Milestone**: Builder invocation contract exists.

**Produces**:
- `prompts/builder/run-builder.md` — Entry prompt for build sessions
  (parallel to `prompts/planner/run-planner.md`)

**Scope**:
- Input gathering: project slug, phase ID, authority declaration
- Pre-build validation checklist (automated)
- Execution procedure: step-by-step, CP-by-CP
- Output capture rules (build report to `docs/system/outputs/`)
- Error handling and escalation procedure
- Stub detection verification step

### Task 2: Update `builder.md` with Checkpoint Types

**Milestone**: Builder requirements distinguish verification, decision, and
action checkpoints.

**Produces**:
- Updated `builder.md` v1.2 — New section defining three CP types and
  Builder behavior for each

**Scope**:
- Define CP type taxonomy (verification / decision / action)
- Specify Builder behavior for each type (auto-proceed / halt-and-ask /
  halt-and-wait)
- Update Planner conventions to tag CPs with type in phase plans

### Task 3: Update `builder-base.md` System Prompt

**Milestone**: Builder system prompt reflects MVP contracts.

**Produces**:
- Updated `prompts/builder/builder-base.md` v1.1

**Scope**:
- Reference `run-builder.md` as the entry point
- Add pre-build validation requirement
- Add stub detection verification step
- Add build report output requirement
- Reference CP type taxonomy from updated `builder.md`

### Task 4: Define Build Report Format

**Milestone**: Build output format is standardized.

**Produces**:
- `docs/system/build-report-template.md` — Template for build reports written
  to `docs/system/outputs/`

**Scope**:
- Header: project slug, phase ID, date, Builder session ID
- Body: commits made (hashes + messages), verification results per CP,
  issues encountered, stub detection results
- Footer: Gatekeeper checklist (completed), recommendation (APPROVE/REVISE),
  resumption instructions (if incomplete)

### Task 5: Update Planner Conventions for CP Types

**Milestone**: Planner knows how to tag commit points.

**Produces**:
- Updated `planning.md` — New guidance for CP type tagging in phase plans

**Scope**:
- Define how Planner marks each CP as verification / decision / action
- Provide examples of each type in a phase plan
- Ensure backward compatibility (untagged CPs default to verification type)

### Task 6: Dry-Run Validation

**Milestone**: MVP contracts validated against a real approved plan.

**Produces**:
- Validation report in `docs/system/outputs/` — Walkthrough of the
  `run-builder.md` prompt against the devotional-generator Phase 001 plan
  (or whichever plan is approved first)

**Scope**:
- Trace through each step of the run-builder prompt
- Confirm all inputs are available
- Confirm all outputs are producible
- Identify any gaps or ambiguities
- Recommend revisions if needed

---

## 7. Exact Next Commands

The following commands start implementation. **Do not run them now** — they
require a new session with explicit authority.

### Command 1: Implement Task 1 (run-builder.md)

```text
Session Access Declaration:
mode = bootstrap-file
target = prompts/builder/run-builder.md

Task: Create the run-builder.md prompt template per the System Builder MVP
plan (docs/system/outputs/2026-02-07__07__planner__system-builder-mvp-plan.md),
Task 1. Use run-planner.md as structural reference. Do not import GSD content.
```

### Command 2: Implement Task 2 (builder.md update)

```text
Session Access Declaration:
mode = bootstrap-file
target = builder.md

Task: Add checkpoint type taxonomy (verification / decision / action) to
builder.md per the System Builder MVP plan, Task 2.
```

### Command 3: Implement Tasks 3–5 (multi-file updates)

```text
Session Access Declaration:
mode = repo-rw

Task: Update builder-base.md, create build-report-template.md, and update
planning.md per the System Builder MVP plan, Tasks 3–5. Commit each update
as a separate CP.
```

### Command 4: Implement Task 6 (dry-run validation)

```text
Session Access Declaration:
mode = planning-only

Task: Dry-run the run-builder.md prompt against the first approved phase plan.
Produce a validation report to docs/system/outputs/.
```

---

## 8. Authority Request

This artifact is complete. To proceed to implementation, I need:

1. **Human review** of this plan
2. **Explicit authority** to begin Task 1 (bootstrap-file session for
   `prompts/builder/run-builder.md`)

I will not proceed without both.
