<!-- STATUS: APPROVED -->

# Checkpoint Taxonomy & Execution Contract

> **Version:** 1.0
> **Last Updated:** 2026-02-07
> **Status:** Approved
> **Task Reference:** System Builder — Implementation Task 2
> **Applies To:** All system sessions (Planner, Builder)

---

## 1. Purpose

This document defines:

1. The **checkpoint taxonomy** — the ordered sequence of verification gates every system session must pass through.
2. The **execution contract** — the rules governing session inputs, outputs, invariants, stop conditions, and evidence requirements.

Both planner and builder sessions are bound by this specification. Gatekeeper sessions operate under their own review protocol and are outside scope.

---

## 2. Definitions

| Term | Meaning |
|------|---------|
| **Checkpoint** | A named verification gate with pass/fail semantics. |
| **HARD stop** | Checkpoint failure halts the session. No forward progress permitted until resolved or session is abandoned. No bypass, no workaround, no human override during the session. |
| **SOFT stop** | Checkpoint failure pauses execution and records the failure. Forward progress may resume with explicit human approval and a documented rationale. The pause and approval are recorded as evidence. |
| **Evidence** | A verifiable record that a checkpoint was evaluated and its outcome. |
| **Session** | A single invocation of a system role (planner or builder) from start to completion or abandonment. |
| **Invariant** | A condition that must hold true throughout the entire session. |

---

## 3. Checkpoint Taxonomy

### 3.1 Checkpoint Summary

| Order | Checkpoint ID | Name | Stop Type | Purpose |
|-------|--------------|------|-----------|---------|
| 1 | `PRECHECK` | Repository & Environment Validation | HARD | Verify repo, branch, working tree, and environment state. |
| 2 | `GOVERNANCE-LOCK` | Governance File Lock | HARD | Identify governance files and enforce read-only status. |
| 3 | `INPUTS-CAPTURE` | Session Inputs Capture | HARD | Capture, validate, and record all required session inputs. |
| 4 | `PLAN` | Execution Plan Declaration | HARD | Declare scope, steps, expected outputs; obtain approval before work begins. |
| 5 | `WORK-EXECUTE` | Substantive Work Execution | SOFT | Execute the declared plan; enforce scope boundaries during work. |
| 6 | `DIFF-REVIEW` | Change Review | HARD | Review all mutations against the declared plan. |
| 7 | `ARTIFACT-PRODUCE` | Output Artifact Production | HARD | Produce the mandatory reviewable output artifact. |
| 8 | `COMMIT-PREPARE` | Commit Validation & Execution | HARD | Validate and execute the commit per git policy. |
| 9 | `POSTCHECK` | Final Verification | HARD | Verify all checkpoints passed, evidence complete, no side effects. |

### 3.2 Ordering Rules

1. Checkpoints MUST be evaluated in the order specified (1 through 9).
2. A checkpoint MUST NOT be entered until all prior checkpoints have passed.
3. No checkpoint may be skipped, even if its verification is trivially satisfied.
4. If a session requires no commit (e.g., a dry-run), `COMMIT-PREPARE` still executes but validates the no-commit decision rather than a commit.

### 3.3 Checkpoint Definitions

---

#### CP-1: PRECHECK — Repository & Environment Validation

**Stop type:** HARD

**Purpose:** Confirm the session is operating in the correct repository, on the correct branch, with a clean starting state.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Working directory | Matches declared repository root. |
| Git repository | Directory is a valid git repo. |
| Branch | Current branch matches the expected branch for this task. |
| Working tree | Clean (no uncommitted changes, no untracked files in scope). |
| Upstream sync | Local branch is not behind remote (if remote exists). |

**Pass condition:** All checks satisfied.
**Fail condition:** Any check fails → HARD stop. Session cannot proceed.

**Evidence required:**
- Branch name
- Working tree status (clean/dirty)
- Repository root path

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-2: GOVERNANCE-LOCK — Governance File Lock

**Stop type:** HARD

**Purpose:** Enumerate governance files for the session and enforce that none are modified.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Governance file list | Explicitly enumerated from task instructions or system defaults. |
| Lock declaration | Session declares these files as read-only and records the list. |
| Baseline capture | Hash or content snapshot of each governance file at session start. |

**Default governance files** (unless overridden by task instructions):
- `CLAUDE.md`
- `docs/system/access.md`
- `docs/system/git.md`
- `docs/system/identity.md`
- `docs/system/index.md`
- `docs/system/initial-prompt.md`
- `docs/system/prompt-template.md`
- `docs/implementation/system/checkpoint-taxonomy.md`
- `prompts/planner/run-planner.md`
- `prompts/builder/run-builder.md`

**Inclusion criterion:** A file belongs in this list if it defines rules,
constraints, contracts, or authority boundaries that sessions operate *under*
rather than *on*.

**Pass condition:** All governance files identified, declared read-only, baselines captured.
**Fail condition:** Governance file missing, unreadable, or cannot be baselined → HARD stop.

**Evidence required:**
- List of locked files
- Baseline reference (hash or confirmation of read)

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-3: INPUTS-CAPTURE — Session Inputs Capture

**Stop type:** HARD

**Purpose:** Capture and validate every required input for the session before work begins.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Required inputs enumerated | All inputs declared by the task definition or invocation template are listed. |
| Each input present | Every required input has a value (not blank, not placeholder). |
| Each input valid | Inputs conform to expected format/type (e.g., path exists, slug is lowercase-hyphenated). |
| Inputs recorded | All captured inputs are written into session evidence. |

**Planner-specific inputs:** Project slug, project goal, requirements, constraints, sources.
**Builder-specific inputs:** `project_repo_root`, `phase_id`, `mode` (dry-run/apply), session authority.

**Pass condition:** All required inputs present, valid, and recorded.
**Fail condition:** Any required input missing or invalid → HARD stop.

**Evidence required:**
- Input manifest (name-value pairs for all captured inputs)

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-4: PLAN — Execution Plan Declaration

**Stop type:** HARD

**Purpose:** Before any substantive work, declare what the session will do, in what order, and what it will produce. Obtain human approval of the plan.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Scope statement | Session declares what is in scope and what is out of scope. |
| Step sequence | Ordered list of steps the session will execute. |
| Expected outputs | List of files to be created or modified, and the output artifact. |
| Constraints acknowledged | Session explicitly lists constraints from task instructions. |
| Human approval | Plan is presented to the human and explicit approval is received before proceeding. |

**Pass condition:** Plan declared, all fields present, human approval received.
**Fail condition:** Plan incomplete or approval not received → HARD stop.

**Evidence required:**
- Plan text (scope, steps, expected outputs, constraints)
- Approval record (confirmation that human approved)

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-5: WORK-EXECUTE — Substantive Work Execution

**Stop type:** SOFT

**Purpose:** Execute the declared plan. This is the only checkpoint where substantive mutations (file creation, file editing) occur.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Scope enforcement | Every mutation is traceable to the declared plan. No out-of-scope changes. |
| Governance integrity | No governance-locked file has been modified (re-verified continuously). |
| Progress tracking | Work items are tracked and marked complete as they finish. |

**Soft-stop triggers:**
- Unexpected ambiguity in task instructions.
- Scope expansion appears necessary.
- A dependency not anticipated in the plan is discovered.
- An error occurs that the session cannot resolve autonomously.

**On soft stop:** Execution pauses. The issue is presented to the human. If the human approves a resolution (with documented rationale), execution may resume from the pause point. The soft stop, rationale, and approval are recorded as evidence.

**Pass condition:** All planned work completed within declared scope.
**Fail condition (SOFT):** Work cannot complete → pause, escalate, record.

**Evidence required:**
- List of files created or modified
- Soft-stop log (if any pauses occurred): trigger, resolution, approval

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-6: DIFF-REVIEW — Change Review

**Stop type:** HARD

**Purpose:** Review every mutation made during `WORK-EXECUTE` against the declared plan. Catch scope drift, unintended changes, and governance violations.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| All changes enumerated | Every file created, modified, or deleted is listed. |
| Plan alignment | Each change maps to a declared plan step. No orphan changes. |
| Governance intact | Governance file baselines match current state (no modifications). |
| No prohibited files | No changes to files outside declared scope. |
| Content review | Changes are substantively correct (not just present). |

**Pass condition:** All changes align with plan, governance intact, no prohibited mutations.
**Fail condition:** Any orphan change, governance violation, or prohibited file mutation → HARD stop.

**Evidence required:**
- File-level diff summary (files changed, type of change)
- Plan-to-change mapping
- Governance integrity confirmation

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-7: ARTIFACT-PRODUCE — Output Artifact Production

**Stop type:** HARD

**Purpose:** Produce the mandatory reviewable output artifact per the output compliance rules in `docs/system/access.md` and `docs/system/outputs/README.md`.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Artifact exists | A file has been written to `docs/system/outputs/`. |
| Filename compliant | Filename follows `YYYY-MM-DD__NN__<context>__<description>.md` format. |
| Filename sourced correctly | Filename was supplied by the system iterator, not invented by the session. |
| Content complete | Artifact contains the required documentation for this task. |
| Task reference | Artifact clearly references the task it fulfills. |

**Pass condition:** Artifact exists, compliant, complete, and correctly referenced.
**Fail condition:** Artifact missing, non-compliant, or incomplete → HARD stop.

**Evidence required:**
- Artifact file path
- Filename source confirmation (iterator-supplied)

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-8: COMMIT-PREPARE — Commit Validation & Execution

**Stop type:** HARD

**Purpose:** Validate that the commit complies with `docs/system/git.md` and execute it.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| Single-purpose | Commit contains exactly one logical change. |
| Message format | `<type>(<scope>): <description>` per git policy. |
| Files staged correctly | Only files within declared scope are staged. No extras, no omissions. |
| No prohibited files | No governance files, no out-of-scope files. |
| Task reference | Commit message or body references the task. |

**For no-commit sessions (e.g., dry-run):**
- Validate that no mutations were made to the working tree.
- Confirm the decision not to commit is correct per task instructions.

**Pass condition:** Commit is compliant and executed (or correctly omitted).
**Fail condition:** Commit non-compliant → HARD stop. Do not commit.

**Evidence required:**
- Commit hash (or "no-commit" with rationale)
- Staged file list
- Commit message

**Applicability:** Planner: yes. Builder: yes.

---

#### CP-9: POSTCHECK — Final Verification

**Stop type:** HARD

**Purpose:** Final gate confirming the session completed correctly with full evidence.

**Verification criteria:**

| Check | Condition |
|-------|-----------|
| All checkpoints passed | CP-1 through CP-8 each have a recorded PASS. |
| Evidence complete | Every checkpoint's required evidence is present in the session record. |
| Working tree clean | No uncommitted changes remain (post-commit). |
| Governance intact | Final re-verification that governance files are unmodified. |
| No side effects | No unintended files, branches, tags, or state changes. |

**Pass condition:** All checks satisfied. Session is complete.
**Fail condition:** Any check fails → HARD stop. Session is incomplete.

**Evidence required:**
- Checkpoint pass/fail summary (CP-1 through CP-8)
- Final working tree status
- Final governance integrity confirmation

**Applicability:** Planner: yes. Builder: yes.

---

## 4. Execution Contract

### 4.1 Inputs

Every session MUST receive the following before CP-1:

| Input | Source | Required |
|-------|--------|----------|
| Task definition | Context fork or invocation prompt | Yes |
| Repository root path | Session context | Yes |
| Expected branch | Task definition | Yes |
| Governance file list | Task definition or system defaults | Yes |
| Role-specific inputs | Invocation template (run-planner.md or run-builder.md) | Yes |
| Output filename | System iterator | Yes (before CP-7) |

### 4.2 Outputs

Every session MUST produce:

| Output | Location | Checkpoint |
|--------|----------|------------|
| Reviewable output artifact | `docs/system/outputs/` | CP-7 |
| Single-purpose commit | Git history | CP-8 |
| Session evidence record | Embedded in output artifact or session transcript | CP-9 |

### 4.3 Invariants

The following conditions MUST hold true from session start to session end:

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| INV-1 | Governance files are never modified. | Checked at CP-2, CP-6, CP-9. |
| INV-2 | All mutations stay within declared scope. | Checked at CP-5, CP-6. |
| INV-3 | Checkpoint ordering is never violated. | Structural; enforced by sequential evaluation. |
| INV-4 | No output filenames are invented by the session. | Checked at CP-7. |
| INV-5 | No commit contains mixed concerns. | Checked at CP-8. |
| INV-6 | Human approval is obtained before substantive work. | Checked at CP-4. |
| INV-7 | Every session produces a reviewable artifact. | Checked at CP-7, CP-9. |

### 4.4 Stop Conditions

| Condition | Type | Behavior |
|-----------|------|----------|
| HARD checkpoint failure | Mandatory | Session halts. No forward progress. Human must decide: fix and retry from failed checkpoint, or abandon session. |
| SOFT checkpoint failure | Advisory | Session pauses. Issue presented to human. Execution may resume with documented approval. |
| Invariant violation detected | Mandatory | Equivalent to HARD stop at the detecting checkpoint. |
| Unrecoverable error | Mandatory | Session halts. Error documented. Escalate to human. |
| Scope expansion required | Mandatory | HARD stop at CP-5. New scope must be approved via a new CP-4 cycle or session abandoned. |

### 4.5 Evidence Requirements

Every session MUST accumulate evidence as it passes through checkpoints. The minimum evidence set:

| Checkpoint | Evidence |
|------------|----------|
| CP-1 PRECHECK | Branch, working tree status, repo root. |
| CP-2 GOVERNANCE-LOCK | Locked file list, baseline confirmation. |
| CP-3 INPUTS-CAPTURE | Input manifest (all name-value pairs). |
| CP-4 PLAN | Plan text, human approval confirmation. |
| CP-5 WORK-EXECUTE | Files created/modified, soft-stop log (if any). |
| CP-6 DIFF-REVIEW | Diff summary, plan-to-change map, governance confirmation. |
| CP-7 ARTIFACT-PRODUCE | Artifact path, filename source. |
| CP-8 COMMIT-PREPARE | Commit hash, staged files, message. |
| CP-9 POSTCHECK | Checkpoint summary, final tree status, governance confirmation. |

Evidence is recorded in the output artifact (CP-7) and/or the session transcript. The output artifact MUST contain at minimum: the checkpoint pass/fail summary and the task reference.

---

## 5. Applicability Matrix

Both planner and builder sessions follow the same checkpoint sequence. Differences are in the content verified, not the structure:

| Checkpoint | Planner Session | Builder Session |
|------------|----------------|-----------------|
| CP-1 PRECHECK | Verify planning branch. | Verify build branch, manifest. |
| CP-2 GOVERNANCE-LOCK | Same. | Same. |
| CP-3 INPUTS-CAPTURE | Slug, goal, requirements, constraints. | Repo root, phase ID, mode, authority. |
| CP-4 PLAN | Declare planning scope and outputs. | Declare build scope, CPs, expected files. |
| CP-5 WORK-EXECUTE | Create/update planning documents. | Execute commit points, create artifacts. |
| CP-6 DIFF-REVIEW | Review docs changes against plan. | Review code/doc changes against phase plan. |
| CP-7 ARTIFACT-PRODUCE | Planning summary artifact. | Build report artifact. |
| CP-8 COMMIT-PREPARE | Docs-only commit. | Phase execution commit(s). |
| CP-9 POSTCHECK | Same. | Same. |

---

## 6. Compatibility Notes

- **Output compliance:** CP-7 enforces the existing output compliance rules from `docs/system/access.md`. This taxonomy does not alter those rules; it provides the checkpoint at which compliance is verified.
- **Git policy:** CP-8 enforces `docs/system/git.md`. This taxonomy does not alter git policy.
- **Governance protection:** CP-2 and the governance invariant (INV-1) align with the existing governance file protections declared in task instructions and `docs/system/access.md`.
- **Run-planner / run-builder prompts:** The checkpoint sequence maps directly onto the existing session flows in both invocation prompts. No changes to those prompts are required.
