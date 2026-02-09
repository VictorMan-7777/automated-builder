# Fix C Implementation Summary

**Date:** 2026-02-09
**Status:** Implemented
**Commit:** `586d740` — `docs(implementation): expand CP-2 default governance file list`
**Source:** Architecture Review Pass 1 (Finding 1), Fix C Proposal (`2026-02-09__06__system__fix-c-governance-lock-list-expansion.md`)

---

## What Changed

In `docs/implementation/system/checkpoint-taxonomy.md`, the CP-2 (GOVERNANCE-LOCK) default governance file list was expanded from 4 files to 10 files. An inclusion criterion was added.

### Previous list (4 files)

- `docs/system/access.md`
- `docs/system/initial-prompt.md`
- `docs/system/prompt-template.md`
- `prompts/planner/run-planner.md`

### New list (10 files)

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

### Inclusion criterion added

> A file belongs in this list if it defines rules, constraints, contracts, or authority boundaries that sessions operate *under* rather than *on*.

## Why

The previous 4-file list left 6 governance-authority files unprotected. A session could modify `git.md`, `identity.md`, `CLAUDE.md`, the taxonomy itself, or `run-builder.md` without triggering a governance lock violation. The builder invocation template (`run-builder.md`) was asymmetrically unprotected while `run-planner.md` was locked.

## What Was NOT Changed

- No other section of the checkpoint taxonomy was modified.
- The `<!-- STATUS: APPROVED -->` marker is preserved.
- Verification criteria, pass/fail conditions, evidence requirements, and applicability for CP-2 remain identical.
- `docs/system/outputs/README.md` was deliberately excluded from the list (sometimes the subject of legitimate maintenance work; can be added per-session via override).
