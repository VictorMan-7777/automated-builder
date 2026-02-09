# Architecture Review — Core System Coherence (Pass 1)

**Date:** 2026-02-09
**Branch:** `planning/system-builder-mvp`
**Scope:** System governance, execution contract, planner interface
**Reviewer:** Opus (architecture review session)
**Task Reference:** Architecture review before continuing builder tasks

---

## 1) Executive Verdict

**PROCEED WITH FIXES**

The core system is architecturally sound — layered correctly, internally logical in its major design decisions, and auditable in the normal-path case. However, five specific inconsistencies create real enforcement gaps that should be resolved before builder sessions operate under the checkpoint taxonomy. None are system-breaking; all are fixable with scoped documentation edits.

---

## 2) System Map

```
AUTHORITY LAYER (immutable per-session)
├── docs/system/initial-prompt.md     Session Authority Header (access modes, rules)
└── docs/system/access.md             Access mode definitions, output compliance clause

GOVERNANCE LAYER (should be read-only during sessions)
├── docs/system/identity.md           System identity, authority model, default posture
├── docs/system/git.md                Git & commit policy (single source of truth)
├── docs/system/index.md              System overview (roles, workflow, artifact locations)
├── CLAUDE.md                         Repository conventions, naming rules
└── docs/system/outputs/README.md     Output capture rules & naming convention

EXECUTION CONTRACT LAYER
└── docs/implementation/system/checkpoint-taxonomy.md   [APPROVED]
    9 checkpoints (CP-1..CP-9), HARD/SOFT semantics, invariants, evidence requirements

ROLE ENTRYPOINTS
├── prompts/planner/planner-base.md   Planner system prompt (role definition)
├── prompts/planner/run-planner.md    Planner invocation template (steps + checklist)
├── prompts/builder/builder-base.md   Builder system prompt (role definition)
└── prompts/builder/run-builder.md    Builder invocation template (validation + execution)

SUPPORTING DOCS
├── docs/system/run-planner.md        Detailed planner runner guide (system doc)
├── docs/system/session-setup.md      Session setup conventions
├── docs/system/prompt-template.md    Prompt structure conventions
└── docs/system/changelog.md          System documentation changes

OUTPUT LAYER
└── docs/system/outputs/*.md          11 artifacts (2026-02-05 through 2026-02-07)
```

**Responsibility boundaries:**
- Authority layer: Immutable per session. Defines what a session *can* do.
- Governance layer: Read-only during sessions. Defines how the system *works*.
- Execution contract: Defines the checkpoint sequence all sessions *must* follow.
- Role entrypoints: Translate the contract into role-specific operational steps.
- Output layer: Write-only during sessions (new files only). Permanent record.

---

## 3) Contract Consistency Checks

### 3A. Governance Boundary Coherence

**FINDING 1 — Governance lock list is incomplete** (Severity: HIGH)

CP-2 (GOVERNANCE-LOCK) in `checkpoint-taxonomy.md:106-111` defines 4 default governance files:
- `docs/system/access.md`
- `docs/system/initial-prompt.md`
- `docs/system/prompt-template.md`
- `prompts/planner/run-planner.md`

Missing from this list but carrying governance authority:

| File | Why it's governance |
|------|-------------------|
| `docs/system/identity.md` | Authority model, default posture, explicit prohibitions. Referenced as prerequisite by both planner and builder prompts. |
| `docs/system/git.md` | Single source of truth for all commit behavior. Enforced at CP-8. |
| `docs/system/index.md` | System entry point defining roles, workflow, artifact locations. |
| `CLAUDE.md` | Naming conventions, directory structure, scope principles. |
| `docs/implementation/system/checkpoint-taxonomy.md` | The execution contract itself (APPROVED). |
| `prompts/builder/run-builder.md` | Builder invocation template. Note: `run-planner.md` IS locked but `run-builder.md` is NOT — asymmetric. |

**Impact:** A session could modify `identity.md`, `git.md`, or `CLAUDE.md` and still pass all checkpoint verifications. The governance lock would not catch it.

---

**FINDING 2 — Planner command prohibition conflicts with CP-1 and CP-8** (Severity: HIGH)

The checkpoint taxonomy applies to "All system sessions (Planner, Builder)" (`checkpoint-taxonomy.md:9`). CP-1 (PRECHECK) requires verifying branch, working tree status, and upstream sync — operations that require `git` commands. CP-8 (COMMIT-PREPARE) requires staging and committing.

But `planner-base.md:43-48` and `run-planner.md:156-162` state: **"YOU MUST NOT Run any commands (bash, git, etc.)"**

This is a direct contradiction. A planner session cannot satisfy CP-1 or CP-8 without violating its own docs-only constraint. No document specifies who performs these checkpoints on the planner's behalf.

**Impact:** Either planner sessions cannot comply with the taxonomy, or the docs-only rule is implicitly relaxed for checkpoint verification. Neither interpretation is documented.

---

### 3B. Output Compliance Coherence

**FINDING 3 — "System iterator" protocol is undefined** (Severity: HIGH)

Five documents reference the "system iterator" as the authority for output filenames:
- `access.md:88`
- `initial-prompt.md:77`
- `checkpoint-taxonomy.md:251` (CP-7)
- `run-planner.md:135`
- `run-builder.md:151`

No document defines the system iterator as a protocol. The naming convention rules in `outputs/README.md` provide the algorithm (date + sequence + context + description), but the term "system iterator" is never defined as "apply the naming convention rules." This creates ambiguity about whether the assistant is permitted to compute the filename or must wait for an external authority.

**Recommendation:** Define "system iterator" explicitly as the deterministic application of the naming convention rules in `outputs/README.md`. State that the assistant applies the rules directly.

---

**FINDING 4 — Sequence number scoping contradiction** (Severity: MEDIUM)

`docs/system/run-planner.md:361-371` states: *"The sequence number (NN) is monotonic across the repository, not scoped to a single date."*

`docs/system/outputs/README.md:148-149` states: *"Starts at 01 each day. Increments for each new output on same day."*

These are contradictory. The existing files follow the per-day convention (2026-02-07 files restart at `01`).

---

**FINDING 5 — `audit` context used but not canonical** (Severity: LOW)

`outputs/README.md:151-155` defines four valid contexts: `planner | builder | gatekeeper | system`.

Two existing files use `audit`:
- `2026-02-07__03__audit__q1-quote-sourcing.md`
- `2026-02-07__05__audit__q1-quote-sourcing.md`

`audit` is not in the canonical set. This is either vocabulary drift or an undocumented extension.

---

**FINDING 6 — outputs/README.md compliance section uses old naming format** (Severity: LOW)

`outputs/README.md:345`: `"Follow naming convention (YYYY-MM-DD-name.md)"`

This references the pre-changelog naming format. The canonical format (defined in the same file at lines 118-158) is `YYYY-MM-DD__NN__<context>__<description>.md`. The compliance section is inconsistent with its own naming convention section.

---

### 3C. Checkpoint Ordering and Stop Semantics

**FINDING 7 — Checkpoint ordering is sound** (No issue)

The 9-checkpoint sequence flows logically:
1. Validate environment (CP-1)
2. Lock governance (CP-2)
3. Capture inputs (CP-3)
4. Declare plan, get approval (CP-4)
5. Execute work (CP-5, SOFT)
6. Review changes (CP-6)
7. Produce artifact (CP-7)
8. Commit (CP-8)
9. Final verification (CP-9)

Dependencies are correctly ordered. No checkpoint requires state from a later checkpoint.

**FINDING 8 — HARD/SOFT classification is appropriate** (No issue)

Only CP-5 (WORK-EXECUTE) is SOFT. This is the correct choice — it's the only phase where mid-execution human judgment is expected. All structural gates are HARD.

**FINDING 9 — Interrupted sessions have no artifact escape path** (Severity: MEDIUM)

Section 3.2 (`checkpoint-taxonomy.md:56`): *"A checkpoint MUST NOT be entered until all prior checkpoints have passed."*

INV-7 (`checkpoint-taxonomy.md:363`): *"Every session produces a reviewable artifact."*

If CP-5 fails (session abandoned), CP-7 cannot be entered (CP-5 didn't pass). But without CP-7, no artifact is produced, violating INV-7. The session is definitionally a failure that cannot produce its own failure record within the checkpoint framework.

`run-builder.md:184-189` handles this informally: on verification failure, "Write an error report to builder repo docs/system/outputs/." But this bypasses the checkpoint ordering rule. The taxonomy has no formalized "exception path" for incomplete sessions.

---

### 3D. Planner ↔ Contract Alignment

**FINDING 10 — run-planner.md does not reference the checkpoint taxonomy** (Severity: MEDIUM)

`prompts/planner/run-planner.md` has its own 8-step sequence and completion checklist. It predates the taxonomy (2026-02-06 vs 2026-02-07) and was not updated.

The taxonomy claims (`checkpoint-taxonomy.md:418`): *"The checkpoint sequence maps directly onto the existing session flows in both invocation prompts. No changes to those prompts are required."*

This claim is only partially true. The planner prompt does not instruct sessions to:
- Lock governance files or capture baselines (CP-2)
- Record inputs as formal evidence (CP-3)
- Accumulate checkpoint evidence (Section 4.5)
- Perform a diff review (CP-6)
- Perform a final postcheck (CP-9)

A planner session following only `run-planner.md` would be "complete" by the prompt's standards but "incomplete" by the taxonomy's standards.

**FINDING 11 — run-builder.md is better aligned but also doesn't reference the taxonomy**

`prompts/builder/run-builder.md` has a 10-check pre-build validation gate, explicit prohibited actions, stop-and-escalate triggers, and completion checklists. Coverage of taxonomy concerns is substantially better than the planner prompt, but it too doesn't reference or crosswalk to the taxonomy.

---

### 3E. Commit Discipline and Auditability

**FINDING 12 — Artifact + work commit separation is convention, not rule** (Severity: LOW)

The commit history shows a pattern of separate commits for implementation artifacts and their output records:
```
f172976 outputs: add task 2 checkpoint taxonomy draft artifact
5fdbef7 docs(implementation): add checkpoint taxonomy & execution contract (task 2)
```

But `git.md` says "one logical change per commit" without specifying whether the output artifact counts as the same logical change or a separate one. The taxonomy's CP-8 says "single-purpose commit" (singular), while the builder applicability matrix says "Phase execution commit(s)" (plural). Convention exists but isn't codified.

---

## 4) Failure Modes & Escapes

### FM-1: Governance file modified without detection

**Scenario:** A session modifies `docs/system/git.md` (not in the CP-2 lock list). CP-2 passes because `git.md` isn't checked. CP-6 reviews changes against the plan — if the plan included modifying `git.md`, the review passes. CP-9 confirms "governance intact" but only checks CP-2's list.

**Evidence of failure:** `git diff` shows `git.md` changed in a session that shouldn't have touched governance.

**Mitigation:** Expand the default governance file list in CP-2 to include all files that carry governance authority (Finding 1).

---

### FM-2: Planner session skips checkpoint evidence

**Scenario:** A planner session follows `run-planner.md`, produces planning artifacts and an output artifact, and declares completion. The output artifact contains no checkpoint evidence (no CP-1 through CP-9 pass/fail summary) because `run-planner.md` doesn't mention the taxonomy.

**Evidence of failure:** Output artifact lacks checkpoint evidence section. Audit reviewer cannot confirm session followed the taxonomy.

**Mitigation:** Add taxonomy reference and evidence template to `run-planner.md` completion checklist (Finding 10).

---

### FM-3: Filename collisions from contradictory sequence rules

**Scenario:** Two sessions run on the same day. Session A follows `docs/system/run-planner.md` (monotonic across repo, next = `12`). Session B follows `outputs/README.md` (reset per day, next = `01`). Both produce valid filenames by their respective rules, but the filenames conflict.

**Evidence of failure:** Two files exist with the same date but different sequence numbers for similar content, or a sequence gap appears that can't be explained.

**Mitigation:** Resolve the contradiction by selecting one rule (Finding 4).

---

### FM-4: System iterator protocol ambiguity normalizes ad-hoc naming

**Scenario:** Since the system iterator protocol is not explicitly defined, sessions vary in how they determine filenames. Some compute them from the naming rules; others ask the human; others invent them without checking existing files. Over time, non-canonical contexts appear (`audit`, then `review`, `analysis`, etc.).

**Evidence of failure:** Output files with contexts not in the canonical set. Filenames with inconsistent formatting.

**Mitigation:** Explicitly define "system iterator" as the deterministic application of the naming convention rules. Codify the definition in `outputs/README.md` (Finding 3).

---

### FM-5: Interrupted builder session leaves orphaned commits with no artifact

**Scenario:** A builder session in apply mode completes CP1 and CP2 (2 commits in the project repo), then CP3 verification fails. The session halts. CP-7 can't be entered (CP-5 didn't pass). No output artifact is written. The project repo has 2 commits with no corresponding record in the builder repo.

**Evidence of failure:** Project repo has commits with no matching builder report. Builder repo output directory has no entry for the session.

**Mitigation:** Formalize an exception path in the taxonomy for interrupted sessions — allow CP-7 (artifact production) even when CP-5 fails, specifically for failure/abandonment reports (Finding 9).

---

## 5) Required Fixes

### Fix 1: Expand default governance file list

**Scope:** `docs/implementation/system/checkpoint-taxonomy.md:106-111` (APPROVED — requires human-approved revision)

**Action:** Add to the default governance file list:
- `docs/system/identity.md`
- `docs/system/git.md`
- `docs/implementation/system/checkpoint-taxonomy.md`
- `CLAUDE.md`
- `prompts/builder/run-builder.md` (parity with `run-planner.md`)

Consider also: `docs/system/index.md`, `docs/system/outputs/README.md`

**Acceptance criteria:** Every file that carries governance authority is in the default lock list or explicitly excluded with rationale.

---

### Fix 2: Resolve planner command prohibition vs checkpoint requirements

**Scope:** `docs/implementation/system/checkpoint-taxonomy.md` Section 5 (Applicability Matrix) — APPROVED, requires revision. Alternatively, `prompts/planner/run-planner.md` and `prompts/planner/planner-base.md`.

**Action:** Add a clarification to the applicability matrix specifying that for planner sessions, CP-1 (PRECHECK) and CP-8 (COMMIT-PREPARE) are performed by the session operator (human), not by the planner agent. The planner's evidence record should capture the *results* provided by the operator, not perform the checks itself.

**Acceptance criteria:** A planner session can satisfy all 9 checkpoints without violating the docs-only constraint. The responsibility for git-command checkpoints is explicitly assigned.

---

### Fix 3: Define the system iterator protocol

**Scope:** `docs/system/outputs/README.md` — new section or clarification in existing Naming Convention section.

**Action:** Add an explicit definition: *"The system iterator is the deterministic application of the naming convention rules defined in this document. The session computes the next filename by scanning existing files in `docs/system/outputs/`, finding the highest `NN` for today's date, and incrementing. If no files exist for today, `NN` = `01`. The assistant applies this algorithm directly; no external tool or human confirmation is required."*

**Acceptance criteria:** A session reading `outputs/README.md` can deterministically resolve the next filename. The term "system iterator" has an explicit definition.

---

### Fix 4: Resolve sequence number scoping contradiction

**Scope:** `docs/system/run-planner.md:361-371`

**Action:** Remove or correct the "monotonic across the repository" rule. Replace with the per-day convention that matches `outputs/README.md` and existing practice.

**Acceptance criteria:** One consistent rule for `NN` in all documents. All existing files comply with the surviving rule.

---

### Fix 5: Formalize the interrupted-session artifact path

**Scope:** `docs/implementation/system/checkpoint-taxonomy.md` — Section 3.2 (Ordering Rules) or new Section 3.4.

**Action:** Add an exception clause: *"If a session is abandoned or terminated due to an unrecoverable failure, the artifact production checkpoint (CP-7) may be entered out of order for the sole purpose of recording an abandonment/failure report. The report must document: which checkpoints passed, which failed, and why the session was terminated. All other ordering rules remain in force."*

**Acceptance criteria:** An interrupted session can produce a failure artifact without violating the taxonomy. The artifact's format distinguishes it from a success artifact.

---

## 6) Optional Improvements (Deferrable)

1. **Explicit crosswalk table** between taxonomy CPs and `run-planner.md`/`run-builder.md` steps. Would make the "maps directly" claim verifiable.

2. **Add `audit` to canonical output context list** — or re-categorize the two `audit`-context files under `system` or `gatekeeper`. Low urgency, but prevents further vocabulary drift.

3. **Fix `outputs/README.md` compliance section** — replace `YYYY-MM-DD-name.md` with the canonical `YYYY-MM-DD__NN__<context>__<description>.md` format. Trivial but prevents confusion.

4. **Changelog entry for checkpoint taxonomy** — `docs/system/changelog.md` has no entry for the taxonomy addition (2026-02-07). Adding one would improve the system's own audit trail.

5. **Clarify single-commit vs multi-commit convention** for sessions that produce both working artifacts and their output record. Codify the observed practice (separate commits) or explicitly permit combined commits.

6. **Consolidation opportunity:** `docs/system/run-planner.md` (system doc) and `prompts/planner/run-planner.md` (invocation prompt) have overlapping content. The planner prompt references the system doc as a prerequisite, but they share sections (output rules, iteration procedure, checklists). This isn't broken but creates maintenance overhead.

---

## 7) Audit Trail Test

### 7A. Normal Session — Planner creates planning artifacts

**Setup:**
- Session Authority: `mode = repo-rw`
- Task: Plan a new project `widget-api`
- Branch: `planning/system-builder-mvp`

**Checkpoint walkthrough:**

| CP | Action | Evidence | Result |
|----|--------|----------|--------|
| CP-1 PRECHECK | Operator runs `git status`, confirms branch and clean tree | Branch: `planning/system-builder-mvp`, Status: clean | PASS |
| CP-2 GOVERNANCE-LOCK | Lock 4 default files (per current list), capture baselines | File list + read confirmation | PASS |
| CP-3 INPUTS-CAPTURE | Slug: `widget-api`, Goal: "REST API for widgets", Requirements: [...], Constraints: [...] | Input manifest recorded | PASS |
| CP-4 PLAN | Declare: create `docs/projects/widget-api/` with index, prd, roadmap, iteration-log, phases/001, phases/002. Human approves. | Plan text + approval | PASS |
| CP-5 WORK-EXECUTE | Create 6 markdown files. No scope drift. Governance files untouched. | 6 files created | PASS |
| CP-6 DIFF-REVIEW | 6 new files, each maps to plan step. No orphan changes. Governance baselines match. | Diff summary + mapping | PASS |
| CP-7 ARTIFACT-PRODUCE | Write output artifact per naming rules | Path + naming rule compliance | PASS |
| CP-8 COMMIT-PREPARE | Stage files. Commit per git policy format. | Commit hash + message | PASS |
| CP-9 POSTCHECK | All CPs passed. Tree clean. Governance intact. | Summary table | PASS |

**Artifacts produced:**
- 6 files in `docs/projects/widget-api/`
- 1 output artifact in `docs/system/outputs/`
- Git commit(s)

**Audit trail verdict:** UNAMBIGUOUS. Every checkpoint has evidence. Commits are traceable to the plan. The output artifact records the session.

---

### 7B. Interrupted Session — Builder apply mode, CP3 verification fails

**Setup:**
- Session Authority: `mode = repo-rw`
- Phase: `001`, project repo: `/path/to/widget-api`
- Phase plan has 4 commit points (CP1–CP4)

**Checkpoint walkthrough:**

| CP | Action | Evidence | Result |
|----|--------|----------|--------|
| CP-1 PRECHECK | Verify project repo branch and clean tree | Branch + status | PASS |
| CP-2 GOVERNANCE-LOCK | Lock governance files, capture baselines | File list + hashes | PASS |
| CP-3 INPUTS-CAPTURE | Repo root, phase_id=001, mode=apply, authority=repo-rw | Input manifest | PASS |
| CP-4 PLAN | Declare: execute CP1–CP4 of phase 001. Human approves. | Plan + approval | PASS |
| CP-5 WORK-EXECUTE | CP1 succeeds (commit made). CP2 succeeds (commit made). CP3 fails verification. Halt. Rollback CP3. | CP1 pass, CP2 pass, CP3 fail | **FAIL** |
| CP-6 | Cannot enter (CP-5 failed) | — | SKIPPED |
| CP-7 | Cannot enter per strict ordering | — | SKIPPED |
| CP-8 | Cannot enter | — | SKIPPED |
| CP-9 | Cannot enter | — | SKIPPED |

**State after interruption:**
- Project repo: 2 commits (CP1, CP2). CP3 rolled back.
- Builder repo: **No output artifact** (CP-7 never reached).
- Session transcript: Contains evidence for CP-1 through CP-5(fail).

**Audit trail verdict:** AMBIGUOUS. Project repo has 2 commits with no corresponding builder report. A future auditor seeing these commits cannot determine — from the builder repo alone — what happened. They must locate the session transcript (external to the repo).

**With Fix 5 applied (interrupted-session escape path):**
CP-7 would be entered out of order to produce a failure report. The report would document: CP1–CP2 succeeded, CP3 failed, CP4 not attempted, session abandoned. Audit trail becomes unambiguous.

---

## Files Read During This Review

| File | Purpose in review |
|------|------------------|
| `docs/system/index.md` | System overview, roles, workflow |
| `docs/system/README.md` | Directory index |
| `docs/system/access.md` | Access modes, output compliance clause |
| `docs/system/git.md` | Git & commit policy |
| `docs/system/outputs/README.md` | Output naming convention, capture rules |
| `docs/system/identity.md` | System identity, authority model |
| `docs/system/initial-prompt.md` | Session authority header |
| `docs/system/run-planner.md` | Planner runner guide (system doc) |
| `docs/system/changelog.md` | System documentation changes |
| `docs/implementation/system/checkpoint-taxonomy.md` | Checkpoint taxonomy & execution contract |
| `prompts/planner/planner-base.md` | Planner system prompt |
| `prompts/planner/run-planner.md` | Planner invocation template |
| `prompts/builder/builder-base.md` | Builder system prompt |
| `prompts/builder/run-builder.md` | Builder invocation template |
| `CLAUDE.md` | Repository conventions (loaded via system context) |

---

## Review Metadata

- **Findings:** 12 (3 HIGH, 3 MEDIUM, 3 LOW, 3 no-issue confirmations)
- **Required fixes:** 5
- **Optional improvements:** 6
- **Failure modes identified:** 5
