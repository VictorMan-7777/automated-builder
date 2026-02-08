# Run Builder — Entry Prompt

**Version**: 1.0
**Purpose**: Canonical invocation template for System Builder build sessions
**Last Updated**: 2026-02-07

---

## Invocation Parameters

Before proceeding, confirm all four parameters are present in the session prompt.
If any parameter is missing, **stop and ask the human**.

| Parameter | Format | Description |
|-----------|--------|-------------|
| `project_repo_root` | Absolute path | Root directory of the target project repository |
| `phase_id` | NNN (three-digit) | Phase number to build (e.g., `001`) |
| `mode` | `dry-run` or `apply` | Execution mode for this session |
| Session authority | See below | Authority level matching the declared mode |

### Session Authority by Mode

| Mode | Required Authority | Scope |
|------|-------------------|-------|
| `dry-run` | `planning-only` | Read-only access to both repos; no mutations |
| `apply` | `repo-rw` | Read-write access to project repo; read-only to builder repo (except reports) |

If the declared authority does not match the mode, **halt immediately** (validation check 10).

---

## Two-Repo Context

This session operates across two repositories. Understand the distinction before proceeding.

| Repo | Path | Role | Write Scope |
|------|------|------|-------------|
| **Builder repo** | `automated-builder` (this repository) | Governance, prompts, build reports | Build reports to `docs/system/outputs/` only |
| **Project repo** | `{project_repo_root}` | Target artifacts, phase plans, manifest | Commit-point artifacts only (`apply` mode) |

**Rule**: The builder reads governance from the builder repo and build targets
from the project repo. System outputs (reports, checklists) are written to the
builder repo. Project artifacts are written to the project repo only during
`apply` mode, only as specified in commit points.

---

## Prerequisites — Read Order

Read these documents **in this exact order** before any validation or execution.
Do not proceed until you have read and understood each document.

### From the Builder Repo

1. [docs/system/identity.md](../../docs/system/identity.md) — System identity and principles
2. [builder.md](../../builder.md) — Builder role requirements
3. [prompts/builder/builder-base.md](builder-base.md) — Builder system prompt
4. [docs/system/git.md](../../docs/system/git.md) — Git policy

### From the Project Repo

5. `{project_repo_root}/builder-manifest.yaml` — Project manifest (read-only)

After reading the manifest, resolve all paths (Step 2) before reading further
project files.

---

## Execution Steps

Follow these steps in exact order. Do not skip, reorder, or combine steps.

### Step 1: Read and Validate Manifest

Read `builder-manifest.yaml` from `{project_repo_root}`.

Validate:
- [ ] File exists
- [ ] Valid YAML syntax
- [ ] `version` field equals `1`
- [ ] `project.slug` is present and non-empty
- [ ] `paths.index`, `paths.prd`, `paths.roadmap`, `paths.phases` are present
- [ ] `approval.mechanism` is present (must be `marker` for MVP)
- [ ] `approval.marker` string is present and non-empty

If any check fails, **halt**: "builder-manifest.yaml is invalid: {specific error}."

The builder **MUST NOT** modify `builder-manifest.yaml` under any circumstances.

### Step 2: Resolve Paths

Resolve all manifest paths relative to `{project_repo_root}`:

| Logical Input | Manifest Key | Resolved Path |
|---------------|-------------|---------------|
| Project index | `paths.index` | `{project_repo_root}/{paths.index}` |
| PRD | `paths.prd` | `{project_repo_root}/{paths.prd}` |
| Roadmap | `paths.roadmap` | `{project_repo_root}/{paths.roadmap}` |
| Phases directory | `paths.phases` | `{project_repo_root}/{paths.phases}` |

### Step 3: Locate Phase Plan

Find the phase plan file matching `{phase_id}`:

- Search `{project_repo_root}/{paths.phases}` for a file matching pattern
  `{phase_id}-*.md` (e.g., `001-*.md`).
- Exactly one file must match.
- If zero matches: **halt**: "Phase plan not found for phase {phase_id}."
- If multiple matches: **halt**: "Multiple phase plans match phase {phase_id}. Ambiguous — escalate."

### Step 4: Pre-Build Validation Gate

Run all 10 checks **in order**. Stop on the **first failure**. No partial
execution, no warnings-only.

| # | Check | Source | On Failure |
|---|-------|--------|------------|
| 1 | `builder-manifest.yaml` exists and is valid YAML with all required fields | Project repo root | Halt: "No valid builder manifest found at {project_repo_root}" |
| 2 | All required manifest paths resolve to existing files or directories | Project repo | Halt: "Missing: {resolved_path}" |
| 3 | Phase plan file exists in `{paths.phases}/` matching `{phase_id}` | Phases directory | Halt: "Phase plan not found for phase {phase_id}" |
| 4 | Approval marker present in phase plan file | Phase plan file | Halt: "Phase {phase_id} not approved" |
| 5 | All commit points parseable (CP1, CP2, ...) | Phase plan file | Halt: "Cannot parse commit points in phase {phase_id}" |
| 6 | Each commit point defines: files-to-stage, commit command, verification steps, rollback instructions | Phase plan file | Halt: "CP{N} incomplete — missing {field}" |
| 7 | Roadmap prerequisite phases marked complete | Roadmap file | Halt: "Prerequisite phase(s) not complete: {list}" |
| 8 | Project repo working directory clean (`git status`) | Project repo | Halt: "Uncommitted changes detected in project repo" |
| 9 | Correct branch checked out in project repo | Project repo | Halt: "Wrong branch: expected {expected}, found {actual}" |
| 10 | Session authority sufficient for declared mode | Session prompt | Halt: "Insufficient authority: mode={mode} requires {required_authority}" |

**All 10 checks must pass before proceeding to Step 5.**

### Step 5: Execute by Mode

---

#### Dry-Run Mode (`mode = dry-run`)

1. **Report validation results**: Confirm all 10 checks passed. List each
   check with its result.

2. **Simulate commit points**: For each commit point (CP1, CP2, ...) in order:
   - List the files that **would** be created or modified.
   - List the commit message that **would** be used.
   - List the verification steps that **would** run.
   - Flag any potential issues (missing dependencies, ambiguous instructions,
     unclear scope).

3. **Simulate stub detection**: Report any commit points whose outputs appear
   likely to produce stubs, placeholders, or incomplete implementations.

4. **Produce dry-run report**: Write to builder repo `docs/system/outputs/`.
   Do not name the output file — the iterator controls naming.

   Report must include:
   - Build context (project slug, repo path, phase, manifest version, date)
   - Validation results (all 10 checks)
   - Simulated commit point walkthrough
   - Stub detection assessment
   - Issues or risks identified
   - Recommendation: proceed to apply, or revise plan first

5. **Confirm no mutations**: No git commands executed. No files created or
   modified in either repo (except the dry-run report in builder repo).

---

#### Apply Mode (`mode = apply`)

1. **Confirm validation**: All 10 pre-build validation checks passed.

2. **Execute commit points sequentially** (CP1, then CP2, then CP3, ...):

   For each commit point:

   a. **Create or modify files** as specified in the commit point.

   b. **Stage files** using the exact `git add` commands from the plan.

   c. **Commit** using the exact commit message from the plan.

   d. **Verify**: Run the verification steps defined in the commit point.

   e. **On verification success**: Log the result and proceed to the next CP.

   f. **On verification failure**:
      1. Halt execution immediately.
      2. Rollback the failed CP using its declared rollback procedure.
      3. Write an error report to builder repo `docs/system/outputs/`.
      4. Report to human: what failed, what was rolled back, last successful CP.
      5. **Do not proceed.**

3. **Stub detection**: After the final CP, scan all newly created files for:
   - TODO / FIXME / HACK comments
   - Empty function or method bodies
   - Placeholder strings (e.g., "lorem ipsum", "placeholder", "TBD")
   - Hardcoded test values in non-test files

   If stubs detected: add findings to build report, mark recommendation as
   REVISE (not APPROVE).

4. **Produce build report**: Write to builder repo `docs/system/outputs/`.
   Do not name the output file — the iterator controls naming.

   Report must include:

   | Section | Content |
   |---------|---------|
   | Build context | Project slug, project repo path, builder repo path, phase ID, phase plan file, manifest version, session date |
   | Commits made | Hash and message for each commit |
   | Verification results | Pass/fail per CP with details |
   | Stub detection results | Clean or list of findings |
   | Gatekeeper checklist | Completed checklist for review |
   | Recommendation | APPROVE or REVISE with rationale |
   | Resumption instructions | Last successful CP and remaining steps (if incomplete) |

---

## Prohibited Actions

The following actions are **unconditionally prohibited** during any build
session, regardless of mode. No exception.

If any of these actions appears necessary to continue, **halt and escalate**
to the human with a specific explanation of what is needed and why.

| # | Prohibited Action | Reason |
|---|-------------------|--------|
| 1 | Modify `builder-manifest.yaml` | Input contract is read-only |
| 2 | Modify governance docs in the builder repo | Builder operates under governance, not on it |
| 3 | Modify the phase plan being executed | The plan is the authority; the builder is the executor |
| 4 | Modify files outside the phase plan's declared scope | Plan fidelity — no undeclared changes |
| 5 | Delete files not specified in the phase plan | Destructive action requires explicit plan authority |
| 6 | Create files not specified in the phase plan | Scope discipline — no surprise artifacts |
| 7 | Push to remote | Requires explicit human instruction per session |
| 8 | Merge, rebase, or amend commits | Prohibited per git.md unless explicitly requested by human |
| 9 | Modify git hooks, CI/CD, or automation | Prohibited per git.md |
| 10 | Operate on a second project repo | MVP is single-project only |

---

## Stop-and-Escalate

**If at any point during this session you encounter any of the following,
stop immediately and report to the human with specifics.**

Escalation triggers:
- Any invocation parameter is missing or ambiguous
- Any pre-build validation check fails
- Any commit point verification step fails
- The phase plan contains ambiguous, contradictory, or incomplete instructions
- A prohibited action appears necessary to continue
- Scope expansion beyond the phase plan is needed
- An unrecoverable error occurs
- Any situation not explicitly covered by this template

When escalating, **always provide**:
1. What went wrong (specific error or ambiguity)
2. Where it happened (step number, check number, or CP number)
3. What you need from the human to proceed
4. What options exist (if any)

**Do not**:
- Retry failed operations silently
- Skip a failing check to continue
- Interpret a warning as permission to proceed
- Auto-fix issues in the phase plan or manifest
- Guess the intent of ambiguous instructions

---

## Completion Checklist

Before declaring the session complete, verify all applicable items.

**Output compliance**: This session may not stop or declare completion until
the output artifact (dry-run report or build report) exists in
`docs/system/outputs/`. The session must confirm output creation explicitly
in chat, citing the file path. Failure to do so is a session failure.

### Dry-Run Mode

- [ ] All 10 pre-build validation checks passed
- [ ] All commit points simulated and reported
- [ ] Stub detection assessment completed
- [ ] Dry-run report written to builder repo `docs/system/outputs/`
- [ ] Output creation confirmed in chat with file path cited
- [ ] No files were modified in the project repo
- [ ] No git commands were executed against the project repo

### Apply Mode

- [ ] All 10 pre-build validation checks passed
- [ ] All commit points executed successfully
- [ ] All commit point verifications passed
- [ ] Stub detection scan completed on newly created files
- [ ] Build report written to builder repo `docs/system/outputs/`
- [ ] Build report includes all required sections (context, commits, verifications, stubs, checklist, recommendation)
- [ ] Output creation confirmed in chat with file path cited
- [ ] No prohibited actions were taken
- [ ] Ready for Gatekeeper review

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial prompt template per Iteration 1 Task 1 and Iteration 2 contracts |
