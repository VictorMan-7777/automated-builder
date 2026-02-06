# Git & Commit Policy

**Version**: 1.0
**Last Updated**: 2026-02-06

---

## Purpose

This document defines **all git and commit behavior** for the automated-builder repository. It applies to:
- Planning-stage commits (docs-only, active now)
- Execution-stage commits (phase implementation, future)

This is the **single source of truth** for commit rules. Other documents reference this policy but do not restate it.

---

## Commit Types

### 1. Docs-Only Commits (Active Now)

**Allowed during**: Planning stage

**Scope**:
- Planning documents (`docs/projects/<slug>/`)
- System documentation (`docs/system/`)
- Prompts and guidelines (`prompts/`)
- Root documentation (`planning.md`, `CLAUDE.md`, etc.)

**Must NOT include**:
- Code files (`.ts`, `.js`, `.py`, etc.)
- Scripts (`.sh`, `.bat`, etc.)
- Hooks or automation
- Agents or workflows
- Runtime configuration, CI config, or operational settings (unless explicitly approved)

**Examples**:
- Creating planning artifacts for a new project
- Updating system rules or conventions
- Clarifying documentation or fixing contradictions
- Adding or revising prompts

---

### 2. Phase Execution Commits (Future)

**Allowed during**: Builder stage (when active)

**Requirements**:
- Must reference an approved phase ID (e.g., `phase-001`)
- Scope limited to that phase's defined outputs
- Must follow commit points identified in phase plan (CP1, CP2, CP3, ...)
- Must include rollback notes and verification steps

**Example**:
```
feat(project-slug): implement core feature (CP2)

Phase 001, Commit Point 2
- Create feature implementation per phase plan
- Add validation logic
- Add tests for feature behavior

Rollback: git reset --soft HEAD~1
Verification: run test suite per phase plan
```

---

## Commit Boundaries

**One logical change per commit**:
- A single, cohesive unit of work
- Can be described in one sentence
- Achieves a complete, testable outcome

**Prohibited**:
- ❌ Mixed concerns (e.g., "fix bug + update docs + refactor")
- ❌ "Cleanup while here" (unrelated formatting or refactoring)
- ❌ Multiple independent changes bundled together

**Example of good boundaries**:
- ✅ "Add underscore policy exception for system outputs"
- ✅ "Create initial scaffold for project"
- ✅ "Implement feature validation (CP3)"

**Example of bad boundaries**:
- ❌ "Update docs, fix typos, and add new feature"
- ❌ "Various improvements"
- ❌ "WIP commit"

---

## Mandatory Pre-Commit Checks

**Before ANY commit, always**:

1. **Review `git status`**
   - Verify staged files match commit intent
   - Check for unexpected files (leftover debugging, temp files)
   - Confirm no unintended changes included

2. **Confirm file scope**
   - Docs-only commits: Only `.md` files in allowed paths
   - Execution commits: Files match phase plan exactly

3. **Verify compliance**
   - Naming conventions followed (lowercase, hyphen-separated)
   - No prohibited file types included
   - Changes align with commit message

**If anything unexpected appears in `git status`, STOP and clarify before committing.**

---

## Commit Message Format

### Subject Line

```
<type>(<scope>): <short, factual description>
```

**Type** (required):
- `docs` - Documentation changes
- `feat` - New feature (implementation)
- `fix` - Bug fix
- `refactor` - Code restructuring (no behavior change)
- `test` - Test additions or modifications
- `chore` - Maintenance (dependencies, tooling)
- `plan` - Planning artifacts (alternative to `docs`)

**Scope** (required):
- For docs: `system`, `planning`, `prompts`
- For projects: `<project-slug>` (e.g., `devotional-generator`)
- For phases: `<project-slug>` with phase noted in body

**Description** (required):
- Present tense ("add" not "added")
- Lowercase (unless proper noun)
- No period at end
- Max 72 characters

### Body (Optional but Recommended)

- **What** changed
- **Why** it changed
- **Constraints** or non-obvious decisions
- **Rollback** notes (for execution commits)
- **Verification** steps (for execution commits)

### Examples

**Docs-only commit**:
```
docs(system): clarify underscore policy for outputs vs project artifacts

- Clarify no-underscore rule for project artifacts
- Explicitly document double-underscore exception for system outputs
- Resolve documentation contradictions without renaming files
- Docs-only change; no filesystem modifications required
```

**Planning commit**:
```
plan(devotional-generator): create initial planning artifacts

- Add PRD with requirements and acceptance criteria
- Define 5-phase roadmap with milestones
- Document 11 commit points across phases
- Initialize iteration log (iteration 1)

Ready for Gatekeeper review.
```

**Execution commit** (future):
```
feat(project-slug): implement core feature (CP2)

Phase 001, Commit Point 2
- Create feature implementation per phase plan
- Add validation logic
- Add tests for feature behavior

Rollback: git reset --soft HEAD~1
Verification: run test suite per phase plan
```

---

## Prohibited Actions

### No Squashing (Unless Explicitly Requested)
- Preserve commit history for audit trail
- Each commit represents a logical checkpoint
- Squashing loses granular rollback capability

**Exception**: User explicitly requests squashing for specific reason

---

### No Amending Previous Commits (Unless Correcting Error)
- Amending rewrites history
- Breaks traceability for review
- Risk of losing work if not careful

**Exception**: Fixing a typo in most recent commit message (before push)

**Alternative**: Create a follow-up commit with correction

---

### No Mixed Concerns
- One type of change per commit
- Don't bundle unrelated fixes
- Don't "clean up while here" unless that's the commit purpose

**Bad**:
- Commit includes bug fix + docs update + refactor

**Good**:
- First commit: bug fix
- Second commit: related docs update
- Third commit: refactor (if needed)

---

### No Committing Generated Artifacts (Unless Approved)
- Build output (dist/, build/)
- Dependency locks (unless explicit decision to track)
- Generated documentation (unless source of truth)
- IDE-specific files (.vscode/, .idea/)

**Exception**: Explicitly approved artifacts that must be tracked

---

## Automation

### No Git Hooks by Default

**Rule**: No hooks, pre-commit scripts, or automated triggers enabled by default

**Rationale**:
- Transparency (what you see is what runs)
- Predictability (no hidden automation)
- Safety (no accidental executions)
- Explicitness (all actions are intentional)

**Exception**: Only when explicitly approved and documented in advance

---

### No Automation Without Approval

**Rule**: No CI/CD, automated merges, or commit triggers without documented approval

**Process if automation needed**:
1. Document the automation purpose and scope
2. Get explicit approval from human reviewer
3. Document how to disable it
4. Add to `docs/system/automation.md` (if created)

---

## Working Tree Hygiene

**Keep working tree clean**:
- Commit frequently at logical checkpoints
- Use branches for experimental work (if needed)
- Don't accumulate uncommitted changes
- Clean working tree after each commit

**Check status regularly**:
```bash
git status
```

**Expected state**:
- After commit: `nothing to commit, working tree clean`
- During work: Only files related to current task modified

---

## Rollback Procedures

### Undo Last Commit (Before Push)

**Soft reset** (keep changes, unstage commit):
```bash
git reset --soft HEAD~1
```

**Hard reset** (discard changes completely):
```bash
git reset --hard HEAD~1
```

---

### Undo Specific Commit (After Push)

**Revert commit** (create new commit that undoes changes):
```bash
git revert <commit-hash>
```

**Never** use `--force` push to rewrite remote history unless absolutely necessary

---

## Review Checklist

Before committing, verify:

- [ ] `git status` reviewed
- [ ] Staged files match commit intent
- [ ] No unexpected files included
- [ ] Commit message follows format
- [ ] Single logical change (no mixed concerns)
- [ ] Docs-only compliance (if planning stage)
- [ ] Working tree will be clean after commit

---

## Integration with Workflow

### Planning Stage
- All commits are docs-only
- Follow this policy for commit messages and boundaries
- No execution or automation

### Builder Stage (Future)
- Commits follow phase plans exactly
- Commit at defined commit points (CP1, CP2, ...)
- Include rollback and verification notes
- Reference phase ID in commit message

### Gatekeeper Review
- Verify commits follow this policy
- Check commit boundaries and messages
- Confirm no prohibited actions
- Validate scope matches phase plan (if execution stage)

---

## Related Documentation

**Core Requirements**:
- [planning.md](../../planning.md) - Planning stage requirements
- [builder.md](../../builder.md) - Builder stage requirements
- [gateway.md](../../gateway.md) - Gatekeeper review criteria

**System Documentation**:
- [docs/system/index.md](index.md) - System overview
- [CLAUDE.md](../../CLAUDE.md) - Project conventions

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-06 | Initial git and commit policy |
