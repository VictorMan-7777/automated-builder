# P-083 Proposal — Relocate Planner Output Root to Parent Projects Directory

**Pending item**: P-083 — Move Planner project planning docs and workflow artifacts from automated-builder to parent-level `../<slug>/`
**Date**: 2026-02-12

---

## Context

The Planner currently writes project planning artifacts (PRD, roadmap,
phase plans, iteration log) to `docs/projects/<slug>/` inside the
automated-builder repository. Project-specific workflow artifacts
(proposals, approvals, verifications, implementation summaries) are written
to `docs/system/outputs/` inside automated-builder, mixed in with
automated-builder's own system artifacts.

This is undesirable for two reasons:

1. Planned projects are not part of the automated-builder system itself —
   they are independent projects that happen to be planned using the
   automated-builder's Planner. Storing them inside automated-builder
   conflates the build system with its outputs.
2. Project-specific workflow artifacts (e.g., a devotional-generator
   proposal) are interleaved with automated-builder system artifacts
   (e.g., an architecture review), making both harder to find.

The parent directory (`..` relative to the automated-builder repo root)
already contains sibling project directories (e.g., `devotional-project-test`,
`gsd-sandbox`, `honey-book`). Writing all project documents alongside
automated-builder in this directory aligns with the existing filesystem
convention.

---

## Current Behavior vs Proposed Behavior

### Current

Planning docs and workflow artifacts are split across two locations inside
automated-builder:

```
automated-builder/
├── docs/
│   ├── projects/
│   │   └── <slug>/                          ← planning docs
│   │       ├── index.md
│   │       ├── prd.md
│   │       ├── roadmap.md
│   │       ├── iteration-log.md
│   │       └── phases/
│   │           ├── 001-phase-one.md
│   │           └── ...
│   └── system/
│       └── outputs/                         ← workflow artifacts (mixed with system artifacts)
│           ├── YYYY-MM-DD__NN__planner__<description>.md
│           ├── YYYY-MM-DD__NN__builder__<description>.md
│           └── YYYY-MM-DD__NN__system__<description>.md   ← system-level (stays here)
```

### Proposed

All project-specific documents — planning docs and workflow artifacts —
live under the project directory alongside automated-builder:

```
<parent-projects-dir>/
├── automated-builder/   (this repo — unchanged)
└── <slug>/
    ├── index.md                             ← planning docs
    ├── prd.md
    ├── roadmap.md
    ├── iteration-log.md
    ├── phases/
    │   ├── 001-phase-one.md
    │   └── ...
    └── docs/
        └── system/
            └── outputs/                     ← project workflow artifacts
                └── YYYY-MM-DD__NN__<context>__<description>.md
```

Two write roots, both under `../<slug>/`:

- **Planning docs**: `../<slug>/` (index.md, prd.md, roadmap.md,
  iteration-log.md, phases/)
- **Workflow artifacts**: `../<slug>/docs/system/outputs/` (proposals,
  approvals, verifications, implementation summaries, run reports)

Automated-builder's own `docs/system/outputs/` continues to store
system-level artifacts (issue resolutions, verification artifacts,
architecture reviews, etc.) that are about the automated-builder itself,
not about a specific project.

---

## How the Planner Discovers the Parent Projects Directory

No runtime discovery mechanism is introduced. The convention is static and
documented:

1. The **parent projects directory** is defined as the immediate parent of
   the automated-builder repository root — i.e., `..` resolved from the
   repo root.
2. Authoritative documents express the planning docs root as `../<slug>/`
   and the workflow artifacts root as `../<slug>/docs/system/outputs/`
   (both relative to the automated-builder repo root).
3. Claude Code, which executes the Planner prompt, resolves these relative
   paths when writing files. No environment variable, configuration file,
   or command execution is required.
4. The project slug remains a required Planner input, formatted as
   lowercase-hyphen-separated (unchanged).

---

## Docs-Only Constraints — Preserved

The Planner's docs-only rule is unchanged in substance:

- The Planner still produces **only markdown documentation**.
- No commands, scripts, code files, or automation are created or executed.
- The only change is **where** the markdown files are written, not **what**
  they contain or **how** the Planner operates.

Stop conditions are updated to reference the new path:

- Current: "Attempting to write outside `docs/projects/<slug>/`" triggers a
  stop (with `docs/system/outputs/` as a separate exception).
- Proposed: "Attempting to write outside `../<slug>/`" triggers a stop. No
  separate exception is needed — workflow artifacts go to
  `../<slug>/docs/system/outputs/`, which is already within the
  `../<slug>/` boundary.

---

## Gatekeeper Review — No Ambiguity

The Gatekeeper checklist is unaffected in structure. Its "Files in correct
location" check references the authoritative docs for the definition of
"correct." Once the authoritative docs define `../<slug>/` as the correct
location, the Gatekeeper applies the same checklist without ambiguity:

| Checklist item | Current reference | Proposed reference |
|---|---|---|
| Files in correct location | `docs/projects/<slug>/` | `../<slug>/` |
| Naming conventions followed | Unchanged | Unchanged |
| All required documents present | Unchanged | Unchanged |
| Commit points identified | Unchanged | Unchanged |

The Planning Approval criteria in `gateway.md` (line 93) explicitly
references `docs/projects/<slug>/` and must be updated. The generic
`gatekeeper-checklist.md` prompt does not hardcode a path and requires no
change.

---

## Non-Goals

- Does not change the **content or structure** of planning docs (index.md,
  prd.md, roadmap.md, iteration-log.md, phases/).
- Does not change the **content or naming convention** of workflow
  artifacts — the system iterator naming convention
  (YYYY-MM-DD__NN__context__description.md) is unchanged; only the target
  directory changes.
- Does not change the Planner's **role, responsibilities, or workflow**.
- Does not move **automated-builder system artifacts** — issue resolutions,
  verification artifacts, architecture reviews, and other system-level
  outputs remain in `docs/system/outputs/` inside automated-builder.
- Does not introduce **runtime discovery**, environment variables, or
  configuration files.
- Does not **retroactively move** existing planned projects (e.g.,
  `docs/projects/devotional-generator/` remains in place) or existing
  project-specific workflow artifacts already in `docs/system/outputs/`.
- Does not introduce **new governance** beyond expressing the new path
  convention.
- Does not change the **GSD template** usage pattern.
- Does not modify `docs/system/index.md`, `prompts/builder/builder-base.md`,
  `prompts/gatekeeper/gatekeeper-checklist.md`, or `builder.md`.

---

## Authoritative Documents Requiring Updates

Six documents define or reference the current output paths. All six require
updates to cover both the planning docs relocation and the workflow
artifacts relocation.

### 1. `planning.md` (v1.2)

- **Section**: "Project Artifacts Location" (lines 40-76)
- **Change**: Replace `docs/projects/<project-slug>/` with
  `../<project-slug>/` in the MANDATORY rule, example structure, and phase
  path. Add `../<project-slug>/docs/system/outputs/` as the workflow
  artifacts location.
- **Section**: "Long Output Capture" (lines 267-302)
- **Change**: Replace `docs/system/outputs/` with
  `../<slug>/docs/system/outputs/` as the destination for project-specific
  workflow artifacts. Clarify that automated-builder's
  `docs/system/outputs/` is for system-level artifacts only.
- **Version bump**: 1.2 to 1.3

### 2. `docs/system/run-planner.md` (v1.0)

- **Sections affected**:
  - "Output Locations" (lines 59-72): Replace directory tree and path. Add
    `docs/system/outputs/` subtree for workflow artifacts.
  - "Allowed Write Paths" (lines 76-79): Replace
    `docs/projects/<slug>/*.md` and `docs/projects/<slug>/phases/*.md`
    with `../<slug>/*.md`, `../<slug>/phases/*.md`, and
    `../<slug>/docs/system/outputs/*.md`. Remove the separate
    `docs/system/outputs/*.md` exception.
  - "Stop Conditions" (lines 83-84): Update path reference to
    `../<slug>/`. Remove the `docs/system/outputs/` exception.
  - "Long Output Rule" (lines 289-349): Replace `docs/system/outputs/`
    with `../<slug>/docs/system/outputs/` as the destination for
    project-specific workflow artifacts.
  - "Planner Run Checklist" (lines 382-404): Update all
    `docs/projects/<slug>/` references. Update output capture checklist
    items to reference `../<slug>/docs/system/outputs/`.
  - "Iteration Procedure" (line 249): Update "Create project directory"
    path.
  - "Related Documentation" (line 463): Update example project path
    reference.
- **Version bump**: 1.0 to 1.1

### 3. `prompts/planner/run-planner.md` (v1.0)

- **Sections affected**:
  - "Step 3: Create Project Structure" (lines 80-92): Replace directory
    tree. Add `docs/system/outputs/` subdirectory.
  - "Output Path Restrictions" (lines 175-180): Replace allowed and
    prohibited write paths. Replace the separate
    `docs/system/outputs/*.md` allowed path with
    `../<slug>/docs/system/outputs/*.md`.
  - "Step 7: Create Output Artifact" (lines 131-141): Replace
    `docs/system/outputs/` with `../<slug>/docs/system/outputs/` as the
    destination.
  - "Completion Checklist" (lines 211-218): Update path references for
    both planning docs and workflow artifacts.
  - "Example Invocation" (line 233): Update `docs/projects/blog-api/` to
    `../blog-api/` and update the output summary path.
- **Version bump**: 1.0 to 1.1

### 4. `prompts/planner/planner-base.md` (v1.0)

- **Section**: "Output Location" (lines 56-65)
- **Change**: Replace `docs/projects/<project-slug>/` and
  `docs/projects/<project-slug>/phases/` with `../<project-slug>/`,
  `../<project-slug>/phases/`, and
  `../<project-slug>/docs/system/outputs/`.
- **Version bump**: 1.0 to 1.1

### 5. `gateway.md` (v1.0)

- **Section**: "Planning Approval" (line 93)
- **Change**: Replace `docs/projects/<slug>/` with `../<slug>/` in the
  Planning Approval checklist item.
- **Version bump**: 1.0 to 1.1

### 6. `docs/system/outputs/README.md` (v1.1)

- **Section**: "DOES NOT BELONG HERE" (lines 62-65)
- **Change**: Update the project-specific planning paths from
  `docs/projects/<slug>/...` to `../<slug>/...`. Clarify that
  project-specific workflow artifacts belong in
  `../<slug>/docs/system/outputs/`, not in this directory.
- **Section**: "Integration with Workflow" (lines 286-306)
- **Change**: Update "When planning phase completes" and "When phase
  completes" to direct project-specific workflow artifacts to
  `../<slug>/docs/system/outputs/` rather than `docs/system/outputs/`.
- **Version bump**: 1.1 to 1.2

### Documents NOT requiring updates

- `CLAUDE.md` — Does not reference `docs/projects/`. The "Standard Directory
  Structure" lists `docs/` generically. The "File Creation Rules" constrain
  files created inside automated-builder; the Planner writing to the parent
  directory is governed by the Planner-specific authoritative docs above,
  not by CLAUDE.md's general file creation rules.
- `prompts/gatekeeper/gatekeeper-checklist.md` — Uses generic "Files in
  correct location" without hardcoding a path. No change needed.
- `builder.md` — Does not define Planner output locations.
- `docs/system/index.md` — Does not define Planner output locations.
- `prompts/builder/builder-base.md` — Not affected.

---

## Acceptance Criteria

1. All six authoritative documents listed above define `../<slug>/` (relative
   to automated-builder root) as the planning docs root.
2. All six authoritative documents define `../<slug>/docs/system/outputs/`
   as the destination for project-specific workflow artifacts.
3. No authoritative document references `docs/projects/<slug>/` as the
   Planner's output location.
4. No authoritative document directs project-specific workflow artifacts to
   `docs/system/outputs/` inside automated-builder.
5. The docs-only constraint is preserved in all updated documents — the
   Planner still produces only markdown.
6. The Gatekeeper checklist can be applied to artifacts at the new location
   without ambiguity — the Planning Approval criteria in `gateway.md`
   references the new path.
7. Stop conditions in `run-planner.md` and `docs/system/run-planner.md`
   reference the new path boundary (`../<slug>/`) without a separate
   `docs/system/outputs/` exception.
8. Each updated document receives a version bump and changelog entry.
9. No documents beyond the six listed are modified.

---

## Notes / Assumptions

- The parent directory (`..` relative to the automated-builder repo root)
  is assumed to be a stable, writable location. This is consistent with
  the existing filesystem layout where sibling projects already exist.
- The `../<slug>/` convention is intentionally expressed as a relative path
  from the repo root, not an absolute path, to remain portable.
- Existing content in `docs/projects/devotional-generator/` is not moved or
  deleted by this proposal. Migration of existing projects is a separate
  concern and explicitly a non-goal. Existing project-specific workflow
  artifacts already in `docs/system/outputs/` are similarly not moved.
- Automated-builder's `docs/system/outputs/` continues to store
  system-level artifacts (issue resolutions, verification artifacts,
  architecture reviews, etc.). Only project-specific workflow artifacts
  relocate.
- The system iterator naming convention
  (YYYY-MM-DD__NN__context__description.md) is unchanged. When writing
  project-specific workflow artifacts to `../<slug>/docs/system/outputs/`,
  the iterator scans that directory (not `docs/system/outputs/`) to
  determine the next sequence number.
- The `docs/system/outputs/` path within each project
  (`../<slug>/docs/system/outputs/`) mirrors automated-builder's own
  internal structure. This is intentional — it provides a consistent,
  recognizable location for workflow artifacts regardless of which
  project directory you are in.
- The `docs/projects/` directory inside automated-builder may become empty
  after this change. Whether to remove it is not in scope.
