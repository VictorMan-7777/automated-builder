# System Identity

**Version**: 1.0
**Last Updated**: 2026-02-06

---

## Repository Identity

**Name**: automated-builder
**Working Directory**: `~/dev/claude-projects/projects/automated-builder/`
**Purpose**: Plan-first, gated-phase framework for software project development

**Primary Function**: Enable comprehensive planning, structured execution, and quality gates for software projects through explicit documentation and human oversight.

---

## Authority Model

### Human in Control

**Principle**: All significant decisions and actions require human approval.

**When to Stop and Ask**:
- Ambiguous requirements or instructions
- Multiple valid approaches to a problem
- Decisions that affect scope, timeline, or architecture
- Actions that are hard to reverse (commits, deletions, deployments)
- Anything unexpected or unclear

**Human Approval Required**:
- Committing changes
- Transitioning between stages (planning → execution)
- Changing scope or approach
- Any action outside explicit instructions

---

## Default Posture

### Plan-First Approach

**Always**:
- Plan before implementing
- Document before executing
- Review before proceeding
- Verify after completing

**Never**:
- Rush to execution without planning
- Skip documentation
- Assume requirements
- Make irreversible changes without approval

---

### Reversible Steps

**Preference Order**:
1. Docs-only changes (fully reversible)
2. Staged changes (can be unstaged)
3. Committed changes (can be reverted)
4. Pushed changes (can be reverted with history)

**Irreversible Actions**:
- Require explicit approval
- Must have documented rollback plan
- Should be avoided when alternatives exist

---

### Minimal Side Effects

**Scope Control**:
- One logical change at a time
- No "cleanup while here" unless that's the task
- No feature creep
- No premature optimization

**MVP Focus**:
- Implement minimum viable solution first
- Add complexity only when requirements demand it
- Prefer simple over clever

---

## Explicit Prohibitions (By Default)

The following are **disabled by default** and require explicit human approval:

### ❌ No Automation
- No CI/CD pipelines
- No scheduled tasks
- No automated merges or deployments
- No self-modifying systems

### ❌ No Hooks
- No git hooks (pre-commit, post-commit, etc.)
- No event triggers
- No automated actions on file changes
- No background processes

### ❌ No Agents
- No autonomous agents running independently
- No multi-agent systems
- No unsupervised execution loops
- All agent invocations require human oversight

### ❌ No Workflows
- No automated workflow execution
- No pipeline orchestration
- No chained automation
- Each step requires human approval

**Exception Process**:
1. Identify specific need for automation/hooks/agents/workflows
2. Document purpose, scope, and safety measures
3. Get explicit human approval
4. Document how to disable it
5. Add to appropriate system documentation

---

## Canonical System Documentation

This repository's behavior is defined by these authoritative documents:

### Core Requirements
- **planning.md** - Planning stage requirements (docs-only)
- **builder.md** - Builder stage requirements (execution, future)
- **gateway.md** - Gatekeeper review criteria

### System Policies
- **docs/system/git.md** - Git and commit policy (single source of truth)
- **docs/system/index.md** - System overview and workflow

### Project Conventions
- **CLAUDE.md** - Repository conventions and naming rules

**Note**: Role-specific prompts define which documents are required reading for each role. This document provides the foundational context applicable to all roles.

---

## Workflow Stages

### Current Stage: Planning (Docs-Only)
- All work is documentation
- No code execution
- No automation enabled
- Reversible by default

### Future Stage: Builder (Execution)
- Requires approved phase plans
- Follows explicit commit points
- Maintains rollback capability
- Subject to Gatekeeper review

### All Stages: Gatekeeper Review
- Independent quality review
- Explicit APPROVE/REVISE/REJECT decisions
- Ensures compliance with requirements
- Provides actionable feedback

---

## Compliance

All work in this repository MUST:
- Follow this identity document's principles
- Adhere to canonical system documentation
- Maintain human oversight and approval gates
- Preserve reversibility and auditability
- Stay within explicit scope boundaries

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-06 | Initial system identity document |
