# CLAUDE.md - Automated Builder Project Guidelines

## Overview

This document defines conventions, workflows, and standards for the automated-builder repository. All contributors—human and AI—must follow these guidelines.

---

## Naming Conventions

- **All lowercase**: File and directory names must be lowercase.
- **Hyphen-separated**: Use hyphens to separate words (e.g., `my-task-file.md`).
- **No underscores or spaces**: Avoid `_` and spaces in all names.
  - **Exception**: System outputs (`docs/system/outputs/`) use double underscores (`__`) as separators in the canonical format: `YYYY-MM-DD__NN__<context>__<description>.md`

---

## Standard Directory Structure

```
automated-builder/
├── commands/       # Command definitions and specifications
├── prompts/        # Numbered prompt templates (NNN format)
├── tasks/          # Task definitions and tracking
├── reports/        # Output reports and logs
├── docs/           # Documentation and guides
├── scripts/        # Utility scripts (manual execution only)
└── CLAUDE.md       # This file
```

---

## Prompt Numbering Convention

All prompts must use a three-digit numeric prefix (NNN format):

- `001-initial-setup.md`
- `002-define-requirements.md`
- `003-implement-feature.md`

This ensures proper ordering and traceability.

---

## Workflow: Plan-First Approach

All work must follow a plan-first methodology:

1. **Plan**: Define scope, steps, and expected outcomes before implementation.
2. **Review**: Validate the plan before proceeding.
3. **Implement**: Execute the plan incrementally.
4. **Verify**: Confirm results match the plan.

**Git Policy**: All commits follow [docs/system/git.md](docs/system/git.md).

---

## Role Definitions

### Claude Code

- **Responsibilities**: Planning, implementation, code generation, documentation.
- **Scope**: Creates plans, writes code, proposes changes, drafts content.

### Clawdbot

- **Responsibilities**: Validation only.
- **Scope**: Reviews outputs, confirms compliance, flags issues.
- **Constraint**: Does not implement or modify; only validates.

---

## Human Involvement Requirements

### Human-Required Steps

The following require direct human action:

- Repository creation and deletion
- Access control and permissions changes
- External service configuration (API keys, secrets)
- Deployment to production environments
- Financial or billing decisions
- Legal or compliance approvals

### Human Review Checkpoints

Human review is required at these stages:

- Before merging any changes to main branch
- After completion of each major milestone
- When scope changes from the original plan
- Before any irreversible action
- When security-sensitive changes are proposed

### Second-AI Review Recommendations

A second AI review (via Clawdbot or equivalent) is recommended when:

- Changes affect multiple systems or components
- Logic complexity exceeds simple CRUD operations
- Security or data integrity is involved
- The implementation deviates from the original plan
- Automated tests are insufficient for validation

---

## Scope Principles

### MVP Focus

- Implement the minimum viable solution first.
- Avoid over-engineering or premature optimization.
- Add complexity only when requirements demand it.

### Reversible Changes

- Prefer reversible over irreversible actions.
- Document rollback procedures for significant changes.
- Test in isolation before applying broadly.

---

## General Guidelines

- Keep changes focused and incremental.
- Document decisions and rationale.
- Maintain traceability between plans, tasks, and implementations.
- When uncertain, ask for clarification rather than assuming.

---

## File Creation Rules

- Create files only in the standard directories listed above.
- Follow the naming conventions strictly.
- Include appropriate headers and metadata in all documents.
