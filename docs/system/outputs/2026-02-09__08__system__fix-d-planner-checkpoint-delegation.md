# Fix D Proposal — Pending Approval

**Date:** 2026-02-09
**Status:** Pending approval
**Source:** Architecture Review Pass 1 (`2026-02-09__01__system__architecture-review-pass-1.md`), Finding 2
**Severity:** HIGH
**Scope:** Single-file clarification to an APPROVED document

---

## 1) The Contradiction

Three checkpoints in the taxonomy require terminal commands:

| Checkpoint | What it requires | Commands implied |
|------------|-----------------|------------------|
| CP-1 PRECHECK | Verify branch, working tree status, upstream sync | `git branch`, `git status`, `git fetch` |
| CP-8 COMMIT-PREPARE | Stage files and execute commit | `git add`, `git commit` |
| CP-9 POSTCHECK | Verify clean tree post-commit | `git status` |

The taxonomy declares applicability to planner sessions:

> `docs/implementation/system/checkpoint-taxonomy.md:9` — "Applies To: All system sessions (Planner, Builder)"

> `checkpoint-taxonomy.md:411` — "CP-1 PRECHECK | Planner Session: Verify planning branch."

> `checkpoint-taxonomy.md:418` — "CP-8 COMMIT-PREPARE | Planner Session: Docs-only commit."

> `checkpoint-taxonomy.md:88` — "Applicability: Planner: yes. Builder: yes." (CP-1)

> `checkpoint-taxonomy.md:294` — "Applicability: Planner: yes. Builder: yes." (CP-8)

But the planner role definition prohibits all commands:

> `prompts/planner/planner-base.md:43-48` — "YOU MUST NOT: Run any commands / Execute any scripts"

> `prompts/planner/run-planner.md:156-162` — "YOU MUST NOT: Run any commands (bash, git, etc.) / Execute any scripts"

A planner session cannot satisfy CP-1, CP-8, or CP-9 without violating its own docs-only constraint. No document specifies an alternative mechanism.

---

## 2) Resolution Approach

**Chosen: Option A — Operator delegation for planner sessions.**

For planner sessions, checkpoints requiring terminal commands (CP-1, CP-8, CP-9) are performed by the session operator (human), not by the planner agent. The planner agent records the operator-provided results as checkpoint evidence.

### Why this approach

- **Preserves docs-only.** The planner's core constraint — no command execution — is maintained without exception. This is the system's strongest separation-of-concerns boundary and should not be weakened.
- **Matches reality.** The human is already present and controlling the session. Running `git status` before starting and `git commit` after planning is natural operator behavior, not an added burden.
- **Minimal change.** One clarifying paragraph in the taxonomy's applicability section. No changes to planner prompts, no changes to checkpoint definitions, no new mechanisms.
- **No slippery slope.** Adding a "read-only git commands" exception to the planner role (Option B) would require modifying 2-3 governance files and would blur the clean docs-only boundary. Future sessions could argue for expanding the exception.

### Why not Option B (allow narrow read-only commands)

Option B would require modifying `planner-base.md`, `run-planner.md`, and `docs/system/run-planner.md` to carve out an exception for read-only git commands. This touches 3 files (vs 1), weakens the docs-only principle, and creates an exception that could be expanded over time. The benefit (slightly more self-contained sessions) does not justify the cost.

---

## 3) Files Affected

**Primary change:**
- `docs/implementation/system/checkpoint-taxonomy.md` — Add an operator-delegation clause to Section 5 (Applicability Matrix).

**No changes required to:**
- `prompts/planner/planner-base.md` — Already correctly prohibits commands. No change needed.
- `prompts/planner/run-planner.md` — Already correctly prohibits commands. No change needed.
- `docs/system/run-planner.md` — No change needed.
- Individual checkpoint definitions (CP-1, CP-8, CP-9) — Their verification criteria remain the same regardless of who performs them.

---

## 4) Rule-Level Change

In Section 5 (Applicability Matrix), after the existing table (line 419) and before the Section 6 heading (line 423), add a subsection clarifying operator delegation:

**Content to add (rule-level description, not literal text):**

- State that for planner sessions, the docs-only constraint means the planner agent does not execute terminal commands.
- State that checkpoints requiring terminal commands (CP-1 PRECHECK, CP-8 COMMIT-PREPARE, CP-9 POSTCHECK) are performed by the session operator for planner sessions.
- State that the planner agent records the operator-provided results as checkpoint evidence.
- State that this does not reduce checkpoint coverage — every checkpoint is still evaluated; only the performer differs.
- State that for builder sessions, the builder agent performs all checkpoints directly (no delegation).

This is a clarification of existing responsibility, not a new rule. The checkpoint definitions, verification criteria, evidence requirements, and pass/fail conditions remain unchanged.

---

## 5) Acceptance Criteria

1. The taxonomy explicitly states who performs terminal-command checkpoints for planner sessions.
2. The planner's docs-only constraint (`planner-base.md`, `run-planner.md`) remains unchanged and uncontradicted.
3. All 9 checkpoints remain applicable to planner sessions (none removed or skipped).
4. Evidence requirements for CP-1, CP-8, and CP-9 remain the same — the evidence is the same regardless of who produced it.
5. Builder sessions are unaffected (builder performs all checkpoints directly).
6. No new mechanisms, tools, or protocols are introduced.

---

## 6) Proposed Commit Message

```
docs(implementation): clarify operator delegation for planner checkpoint commands
```

Single-purpose commit. One file modified (`docs/implementation/system/checkpoint-taxonomy.md`).
