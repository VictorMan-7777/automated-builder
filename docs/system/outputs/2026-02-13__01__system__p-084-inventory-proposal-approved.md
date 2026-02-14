# P-084 — Inventory-Proposal: run-create-project Bootstrap Specification

**Item**: P-084 — run-create-project — create project directory + bootstrap required system docs
**Artifact Type**: Inventory-Proposal
**Date**: 2026-02-13
**Status**: Definition Only
**Version**: 2.1
**Revision**: Lifecycle alignment - removed insertion behavior, added Inventory Lifecycle Contract per issue-resolution.md

---

## Executive Summary

This proposal defines the complete specification for `run-create-project`, the prerequisite step before running Builder on any new project. This capability creates the target project directory and bootstraps all required system documentation so planner/builder loops can run without manual setup.

**Scope**: Definition only (non-goal: implementation)
**Output**: Explicit list of files/directories with contract traceability

---

## Problem Statement

Current State:
- Projects like `devotional-generator` cannot run Builder without manual bootstrap
- Required directory structure and manifest files must be created by hand
- No canonical specification exists for what constitutes a "ready" project

Required State:
- Zero manual bootstrap steps before first planner run
- All planner/builder prerequisites satisfied automatically
- Clear contract mapping for every required file

---

## Input Normalization vs Artifact Enforcement

**Governing Principle**: Rule files enforce deterministic structure and invariants on **system artifacts**, not on **human input**.

### Human Input (Flexible)
- Human-provided parameters are **normalized**, not rejected
- Input parsing is **interpretive** - if intent is understood, proceed
- Format variations are accepted and normalized to canonical form
- Examples:
  - Project name: "My Project" → normalized to slug: "my-project"
  - Prefix input: "dg" → normalized to: "DG"
  - Slug input: "My_Cool-App" → normalized to: "my-cool-app"

### System Artifacts (Deterministic)
- Enforcement rules apply at **artifact-write time** (not input time)
- Files written to `project.yaml`, `pending-items.md`, `builder-manifest.yaml` MUST conform to strict formats
- Validation failures HALT execution only when writing to artifacts
- Rule files enforce:
  - Structure (directory layout, file naming)
  - Identifiers (canonical ID format, prefix format)
  - Ordering (creation order, dependency chains)
  - Invariants (sibling relationships, consistency checks)

### Ambiguity Handling
- If input is ambiguous or intent cannot be determined, ask clarifying questions
- Do NOT guess or auto-fix ambiguous input
- Do NOT reject input for minor format variations if intent is clear

**Application to P-084**:
- `run-create-project` accepts flexible human input
- Normalizes input to canonical forms
- Enforces strict validation only when writing artifacts (`project.yaml`, templates, etc.)
- HALT behavior (described throughout this spec) applies at artifact-write time

---

## Bootstrap Specification

### 1. Directory Structure

`run-create-project` MUST create the following directory tree at `../<project-slug>/`:

```
<parent-projects-dir>/
└── <project-slug>/
    ├── project.yaml
    ├── index.md
    ├── prd.md
    ├── roadmap.md
    ├── iteration-log.md
    ├── builder-manifest.yaml
    ├── phases/
    │   └── .gitkeep
    └── docs/
        └── system/
            ├── ai-process.md
            └── outputs/
                └── .gitkeep
```

**Rationale**: This structure satisfies all prerequisites for both run-planner and run-builder operations.

---

### 2. Canonical Template Source-of-Truth

**Template Location**: `automated-builder/templates/project/`

**Rule**: All project bootstrap files MUST be generated from canonical templates stored in the automated-builder repository.

#### 2.1 Template Storage Contract

Templates MUST reside in:
```
automated-builder/
└── templates/
    └── project/
        ├── project.yaml.tmpl
        ├── index.md.tmpl
        ├── prd.md.tmpl
        ├── roadmap.md.tmpl
        ├── iteration-log.md.tmpl
        ├── builder-manifest.yaml.tmpl
        └── ai-process.md.tmpl
```

**Immutability**: Templates are versioned with the automated-builder repository. Changes to templates require:
1. Commit to automated-builder repository
2. Version increment in template metadata (if applicable)
3. Documentation update in this specification

**Generation Method**: `run-create-project` MUST read from canonical template files and apply placeholder substitution. Inline generation (hardcoded strings in implementation) is prohibited.

#### 2.2 Template Validation

Before project creation, `run-create-project` MUST verify:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| Template directory exists | `templates/project/` is present | HALT: "Template directory not found at {path}" |
| All required templates exist | 7 template files present with `.tmpl` extension (project, index, prd, roadmap, iteration-log, manifest, ai-process) | HALT: "Missing template: {filename}" |
| Templates are readable | All template files have read permissions | HALT: "Cannot read template: {filename}" |
| Templates contain valid placeholders | All templates use only allowed token syntax (see Section 2.3) | HALT: "Invalid placeholder syntax in {filename}: {token}" |

#### 2.3 Placeholder Substitution Contract

**Token Syntax**: All placeholders MUST use the format `{Token Name}` (curly braces, Title Case or UPPERCASE).

**Allowed Tokens**:

| Token | Source | Type | Example Value |
|-------|--------|------|---------------|
| `{project-slug}` | Input parameter | string | `devotional-generator` |
| `{Project Slug}` | Derived from `{project-slug}` | string | `devotional-generator` |
| `{Project Name}` | Input parameter | string | `Devotional Generator` |
| `{YYYY-MM-DD}` | System date (execution time) | date | `2026-02-13` |
| `{PREFIX}` | Input parameter or derived | string | `DG` |

**Derivation Rules**:
- `{Project Slug}` = `{project-slug}` (identity transformation for consistency)
- `{YYYY-MM-DD}` = Current date in ISO 8601 format at time of execution
- `{PREFIX}` = See Section 5.1 (Namespace Conversion Contract)

**Substitution Source**: All token values MUST be read from `project.yaml` (see Section 2.4). The identity file is the single source-of-truth for all placeholder substitution operations.

**Replacement Requirements**:
1. All tokens MUST be replaced before file creation
2. Token replacement MUST be deterministic (same input → same output)
3. Token replacement MUST be complete (no partial replacements)
4. Unrecognized tokens MUST cause immediate failure

**Post-Substitution Validation**:

After substitution, `run-create-project` MUST scan all generated content for:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| No unreplaced tokens | No `{...}` patterns remain except in code blocks or examples | HALT: "Unresolved token in {filename}: {token}" |
| No empty values | No tokens replaced with empty strings | HALT: "Empty value for token: {token}" |
| Date format valid | `{YYYY-MM-DD}` produces valid ISO 8601 date | HALT: "Invalid date format: {value}" |

---

#### 2.4 Project Identity (Slug + Prefix Registry)

**Purpose**: Establish a single source-of-truth for project identity metadata.

**Identity File**: `project.yaml`
**Location**: Project root directory
**Creation Order**: FIRST file created during bootstrap (before all other files)

#### Identity File Format

**Required Structure**:

```yaml
# Project Identity
# Single source-of-truth for project metadata
# Generated by run-create-project

identity:
  slug: {project-slug}
  name: {Project Name}
  prefix: {PREFIX}
  created: {YYYY-MM-DD}

schema_version: 1
```

**Field Specifications**:

| Field | Type | Format | Example | Source |
|-------|------|--------|---------|--------|
| `identity.slug` | string | lowercase, hyphen-separated | `devotional-generator` | Input parameter |
| `identity.name` | string | Human-readable title | `Devotional Generator` | Input parameter |
| `identity.prefix` | string | 1-4 uppercase letters | `DG` | Input parameter or derived per Section 5.1 |
| `identity.created` | date | ISO 8601 (YYYY-MM-DD) | `2026-02-13` | System date at creation time |
| `schema_version` | integer | Positive integer | `1` | Fixed value for MVP |

#### Source-of-Truth Rules

**Creation Order Contract**:
1. `run-create-project` MUST create `project.yaml` FIRST
2. After `project.yaml` exists, all other files are generated from it
3. No other file creation may proceed until `project.yaml` is validated

**Reference Hierarchy**:

```
project.yaml (source-of-truth)
    ↓
All other bootstrap files (generated/derived)
    ├── index.md
    ├── prd.md
    ├── roadmap.md
    ├── iteration-log.md
    └── builder-manifest.yaml
```

**Prohibition**: No other file is allowed to be the authoritative source for:
- Project slug
- Project name
- Project prefix
- Project creation date

**Enforcement**:
- All placeholder substitutions MUST read from `project.yaml`
- If `project.yaml` is missing or invalid, all subsequent operations MUST HALT
- Any conflict between `project.yaml` and another file MUST be resolved in favor of `project.yaml`

#### Identity File Validation

Before using `project.yaml` as substitution source, `run-create-project` MUST verify:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| File exists | `project.yaml` is present in project root | HALT: "Identity file missing: project.yaml" |
| Valid YAML | File is parseable as valid YAML | HALT: "Identity file is not valid YAML: {error}" |
| Schema version present | `schema_version` field exists and equals `1` | HALT: "Invalid or missing schema_version in project.yaml" |
| Identity section present | `identity` top-level key exists | HALT: "Missing identity section in project.yaml" |
| Slug present and valid | `identity.slug` matches format `^[a-z][a-z0-9-]*[a-z0-9]$` (lowercase, hyphen-separated, no leading/trailing hyphens) | HALT: "Invalid slug in project.yaml: {slug}" |
| Name present | `identity.name` is non-empty string | HALT: "Missing or empty name in project.yaml" |
| Prefix present and valid | `identity.prefix` matches format `^[A-Z]{1,4}$` | HALT: "Invalid prefix in project.yaml: {prefix}" |
| Created date present and valid | `identity.created` matches ISO 8601 format `YYYY-MM-DD` | HALT: "Invalid or missing created date in project.yaml" |

**Post-Generation Validation**:

After all bootstrap files are generated, `run-create-project` MUST verify:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| No unresolved placeholders | No file contains unresolved `{...}` tokens (except in code blocks) | HALT: "Unresolved placeholder in {filename}: {token}" |
| Consistency check | All references to slug/name/prefix match `project.yaml` values exactly | HALT: "Inconsistency detected: {filename} contains {field}={value}, expected {expected} from project.yaml" |
| Immutability verification | `project.yaml` has not been modified since initial creation | HALT: "Identity file was modified during bootstrap" |

#### Identity File Template

**Template Location**: `automated-builder/templates/project/project.yaml.tmpl`

**Template Content**:
```yaml
# Project Identity
# Single source-of-truth for project metadata
# Generated by run-create-project

identity:
  slug: {project-slug}
  name: {Project Name}
  prefix: {PREFIX}
  created: {YYYY-MM-DD}

schema_version: 1
```

---

#### Slug Identity Source-of-Truth vs Deployment

**Separation of Concerns**: The identity template source and the deployed identity file serve different purposes and reside in different locations.

**Template Source (Canonical Definition)**:
- **Location**: `automated-builder/templates/project/project.yaml.tmpl`
- **Purpose**: Canonical template definition for all projects
- **Scope**: System-wide, governs all project bootstraps
- **Mutability**: Version-controlled in automated-builder repository
- **Authority**: Defines the identity file structure and schema

**Deployed Identity File (Project Authority)**:
- **Location**: `../<project-slug>/project.yaml`
- **Purpose**: Single source-of-truth for THIS project's identity
- **Scope**: Project-local, authoritative only within project boundary
- **Mutability**: Immutable after bootstrap (except manual human edits)
- **Authority**: Authoritative for all project-specific identity references

**Deployment Flow**:

```
automated-builder/templates/project/project.yaml.tmpl
    ↓ (render with input parameters)
../<project-slug>/project.yaml
    ↓ (substitute tokens from)
All other project files
```

**Within-Project Authority Rules**:

1. **project.yaml is ONLY authority**: Within the project repository, `project.yaml` is the sole authoritative source for:
   - Project slug
   - Project name
   - Project prefix
   - Project creation date

2. **No competing authority**: No other file in the project may:
   - Define these values independently
   - Override values from `project.yaml`
   - Serve as primary source for these fields

3. **Derived copies allowed**: Other files (e.g., `builder-manifest.yaml`) MAY contain copies of these values, but:
   - MUST reference `project.yaml` as the source
   - MUST include comments indicating derivation
   - MUST pass consistency validation (values match exactly)

**Acceptance Criteria**:

`run-create-project` MUST satisfy:

| Criterion | Requirement | Validation |
|-----------|-------------|------------|
| Template source exists | `automated-builder/templates/project/project.yaml.tmpl` is present and readable | HALT if missing: "Identity template not found at {path}" |
| Deployment target correct | Rendered file created at `../<project-slug>/project.yaml` | HALT if wrong location: "Identity file not at expected path" |
| All tokens resolved | No `{...}` patterns remain in deployed `project.yaml` | HALT if unresolved: "Unresolved token in project.yaml: {token}" |
| Bootstrap files derived | All other bootstrap files generated using tokens from deployed `project.yaml` | HALT if inconsistency: "File {name} not derived from project.yaml" |
| project.yaml parseable | Deployed `project.yaml` is valid YAML with required structure | HALT if invalid: "Deployed identity file is not valid YAML" |
| No competing authority | No other file in project contains independent definitions of slug/prefix/name | HALT if violation: "Competing authority detected in {file}" |

**Failure Cases**:

If any of the following occur, `run-create-project` MUST HALT:

1. **Template missing**: `templates/project/project.yaml.tmpl` not found in automated-builder
2. **Deployment location wrong**: `project.yaml` created at incorrect path
3. **Unresolved tokens in identity file**: Deployed `project.yaml` contains `{...}` patterns
4. **Unparseable identity file**: Deployed `project.yaml` is not valid YAML
5. **Downstream derivation failure**: Other files not generated from `project.yaml` tokens
6. **Competing authority detected**: Another file claims to be authoritative for slug/prefix/name

---

#### Integration with Other Files

**builder-manifest.yaml Integration**:

The `builder-manifest.yaml` MUST reference (not duplicate) the identity file:

```yaml
identity_source: project.yaml

project:
  # Values below are derived from project.yaml for convenience
  # project.yaml is the authoritative source
  slug: {project-slug}
  name: {Project Name}
  prefix: {PREFIX}
  created: {YYYY-MM-DD}
```

**Documentation Integration**:

All markdown files (index.md, prd.md, etc.) MUST be generated using placeholders that are resolved from `project.yaml`.

#### Failure Cases

If any of the following occur, `run-create-project` MUST HALT immediately:

1. **Identity file creation fails**: Cannot write `project.yaml` to project root
2. **Identity file validation fails**: Any validation check fails (see table above)
3. **Substitution source unavailable**: Cannot read values from `project.yaml` for placeholder substitution
4. **Inconsistency detected**: Generated files contain values that don't match `project.yaml`
5. **Unresolved placeholders remain**: Any file (except code blocks) contains `{...}` after substitution
6. **Schema version mismatch**: `schema_version` is not `1`

---

### 3. Required Files and Contract Mapping

Each file listed below MUST be created with the specified content. Contract sources indicate which documents require each file's existence.

**Creation Order**: `project.yaml` MUST be created and validated FIRST (see Section 2.4), then all other files are generated from it.

#### 3.1 — project.yaml

**Contract Source**: Section 2.4 (Project Identity)
**Purpose**: Single source-of-truth for project identity metadata
**Required By**: All other bootstrap files (for placeholder substitution)
**Creation Order**: FIRST (before all other files)

**Initial Content**: See Section 2.4 for complete specification.

**Critical Rules**:
- Created before any other bootstrap file
- Validated before use as substitution source
- Never modified after initial creation during bootstrap
- All other files derive slug/name/prefix/created from this file

---

#### 3.2 — index.md

**Contract Source**: [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md) Step 3, Step 4
**Purpose**: Project navigation and overview
**Required By**: run-planner (Step 4: "index.md: Overview, navigation links, project status")

**Initial Content**:
```markdown
# {Project Name}

**Status**: Planning
**Last Updated**: {YYYY-MM-DD}

---

## Overview

[Brief project description - to be completed by Planner]

---

## Navigation

- [PRD](prd.md) - Product Requirements Document
- [Roadmap](roadmap.md) - Project roadmap and milestones
- [Iteration Log](iteration-log.md) - Planning evolution tracking
- [Phases](phases/) - Detailed phase plans

---

## Quick Links

### Planning Artifacts
- [Project Index](index.md) (this file)
- [PRD](prd.md)
- [Roadmap](roadmap.md)
- [Iteration Log](iteration-log.md)

### Build Artifacts
- [Build Outputs](docs/system/outputs/)

---

## Status

**Current Phase**: Pre-planning
**Next Step**: Run planner to generate initial planning artifacts
```

---

#### 3.3 — prd.md

**Contract Source**: [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md) Step 4
**Purpose**: Product requirements document
**Required By**: run-planner (Step 4: "prd.md: Goals, requirements, acceptance criteria")

**Initial Content**:
```markdown
# Product Requirements Document

**Project**: {Project Slug}
**Version**: 0.1 (pre-planning)
**Last Updated**: {YYYY-MM-DD}

---

## Overview

[To be completed by Planner]

---

## Goals

[To be completed by Planner]

---

## Requirements

### Functional Requirements

[To be completed by Planner]

### Non-Functional Requirements

[To be completed by Planner]

---

## Acceptance Criteria

[To be completed by Planner]

---

## Out of Scope

[To be completed by Planner]
```

---

#### 3.4 — roadmap.md

**Contract Source**: [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md) Step 4
**Purpose**: Milestones and timeline
**Required By**: run-planner (Step 4: "roadmap.md: Phases, milestones, dependencies")

**Initial Content**:
```markdown
# Project Roadmap

**Project**: {Project Slug}
**Last Updated**: {YYYY-MM-DD}

---

## Phases

[To be completed by Planner]

---

## Milestones

[To be completed by Planner]

---

## Dependencies

[To be completed by Planner]

---

## Timeline

[To be completed by Planner]
```

---

#### 3.5 — iteration-log.md

**Contract Source**: [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md) Step 4, Step 202
**Purpose**: Planning evolution tracking
**Required By**: run-planner (Step 4: "iteration-log.md: Initial iteration entry")

**Initial Content**:
```markdown
# Iteration Log

**Project**: {Project Slug}

---

## Iteration 0 — Bootstrap

**Date**: {YYYY-MM-DD}
**Type**: System bootstrap
**Status**: Complete

### Changes
- Project directory structure created
- Bootstrap files initialized
- Ready for Planner iteration 1

### Next Steps
- Run planner to generate initial planning artifacts

---

[Subsequent iterations will be added by Planner]
```

---

#### 3.6 — builder-manifest.yaml

**Contract Source**: [prompts/builder/run-builder.md](../../prompts/builder/run-builder.md) Step 1
**Purpose**: Project manifest for Builder operations
**Required By**: run-builder (Step 1: "Read `builder-manifest.yaml` from `{project_repo_root}`")

**Initial Content**:
```yaml
# Builder Manifest
# Version 1.0
# Auto-generated by run-create-project

version: 1

# Identity source-of-truth reference
identity_source: project.yaml

project:
  # Values derived from project.yaml (see Section 2.4)
  # project.yaml is the authoritative source
  slug: {project-slug}
  name: {Project Name}
  prefix: {PREFIX}
  created: {YYYY-MM-DD}

paths:
  index: index.md
  prd: prd.md
  roadmap: roadmap.md
  phases: phases
  iteration_log: iteration-log.md

approval:
  mechanism: marker
  marker: "<!-- APPROVED -->"

governance:
  builder_repo: ../automated-builder
  references:
    - ../automated-builder/docs/system/identity.md
    - ../automated-builder/docs/system/git.md
    - ../automated-builder/docs/system/outputs/README.md
    - ../automated-builder/docs/system/issue-resolution.md
```

**Validation Requirements** (from run-builder.md Step 1):
- Valid YAML syntax
- `version` field equals `1`
- `project.slug` is present and non-empty
- `paths.index`, `paths.prd`, `paths.roadmap`, `paths.phases` are present
- `approval.mechanism` is present (must be `marker` for MVP)
- `approval.marker` string is present and non-empty

---

#### 3.7 — phases/ directory

**Contract Source**: [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md) Step 3
**Purpose**: Container for detailed phase plans
**Required By**: run-planner (Step 3: creates phases directory structure)

**Initial State**: Empty directory with `.gitkeep` file

---

#### 3.8 — docs/system/outputs/ directory

**Contract Source**: [docs/system/outputs/README.md](../outputs/README.md)
**Purpose**: Project workflow artifacts storage
**Required By**:
- run-planner (Step 7: output artifact creation)
- run-builder (apply mode: build report creation)
- [planning.md](../../planning.md) Section "Project Artifacts Location"

**Initial State**: Empty directory with `.gitkeep` file

---

### 4. Governance References and Protection Rules

The following governance documents MUST be accessible (not copied, but referenced via relative paths in `builder-manifest.yaml`):

| Document | Path from project root | Purpose |
|----------|------------------------|---------|
| System Identity | `../automated-builder/docs/system/identity.md` | Core principles |
| Git Policy | `../automated-builder/docs/system/git.md` | Commit conventions |
| Output Rules | `../automated-builder/docs/system/outputs/README.md` | Output file naming and location |
| Issue Resolution | `../automated-builder/docs/system/issue-resolution.md` | Issue loop templates |

**Implementation Note**: These are NOT copied into the project directory. The `builder-manifest.yaml` governance section documents their canonical locations for reference.

#### 4.1 Governance File Protection Rules

**Prohibition**: `run-create-project` MUST NEVER copy governance files or directories from automated-builder into the project directory.

**Prohibited Paths** (MUST NOT be copied):

| Path Pattern | Scope | Rationale |
|--------------|-------|-----------|
| `docs/system/**` | All system documentation | Governance is single-source-of-truth in automated-builder |
| `prompts/**` | All prompt templates | Role definitions are centralized |
| `*.md` (root level) | Planning, builder, gateway contracts | Core requirements must not be duplicated |
| `CLAUDE.md` | Repository guidelines | Project-specific CLAUDE.md should be created separately if needed |
| `.git/**` | Git metadata | Each project has its own repository |
| `templates/**` | Bootstrap templates | Templates are implementation details, not project artifacts |

**Allowed References**: Projects MAY reference governance files via:
1. Relative paths in `builder-manifest.yaml` (as shown above)
2. Symbolic links (if filesystem supports and explicitly requested)
3. Documentation links in project markdown files

**Validation Checks**:

`run-create-project` MUST verify after project creation:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| No governance duplication | Project directory contains NO files matching prohibited path patterns | HALT: "Governance file copied: {path}" |
| No docs/system/ directory | Project MUST NOT contain `docs/system/` except for `docs/system/outputs/` and `docs/system/ai-process.md` | HALT: "Prohibited governance directory created: docs/system/" |
| No root-level contract files | Project MUST NOT contain `planning.md`, `builder.md`, or `gateway.md` at root | HALT: "Contract file copied: {filename}" |
| Manifest references valid | All governance paths in manifest resolve to automated-builder, not project | HALT: "Invalid governance reference: {path}" |

**Enforcement**: If any validation check fails, `run-create-project` MUST:
1. Halt immediately
2. Report the specific violation
3. NOT commit or finalize the project directory
4. Clean up partial artifacts (optional but recommended)

#### 4.2 AI Process Contract

**Purpose**: Establish project-specific AI interaction rules that govern how AI agents (Claude Code, Planner, Builder, Gatekeeper) process human input and enforce artifact constraints.

**Deployment**: `docs/system/ai-process.md` is deployed from `automated-builder/templates/project/ai-process.md.tmpl` during project creation.

**Content Requirements**: The ai-process.md file MUST document:

1. **Human Input Flexibility**:
   - Human input is flexible by design; conversational and informal phrasing is valid input
   - Human-provided input is **flexible, interpretive, and may be informal**
   - Conversational instructions, shorthand, and format variations are accepted
   - Format variations are normalized, not rejected
   - If intent is understood, proceed with normalization
   - If intent is ambiguous, ask clarifying questions
   - Examples: "My Project" → "my-project", "dg" → "DG", "make a new project called foo" → project-slug: "foo"

2. **Artifact Enforcement Timing**:
   - Enforcement applies at **artifact-write time** only
   - Rule enforcement applies at **artifact-write time** only
   - **File outputs must conform strictly to rules** when committed to disk
   - Validation failures HALT execution when writing to system artifacts
   - System artifacts include: `project.yaml`, `{PREFIX}-pending-items.md`, `builder-manifest.yaml`, phase plans, output artifacts
   - Input parsing and normalization do NOT trigger HALT conditions
   - Conversational flexibility does NOT extend to artifact structure

3. **Inventory-Proposal Validation Protocol**:
   - Validation MUST locate the most recent inventory-proposal for the target item ID
   - When validating an Inventory-Proposal implementation, agents MUST **deterministically locate** the most recent inventory-proposal artifact in `docs/system/outputs/`
   - Filename pattern: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal.md`
   - **Deterministic selection**: Highest date (YYYY-MM-DD), then highest sequence number (NN), matching the item ID
   - Validation MUST reference the most recent (highest date + sequence number) matching the item ID
   - If no inventory-proposal found, HALT: "No inventory-proposal found for item {id}"
   - If multiple candidates with same date+sequence, HALT: "Ambiguous inventory-proposal artifacts for item {id}"

4. **Enforcement Scope**:
   - Rule files enforce: structure, identifiers, ordering, invariants
   - Enforcement targets: files written to project directories, committed artifacts
   - Non-enforcement: conversational responses, exploratory questions, human input parsing

**Template Placeholders**: The ai-process.md.tmpl file uses:
- `{project-slug}`: Project identifier
- `{PREFIX}`: Project prefix for pending items
- `{Project Name}`: Human-readable project name

**Contract Validation**: After deployment, `run-create-project` MUST verify:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| File exists | `docs/system/ai-process.md` exists | HALT: "Required file missing: docs/system/ai-process.md" |
| File readable | File has read permissions | HALT: "Cannot read: docs/system/ai-process.md" |
| Placeholders resolved | No unresolved `{...}` tokens remain | HALT: "Unresolved placeholders in ai-process.md" |
| Prefix present | File contains project-specific prefix reference | HALT: "Prefix not set in ai-process.md" |

---

## Input Parameters and Resolution Rules

`run-create-project` MUST accept the following parameters:

| Parameter | Type | Required | Format | Example |
|-----------|------|----------|--------|---------|
| `project-slug` | string | Yes | lowercase, hyphen-separated | `devotional-generator` |
| `project-name` | string | Yes | Human-readable title | `Devotional Generator` |
| `prefix` | string | No* | 1-4 uppercase letters | `DG` |
| `parent-dir` | path | No** | Absolute path | `/Users/me/projects` |

\* *Default for prefix*: Derived from `project-slug` (see Section 5.1)
\*\* *Default for parent-dir*: Parent directory of `automated-builder` repository

---

### 5.1 Namespace Conversion Contract

**Purpose**: Map automated-builder's `P-###` pending items to project-specific `<PREFIX>-###` identifiers.

#### Prefix Determination Rules

**Explicit Prefix** (when `prefix` parameter provided):
- Use the provided prefix value directly
- MUST be 1-4 uppercase letters (A-Z only)
- MUST be unique across all projects (implementation should warn if collision detected)

**Derived Prefix** (when `prefix` parameter omitted):

Algorithm:
1. Extract capital letters from `project-name` parameter
2. If result is 1-4 letters, use as prefix
3. If result is 0 letters (no capitals), extract first 2 letters of first word in `project-slug` and uppercase
4. If result is >4 letters, use first 2 and last 1 letter

Examples:

| project-name | project-slug | Derived Prefix |
|--------------|--------------|----------------|
| Devotional Generator | devotional-generator | DG |
| API Gateway | api-gateway | AG |
| blog-api | blog-api | BLO (derived from slug) |
| MyCoolApp | my-cool-app | MCA |
| ULTRA_MEGA_SUPER_APP | ultra-mega-super-app | UMA (first 2 + last 1) |

#### Namespace Mapping Rules

Once prefix is determined:

| Source Identifier | Project Identifier | Example (prefix=DG) |
|-------------------|-------------------|---------------------|
| P-001 | {PREFIX}-001 | DG-001 |
| P-042 | {PREFIX}-042 | DG-042 |
| P-999 | {PREFIX}-999 | DG-999 |

**Enforcement**:
- All project-specific pending items MUST use `{PREFIX}-###` format
- Project MUST NOT reference automated-builder `P-###` identifiers directly
- Prefix MUST be stored in `project.yaml` as the authoritative source (see Section 2.4)
- `builder-manifest.yaml` includes the prefix (derived from `project.yaml`)

**Storage Location**:
- Primary: `project.yaml` field `identity.prefix` (authoritative)
- Secondary: `builder-manifest.yaml` field `project.prefix` (derived copy for convenience)

**Template Substitution**:
- `{PREFIX}` token in templates MUST be replaced with value from `project.yaml`
- If prefix determination fails, HALT immediately (see failure cases below)

#### Validation and Failure Cases

**Validation Timing**: These checks apply at **artifact-write time** (when creating `project.yaml`), not at input-parsing time.

**Input Normalization**: Before validation:
- Prefix input normalized to uppercase (e.g., "dg" → "DG")
- Slug input normalized to lowercase-hyphen format
- Name input trimmed and whitespace normalized

`run-create-project` MUST validate at artifact-write time:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| Explicit prefix format | If provided (after normalization), matches regex `^[A-Z]{1,4}$` | HALT: "Invalid prefix format: {prefix}. Must be 1-4 uppercase letters." |
| Derivation successful | Derived prefix (after normalization) is 1-4 letters | HALT: "Cannot derive valid prefix from project-name: {name} and project-slug: {slug}" |
| No empty prefix | Prefix (after normalization) is not empty string | HALT: "Empty prefix not allowed" |
| Prefix in identity file | `project.yaml` contains `identity.prefix` field with valid value | HALT: "Prefix not set in project.yaml identity section" |
| Prefix consistency | If present in both files, `project.yaml` and `builder-manifest.yaml` prefix values match | HALT: "Prefix mismatch: project.yaml={value1}, manifest={value2}" |

---

### 5.2 Path Resolution Invariants

**Required Relationship**: Project directory MUST be sibling to automated-builder directory.

#### Resolution Algorithm

1. **Determine automated-builder root**:
   - Find git repository root of automated-builder
   - Verify `.git/` directory exists
   - This is `BUILDER_ROOT`

2. **Determine parent directory**:
   - If `parent-dir` parameter provided: use it directly
   - If `parent-dir` parameter omitted: use `dirname(BUILDER_ROOT)`
   - This is `PARENT_DIR`

3. **Compute project path**:
   - `PROJECT_PATH` = `PARENT_DIR` + `/` + `project-slug`

4. **Verify sibling relationship**:
   - `dirname(PROJECT_PATH)` MUST equal `dirname(BUILDER_ROOT)`
   - Both must have same parent directory

#### Required Invariants

`run-create-project` MUST enforce:

| Invariant | Rule | Example |
|-----------|------|---------|
| Sibling structure | `PROJECT_PATH` and `BUILDER_ROOT` share same parent | `/projects/automated-builder` and `/projects/my-project` |
| Relative path determinism | `../automated-builder` from project root MUST resolve to builder root | From `/projects/my-project/`, `../automated-builder/` → `/projects/automated-builder/` |
| No nesting | Project MUST NOT be inside automated-builder or vice versa | ❌ `/projects/automated-builder/my-project/` |
| Absolute paths | All internal path computations use absolute paths | `/Users/me/projects/...` not `../...` |

#### Validation and Failure Cases

Before project creation, `run-create-project` MUST verify:

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| Builder root exists | `BUILDER_ROOT` is valid directory with `.git/` | HALT: "Cannot locate automated-builder repository root" |
| Parent dir exists | `PARENT_DIR` exists and is writable | HALT: "Parent directory does not exist or is not writable: {PARENT_DIR}" |
| No path collision | `PROJECT_PATH` does not already exist | HALT: "Project directory already exists: {PROJECT_PATH}" |
| Sibling relationship | `dirname(PROJECT_PATH)` == `dirname(BUILDER_ROOT)` | HALT: "Project must be sibling to automated-builder. Expected parent: {dirname(BUILDER_ROOT)}, got: {dirname(PROJECT_PATH)}" |
| No nested paths | Neither path is prefix of the other | HALT: "Invalid nesting: project and builder must be siblings, not nested" |
| Relative path valid | `../automated-builder` from `PROJECT_PATH` resolves to `BUILDER_ROOT` | HALT: "Relative path invariant violated: cannot reach builder from project" |

**Post-Creation Verification**:

After project creation, verify:
1. `PROJECT_PATH` exists
2. `PROJECT_PATH/../automated-builder/` resolves to `BUILDER_ROOT`
3. All governance references in manifest resolve correctly

If any check fails, halt and clean up (delete partial project directory).

---

## 6. Validation Contract

After execution, `run-create-project` MUST verify:

1. ✅ Project directory exists at `{parent-dir}/{project-slug}/`
2. ✅ Identity file (`project.yaml`) created FIRST and passes all validation per Section 2.4
3. ✅ All 9 required files exist (project.yaml, index.md, prd.md, roadmap.md, iteration-log.md, builder-manifest.yaml, docs/system/ai-process.md, phases/.gitkeep, docs/system/outputs/.gitkeep)
4. ✅ All files contain valid content (no empty files)
5. ✅ `builder-manifest.yaml` passes all validation requirements from run-builder.md
6. ✅ `builder-manifest.yaml` references `project.yaml` as identity source
7. ✅ All governance reference paths in manifest resolve correctly
8. ✅ `phases/` directory exists and is empty except for `.gitkeep`
9. ✅ `docs/system/` contains only `ai-process.md` and `outputs/` (no governance duplication per Section 4.1)
10. ✅ `docs/system/outputs/` directory exists and is empty except for `.gitkeep`
11. ✅ `docs/system/ai-process.md` passes all validation requirements per Section 4.2
12. ✅ All placeholder values resolved from `project.yaml` per Section 2.4
13. ✅ No unresolved placeholders remain per Section 2.3 (all `{...}` tokens replaced)
14. ✅ All references to slug/name/prefix/created match `project.yaml` exactly (consistency check per Section 2.4)
15. ✅ Prefix determined and set in `project.yaml` per Section 5.1
16. ✅ Path resolution invariants satisfied per Section 5.2
17. ✅ No governance files duplicated per Section 4.1

If any check fails, `run-create-project` MUST halt with a specific error message.

### 6.1 Inventory Lifecycle Contract (Aligned with issue-resolution.md)

When this Inventory-Proposal is approved:

1. The corresponding P-### entry in pending-items.md MUST be updated
   to reflect the approved inventory scope in descriptive form.
2. Issue-### items defined in this document are execution slices only.
3. Issue-### items MUST NOT be inserted into pending-items.md.
4. Execution proceeds through the issue-resolution loop using
   Issue-### proposal → approval → implementation → summary.
5. Validation is two-stage:
   - Primary: Confirm implemented Issue-### items match this Inventory-Proposal.
   - Secondary: Confirm resulting system state satisfies P-### descriptive requirements.
6. If a deferred Issue-### is required to satisfy P-### requirements,
   validation MUST fail and P-### cannot be marked complete.
7. P-### completion is authorized only by successful validation,
   not by inventory approval.

---

## 7. Non-Goals (Explicit Exclusions)

The following are **explicitly excluded** from this specification:

1. ❌ Implementation of `run-create-project` (P-084 is definition only)
2. ❌ Git initialization or first commit (manual human step)
3. ❌ Copying governance docs into project directory (use references only, per Section 4.1)
4. ❌ Running planner automatically after bootstrap
5. ❌ Creating phase plan files (planner's responsibility)
6. ❌ Pre-populating PRD with requirements (planner's responsibility)
7. ❌ Setting up external integrations, APIs, or services
8. ❌ Installing dependencies or tools
9. ❌ Template versioning system (templates are versioned with automated-builder repository)
10. ❌ Multi-project batch creation

---

## 8. Prerequisite Documentation

`run-create-project` is documented as a prerequisite in:

- [docs/system/pending-items.md](../pending-items.md) P-084 Definition of Done
- This proposal (when approved)

**Blocking Rule**: Builder MUST NOT run on `devotional-generator` (or any project) until:
1. `run-create-project` is implemented and validated
2. Project bootstrap is confirmed complete per validation contract above

---

## 9. Success Criteria (Definition of Done)

P-084 is complete when:

- [x] Explicit list of files/directories defined (Section 3)
- [x] Each required file mapped to its contract source (Section 3.1-3.8)
- [x] Initial content specified for each file (Section 3.1-3.6)
- [x] Canonical template source-of-truth defined (Section 2.1)
- [x] Placeholder substitution contract specified (Section 2.3)
- [x] Project identity (slug + prefix registry) defined (Section 2.4)
- [x] Identity file as single source-of-truth established (Section 2.4)
- [x] Creation order contract specified (project.yaml FIRST)
- [x] Governance file protection rules defined (Section 4.1)
- [x] Input parameters defined (Section 5)
- [x] Namespace conversion contract specified (Section 5.1)
- [x] Path resolution invariants specified (Section 5.2)
- [x] Validation contract specified (Section 6, 15 checks)
- [x] Non-goals explicitly documented (Section 7)
- [x] Prerequisite blocking rule documented (Section 8)
- [x] This proposal approved and committed

---

## 10. Issue-### Implementation Plan

This section defines ordered implementation slices (Issue-### items) that will safely implement P-084 end-to-end. Each Issue is independently testable with clear acceptance criteria.

**Implementation Approach**: Deterministic, contract-driven. Prefix is REQUIRED input by default (derivation requires explicit opt-in flag).

---

### Issue-001 — Create Template Directory and Base Templates

**Objective**: Establish canonical template source per Section 2.1

**Scope**:
- ✅ In: Create `automated-builder/templates/project/` directory
- ✅ In: Create 7 `.tmpl` files with placeholder content per Section 3
- ✅ In: Create `pending-items-rules.md.tmpl` for project rules pack
- ✅ In: Create `ai-process.md.tmpl` per Section 4.2
- ❌ Out: Placeholder substitution logic
- ❌ Out: Template rendering

**Acceptance Criteria**:
- [ ] Directory `templates/project/` exists at automated-builder root
- [ ] File `templates/project/project.yaml.tmpl` exists with Section 2.4 structure
- [ ] File `templates/project/index.md.tmpl` exists per Section 3.2
- [ ] File `templates/project/prd.md.tmpl` exists per Section 3.3
- [ ] File `templates/project/roadmap.md.tmpl` exists per Section 3.4
- [ ] File `templates/project/iteration-log.md.tmpl` exists per Section 3.5
- [ ] File `templates/project/builder-manifest.yaml.tmpl` exists per Section 3.6
- [ ] File `templates/project/ai-process.md.tmpl` exists per Section 4.2
- [ ] File `templates/project/pending-items-rules.md.tmpl` exists with `{PREFIX}` token
- [ ] All templates contain ONLY allowed tokens: `{project-slug}`, `{Project Slug}`, `{Project Name}`, `{YYYY-MM-DD}`, `{PREFIX}`
- [ ] All templates are readable (644 permissions minimum)

**Dependencies**: None

**Files Likely Touched**:
- `templates/project/project.yaml.tmpl` (create)
- `templates/project/index.md.tmpl` (create)
- `templates/project/prd.md.tmpl` (create)
- `templates/project/roadmap.md.tmpl` (create)
- `templates/project/iteration-log.md.tmpl` (create)
- `templates/project/builder-manifest.yaml.tmpl` (create)
- `templates/project/ai-process.md.tmpl` (create)
- `templates/project/pending-items-rules.md.tmpl` (create)

**Risks / Failure Modes**:
- Token syntax inconsistency across templates
- Missing required placeholders
- Template content not matching Section 3 specifications exactly

---

### Issue-002 — Implement run-create-project Command Scaffolding

**Objective**: Create command entry point with parameter parsing and normalization per Section 5

**Scope**:
- ✅ In: Command-line interface (bash script or other)
- ✅ In: Parameter parsing (project-slug, project-name, prefix, parent-dir)
- ✅ In: Input normalization (flexible interpretation, format conversion)
- ✅ In: Input validation (basic sanity checks only)
- ✅ In: Help/usage text
- ✅ In: `--derive-prefix` flag for optional derivation
- ❌ Out: Path resolution logic (Issue-003)
- ❌ Out: Prefix derivation algorithm (Issue-004)
- ❌ Out: File creation
- ❌ Out: Strict artifact validation (happens at write time in Issue-005, Issue-006, Issue-011)

**Acceptance Criteria**:
- [ ] Command `run-create-project` exists and is executable
- [ ] Parameter: `project-slug` (normalized to `^[a-z][a-z0-9-]*[a-z0-9]$`)
  - Accept flexible input: "My-Project", "my_project", "MY PROJECT" → normalize to "my-project"
- [ ] Parameter: `project-name` (non-empty string, whitespace trimmed)
- [ ] Parameter: `prefix` (normalized to `^[A-Z]{1,4}$`) - NO automatic derivation
  - Accept flexible input: "dg", "Dg", "DG" → normalize to "DG"
  - HALT only if normalized result invalid (e.g., "12DG", "DGXYZ5")
- [ ] Optional parameter: `parent-dir` (absolute path, defaults to dirname(BUILDER_ROOT))
- [ ] Optional flag: `--derive-prefix` (enables Section 5.1 derivation algorithm)
- [ ] HALT: "Prefix is required. Provide --prefix or use --derive-prefix" if prefix omitted and flag not set
- [ ] HALT: "Invalid slug format after normalization" if project-slug cannot be normalized to valid format
- [ ] HALT: "Invalid prefix format after normalization" if prefix cannot be normalized to valid format
- [ ] Help text documents all parameters, formats, normalization behavior, and --derive-prefix flag
- [ ] Normalizes and validates parameters but creates NO files yet
- [ ] Strict format validation deferred to artifact-write time (Issue-005, Issue-006, Issue-011)

**Dependencies**: Issue-001

**Files Likely Touched**:
- `scripts/run-create-project` or `bin/run-create-project` (create)

**Risks / Failure Modes**:
- Parameter parsing ambiguity
- Unclear error messages
- Platform-specific compatibility (bash availability)

---

### Issue-003 — Implement Path Resolution and Validation

**Objective**: Implement Section 5.2 path resolution invariants

**Scope**:
- ✅ In: Determine BUILDER_ROOT (git repo root via `.git/`)
- ✅ In: Compute PARENT_DIR (from parameter or dirname(BUILDER_ROOT))
- ✅ In: Compute PROJECT_PATH (PARENT_DIR/project-slug)
- ✅ In: Validate all 6 invariants from Section 5.2 table
- ❌ Out: File/directory creation
- ❌ Out: Post-creation verification (handled by Issue-009)

**Acceptance Criteria**:
- [ ] Locates automated-builder git root via `.git/` directory
- [ ] HALT: "Cannot locate automated-builder repository root" if not found
- [ ] HALT: "Parent directory does not exist or is not writable" if PARENT_DIR invalid
- [ ] HALT: "Project directory already exists" if PROJECT_PATH exists
- [ ] HALT: "Project must be sibling to automated-builder" if dirname mismatch
- [ ] HALT: "Invalid nesting" if either path is prefix of the other
- [ ] HALT: "Relative path invariant violated" if `../automated-builder` doesn't resolve to BUILDER_ROOT
- [ ] All path computations use absolute paths internally
- [ ] Returns validated PROJECT_PATH on success

**Dependencies**: Issue-002

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)

**Risks / Failure Modes**:
- Symbolic link resolution edge cases
- Cross-platform path handling (macOS vs Linux)
- Permission check reliability

---

### Issue-004 — Implement Prefix Determination (Required by Default)

**Objective**: Implement Section 5.1 namespace conversion with required prefix

**Scope**:
- ✅ In: Validate explicit prefix format (`^[A-Z]{1,4}$`)
- ✅ In: Optional derivation algorithm (ONLY if `--derive-prefix` flag set)
- ✅ In: Warn if derived prefix might collide (best-effort)
- ❌ Out: Automatic derivation without explicit opt-in
- ❌ Out: Storage in project.yaml (handled by Issue-005)

**Acceptance Criteria**:
- [ ] If prefix provided: validate format `^[A-Z]{1,4}$`
- [ ] If prefix NOT provided and `--derive-prefix` NOT set: HALT with required error
- [ ] If `--derive-prefix` set: execute Section 5.1 derivation algorithm
- [ ] Derivation: extract capitals from project-name
- [ ] Derivation: if 0 capitals, extract first 2 letters from project-slug and uppercase
- [ ] Derivation: if >4 capitals, use first 2 + last 1
- [ ] HALT: "Empty prefix not allowed" if derivation produces empty string
- [ ] HALT: "Cannot derive valid prefix" if derivation fails
- [ ] Returns validated prefix value on success

**Dependencies**: Issue-002

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)

**Risks / Failure Modes**:
- Prefix collision detection (no registry exists; warn only)
- Non-ASCII character handling in derivation
- Edge cases in derivation algorithm

---

### Issue-005 — Implement project.yaml Creation and Validation (FIRST)

**Objective**: Implement Section 2.4 identity file as source-of-truth, created FIRST

**Scope**:
- ✅ In: Create project root directory (PROJECT_PATH)
- ✅ In: Render `project.yaml.tmpl` → `project.yaml` (FIRST file)
- ✅ In: Substitute tokens from input parameters
- ✅ In: Validate identity file (8 checks from Section 2.4 table)
- ✅ In: Timestamp with current date (YYYY-MM-DD)
- ❌ Out: Other file creation (must wait until this succeeds)

**Acceptance Criteria**:
- [ ] Creates PROJECT_PATH directory with appropriate permissions
- [ ] Creates `PROJECT_PATH/project.yaml` BEFORE any other file
- [ ] Deployed file has no unresolved `{...}` tokens
- [ ] `identity.slug` matches input project-slug exactly
- [ ] `identity.name` matches input project-name exactly
- [ ] `identity.prefix` matches validated prefix from Issue-004
- [ ] `identity.created` is current date in ISO 8601 format (YYYY-MM-DD)
- [ ] `schema_version = 1`
- [ ] File is valid YAML (parseable via YAML parser)
- [ ] HALT: "Identity file is not valid YAML" if parse fails
- [ ] HALT: "Unresolved token in project.yaml" if `{...}` patterns remain
- [ ] HALT: "Invalid slug/prefix/date in project.yaml" if validation fails per Section 2.4 table
- [ ] File permissions are readable (minimum 644)

**Dependencies**: Issue-003, Issue-004

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)
- `../<project-slug>/project.yaml` (create - deployed file)

**Risks / Failure Modes**:
- Template read failure (Issue-001 dependency)
- Token substitution incomplete
- YAML rendering produces invalid syntax
- Filesystem write failure (permissions, disk space)
- File created but validation fails (requires cleanup)

---

### Issue-006 — Implement Placeholder Substitution for Remaining Files

**Objective**: Implement Section 2.3 placeholder substitution from project.yaml

**Scope**:
- ✅ In: Read identity values from deployed `project.yaml`
- ✅ In: Render remaining 5 templates using project.yaml as source
- ✅ In: Create index.md, prd.md, roadmap.md, iteration-log.md, builder-manifest.yaml
- ✅ In: Create phases/ and docs/system/outputs/ directories with .gitkeep
- ✅ In: Post-substitution validation (Section 2.3 table)
- ❌ Out: Governance file copying (prohibited by Section 4.1)
- ❌ Out: ai-process.md deployment (handled by Issue-011)

**Acceptance Criteria**:
- [ ] Reads identity values from `PROJECT_PATH/project.yaml` (NOT from input parameters)
- [ ] Creates `PROJECT_PATH/index.md` with all tokens substituted per Section 3.2
- [ ] Creates `PROJECT_PATH/prd.md` with all tokens substituted per Section 3.3
- [ ] Creates `PROJECT_PATH/roadmap.md` with all tokens substituted per Section 3.4
- [ ] Creates `PROJECT_PATH/iteration-log.md` with all tokens substituted per Section 3.5
- [ ] Creates `PROJECT_PATH/builder-manifest.yaml` with identity_source reference per Section 3.6
- [ ] builder-manifest.yaml contains comment: "project.yaml is the authoritative source"
- [ ] Creates `PROJECT_PATH/phases/` directory with `.gitkeep`
- [ ] Creates `PROJECT_PATH/docs/system/outputs/` directory with `.gitkeep`
- [ ] HALT: "Unresolved token in {file}" if any `{...}` patterns remain (except code blocks)
- [ ] HALT: "Empty value for token" if any token replaced with empty string
- [ ] HALT: "Inconsistency detected" if any file contains values not matching project.yaml
- [ ] All 8 non-ai-process bootstrap files exist after completion

**Dependencies**: Issue-005

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)
- `../<project-slug>/index.md` (create)
- `../<project-slug>/prd.md` (create)
- `../<project-slug>/roadmap.md` (create)
- `../<project-slug>/iteration-log.md` (create)
- `../<project-slug>/builder-manifest.yaml` (create)
- `../<project-slug>/phases/.gitkeep` (create)
- `../<project-slug>/docs/system/outputs/.gitkeep` (create)

**Risks / Failure Modes**:
- Reading deployed project.yaml fails (should not happen, just created)
- Template missing for a file
- Token substitution logic inconsistent with Issue-005
- Directory creation permissions issues

---

### Issue-011 — Deploy ai-process.md and Enforce AI Process Contract

**Objective**: Deploy `docs/system/ai-process.md` and enforce Section 4.2 contract guarantees

**Scope**:
- ✅ In: Render `ai-process.md.tmpl` using identity values from deployed `project.yaml`
- ✅ In: Create `PROJECT_PATH/docs/system/ai-process.md`
- ✅ In: Validate ai-process contract content for:
  - human input flexibility language
  - artifact-write-time enforcement language
  - deterministic lookup of most recent inventory-proposal
- ✅ In: Apply Section 4.2 post-deployment validation checks
- ❌ Out: Governance artifact-type policy updates (Issue-010)

**Acceptance Criteria**:
- [ ] Reads identity values from `PROJECT_PATH/project.yaml` (not raw CLI input)
- [ ] Creates `PROJECT_PATH/docs/system/ai-process.md` from template with all tokens resolved
- [ ] ai-process.md explicitly states human input is flexible and normalizable
- [ ] ai-process.md explicitly states enforcement occurs at artifact-write time
- [ ] ai-process.md explicitly requires deterministic selection of most recent inventory-proposal artifact
- [ ] HALT: "Required file missing: docs/system/ai-process.md" if deployment fails
- [ ] HALT: "Unresolved placeholders in ai-process.md" if any `{...}` tokens remain
- [ ] HALT: "Prefix not set in ai-process.md" if project-specific prefix is missing
- [ ] Combined with Issue-006 outputs, all 9 required files exist

**Dependencies**: Issue-005

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)
- `../<project-slug>/docs/system/ai-process.md` (create)

**Risks / Failure Modes**:
- ai-process.md generated with stale values instead of project.yaml identity source
- Contract language drift from Section 4.2 requirements
- Token substitution incomplete

---

### Issue-007 — Implement Governance Protection Validation

**Objective**: Implement Section 4.1 governance file protection rules

**Scope**:
- ✅ In: Post-creation scan of PROJECT_PATH
- ✅ In: Validate no prohibited paths present per Section 4.1 table
- ✅ In: Validate governance references in manifest point to automated-builder
- ❌ Out: Prevention during creation (this is post-validation only)

**Acceptance Criteria**:
- [ ] Scans PROJECT_PATH recursively for prohibited patterns
- [ ] HALT: "Governance file copied: {path}" if `docs/system/**` found (except `docs/system/outputs/`)
- [ ] HALT: "Prohibited governance directory created" if `docs/system/` exists without outputs subdirectory
- [ ] HALT: "Contract file copied" if `planning.md`, `builder.md`, or `gateway.md` found at root
- [ ] HALT: "Governance file copied" if `prompts/**`, `templates/**`, `.git/**` found
- [ ] Validates `builder-manifest.yaml` governance.references paths resolve to `../automated-builder/`
- [ ] HALT: "Invalid governance reference" if any reference resolves within PROJECT_PATH
- [ ] Passes if only `docs/system/outputs/` exists under docs/system/
- [ ] Allows `docs/system/pending-items-rules.md` (project-specific, not governance)

**Dependencies**: Issue-006, Issue-011

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)

**Risks / Failure Modes**:
- Symbolic link traversal could bypass detection
- Hidden files (`.filename`) might not be scanned
- Case-insensitive filesystems (macOS) create ambiguity
- Relative path resolution edge cases

---

### Issue-008 — Deploy Project Rules Pack Template

**Objective**: Deploy project-specific pending-items-rules.md with PREFIX substitution

**Scope**:
- ✅ In: Render `pending-items-rules.md.tmpl` with `{PREFIX}` substituted
- ✅ In: Deploy to `PROJECT_PATH/docs/system/pending-items-rules.md`
- ✅ In: Create parent directory `docs/system/` if not exists
- ❌ Out: Complex rules logic (just template rendering)

**Acceptance Criteria**:
- [ ] Template exists: `templates/project/pending-items-rules.md.tmpl` (from Issue-001)
- [ ] Template contains P-### → {PREFIX}-### mapping rule
- [ ] Creates `PROJECT_PATH/docs/system/` directory if needed
- [ ] Deploys to `PROJECT_PATH/docs/system/pending-items-rules.md`
- [ ] `{PREFIX}` token replaced with actual project prefix from project.yaml
- [ ] HALT: "Unresolved token in pending-items-rules.md" if `{PREFIX}` remains
- [ ] File references project.yaml as identity source
- [ ] Does NOT conflict with governance protection (rules are project-specific)

**Dependencies**: Issue-005 (needs project.yaml for PREFIX value)

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)
- `../<project-slug>/docs/system/pending-items-rules.md` (create)

**Risks / Failure Modes**:
- Creates docs/system/ which governance protection checks for (but allows project-specific files)
- Template content unclear (what rules to include?)
- Prefix substitution inconsistent with Issue-005

---

### Issue-009 — End-to-End Validation and Cleanup

**Objective**: Implement Section 6 validation contract (15 checks) and cleanup on failure

**Scope**:
- ✅ In: Execute all 15 validation checks from Section 6
- ✅ In: Provide clear error messages for each failure
- ✅ In: Cleanup partial artifacts on any failure
- ✅ In: Success confirmation message with project path
- ❌ Out: Git initialization (explicit non-goal per Section 7)
- ❌ Out: Running planner automatically (explicit non-goal per Section 7)

**Acceptance Criteria**:
- [ ] Check 1: Project directory exists at expected path
- [ ] Check 2: project.yaml created FIRST and passes all Section 2.4 validation
- [ ] Check 3: All 9 required files exist
- [ ] Check 4: All files contain valid content (no empty files)
- [ ] Check 5: builder-manifest.yaml passes run-builder.md validation
- [ ] Check 6: builder-manifest.yaml references project.yaml as identity_source
- [ ] Check 7: All governance reference paths resolve correctly
- [ ] Check 8: phases/ directory exists and contains only .gitkeep
- [ ] Check 9: docs/system/outputs/ directory exists and contains only .gitkeep
- [ ] Check 10: All placeholder values resolved from project.yaml
- [ ] Check 11: No unresolved placeholders remain
- [ ] Check 12: All references match project.yaml exactly (consistency)
- [ ] Check 13: Prefix determined and set in project.yaml
- [ ] Check 14: Path resolution invariants satisfied
- [ ] Check 15: No governance files duplicated
- [ ] On ANY failure: delete PROJECT_PATH recursively (cleanup)
- [ ] On success: output "Project created: {PROJECT_PATH}"
- [ ] On success: output "Identity file: {PROJECT_PATH}/project.yaml"
- [ ] Does NOT initialize git repository
- [ ] Does NOT run planner automatically

**Dependencies**: Issue-006, Issue-007, Issue-008, Issue-011

**Files Likely Touched**:
- Same as Issue-002 (extend command implementation)

**Risks / Failure Modes**:
- Cleanup failure leaves partial state
- Validation check order matters (some depend on others)
- Error messages too generic or unclear
- Cleanup too aggressive (deletes unintended files if PROJECT_PATH computed incorrectly)
- Success message unclear about next steps

---

### Issue-010 — Introduce Inventory-Proposal Artifact Type (Governance)

**Objective**: Establish inventory-proposal as a formal artifact type with standardized naming and validation lookup behavior

**Scope**:
- ✅ In: Define artifact type: inventory-proposal
- ✅ In: Document naming convention: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal.md`
- ✅ In: Update validation lookup to reference most recent inventory-proposal in docs/system/outputs/
- ✅ In: Document Inventory Lifecycle Contract (Section 6.1)
- ✅ In: Document in governance (docs/system/ or similar)
- ❌ Out: Implementation of run-create-project (that's Issue-001 through Issue-009 and Issue-011)

**Acceptance Criteria**:
- [ ] Artifact type "inventory-proposal" defined in governance documentation
- [ ] Naming convention documented: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal.md`
- [ ] Example: `2026-02-13__01__system__p-084-inventory-proposal.md`
- [ ] Purpose documented: "Specification/inventory for implementation; does not execute"
- [ ] Relationship to Issue-### documented: "Inventory-proposals contain Issue-### implementation plans"
- [ ] Validation lookup behavior: "Tools/processes reference most recent inventory-proposal in docs/system/outputs/ for item {id}"
- [ ] Distinction from regular proposals: "Inventory-proposals are definition-only; Issue-### items are implementation"
- [ ] Renaming rule: This P-084 document renamed to `2026-02-13__01__system__p-084-inventory-proposal.md` when committed
- [ ] Document added to: `docs/system/outputs/README.md` or new `docs/system/artifact-types.md`
- [ ] **Inventory Lifecycle Contract** documented per Section 6.1:
  - P-### entry updated to reflect approved inventory scope
  - Issue-### items are execution slices only
  - Issue-### items MUST NOT be inserted into pending-items.md
  - Execution proceeds through issue-resolution loop
  - Two-stage validation (Issue-### match + P-### requirements)
  - Deferred Issue-### prevents P-### completion
  - P-### completion requires successful validation only
- [ ] **Input Normalization vs Artifact Enforcement** principle documented:
  - Rule files enforce deterministic structure and invariants on **system artifacts** only
  - Human input remains flexible and is normalized, not rejected
  - Enforcement rules apply at **artifact-write time**, not at conversational input time
  - If intent is understood, implement; if ambiguous, ask clarifying questions
  - Rule files enforce: structure, IDs, ordering, invariants **after artifact write**
  - Examples documented showing input normalization (e.g., "dg" → "DG", "My Project" → "my-project")

**Dependencies**: None (governance change, independent of implementation)

**Files Likely Touched**:
- `docs/system/outputs/README.md` (extend with new artifact type)
- OR `docs/system/artifact-types.md` (create)
- `docs/system/issue-resolution.md` (add inventory lifecycle contract documentation)
- `2026-02-13__01__system__p-084-proposal.md` (rename to `p-084-inventory-proposal.md` on commit)

**Risks / Failure Modes**:
- Artifact type not clear vs existing proposal types
- Naming convention conflicts with existing patterns
- Unclear when to use inventory-proposal vs regular proposal
- Validation lookup logic not implemented (out of scope; documented only)
- Inventory lifecycle contract not followed consistently
- Two-stage validation not performed correctly

---

### Implementation Summary

**Execution Order**:
1. Issue-010: Governance (artifact type) - can be parallel
2. Issue-001: Templates
3. Issue-002: Command scaffolding
4. Issue-003 + Issue-004: Path resolution and prefix (parallel)
5. Issue-005: project.yaml (FIRST file, depends on 003+004)
6. Issue-006 + Issue-011: Remaining files + ai-process deployment (parallel, both depend on 005)
7. Issue-007: Governance protection (depends on 006+011)
8. Issue-008: Rules pack deployment (depends on 005)
9. Issue-009: End-to-end validation (depends on 006+007+008+011)

**Critical Path**: Issue-001 → Issue-002 → {Issue-003, Issue-004} → Issue-005 → Issue-011 → Issue-007 → Issue-009

**Total Issue Items**: 11 (10 implementation + 1 governance)

**Determinism Enforced**:
- Prefix is REQUIRED by default (Issue-004)
- Derivation requires explicit `--derive-prefix` flag
- Template source is canonical (Issue-001)
- project.yaml is FIRST and source-of-truth (Issue-005)
- All validation is explicit and deterministic (Issue-009)

---

## 11. Next Steps (Post-Approval)

**Phase 1: Approval and Governance**

1. Human approves this inventory-proposal
2. Artifact renamed to `2026-02-13__01__system__p-084-inventory-proposal.md` (if not already done)
3. Approved artifact committed (this is definition; implementation is separate)
4. P-084 remains in Pending (definition complete, implementation TBD)

**Phase 2: Governance Update (Issue-010)**

5. Execute Issue-010: Introduce inventory-proposal artifact type in governance
   - Update `docs/system/outputs/README.md` or create `docs/system/artifact-types.md`
   - Document artifact type, naming convention, and purpose
   - Document INVENTORY VALIDATION INSERTION RULE in `docs/system/issue-resolution.md`
   - Commit governance changes

**Phase 3: Execution**

6. Issue-001 through Issue-009 and Issue-011 follow normal execution lifecycle:
   - Each requires separate approval before execution
   - Each generates proposal → approval → implementation → summary
   - Dependencies per Section 10 Implementation Summary must be respected

---

## References

- [P-084 in pending-items.md](../pending-items.md#P-084)
- [prompts/planner/run-planner.md](../../prompts/planner/run-planner.md)
- [prompts/builder/run-builder.md](../../prompts/builder/run-builder.md)
- [docs/system/outputs/README.md](../outputs/README.md)
- [planning.md](../../planning.md)
- [docs/system/issue-resolution.md](../issue-resolution.md)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 2.1 | 2026-02-13 | Lifecycle alignment with issue-resolution.md: DELETED Section 6.1 INVENTORY VALIDATION INSERTION RULE (~70 lines); REPLACED with new Section 6.1 Inventory Lifecycle Contract (7 principles); REMOVED Phase 3 Issue-### Insertion from Section 11; REMOVED insertion-related content from Issue-010 (objective, scope, acceptance criteria, files, risks); Issue-### items remain as execution slices only; no insertion into pending-items.md; validation is two-stage (Issue-### match + P-### requirements) |
| 2.0 | 2026-02-13 | Terminology alignment with issue-resolution.md: systematically replaced all Fix-### with Issue-### (11 section headers, 50+ inline references); updated Section 10 title to Issue-### Implementation Plan; updated all cross-references, dependencies, and execution order; updated INVENTORY VALIDATION INSERTION RULE terminology; updated all acceptance criteria and risks; no technical content changed, only terminology aligned |
| 1.9 | 2026-02-13 | Add dedicated Issue-011 for `docs/system/ai-process.md` deployment and validation; narrow Issue-006 scope to non-ai-process files; update Issue-007/Issue-009 dependency chain; update execution order, critical path, total issue count, and Next Steps insertion range; make Section 4.2 clarifications explicit (human input flexibility, artifact-write enforcement timing, most-recent inventory-proposal lookup) |
| 1.8 | 2026-02-13 | Strengthen AI Process Contract wording: update Section 4.2 item 1 (add "may be informal", conversational examples); update Section 4.2 item 2 (add "file outputs must conform strictly", conversational flexibility caveat); update Section 4.2 item 3 (add "deterministically locate", deterministic selection rules, ambiguity HALT); update Issue-010 acceptance criteria (add ID Allocation Rule Reconciliation requirement); update Issue-010 risks (add ID allocation conflict risks) |
| 1.7 | 2026-02-13 | Add ai-process.md deployment: update Section 1 (directory structure); update Section 2.1 (template storage, add ai-process.md.tmpl); update Section 2.2 (7 templates); add Section 4.2 (AI Process Contract); update Section 4.1 (allow ai-process.md exception); update Section 6 (9 required files, add checks 9, 11); update Issue-001 (8 templates); update Issue-006 (6 templates deployed, ai-process.md deployment) |
| 1.6 | 2026-02-13 | Clarify input normalization vs artifact enforcement principle: add new section after Problem Statement; update Section 5.1 (validation timing, input normalization); update Section 6.1 (enforcement timing, human input flexibility); update Issue-002 (normalization scope, flexible input acceptance); update Issue-010 acceptance criteria (add Input Normalization vs Artifact Enforcement principle) |
| 1.5 | 2026-02-13 | Add INVENTORY VALIDATION INSERTION RULE: define protocol for inserting Issue-### items into pending-items.md as canonical items; update Issue-010 acceptance criteria; add Section 6.1 (Inventory-Proposal Validation Protocol); restructure Section 11 (Next Steps) into 4 phases; add governance file targets and deferred marker handling |
| 1.4 | 2026-02-13 | Reclassify as Inventory-Proposal artifact type; add Section 10: Issue-### Implementation Plan (10 issue items: 9 implementation + 1 governance); update header to "Definition Only" status; add Issue-010 to introduce inventory-proposal artifact type; update Next Steps for inventory-proposal workflow |
| 1.3 | 2026-02-13 | Add "Slug Identity Source-of-Truth vs Deployment" section clarifying template source (automated-builder) vs deployed file (project); update template paths from `templates/project-bootstrap/*.template` to `templates/project/*.tmpl`; add 6 acceptance criteria and 6 failure cases for template-to-deployment flow |
| 1.2 | 2026-02-13 | Add Project Identity section (2.4): project.yaml as single source-of-truth for slug/name/prefix/created; enforce creation-order contract (identity file FIRST); update all sections to reference identity file; expand validation to 15 checks |
| 1.1 | 2026-02-13 | Add architectural contracts: Namespace Conversion (5.1), Canonical Template Source-of-Truth (2), Placeholder Substitution (2.3), Governance File Protection (4.1), Path Resolution Invariants (5.2) |
| 1.0 | 2026-02-13 | Initial proposal for P-084 |
