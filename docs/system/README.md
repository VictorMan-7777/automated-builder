# System Documentation

**Location**: `docs/system/`
**Purpose**: System-level documentation and outputs for the automated-builder framework
**Version**: 1.0
**Last Updated**: 2026-02-05

---

## Quick Start

**👉 New to the system?** Start here: **[index.md](index.md)** - System Overview

The system overview provides:
- Purpose and non-goals
- Role definitions (Planner, Builder, Gatekeeper)
- Typical workflow
- How to get started

---

## Overview

This directory contains system-level documentation that applies to the entire automated-builder framework, as opposed to individual project planning artifacts.

---

## Directory Structure

```
docs/
├── system/                 # System-level documentation
│   ├── index.md            # System Overview (START HERE)
│   ├── README.md           # This file (directory index)
│   ├── changelog.md        # System documentation changes
│   ├── issue-resolution.md # Issue numbering and severity scheme
│   └── outputs/            # Long output capture directory
│       ├── README.md       # Output capture rules
│       └── YYYY-MM-DD__NN__<context>__*.md
├── global/                 # Cross-cutting references
│   └── tooling-locations.md
└── implementation/         # Approved operational contracts
    └── system/
        └── checkpoint-taxonomy.md  (APPROVED)
```

---

## Subdirectories

### outputs/

**Purpose**: Canonical storage for lengthy Claude Code outputs

Long outputs (summaries, reports, file trees) that exceed comfortable chat readability are saved here as permanent records.

**See**: [outputs/README.md](outputs/README.md) for complete rules

**Examples**:
- Planning phase completion summaries
- Build phase completion reports
- Gatekeeper review decisions
- Reorganization summaries
- Project file trees

### ../global/

**Purpose**: Cross-cutting references that apply outside any single role or project

- **[tooling-locations.md](../global/tooling-locations.md)** — Clawdbot CLI install paths and runtime details

### ../implementation/

**Purpose**: Approved operational contracts governing session behaviour

- **[system/checkpoint-taxonomy.md](../implementation/system/checkpoint-taxonomy.md)** — Checkpoint taxonomy and execution contract (APPROVED)

---

## System Documentation vs Project Documentation

### System Documentation (this directory)

**Location**: `docs/system/`

**Purpose**: Framework-level documentation

**Contains**:
- Framework outputs (this directory)
- System-wide rules and processes
- Cross-project reports
- Framework evolution logs

**Examples**:
- Long output captures
- Multi-project status reports
- Framework migration logs

### Project Documentation

**Location**: `../<project-slug>/` (parent directory, per P-083)

**Purpose**: Individual project planning artifacts

**Contains**:
- Project PRD, roadmap, iteration logs
- Phase plans
- Project-specific workflow outputs

**Structure**:
```
<parent-projects-dir>/
├── automated-builder/   (this repo)
└── <project-slug>/
    ├── prd.md
    ├── phases/001-phase-name.md
    └── docs/system/outputs/  # Project workflow artifacts
```

_Note: Previously stored in `docs/projects/<slug>/` before P-083 relocation._

---

## Root-Level Documentation

The following docs live at repository root (not in docs/system/):

- **[planning.md](../../planning.md)** - Planning stage requirements
- **[builder.md](../../builder.md)** - Builder stage requirements
- **[gateway.md](../../gateway.md)** - Gatekeeper requirements
- **[CLAUDE.md](../../CLAUDE.md)** - Project conventions

These are framework requirements, not system outputs or project plans.

---

## When to Add System Documentation

Add documentation to `docs/system/` when:

1. **Framework-level outputs** - Applies to entire framework, not single project
2. **Cross-cutting concerns** - Affects multiple projects or roles
3. **Permanent reference** - Long-term record needed
4. **System evolution** - Tracking framework changes over time

Do NOT add:
- Project-specific planning (goes to `../<slug>/`, per P-083)
- Role requirements (goes to root level: planning.md, builder.md, gateway.md)
- System prompts (goes to `prompts/planner/`, `prompts/builder/`, `prompts/gatekeeper/`)

---

## Related Documentation

- [Root README](../../README.md) - Repository overview
- [planning.md](../../planning.md) - Planning requirements
- [builder.md](../../builder.md) - Builder requirements
- [gateway.md](../../gateway.md) - Gatekeeper requirements
- [CLAUDE.md](../../CLAUDE.md) - Project conventions

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Initial system documentation index |
