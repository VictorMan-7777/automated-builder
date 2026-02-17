# Issue-006 Implementation Summary

**Issue**: Issue-006 — Implement Placeholder Substitution for Remaining Files
**Parent**: P-084 — run-create-project Bootstrap Specification
**Date**: 2026-02-16
**Status**: Complete

---

## Implementation Overview

Extended `system/scripts/run-create-project.md` to create remaining bootstrap files from project.yaml as source-of-truth. Implements bounded awk extraction from identity: block, explicit token pattern validation, and safe sed substitution.

---

## Files Modified

- `system/scripts/run-create-project.md` (+130 lines, -4 lines)

---

## Implementation Details

### Source-of-Truth Reading

**read_yaml_field() function** (added):
```bash
read_yaml_field() {
  local file="$1"
  local field="$2"
  # Extract value from identity: block only using bounded awk extraction
  # awk extracts lines BETWEEN "identity:" and next top-level key (exclusive of both endpoints)
  # then grep searches only within that extracted block
  local value="$(awk '/^identity:/ {in_identity=1; next} /^[a-z_]+:/ {if (in_identity) exit} in_identity {print}' "${file}" | grep "^  ${field}:" | head -1 | sed 's/^  [^:]*: *//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")"
  echo "${value}"
}
```

**Key Features**:
- Bounded awk extraction: `/^identity:/ {in_identity=1; next} /^[a-z_]+:/ {if (in_identity) exit}`
- Extracts only lines BETWEEN `identity:` and next top-level key (exclusive endpoints)
- Eliminates cross-block field collision risk
- grep searches only within extracted identity: block

**Identity Block Verification**:
```bash
# Verify identity: block exists (scoped extraction)
if ! grep -q "^identity:" "${PROJECT_YAML}"; then
  validation_error "Invalid project.yaml structure: missing identity: block"
fi
```

**Field Extraction**:
```bash
IDENTITY_SLUG="$(read_yaml_field "${PROJECT_YAML}" "slug")"
IDENTITY_NAME="$(read_yaml_field "${PROJECT_YAML}" "name")"
IDENTITY_PREFIX="$(read_yaml_field "${PROJECT_YAML}" "prefix")"
IDENTITY_CREATED="$(read_yaml_field "${PROJECT_YAML}" "created")"
```

### Directory Creation

**phases/ and docs/system/outputs/ with .gitkeep**:
```bash
mkdir -p "${PROJECT_PATH}/phases" || validation_error "Cannot create phases directory"
touch "${PROJECT_PATH}/phases/.gitkeep" || validation_error "Cannot create phases/.gitkeep"

mkdir -p "${PROJECT_PATH}/docs/system/outputs" || validation_error "Cannot create docs/system/outputs directory"
touch "${PROJECT_PATH}/docs/system/outputs/.gitkeep" || validation_error "Cannot create docs/system/outputs/.gitkeep"
```

### Template Rendering

**render_template() function** (added):
```bash
render_template() {
  local template_name="$1"
  local output_file="$2"

  local template_path="${BUILDER_ROOT}/templates/project/${template_name}.tmpl"

  # Verify template exists
  if [[ ! -f "${template_path}" ]]; then
    validation_error "Template not found: ${template_path}"
  fi

  # Render template with safe token substitution (use '|' delimiter)
  cat "${template_path}" \
    | sed "s|{project-slug}|${ESCAPED_SLUG}|g" \
    | sed "s|{Project Slug}|${ESCAPED_SLUG}|g" \
    | sed "s|{Project Name}|${ESCAPED_NAME}|g" \
    | sed "s|{PREFIX}|${ESCAPED_PREFIX}|g" \
    | sed "s|{YYYY-MM-DD}|${ESCAPED_CREATED}|g" \
    > "${output_file}"

  # Validate file created
  if [[ ! -f "${output_file}" ]]; then
    validation_error "Failed to create ${output_file}"
  fi

  # Check for unresolved allowed tokens (explicit pattern matching)
  if grep -E '\{(project-slug|Project Slug|Project Name|PREFIX|YYYY-MM-DD)\}' "${output_file}" >/dev/null 2>&1; then
    UNRESOLVED=$(grep -oE '\{(project-slug|Project Slug|Project Name|PREFIX|YYYY-MM-DD)\}' "${output_file}" | head -1)
    validation_error "Unresolved token in ${output_file}: ${UNRESOLVED}"
  fi

  # Validate file readable
  if [[ ! -r "${output_file}" ]]; then
    validation_error "${output_file} is not readable"
  fi
}
```

**Key Features**:
- Reuses escape_sed() function from Issue-005
- Safe sed substitution with '|' delimiter
- Explicit token pattern validation (5 allowed patterns only)
- No generic `{.*}` grep (prevents false matches)

**Files Created**:
```bash
render_template "index.md" "${PROJECT_PATH}/index.md"
render_template "prd.md" "${PROJECT_PATH}/prd.md"
render_template "roadmap.md" "${PROJECT_PATH}/roadmap.md"
render_template "iteration-log.md" "${PROJECT_PATH}/iteration-log.md"
render_template "builder-manifest.yaml" "${PROJECT_PATH}/builder-manifest.yaml"
```

### Post-Creation Validation

**Required Files Check**:
```bash
REQUIRED_FILES=(
  "project.yaml"
  "index.md"
  "prd.md"
  "roadmap.md"
  "iteration-log.md"
  "builder-manifest.yaml"
  "phases/.gitkeep"
  "docs/system/outputs/.gitkeep"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "${PROJECT_PATH}/${file}" ]]; then
    validation_error "Required file missing: ${file}"
  fi
done
```

---

## Acceptance Criteria — Verification

**Source-of-Truth Reading**:
- ✅ Reads identity values from `PROJECT_PATH/project.yaml` (NOT from input parameters)
- ✅ Parsing extracts: identity.slug, identity.name, identity.prefix, identity.created
- ✅ HALT: "Cannot read project.yaml" if file missing or unreadable
- ✅ HALT: "Invalid project.yaml structure" if required fields missing

**File Creation**:
- ✅ Creates `PROJECT_PATH/index.md` with all tokens substituted per Section 3.2
- ✅ Creates `PROJECT_PATH/prd.md` with all tokens substituted per Section 3.3
- ✅ Creates `PROJECT_PATH/roadmap.md` with all tokens substituted per Section 3.4
- ✅ Creates `PROJECT_PATH/iteration-log.md` with all tokens substituted per Section 3.5
- ✅ Creates `PROJECT_PATH/builder-manifest.yaml` with identity_source reference per Section 3.6
- ✅ builder-manifest.yaml contains comment: "project.yaml is the authoritative source"

**Directory Creation**:
- ✅ Creates `PROJECT_PATH/phases/` directory with `.gitkeep`
- ✅ Creates `PROJECT_PATH/docs/system/outputs/` directory with `.gitkeep`
- ✅ Directory permissions allow read/write/execute (755 or better)

**Validation**:
- ✅ HALT: "Unresolved token in {file}" if allowed token patterns remain
- ✅ HALT: "Empty value for token" if any token replaced with empty string (non-empty check implemented)
- ✅ HALT: "Inconsistency detected" if any file contains values not matching project.yaml (source-of-truth enforced)
- ✅ All 8 non-ai-process bootstrap files exist after completion
- ✅ Full YAML syntax and semantic validation explicitly deferred to Issue-009

**Token Substitution Safety**:
- ✅ Reuses escape_sed() function from Issue-005
- ✅ Safe for values containing '/', '&', or backslashes
- ✅ Uses '|' delimiter in sed commands

---

## Token Sources

All tokens read from project.yaml identity: block:

| Token | Source Field | Read Method | Implementation |
|-------|--------------|-------------|----------------|
| `{project-slug}` | identity.slug | read_yaml_field() | Bounded awk extraction |
| `{Project Slug}` | identity.slug | read_yaml_field() | Bounded awk extraction |
| `{Project Name}` | identity.name | read_yaml_field() | Bounded awk extraction |
| `{PREFIX}` | identity.prefix | read_yaml_field() | Bounded awk extraction |
| `{YYYY-MM-DD}` | identity.created | read_yaml_field() | Bounded awk extraction |

**Critical Rule Satisfied**: Input parameters from command-line NOT used for token substitution in Issue-006. Only project.yaml is authoritative.

---

## Output Updates

**New success output**:
```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully

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

Created Directories:
  phases/:              /Users/me/projects/my-project/phases/
  docs/system/outputs/: /Users/me/projects/my-project/docs/system/outputs/

Path Invariants:
  ✅ Sibling structure verified
  ✅ No nesting detected
  ✅ Relative path invariant satisfied

Note: ai-process.md deployment is deferred to Issue-011
      YAML syntax and semantic validation deferred to Issue-009
      Git initialization is explicit non-goal per P-084 Section 7
```

---

## Integration with Previous Issues

**Issue-001** (templates):
- Uses 5 template files created in Issue-001
- Templates validated for correct token syntax

**Issue-002** (parameters):
- DOES NOT use command-line parameters for token substitution
- Only uses parameters for initial project.yaml creation (Issue-005)

**Issue-003** (paths):
- Uses validated PROJECT_PATH for file creation
- Creates files only after all path invariants verified

**Issue-004** (prefix):
- Reads validated prefix from project.yaml identity: block

**Issue-005** (project.yaml):
- Reads identity values from project.yaml created in Issue-005
- Reuses escape_sed() function for safe token substitution
- Uses same sed patterns with '|' delimiter

---

## Technical Highlights

### Bounded awk Extraction (Inclusive Range Bug Fix)

**Problem**: Range operator `/^identity:/,/^[a-z_]+:/` is inclusive of both endpoints, including the next top-level key in output.

**Solution**: Flag-based extraction with explicit exit:
```bash
awk '/^identity:/ {in_identity=1; next} /^[a-z_]+:/ {if (in_identity) exit} in_identity {print}' "${file}"
```

**Benefits**:
- Extracts only lines BETWEEN endpoints (exclusive)
- Stops before next top-level key (e.g., `schema_version:`)
- Eliminates cross-block field collision risk
- Scoped extraction ensures correct field values

### Explicit Token Pattern Validation

**Pattern**: `grep -E '\{(project-slug|Project Slug|Project Name|PREFIX|YYYY-MM-DD)\}'`

**Benefits**:
- Checks only allowed token patterns (5 patterns)
- No false matches from other brace patterns (code examples, JSON snippets)
- Strict validation without code block exclusion logic
- Deterministic detection

---

## Commits

- `e114249` — Issue-006 proposal (initial)
- `69476d7` — Issue-006 approved artifact (with awk fix)
- `756305a` — Issue-006 implementation (remaining bootstrap files)

---

## Next Steps

Per P-084 Section 10 Implementation Plan:
- **Issue-011**: Deploy ai-process.md (can be parallel with Issue-006, now unblocked)
- **Issue-009**: End-to-end validation (YAML parsing, semantic checks)

---

## References

- Approved Artifact: [2026-02-16__14__system__issue-006-approved.md](2026-02-16__14__system__issue-006-approved.md)
- P-084 Inventory: [2026-02-13__01__system__p-084-inventory-approved.md](2026-02-13__01__system__p-084-inventory-approved.md)
- P-084 Section 2.3: Placeholder Substitution Contract
- P-084 Section 2.4: Project Identity (Source-of-Truth)
- P-084 Section 3.2-3.8: Bootstrap File Specifications
- Implementation: [system/scripts/run-create-project.md](../../../system/scripts/run-create-project.md)
