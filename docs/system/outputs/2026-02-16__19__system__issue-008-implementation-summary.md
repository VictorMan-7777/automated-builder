# Issue-008 Implementation Summary

**Issue**: Issue-008 — Deploy Project Rules Pack Template
**Parent**: P-084 — run-create-project Bootstrap Specification
**Date**: 2026-02-16
**Status**: Complete

---

## Implementation Overview

Extended `scripts/run-create-project` to deploy pending-items-rules.md from template as project-specific namespace mapping documentation. Implements dependency-scoped verification, explicit 3-token substitution, and outputs/ directory existence check.

---

## Files Modified

- `scripts/run-create-project` (+67 lines)

---

## Implementation Details

### Template Rendering

**pending-items-rules.md deployment**:
```bash
PENDING_ITEMS_TEMPLATE="${BUILDER_ROOT}/templates/project/pending-items-rules.md.tmpl"
PENDING_ITEMS_OUTPUT="${PROJECT_PATH}/docs/system/pending-items-rules.md"

# Verify docs/system/outputs/ directory exists (created in Issue-006)
if [[ ! -d "${PROJECT_PATH}/docs/system/outputs" ]]; then
  validation_error "docs/system/outputs/ directory missing (should have been created in Issue-006)"
fi

# Render template with safe token substitution (reuse escaped values from Issue-006)
cat "${PENDING_ITEMS_TEMPLATE}" \
  | sed "s|{project-slug}|${ESCAPED_SLUG}|g" \
  | sed "s|{Project Name}|${ESCAPED_NAME}|g" \
  | sed "s|{PREFIX}|${ESCAPED_PREFIX}|g" \
  > "${PENDING_ITEMS_OUTPUT}"
```

**Key Features**:
- Reuses escaped identity values from Issue-006 (ESCAPED_SLUG, ESCAPED_NAME, ESCAPED_PREFIX)
- Only 3 tokens for this template (no date token)
- Same safe sed substitution with '|' delimiter
- Verifies outputs/ subdirectory exists (confirms docs/system/ parent exists)

### Validation Checks

**Explicit Token Pattern Detection**:
```bash
# Check for unresolved allowed tokens (explicit pattern matching)
# Only 3 tokens for this template: project-slug, Project Name, PREFIX
if grep -E '\{(project-slug|Project Name|PREFIX)\}' "${PENDING_ITEMS_OUTPUT}" >/dev/null 2>&1; then
  UNRESOLVED=$(grep -oE '\{(project-slug|Project Name|PREFIX)\}' "${PENDING_ITEMS_OUTPUT}" | head -1)
  validation_error "Unresolved token in pending-items-rules.md: ${UNRESOLVED}"
fi
```

**Key Features**:
- Checks only 3 allowed token patterns (not 4 like ai-process.md)
- No false matches from other brace patterns
- Consistent with Issue-006/011 explicit validation approach

### Dependency Verification

**Dependency-scoped verification**:
```bash
# Verify required artifacts from dependencies exist
ISSUE_008_DEPENDENCIES=(
  "project.yaml"                      # Issue-005
  "docs/system/outputs/.gitkeep"      # Issue-006
  "docs/system/ai-process.md"         # Issue-011
)

for file in "${ISSUE_008_DEPENDENCIES[@]}"; do
  if [[ ! -f "${PROJECT_PATH}/${file}" ]]; then
    validation_error "Dependency artifact missing: ${file}"
  fi
done

# Verify own artifact created
if [[ ! -f "${PROJECT_PATH}/docs/system/pending-items-rules.md" ]]; then
  validation_error "Failed to create docs/system/pending-items-rules.md"
fi

echo "✅ pending-items-rules.md deployed successfully"
```

**Key Features**:
- Verifies only 3 dependency artifacts from prior issues (005, 006, 011)
- Does NOT assert full bootstrap completeness
- Dependency-scoped verification per user requirement
- Verifies own artifact created successfully

---

## Acceptance Criteria — Verification

**Template Verification**:
- ✅ Template exists: `templates/project/pending-items-rules.md.tmpl` (from Issue-001)
- ✅ Template contains P-### → {PREFIX}-### mapping rule

**Source-of-Truth Reading**:
- ✅ Reads identity values from `PROJECT_PATH/project.yaml` (NOT from raw CLI input)
- ✅ Uses same read_yaml_field() function from Issue-006 (bounded awk extraction)

**File Creation**:
- ✅ Verifies `PROJECT_PATH/docs/system/outputs/` directory exists (created in Issue-006)
- ✅ Parent directory `PROJECT_PATH/docs/system/` inferred to exist (contains outputs/ subdirectory)
- ✅ Deploys to `PROJECT_PATH/docs/system/pending-items-rules.md`
- ✅ File permissions are readable (minimum 644)

**Token Substitution**:
- ✅ `{Project Name}` token replaced with actual project name from project.yaml
- ✅ `{project-slug}` token replaced with actual project slug from project.yaml
- ✅ `{PREFIX}` token replaced with actual project prefix from project.yaml
- ✅ HALT: "Unresolved token in pending-items-rules.md" if allowed token patterns remain
- ✅ File references project.yaml as identity source (template contains link)

**Governance Compatibility**:
- ✅ Does NOT conflict with governance protection (rules are project-specific, not governance)
- ✅ File is allowed in docs/system/ per P-084 Section 4.1 (project-specific rules)

**Dependency Verification**:
- ✅ Verifies required artifacts from dependencies exist:
  - project.yaml (Issue-005 dependency)
  - docs/system/outputs/.gitkeep (Issue-006 dependency)
  - docs/system/ai-process.md (Issue-011 dependency)
- ✅ Creates own artifact: docs/system/pending-items-rules.md

---

## Output Updates

**New success output**:
```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully
✅ ai-process.md deployed successfully
✅ pending-items-rules.md deployed successfully

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
  pending-items-rules.md: /Users/me/projects/my-project/docs/system/pending-items-rules.md

Created Directories:
  phases/:              /Users/me/projects/my-project/phases/
  docs/system/outputs/: /Users/me/projects/my-project/docs/system/outputs/

Path Invariants:
  ✅ Sibling structure verified
  ✅ No nesting detected
  ✅ Relative path invariant satisfied

Bootstrap Complete:
  ✅ P-084 bootstrap artifacts deployed
  ✅ AI Process Contract deployed (Issue-011)
  ✅ Namespace mapping documented (P-### → MP-###)
  ✅ Ready for project planning and building

Note: YAML syntax and semantic validation deferred to Issue-009
      Git initialization is explicit non-goal per P-084 Section 7
```

---

## Integration with Previous Issues

**Issue-001** (templates):
- Uses pending-items-rules.md.tmpl created in Issue-001
- Template validated for correct token syntax and namespace mapping

**Issue-005** (project.yaml):
- Reads identity values from project.yaml created in Issue-005
- Reuses escape_sed() function for safe token substitution

**Issue-006** (remaining bootstrap files):
- Reuses read_yaml_field() function from Issue-006
- Reuses escaped identity values (ESCAPED_SLUG, ESCAPED_NAME, ESCAPED_PREFIX)
- Uses docs/system/outputs/ directory created in Issue-006
- Consistent token substitution logic

**Issue-011** (ai-process.md):
- Uses docs/system/ directory existence from Issue-011
- Verifies ai-process.md dependency artifact
- Consistent rendering approach

---

## Technical Highlights

### 3-Token Substitution

**Tokens** (pending-items-rules.md only):
1. `{project-slug}` → actual project slug
2. `{Project Name}` → actual project name
3. `{PREFIX}` → actual project prefix

**No date token**: pending-items-rules.md does not require `{YYYY-MM-DD}` token.

### Dependency-Scoped Verification

**Pattern**: Verify only required dependency artifacts, not full bootstrap completeness.

**Benefits**:
- Issue-level verification scoped to actual dependencies
- Does NOT assert global bootstrap state at individual issue level
- Clearer dependency chain (Issue-008 depends on 005, 006, 011)
- Allows independent issue verification without full bootstrap assumption

**Dependency Chain**:
- Issue-005: project.yaml (identity source-of-truth)
- Issue-006: read_yaml_field(), docs/system/outputs/ directory
- Issue-011: docs/system/ directory existence

### outputs/ Directory Check

**Pattern**: Check outputs/ subdirectory existence to confirm docs/system/ parent exists.

**Benefits**:
- Does NOT assume docs/system/ directory independently
- Verifies outputs/ subdirectory created in Issue-006
- outputs/ existence confirms docs/system/ parent exists
- More explicit dependency verification

### Documentation-Only File

**Purpose**: pending-items-rules.md documents namespace mapping but does NOT enforce it at runtime.

**Enforcement Clarification**:
- File provides reference documentation for P-### → {PREFIX}-### mapping
- Mapping rule defined in P-084 Section 5.1
- Runtime enforcement is NOT in scope for Issue-008
- AI agents reading the file understand the mapping, but file does NOT validate identifiers

---

## Namespace Mapping Documentation

**Purpose**: pending-items-rules.md serves as project-specific reference documentation for the P-### → {PREFIX}-### mapping rule defined in P-084 Section 5.1.

**Mapping Examples** (template content):
- P-001 → {PREFIX}-001
- P-042 → {PREFIX}-042
- P-999 → {PREFIX}-999

**Enforcement** (template content):
- All project-specific pending items MUST use {PREFIX}-### format
- This project MUST NOT reference automated-builder P-### identifiers directly
- The prefix value is immutable after project creation

**Identity Source** (template content):
- All prefix references derive from [project.yaml](../project.yaml)
- project.yaml is the authoritative source for project identity

---

## Commits

- `dfe011b` — Issue-008 approved artifact (renamed from proposal)
- `9377ed0` — Issue-008 implementation (pending-items-rules.md deployment)

---

## Next Steps

Per P-084 Section 10 Implementation Plan:
- **Issue-009**: End-to-end validation (YAML parsing, semantic checks)
- **Issue-007**: Governance protection validation (post-creation scan)

**Bootstrap Status**: Complete. All P-084 bootstrap artifacts deployed. Ready for Issue-009 validation.

---

## References

- Approved Artifact: [2026-02-16__18__system__issue-008-approved.md](2026-02-16__18__system__issue-008-approved.md)
- P-084 Inventory: [2026-02-13__01__system__p-084-inventory-approved.md](2026-02-13__01__system__p-084-inventory-approved.md)
- P-084 Section 5.1: Namespace Conversion Contract
- Template: [templates/project/pending-items-rules.md.tmpl](../../../templates/project/pending-items-rules.md.tmpl)
- Implementation: [scripts/run-create-project](../../../scripts/run-create-project)
