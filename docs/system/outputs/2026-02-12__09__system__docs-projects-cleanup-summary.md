# System Update — docs/projects References Cleanup

**Date**: 2026-02-12
**Context**: Post-P-083 cleanup of `docs/projects/` references
**Scope**: Documentation updates following relocation of project planning outputs

---

## Context

Following P-083 (relocation of Planner output from `docs/projects/<slug>/` to
`../<slug>/`), and the removal of the devotional-generator project directory,
all references to `docs/projects/` in documentation needed to be updated to:

1. Reflect the new `../<slug>/` output location per P-083
2. Remove broken links to the deleted devotional-generator project
3. Update rules and policies about project location

---

## Files Updated

### 1. README.md

**Changes**:
- Removed directory structure showing `docs/projects/` (lines 63-72)
- Removed entire "Current Projects" section with devotional-generator references (lines 82-106)
- Added new "Project Planning Output Location" section explaining P-083 structure
- Updated "For Planners" workflow: `docs/projects/<project-slug>/` → `../<project-slug>/`
- Updated "Mandatory Constraints": Planning stage location updated to `../<slug>/`
- Updated "Getting Started" section: removed devotional-generator references, updated paths
- Removed "Status: Devotional Generator" section

**Rules Updated**:
- Project directory creation path
- Planning output location constraint
- Getting started instructions

---

### 2. docs/system/index.md

**Changes**:
- Line 53: Planner output location: `docs/projects/<slug>/` → `../<slug>/` (per P-083)
- Line 111: Projects location rule: `docs/projects/<slug>/` → `../<slug>/` (per P-083)
- Lines 168-183: Complete "Project Artifacts" section rewritten with new structure
- Line 232: Workflow instruction: `docs/projects/<slug>/` → `../<slug>/`
- Line 344: Removed devotional-generator example link
- Line 352: mkdir command: `docs/projects/<your-project-slug>` → `../<your-project-slug>`
- Line 371: Review instruction: `docs/projects/<slug>/index.md` → `../<slug>/index.md`
- Line 418: Replaced devotional-generator example with run-planner.md guide

**Rules Updated**:
- Planner output constraint
- Projects location rule
- Project artifacts structure
- Workflow directory creation
- Review starting point
- Example references

---

### 3. docs/system/README.md

**Changes**:
- Lines 83-94: Complete "Project Documentation" section rewritten
  - Location: `docs/projects/<project-slug>/` → `../<project-slug>/`
  - Removed devotional-generator examples
  - Added structure diagram showing parent directory layout
  - Added note about P-083 relocation
- Line 121: "Do NOT add" rule: `docs/projects/<slug>/` → `../<slug>/`

**Rules Updated**:
- Project documentation location
- When NOT to add to docs/system (project-specific planning location)

---

### 4. docs/system/git.md

**Changes**:
- Line 25: Docs-only commit scope: `docs/projects/<slug>/` → `../<slug>/` (per P-083)

**Rules Updated**:
- Planning documents scope in docs-only commits

---

### 5. gateway.md

**Changes**:
- No changes required (only contains version history documenting P-083)

---

### 6. prompts/gatekeeper/gatekeeper-checklist.md

**Changes**:
- Line 232: REVISE example: `docs/projects/X/phases/003-X.md` → `../X/phases/003-X.md`
- Line 249: REJECT example: `prompts/ instead of docs/projects/` → `prompts/ instead of ../<slug>/`

**Rules Updated**:
- Example file paths in decision templates

---

## Rules and Policies Identified

### Core Location Rules (Updated)

1. **Project Creation Directory**:
   - Before: `docs/projects/<project-slug>/`
   - After: `../<project-slug>/` (parent directory)
   - Files: README.md, docs/system/index.md, docs/system/README.md

2. **Planning Output Location Constraint**:
   - Before: `docs/projects/<slug>/`
   - After: `../<slug>/`
   - Files: README.md, docs/system/index.md

3. **Docs-Only Commit Scope**:
   - Before: Planning documents (`docs/projects/<slug>/`)
   - After: Planning documents (`../<slug>/`, per P-083)
   - File: docs/system/git.md

4. **Project Documentation Location**:
   - Before: `docs/projects/<project-slug>/`
   - After: `../<project-slug>/`
   - File: docs/system/README.md

5. **Example References**:
   - Before: Multiple references to devotional-generator in `docs/projects/`
   - After: References to planning guide (docs/system/run-planner.md)
   - Files: README.md, docs/system/index.md

---

## Annotations for Moved Content

**Devotional Generator Project**:
- **Previous Location**: `docs/projects/devotional-generator/`
- **Status**: Moved to individual project directory per P-083
- **Files Deleted**: 11 files (index.md, prd.md, roadmap.md, iteration-log.md, 7 phase plans)
- **Commit**: 823c585 "Reason cleaned out old projects"
- **Note**: Planning content now lives in `../<slug>/` alongside automated-builder

**docs/projects/ Directory**:
- **Previous Purpose**: Container for project planning artifacts inside automated-builder
- **Current Status**: Empty (may be removed)
- **Rationale**: Per P-083, project planning outputs should live in parent directory alongside automated-builder, not inside it

---

## Historical Outputs

**Decision**: Historical outputs in `docs/system/outputs/` were NOT updated.

**Rationale**:
- Historical records should preserve original context
- These documents capture the state of the system at the time they were created
- Updating them would lose historical accuracy
- 25+ output files contain `docs/projects/` references, including P-083 proposal itself

---

## Verification

### Grep Results After Update

Ran `grep -r "docs/projects" .` to verify:
- ✅ All authoritative documents updated
- ✅ All rules and policies updated
- ✅ All broken links removed
- ✅ Historical outputs preserved (expected)

### Files Still Containing "docs/projects"

**Expected (Historical)**:
- docs/system/outputs/*.md (25+ files) - Historical records
- gateway.md (version history entry documenting P-083)

**None (Authoritative)**:
- All current rules and policies now reference `../<slug>/` per P-083

---

## Impact Summary

### Breaking Changes
- None (P-083 already implemented, this is documentation cleanup)

### Non-Breaking Changes
- Documentation now consistent with P-083 implementation
- Broken devotional-generator links removed
- Rules and policies clarified

### Future Considerations
- May remove empty `docs/projects/` directory if confirmed unused
- Any new documentation should reference `../<slug>/` per P-083
- Historical devotional-generator references in outputs remain for context

---

## Related Documents

- [P-083 Proposal](2026-02-12__04__system__p-083-planner-output-root-approved.md) - Original relocation proposal
- [P-083 Implementation](2026-02-12__06__system__p-083-implementation-summary.md) - Implementation summary
- [P-083 Verification](2026-02-12__07__system__p-083-verification.md) - Verification results
- [docs/system/run-planner.md](../run-planner.md) - Updated planning guide (v1.1)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-12 | Initial cleanup summary |
