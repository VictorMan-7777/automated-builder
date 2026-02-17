# Issue-009 Proposal — End-to-End Validation and Bootstrap Verification

**Issue**: Issue-009 — End-to-End Validation and Bootstrap Verification
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Approved
**Date**: 2026-02-16
**Status**: Approved

---

## Objective

Implement comprehensive end-to-end validation of bootstrapped project structure per P-084 Section 6 validation contract. Execute 15 validation checks after all bootstrap files created, with cleanup on failure.

---

## Scope

### In Scope

- ✅ Execute all 15 validation checks from P-084 Section 6
- ✅ YAML syntax validation for project.yaml and builder-manifest.yaml
- ✅ Semantic validation (identity values, consistency, path resolution)
- ✅ Post-creation verification (all files exist, no empty files)
- ✅ Cleanup partial artifacts on any validation failure
- ✅ Success confirmation message with project path
- ✅ Consolidate incremental validations into final comprehensive check

### Out of Scope

- ❌ Git initialization (explicit non-goal per P-084 Section 7)
- ❌ Running planner automatically (explicit non-goal per P-084 Section 7)
- ❌ Template content validation (verified in Issue-001)
- ❌ Re-implementation of checks already performed (reuse existing validation functions)

---

## Acceptance Criteria

**Validation Checks** (P-084 Section 6):

- [ ] **Check 1**: Project directory exists at `${PROJECT_PATH}`
- [ ] **Check 2**: project.yaml created FIRST and passes all Section 2.4 validation (8 checks)
- [ ] **Check 3**: All P-084 bootstrap artifacts exist (per P-084 Section 3):
  - project.yaml
  - index.md, prd.md, roadmap.md, iteration-log.md
  - builder-manifest.yaml
  - phases/.gitkeep
  - docs/system/outputs/.gitkeep
  - docs/system/ai-process.md
  - docs/system/pending-items-rules.md
- [ ] **Check 4**: All files contain valid content (no empty files, minimum size check)
- [ ] **Check 5**: builder-manifest.yaml is valid YAML with required fields
- [ ] **Check 6**: builder-manifest.yaml contains `identity_source: ../project.yaml` reference
- [ ] **Check 7**: All governance reference paths in manifest resolve to `../automated-builder/`
- [ ] **Check 8**: phases/ directory exists and contains only .gitkeep (no other files)
- [ ] **Check 9**: docs/system/outputs/ directory exists and contains only .gitkeep (no other files)
- [ ] **Check 10**: All placeholder values resolved from project.yaml (identity values match)
- [ ] **Check 11**: No unresolved placeholders remain in any file (explicit token pattern check)
- [ ] **Check 12**: All references to slug/name/prefix/created match project.yaml exactly (consistency check)
- [ ] **Check 13**: Prefix determined and set in project.yaml (identity.prefix non-empty)
- [ ] **Check 14**: Path resolution invariants satisfied (sibling structure, relative path valid)
- [ ] **Check 15**: No governance files duplicated (docs/system/ contains only allowed files)

**Cleanup on Failure**:
- [ ] On ANY validation failure: delete `${PROJECT_PATH}` recursively
- [ ] HALT: "{specific error message}" with cleanup confirmation
- [ ] Cleanup guards against incorrect PROJECT_PATH (verify path contains project-slug)

**Success Output**:
- [ ] On success: output "✅ All validation checks passed"
- [ ] On success: output "Project created: {PROJECT_PATH}"
- [ ] On success: output "Identity file: {PROJECT_PATH}/project.yaml"
- [ ] Does NOT initialize git repository
- [ ] Does NOT run planner automatically

**Dependencies**:
- [ ] Verifies artifacts from Issues 005, 006, 008, 011 exist
- [ ] Reuses validation functions (read_yaml_field, token pattern detection)

---

## P-084 Section 6 Validation Contract

### 15 Validation Checks (Consolidated)

| Check | Validation | Failure Message | Already Implemented? |
|-------|------------|----------------|---------------------|
| 1 | Project directory exists | "Project directory does not exist: {PROJECT_PATH}" | Partial (created in Issue-005) |
| 2 | project.yaml valid | "Identity file validation failed" | Yes (Issue-005) |
| 3 | All 10 files exist | "Required file missing: {file}" | Partial (Issues 006, 008, 011) |
| 4 | No empty files | "Empty file detected: {file}" | **New** |
| 5 | builder-manifest.yaml valid YAML | "Invalid YAML in builder-manifest.yaml" | **New (YAML parsing)** |
| 6 | identity_source reference | "Missing identity_source in builder-manifest.yaml" | **New** |
| 7 | Governance paths resolve | "Invalid governance reference: {path}" | **New** |
| 8 | phases/ contains only .gitkeep | "Unexpected files in phases/: {files}" | **New** |
| 9 | outputs/ contains only .gitkeep | "Unexpected files in docs/system/outputs/: {files}" | **New** |
| 10 | Values from project.yaml | "Inconsistent identity value in {file}" | Partial (token substitution) |
| 11 | No unresolved tokens | "Unresolved token in {file}: {token}" | Yes (Issues 006, 008, 011) |
| 12 | Consistency check | "Inconsistency detected: {detail}" | **New** |
| 13 | Prefix set | "Prefix not set in project.yaml" | Yes (Issue-005) |
| 14 | Path invariants | "Path resolution invariant violated" | Partial (pre-creation check) |
| 15 | No governance duplication | "Governance file copied: {path}" | **New** |

**New validations in Issue-009**: Checks 4, 5, 6, 7, 8, 9, 12, 15
**Existing validations to consolidate**: Checks 1, 2, 3, 10, 11, 13, 14

---

## Implementation Approach

### Step 1: YAML Syntax Validation

**New functionality**: Parse YAML files to confirm syntax validity.

```bash
# Validate project.yaml is parseable YAML
if ! yq eval '.' "${PROJECT_PATH}/project.yaml" >/dev/null 2>&1; then
  validation_error "Invalid YAML syntax in project.yaml"
fi

# Validate builder-manifest.yaml is parseable YAML
if ! yq eval '.' "${PROJECT_PATH}/builder-manifest.yaml" >/dev/null 2>&1; then
  validation_error "Invalid YAML syntax in builder-manifest.yaml"
fi
```

**Rationale**: YAML syntax validation deferred from Issues 005 and 006. Issue-009 validates YAML is parseable.

### Step 2: File Existence and Content Checks

**Consolidate existing checks + add new ones**:

```bash
# Check 3: All P-084 bootstrap artifacts exist (reuse from previous issues)
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
  "docs/system/pending-items-rules.md"
)

for file in "${ALL_REQUIRED_FILES[@]}"; do
  if [[ ! -f "${PROJECT_PATH}/${file}" ]]; then
    validation_error "Required file missing: ${file}"
  fi
done

# Check 4: No empty files (NEW)
for file in "${ALL_REQUIRED_FILES[@]}"; do
  # .gitkeep files are allowed to be empty
  if [[ "${file}" == *".gitkeep" ]]; then
    continue
  fi

  if [[ ! -s "${PROJECT_PATH}/${file}" ]]; then
    validation_error "Empty file detected: ${file}"
  fi
done
```

### Step 3: Semantic Validation (identity_source, governance paths)

**New functionality**: Validate builder-manifest.yaml references.

```bash
# Check 6: builder-manifest.yaml contains identity_source reference (NEW)
if ! grep -q "identity_source:.*project.yaml" "${PROJECT_PATH}/builder-manifest.yaml"; then
  validation_error "Missing identity_source reference in builder-manifest.yaml"
fi

# Check 7: Governance reference paths resolve to ../automated-builder/ (NEW)
# Extract governance.references paths from builder-manifest.yaml
GOVERNANCE_REFS=$(yq eval '.governance.references[]' "${PROJECT_PATH}/builder-manifest.yaml" 2>/dev/null || echo "")

if [[ -z "${GOVERNANCE_REFS}" ]]; then
  validation_error "No governance references found in builder-manifest.yaml"
fi

# Verify each reference resolves to automated-builder directory
while IFS= read -r ref_path; do
  # Resolve path relative to PROJECT_PATH
  RESOLVED_PATH=$(cd "${PROJECT_PATH}" && realpath "${ref_path}" 2>/dev/null || echo "")

  # Check if resolved path is within BUILDER_ROOT
  if [[ ! "${RESOLVED_PATH}" =~ ^${BUILDER_ROOT} ]]; then
    validation_error "Invalid governance reference (does not resolve to automated-builder): ${ref_path}"
  fi
done <<< "${GOVERNANCE_REFS}"
```

### Step 4: Directory Content Validation

**New functionality**: Verify directories contain only expected files.

```bash
# Check 8: phases/ contains only .gitkeep (NEW)
PHASES_CONTENTS=$(ls -A "${PROJECT_PATH}/phases/" 2>/dev/null | grep -v "^\.gitkeep$" || true)
if [[ -n "${PHASES_CONTENTS}" ]]; then
  validation_error "Unexpected files in phases/: ${PHASES_CONTENTS}"
fi

# Check 9: docs/system/outputs/ contains only .gitkeep (NEW)
OUTPUTS_CONTENTS=$(ls -A "${PROJECT_PATH}/docs/system/outputs/" 2>/dev/null | grep -v "^\.gitkeep$" || true)
if [[ -n "${OUTPUTS_CONTENTS}" ]]; then
  validation_error "Unexpected files in docs/system/outputs/: ${OUTPUTS_CONTENTS}"
fi
```

### Step 5: Consistency Check (Cross-File Identity Validation)

**New functionality**: Verify all files use consistent identity values.

```bash
# Check 12: Consistency check — all identity references match project.yaml (NEW)
# Read identity values from project.yaml (source-of-truth)
IDENTITY_SLUG=$(read_yaml_field "${PROJECT_PATH}/project.yaml" "slug")
IDENTITY_NAME=$(read_yaml_field "${PROJECT_PATH}/project.yaml" "name")
IDENTITY_PREFIX=$(read_yaml_field "${PROJECT_PATH}/project.yaml" "prefix")
IDENTITY_CREATED=$(read_yaml_field "${PROJECT_PATH}/project.yaml" "created")

# Verify identity values appear correctly in other files
# Check builder-manifest.yaml references project.yaml (already validated in Check 6)
# Check ai-process.md contains correct prefix (already validated in Issue-011)
# Check pending-items-rules.md contains correct prefix

# Verify project-slug appears in index.md
if ! grep -q "${IDENTITY_SLUG}" "${PROJECT_PATH}/index.md"; then
  validation_error "Inconsistency detected: project-slug missing in index.md"
fi

# Verify PREFIX appears in pending-items-rules.md (reuse anchored check from Issue-008)
if ! grep -q "${IDENTITY_PREFIX}" "${PROJECT_PATH}/docs/system/pending-items-rules.md"; then
  validation_error "Inconsistency detected: prefix missing in pending-items-rules.md"
fi

# Additional consistency checks as needed
```

### Step 6: Governance File Duplication Check

**New functionality**: Verify no governance files copied into project.

```bash
# Check 15: No governance files duplicated (NEW)
# docs/system/ should contain ONLY:
#   - ai-process.md (allowed, created in Issue-011)
#   - pending-items-rules.md (allowed, created in Issue-008)
#   - outputs/ subdirectory (allowed, created in Issue-006)

# Scan docs/system/ for disallowed files
DISALLOWED_PATTERNS=(
  "planning.md"
  "builder.md"
  "gateway.md"
  "git.md"
  "issue-resolution.md"
  "prompts"
  "templates"
)

for pattern in "${DISALLOWED_PATTERNS[@]}"; do
  if [[ -e "${PROJECT_PATH}/docs/system/${pattern}" ]]; then
    validation_error "Governance file copied: docs/system/${pattern}"
  fi
done

# Verify docs/system/ contains only allowed files
DOCS_SYSTEM_CONTENTS=$(ls -A "${PROJECT_PATH}/docs/system/" 2>/dev/null | grep -v "^ai-process.md$" | grep -v "^pending-items-rules.md$" | grep -v "^outputs$" || true)
if [[ -n "${DOCS_SYSTEM_CONTENTS}" ]]; then
  validation_error "Unexpected files in docs/system/: ${DOCS_SYSTEM_CONTENTS}"
fi
```

### Step 7: Cleanup on Failure

**New functionality**: Delete PROJECT_PATH recursively on validation failure.

```bash
# Cleanup function (called by validation_error if validation fails)
cleanup_on_failure() {
  local error_msg="$1"

  echo "❌ Validation failed: ${error_msg}"

  # Safety check: verify PROJECT_PATH contains project-slug before deletion
  if [[ ! "${PROJECT_PATH}" =~ /${IDENTITY_SLUG}$ ]]; then
    echo "⚠️  WARNING: PROJECT_PATH does not end with project-slug. Skipping cleanup to prevent data loss."
    echo "⚠️  PROJECT_PATH: ${PROJECT_PATH}"
    echo "⚠️  IDENTITY_SLUG: ${IDENTITY_SLUG}"
    exit 1
  fi

  # Safety check: verify PROJECT_PATH is not automated-builder
  if [[ "${PROJECT_PATH}" == "${BUILDER_ROOT}" ]]; then
    echo "⚠️  CRITICAL: PROJECT_PATH matches BUILDER_ROOT. Aborting cleanup."
    exit 1
  fi

  # Delete PROJECT_PATH recursively
  if [[ -d "${PROJECT_PATH}" ]]; then
    echo "🧹 Cleaning up partial project directory: ${PROJECT_PATH}"
    rm -rf "${PROJECT_PATH}"
    echo "✅ Cleanup complete"
  fi

  exit 1
}

# Update validation_error function to call cleanup_on_failure
validation_error() {
  local msg="$1"
  cleanup_on_failure "${msg}"
}
```

### Step 8: Success Confirmation Output

**New functionality**: Enhanced success output after all validations pass.

```bash
# After all 15 validation checks pass
echo ""
echo "✅ All validation checks passed"
echo ""
echo "Project created: ${PROJECT_PATH}"
echo "Identity file: ${PROJECT_PATH}/project.yaml"
echo ""
echo "Bootstrap Complete:"
echo "  ✅ All P-084 bootstrap artifacts deployed"
echo "  ✅ YAML syntax validation passed"
echo "  ✅ Identity consistency verified"
echo "  ✅ Governance protection verified"
echo "  ✅ Ready for project planning and building"
echo ""
echo "Note: Git initialization is manual (per P-084 Section 7)"
echo "      Run 'git init' in project directory when ready"
```

---

## Validation Strategy

### Incremental vs End-to-End

**Incremental validations** (already implemented in Issues 005, 006, 008, 011):
- Token substitution validation (explicit pattern detection)
- File creation validation (file exists, readable)
- Anchored line validation (ai-process.md prefix check)
- Dependency artifact verification

**End-to-end validations** (new in Issue-009):
- YAML syntax parsing (yq eval)
- Semantic validation (identity_source, governance paths)
- Consistency check (cross-file identity values)
- Directory content validation (only expected files)
- Governance duplication check (disallowed files)
- Empty file detection
- Cleanup on failure

**Integration approach**: Issue-009 consolidates incremental validations into comprehensive final check, adds new semantic validations, and implements cleanup on failure.

### YAML Parsing Tools

**Tool selection**: Use `yq` for YAML parsing and validation.

**Installation check**:
```bash
# Verify yq available
if ! command -v yq >/dev/null 2>&1; then
  validation_error "yq not installed (required for YAML validation). Install: brew install yq"
fi
```

**Alternative**: If yq not available, use python3 with yaml module as fallback.

---

## Token Sources

All tokens already resolved in Issues 005, 006, 008, 011. Issue-009 validates tokens resolved correctly.

| Token | Source Field | Already Validated By | Issue-009 Check |
|-------|--------------|---------------------|-----------------|
| `{project-slug}` | identity.slug | Issue-006 | Consistency check |
| `{Project Name}` | identity.name | Issue-006 | Consistency check |
| `{PREFIX}` | identity.prefix | Issues 008, 011 | Consistency check |
| `{YYYY-MM-DD}` | identity.created | Issue-006 | Consistency check |

**Issue-009 focus**: Cross-file consistency validation, not token substitution.

---

## Dependencies

- Issue-005 (project.yaml created and validated) ✅
- Issue-006 (remaining bootstrap files, read_yaml_field() function) ✅
- Issue-008 (pending-items-rules.md deployed) ✅
- Issue-011 (ai-process.md deployed) ✅

**Issue-009 consolidates**: All prior issue validations into comprehensive end-to-end check.

---

## Files Likely Touched

- `system/scripts/run-create-project.md` (add end-to-end validation function, cleanup logic)

**No new files created**: Issue-009 is validation-only.

---

## Risks / Failure Modes

- **yq not installed**: YAML parsing requires yq tool
  - Mitigation: Check for yq installation, provide clear error with installation instructions
  - Alternative: Fallback to python3 yaml module if yq unavailable

- **Cleanup too aggressive**: Incorrect PROJECT_PATH calculation could delete wrong directory
  - Mitigation: Safety checks before deletion (verify path contains project-slug, not BUILDER_ROOT)
  - Guard against edge cases (symlinks, relative paths)

- **Validation order matters**: Some checks depend on others (e.g., file must exist before checking content)
  - Mitigation: Order checks logically (existence → content → syntax → semantics)

- **Governance path resolution edge cases**: Relative paths, symlinks, case-insensitive filesystems
  - Mitigation: Use realpath for resolution, test on macOS (case-insensitive)

- **Incremental validations duplicated**: Some checks already performed in prior issues
  - Mitigation: Reuse existing validation functions, consolidate rather than duplicate

- **Empty .gitkeep files flagged**: .gitkeep files are expected to be empty
  - Mitigation: Explicitly skip .gitkeep files in empty file check

---

## Testing Strategy

### Manual Test Cases

1. **Valid bootstrap (happy path)**:
   ```bash
   run-create-project --slug test-validate --name "Test Validate" --prefix TV
   # Expected: All 15 validation checks pass, success output
   ```

2. **Invalid YAML syntax**:
   ```bash
   run-create-project --slug bad-yaml --name "Bad YAML" --prefix BY
   # Manually corrupt project.yaml or builder-manifest.yaml
   # Expected: HALT with "Invalid YAML syntax" message, cleanup triggered
   ```

3. **Missing required file**:
   ```bash
   run-create-project --slug missing-file --name "Missing File" --prefix MF
   # Manually delete one required file (e.g., index.md)
   # Expected: HALT with "Required file missing: index.md", cleanup triggered
   ```

4. **Empty file detection**:
   ```bash
   run-create-project --slug empty-file --name "Empty File" --prefix EF
   # Manually create empty index.md
   # Expected: HALT with "Empty file detected: index.md", cleanup triggered
   ```

5. **Governance file duplication**:
   ```bash
   run-create-project --slug gov-dup --name "Governance Duplication" --prefix GD
   # Manually copy planning.md into docs/system/
   # Expected: HALT with "Governance file copied: docs/system/planning.md", cleanup triggered
   ```

6. **Inconsistent identity values**:
   ```bash
   run-create-project --slug inconsistent --name "Inconsistent" --prefix IC
   # Manually edit index.md to use wrong project-slug
   # Expected: HALT with "Inconsistency detected", cleanup triggered
   ```

7. **Unexpected files in phases/**:
   ```bash
   run-create-project --slug extra-phase --name "Extra Phase" --prefix EP
   # Manually create phases/phase-01.md
   # Expected: HALT with "Unexpected files in phases/", cleanup triggered
   ```

8. **Invalid governance reference**:
   ```bash
   run-create-project --slug bad-ref --name "Bad Reference" --prefix BR
   # Manually edit builder-manifest.yaml to use invalid governance reference
   # Expected: HALT with "Invalid governance reference", cleanup triggered
   ```

---

## Output Updates

Update success output to include validation confirmation:

```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully
✅ ai-process.md deployed successfully
✅ pending-items-rules.md deployed successfully
✅ All validation checks passed

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

Validation Summary:
  ✅ YAML syntax validation passed
  ✅ Identity consistency verified
  ✅ Governance protection verified
  ✅ All required files exist and non-empty
  ✅ Directory structure validated
  ✅ Path resolution invariants satisfied

Bootstrap Complete:
  ✅ All P-084 bootstrap artifacts deployed
  ✅ Ready for project planning and building

Project created: /Users/me/projects/test-project
Identity file: /Users/me/projects/test-project/project.yaml

Note: Git initialization is manual (per P-084 Section 7)
      Run 'git init' in project directory when ready
```

---

## Integration with Previous Issues

**Issue-001** (templates):
- Validates templates rendered correctly (no unresolved tokens)

**Issue-005** (project.yaml):
- Validates project.yaml is parseable YAML (new)
- Validates identity values set correctly (reuse)
- Validates prefix determined (reuse)

**Issue-006** (remaining bootstrap files):
- Validates all 5 files + 2 directories exist (consolidate)
- Validates read_yaml_field() returns consistent values (reuse)
- Validates no unresolved tokens (consolidate)

**Issue-008** (pending-items-rules.md):
- Validates pending-items-rules.md exists (consolidate)
- Validates prefix appears correctly (reuse)

**Issue-011** (ai-process.md):
- Validates ai-process.md exists (consolidate)
- Validates prefix anchored line (reuse)

**Issue-009 adds**:
- YAML syntax validation
- Semantic validation (identity_source, governance paths)
- Consistency check (cross-file identity values)
- Directory content validation
- Governance duplication check
- Empty file detection
- Cleanup on failure

---

## References

- Primary Authority: [P-084 Section 10: Issue-009](2026-02-13__01__system__p-084-inventory-approved.md)
- Validation Contract: P-084 Section 6 (15 checks)
- Dependencies: Issue-005 (project.yaml), Issue-006 (files), Issue-008 (rules), Issue-011 (ai-process)
- YAML Parsing: yq tool (https://github.com/mikefarah/yq)
