# Builder v1 Lifecycle Overview

**Version**: 1.0
**Last Updated**: 2026-02-23
**Status**: Draft
**Phase**: builder-v1 Phase 001

---

## Purpose

This document is the authoritative Builder v1 lifecycle overview. It defines how the three-stage lifecycle (Planner → Builder → Verification) operates: what each stage does, how stages transition, and what constitutes a valid STOP condition at each stage.

This document sits above the stage-specific prompts (`run-planner.md`, `run-builder.md`, `prompts/verification/run-verification.md`). Those prompts are the execution layer; this document is the lifecycle framework they operate within.

This document does not modify the checkpoint taxonomy (`docs/implementation/system/checkpoint-taxonomy.md`), which defines the verification gate sequence that governs all stage executions.

---

## Stage Definitions

### Stage 1: Planner

**Role**: Produce approved, implementation-ready phase plans. The Planner is the planning authority — it defines what will be built but does not build it.

**Entry Condition**:
- Human has initiated a planning session with a project slug and goal
- No uncommitted changes exist in the project planning directory
- Planner has read and understood all required governance documents

**Allowed Actions**:
- Create and edit markdown documentation
- Define requirements, acceptance criteria, and scope boundaries
- Specify phase plans with explicit commit points (CP1, CP2, ...)
- Propose file structures and directory layouts
- Document rollback procedures and verification steps

**Prohibited Actions**:
- Running commands (bash, scripts, git operations)
- Creating code or executable files
- Enabling hooks, agents, workflows, or automation
- Modifying governance files
- Modifying files outside the project's declared write scope
- Modifying any artifact marked `<!-- APPROVED -->`

**Outputs**:
- `index.md` — project navigation and status
- `prd.md` — product requirements document
- `roadmap.md` — phases, milestones, dependencies
- `iteration-log.md` — planning evolution tracking
- `phases/NNN-*.md` — phase plan files with explicit commit points
- Planning output artifact in `../<slug>/docs/system/outputs/`

**Exit Condition**:
- All required planning documents exist and are complete
- Every phase plan contains explicit commit points with files-to-stage, commit command, verification steps, and rollback instructions
- Output artifact written and committed
- Human review requested (Gatekeeper or human approval required before Builder stage begins)

---

### Stage 2: Builder

**Role**: Execute approved phase plans by creating artifacts, committing changes, and maintaining quality. The Builder is the execution authority — it does what the plan says, exactly as written, and nothing beyond it.

**Entry Condition**:
- Phase plan file exists and carries the approval marker (`<!-- APPROVED -->`)
- `builder-manifest.yaml` is valid and all declared paths resolve
- Roadmap prerequisite phases are complete
- Target repository working tree is clean
- Session invoked with `mode=apply` and `session_authority=repo-rw`
- All 10 pre-build validation checks pass (per `prompts/builder/run-builder.md`)

**Allowed Actions**:
- Create and modify files declared in the phase plan's commit points
- Execute `git add` and `git commit` as specified in commit points
- Write build report to `docs/system/outputs/` in the builder repo
- Read governance and reference documents
- Run verification commands specified in the phase plan

**Prohibited Actions**:
- Modifying `builder-manifest.yaml`
- Modifying governance files (per `checkpoint-taxonomy.md` CP-2 default list)
- Modifying the phase plan being executed
- Creating or modifying files outside the phase plan's declared scope
- Deleting files not specified in the phase plan
- Pushing to remote
- Merging, rebasing, or amending commits (unless explicitly requested by human)
- Operating on a second project repo

**Outputs**:
- Committed implementation artifacts as declared in each commit point
- Build report in `automated-builder/docs/system/outputs/` following filename format `YYYY-MM-DD__NN__builder__<description>.md`

**Exit Condition**:
- All commit points executed in order
- All CP verification steps passed
- Stub detection scan completed on all newly created files
- Build report written and path confirmed in chat

---

### Stage 3: Verification

**Role**: Validate that Builder output satisfies the phase plan's acceptance criteria and produce a PASS or FAIL verdict. Verification is the quality gate authority — it evaluates but does not implement.

**Entry Condition**:
- Builder session has completed all commit points for the target phase
- Build report exists in `docs/system/outputs/`
- All committed artifacts from the phase exist on disk
- Verification session invoked with reference to the build report and phase plan

**Allowed Actions**:
- Read all committed artifacts and governance documents
- Execute read-only verification commands (file existence checks, grep, git log)
- Evaluate artifact content against acceptance criteria and governance requirements
- Produce a verification artifact in `docs/system/outputs/`

**Prohibited Actions**:
- Modifying any committed artifact
- Modifying governance files
- Making git commits (except for the verification artifact itself)
- Fixing issues found during verification (document and escalate; do not fix)

**Outputs**:
- Verification artifact in `automated-builder/docs/system/outputs/` following filename format `YYYY-MM-DD__NN__verification__<description>.md`
- Verdict: PASS or FAIL (never partial or conditional)
- If FAIL: remediation path specifying which stage must act and what criteria must be satisfied before re-verification

**Exit Condition**:
- All acceptance criteria evaluated (no skipped checks)
- Verdict determined: PASS or FAIL
- Verification artifact written and committed
- If PASS: handoff to Gatekeeper
- If FAIL: remediation path documented; handed off to appropriate stage

---

## Stage Transitions

### Transition 1: Planner → Builder

| Field | Detail |
|-------|--------|
| **Trigger** | Human invokes Builder session with an approved phase ID and `mode=apply` |
| **Gate** | Phase plan carries `<!-- APPROVED -->` marker; all 10 pre-build validation checks pass |
| **Handoff Artifact** | Phase plan file (`phases/NNN-*.md`); `builder-manifest.yaml` |

### Transition 2: Builder → Verification

| Field | Detail |
|-------|--------|
| **Trigger** | Builder session completes all declared commit points for the phase |
| **Gate** | Build report written to `docs/system/outputs/`; all CP verification steps passed; no unresolved HARD stop conditions |
| **Handoff Artifact** | Build report (in `docs/system/outputs/`); committed phase artifacts |

### Transition 3: Verification → Gatekeeper (PASS)

| Field | Detail |
|-------|--------|
| **Trigger** | Verification session produces a PASS verdict |
| **Gate** | Verification artifact written and committed; all acceptance criteria evaluated with PASS outcome |
| **Handoff Artifact** | Verification artifact (in `docs/system/outputs/`) |

### Transition 4: Verification → Builder (FAIL)

| Field | Detail |
|-------|--------|
| **Trigger** | Verification session produces a FAIL verdict |
| **Gate** | Verification artifact written and committed; remediation path explicitly documented |
| **Handoff Artifact** | Verification artifact with FAIL verdict and remediation instructions; list of failed checks with evidence |

---

## STOP Conditions

### Planner Stage

| ID | Condition | Stop Type | Recovery Path |
|----|-----------|-----------|---------------|
| P-S1 | Required input missing (slug, goal, requirements) | HARD | Obtain missing input from human; do not begin work until all inputs are present |
| P-S2 | An artifact marked `<!-- APPROVED -->` would need to be modified | HARD | Do not modify. Propose revision in chat; await explicit human approval before any change |
| P-S3 | Scope expansion beyond original goal is required | SOFT | Document the expansion. Present to human. Proceed only with documented approval |
| P-S4 | Governance file would need modification to complete planning | HARD | Halt. Escalate with specific explanation of what governance change is needed and why; await human decision |

### Builder Stage

| ID | Condition | Stop Type | Recovery Path |
|----|-----------|-----------|---------------|
| B-S1 | Any pre-build validation check fails (checks 1–10) | HARD | Do not proceed. Report the specific failed check to human; await resolution |
| B-S2 | Commit point verification step fails | HARD | Halt immediately. Execute rollback per CP's declared rollback instructions. Write error report. Report last successful CP to human |
| B-S3 | Scope expansion required (work needed outside phase plan's declared scope) | HARD | Halt. Document exactly what additional scope is needed and why. Do not proceed until scope is approved via a revised phase plan |
| B-S4 | A prohibited action appears necessary to continue | HARD | Halt. Escalate: state what action is needed, why it appears necessary, and what options exist |
| B-S5 | Phase plan contains ambiguous, contradictory, or incomplete instructions | HARD | Halt. Document the specific ambiguity. Do not interpret or guess; escalate to human |
| B-S6 | An approved artifact in the target repository would be modified | HARD | Halt. Approved artifacts are immutable. Escalate with specific artifact path and proposed change |

### Verification Stage

| ID | Condition | Stop Type | Recovery Path |
|----|-----------|-----------|---------------|
| V-S1 | Build report not found in `docs/system/outputs/` | HARD | Halt. Cannot verify without build report. Confirm Builder session completed and report was committed |
| V-S2 | A required implementation artifact is missing from the repository | HARD | Halt. Document missing artifact. Write FAIL verdict with the missing artifact as the remediation target |
| V-S3 | Verdict cannot be determined (acceptance criteria are ambiguous or missing) | HARD | Halt. Escalate to human with the specific criteria that are ambiguous. Do not produce a PASS verdict under uncertainty |
| V-S4 | A fix is required to resolve a failing check | HARD | Halt. Verification does not fix — it reports. Write FAIL verdict with remediation path pointing to Builder or Planner |

---

## Iteration Protocol

### FAIL Verdict Path (Verification → Builder Revision)

When Verification produces a FAIL verdict:

1. **Verification** writes FAIL artifact with: verdict, all failed checks with evidence, and remediation path (which stage must act and what specific criteria must be satisfied)
2. **Human** reviews FAIL artifact and decides: fix via Builder revision, or escalate
3. **Builder** is re-invoked (with a revised phase plan if the failure was a plan issue, or with the same plan if the failure was an implementation quality issue)
4. **Builder** produces a new build report
5. **Verification** is re-invoked against the new build report
6. Cycle repeats until PASS or until maximum iteration depth triggers escalation

### REVISE Decision Path (Gatekeeper → Planner Revision)

When Gatekeeper issues a REVISE decision after a PASS verification:

1. **Gatekeeper** writes REVISE decision with: specific issues, required changes, and explicit criteria for what constitutes an acceptable revision
2. **Planner** is re-invoked; revises the relevant planning artifacts and increments the iteration log
3. **Planner** produces a new output artifact and requests re-review
4. **Gatekeeper** reviews and issues a new decision (APPROVE or REVISE)
5. Cycle repeats until APPROVE or REJECT

### Maximum Iteration Depth — Escalation

If three or more full iterations of the same iteration path fail to converge (same FAIL criteria recurring, or same REVISE issues unresolved):

1. **Halt**: Do not initiate another iteration automatically
2. **Document**: Record all iteration artifacts, the recurring failure pattern, and what has not been resolved across iterations
3. **Escalate to human**: Present the full iteration history and request an explicit decision on path forward
4. **Human decides**: continue with a modified approach (new plan revision), change scope, or abandon the phase

---

## Governance Boundaries

Governance files are files that define rules, constraints, contracts, and authority boundaries that sessions operate *under*, not *on*. They are declared read-only at the start of every session (CP-2: GOVERNANCE-LOCK in `docs/implementation/system/checkpoint-taxonomy.md`) and must not be modified during any stage.

The authoritative default governance file list is defined in `docs/implementation/system/checkpoint-taxonomy.md` (Section 3.3, CP-2). This document does not restate or extend that list.

Project scope files are files that a stage creates or modifies as part of its declared work. The boundary is explicit: if a file is in the governance lock list, it is governance scope; if it is declared in the phase plan's commit points, it is project scope. Any file in neither category must not be touched.

Full specification of allowed write paths per stage, governance file enumeration, governance leakage detection rules, and write-time validation rules is defined in `docs/implementation/system/artifact-discipline.md` (builder-v1 Phase 003). Until that document exists, sessions must apply conservative judgment: when in doubt about whether a write is permitted, halt and escalate.

This document does not modify `docs/implementation/system/checkpoint-taxonomy.md`.

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-23 | Initial lifecycle overview — builder-v1 Phase 001 |
