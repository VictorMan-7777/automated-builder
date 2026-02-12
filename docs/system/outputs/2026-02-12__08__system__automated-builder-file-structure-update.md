# Automated Builder File Structure (Updated State)

- Date captured: 2026-02-12
- Context: system
- Purpose: Updated human design reference for repository structure (non-destructive update; prior snapshot retained).

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

## Update Notes

- This snapshot supersedes structural assumptions from `2026-02-12__05__system__automated-builder-file-structure.md` while preserving that file as historical record.
- `docs/projects/` is not part of the current repository tree.
- Per approved P-083 direction, planner project outputs are rooted in the parent projects directory (outside this repository).
- `.git/`, `.vscode/`, `.claude/`, and `.DS_Store` are intentionally excluded from the contract tree view.
