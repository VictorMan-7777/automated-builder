# Issue-008 Proposal — Deploy Project Rules Pack Template

**Issue**: Issue-008 — Deploy Project Rules Pack Template
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Proposed

---

## Objective

Deploy project-specific pending-items-rules.md with PREFIX substitution to document P-### → {PREFIX}-### namespace mapping. This file provides reference documentation only; it does not enforce the mapping at runtime.

---

## Scope

### In Scope

- ✅ Render `pending-items-rules.md.tmpl` with `{PREFIX}` substituted
- ✅ Deploy to `PROJECT_PATH/docs/system/pending-items-rules.md`
- ✅ Verify parent directory `docs/system/` exists (created in Issue-006/011)
- ✅ Reuse token substitution logic from Issue-006/011
- ✅ Explicit token pattern validation

### Out of Scope

- ❌ Runtime enforcement of namespace mapping (file is documentation only)
- ❌ Complex rules logic (just template rendering)
- ❌ Git initialization (explicit non-goal per P-084 Section 7)
- ❌ YAML syntax and semantic validation (deferred to Issue-009)

---

## Acceptance Criteria

**Template Verification**:
- [ ] Template exists: `templates/project/pending-items-rules.md.tmpl` (from Issue-001)
- [ ] Template contains P-### → {PREFIX}-### mapping rule

**Source-of-Truth Reading**:
- [ ] Reads identity values from `PROJECT_PATH/project.yaml` (NOT from raw CLI input)
- [ ] Uses same read_yaml_field() function from Issue-006 (bounded awk extraction)

**File Creation**:
- [ ] Verifies `PROJECT_PATH/docs/system/outputs/` directory exists (created in Issue-006)
- [ ] Parent directory `PROJECT_PATH/docs/system/` inferred to exist (contains outputs/ subdirectory)
- [ ] Deploys to `PROJECT_PATH/docs/system/pending-items-rules.md`
- [ ] File permissions are readable (minimum 644)

**Token Substitution**:
- [ ] `{Project Name}` token replaced with actual project name from project.yaml
- [ ] `{project-slug}` token replaced with actual project slug from project.yaml
- [ ] `{PREFIX}` token replaced with actual project prefix from project.yaml
- [ ] HALT: "Unresolved token in pending-items-rules.md" if allowed token patterns remain
- [ ] File references project.yaml as identity source (template contains link)

**Governance Compatibility**:
- [ ] Does NOT conflict with governance protection (rules are project-specific, not governance)
- [ ] File is allowed in docs/system/ per P-084 Section 4.1 (project-specific rules)

**Dependency Verification**:
- [ ] Verifies required artifacts from dependencies exist:
  - project.yaml (Issue-005 dependency)
  - docs/system/outputs/.gitkeep (Issue-006 dependency)
  - docs/system/ai-process.md (Issue-011 dependency)
- [ ] Creates own artifact: docs/system/pending-items-rules.md

---

## P-084 Section Requirements

### Section 5.1 — Namespace Conversion Contract

**Purpose**: Map automated-builder's `P-###` pending items to project-specific `<PREFIX>-###` identifiers.

**Mapping Rule**:

| Source Identifier | Project Identifier | Example (prefix=DG) |
|-------------------|-------------------|---------------------|
| P-001 | {PREFIX}-001 | DG-001 |
| P-042 | {PREFIX}-042 | DG-042 |
| P-999 | {PREFIX}-999 | DG-999 |

**Enforcement**:
- All project-specific pending items MUST use `{PREFIX}-###` format
- Project MUST NOT reference automated-builder `P-###` identifiers directly
- Prefix MUST be stored in `project.yaml` as the authoritative source

**Template Purpose**: pending-items-rules.md documents this mapping for project-specific reference.

### Template Placeholders

| Token | Source | Example Value |
|-------|--------|---------------|
| `{Project Name}` | project.yaml: identity.name | `Devotional Generator` |
| `{project-slug}` | project.yaml: identity.slug | `devotional-generator` |
| `{PREFIX}` | project.yaml: identity.prefix | `DG` |

**Note**: Only 3 tokens (no date token needed for this template).

---

## Implementation Approach

### Step 1: Read Identity Values (Reuse from Issue-006/011)

Issue-008 reuses the same read_yaml_field() and identity extraction logic:

```bash
# Read identity values from project.yaml (source-of-truth)
# read_yaml_field() function already defined in Issue-006

PROJECT_YAML="${PROJECT_PATH}/project.yaml"

# Extract identity values (reuse from Issue-006/011)
IDENTITY_SLUG="$(read_yaml_field "${PROJECT_YAML}" "slug")"
IDENTITY_NAME="$(read_yaml_field "${PROJECT_YAML}" "name")"
IDENTITY_PREFIX="$(read_yaml_field "${PROJECT_YAML}" "prefix")"

# Values already validated in Issue-006 (non-empty checks)
```

### Step 2: Verify Directory and Template

```bash
# Template path
PENDING_ITEMS_TEMPLATE="${BUILDER_ROOT}/templates/project/pending-items-rules.md.tmpl"
PENDING_ITEMS_OUTPUT="${PROJECT_PATH}/docs/system/pending-items-rules.md"

# Verify template exists
if [[ ! -f "${PENDING_ITEMS_TEMPLATE}" ]]; then
  validation_error "Template not found: ${PENDING_ITEMS_TEMPLATE}"
fi

# Verify docs/system/outputs/ directory exists (created in Issue-006)
# This implicitly confirms docs/system/ exists (parent of outputs/)
if [[ ! -d "${PROJECT_PATH}/docs/system/outputs" ]]; then
  validation_error "docs/system/outputs/ directory missing (should have been created in Issue-006)"
fi
```

### Step 3: Render Template

Reuse escape_sed() and rendering logic from Issue-006/011:

```bash
# Escape values for safe sed substitution (reuse from Issue-005/006/011)
ESCAPED_SLUG="$(escape_sed "${IDENTITY_SLUG}")"
ESCAPED_NAME="$(escape_sed "${IDENTITY_NAME}")"
ESCAPED_PREFIX="$(escape_sed "${IDENTITY_PREFIX}")"

# Render template with safe token substitution (use '|' delimiter)
cat "${PENDING_ITEMS_TEMPLATE}" \
  | sed "s|{project-slug}|${ESCAPED_SLUG}|g" \
  | sed "s|{Project Name}|${ESCAPED_NAME}|g" \
  | sed "s|{PREFIX}|${ESCAPED_PREFIX}|g" \
  > "${PENDING_ITEMS_OUTPUT}"

# Validate file created
if [[ ! -f "${PENDING_ITEMS_OUTPUT}" ]]; then
  validation_error "Failed to create docs/system/pending-items-rules.md"
fi
```

### Step 4: Post-Deployment Validation

**Unresolved Token Check** (explicit pattern matching):
```bash
# Check for unresolved allowed tokens (explicit pattern matching)
# Only 3 tokens for this template: project-slug, Project Name, PREFIX
if grep -E '\{(project-slug|Project Name|PREFIX)\}' "${PENDING_ITEMS_OUTPUT}" >/dev/null 2>&1; then
  UNRESOLVED=$(grep -oE '\{(project-slug|Project Name|PREFIX)\}' "${PENDING_ITEMS_OUTPUT}" | head -1)
  validation_error "Unresolved token in pending-items-rules.md: ${UNRESOLVED}"
fi
```

**File Readability Check**:
```bash
# Validate file readable
if [[ ! -r "${PENDING_ITEMS_OUTPUT}" ]]; then
  validation_error "Cannot read: docs/system/pending-items-rules.md"
fi
```

### Step 5: Dependency Verification

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

---

## Token Sources

All tokens MUST be read from `project.yaml` (source-of-truth):

| Token | Source Field | Read Method | Example Value |
|-------|--------------|-------------|---------------|
| `{project-slug}` | identity.slug | read_yaml_field() | `devotional-generator` |
| `{Project Name}` | identity.name | read_yaml_field() | `Devotional Generator` |
| `{PREFIX}` | identity.prefix | read_yaml_field() | `DG` |

**Consistent with Issue-006/011**: Same source-of-truth enforcement, same read logic.

---

## Validation Strategy

### File Creation Validation

1. **Template existence**: Check template file before rendering
2. **Directory existence**: Verify docs/system/outputs/ exists (created in Issue-006); docs/system/ inferred from outputs/ subdirectory
3. **File creation**: Verify output file exists after rendering
4. **Unresolved tokens**: Explicit grep for allowed token patterns only (3 patterns)
5. **File readability**: Check file permissions

### Content Validation

1. **P-### → {PREFIX}-### mapping**: Template contains mapping table (verified in Issue-001)
2. **Identity source reference**: Template contains link to project.yaml (verified in Issue-001)
3. **Enforcement rules**: Template documents prefix enforcement (verified in Issue-001)

**Note**: Template correctness verified in Issue-001. Issue-008 validates tokens replaced, not template content itself.

### Completion Verification

1. **Dependency artifacts**: Required artifacts from Issues 005, 006, 011 exist
2. **Own artifact created**: pending-items-rules.md successfully deployed
3. **No unresolved tokens**: Explicit token pattern check (3 patterns)
4. **Governance compatibility**: File allowed in docs/system/ (project-specific)

---

## Dependencies

- Issue-005 (project.yaml created and validated) ✅
- Issue-006 (docs/system/outputs/ created, read_yaml_field() function) ✅
- Issue-011 (docs/system/ directory exists) ✅

---

## Files Likely Touched

- `scripts/run-create-project` (extend with pending-items-rules.md deployment)
- `../<project-slug>/docs/system/pending-items-rules.md` (create)

---

## Risks / Failure Modes

- **docs/system/outputs/ directory missing**: Should have been created in Issue-006
  - Mitigation: Explicit outputs/ directory existence check (confirms docs/system/ parent exists)
- **Template content unclear**: What rules to include?
  - Mitigation: Template correctness verified in Issue-001; template documents P-### → {PREFIX}-### mapping per P-084 Section 5.1
- **Prefix substitution inconsistent**: Different logic from previous issues
  - Mitigation: Reuse escape_sed() and rendering logic from Issue-006/011
- **Governance protection conflict**: docs/system/ triggers governance validation
  - Mitigation: P-084 Section 4.1 explicitly allows project-specific files like pending-items-rules.md
- **Runtime enforcement confusion**: Users may expect file to enforce mapping automatically
  - Mitigation: Document clearly that file is reference documentation only, not runtime enforcement

---

## Testing Strategy

### Manual Test Cases

1. **Valid pending-items-rules.md deployment**:
   ```bash
   run-create-project --slug test-rules --name "Test Rules" --prefix TR
   cat ../test-rules/docs/system/pending-items-rules.md
   ```
   Expected: File exists, all tokens replaced, P-### → TR-### mapping documented

2. **Token substitution verification**:
   ```bash
   run-create-project --slug token-rules --name "Token Rules Test" --prefix TK
   grep -E '\{(project-slug|Project Name|PREFIX)\}' ../token-rules/docs/system/pending-items-rules.md
   ```
   Expected: No unresolved allowed token patterns found

3. **Prefix mapping verification**:
   ```bash
   run-create-project --slug map-rules --name "Mapping Rules Test" --prefix MR
   grep 'MR-001' ../map-rules/docs/system/pending-items-rules.md
   grep 'MR-042' ../map-rules/docs/system/pending-items-rules.md
   ```
   Expected: Prefix appears in mapping table examples

4. **Dependency verification**:
   ```bash
   run-create-project --slug deps-rules --name "Dependency Rules Test" --prefix DR
   ls ../deps-rules/project.yaml ../deps-rules/docs/system/outputs/.gitkeep ../deps-rules/docs/system/ai-process.md ../deps-rules/docs/system/pending-items-rules.md
   ```
   Expected: Required dependency artifacts exist (Issues 005, 006, 011) plus own artifact created

5. **Identity source reference**:
   ```bash
   run-create-project --slug source-rules --name "Source Rules Test" --prefix SR
   grep 'project.yaml' ../source-rules/docs/system/pending-items-rules.md
   ```
   Expected: File references project.yaml as identity source

---

## Output Updates

Update success output to include pending-items-rules.md deployment:

```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully
✅ ai-process.md deployed successfully
✅ pending-items-rules.md deployed successfully

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
  ai-process.md:        /Users/me/projects/test-project/docs/system/ai-process.md
  pending-items-rules.md: /Users/me/projects/test-project/docs/system/pending-items-rules.md

Created Directories:
  phases/:              /Users/me/projects/test-project/phases/
  docs/system/outputs/: /Users/me/projects/test-project/docs/system/outputs/

Path Invariants:
  ✅ Sibling structure verified
  ✅ No nesting detected
  ✅ Relative path invariant satisfied

Issue-008 Complete:
  ✅ pending-items-rules.md deployed
  ✅ Namespace mapping documented (P-### → TP-###)
  ✅ Dependency artifacts verified (Issues 005, 006, 011)

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
- Uses docs/system/outputs/ directory created in Issue-006
- Consistent token substitution logic

**Issue-011** (ai-process.md):
- Uses docs/system/ directory existence from Issue-011
- Reuses escaped identity values
- Consistent rendering approach

---

## Namespace Mapping Documentation

**Purpose**: pending-items-rules.md serves as project-specific reference documentation for the P-### → {PREFIX}-### mapping rule defined in P-084 Section 5.1. This file documents the enforcement rules but does not enforce them at runtime.

**Mapping Examples** (template content):
- P-001 → {PREFIX}-001
- P-042 → {PREFIX}-042
- P-999 → {PREFIX}-999

**Enforcement** (template content):
- All project-specific pending items MUST use {PREFIX}-### format
- This project MUST NOT reference automated-builder P-### identifiers directly
- The prefix value is immutable after project creation

**Identity Source** (template content):
- All prefix references derive from project.yaml
- project.yaml is the authoritative source for project identity

---

## References

- Primary Authority: [P-084 Section 10: Issue-008](2026-02-13__01__system__p-084-inventory-approved.md)
- Namespace Conversion: P-084 Section 5.1
- Template: [templates/project/pending-items-rules.md.tmpl](../../../templates/project/pending-items-rules.md.tmpl)
- Dependencies: Issue-005 (project.yaml), Issue-006 (read_yaml_field), Issue-011 (directory)
- Safe Substitution: Issue-005 implementation (escape_sed() function)
