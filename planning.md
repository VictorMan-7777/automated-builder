# Planning Requirements

**Version**: 1.1
**Last Updated**: 2026-02-05

---

## Overview

This document defines requirements and constraints for the **Planning** stage of the Planner-Builder-Gatekeeper workflow.

---

## Planning-Only Rule

**CRITICAL**: Planning is a **docs-only** activity. No execution, automation, or implementation.

### Prohibited During Planning

- Running commands (bash, scripts, etc.)
- Modifying code or configuration files
- Enabling hooks, agents, workflows, or automation
- Creating executable scripts (planning may document their future design)
- Installing dependencies or tools
- Making irreversible system changes

### Allowed During Planning

- Creating markdown documentation
- Designing workflows and processes
- Specifying requirements and acceptance criteria
- Defining directory structures
- Documenting commit points and rollback procedures
- Writing phase plans and checklists

---

## Project Artifacts Location

**MANDATORY**: All project artifacts produced by the Planner MUST live under:

```
docs/projects/<project-slug>/
```

With phase prompts under:

```
docs/projects/<project-slug>/phases/
```

### Example Structure

```
docs/
└── projects/
    └── my-project/
        ├── index.md
        ├── prd.md
        ├── roadmap.md
        ├── iteration-log.md
        └── phases/
            ├── 001-phase-one.md
            ├── 002-phase-two.md
            └── 003-phase-three.md
```

### Naming Conventions

- **Project slug**: lowercase, hyphen-separated (e.g., `devotional-generator`)
- **Phase files**: NNN format (001, 002, 003, etc.)
- **All files**: lowercase, hyphen-separated, `.md` extension

---

## Commit Points Requirement

**MANDATORY**: Plans MUST identify explicit commit points.

### Commit Point Definition

A **commit point** (CP) is a milestone where:
- A logical unit of work is complete
- Files are staged and committed to git
- The working tree is clean
- Progress can be verified
- Rollback is possible

### Commit Point Specification

Each phase plan MUST include:

1. **Commit point identifier**: CP1, CP2, CP3, etc.
2. **Files to stage**: Explicit list of files for this commit
3. **Commit command**: Exact command to run (with message)
4. **Verification steps**: How to confirm commit succeeded
5. **Rollback instructions**: How to undo if needed

### Example Commit Point

```markdown
### CP1: Initial Scaffold

**Files to Stage**:
- `CLAUDE.md`
- `README.md`

**Commit Command**:
```bash
git add CLAUDE.md README.md
git commit -m "chore: initial project scaffold"
```

**Verification**:
- `git status` shows clean working tree
- `git log -n 1` shows commit

**Rollback**:
- `git reset --soft HEAD~1` (before push)
```

---

## Gatekeeper Checks Apply to Plans

**IMPORTANT**: Gatekeeper review applies to planning outputs, not just implementation.

### Planning Review Checkpoints

Before a plan is approved for implementation, verify:

- [ ] All required sections present (PRD, roadmap, phases)
- [ ] Commit points explicitly identified
- [ ] Acceptance criteria are measurable
- [ ] Rollback procedures documented
- [ ] Verification steps are concrete
- [ ] No ambiguous or vague language
- [ ] Naming conventions followed
- [ ] File structure matches requirements

### Planning Approval Gate

Plans require explicit approval:
- **APPROVED**: Ready for Builder stage
- **REVISE**: Changes needed, re-submit
- **REJECT**: Fundamental issues, start over

---

## Plan Structure Requirements

### Required Documents

Every project plan MUST include:

1. **index.md** - Navigation and overview
2. **prd.md** - Product requirements document
3. **roadmap.md** - Milestones and timeline
4. **iteration-log.md** - Planning evolution tracking
5. **phases/*.md** - Detailed phase plans (numbered)

### Phase Plan Requirements

Each phase plan MUST include:

- **Objective**: What this phase accomplishes
- **Prerequisites**: What must be complete first
- **Inputs**: What information/artifacts are needed
- **Outputs**: What will be produced
- **Steps**: Detailed instructions
- **Commit Points**: Explicit CP identifiers
- **Acceptance Criteria**: How to know phase is complete
- **Rollback Notes**: How to undo changes
- **Verification Steps**: Concrete checks with expected output
- **Gatekeeper Checklist**: Approval criteria

---

## Reversibility Principle

All planned changes MUST be reversible.

### Reversibility Requirements

- Git-based version control (can revert commits)
- Documented rollback procedures (per-step and per-commit)
- No destructive operations without backup plan
- "Nuclear option" full reset documented

---

## Traceability

Every output must be traceable to inputs.

### Traceability Requirements

- Link requirements to deliverables
- Link phases to milestones
- Link commit points to acceptance criteria
- Document decision rationale

---

## Iteration Support

Plans are living documents that evolve.

### Iteration Requirements

- Version tracking in iteration-log.md
- Document changes made each iteration
- Explain rationale for changes
- Preserve history (don't delete old iterations)

---

## Human Review Checkpoints

Plans MUST specify where human review is required:

- Before proceeding to next phase
- After major milestones
- When scope changes
- Before irreversible actions
- For security-sensitive changes

---

## Constraints

### Scope Control

- MVP focus (minimum viable product)
- No premature optimization
- No feature creep
- Clear in-scope vs out-of-scope

### Documentation Standards

- Clear, concise language
- Actionable instructions
- No ambiguity
- Examples provided where helpful

---

## Long Output Capture

**MANDATORY**: When Planner generates lengthy outputs, those outputs MUST be saved to file for permanent record.

### Output File Requirements

When planning phase completes or generates comprehensive output:

1. **Save to**: `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md`
2. **Naming**: Follow canonical format with daily sequence and context
3. **Content**: Comprehensive details (file trees, checklists, summaries)
4. **Chat**: Provide summary + file path pointer

### When to Save Output

Save to file when output is:
- > 500 lines or multiple detailed sections
- Permanent record of planning completion
- Reference material (file trees, status reports)
- User explicitly requests ("save output to file")

### What to Include

Planning outputs should contain:
- All files created/modified/deleted
- Complete structure diagrams
- Verification checklists
- Detailed next steps
- Compliance confirmation

### Chat vs Repository

**Chat**: High-level summary + file path
**Repository**: Complete detailed output

**See**: [docs/system/outputs/README.md](docs/system/outputs/README.md) for complete rules

---

## Compliance

All planning outputs MUST comply with:

1. This document (planning.md)
2. Project conventions (CLAUDE.md)
3. Builder requirements (builder.md) - forward compatibility
4. Gatekeeper criteria (gateway.md) - approval readiness

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-05 | Added Long Output Capture requirement |
| 1.0 | 2026-02-05 | Initial planning requirements |
