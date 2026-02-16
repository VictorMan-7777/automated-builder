# Issue-006 Proposal — Implement Remaining File Creation from project.yaml

**Issue**: Issue-006 — Implement Placeholder Substitution for Remaining Files
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Proposed

---

## Objective

Implement P-084 Section 2.3 placeholder substitution from project.yaml as source-of-truth for remaining bootstrap files and directories.

---

## Scope

### In Scope

- ✅ Read identity values from deployed `PROJECT_PATH/project.yaml` (NOT from input parameters)
- ✅ Render 5 remaining templates using project.yaml as single source-of-truth
- ✅ Create index.md, prd.md, roadmap.md, iteration-log.md, builder-manifest.yaml
- ✅ Create phases/ directory with .gitkeep
- ✅ Create docs/system/outputs/ directory with .gitkeep
- ✅ Post-substitution validation (Section 2.3 table)
- ✅ Reuse safe token substitution from Issue-005 (escape_sed() function)

### Out of Scope

- ❌ ai-process.md deployment (handled by Issue-011)
- ❌ Governance file copying (prohibited by Section 4.1)
- ❌ Git initialization (explicit non-goal per P-084 Section 7)
- ❌ YAML parsing for project.yaml (already validated in Issue-005)

---

## Acceptance Criteria

**Source-of-Truth Reading**:
- [ ] Reads identity values from `PROJECT_PATH/project.yaml` (NOT from input parameters)
- [ ] Parsing extracts: identity.slug, identity.name, identity.prefix, identity.created
- [ ] HALT: "Cannot read project.yaml" if file missing or unreadable
- [ ] HALT: "Invalid project.yaml structure" if required fields missing

**File Creation**:
- [ ] Creates `PROJECT_PATH/index.md` with all tokens substituted per Section 3.2
- [ ] Creates `PROJECT_PATH/prd.md` with all tokens substituted per Section 3.3
- [ ] Creates `PROJECT_PATH/roadmap.md` with all tokens substituted per Section 3.4
- [ ] Creates `PROJECT_PATH/iteration-log.md` with all tokens substituted per Section 3.5
- [ ] Creates `PROJECT_PATH/builder-manifest.yaml` with identity_source reference per Section 3.6
- [ ] builder-manifest.yaml contains comment: "project.yaml is the authoritative source"

**Directory Creation**:
- [ ] Creates `PROJECT_PATH/phases/` directory with `.gitkeep`
- [ ] Creates `PROJECT_PATH/docs/system/outputs/` directory with `.gitkeep`
- [ ] Directory permissions allow read/write/execute (755 or better)

**Validation**:
- [ ] HALT: "Unresolved token in {file}" if any `{...}` patterns remain (except code blocks)
- [ ] HALT: "Empty value for token" if any token replaced with empty string
- [ ] HALT: "Inconsistency detected" if any file contains values not matching project.yaml
- [ ] All 8 non-ai-process bootstrap files exist after completion (project.yaml + 5 files + 2 .gitkeep files)

**Token Substitution Safety**:
- [ ] Reuses escape_sed() function from Issue-005
- [ ] Safe for values containing '/', '&', or backslashes
- [ ] Uses '|' delimiter in sed commands

---

## P-084 Section Requirements

### Section 2.3 — Placeholder Substitution Contract

**Token Syntax**: `{Token Name}` (curly braces, Title Case or UPPERCASE)

**Allowed Tokens**:

| Token | Source | Example Value |
|-------|--------|---------------|
| `{project-slug}` | project.yaml: identity.slug | `devotional-generator` |
| `{Project Slug}` | project.yaml: identity.slug | `devotional-generator` |
| `{Project Name}` | project.yaml: identity.name | `Devotional Generator` |
| `{PREFIX}` | project.yaml: identity.prefix | `DG` |
| `{YYYY-MM-DD}` | project.yaml: identity.created | `2026-02-16` |

**Substitution Source**: All token values MUST be read from `project.yaml` (Section 2.4 source-of-truth).

**Post-Substitution Validation** (Section 2.3 table):

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| No unreplaced tokens | No `{...}` patterns remain except in code blocks or examples | HALT: "Unresolved token in {filename}: {token}" |
| No empty values | No tokens replaced with empty strings | HALT: "Empty value for token: {token}" |
| Date format valid | `{YYYY-MM-DD}` is valid ISO 8601 date | HALT: "Invalid date format: {value}" |

### Section 3 — Bootstrap File Specifications

**3.2 — index.md**: Project navigation and overview (see P-084 lines 427-468)
**3.3 — prd.md**: Product Requirements Document (see P-084 lines 478-521)
**3.4 — roadmap.md**: Milestones and timeline (see P-084 lines 531-561)
**3.5 — iteration-log.md**: Planning evolution tracking (see P-084 lines 571-596)
**3.6 — builder-manifest.yaml**: Project manifest for Builder operations (see P-084 lines 606-643)

**3.7 — phases/ directory**: Container for detailed phase plans (empty with .gitkeep)
**3.8 — docs/system/outputs/ directory**: Project workflow artifacts storage (empty with .gitkeep)

---

## Implementation Approach

### Step 1: Read project.yaml (Source-of-Truth)

Extend `scripts/run-create-project` to read identity values from deployed project.yaml:

```bash
# After project.yaml created and validated (Issue-005)

# Read identity values from project.yaml (source-of-truth)
# Use grep/sed for POSIX-compliant YAML parsing (simple structure)

read_yaml_field() {
  local file="$1"
  local field="$2"
  # Extract value after "field: " (handles quoted and unquoted values)
  local value="$(grep "^  ${field}:" "${file}" | sed 's/^  [^:]*: *//' | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/")"
  echo "${value}"
}

PROJECT_YAML="${PROJECT_PATH}/project.yaml"

# Verify project.yaml exists and is readable
if [[ ! -f "${PROJECT_YAML}" ]]; then
  validation_error "Cannot read project.yaml: file missing"
fi
if [[ ! -r "${PROJECT_YAML}" ]]; then
  validation_error "Cannot read project.yaml: file not readable"
fi

# Extract identity values (source-of-truth)
IDENTITY_SLUG="$(read_yaml_field "${PROJECT_YAML}" "slug")"
IDENTITY_NAME="$(read_yaml_field "${PROJECT_YAML}" "name")"
IDENTITY_PREFIX="$(read_yaml_field "${PROJECT_YAML}" "prefix")"
IDENTITY_CREATED="$(read_yaml_field "${PROJECT_YAML}" "created")"

# Validate extracted values (basic non-empty check)
[[ -z "${IDENTITY_SLUG}" ]] && validation_error "Invalid project.yaml structure: missing identity.slug"
[[ -z "${IDENTITY_NAME}" ]] && validation_error "Invalid project.yaml structure: missing identity.name"
[[ -z "${IDENTITY_PREFIX}" ]] && validation_error "Invalid project.yaml structure: missing identity.prefix"
[[ -z "${IDENTITY_CREATED}" ]] && validation_error "Invalid project.yaml structure: missing identity.created"
```

### Step 2: Create Directories

```bash
# Create phases/ directory with .gitkeep
mkdir -p "${PROJECT_PATH}/phases" || validation_error "Cannot create phases directory"
touch "${PROJECT_PATH}/phases/.gitkeep" || validation_error "Cannot create phases/.gitkeep"

# Create docs/system/outputs/ directory with .gitkeep
mkdir -p "${PROJECT_PATH}/docs/system/outputs" || validation_error "Cannot create docs/system/outputs directory"
touch "${PROJECT_PATH}/docs/system/outputs/.gitkeep" || validation_error "Cannot create docs/system/outputs/.gitkeep"
```

### Step 3: Render Templates with Safe Token Substitution

Reuse `escape_sed()` function from Issue-005 for safe token substitution:

```bash
# Escape values for safe sed substitution (reuse from Issue-005)
ESCAPED_SLUG="$(escape_sed "${IDENTITY_SLUG}")"
ESCAPED_NAME="$(escape_sed "${IDENTITY_NAME}")"
ESCAPED_PREFIX="$(escape_sed "${IDENTITY_PREFIX}")"
ESCAPED_CREATED="$(escape_sed "${IDENTITY_CREATED}")"

# Render each template
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

  # Check for unresolved tokens (excluding code blocks - basic check)
  if grep -q '{.*}' "${output_file}"; then
    UNRESOLVED=$(grep -o '{[^}]*}' "${output_file}" | head -1)
    validation_error "Unresolved token in ${output_file}: ${UNRESOLVED}"
  fi

  # Validate file readable
  if [[ ! -r "${output_file}" ]]; then
    validation_error "${output_file} is not readable"
  fi
}

# Create bootstrap files
render_template "index.md" "${PROJECT_PATH}/index.md"
render_template "prd.md" "${PROJECT_PATH}/prd.md"
render_template "roadmap.md" "${PROJECT_PATH}/roadmap.md"
render_template "iteration-log.md" "${PROJECT_PATH}/iteration-log.md"
render_template "builder-manifest.yaml" "${PROJECT_PATH}/builder-manifest.yaml"
```

### Step 4: Post-Creation Validation

```bash
# Verify all required files exist (8 files total: 1 + 5 + 2 .gitkeep)
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

echo "✅ All bootstrap files created successfully"
```

---

## Token Sources

All tokens MUST be read from `project.yaml` (source-of-truth):

| Token | Source Field | Read Method | Example Value |
|-------|--------------|-------------|---------------|
| `{project-slug}` | identity.slug | read_yaml_field | `devotional-generator` |
| `{Project Slug}` | identity.slug | read_yaml_field | `devotional-generator` |
| `{Project Name}` | identity.name | read_yaml_field | `Devotional Generator` |
| `{PREFIX}` | identity.prefix | read_yaml_field | `DG` |
| `{YYYY-MM-DD}` | identity.created | read_yaml_field | `2026-02-16` |

**Critical Rule**: Input parameters from command-line MUST NOT be used for token substitution in Issue-006. Only project.yaml is authoritative.

---

## Validation Strategy

### File Creation Validation

1. **Template existence**: Check template file before rendering
2. **File creation**: Verify output file exists after rendering
3. **Unresolved tokens**: grep for `{...}` patterns (basic check)
4. **File readability**: Check file permissions

### Source-of-Truth Validation

1. **project.yaml readable**: File exists and has read permissions
2. **Required fields present**: All identity fields extracted successfully
3. **No empty values**: All extracted values are non-empty strings

### Post-Substitution Validation

1. **All files exist**: 8 required files present
2. **Directories created**: phases/ and docs/system/outputs/ exist
3. **No unresolved tokens**: No `{...}` patterns remain (basic check)

**Note**: Code block handling (excluding `{...}` in markdown code blocks) is a basic grep check. Full AST-based parsing is deferred.

---

## Dependencies

- Issue-005 (project.yaml created and validated) ✅

---

## Files Likely Touched

- `scripts/run-create-project` (extend with file creation logic)
- `../<project-slug>/index.md` (create)
- `../<project-slug>/prd.md` (create)
- `../<project-slug>/roadmap.md` (create)
- `../<project-slug>/iteration-log.md` (create)
- `../<project-slug>/builder-manifest.yaml` (create)
- `../<project-slug>/phases/.gitkeep` (create)
- `../<project-slug>/docs/system/outputs/.gitkeep` (create)

---

## Risks / Failure Modes

- **Reading project.yaml fails**: File missing or corrupted
  - Mitigation: Explicit existence and readability checks; should not happen (just created in Issue-005)
- **Template missing**: Template file not found for a file
  - Mitigation: Template existence check before rendering; templates created in Issue-001
- **Token substitution inconsistent with Issue-005**: Different logic produces different results
  - Mitigation: Reuse escape_sed() function and sed patterns from Issue-005
- **Directory creation permissions issues**: Cannot create phases/ or docs/system/outputs/
  - Mitigation: Check mkdir success; validate directory exists after creation
- **Code block tokens falsely detected**: Grep finds `{...}` in markdown code blocks
  - Mitigation: Basic grep check; false positives acceptable for MVP (manual review catches them)

---

## Testing Strategy

### Manual Test Cases

1. **Valid project bootstrap** (end-to-end):
   ```bash
   run-create-project --slug test-project --name "Test Project" --prefix TP
   ls -la ../test-project/
   ```
   Expected: All 8 files/directories created

2. **Token substitution verification**:
   ```bash
   run-create-project --slug token-test --name "Token Test App" --prefix TT
   grep -r '{' ../token-test/
   ```
   Expected: No unresolved `{...}` tokens (except in code blocks)

3. **Source-of-truth reading**:
   ```bash
   run-create-project --slug source-test --name "Source Test" --prefix ST
   grep 'slug: source-test' ../source-test/project.yaml
   grep 'source-test' ../source-test/index.md
   grep 'ST' ../source-test/builder-manifest.yaml
   ```
   Expected: All files contain values from project.yaml (not from command-line directly)

4. **Directory structure**:
   ```bash
   run-create-project --slug dir-test --name "Directory Test" --prefix DT
   tree -a ../dir-test/
   ```
   Expected: phases/ and docs/system/outputs/ exist with .gitkeep

5. **Special characters in values** (Issue-005 safety):
   ```bash
   run-create-project --slug special --name "Test/Name&Value" --prefix SC
   cat ../special/index.md
   ```
   Expected: Special characters rendered correctly (escaped sed prevents corruption)

---

## Output Updates

Update success output to include all file creation:

```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully

Normalized Parameters:
  project-slug: test-project
  project-name: Test Project
  prefix:       TP
  parent-dir:   /Users/me/projects

Resolved Paths:
  BUILDER_ROOT: /Users/me/projects/automated-builder
  PARENT_DIR:   /Users/me/projects
  PROJECT_PATH: /Users/me/projects/test-project

Created Files:
  project.yaml:         /Users/me/projects/test-project/project.yaml
  index.md:             /Users/me/projects/test-project/index.md
  prd.md:               /Users/me/projects/test-project/prd.md
  roadmap.md:           /Users/me/projects/test-project/roadmap.md
  iteration-log.md:     /Users/me/projects/test-project/iteration-log.md
  builder-manifest.yaml: /Users/me/projects/test-project/builder-manifest.yaml

Created Directories:
  phases/:              /Users/me/projects/test-project/phases/
  docs/system/outputs/: /Users/me/projects/test-project/docs/system/outputs/

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
- Templates already validated for correct token syntax

**Issue-002** (parameters):
- DOES NOT use command-line parameters for token substitution
- Only uses parameters for initial project.yaml creation (Issue-005)

**Issue-003** (paths):
- Uses validated PROJECT_PATH for file creation
- Creates files only after all path invariants verified

**Issue-005** (project.yaml):
- Reads identity values from project.yaml created in Issue-005
- Reuses escape_sed() function for safe token substitution
- Uses same sed patterns with '|' delimiter

---

## References

- Primary Authority: [P-084 Section 10: Issue-006](2026-02-13__01__system__p-084-inventory-approved.md)
- Placeholder Substitution: P-084 Section 2.3
- Source-of-Truth: P-084 Section 2.4
- Bootstrap Files: P-084 Section 3.2-3.8
- Dependencies: Issue-005 (project.yaml creation)
- Safe Substitution: Issue-005 implementation (escape_sed() function)
