# Issue-003 Proposal — Implement Path Resolution and Validation

**Issue**: Issue-003 — Implement Path Resolution and Validation
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Approved

---

## Objective

Implement P-084 Section 5.2 path resolution invariants to ensure project directory is sibling to automated-builder.

---

## Scope

### In Scope

- ✅ Determine BUILDER_ROOT (git repo root via `git rev-parse --show-toplevel`)
- ✅ Compute PARENT_DIR (from parameter or dirname(BUILDER_ROOT))
- ✅ Compute PROJECT_PATH (PARENT_DIR/project-slug)
- ✅ Canonicalize all paths with `pwd -P` before invariant checks
- ✅ Validate all 6 invariants from Section 5.2 table

### Out of Scope

- ❌ File/directory creation (Issue-005, Issue-006)
- ❌ Post-creation verification (Issue-009)

---

## Acceptance Criteria

- [ ] Locates automated-builder git root via `git rev-parse --show-toplevel`
- [ ] HALT: "Cannot locate automated-builder repository root" if git command fails
- [ ] Canonicalizes BUILDER_ROOT with `pwd -P` to resolve symlinks
- [ ] HALT: "Parent directory does not exist" if PARENT_DIR does not exist
- [ ] HALT: "Parent directory is not writable" if PARENT_DIR lacks write permissions
- [ ] Canonicalizes PARENT_DIR with `pwd -P` before validation
- [ ] Canonicalizes PROJECT_PATH (computed, not created) for comparison
- [ ] HALT: "Project directory already exists" if PROJECT_PATH exists
- [ ] HALT: "Project must be sibling to automated-builder" if dirname mismatch
- [ ] HALT: "Invalid nesting" if either path is prefix of the other
- [ ] HALT: "Relative path invariant violated" if `../automated-builder` doesn't resolve to BUILDER_ROOT
- [ ] All path computations use absolute, canonical paths internally
- [ ] Returns validated PROJECT_PATH on success

---

## Path Resolution Invariants (P-084 Section 5.2)

### Required Invariants

| Invariant | Rule | Example |
|-----------|------|---------|
| Sibling structure | PROJECT_PATH and BUILDER_ROOT share same parent | `/projects/automated-builder` and `/projects/my-project` |
| Relative path determinism | `../automated-builder` from project root MUST resolve to builder root | From `/projects/my-project/`, `../automated-builder/` → `/projects/automated-builder/` |
| No nesting | Project MUST NOT be inside automated-builder or vice versa | ❌ `/projects/automated-builder/my-project/` |
| Absolute paths | All internal path computations use absolute paths | `/Users/me/projects/...` not `../...` |

---

## Implementation Approach

### Resolution Algorithm

Extend `system/scripts/run-create-project.md` with path resolution logic:

```bash
# 1. Determine BUILDER_ROOT using git rev-parse
#    - Use git to find repository root directly (no script directory traversal)
#    - Canonicalize with pwd -P to resolve symlinks

BUILDER_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" ||
  validation_error "Cannot locate automated-builder repository root"

# Canonicalize BUILDER_ROOT (resolve symlinks)
BUILDER_ROOT="$(cd "${BUILDER_ROOT}" && pwd -P)"

# 2. Determine PARENT_DIR
#    - If parent-dir parameter provided: use it directly
#    - If parent-dir parameter omitted: use dirname(BUILDER_ROOT)

PARENT_DIR="${NORMALIZED_PARENT_DIR}"  # from Issue-002

# 3. Validate PARENT_DIR explicitly
#    - Check existence
#    - Check writability
#    - Canonicalize with pwd -P

if [[ ! -d "${PARENT_DIR}" ]]; then
  validation_error "Parent directory does not exist: ${PARENT_DIR}"
fi

if [[ ! -w "${PARENT_DIR}" ]]; then
  validation_error "Parent directory is not writable: ${PARENT_DIR}"
fi

# Canonicalize PARENT_DIR (resolve symlinks)
PARENT_DIR="$(cd "${PARENT_DIR}" && pwd -P)"

# 4. Compute PROJECT_PATH
#    - Compute path (do NOT create directory)
#    - Canonicalize parent for comparison (project itself doesn't exist yet)

PROJECT_PATH="${PARENT_DIR}/${NORMALIZED_SLUG}"

# 5. Check project path doesn't already exist
if [[ -e "${PROJECT_PATH}" ]]; then
  validation_error "Project directory already exists: ${PROJECT_PATH}"
fi

# 6. Verify sibling relationship (using canonicalized paths)
if [[ "$(dirname "${PROJECT_PATH}")" != "$(dirname "${BUILDER_ROOT}")" ]]; then
  validation_error "Project must be sibling to automated-builder. Expected parent: $(dirname "${BUILDER_ROOT}"), got: $(dirname "${PROJECT_PATH}")"
fi

# 7. Check no nesting (using canonicalized paths)
if [[ "${PROJECT_PATH}" == "${BUILDER_ROOT}"* ]]; then
  validation_error "Invalid nesting: project cannot be inside automated-builder"
fi

if [[ "${BUILDER_ROOT}" == "${PROJECT_PATH}"* ]]; then
  validation_error "Invalid nesting: automated-builder cannot be inside project"
fi

# 8. Verify relative path invariant (using canonicalized paths)
RELATIVE_BUILDER_FROM_PROJECT="$(cd "${PARENT_DIR}" && cd automated-builder 2>/dev/null && pwd -P)" ||
  validation_error "Relative path invariant violated: cannot reach automated-builder from parent directory"

if [[ "${RELATIVE_BUILDER_FROM_PROJECT}" != "${BUILDER_ROOT}" ]]; then
  validation_error "Relative path invariant violated: ../automated-builder does not resolve to BUILDER_ROOT (expected: ${BUILDER_ROOT}, got: ${RELATIVE_BUILDER_FROM_PROJECT})"
fi
```

### Validation Checks

All 6 invariant checks from P-084 Section 5.2 (using canonicalized paths):

1. ✅ Builder root exists (detected via `git rev-parse --show-toplevel`)
2. ✅ Parent dir exists and is writable (explicit checks)
3. ✅ No path collision (PROJECT_PATH does not exist)
4. ✅ Sibling relationship (same parent directory, after canonicalization)
5. ✅ No nested paths (neither is prefix of the other, after canonicalization)
6. ✅ Relative path valid (`../automated-builder` resolves to BUILDER_ROOT, canonicalized)

### Output

On successful validation, print:

```
✅ Path resolution successful

Resolved Paths:
  BUILDER_ROOT: /Users/me/projects/automated-builder
  PARENT_DIR:   /Users/me/projects
  PROJECT_PATH: /Users/me/projects/my-project

Path Invariants:
  ✅ Sibling structure verified
  ✅ No nesting detected
  ✅ Relative path invariant satisfied
  ✅ Project path available (does not exist)
```

---

## Dependencies

- Issue-002 (command scaffolding and parameter normalization)

---

## Files Likely Touched

- `system/scripts/run-create-project.md` (extend with path resolution)

---

## Risks / Failure Modes

- **Symbolic link resolution edge cases**: Symlinks in paths could bypass sibling checks
  - Mitigation: Use `pwd -P` (canonical path) after `cd` to resolve symlinks deterministically
- **Cross-platform path handling**: macOS vs Linux path differences
  - Mitigation: Use POSIX-compliant path operations; `pwd -P` is POSIX standard
- **Git not available**: `git rev-parse` requires git to be installed
  - Mitigation: Clear error message if git command fails
- **Permission check reliability**: Write permission check is explicit but may have edge cases
  - Mitigation: Explicit `-w` test before path validation; final verification at file creation in Issue-005
- **Relative path computation errors**: `cd` failures could give false negatives
  - Mitigation: Explicit error handling for all `cd` operations with `2>/dev/null` and `||` checks

---

## Testing Strategy

### Manual Test Cases

1. **Valid sibling structure**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix MP
   ```
   Expected: Success, paths resolved and validated

2. **Custom parent directory**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix MP --parent-dir /tmp/projects
   ```
   Expected: Success if /tmp/projects exists and is writable

3. **Project already exists**:
   ```bash
   mkdir -p ../my-project
   run-create-project --slug my-project --name "My Project" --prefix MP
   ```
   Expected: HALT with "Project directory already exists"

4. **Nested path attempt**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix MP --parent-dir "$(pwd)"
   ```
   Expected: HALT with "Invalid nesting: project cannot be inside automated-builder"

5. **Parent directory does not exist**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix MP --parent-dir /nonexistent
   ```
   Expected: HALT with "Parent directory does not exist or is not writable"

6. **Sibling relationship violation**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix MP --parent-dir /tmp
   ```
   Expected: HALT with "Project must be sibling to automated-builder"

---

## Integration with Issue-002

Issue-003 extends the `run-create-project` script created in Issue-002:

- Reuses normalized parameters from Issue-002 (`NORMALIZED_SLUG`, `NORMALIZED_PARENT_DIR`)
- Adds path resolution logic after parameter normalization
- Validates path invariants before proceeding
- Maintains Issue-002's error handling patterns and exit codes

---

## References

- Primary Authority: [P-084 Section 10: Issue-003](2026-02-13__01__system__p-084-inventory-approved.md)
- Path Resolution Invariants: P-084 Section 5.2
- Integration: Issue-002 (command scaffolding)
