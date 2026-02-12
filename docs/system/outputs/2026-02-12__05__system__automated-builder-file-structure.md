# Automated Builder File Structure (Current State)

- Date captured: 2026-02-12
- Context: system
- Purpose: Human design reference for planning `run-create-project` (not an automation spec).

## Repository Tree (Directories + Key Files)

```text
.
├── CLAUDE.md - Session-level collaboration and execution instructions.
├── automated-builder.code-workspace - Workspace configuration.
├── builder.md - Builder system contract and behavior reference.
├── gateway.md - Gatekeeper/gateway contract reference.
├── planning.md - High-level planning and system direction document.
├── docs/
│   ├── global/
│   │   └── tooling-locations.md - Tooling/path reference used across the system.
│   ├── implementation/
│   │   └── system/
│   │       └── checkpoint-taxonomy.md - Checkpoint definitions used by planner/builder flow.
│   ├── projects/
│   │   └── devotional-generator/
│   │       ├── index.md - Project entry point.
│   │       ├── iteration-log.md - Iteration history for the project.
│   │       ├── prd.md - Product requirements document.
│   │       ├── roadmap.md - Phased plan and sequencing.
│   │       └── phases/
│   │           ├── 001-data-model-inputs.md
│   │           ├── 001-project-scaffold.md
│   │           ├── 002-template-system.md
│   │           ├── 003-content-library.md
│   │           ├── 003-kdp-pdf-export.md
│   │           ├── 004-validation-preview.md
│   │           └── 005-export-distribution.md
│   └── system/
│       ├── README.md - System docs overview.
│       ├── access.md - Access and execution governance.
│       ├── ai.md - AI usage/system guidance.
│       ├── changelog.md - System documentation change history.
│       ├── git.md - Git workflow rules.
│       ├── identity.md - System identity and role framing.
│       ├── index.md - Navigation index for system docs.
│       ├── initial-prompt.md - Base prompt/bootstrap context.
│       ├── issue-resolution.md - Issue proposal/approval loop contract.
│       ├── pending-items.md - Pending/completed item registry.
│       ├── prompt-template.md - Reusable prompt template.
│       ├── run-planner.md - Planner run contract and required flow.
│       ├── session-setup.md - Session bootstrap instructions.
│       └── outputs/
│           ├── README.md - Output artifact naming/iterator and storage rules.
│           ├── active-pending.md - Current active pending subset.
│           └── YYYY-MM-DD__NN__<context>__<description>.md - Iteration output artifacts.
└── prompts/
    ├── builder/
    │   ├── builder-base.md - Base builder prompt.
    │   └── run-builder.md - Builder run prompt/contract.
    ├── gatekeeper/
    │   └── gatekeeper-checklist.md - Gatekeeper review checklist.
    └── planner/
        ├── planner-base.md - Base planner prompt.
        └── run-planner.md - Planner run prompt.
```

## Notes

- `.git/`, `.vscode/`, `.claude/`, and `.DS_Store` files are intentionally omitted from the tree above because they are not part of the runtime doc contracts.
- The `docs/system/` + `prompts/` paths are the core contract surface that `run-create-project` will need to bootstrap for new projects.
