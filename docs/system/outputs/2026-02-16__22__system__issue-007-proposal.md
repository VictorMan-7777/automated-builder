# Issue-007 Proposal — Comprehensive Governance Protection Validation

**Issue**: Issue-007 — Comprehensive Governance Protection Validation
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Proposed

---

## Objective

Implement comprehensive governance file protection per P-084 Section 4.1 with recursive PROJECT_PATH scanning, symbolic link detection, and full governance reference resolution. Extends Issue-009 Check 15 with deeper validation.

---

## Scope

### In Scope

- ✅ Recursive scan of PROJECT_PATH for prohibited patterns
- ✅ Symbolic link detection and traversal protection
- ✅ Hidden file/directory scanning (`.filename`, `.git/`)
- ✅ Full governance reference resolution (realpath validation, not just pattern match)
- ✅ Root-level contract file detection (planning.md, builder.md, gateway.md)
- ✅ Prohibited directory detection (prompts/, templates/, .git/)
- ✅ Extends Issue-009 Check 15 with recursive and symlink protection

### Out of Scope

- ❌ Prevention during creation (validation only, not active blocking)
- ❌ File content validation (structure only)
- ❌ Permission modification (read-only enforcement)

---

## Relationship to Issue-009 Check 15

**Issue-009 Check 15** (already implemented):
- Validates docs/system/ contains only allowed files
- Checks for disallowed patterns in docs/system/
- Pattern-based governance reference validation

**Issue-007** (this proposal):
- **Extends** Issue-009 Check 15 with recursive scanning
- Adds symbolic link detection
- Adds hidden file/directory scanning
- Upgrades governance reference validation from pattern match to realpath resolution
- Scans entire PROJECT_PATH, not just docs/system/

**Integration**: Issue-007 complements Issue-009 Check 15, providing deeper defensive validation.

---

## Acceptance Criteria

**Recursive Scanning**:
- [ ] Scans PROJECT_PATH recursively for prohibited patterns
- [ ] Includes all subdirectories, not just top-level
- [ ] Detects files at any depth in project tree

**Prohibited Patterns Detection**:
- [ ] HALT: "Governance file copied: {path}" if `docs/system/**` found (except `docs/system/outputs/`, `docs/system/ai-process.md`, `docs/system/pending-items-rules.md`)
- [ ] HALT: "Contract file copied: {path}" if `planning.md`, `builder.md`, or `gateway.md` found at root
- [ ] HALT: "Governance directory copied: {path}" if `prompts/**` found anywhere
- [ ] HALT: "Governance directory copied: {path}" if `templates/**` found anywhere
- [ ] HALT: "Git repository copied: {path}" if `.git/**` found anywhere
- [ ] Allows `docs/system/outputs/` subdirectory
- [ ] Allows `docs/system/ai-process.md` (created in Issue-011)
- [ ] Allows `docs/system/pending-items-rules.md` (created in Issue-008)

**Symbolic Link Protection**:
- [ ] Detects symbolic links in PROJECT_PATH
- [ ] HALT: "Symbolic link detected: {path}" if any symlinks found
- [ ] Prevents traversal of symlinks during recursive scan

**Hidden File/Directory Scanning**:
- [ ] Scans for hidden files (`.filename`)
- [ ] Scans for hidden directories (`.git/`, `.github/`)
- [ ] HALT: "Hidden governance directory: {path}" if `.git/` detected

**Governance Reference Resolution**:
- [ ] Validates `builder-manifest.yaml` governance.references paths resolve to `../automated-builder/`
- [ ] Uses realpath for resolution (not just pattern matching)
- [ ] HALT: "Invalid governance reference: {path}" if any reference resolves within PROJECT_PATH
- [ ] HALT: "Governance reference does not resolve to automated-builder: {path}" if realpath not in BUILDER_ROOT

**Dependencies**:
- [ ] Runs after Issue-009 end-to-end validation
- [ ] Reuses BUILDER_ROOT and PROJECT_PATH variables
- [ ] Complements Issue-009 Check 15 (docs/system/ validation)

---

## Implementation Approach

### Step 1: Recursive Prohibited Pattern Scan

**Recursive find with prohibited patterns**:

```bash
# Prohibited patterns (files and directories)
PROHIBITED_PATTERNS=(
  "planning.md"
  "builder.md"
  "gateway.md"
  "prompts"
  "templates"
  ".git"
)

# Recursively scan PROJECT_PATH for prohibited patterns
for pattern in "${PROHIBITED_PATTERNS[@]}"; do
  FOUND_PATHS=$(find "${PROJECT_PATH}" -name "${pattern}" 2>/dev/null || true)

  if [[ -n "${FOUND_PATHS}" ]]; then
    while IFS= read -r found_path; do
      validation_error "Governance file/directory copied: ${found_path}" true
    done <<< "${FOUND_PATHS}"
  fi
done
```

**Rationale**: Find command recursively scans all subdirectories, catching prohibited files at any depth.

### Step 2: docs/system/ Comprehensive Validation

**Extends Issue-009 Check 15 with recursive scan**:

```bash
# Scan docs/system/ for any governance files (except allowed files)
# Allowed: ai-process.md, pending-items-rules.md, outputs/ subdirectory

if [[ -d "${PROJECT_PATH}/docs/system" ]]; then
  # Find all files in docs/system/ (excluding outputs/ subdirectory)
  DOCS_SYSTEM_FILES=$(find "${PROJECT_PATH}/docs/system" -type f -not -path "${PROJECT_PATH}/docs/system/outputs/*" 2>/dev/null || true)

  # Check each file is in allowed list
  while IFS= read -r file_path; do
    file_basename=$(basename "${file_path}")

    if [[ "${file_basename}" != "ai-process.md" && "${file_basename}" != "pending-items-rules.md" ]]; then
      validation_error "Unexpected file in docs/system/: ${file_path}" true
    fi
  done <<< "${DOCS_SYSTEM_FILES}"

  # Find all directories in docs/system/ (except outputs/)
  DOCS_SYSTEM_DIRS=$(find "${PROJECT_PATH}/docs/system" -mindepth 1 -maxdepth 1 -type d -not -name "outputs" 2>/dev/null || true)

  if [[ -n "${DOCS_SYSTEM_DIRS}" ]]; then
    while IFS= read -r dir_path; do
      validation_error "Unexpected directory in docs/system/: ${dir_path}" true
    done <<< "${DOCS_SYSTEM_DIRS}"
  fi
fi
```

### Step 3: Symbolic Link Detection

**Scan for symbolic links**:

```bash
# Find all symbolic links in PROJECT_PATH
SYMLINKS=$(find "${PROJECT_PATH}" -type l 2>/dev/null || true)

if [[ -n "${SYMLINKS}" ]]; then
  while IFS= read -r symlink_path; do
    validation_error "Symbolic link detected: ${symlink_path}" true
  done <<< "${SYMLINKS}"
fi
```

**Rationale**: Symbolic links could bypass governance protection by linking to automated-builder governance files. Reject any symlinks in project.

### Step 4: Hidden Directory Scanning

**Scan for hidden directories**:

```bash
# Find hidden directories (starting with .)
HIDDEN_DIRS=$(find "${PROJECT_PATH}" -type d -name ".*" 2>/dev/null || true)

# Filter for governance-related hidden directories
GOVERNANCE_HIDDEN_DIRS=""
while IFS= read -r hidden_dir; do
  dir_basename=$(basename "${hidden_dir}")

  # Check for governance-related hidden directories
  if [[ "${dir_basename}" == ".git" ]]; then
    GOVERNANCE_HIDDEN_DIRS+="${hidden_dir}"$'\n'
  fi
done <<< "${HIDDEN_DIRS}"

if [[ -n "${GOVERNANCE_HIDDEN_DIRS}" ]]; then
  while IFS= read -r gov_hidden_dir; do
    validation_error "Hidden governance directory: ${gov_hidden_dir}" true
  done <<< "${GOVERNANCE_HIDDEN_DIRS}"
fi
```

**Rationale**: `.git/` directory would indicate git repository copied, not initialized fresh. Detect and reject.

### Step 5: Governance Reference Resolution (Realpath Validation)

**Upgrade from pattern match to realpath resolution**:

```bash
# Extract governance.references paths from builder-manifest.yaml
# (Already extracted in Issue-009 Check 7)
GOVERNANCE_REFS=$(grep -A 10 "^  references:" "${PROJECT_PATH}/builder-manifest.yaml" | grep "    -" | sed 's/.*- //' || echo "")

if [[ -z "${GOVERNANCE_REFS}" ]]; then
  validation_error "No governance references found in builder-manifest.yaml" true
fi

# Verify each reference resolves to BUILDER_ROOT (using realpath)
while IFS= read -r ref_path; do
  # Resolve path relative to PROJECT_PATH
  RESOLVED_PATH=$(cd "${PROJECT_PATH}" && realpath "${ref_path}" 2>/dev/null || echo "")

  if [[ -z "${RESOLVED_PATH}" ]]; then
    validation_error "Cannot resolve governance reference: ${ref_path}" true
  fi

  # Check if resolved path is within BUILDER_ROOT
  if [[ ! "${RESOLVED_PATH}" =~ ^${BUILDER_ROOT} ]]; then
    validation_error "Governance reference does not resolve to automated-builder: ${ref_path} (resolved to: ${RESOLVED_PATH})" true
  fi

  # Check if resolved path is within PROJECT_PATH (should NOT be)
  if [[ "${RESOLVED_PATH}" =~ ^${PROJECT_PATH} ]]; then
    validation_error "Invalid governance reference resolves within project: ${ref_path}" true
  fi
done <<< "${GOVERNANCE_REFS}"
```

**Rationale**: Realpath resolution catches edge cases that pattern matching misses (relative paths, symlinks, etc.).

### Step 6: Integration with Issue-009

**Execution order**:
1. Issue-009 runs all 15 validation checks (including Check 15: docs/system/ basic validation)
2. Issue-007 runs comprehensive governance protection validation
3. Both share validation_error function with cleanup capability

**No duplication**: Issue-007 extends Issue-009 Check 15, not replaces it.

---

## Validation Strategy

### Defensive Layers

**Layer 1** (Issue-009 Check 15):
- Basic docs/system/ validation
- Pattern-based governance reference check
- Non-recursive

**Layer 2** (Issue-007):
- Recursive PROJECT_PATH scan
- Symbolic link detection
- Hidden directory scanning
- Realpath governance reference resolution

**Benefits**: Multi-layer defense catches edge cases and manual file additions.

### Find Command Safety

**Potential issues**:
- Large directory trees (performance)
- Permission errors (unreadable directories)
- Special characters in filenames

**Mitigations**:
- Use `2>/dev/null` to suppress permission errors
- Use `|| true` to prevent find errors from halting script
- Quote variables to handle special characters

---

## Dependencies

- Issue-009 (end-to-end validation, Check 15 basic docs/system/ validation) ✅

**Integration**: Issue-007 runs after Issue-009 as additional governance protection layer.

---

## Files Likely Touched

- `scripts/run-create-project` (add comprehensive governance protection validation)

**No new files created**: Issue-007 is validation-only.

---

## Risks / Failure Modes

- **Symbolic link traversal could bypass detection**:
  - Mitigation: Explicit symlink detection with `-type l` check
  - Reject any symlinks found in PROJECT_PATH

- **Hidden files (`.filename`) might not be scanned**:
  - Mitigation: Find command scans hidden files by default
  - Explicit check for governance-related hidden directories (`.git/`)

- **Case-insensitive filesystems (macOS) create ambiguity**:
  - Mitigation: Use exact pattern matching, not case-insensitive
  - Pattern list includes both lowercase and expected case

- **Relative path resolution edge cases**:
  - Mitigation: Use realpath for canonical path resolution
  - Verify resolved path not within PROJECT_PATH

- **Performance on large directory trees**:
  - Mitigation: Scope find to PROJECT_PATH only (not entire filesystem)
  - Bootstrap projects are small (10 files, 2 directories)

- **find command errors halt script**:
  - Mitigation: Use `|| true` to prevent errors from halting
  - Use `2>/dev/null` to suppress permission errors

---

## Testing Strategy

### Manual Test Cases

1. **Valid project (no prohibited files)**:
   ```bash
   run-create-project --slug test-gov --name "Test Governance" --prefix TG
   # Expected: All validation checks pass, no governance violations
   ```

2. **Prohibited file at root (planning.md)**:
   ```bash
   run-create-project --slug bad-planning --name "Bad Planning" --prefix BP
   # Manually create planning.md at root
   # Expected: HALT with "Contract file copied: planning.md", cleanup triggered
   ```

3. **Prohibited directory (prompts/)**:
   ```bash
   run-create-project --slug bad-prompts --name "Bad Prompts" --prefix BP
   # Manually create prompts/ directory
   # Expected: HALT with "Governance directory copied: prompts/", cleanup triggered
   ```

4. **Hidden governance directory (.git/)**:
   ```bash
   run-create-project --slug bad-git --name "Bad Git" --prefix BG
   # Manually create .git/ directory
   # Expected: HALT with "Hidden governance directory: .git/", cleanup triggered
   ```

5. **Symbolic link in project**:
   ```bash
   run-create-project --slug bad-symlink --name "Bad Symlink" --prefix BS
   # Manually create symbolic link: ln -s ../automated-builder/docs/system/planning.md symlink.md
   # Expected: HALT with "Symbolic link detected: symlink.md", cleanup triggered
   ```

6. **Invalid governance reference (resolves to PROJECT_PATH)**:
   ```bash
   run-create-project --slug bad-ref-project --name "Bad Ref Project" --prefix BR
   # Manually edit builder-manifest.yaml to use ./docs/system/planning.md
   # Expected: HALT with "Invalid governance reference resolves within project", cleanup triggered
   ```

7. **Nested prohibited file (deep in tree)**:
   ```bash
   run-create-project --slug nested-bad --name "Nested Bad" --prefix NB
   # Manually create nested/path/to/templates/file.tmpl
   # Expected: HALT with "Governance directory copied: nested/path/to/templates", cleanup triggered
   ```

8. **Unexpected file in docs/system/**:
   ```bash
   run-create-project --slug extra-docs --name "Extra Docs" --prefix ED
   # Manually create docs/system/planning.md
   # Expected: HALT with "Unexpected file in docs/system/: planning.md", cleanup triggered
   ```

---

## Output Updates

No output changes. Issue-007 validation is silent on success, errors trigger cleanup with specific messages.

**Example error output**:
```
Running end-to-end validation checks...
✅ All validation checks passed

Running comprehensive governance protection validation...
❌ Validation Error: Governance file copied: /Users/me/projects/test-project/prompts/
🧹 Cleaning up partial project directory: /Users/me/projects/test-project
✅ Cleanup complete
```

---

## Integration with Previous Issues

**Issue-009** (end-to-end validation):
- Issue-007 runs after Issue-009 as additional governance protection layer
- Reuses validation_error function with cleanup capability
- Extends Check 15 (docs/system/ validation) with recursive scanning
- Upgrades Check 7 (governance reference validation) with realpath resolution

**Issue-006, Issue-008, Issue-011** (file creation):
- Issue-007 validates no additional files created beyond bootstrap artifacts
- Ensures only expected files exist in PROJECT_PATH

---

## Prohibited Patterns Reference

Per P-084 Section 4.1, the following patterns are prohibited in PROJECT_PATH:

| Pattern | Location | Rationale |
|---------|----------|-----------|
| `planning.md` | Root | Contract file (governance) |
| `builder.md` | Root | Contract file (governance) |
| `gateway.md` | Root | Contract file (governance) |
| `prompts/` | Anywhere | Governance directory |
| `templates/` | Anywhere | Governance directory |
| `.git/` | Anywhere | Git repository (should be initialized, not copied) |
| `docs/system/**` | docs/system/ | Governance docs (except outputs/, ai-process.md, pending-items-rules.md) |

**Allowed exceptions**:
- `docs/system/outputs/` — Output artifacts directory (created in Issue-006)
- `docs/system/ai-process.md` — AI Process Contract (created in Issue-011)
- `docs/system/pending-items-rules.md` — Project-specific rules (created in Issue-008)

---

## References

- Primary Authority: [P-084 Section 10: Issue-007](2026-02-13__01__system__p-084-inventory-approved.md)
- Governance Protection: P-084 Section 4.1
- Dependencies: Issue-009 (end-to-end validation)
- Integration: Extends Issue-009 Check 15 with recursive scanning
