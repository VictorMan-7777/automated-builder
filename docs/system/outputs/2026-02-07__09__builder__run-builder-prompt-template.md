# System Builder MVP — Task 1: run-builder.md Prompt Template

**Output**: 2026-02-07__09__builder
**Type**: Implementation artifact
**Status**: Draft — awaiting human review
**Predecessor**: 2026-02-07__08__planner__system-builder-iteration-2-contracts.md (Iteration 2)

---

## What Was Done

Created `prompts/builder/run-builder.md` — the canonical invocation template
for the System Builder, per Iteration 1 Task 1 and Iteration 2 contracts.

**File created**: `prompts/builder/run-builder.md`
**Files modified**: None
**Files deleted**: None

---

## Template Structure

The template contains seven sections:

### 1. Invocation Parameters

Four required parameters gathered up front:
- `project_repo_root` (absolute path to target project)
- `phase_id` (NNN three-digit format)
- `mode` (dry-run or apply)
- Session authority (`planning-only` for dry-run, `repo-rw` for apply)

### 2. Two-Repo Context

Explicit separation of builder repo (governance, prompts, reports) and project
repo (plans, target artifacts). Includes write-scope rules per repo.

### 3. Prerequisites — Read Order

Five-document read sequence enforced before any execution:
1. identity.md (builder repo)
2. builder.md (builder repo)
3. builder-base.md (builder repo)
4. git.md (builder repo)
5. builder-manifest.yaml (project repo — read-only)

### 4. Execution Steps (5 steps)

1. Read and validate manifest (YAML validity, required fields, version check)
2. Resolve all manifest paths relative to project repo root
3. Locate phase plan matching the NNN phase ID
4. Pre-build validation gate — 10 checks, stop on first failure
5. Execute by mode (dry-run: simulate and report; apply: execute, verify, rollback on failure)

### 5. Prohibited Actions

10 unconditionally prohibited actions matching Iteration 2 section 2.4:
manifest modification, governance modification, phase plan modification,
out-of-scope file changes, unauthorized git operations, multi-project
operation.

### 6. Stop-and-Escalate

Explicit escalation triggers, required reporting format (what/where/need/options),
and prohibited recovery behaviors (no silent retry, no skip, no auto-fix).

### 7. Completion Checklists

Separate checklists for dry-run mode (6 items) and apply mode (8 items).

---

## Authoritative Sources Used

| Source | Commit | Sections Referenced |
|--------|--------|---------------------|
| System Builder MVP plan (Iteration 1) | 8f00e36 | Task 1 scope (section 6), inputs contract (section 2), outputs contract (section 3), review gates (section 4), escalation rules (section 4) |
| Iteration 2 contracts | acc0c53 | Manifest (section 1.2), 10-check validation (section 2.2), dry-run/apply modes (section 2.3), prohibited actions (section 2.4), outputs + provenance (section 3), failure modes (section 4) |
| run-planner.md | — | Structural reference only (heading patterns, checklist style) |

---

## Decisions Made During Implementation

| Decision | Rationale |
|----------|-----------|
| Manifest validation split into Step 1 (read/validate) and Step 2 (resolve paths) | Clearer failure diagnostics — manifest format errors caught before path resolution |
| Phase plan location as its own Step 3 | Separates "find the file" from "validate its contents" (checks 3-6 in the gate) |
| Stub detection patterns listed explicitly (TODO, FIXME, empty bodies, placeholders, hardcoded values) | Iteration 1 section 5.6 says "documented verification step" — explicit patterns are more deterministic than vague guidance |
| Dry-run report includes recommendation field (proceed vs revise) | Supports the dry-run-before-apply workflow described in Iteration 2 section 2.3 |
| Output file naming deferred to iterator in both modes | Per Iteration 2 output conventions and task prompt requirement |

---

## Remaining Tasks (Iteration 1 Phase 1)

| Task | Status | Dependency |
|------|--------|------------|
| Task 1: run-builder.md | **Done** (this session) | — |
| Task 2: builder.md checkpoint types | Pending | None |
| Task 3: builder-base.md system prompt update | Pending | Task 1, Task 2 |
| Task 4: build-report-template.md | Pending | Task 1 |
| Task 5: planning.md CP type conventions | Pending | Task 2 |
| Task 6: dry-run validation | Pending | Tasks 1-5, project repo manifest, approved phase plan |

---

## Authority Request

This artifact is ready for review. To proceed to Task 2, I need:

1. **Human review** of `prompts/builder/run-builder.md`
2. **Explicit authorization** to begin Task 2 (checkpoint type taxonomy in builder.md)

I will not proceed without both.
