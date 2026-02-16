# Issue-011 Proposal — Deploy ai-process.md and Enforce AI Process Contract

**Issue**: Issue-011 — Deploy ai-process.md and Enforce AI Process Contract
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Proposed

---

## Objective

Deploy `docs/system/ai-process.md` from template and enforce P-084 Section 4.2 AI Process Contract guarantees.

---

## Scope

### In Scope

- ✅ Render `ai-process.md.tmpl` using identity values from deployed `project.yaml`
- ✅ Create `PROJECT_PATH/docs/system/ai-process.md`
- ✅ Validate ai-process contract content for required language:
  - Human input flexibility language
  - Artifact-write-time enforcement language
  - Deterministic lookup of most recent inventory-proposal
- ✅ Apply Section 4.2 post-deployment validation checks
- ✅ Reuse token substitution logic from Issue-006

### Out of Scope

- ❌ Governance artifact-type policy updates (Issue-010)
- ❌ Git initialization (explicit non-goal per P-084 Section 7)
- ❌ YAML syntax and semantic validation (deferred to Issue-009)

---

## Acceptance Criteria

**Source-of-Truth Reading**:
- [ ] Reads identity values from `PROJECT_PATH/project.yaml` (NOT from raw CLI input)
- [ ] Uses same read_yaml_field() function from Issue-006 (bounded awk extraction)

**File Creation**:
- [ ] Creates `PROJECT_PATH/docs/system/ai-process.md` from template with all tokens resolved
- [ ] Directory `PROJECT_PATH/docs/system/` already exists from Issue-006
- [ ] File permissions are readable (minimum 644)

**Content Validation** (P-084 Section 4.2 requirements):
- [ ] ai-process.md explicitly states human input is flexible and normalizable
- [ ] ai-process.md explicitly states enforcement occurs at artifact-write time
- [ ] ai-process.md explicitly requires deterministic selection of most recent inventory-proposal artifact
- [ ] ai-process.md contains project-specific prefix reference (`{PREFIX}` token replaced)

**Post-Deployment Validation**:
- [ ] HALT: "Required file missing: docs/system/ai-process.md" if deployment fails
- [ ] HALT: "Unresolved placeholders in ai-process.md" if allowed token patterns remain (`{project-slug}`, `{Project Name}`, `{PREFIX}`, `{YYYY-MM-DD}`)
- [ ] HALT: "Prefix not set in ai-process.md" if project-specific prefix is missing
- [ ] File readable: HALT: "Cannot read: docs/system/ai-process.md" if permissions invalid

**Completion Verification**:
- [ ] Combined with Issue-006 outputs, all 9 required bootstrap files exist:
  - project.yaml (Issue-005)
  - index.md, prd.md, roadmap.md, iteration-log.md, builder-manifest.yaml (Issue-006)
  - phases/.gitkeep, docs/system/outputs/.gitkeep (Issue-006)
  - docs/system/ai-process.md (Issue-011)

---

## P-084 Section Requirements

### Section 4.2 — AI Process Contract

**Purpose**: Establish project-specific AI interaction rules governing how AI agents process human input and enforce artifact constraints.

**Deployment**: `docs/system/ai-process.md` deployed from `automated-builder/templates/project/ai-process.md.tmpl`.

**Content Requirements** (must be present in deployed file):

1. **Human Input Flexibility**:
   - Human input is flexible by design; conversational and informal phrasing is valid input
   - Conversational instructions, shorthand, and format variations are accepted
   - Format variations are normalized, not rejected
   - If intent is understood, proceed with normalization
   - If intent is ambiguous, ask clarifying questions

2. **Artifact Enforcement Timing**:
   - Enforcement applies at **artifact-write time** only
   - Rule enforcement applies at **artifact-write time** only
   - File outputs must conform strictly to rules when committed to disk
   - Validation failures HALT execution when writing to system artifacts
   - Input parsing and normalization do NOT trigger HALT conditions

3. **Inventory-Proposal Validation Protocol**:
   - Validation MUST locate the most recent inventory-proposal for the target item ID
   - Deterministically locate the most recent inventory-proposal artifact in `docs/system/outputs/`
   - Filename pattern: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal.md`
   - Deterministic selection: Highest date (YYYY-MM-DD), then highest sequence number (NN)

4. **Enforcement Scope**:
   - Rule files enforce: structure, identifiers, ordering, invariants
   - Enforcement targets: files written to project directories, committed artifacts
   - Non-enforcement: conversational responses, exploratory questions, human input parsing

**Template Placeholders**:

| Token | Source | Example Value |
|-------|--------|---------------|
| `{project-slug}` | project.yaml: identity.slug | `devotional-generator` |
| `{Project Name}` | project.yaml: identity.name | `Devotional Generator` |
| `{PREFIX}` | project.yaml: identity.prefix | `DG` |
| `{YYYY-MM-DD}` | project.yaml: identity.created | `2026-02-16` |

**Contract Validation** (Section 4.2 table):

| Check | Acceptance Criteria | Failure Behavior |
|-------|---------------------|------------------|
| File exists | `docs/system/ai-process.md` exists | HALT: "Required file missing: docs/system/ai-process.md" |
| File readable | File has read permissions | HALT: "Cannot read: docs/system/ai-process.md" |
| Placeholders resolved | No unresolved `{...}` tokens remain | HALT: "Unresolved placeholders in ai-process.md" |
| Prefix present | File contains project-specific prefix reference | HALT: "Prefix not set in ai-process.md" |

---

## Implementation Approach

### Step 1: Read Identity Values (Reuse from Issue-006)

Issue-011 reuses the same read_yaml_field() and identity extraction logic from Issue-006:

```bash
# Read identity values from project.yaml (source-of-truth)
# read_yaml_field() function already defined in Issue-006

PROJECT_YAML="${PROJECT_PATH}/project.yaml"

# Extract identity values (reuse from Issue-006)
IDENTITY_SLUG="$(read_yaml_field "${PROJECT_YAML}" "slug")"
IDENTITY_NAME="$(read_yaml_field "${PROJECT_YAML}" "name")"
IDENTITY_PREFIX="$(read_yaml_field "${PROJECT_YAML}" "prefix")"
IDENTITY_CREATED="$(read_yaml_field "${PROJECT_YAML}" "created")"

# Values already validated in Issue-006 (non-empty checks)
```

### Step 2: Render ai-process.md Template

Reuse render_template() function from Issue-006 or create inline rendering:

```bash
# Template path
AI_PROCESS_TEMPLATE="${BUILDER_ROOT}/templates/project/ai-process.md.tmpl"
AI_PROCESS_OUTPUT="${PROJECT_PATH}/docs/system/ai-process.md"

# Verify template exists
if [[ ! -f "${AI_PROCESS_TEMPLATE}" ]]; then
  validation_error "Template not found: ${AI_PROCESS_TEMPLATE}"
fi

# Verify docs/system/ directory exists (created in Issue-006)
if [[ ! -d "${PROJECT_PATH}/docs/system" ]]; then
  validation_error "docs/system/ directory missing (should have been created in Issue-006)"
fi

# Escape values for safe sed substitution (reuse from Issue-005/006)
ESCAPED_SLUG="$(escape_sed "${IDENTITY_SLUG}")"
ESCAPED_NAME="$(escape_sed "${IDENTITY_NAME}")"
ESCAPED_PREFIX="$(escape_sed "${IDENTITY_PREFIX}")"
ESCAPED_CREATED="$(escape_sed "${IDENTITY_CREATED}")"

# Render template with safe token substitution (use '|' delimiter)
cat "${AI_PROCESS_TEMPLATE}" \
  | sed "s|{project-slug}|${ESCAPED_SLUG}|g" \
  | sed "s|{Project Name}|${ESCAPED_NAME}|g" \
  | sed "s|{PREFIX}|${ESCAPED_PREFIX}|g" \
  | sed "s|{YYYY-MM-DD}|${ESCAPED_CREATED}|g" \
  > "${AI_PROCESS_OUTPUT}"

# Validate file created
if [[ ! -f "${AI_PROCESS_OUTPUT}" ]]; then
  validation_error "Failed to create docs/system/ai-process.md"
fi
```

### Step 3: Post-Deployment Validation

**Unresolved Token Check** (explicit pattern matching):
```bash
# Check for unresolved allowed tokens (explicit pattern matching)
if grep -E '\{(project-slug|Project Name|PREFIX|YYYY-MM-DD)\}' "${AI_PROCESS_OUTPUT}" >/dev/null 2>&1; then
  UNRESOLVED=$(grep -oE '\{(project-slug|Project Name|PREFIX|YYYY-MM-DD)\}' "${AI_PROCESS_OUTPUT}" | head -1)
  validation_error "Unresolved placeholders in ai-process.md: ${UNRESOLVED}"
fi
```

**Prefix Presence Check**:
```bash
# Verify prefix is present in file (not just template token replaced)
if ! grep -q "${IDENTITY_PREFIX}" "${AI_PROCESS_OUTPUT}"; then
  validation_error "Prefix not set in ai-process.md"
fi
```

**File Readability Check**:
```bash
# Validate file readable
if [[ ! -r "${AI_PROCESS_OUTPUT}" ]]; then
  validation_error "Cannot read: docs/system/ai-process.md"
fi
```

### Step 4: Final File Count Verification

```bash
# Verify all 9 required bootstrap files exist
REQUIRED_FILES=(
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

for file in "${REQUIRED_FILES[@]}"; do
  if [[ ! -f "${PROJECT_PATH}/${file}" ]]; then
    validation_error "Required file missing: ${file}"
  fi
done

echo "✅ ai-process.md deployed successfully"
echo "✅ All 9 required bootstrap files exist"
```

---

## Token Sources

All tokens MUST be read from `project.yaml` (source-of-truth):

| Token | Source Field | Read Method | Example Value |
|-------|--------------|-------------|---------------|
| `{project-slug}` | identity.slug | read_yaml_field() | `devotional-generator` |
| `{Project Name}` | identity.name | read_yaml_field() | `Devotional Generator` |
| `{PREFIX}` | identity.prefix | read_yaml_field() | `DG` |
| `{YYYY-MM-DD}` | identity.created | read_yaml_field() | `2026-02-16` |

**Consistent with Issue-006**: Same source-of-truth enforcement, same read logic.

---

## Validation Strategy

### File Creation Validation

1. **Template existence**: Check template file before rendering
2. **Directory existence**: Verify docs/system/ exists (created in Issue-006)
3. **File creation**: Verify output file exists after rendering
4. **Unresolved tokens**: Explicit grep for allowed token patterns only
5. **Prefix presence**: Verify PREFIX value appears in rendered file
6. **File readability**: Check file permissions

### Content Validation (Section 4.2 Requirements)

Issue-011 validates that the template contains required contract language by checking rendered output:

1. **Human input flexibility**: Template contains "flexible, interpretive, and may be informal"
2. **Artifact-write-time enforcement**: Template contains "artifact-write time"
3. **Inventory-proposal protocol**: Template contains "deterministically locate"

**Note**: Template correctness verified in Issue-001. Issue-011 validates tokens replaced, not template content itself.

### Completion Verification

1. **9-file count**: All required bootstrap files exist
2. **No unresolved tokens**: Explicit token pattern check
3. **Prefix present**: grep for actual prefix value in file

---

## Dependencies

- Issue-005 (project.yaml created and validated) ✅
- Issue-006 (docs/system/outputs/ created, read_yaml_field() function) ✅

---

## Files Likely Touched

- `scripts/run-create-project` (extend with ai-process.md deployment)
- `../<project-slug>/docs/system/ai-process.md` (create)

---

## Risks / Failure Modes

- **ai-process.md generated with stale values**: File reads from project.yaml (not CLI parameters)
  - Mitigation: Use read_yaml_field() from Issue-006
- **Contract language drift from Section 4.2**: Template may not match P-084 requirements
  - Mitigation: Template correctness verified in Issue-001; Issue-011 validates tokens only
- **Token substitution incomplete**: Unresolved tokens remain
  - Mitigation: Explicit token pattern validation (5 patterns)
- **docs/system/ directory missing**: Should have been created in Issue-006
  - Mitigation: Explicit directory existence check before rendering

---

## Testing Strategy

### Manual Test Cases

1. **Valid ai-process.md deployment**:
   ```bash
   run-create-project --slug test-ai --name "Test AI Process" --prefix TA
   cat ../test-ai/docs/system/ai-process.md
   ```
   Expected: File exists, all tokens replaced, prefix "TA" appears

2. **Token substitution verification**:
   ```bash
   run-create-project --slug token-ai --name "Token AI Test" --prefix TK
   grep -E '\{(project-slug|Project Name|PREFIX|YYYY-MM-DD)\}' ../token-ai/docs/system/ai-process.md
   ```
   Expected: No unresolved allowed token patterns found

3. **Prefix presence check**:
   ```bash
   run-create-project --slug prefix-ai --name "Prefix AI Test" --prefix PA
   grep 'PA' ../prefix-ai/docs/system/ai-process.md
   ```
   Expected: Prefix value appears in file (not just token replaced)

4. **9-file verification**:
   ```bash
   run-create-project --slug complete-ai --name "Complete AI Test" --prefix CA
   find ../complete-ai -type f | wc -l
   ```
   Expected: 9 files total (including .gitkeep files)

5. **Contract content verification**:
   ```bash
   run-create-project --slug contract-ai --name "Contract AI Test" --prefix CT
   grep -i "flexible, interpretive" ../contract-ai/docs/system/ai-process.md
   grep -i "artifact-write time" ../contract-ai/docs/system/ai-process.md
   grep -i "deterministically locate" ../contract-ai/docs/system/ai-process.md
   ```
   Expected: All required contract language present

---

## Output Updates

Update success output to include ai-process.md deployment:

```
✅ Parameter validation successful
✅ Path resolution successful
✅ project.yaml created (YAML validation deferred to Issue-009)
✅ All bootstrap files created successfully
✅ ai-process.md deployed successfully
✅ All 9 required bootstrap files exist

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

Created Directories:
  phases/:              /Users/me/projects/test-project/phases/
  docs/system/outputs/: /Users/me/projects/test-project/docs/system/outputs/

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
- Template validated for correct token syntax

**Issue-005** (project.yaml):
- Reads identity values from project.yaml created in Issue-005
- Reuses escape_sed() function for safe token substitution

**Issue-006** (remaining bootstrap files):
- Reuses read_yaml_field() function from Issue-006
- Uses docs/system/outputs/ directory created in Issue-006
- Consistent token substitution logic

---

## References

- Primary Authority: [P-084 Section 10: Issue-011](2026-02-13__01__system__p-084-inventory-approved.md)
- AI Process Contract: P-084 Section 4.2
- Template: [templates/project/ai-process.md.tmpl](../../../templates/project/ai-process.md.tmpl)
- Dependencies: Issue-005 (project.yaml), Issue-006 (read_yaml_field, directory)
- Safe Substitution: Issue-005 implementation (escape_sed() function)
