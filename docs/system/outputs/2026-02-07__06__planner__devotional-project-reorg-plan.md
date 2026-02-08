# Devotional Project Directory Review & Reorganization Plan

## Document Information

- **Project**: Devotional Generator (devotional-project-test)
- **Type**: Review + Reorganization Plan
- **Date**: 2026-02-07
- **Executor**: AI: Claude Code (read-only analysis)
- **Reviewer**: Human: Barbara
- **Status**: PENDING HUMAN REVIEW
- **Target Directory**: `~/dev/claude-projects/projects/devotional-project-test`

---

## 1. Current Inventory

### 1.1 Directory Tree

```
devotional-project-test/
├── .DS_Store
└── docs/
    ├── planning/
    │   ├── index.md
    │   ├── iteration-log.md
    │   ├── prd.md
    │   ├── roadmap.md
    │   ├── 2026-02-06__01__planner__devotional-generator-revision.md
    │   ├── 2026-02-07__02__planner__open-questions-q1-q13-final.md
    │   ├── audits/
    │   │   ├── 2026-02-07__03__audit__q1-quote-sourcing.md
    │   │   └── 2026-02-07__05__audit__q1-quote-sourcing.md
    │   └── phases/
    │       ├── 001-data-model-inputs.md        (current)
    │       ├── 001-project-scaffold.md         (superseded)
    │       ├── 002-template-system.md          (current)
    │       ├── 003-content-library.md          (superseded)
    │       ├── 003-kdp-pdf-export.md           (current)
    │       ├── 004-validation-preview.md       (current)
    │       └── 005-export-distribution.md      (superseded)
    └── provenance/
        └── README.md
```

**Total files**: 14 markdown files + 1 provenance README + 1 .DS_Store
**Git status**: NOT a git repository

### 1.2 File Summary

| File | Purpose | Version | Status |
|------|---------|---------|--------|
| `docs/planning/index.md` | Project navigation hub, key specs | v3.0 | Current |
| `docs/planning/prd.md` | Product Requirements Document | v3.0 | Current |
| `docs/planning/roadmap.md` | 4-phase implementation roadmap | v3.0 | Current |
| `docs/planning/iteration-log.md` | Decision history (Iter 0–3) | v3.0 | Current |
| `docs/planning/2026-02-06__01__planner__devotional-generator-revision.md` | Planner Iteration 1 output | — | Session artifact |
| `docs/planning/2026-02-07__02__planner__open-questions-q1-q13-final.md` | Planner Iteration 3 output (Q1–Q13 final) | — | Session artifact |
| `docs/planning/audits/2026-02-07__03__audit__q1-quote-sourcing.md` | Q1 audit: consolidated findings | — | Audit |
| `docs/planning/audits/2026-02-07__05__audit__q1-quote-sourcing.md` | Q1 audit: recommendations applied | — | Audit |
| `docs/planning/phases/001-data-model-inputs.md` | Phase 001 plan (current 4-phase roadmap) | — | Current |
| `docs/planning/phases/001-project-scaffold.md` | Phase 001 plan (original 5-phase roadmap) | — | **Superseded** |
| `docs/planning/phases/002-template-system.md` | Phase 002 plan | — | Current |
| `docs/planning/phases/003-content-library.md` | Phase 003 plan (original 5-phase roadmap) | — | **Superseded** |
| `docs/planning/phases/003-kdp-pdf-export.md` | Phase 003 plan (current 4-phase roadmap) | — | Current |
| `docs/planning/phases/004-validation-preview.md` | Phase 004 plan | — | Current |
| `docs/planning/phases/005-export-distribution.md` | Phase 005 plan (original 5-phase roadmap) | — | **Superseded** |
| `docs/provenance/README.md` | Traces origin to automated-builder repo | — | Current |

### 1.3 Provenance

Per `docs/provenance/README.md`, all files were copied from:
- **Source repo**: `~/dev/claude-projects/projects/automated-builder`
- **Source locations**:
  - `docs/projects/devotional-generator/` (planning docs, phases)
  - `docs/system/outputs/` (selected devotional-related artifacts)
- Originals remain in automated-builder for system-level traceability.

### 1.4 Issues Found

#### Critical: Not a git repo
The directory has no `.git` — no version history exists. `git mv` cannot be used until `git init` is run.

#### Superseded files mixed with current files
Three phase plans from the original 5-phase roadmap (superseded in Iteration 1) sit alongside current 4-phase plans with no visual distinction:
- `001-project-scaffold.md` — superseded by `001-data-model-inputs.md`
- `003-content-library.md` — superseded by `003-kdp-pdf-export.md`
- `005-export-distribution.md` — entire phase removed from roadmap

#### Session artifacts mixed into planning directory
Two files use the automated-builder's `__NN__` output naming convention and were placed directly in `docs/planning/`:
- `2026-02-06__01__planner__devotional-generator-revision.md`
- `2026-02-07__02__planner__open-questions-q1-q13-final.md`

These are planner session outputs (decision records), not planning documents. They are reference artifacts that other docs cite.

#### Audits nested under planning
`docs/planning/audits/` positions audits as a subcategory of planning. Audits are a distinct quality-assurance activity — they review planning/execution, they don't belong inside the thing they review.

#### Broken internal references
Multiple files reference automated-builder paths that don't exist in this repo:
- `../../system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` (in index.md line 95)
- `docs/system/ai.md` (referenced in prd.md, roadmap.md, phase plans)
- `docs/system/outputs/...` (referenced in iteration-log.md, prd.md, roadmap.md)

These references were broken at copy time, not by this review.

#### Everything lives under docs/
The entire repository is inside `docs/`. There is no top-level README, no CLAUDE.md, and no separation between document types at the top level. This makes the directory opaque to new contributors.

#### No duplicate files detected
All files are unique — no content duplicates found. The two Q1 audit files (`__03__` and `__05__`) serve different purposes: `__03__` is findings, `__05__` is the application record.

---

## 2. Proposed Target Structure

### 2.1 Directory Layout

```
devotional-project-test/
├── README.md                       # (NEW) Project overview + directory guide
├── PROVENANCE.md                   # (MOVED) Traceability to automated-builder
├── docs/                           # Core project documentation
│   ├── index.md                    #   Navigation hub
│   ├── prd.md                      #   Product Requirements Document
│   ├── roadmap.md                  #   Implementation roadmap
│   └── iteration-log.md            #   Decision/iteration history
├── plans/                          # Phase implementation plans
│   ├── 001-data-model-inputs.md
│   ├── 002-template-system.md
│   ├── 003-kdp-pdf-export.md
│   ├── 004-validation-preview.md
│   └── superseded/                 # Clearly separated old plans
│       ├── 001-project-scaffold.md
│       ├── 003-content-library.md
│       └── 005-export-distribution.md
├── audits/                         # Quality assurance reviews
│   ├── 2026-02-07__03__audit__q1-quote-sourcing.md
│   └── 2026-02-07__05__audit__q1-quote-sourcing.md
└── artifacts/                      # Session outputs (planner decisions)
    ├── 2026-02-06__01__planner__devotional-generator-revision.md
    └── 2026-02-07__02__planner__open-questions-q1-q13-final.md
```

### 2.2 Rationale

| Directory | Why | What goes here |
|-----------|-----|----------------|
| `docs/` | Core project documentation that contributors read first. Stable paths for the "what" of the project. | PRD, roadmap, index, iteration log |
| `plans/` | The "how we're going to build it" documents. Separate from "what" (docs) to avoid conflation. | Phase plans (current and superseded) |
| `plans/superseded/` | Superseded plans are historical record, not active guidance. Separating them prevents confusion about which plans are current. | Old phase plans from the 5-phase roadmap |
| `audits/` | Quality reviews are distinct from planning — they assess planning/execution, they don't belong inside it. | Q1 quote sourcing audit and its implementation record |
| `artifacts/` | Planner session outputs that record decisions. Referenced by other docs but not themselves planning documents. Preserves `__NN__` naming for traceability to automated-builder. | Planner iteration outputs |
| `PROVENANCE.md` | Top-level visibility for traceability. A contributor should see this immediately, not hunt for it inside `docs/provenance/`. | Origin info, source paths |
| `README.md` | Every project repo needs a top-level README. Currently absent. | Project overview, directory guide, status |

### 2.3 Design Principles Applied

1. **Separate concerns**: docs (what) / plans (how) / audits (review) / artifacts (decisions)
2. **Preserve provenance**: All `__NN__` filenames kept intact for traceability to automated-builder
3. **No deep nesting**: Maximum depth is 2 levels (e.g., `plans/superseded/file.md`)
4. **Stable paths**: Top-level directories are general-purpose and won't need renaming as project evolves
5. **Superseded content isolated**: Not deleted (historical value) but clearly separated from active docs
6. **No builder governance imported**: `docs/system/ai.md` and other automated-builder system docs are NOT copied in — references to them are noted as broken (see Section 4)

---

## 3. File-by-File Mapping

### 3.1 Files That Move

| # | Current Location | New Location | Reason |
|---|-----------------|--------------|--------|
| 1 | `docs/planning/index.md` | `docs/index.md` | Core doc, not a "planning" subcategory |
| 2 | `docs/planning/prd.md` | `docs/prd.md` | Core doc |
| 3 | `docs/planning/roadmap.md` | `docs/roadmap.md` | Core doc |
| 4 | `docs/planning/iteration-log.md` | `docs/iteration-log.md` | Core doc |
| 5 | `docs/planning/phases/001-data-model-inputs.md` | `plans/001-data-model-inputs.md` | Active phase plan |
| 6 | `docs/planning/phases/002-template-system.md` | `plans/002-template-system.md` | Active phase plan |
| 7 | `docs/planning/phases/003-kdp-pdf-export.md` | `plans/003-kdp-pdf-export.md` | Active phase plan |
| 8 | `docs/planning/phases/004-validation-preview.md` | `plans/004-validation-preview.md` | Active phase plan |
| 9 | `docs/planning/phases/001-project-scaffold.md` | `plans/superseded/001-project-scaffold.md` | Superseded |
| 10 | `docs/planning/phases/003-content-library.md` | `plans/superseded/003-content-library.md` | Superseded |
| 11 | `docs/planning/phases/005-export-distribution.md` | `plans/superseded/005-export-distribution.md` | Superseded |
| 12 | `docs/planning/audits/2026-02-07__03__audit__q1-quote-sourcing.md` | `audits/2026-02-07__03__audit__q1-quote-sourcing.md` | Audit (own top-level) |
| 13 | `docs/planning/audits/2026-02-07__05__audit__q1-quote-sourcing.md` | `audits/2026-02-07__05__audit__q1-quote-sourcing.md` | Audit (own top-level) |
| 14 | `docs/planning/2026-02-06__01__planner__devotional-generator-revision.md` | `artifacts/2026-02-06__01__planner__devotional-generator-revision.md` | Session artifact |
| 15 | `docs/planning/2026-02-07__02__planner__open-questions-q1-q13-final.md` | `artifacts/2026-02-07__02__planner__open-questions-q1-q13-final.md` | Session artifact |
| 16 | `docs/provenance/README.md` | `PROVENANCE.md` | Elevated to root for visibility |

### 3.2 Files That Stay (Remain or Are Created)

| File | Action | Notes |
|------|--------|-------|
| `README.md` | **CREATE** | New top-level project readme (Phase 2 scope) |
| `.DS_Store` | **IGNORE** | macOS metadata, should be .gitignored |

### 3.3 Directories Removed After Migration

After all files are moved, these directories will be empty and can be deleted:
- `docs/planning/phases/`
- `docs/planning/audits/`
- `docs/planning/`
- `docs/provenance/`

---

## 4. Known Broken References (Pre-existing)

These references were already broken when files were copied from automated-builder. They are **out of scope** for this reorg but documented for a follow-up pass:

| File | Broken Reference | What It Points To |
|------|-----------------|-------------------|
| `index.md` (line 95) | `../../system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` | automated-builder system output |
| `prd.md` (line 295) | `docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` | automated-builder system output |
| `prd.md` (line 386) | `docs/system/ai.md` | automated-builder governance doc |
| `roadmap.md` (line 217) | `docs/system/ai.md` | automated-builder governance doc |
| `roadmap.md` (line 316) | `docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` | automated-builder system output |
| `iteration-log.md` (line 78) | `docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` | automated-builder system output |
| Multiple phase plans | `docs/system/ai.md` | automated-builder governance doc |

**Recommended follow-up**: After reorg, run a separate pass to update these references to point to the local `artifacts/` directory where applicable, and add a note in PROVENANCE.md about `docs/system/ai.md` being an automated-builder-only document.

---

## 5. Migration Plan

### 5.1 Pre-requisite: Initialize Git

Since the directory is not a git repo, `git init` must run first:

```bash
cd ~/dev/claude-projects/projects/devotional-project-test
git init
git add -A
git commit -m "Initial commit: imported planning docs from automated-builder

Source: ~/dev/claude-projects/projects/automated-builder
Locations: docs/projects/devotional-generator/, docs/system/outputs/ (selected)
See docs/provenance/README.md for details."
```

### 5.2 Move Commands

All commands assume working directory is the repo root (`devotional-project-test/`).

#### Commit 1: Create target directories and move core docs

```bash
# Create target directories
mkdir -p plans/superseded
mkdir -p audits
mkdir -p artifacts

# Move core docs up from docs/planning/ to docs/
git mv docs/planning/index.md docs/index.md
git mv docs/planning/prd.md docs/prd.md
git mv docs/planning/roadmap.md docs/roadmap.md
git mv docs/planning/iteration-log.md docs/iteration-log.md
```

#### Commit 2: Move active phase plans to plans/

```bash
git mv docs/planning/phases/001-data-model-inputs.md plans/001-data-model-inputs.md
git mv docs/planning/phases/002-template-system.md plans/002-template-system.md
git mv docs/planning/phases/003-kdp-pdf-export.md plans/003-kdp-pdf-export.md
git mv docs/planning/phases/004-validation-preview.md plans/004-validation-preview.md
```

#### Commit 3: Move superseded phase plans to plans/superseded/

```bash
git mv docs/planning/phases/001-project-scaffold.md plans/superseded/001-project-scaffold.md
git mv docs/planning/phases/003-content-library.md plans/superseded/003-content-library.md
git mv docs/planning/phases/005-export-distribution.md plans/superseded/005-export-distribution.md
```

#### Commit 4: Move audits and session artifacts

```bash
git mv docs/planning/audits/2026-02-07__03__audit__q1-quote-sourcing.md audits/2026-02-07__03__audit__q1-quote-sourcing.md
git mv docs/planning/audits/2026-02-07__05__audit__q1-quote-sourcing.md audits/2026-02-07__05__audit__q1-quote-sourcing.md
git mv docs/planning/2026-02-06__01__planner__devotional-generator-revision.md artifacts/2026-02-06__01__planner__devotional-generator-revision.md
git mv docs/planning/2026-02-07__02__planner__open-questions-q1-q13-final.md artifacts/2026-02-07__02__planner__open-questions-q1-q13-final.md
```

#### Commit 5: Elevate provenance, add README, clean up empty dirs

```bash
# Move provenance to root
git mv docs/provenance/README.md PROVENANCE.md

# Remove now-empty directories
rmdir docs/planning/phases
rmdir docs/planning/audits
rmdir docs/planning
rmdir docs/provenance

# Create .gitignore
echo ".DS_Store" > .gitignore

# README.md will be created (content below)
```

### 5.3 Commit Plan

| # | Message | Files Affected | Category |
|---|---------|---------------|----------|
| 0 | `Initial commit: imported planning docs from automated-builder` | All existing files | Bootstrap |
| 1 | `Restructure: move core docs from docs/planning/ to docs/` | 4 files moved | docs |
| 2 | `Restructure: move active phase plans to plans/` | 4 files moved | plans |
| 3 | `Restructure: move superseded phase plans to plans/superseded/` | 3 files moved | plans |
| 4 | `Restructure: move audits and artifacts to top-level directories` | 4 files moved | audits + artifacts |
| 5 | `Restructure: elevate provenance, add README and .gitignore` | 3 files (1 moved, 2 created) | project metadata |

**Total**: 6 commits (1 bootstrap + 5 reorg)

### 5.4 README.md Content (to be created in Commit 5)

```markdown
# Devotional Generator

Weekly devotional content generator for Amazon KDP self-publishing.

## Status

- **Phase**: Planning (all open questions resolved)
- **Version**: 3.0
- **Last Updated**: 2026-02-07

## Directory Guide

| Directory | Contents |
|-----------|----------|
| `docs/` | Core project documentation (PRD, roadmap, iteration log) |
| `plans/` | Phase implementation plans (001–004) |
| `plans/superseded/` | Archived plans from earlier iterations |
| `audits/` | Quality assurance reviews |
| `artifacts/` | Planner session outputs and decision records |

## Quick Start

- Start with [docs/index.md](docs/index.md) for project overview
- See [docs/prd.md](docs/prd.md) for requirements
- See [docs/roadmap.md](docs/roadmap.md) for implementation phases

## Provenance

These documents originated in the automated-builder repository.
See [PROVENANCE.md](PROVENANCE.md) for details.
```

### 5.5 Rollback Strategy

Since all moves are done via `git mv` with individual commits:

**Full rollback** (revert all reorg):
```bash
git log --oneline  # find the initial commit hash
git reset --hard <initial-commit-hash>
```

**Partial rollback** (revert specific commits):
```bash
git revert <commit-hash>  # revert a single commit
```

**Pre-reorg safety**: Before starting Phase 2, optionally create a branch:
```bash
git checkout -b pre-reorg-backup
git checkout main
```

---

## 6. Post-Reorg Follow-Up Tasks (Out of Scope)

These are identified but NOT part of Phase 2:

1. **Fix broken internal references** — Update links to automated-builder paths (see Section 4)
2. **Update PROVENANCE.md** — Expand to list each file and its source path
3. **Consider CLAUDE.md** — If Claude Code sessions will run in this repo, a project-specific CLAUDE.md may be needed

---

## End of Artifact

This review was performed as read-only analysis. No files in devotional-project-test were modified. The plan above requires explicit human authorization before any Phase 2 actions are taken.
