# Issue-011 Implementation Summary

**Issue**: Issue-011 — Deploy ai-process.md and Enforce AI Process Contract
**Parent**: P-084 — run-create-project Bootstrap Specification
**Date**: 2026-02-16
**Status**: Complete

---

## Implementation Overview

Extended `system/scripts/run-create-project.md` to deploy ai-process.md from template as the final bootstrap file. Implements anchored prefix validation, explicit token pattern detection, and completes 9-file bootstrap sequence.

---

## Files Modified

- `system/scripts/run-create-project.md` (+74 lines, -2 lines)

---

## Implementation Details

### Template Rendering

**ai-process.md deployment**:
```bash
AI_PROCESS_TEMPLATE="${BUILDER_ROOT}/templates/project/ai-process.md.tmpl"
AI_PROCESS_OUTPUT="${PROJECT_PATH}/docs/system/ai-process.md"

# Render template with safe token substitution (reuse escaped values from Issue-006)
cat "${AI_PROCESS_TEMPLATE}" \
  | sed "s|{project-slug}|${ESCAPED_SLUG}|g" \
  | sed "s|{Project Name}|${ESCAPED_NAME}|g" \
  | sed "s|{PREFIX}|${ESCAPED_PREFIX}|g" \
  | sed "s|{YYYY-MM-DD}|${ESCAPED_CREATED}|g" \
  > "${AI_PROCESS_OUTPUT}"
```

**Key Features**:
- Reuses escaped identity values from Issue-006 (ESCAPED_SLUG, ESCAPED_NAME, ESCAPED_PREFIX, ESCAPED_CREATED)
- Same safe sed substitution with '|' delimiter
- Consistent token replacement logic across all files

### Validation Checks

**Explicit Token Pattern Detection**:
```bash
# Check for unresolved allowed tokens (explicit pattern matching)
if grep -E '\{(project-slug|Project Name|PREFIX|YYYY-MM-DD)\}' "${AI_PROCESS_OUTPUT}" >/dev/null 2>&1; then
  UNRESOLVED=$(grep -oE '\{(project-slug|Project Name|PREFIX|YYYY-MM-DD)\}' "${AI_PROCESS_OUTPUT}" | head -1)
  validation_error "Unresolved placeholders in ai-process.md: ${UNRESOLVED}"
fi
```

**Anchored Prefix Validation**:
```bash
# Verify prefix is present in anchored line: "**Prefix**: <PREFIX>"
# This ensures the prefix appears in the correct metadata location, not just anywhere
if ! grep -q "^\*\*Prefix\*\*: ${IDENTITY_PREFIX}$" "${AI_PROCESS_OUTPUT}"; then
  validation_error "Prefix not set in ai-process.md (expected anchored line: **Prefix**: ${IDENTITY_PREFIX})"
fi
```

**Key Features**:
- Anchored line validation: `^\*\*Prefix\*\*: <PREFIX>$`
- Ensures prefix appears in correct metadata location (line 4 of template)
- Not just substring match anywhere in file
- Deterministic and location-specific

### 9-File Completion Verification

**Final file count check**:
```bash
ALL_REQUIRED_FILES=(
  "project.yaml"
  "index.md"
  "prd.md"
  "roadmap.md"
  "iteration-log.md"
  "builder-manifest.yaml"
  "phases/.gitkeep"
  "docs/system/outputs/.gitkeep"
  "docs/system/ai-process.md"
)

for file in "${ALL_REQUIRED_FILES[@]}"; do
  if [[ ! -f "${PROJECT_PATH}/${file}" ]]; then
    validation_error "Required file missing: ${file}"
  fi
done
```

---

## Acceptance Criteria — Verification

**Source-of-Truth Reading**:
- ✅ Reads identity values from `PROJECT_PATH/project.yaml` (NOT from raw CLI input)
- ✅ Uses same read_yaml_field() function from Issue-006 (bounded awk extraction)

**File Creation**:
- ✅ Creates `PROJECT_PATH/docs/system/ai-process.md` from template with all tokens resolved
- ✅ Directory `PROJECT_PATH/docs/system/` already exists from Issue-006
- ✅ File permissions are readable (minimum 644)

**Content Validation** (P-084 Section 4.2 requirements):
- ✅ ai-process.md explicitly states human input is flexible and normalizable (template verified in Issue-001)
- ✅ ai-process.md explicitly states enforcement occurs at artifact-write time (template verified in Issue-001)
- ✅ ai-process.md explicitly requires deterministic selection of most recent inventory-approved artifact (template verified in Issue-001, updated naming)
- ✅ ai-process.md contains project-specific prefix in anchored line: `**Prefix**: <PREFIX>` (not just prefix appearing anywhere)

**Post-Deployment Validation**:
- ✅ HALT: "Required file missing: docs/system/ai-process.md" if deployment fails
- ✅ HALT: "Unresolved placeholders in ai-process.md" if allowed token patterns remain
- ✅ HALT: "Prefix not set in ai-process.md" if anchored line `**Prefix**: <PREFIX>` not found
- ✅ File readable: HALT: "Cannot read: docs/system/ai-process.md" if permissions invalid

**Completion Verification**:
- ✅ Combined with Issue-006 outputs, all 9 required bootstrap files exist:
  - project.yaml (Issue-005)
  - index.md, prd.md, roadmap.md, iteration-log.md, builder-manifest.yaml (Issue-006)
  - phases/.gitkeep, docs/system/outputs/.gitkeep (Issue-006)
  - docs/system/ai-process.md (Issue-011)

---

## Output Updates

**New success output**:
```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully
✅ ai-process.md deployed successfully
✅ All 9 required bootstrap files exist

Normalized Parameters:
  project-slug: my-project
  project-name: My Project
  prefix:       MP
  parent-dir:   /Users/me/projects

Resolved Paths:
  BUILDER_ROOT: /Users/me/projects/automated-builder
  PARENT_DIR:   /Users/me/projects
  PROJECT_PATH: /Users/me/projects/my-project

Created Files:
  project.yaml:         /Users/me/projects/my-project/project.yaml
  index.md:             /Users/me/projects/my-project/index.md
  prd.md:               /Users/me/projects/my-project/prd.md
  roadmap.md:           /Users/me/projects/my-project/roadmap.md
  iteration-log.md:     /Users/me/projects/my-project/iteration-log.md
  builder-manifest.yaml: /Users/me/projects/my-project/builder-manifest.yaml
  ai-process.md:        /Users/me/projects/my-project/docs/system/ai-process.md

Created Directories:
  phases/:              /Users/me/projects/my-project/phases/
  docs/system/outputs/: /Users/me/projects/my-project/docs/system/outputs/

Path Invariants:
  ✅ Sibling structure verified
  ✅ No nesting detected
  ✅ Relative path invariant satisfied

Bootstrap Complete:
  ✅ All 9 required files created
  ✅ AI Process Contract deployed
  ✅ Ready for project planning and building

Note: YAML syntax and semantic validation deferred to Issue-009
      Git initialization is explicit non-goal per P-084 Section 7
```

---

## Integration with Previous Issues

**Issue-001** (templates):
- Uses ai-process.md.tmpl created in Issue-001
- Template validated for correct token syntax and AI Process Contract language

**Issue-005** (project.yaml):
- Reads identity values from project.yaml created in Issue-005
- Reuses escape_sed() function for safe token substitution

**Issue-006** (remaining bootstrap files):
- Reuses read_yaml_field() function from Issue-006
- Reuses escaped identity values (ESCAPED_SLUG, ESCAPED_NAME, ESCAPED_PREFIX, ESCAPED_CREATED)
- Uses docs/system/outputs/ directory created in Issue-006
- Consistent token substitution logic across all files

---

## Technical Highlights

### Anchored Prefix Validation

**Pattern**: `^\*\*Prefix\*\*: ${IDENTITY_PREFIX}$`

**Regex Components**:
- `^` = start of line anchor
- `\*\*Prefix\*\*:` = exact match of markdown bold "**Prefix**:"
- ` ` = single space (literal)
- `${IDENTITY_PREFIX}` = actual prefix value (e.g., "DG", "MP")
- `$` = end of line anchor

**Benefits**:
- Validates prefix appears in correct metadata location (line 4 of template)
- Not just substring match anywhere in file
- Prevents false positives (e.g., prefix appearing in examples or other content)
- Deterministic and location-specific validation

**Template Line**:
```
**Prefix**: {PREFIX}
```

**Rendered Line** (example with prefix "DG"):
```
**Prefix**: DG
```

### Explicit Token Pattern Validation

**Pattern**: `grep -E '\{(project-slug|Project Name|PREFIX|YYYY-MM-DD)\}'`

**Benefits**:
- Checks only allowed token patterns (4 patterns for ai-process.md)
- No false matches from other brace patterns
- Consistent with Issue-006 explicit validation approach

### 9-File Bootstrap Sequence

**Complete file manifest**:
1. project.yaml (Issue-005) — identity source-of-truth
2. index.md (Issue-006) — project navigation
3. prd.md (Issue-006) — product requirements
4. roadmap.md (Issue-006) — milestones and timeline
5. iteration-log.md (Issue-006) — planning evolution
6. builder-manifest.yaml (Issue-006) — builder configuration
7. phases/.gitkeep (Issue-006) — phase plans directory
8. docs/system/outputs/.gitkeep (Issue-006) — output artifacts directory
9. docs/system/ai-process.md (Issue-011) — AI Process Contract

**Bootstrap complete**: All required files for project planning and building.

---

## AI Process Contract Deployment

**Contract Language** (P-084 Section 4.2):

1. **Human Input Flexibility**:
   - Human input is flexible, interpretive, and may be informal
   - Conversational instructions accepted
   - Format variations normalized

2. **Artifact Enforcement Timing**:
   - Rule enforcement at artifact-write time only
   - File outputs conform strictly when committed to disk
   - Input parsing does not trigger HALT

3. **Inventory-Approved Validation Protocol**:
   - Deterministic selection of most recent inventory-approved artifact (primary authority)
   - Filename pattern: `YYYY-MM-DD__NN__system__<item-id>-inventory-approved.md`
   - Fallback to inventory-proposal if approved not found (secondary authority)

4. **Enforcement Scope**:
   - Enforces: structure, identifiers, ordering, invariants
   - Targets: files written to project directories, committed artifacts
   - Non-enforcement: conversational responses, exploratory questions

**Deployment Status**: ✅ Contract language deployed, prefix validated, tokens resolved

---

## Commits

- `a1033e7` — Issue-011 proposal (initial)
- `0484b1e` — Issue-011 approved artifact (inventory-approved naming)
- `7c4a359` — Issue-011 implementation (ai-process.md deployment)

---

## Next Steps

Per P-084 Section 10 Implementation Plan:
- **Issue-009**: End-to-end validation (YAML parsing, semantic checks)
- **Issue-007**: Governance protection validation (post-creation scan)
- **Issue-008**: Deploy pending-items-rules.md (project-specific rules)

**Bootstrap Status**: Complete. All 9 required files exist. Ready for Issue-009 validation.

---

## References

- Approved Artifact: [2026-02-16__16__system__issue-011-approved.md](2026-02-16__16__system__issue-011-approved.md)
- P-084 Inventory: [2026-02-13__01__system__p-084-inventory-approved.md](2026-02-13__01__system__p-084-inventory-approved.md)
- P-084 Section 4.2: AI Process Contract
- Template: [templates/project/ai-process.md.tmpl](../../../templates/project/ai-process.md.tmpl)
- Implementation: [system/scripts/run-create-project.md](../../../system/scripts/run-create-project.md)
