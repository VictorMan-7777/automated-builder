# Automated Builder — System Overview

**Version**: 1.0
**Last Updated**: 2026-02-05

---

## Purpose

### What This System Is For

A **plan-first, gated-phase framework** for software project development using explicit planning, structured execution, and quality gates.

**Primary Goals**:
- Create comprehensive, reviewable plans before implementation
- Maintain strict separation between planning (docs-only) and execution
- Enforce quality gates at every phase transition
- Preserve complete audit trail via git and structured outputs
- Support iterative refinement of plans before committing to implementation

### What This System Is NOT For

**Not designed for**:
- Rapid prototyping or exploratory coding
- Time-critical emergency fixes
- Simple, well-understood one-off tasks
- Automated code generation without human oversight
- Projects where planning overhead exceeds implementation time

### System Identity

**See**: [docs/system/identity.md](identity.md) for repository identity, authority model, and default posture.

---

## Roles

### Planner (Docs-Only)

**Responsibility**: Create comprehensive planning artifacts

**Scope**:
- Design project structure and phases
- Define commit points and acceptance criteria
- Document rollback and verification procedures
- Prepare gatekeeper checklists
- Generate planning summaries

**Constraints**:
- ❌ No code execution
- ❌ No automation setup
- ✅ Markdown documentation only
- ✅ Outputs to `../<slug>/` (per P-083)

**System Prompt**: [prompts/planner/planner-base.md](prompts/planner/planner-base.md)

---

### Builder (Implementation, Later)

**Responsibility**: Execute approved phase plans

**Scope**:
- Follow phase plans step-by-step
- Execute exact commit points (CP1, CP2, etc.)
- Run verification checks
- Document issues and deviations
- Prepare handoff to Gatekeeper

**Constraints**:
- ❌ Cannot proceed without approved plan
- ❌ No scope creep (strict plan adherence)
- ✅ Must verify every step
- ✅ Must maintain rollback capability

**System Prompt**: [prompts/builder/builder-base.md](prompts/builder/builder-base.md)

**Status**: Framework defined, implementation stage not yet active

---

### Gatekeeper (Review + Approval)

**Responsibility**: Review and approve/reject planning or implementation outputs

**Scope**:
- Validate planning artifacts against requirements
- Review implementation for plan compliance
- Make explicit APPROVE/REVISE/REJECT decisions
- Document rationale for all decisions
- Provide actionable feedback

**Constraints**:
- ❌ Does not implement changes
- ❌ Does not rubber-stamp approvals
- ✅ Independent review based on criteria
- ✅ Explicit decision required

**System Prompt**: [prompts/gatekeeper/gatekeeper-checklist.md](prompts/gatekeeper/gatekeeper-checklist.md)

---

## Canonical Documents

### planning.md

**Purpose**: Planning stage invariants and requirements

**Key Rules**:
- Docs-only (no execution during planning)
- All projects under `../<slug>/` (per P-083)
- Commit points must be explicitly identified
- Long outputs saved to `docs/system/outputs/` (system) or `../<slug>/docs/system/outputs/` (project-specific)

**Read**: [planning.md](planning.md)

---

### builder.md

**Purpose**: Build stage invariants and requirements

**Key Rules**:
- Approved phase ID required before proceeding
- Mandatory commit cadence (follow plan exactly)
- Rollback + verification required for every step
- No scope creep (strict plan adherence)

**Read**: [builder.md](builder.md)

---

### gateway.md

**Purpose**: Review and approval criteria

**Key Rules**:
- Explicit APPROVE/REVISE/REJECT decision
- Documented rationale required
- Actionable feedback for revisions
- Independence from Planner/Builder

**Read**: [gateway.md](gateway.md)

---

## Artifact Approval Status

Artifacts in this system have one of two statuses:

**Draft** (default):
- No explicit status marker
- May be revised directly by the Planner

**Approved**:
- Explicitly marked with: `<!-- STATUS: APPROVED -->`
- Must not be modified directly
- Changes require a proposed revision and explicit human approval

This rule applies globally unless a more specific rule exists for a particular artifact type.

---

## Where Things Live

### Project Artifacts

**Location**: `../<project-slug>/` (parent directory, per P-083)

**Structure**:
```
<parent-projects-dir>/
├── automated-builder/   (this repo)
└── <project-slug>/
    ├── index.md           # Navigation and overview
    ├── prd.md             # Product requirements
    ├── roadmap.md         # Milestones and timeline
    ├── iteration-log.md   # Planning evolution
    ├── phases/            # Phase plans
    │   ├── 001-phase-one.md
    │   ├── 002-phase-two.md
    │   └── ...
    └── docs/
        └── system/
            └── outputs/   # Project workflow artifacts
```

_Note: Previously stored in `docs/projects/<slug>/` before P-083 relocation._

---

### System Prompts

**Location**: `prompts/<role>/`

**Structure**:
```
prompts/
├── planner/
│   └── planner-base.md       # Planner agent system prompt
├── builder/
│   └── builder-base.md       # Builder agent system prompt
└── gatekeeper/
    └── gatekeeper-checklist.md  # Gatekeeper agent system prompt
```

System prompts should follow the canonical prompt template: [docs/system/prompt-template.md](prompt-template.md)

---

### Bootstrap Templates

**Location**: `templates/project/`

**Purpose**: Canonical template source-of-truth for `run-create-project`. All project bootstrap
files are generated from these templates with placeholder substitution.

**Templates**:

| Template | Deploys to (project-relative) |
|---|---|
| `project.yaml.tmpl` | `project.yaml` |
| `index.md.tmpl` | `index.md` |
| `prd.md.tmpl` | `prd.md` |
| `roadmap.md.tmpl` | `roadmap.md` |
| `iteration-log.md.tmpl` | `iteration-log.md` |
| `builder-manifest.yaml.tmpl` | `builder-manifest.yaml` |
| `ai-process.md.tmpl` | `docs/system/ai-process.md` |
| `pending-items-rules.md.tmpl` | `docs/system/pending-items-rules.md` |

**Placeholder syntax**: `{Token}` — e.g. `{project-slug}`, `{Project Name}`, `{PREFIX}`, `{YYYY-MM-DD}`.
Substitution source is `project.yaml` (`identity.*` fields).

**Normative spec**: [docs/implementation/system/template-specification.md](../implementation/system/template-specification.md)

**Authority**: Template files are system-controlled. Changes require a proposal and approval.
`run-create-project` may read templates and write only to `../<project-slug>/`.

---

### Long Outputs / Summaries

**Location**: `docs/system/outputs/`

**Naming**: `YYYY-MM-DD__NN__<context>__<description>.md`

**Contexts**: planner | builder | gatekeeper | system

**When to Save**:
- Planning phase completion summaries
- Build phase completion reports
- Gatekeeper review decisions
- System reorganization summaries
- User explicitly requests ("save output to file")

**See**: [docs/system/outputs/README.md](docs/system/outputs/README.md) for complete rules

---

## Typical Workflow

### 1. Run Planner

**Input**: Project requirements, scope, constraints

**Process**:
- Create `../<slug>/` directory (parent directory, per P-083)
- Generate PRD, roadmap, iteration-log
- Write phase plans (001, 002, 003, ...)
- Identify commit points (CP1, CP2, ...)
- Document rollback and verification procedures
- Save planning summary to `../<slug>/docs/system/outputs/` (project-specific) or `docs/system/outputs/` (system-level)

**Output**: Complete planning artifacts ready for review

---

### 2. Gatekeeper Review (Planning)

**Input**: Planning artifacts from Planner

**Process**:
- Review structure and completeness
- Validate commit points identified
- Check acceptance criteria are measurable
- Verify rollback procedures documented
- Complete gatekeeper checklist

**Decisions**:
- **APPROVED** → Proceed to Builder stage (when active)
- **REVISE** → Return to Planner with feedback
- **REJECT** → Fundamental issues, restart planning

---

### 3. Iterate Planning OR Approve

**If REVISE**:
1. Planner reads feedback
2. Updates affected documents
3. Increments iteration in iteration-log.md
4. Resubmits for Gatekeeper review
5. Repeat until APPROVED

**If APPROVED**:
- Planning phase complete
- Ready for Builder stage (when implemented)
- Or: Ready for human implementation using phase plans

---

### 4. (Later) Builder Stage

**Status**: Not yet implemented

**When Active**:
- Builder reads approved phase plan
- Executes steps sequentially
- Follows commit points exactly (CP1 → CP2 → ...)
- Verifies after each step
- Completes phase, submits to Gatekeeper
- Gatekeeper reviews implementation

---

## Non-Goals

### No Automation By Default

**Rule**: No hooks, agents, workflows, or execution systems enabled by default

**Rationale**:
- Explicit human control required
- Prevents unintended side effects
- Maintains audit trail clarity
- Reduces complexity

**Exception**: Only when explicitly approved and documented

---

### No Hooks Unless Explicitly Approved

**Rule**: No git hooks, pre-commit scripts, or automated triggers

**Rationale**:
- Transparency (what you see is what runs)
- Predictability (no hidden automation)
- Safety (no accidental executions)

**Exception**: Human-approved hooks for specific, documented purposes

---

### No Execution During Planning

**Rule**: Planning stage is docs-only, zero execution

**Rationale**:
- Separation of concerns (plan vs execute)
- Reversibility (plans are just markdown)
- Safety (can't break anything while planning)
- Iteration-friendly (refine without risk)

**Enforcement**: Planner system prompt prohibits execution

---

## How to Start

### For New Projects

**1. Read Core Documents**:
- [planning.md](planning.md) - Understand planning requirements
- [CLAUDE.md](CLAUDE.md) - Learn project conventions
- [gateway.md](gateway.md) - Understand approval criteria

**2. Read Planning Guide**:
- [docs/system/run-planner.md](run-planner.md) - Detailed planning workflow

**3. Use Planner Prompt**:
- [prompts/planner/planner-base.md](prompts/planner/planner-base.md) - Planner system prompt

**4. Create Project Plan**:
```bash
# 1. Create project directory (parent directory)
mkdir -p ../<your-project-slug>

# 2. Generate planning artifacts
# (Use Planner with planner-base.md prompt)

# 3. Submit for Gatekeeper review
```

---

### For Reviewing Plans

**1. Read Gatekeeper Requirements**:
- [gateway.md](gateway.md) - Review criteria

**2. Use Gatekeeper Prompt**:
- [prompts/gatekeeper/gatekeeper-checklist.md](prompts/gatekeeper/gatekeeper-checklist.md) - Review template

**3. Review Project Artifacts**:
- Start with `../<slug>/index.md` (per P-083)
- Check PRD, roadmap, phases
- Validate commit points, acceptance criteria
- Complete gatekeeper checklist

**4. Make Decision**:
- APPROVE / REVISE / REJECT
- Document rationale
- Provide actionable feedback (if REVISE)

---

### For Implementing Approved Plans

**Option A: Human Implementation**
- Use phase plans as detailed instructions
- Follow commit points exactly
- Run verification steps
- Document any deviations

**Option B: Builder Stage (Future)**
- Wait for Builder stage implementation
- Builder will execute approved phase plans
- Gatekeeper will review implementation

---

## Quick Links

**Core Documentation**:
- [README.md](README.md) - Repository overview and detailed guide
- [planning.md](planning.md) - Planning requirements
- [builder.md](builder.md) - Builder requirements
- [gateway.md](gateway.md) - Gatekeeper requirements
- [CLAUDE.md](CLAUDE.md) - Project conventions

**System Documentation**:
- [docs/system/README.md](docs/system/README.md) - System docs index
- [docs/system/outputs/README.md](docs/system/outputs/README.md) - Long output rules
- [docs/system/changelog.md](docs/system/changelog.md) - System changes log

**System Prompts**:
- [prompts/planner/planner-base.md](prompts/planner/planner-base.md)
- [prompts/builder/builder-base.md](prompts/builder/builder-base.md)
- [prompts/gatekeeper/gatekeeper-checklist.md](prompts/gatekeeper/gatekeeper-checklist.md)

**Planning Guide**:
- [docs/system/run-planner.md](run-planner.md) - Complete planning workflow guide

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-18 | Add Bootstrap Templates subsection linking to stable normative spec (P-085) |
| 1.0 | 2026-02-05 | Initial system overview |
