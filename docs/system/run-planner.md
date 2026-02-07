# Running the Planner

**Version**: 1.0
**Last Updated**: 2026-02-06

---

## Purpose

This document describes how to **run the Planner** to create comprehensive planning documentation for a project. Running the Planner is a **docs-only activity** that produces structured planning artifacts without any code execution or implementation.

**What "Running the Planner" Means:**
- Start with project requirements and constraints
- Generate complete planning documentation
- Define phases with explicit commit points
- Create actionable implementation guides
- Prepare artifacts for Gatekeeper review
- Support iterative refinement based on feedback

**Key Principle**: The Planner produces markdown documentation only. No code, scripts, or automation are created or executed during planning.

---

## Required Inputs

Before running the Planner, gather these inputs:

### 1. Project Slug
- **Format**: lowercase, hyphen-separated
- **Example**: `devotional-generator`, `api-gateway`, `user-dashboard`
- **Purpose**: Determines output directory (`docs/projects/<slug>/`)

### 2. Project Goal
- **What**: Brief description of what the project does or achieves
- **Why**: Core problem being solved or need being met
- **Example**: "Generate daily devotional content with scripture references"

### 3. Requirements
- **Functional**: What the system must do
- **Non-functional**: Performance, security, usability constraints
- **Scope boundaries**: What's in-scope vs out-of-scope
- **Example**: "Must support multiple Bible translations, generate 300-500 word devotionals, include 2-3 reflection questions"

### 4. Constraints
- **Technical**: Technology stack, platform limitations
- **Timeline**: Deadlines or milestones
- **Resources**: Available tools, APIs, libraries
- **Example**: "Use OpenAI API, must complete in 2 weeks, no custom database"

### 5. Sources (Optional)
- **Existing docs**: PRDs, specs, design documents
- **Reference projects**: Similar implementations
- **Templates**: GSD templates or other planning frameworks
- **Example**: "Use GSD template for phase structure, reference existing blog-generator project"

---

## Output Locations

All Planner outputs are written to:

```
docs/projects/<project-slug>/
├── index.md           # Navigation and overview
├── prd.md             # Product requirements document
├── roadmap.md         # Milestones and timeline
├── iteration-log.md   # Planning evolution tracking
└── phases/            # Detailed phase plans (numbered)
    ├── 001-phase-name.md
    ├── 002-phase-name.md
    └── ...
```

### Allowed Write Paths

**ONLY these paths are allowed during planning:**
- `docs/projects/<slug>/*.md` (project root files)
- `docs/projects/<slug>/phases/*.md` (phase plans)
- `docs/system/outputs/*.md` (planning summaries, when output is lengthy)

### Stop Conditions

**Planner MUST STOP if:**
- Attempting to write outside `docs/projects/<slug>/` (except outputs)
- Attempting to create or modify code files
- Attempting to run commands or scripts
- Attempting to enable automation, hooks, or workflows
- Any action violates the docs-only rule

**If stopped, state clearly:**
- What action was attempted
- Why it violates planning constraints
- What the user should do instead

---

## Required Outputs

Every Planner run MUST produce these files:

### 1. index.md
- **Purpose**: Navigation hub for all planning documents
- **Contents**: Links to PRD, roadmap, phases; project overview; status
- **Example**: [docs/projects/devotional-generator/index.md](../projects/devotional-generator/index.md)

### 2. prd.md
- **Purpose**: Detailed product requirements document
- **Contents**: Goals, functional requirements, non-functional requirements, scope, constraints, acceptance criteria
- **Must include**: Measurable acceptance criteria for project completion

### 3. roadmap.md
- **Purpose**: Timeline and milestone planning
- **Contents**: Phases overview, milestones, dependencies, timeline estimates (optional)
- **Must include**: Clear phase sequence and milestone definitions

### 4. iteration-log.md
- **Purpose**: Track planning evolution across iterations
- **Contents**: Version history, changes made, rationale, feedback addressed
- **Must include**: Initial entry (Iteration 1) even if no revisions yet

### 5. phases/NNN-phase-name.md
- **Purpose**: Detailed, executable instructions for each phase
- **Contents**: See Phase Plan Requirements below
- **Naming**: `001-phase-one.md`, `002-phase-two.md`, etc.

---

## Phase Plan Requirements

Each phase plan MUST include all of these sections:

### Objective
- What this phase accomplishes
- Why this phase is necessary
- Success definition for this phase

### Prerequisites
- What must be complete before starting
- Dependencies on other phases
- Required tools, access, or setup

### Inputs
- Information needed to execute this phase
- Artifacts from previous phases
- External resources or references

### Outputs
- What will be produced in this phase
- Files created or modified
- Artifacts passed to next phase

### Steps
- Detailed, sequential instructions
- Concrete actions (not vague descriptions)
- Numbered for clarity

### Commit Points
- **MANDATORY**: Explicit CP identifiers (CP1, CP2, CP3, ...)
- For each CP:
  - Files to stage (explicit list)
  - Commit command (exact `git add` and `git commit` commands)
  - Verification steps (how to confirm commit succeeded)
  - Rollback instructions (how to undo if needed)

**Example Commit Point:**
```markdown
### CP1: Initial Scaffold

**Files to Stage**:
- `src/index.ts`
- `README.md`

**Commit Command**:
```bash
git add src/index.ts README.md
git commit -m "feat: initial project scaffold"
```

**Verification**:
- `git status` shows clean working tree
- `git log -n 1` shows commit with correct message

**Rollback**:
- `git reset --soft HEAD~1` (before push)
- `git reset --hard HEAD~1` (if changes should be discarded)
```

### Acceptance Criteria
- How to know phase is complete
- Measurable, testable conditions
- Pass/fail criteria

### Rollback Notes
- How to undo this phase if needed
- Emergency rollback procedure ("nuclear option")
- What state system returns to

### Verification Steps
- Concrete checks to run
- Expected output for each check
- How to interpret results

### Gatekeeper Checklist
- Approval criteria for this phase
- What Gatekeeper should verify
- Criteria for APPROVE/REVISE/REJECT

---

## Using GSD Templates

**Status**: GSD is used as a **TEMPLATE LIBRARY ONLY** for planning structure and organization.

### What GSD Templates Provide
- Standardized phase plan structure
- Commit point documentation patterns
- Acceptance criteria examples
- Verification step templates

### Where GSD Templates Live
- **External reference**: GSD templates are referenced but not stored in this repository
- **Example projects**: See [docs/projects/devotional-generator/](../projects/devotional-generator/) for structure examples
- **System docs**: [planning.md](../../planning.md) defines required structure

### Which Templates to Reference
When planning, use these GSD patterns:
- **Phase structure**: Objective → Prerequisites → Steps → Commit Points → Acceptance Criteria
- **Commit points**: CP identifier, files, command, verification, rollback
- **Acceptance criteria**: Measurable, testable, pass/fail

### What GSD Templates Do NOT Provide
- ❌ Commands or workflows
- ❌ Automation hooks
- ❌ Executable scripts
- ❌ CI/CD integration

**Rule**: Use GSD as inspiration for structure, not for automation.

---

## Iteration Procedure

Planning is iterative. Here's how to run subsequent iterations:

### Initial Run (Iteration 1)

1. **Gather inputs** (slug, goal, requirements, constraints, sources)
2. **Read authoritative docs** ([planning.md](../../planning.md), [docs/system/index.md](index.md))
3. **Create project directory** (`docs/projects/<slug>/`)
4. **Generate all required outputs** (index, prd, roadmap, iteration-log, phases)
5. **Save planning summary** (if output is lengthy, see Long Output Rule below)
6. **Submit for Gatekeeper review**

### Subsequent Runs (Iteration N)

1. **Read Gatekeeper feedback** (from previous review)
2. **Update iteration-log.md** (document what's changing and why)
3. **Modify affected documents** (prd, roadmap, phases as needed)
4. **Increment iteration number** (in iteration-log.md)
5. **Save iteration summary** (if output is lengthy)
6. **Resubmit for Gatekeeper review**

### Iteration Log Format

```markdown
## Iteration 1 (2026-02-06)

**Status**: Initial planning
**Changes**: Created all planning documents
**Rationale**: First iteration, establishing project structure
**Submitted for review**: 2026-02-06

---

## Iteration 2 (2026-02-07)

**Status**: Revisions based on Gatekeeper feedback
**Changes**:
- Updated CP2 in phase 001 to include missing verification steps
- Refined acceptance criteria in prd.md to be more measurable
- Added rollback notes to phase 002

**Rationale**: Gatekeeper feedback identified missing verification and ambiguous criteria
**Submitted for review**: 2026-02-07
```

---

## Long Output Rule

**MANDATORY**: When Planner generates lengthy outputs, save to file instead of displaying in chat.

### When to Save Output

Save to `docs/system/outputs/` when:
- Planning phase completes (comprehensive summary)
- Output exceeds ~500 lines or has multiple detailed sections
- Output includes complete file trees, checklists, or status reports
- User explicitly requests ("save output to file")

### Output File Format

```
docs/system/outputs/YYYY-MM-DD__NN__planner__<description>.md
```

**Components:**
- `YYYY-MM-DD`: ISO 8601 date (e.g., 2026-02-06)
- `NN`: Daily sequence number (01, 02, 03, ...)
- `planner`: Context identifier (always "planner" for planning outputs)
- `<description>`: Brief description (lowercase, hyphen-separated)

**Examples:**
- `2026-02-06__01__planner__initial-planning-complete.md`
- `2026-02-06__02__planner__iteration-2-updates.md`
- `2026-02-10__01__planner__devotional-generator-approved.md`

### What to Include in Output File

Planning outputs should contain:
- **Summary**: High-level overview of planning phase
- **Files Created**: Complete list of all files generated
- **Structure**: Directory tree showing project layout
- **Commit Points**: Summary of all CPs identified across phases
- **Next Steps**: What happens next (Gatekeeper review, iteration, approval)
- **Compliance**: Confirmation of requirements met

### Chat vs File

**In Chat** (brief summary):
```
✅ Planning complete for devotional-generator!

Created:
- 5 planning documents (index, prd, roadmap, iteration-log)
- 4 phase plans (001-004)
- 11 commit points identified

Full details: docs/system/outputs/2026-02-06__01__planner__initial-planning-complete.md
```

**In File** (comprehensive details):
- Complete file tree
- All files with descriptions
- Full commit point list
- Detailed next steps
- Compliance checklist confirmation

**See**: [docs/system/outputs/README.md](outputs/README.md) for complete output rules

---

## Output Immutability

Planner outputs are **append-only artifacts**.

### Rules

- A planner iteration MUST NOT overwrite an existing output file.
- If the specified output filename already exists, the planner MUST increment the sequence number (`__NN__`) and write a new file.
- The sequence number (`NN`) is **monotonic across the repository**, not scoped to a single date.

### When This Applies

- Re-running the same iteration
- Correcting a flawed prompt
- Repeating an iteration on the same day

### Determining the Next Sequence Number

Scan all existing files in `docs/system/outputs/` and use the next available number, regardless of date.

**Example**: If the highest existing sequence number is `03` (from any date), the next output MUST use `04`.

---

## Planner Run Checklist

Use this checklist to confirm a Planner run is complete:

### Required Files
- [ ] `docs/projects/<slug>/index.md` exists
- [ ] `docs/projects/<slug>/prd.md` exists
- [ ] `docs/projects/<slug>/roadmap.md` exists
- [ ] `docs/projects/<slug>/iteration-log.md` exists
- [ ] `docs/projects/<slug>/phases/` directory exists
- [ ] At least one phase plan (`001-*.md`) exists

### Content Requirements
- [ ] PRD includes measurable acceptance criteria
- [ ] Roadmap defines clear milestones
- [ ] Each phase plan includes all required sections
- [ ] Every phase has explicit commit points (CP1, CP2, ...)
- [ ] All commit points include: files, command, verification, rollback
- [ ] Acceptance criteria are measurable and testable
- [ ] Rollback procedures are documented
- [ ] Verification steps are concrete with expected outputs

### Naming Conventions
- [ ] Project slug is lowercase, hyphen-separated
- [ ] Phase files use NNN format (001, 002, 003, ...)
- [ ] Project artifact filenames are lowercase, hyphen-separated (no underscores)
- [ ] System output filenames use double underscores (`__`) per canonical format

### Docs-Only Compliance
- [ ] No code files created
- [ ] No scripts created
- [ ] No commands executed
- [ ] No automation enabled
- [ ] All outputs are markdown documentation

### Output Capture
- [ ] If output is lengthy, saved to `docs/system/outputs/`
- [ ] Output file follows naming convention (YYYY-MM-DD__NN__planner__desc.md)
- [ ] Chat includes summary + file path pointer

### Next Steps
- [ ] Planning artifacts ready for Gatekeeper review
- [ ] Iteration log initialized
- [ ] Path to iteration (if REVISE) is clear

**When all boxes checked**: ✅ Planner run complete, ready for Gatekeeper review

---

## Common Issues and Solutions

### Issue: Unclear Requirements
**Solution**: Use iteration-log.md to document assumptions and flag questions for user clarification

### Issue: Too Many Phases
**Solution**: Consolidate related work; aim for 3-7 phases for most projects

### Issue: Vague Acceptance Criteria
**Solution**: Make criteria measurable (e.g., "Test coverage > 80%" not "Good test coverage")

### Issue: Missing Commit Points
**Solution**: Every significant change should be a commit point; err on side of more CPs

### Issue: Output Too Long for Chat
**Solution**: Save to `docs/system/outputs/` and provide summary + file path in chat

---

## Related Documentation

**Core Requirements**:
- [planning.md](../../planning.md) - Planning stage requirements
- [docs/system/index.md](index.md) - System overview
- [CLAUDE.md](../../CLAUDE.md) - Project conventions

**System Prompts**:
- [prompts/planner/planner-base.md](../../prompts/planner/planner-base.md) - Planner agent prompt
- [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md) - Runnable entry prompt

**Review Process**:
- [gateway.md](../../gateway.md) - Gatekeeper review criteria

**Output Rules**:
- [docs/system/outputs/README.md](outputs/README.md) - Long output capture rules

**Example Project**:
- [docs/projects/devotional-generator/](../projects/devotional-generator/) - Complete planning example

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-06 | Initial run-planner system documentation |
