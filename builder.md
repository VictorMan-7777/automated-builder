# Builder Requirements

**Version**: 1.1
**Last Updated**: 2026-02-05

---

## Overview

This document defines requirements and constraints for the **Builder** stage of the Planner-Builder-Gatekeeper workflow.

**Builder Role**: Execute approved plans by creating artifacts, committing changes, and maintaining quality.

---

## Prerequisites

### Before Building

Builder MUST verify:

1. **Approved Phase ID**: Phase plan has been reviewed and approved
2. **Planning Complete**: All planning documents exist and are current
3. **Prerequisites Met**: Previous phases complete (if sequential)
4. **Tools Available**: Required dependencies installed
5. **Clean State**: Working directory clean, no conflicts

### Approval Requirement

Builder MUST NOT proceed without:
- Explicit approval of the phase plan
- Gatekeeper sign-off (or human approval)
- Clear understanding of objectives

---

## Mandatory Commit Cadence (Policy B)

**CRITICAL**: Builder MUST follow the commit cadence defined in the approved plan.

### Commit Policy

1. **Follow Plan**: Use exact commit points specified (CP1, CP2, etc.)
2. **No Skipping**: All commit points must be executed in order
3. **No Combining**: Don't combine multiple CPs into one commit
4. **No Extras**: Don't add commits not specified in plan
5. **Clean Commits**: Each commit must represent a logical unit

### Commit Execution

For each commit point:

```bash
# 1. Verify files exist
ls <files-to-commit>

# 2. Stage files (exact list from plan)
git add <file1> <file2> ...

# 3. Commit with specified message
git commit -m "<exact-message-from-plan>"

# 4. Verify commit succeeded
git log -n 1
git status  # Should be clean
```

### Commit Message Format

Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `chore:` - Maintenance tasks
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `build:` - Build system changes

---

## Rollback Requirement

**MANDATORY**: Builder MUST maintain ability to rollback at every step.

### Rollback Procedures

Before each action, Builder must:
1. Understand rollback procedure (from plan)
2. Test rollback if uncertain
3. Document any deviations

### Rollback Types

1. **Per-Step Rollback**: Undo individual actions (file deletion, etc.)
2. **Per-Commit Rollback**: `git revert <hash>` or `git reset --soft HEAD~1`
3. **Phase Rollback**: Reset to state before phase started
4. **Nuclear Option**: Full repository reset (documented in plan)

### When to Rollback

Rollback if:
- Error occurs during execution
- Acceptance criteria not met
- Plan instructions unclear/incorrect
- Human intervention required

---

## Verification Requirement

**MANDATORY**: Builder MUST verify each step before proceeding.

### Verification Process

After each action:
1. Run verification commands (from plan)
2. Compare actual output to expected output
3. Confirm acceptance criteria met
4. Document any discrepancies

### Verification Failure

If verification fails:
1. **STOP**: Do not proceed to next step
2. **Rollback**: Undo failed action
3. **Document**: Record failure and context
4. **Escalate**: Request human review or plan revision

---

## No Scope Creep

**CRITICAL**: Builder MUST NOT deviate from approved plan.

### Prohibited Actions

- Adding features not in plan
- "Improving" code beyond plan scope
- Reorganizing files not specified
- Adding documentation not required
- Installing tools not approved
- Changing naming conventions

### When Changes Are Needed

If plan is insufficient or incorrect:
1. **STOP**: Halt execution
2. **Document**: Explain issue clearly
3. **Propose**: Suggest plan revision
4. **Wait**: Get approval before proceeding

---

## Quality Standards

Builder MUST maintain quality at every step.

### Code Quality (If Applicable)

- Follow existing conventions
- No security vulnerabilities
- No breaking changes (unless planned)
- Tests pass (if applicable)

### Documentation Quality

- Clear and accurate
- Matches actual implementation
- No placeholder text
- Examples are correct

### Commit Quality

- Atomic commits (one logical change)
- Descriptive messages
- Clean history (no "oops" commits)
- Working tree clean after each commit

---

## Error Handling

Builder MUST handle errors gracefully.

### Error Response

When errors occur:
1. **Capture**: Record full error message
2. **Rollback**: Undo partial changes
3. **Document**: Log error and context
4. **Report**: Notify human/Gatekeeper
5. **Halt**: Do not proceed until resolved

### Common Errors

- File not found → Check prerequisites
- Permission denied → Verify access
- Merge conflict → Resolve before continuing
- Test failure → Fix before committing
- Validation error → Correct and re-verify

---

## Phase Completion

Builder MUST complete all phase requirements.

### Completion Checklist

Before marking phase complete:
- [ ] All steps executed
- [ ] All commit points completed
- [ ] All verification steps passed
- [ ] Acceptance criteria met
- [ ] Documentation updated
- [ ] Working tree clean
- [ ] No known issues

### Completion Output

Builder must provide:
- Summary of work completed
- List of commits made (with hashes)
- Verification results
- Any deviations from plan (with justification)
- Gatekeeper checklist filled out

---

## Communication

Builder MUST communicate status clearly.

### Status Updates

Provide updates:
- Before starting phase
- After each major step
- After each commit point
- Upon completion
- When blocked/errors occur

### Status Format

```markdown
**Phase**: 001-project-scaffold
**Step**: 3/5 (Creating directory structure)
**Status**: In Progress
**Last Commit**: CP1 (abc123f)
**Next**: Create CLAUDE.md
```

---

## Long Output Capture

**MANDATORY**: When Builder generates lengthy outputs, those outputs MUST be saved to file for permanent record.

### Output File Requirements

When phase completes or generates comprehensive output:

1. **Save to**: `docs/system/outputs/YYYY-MM-DD-descriptive-name.md`
2. **Naming**: Follow date-prefixed naming convention
3. **Content**: Comprehensive details (commits, verification results, issues)
4. **Chat**: Provide summary + file path pointer

### When to Save Output

Save to file when output is:
- Phase completion report (> 500 lines)
- Comprehensive verification results
- Detailed issue documentation
- User explicitly requests ("save output to file")

### What to Include

Build phase outputs should contain:
- All commits made (with hashes and messages)
- Complete verification results (all steps, pass/fail)
- Issues encountered and resolutions
- Gatekeeper checklist (completed)
- Recommendation for approval

### Chat vs Repository

**Chat**: High-level summary + file path
**Repository**: Complete detailed output

**Example Chat Response**:
```
✅ Phase 001 Complete

Commits: CP1 (abc123f), CP2 (def456g)
Verification: All passed
Issues: None

Full report: docs/system/outputs/2026-02-10-phase-001-completion.md
```

**See**: [docs/system/outputs/README.md](docs/system/outputs/README.md) for complete rules

---

## Gatekeeper Coordination

Builder prepares work for Gatekeeper review.

### Handoff to Gatekeeper

When phase complete, Builder provides:
1. Completed gatekeeper checklist
2. Verification results
3. Commit history
4. Any issues encountered
5. Recommendation (APPROVE/REVISE)

---

## Tool Usage

Builder follows tool constraints.

### Git Usage

- Always use `-b main` when initializing
- Never force push to main
- Never skip hooks (unless approved)
- Always verify branch before committing

### File Operations

- Use Read/Edit/Write tools (not bash cat/sed)
- Verify paths before operations
- Maintain backups for destructive changes

---

## Safety

Builder prioritizes safety.

### Safety Checklist

- [ ] Understand rollback before action
- [ ] Verify commands before execution
- [ ] Test on samples before batch operations
- [ ] Maintain clean git history
- [ ] Never delete without backup

---

## Constraints Summary

Builder MUST:
1. ✅ Have approved phase ID
2. ✅ Follow mandatory commit cadence (Policy B)
3. ✅ Maintain rollback capability
4. ✅ Verify every step
5. ✅ Avoid scope creep
6. ✅ Handle errors gracefully
7. ✅ Meet quality standards
8. ✅ Communicate status
9. ✅ Coordinate with Gatekeeper

Builder MUST NOT:
1. ❌ Proceed without approval
2. ❌ Skip or combine commit points
3. ❌ Deviate from plan
4. ❌ Continue after verification failure
5. ❌ Add unapproved features

---

## Compliance

All Builder actions MUST comply with:

1. This document (builder.md)
2. Approved phase plan
3. Project conventions (CLAUDE.md)
4. Planning requirements (planning.md)
5. Gatekeeper criteria (gateway.md)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-05 | Added Long Output Capture requirement |
| 1.0 | 2026-02-05 | Initial builder requirements |
