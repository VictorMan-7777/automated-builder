# Automated Builder

**Framework**: Planner-Builder-Gatekeeper Workflow
**Status**: Planning Scaffold Active
**Version**: 1.0
**Last Updated**: 2026-02-05

---

## Overview

This repository implements a **plan-first, gated-phase approach** to software project development using a three-role workflow:

1. **Planner** - Creates comprehensive, docs-only planning artifacts
2. **Builder** - Executes approved plans with strict commit cadence
3. **Gatekeeper** - Reviews and approves/rejects work at each gate

All work follows conventions defined in [CLAUDE.md](CLAUDE.md).

---

## Core Requirements

### Root Reference Documents

- **[planning.md](planning.md)** - Planning stage requirements (docs-only, commit points, project structure)
- **[builder.md](builder.md)** - Build stage requirements (approved phases, commit cadence, rollback, verification)
- **[gateway.md](gateway.md)** - Gatekeeper requirements (approval criteria, review process, decision documentation)

### System Prompts

Located in `prompts/`:
- **[prompts/planner/planner-base.md](prompts/planner/planner-base.md)** - Planner agent system prompt
- **[prompts/builder/builder-base.md](prompts/builder/builder-base.md)** - Builder agent system prompt
- **[prompts/gatekeeper/gatekeeper-checklist.md](prompts/gatekeeper/gatekeeper-checklist.md)** - Gatekeeper agent system prompt

---

## Directory Structure

```
automated-builder/
├── planning.md              # Planning stage requirements
├── builder.md               # Builder stage requirements
├── gateway.md               # Gatekeeper requirements
├── CLAUDE.md                # Project conventions
├── README.md                # This file
│
├── prompts/                 # System prompts for workflow roles
│   ├── planner/
│   │   └── planner-base.md
│   ├── builder/
│   │   └── builder-base.md
│   └── gatekeeper/
│       └── gatekeeper-checklist.md
│
├── docs/
│   ├── system/              # System documentation and outputs
│   │   ├── README.md        # System docs index
│   │   └── outputs/         # Long output captures (permanent records)
│   │       ├── README.md    # Output capture rules
│   │       └── YYYY-MM-DD-*.md  # Dated output files
│   └── projects/            # Project planning artifacts
│       └── <project-slug>/
│           ├── index.md
│           ├── prd.md
│           ├── roadmap.md
│           ├── iteration-log.md
│           └── phases/
│               ├── 001-phase-one.md
│               ├── 002-phase-two.md
│               └── ...
│
├── commands/                # Command definitions (future)
├── tasks/                   # Task tracking (future)
├── reports/                 # Output reports (future)
└── scripts/                 # Utility scripts (manual execution only)
```

---

## Current Projects

### Devotional Generator

**Status**: Planning Complete, Ready for Gatekeeper Review
**Project Slug**: `devotional-generator`
**Location**: [docs/projects/devotional-generator/](docs/projects/devotional-generator/)

A devotional content generation system with template-based workflow.

**Entry Point**: [docs/projects/devotional-generator/index.md](docs/projects/devotional-generator/index.md)

**Quick Links**:
- [PRD](docs/projects/devotional-generator/prd.md) - Product requirements
- [Roadmap](docs/projects/devotional-generator/roadmap.md) - 5 phases, 11 commit points
- [Phases](docs/projects/devotional-generator/phases/) - Detailed phase plans (001-005)
- [Iteration Log](docs/projects/devotional-generator/iteration-log.md) - Planning evolution

**Phase Structure**:
- Phase 001: Project Scaffold (CP1, CP2)
- Phase 002: Template System (CP3, CP4, CP5)
- Phase 003: Content Library (CP6, CP7)
- Phase 004: Validation & Preview (CP8, CP9)
- Phase 005: Export & Distribution (CP10, CP11)

---

## Workflow

### For Planners

1. Read [planning.md](planning.md) completely
2. Create project directory: `docs/projects/<project-slug>/`
3. Generate required documents (index, PRD, roadmap, iteration-log)
4. Write phase plans in `phases/` subdirectory (001, 002, etc.)
5. Ensure all commit points explicitly identified
6. Submit to Gatekeeper for review

### For Builders

1. Read [builder.md](builder.md) completely
2. Verify phase plan approval from Gatekeeper
3. Execute phase steps sequentially
4. Follow commit cadence exactly (CP1, CP2, etc.)
5. Verify after each step
6. Maintain rollback capability
7. Complete gatekeeper checklist
8. Submit to Gatekeeper for review

### For Gatekeepers

1. Read [gateway.md](gateway.md) completely
2. Review planning artifacts or implementation outputs
3. Use gatekeeper checklist template
4. Validate against requirements
5. Make explicit decision: APPROVE / REVISE / REJECT
6. Document rationale clearly
7. Provide actionable feedback

---

## Key Principles

### Plan-First Methodology

1. **Plan**: Define scope, steps, outcomes before implementation
2. **Review**: Validate plan before proceeding
3. **Implement**: Execute plan incrementally
4. **Verify**: Confirm results match plan

### Mandatory Constraints

**Planning Stage**:
- Docs-only (no execution)
- All projects under `docs/projects/<slug>/`
- Commit points explicitly identified
- Gatekeeper checks apply to plans

**Builder Stage**:
- Approved phase ID required
- Mandatory commit cadence (Policy B)
- Rollback + verification required
- No scope creep

**Gatekeeper Stage**:
- Explicit APPROVE/REVISE/REJECT decision
- Documented rationale
- Actionable feedback
- Independence maintained

### Quality Gates

Every phase requires:
1. Explicit commit points (CP1, CP2, ...)
2. Acceptance criteria (measurable)
3. Rollback procedures (per-step, per-commit)
4. Verification steps (commands + expected output)
5. Gatekeeper checklist (approval criteria)

---

## Naming Conventions

From [CLAUDE.md](CLAUDE.md):

- **All lowercase**: File and directory names
- **Hyphen-separated**: Use hyphens between words (e.g., `my-project-file.md`)
- **No underscores or spaces**: Avoid `_` and spaces
- **Numbered prompts**: Three-digit format (001, 002, 003)

---

## Long Output Capture Rule

**CRITICAL**: When Claude generates lengthy outputs (> 500 lines, comprehensive summaries, detailed reports), those outputs MUST be saved to file for permanent record.

### Location

All long outputs saved to: **`docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md`**

**Format**: Date, sequence number, context (planner/builder/gatekeeper/system), description

### When to Save

- Planning phase completion summaries
- Build phase completion reports
- Gatekeeper review decisions
- File trees and structure diagrams
- User explicitly requests ("save output to file")

### Chat vs Repository

**Chat**: High-level summary + file path pointer
**Repository**: Complete detailed output (permanent record)

**Example**:
```
✅ Planning complete!

Summary: 9 files created, 5 phases defined, 11 commit points.
Full details: docs/system/outputs/2026-02-05__01__planner__planning-complete.md
```

**See**: [docs/system/outputs/README.md](docs/system/outputs/README.md) for complete rules

---

## Getting Started

### To Create a New Project Plan

1. Review [devotional-generator](docs/projects/devotional-generator/) as example
2. Create directory: `docs/projects/<your-project-slug>/`
3. Use [prompts/planner/planner-base.md](prompts/planner/planner-base.md) as guide
4. Generate: index.md, prd.md, roadmap.md, iteration-log.md
5. Write phase plans in `phases/` subdirectory
6. Submit for gatekeeper review

### To Implement an Existing Plan

1. Verify plan has gatekeeper approval
2. Use [prompts/builder/builder-base.md](prompts/builder/builder-base.md) as guide
3. Execute phases sequentially
4. Follow commit points exactly
5. Verify at each step
6. Submit for gatekeeper review

### To Review Plans or Implementations

1. Use [prompts/gatekeeper/gatekeeper-checklist.md](prompts/gatekeeper/gatekeeper-checklist.md)
2. Review against requirements docs
3. Complete checklist honestly
4. Make explicit decision
5. Provide clear, actionable feedback

---

## Status: Devotional Generator

- **Planning**: ✅ Iteration 0 Complete (awaiting Gatekeeper review)
- **Implementation**: ⏸️ Not Started
- **Phases Completed**: 0/5
- **Commit Points Completed**: 0/11

---

## Meta: This Repository as a Tool

This repository demonstrates using the Planner-Builder-Gatekeeper pattern for:

1. **Comprehensive planning** without execution pressure
2. **Iterative refinement** before committing to approach
3. **Documentation-first** ensures clarity
4. **Quality gates** prevent scope creep and errors
5. **Reusable patterns** across projects

---

## References

- [CLAUDE.md](CLAUDE.md) - Project conventions and guardrails
- [planning.md](planning.md) - Planning stage requirements
- [builder.md](builder.md) - Builder stage requirements
- [gateway.md](gateway.md) - Gatekeeper requirements

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Reorganized with Planner-Builder-Gatekeeper structure |
