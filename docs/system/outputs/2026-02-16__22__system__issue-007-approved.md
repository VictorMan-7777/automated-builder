# Issue-007 Proposal — Comprehensive Governance Protection Validation

**Issue**: Issue-007 — Comprehensive Governance Protection Validation
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Approved
**Date**: 2026-02-16
**Status**: Approved

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

## Relationship to Issue-009

**Issue-009 Baseline** (already implemented, single source of truth):
- **Check 7**: Governance references start with `../automated-builder/` (pattern-based)
- **Check 15**: docs/system/ contains only allowed files (non-recursive, top-level only)

**Issue-007 Extensions** (this proposal, extends Issue-009 only):
- **Extends Check 7**: Upgrades governance reference validation from pattern match to canonical path resolution
- **Extends Check 15**: Adds recursive scanning, symbolic link detection, hidden directory scanning
- **Scans entire PROJECT_PATH**: Not just docs/system/, catches violations at any depth
- **No duplicate validation**: Issue-007 does NOT re-implement Issue-009 checks, only extends them

**Integration**: Issue-007 runs after Issue-009 as additional defensive layer. Issue-009 remains source of truth for baseline validation.

---

## Acceptance Criteria

**Recursive Scanning**:
- [ ] Scans PROJECT_PATH recursively for prohibited patterns
- [ ] Includes all subdirectories, not just top-level
- [ ] Detects files at any depth in project tree

**Prohibited Patterns Detection**:
- [ ] Collect violations (avoid noisy multi-HALTs)
- [ ] HALT deterministically with single cleanup after collecting all violations
- [ ] Contract files: Check root level only (`-maxdepth 1 -type f`) for planning.md, builder.md, gateway.md
- [ ] Governance directories: Check recursively (`-type d`) for prompts/, templates/, .git/
- [ ] HALT: "Governance file copied: {path}" if `docs/system/**` found (except `docs/system/outputs/`, `docs/system/ai-process.md`, `docs/system/pending-items-rules.md`)
- [ ] Allows `docs/system/outputs/` subdirectory
- [ ] Allows `docs/system/ai-process.md` (created in Issue-011)
- [ ] Allows `docs/system/pending-items-rules.md` (created in Issue-008)

**Symbolic Link Protection**:
- [ ] Detects symbolic links in PROJECT_PATH recursively
- [ ] Collects violations (avoid noisy multi-HALTs)
- [ ] HALT deterministically with single cleanup if symlinks found
- [ ] Prevents traversal of symlinks during recursive scan

**Hidden File/Directory Scanning**:
- [ ] Hidden directories covered by prohibited directory patterns (`.git/` in PROHIBITED_DIRS)
- [ ] No separate hidden directory scan needed (already covered in Step 1)

**Governance Reference Resolution**:
- [ ] Extends Issue-009 Check 7 (pattern validation) with canonical path resolution
- [ ] Uses indent-aware awk extractor for governance.references (does not truncate lists)
- [ ] Uses portable realpath resolver (realpath command or python3 fallback)
- [ ] Collects violations in per-step buffer (deterministic)
- [ ] HALT deterministically with single cleanup after merging all step buffers
- [ ] HALT: "Invalid governance reference resolves within project: {path}" if resolves to PROJECT_PATH
- [ ] HALT: "Governance reference does not resolve to automated-builder: {path}" if not in BUILDER_ROOT

**Dependencies**:
- [ ] Runs after Issue-009 end-to-end validation
- [ ] Reuses BUILDER_ROOT and PROJECT_PATH variables
- [ ] Complements Issue-009 Check 15 (docs/system/ validation)

---

## Implementation Approach

### Step 1: Recursive Prohibited Pattern Scan

**Collect violations, then HALT deterministically (single cleanup)**:

```bash
# Prohibited file patterns (contract files at root)
PROHIBITED_FILES=(
  "planning.md"
  "builder.md"
  "gateway.md"
)

# Prohibited directory patterns (governance directories anywhere)
PROHIBITED_DIRS=(
  "prompts"
  "templates"
  ".git"
)

# Step 1 violations buffer (deterministic per-step collection)
STEP1_VIOLATIONS=""

# Scan for prohibited files (contract files should not exist at root)
for pattern in "${PROHIBITED_FILES[@]}"; do
  FOUND_PATHS=$(find "${PROJECT_PATH}" -maxdepth 1 -type f -name "${pattern}" 2>/dev/null || true)

  if [[ -n "${FOUND_PATHS}" ]]; then
    while IFS= read -r found_path; do
      STEP1_VIOLATIONS+="Contract file copied: ${found_path}"$'\n'
    done <<< "${FOUND_PATHS}"
  fi
done

# Scan for prohibited directories (governance directories anywhere in tree)
for pattern in "${PROHIBITED_DIRS[@]}"; do
  FOUND_PATHS=$(find "${PROJECT_PATH}" -type d -name "${pattern}" 2>/dev/null || true)

  if [[ -n "${FOUND_PATHS}" ]]; then
    while IFS= read -r found_path; do
      STEP1_VIOLATIONS+="Governance directory copied: ${found_path}"$'\n'
    done <<< "${FOUND_PATHS}"
  fi
done
```

**Rationale**:
- Per-step violation buffer (STEP1_VIOLATIONS) for deterministic collection
- Collect all violations before HALTing (avoid noisy multi-HALTs)
- Restrict directory patterns to `-type d` (not `-type f`)
- Contract files checked at root only (`-maxdepth 1`)
- Governance directories checked recursively (any depth)

### Step 2: docs/system/ Comprehensive Validation

**Extends Issue-009 Check 15 with recursive scan (collect violations, HALT once)**:

```bash
# Scan docs/system/ for any governance files (except allowed files)
# Allowed: ai-process.md, pending-items-rules.md, outputs/ subdirectory
# Issue-009 Check 15 already validates top-level; Issue-007 adds recursive depth

# Step 2 violations buffer (deterministic per-step collection)
STEP2_VIOLATIONS=""

if [[ -d "${PROJECT_PATH}/docs/system" ]]; then
  # Find all files in docs/system/ recursively (excluding outputs/ subdirectory)
  DOCS_SYSTEM_FILES=$(find "${PROJECT_PATH}/docs/system" -type f -not -path "${PROJECT_PATH}/docs/system/outputs/*" 2>/dev/null || true)

  # Check each file is in allowed list
  while IFS= read -r file_path; do
    file_basename=$(basename "${file_path}")

    if [[ "${file_basename}" != "ai-process.md" && "${file_basename}" != "pending-items-rules.md" ]]; then
      STEP2_VIOLATIONS+="Unexpected file in docs/system/: ${file_path}"$'\n'
    fi
  done <<< "${DOCS_SYSTEM_FILES}"

  # Find all directories in docs/system/ recursively (except outputs/ and its subdirectories)
  DOCS_SYSTEM_DIRS=$(find "${PROJECT_PATH}/docs/system" -mindepth 1 -type d -not -path "${PROJECT_PATH}/docs/system/outputs" -not -path "${PROJECT_PATH}/docs/system/outputs/*" 2>/dev/null || true)

  if [[ -n "${DOCS_SYSTEM_DIRS}" ]]; then
    while IFS= read -r dir_path; do
      STEP2_VIOLATIONS+="Unexpected directory in docs/system/: ${dir_path}"$'\n'
    done <<< "${DOCS_SYSTEM_DIRS}"
  fi
fi
```

### Step 3: Symbolic Link Detection

**Scan for symbolic links (collect, then HALT if violations found)**:

```bash
# Step 3 violations buffer (deterministic per-step collection)
STEP3_VIOLATIONS=""

# Find all symbolic links in PROJECT_PATH
SYMLINKS=$(find "${PROJECT_PATH}" -type l 2>/dev/null || true)

if [[ -n "${SYMLINKS}" ]]; then
  while IFS= read -r symlink_path; do
    STEP3_VIOLATIONS+="Symbolic link detected: ${symlink_path}"$'\n'
  done <<< "${SYMLINKS}"
fi
```

**Rationale**: Symbolic links could bypass governance protection by linking to automated-builder governance files. Per-step buffer for deterministic collection.

### Step 4: Hidden Directory Scanning

**Scan for hidden governance directories (already covered in Step 1)**:

```bash
# Note: .git/ already covered in Step 1 (PROHIBITED_DIRS)
# No additional hidden directory scanning needed
```

**Rationale**: `.git/` directory covered by Step 1 prohibited directory scan with `-type d -name ".git"`. No duplicate scanning needed.

### Step 5: Governance Reference Resolution (Canonical Path Validation)

**Upgrade from pattern match to canonical path resolution using portable resolver**:

```bash
# Portable realpath function (python3 fallback)
portable_realpath() {
  local path="$1"
  local base_dir="$2"

  # Try realpath command first (most portable)
  if command -v realpath >/dev/null 2>&1; then
    (cd "${base_dir}" && realpath "${path}" 2>/dev/null || echo "")
  else
    # Fallback to python3 (always available on macOS/Linux)
    python3 -c "import os,sys; print(os.path.realpath(os.path.join(sys.argv[1], sys.argv[2])))" "${base_dir}" "${path}" 2>/dev/null || echo ""
  fi
}

# Extract governance.references paths from builder-manifest.yaml
# (Issue-009 Check 7 already validates pattern, Issue-007 validates resolved paths)
# Use indent-aware awk extractor (does not truncate lists like grep -A 10)
GOVERNANCE_REFS=$(awk '
  /^governance:/ { in_governance=1; next }
  /^[a-z_]+:/ { if (in_governance) in_governance=0 }
  in_governance && /^  references:/ { in_references=1; next }
  in_governance && /^  [a-z_]+:/ { if (in_references) in_references=0 }
  in_references && /^    - / { gsub(/^    - /, ""); print }
' "${PROJECT_PATH}/builder-manifest.yaml" || echo "")

if [[ -z "${GOVERNANCE_REFS}" ]]; then
  validation_error "No governance references found in builder-manifest.yaml" true
fi

# Step 5 violations buffer (deterministic per-step collection)
STEP5_VIOLATIONS=""

# Verify each reference resolves to BUILDER_ROOT (using portable realpath)
while IFS= read -r ref_path; do
  # Resolve path relative to PROJECT_PATH
  RESOLVED_PATH=$(portable_realpath "${ref_path}" "${PROJECT_PATH}")

  if [[ -z "${RESOLVED_PATH}" ]]; then
    STEP5_VIOLATIONS+="Cannot resolve governance reference: ${ref_path}"$'\n'
    continue
  fi

  # Check if resolved path is within BUILDER_ROOT
  if [[ ! "${RESOLVED_PATH}" =~ ^${BUILDER_ROOT} ]]; then
    STEP5_VIOLATIONS+="Governance reference does not resolve to automated-builder: ${ref_path} (resolved to: ${RESOLVED_PATH})"$'\n'
  fi

  # Check if resolved path is within PROJECT_PATH (should NOT be)
  if [[ "${RESOLVED_PATH}" =~ ^${PROJECT_PATH} ]]; then
    STEP5_VIOLATIONS+="Invalid governance reference resolves within project: ${ref_path}"$'\n'
  fi
done <<< "${GOVERNANCE_REFS}"
```

**Rationale**:
- Portable realpath: Use `realpath` command if available, fallback to `python3` (always available)
- Indent-aware awk extractor: Does not truncate lists (unlike `grep -A 10`)
- Per-step violation buffer (STEP5_VIOLATIONS) for deterministic collection
- Canonical path resolution catches edge cases pattern matching misses
- Issue-009 Check 7 validates pattern (baseline), Issue-007 validates resolved paths (extension)

### Step 6: Merge Violations and HALT Deterministically

**Merge per-step buffers and HALT once with all violations**:

```bash
# Merge all per-step violation buffers
ALL_VIOLATIONS=""
ALL_VIOLATIONS+="${STEP1_VIOLATIONS}"
ALL_VIOLATIONS+="${STEP2_VIOLATIONS}"
ALL_VIOLATIONS+="${STEP3_VIOLATIONS}"
ALL_VIOLATIONS+="${STEP5_VIOLATIONS}"

# HALT deterministically with all violations if any found
if [[ -n "${ALL_VIOLATIONS}" ]]; then
  echo "Governance protection violations detected:" >&2
  echo "${ALL_VIOLATIONS}" >&2
  validation_error "Governance protection validation failed (see violations above)" true
fi

echo "✅ Comprehensive governance protection validation passed"
```

**Rationale**:
- Deterministic violation collection (per-step buffers merged once)
- Single HALT with all violations (avoid noisy multi-HALTs)
- Single cleanup operation (consistent with validation_error logic)
- Clear violation report (all issues shown together)

### Step 7: Integration with Issue-009

**Execution order**:
1. Issue-009 runs all 15 validation checks (baseline validation)
   - Check 7: Governance references pattern validation (baseline)
   - Check 15: docs/system/ top-level validation (baseline)
2. Issue-007 runs comprehensive governance protection validation (extensions only)
   - Extends Check 7: Canonical path resolution of governance references
   - Extends Check 15: Recursive docs/system/ scanning
   - Adds: Prohibited pattern scanning (entire PROJECT_PATH)
   - Adds: Symbolic link detection
3. Both share validation_error function with cleanup capability

**No duplication**: Issue-007 extends Issue-009, does not re-implement baseline checks. Issue-009 remains single source of truth for baseline validation.

---

## Validation Strategy

### Defensive Layers (Issue-007 extends Issue-009)

**Baseline** (Issue-009):
- **Check 7**: Pattern-based governance reference validation (single source of truth)
- **Check 15**: Top-level docs/system/ validation (single source of truth)

**Extensions** (Issue-007):
- **Extends Check 7**: Canonical path resolution of governance references (portable realpath)
- **Extends Check 15**: Recursive docs/system/ scanning
- **Adds**: Full PROJECT_PATH prohibited pattern scan
- **Adds**: Symbolic link detection
- **Adds**: Contract file detection at root

**Benefits**: Multi-layer defense catches edge cases and manual file additions. Issue-009 remains source of truth, Issue-007 adds depth.

### Portable Realpath Resolution

**Approach**: Deterministic, portable resolver with explicit dependency.

**Implementation**:
```bash
portable_realpath() {
  if command -v realpath >/dev/null 2>&1; then
    (cd "${base_dir}" && realpath "${path}" 2>/dev/null || echo "")
  else
    python3 -c "import os,sys; print(os.path.realpath(...))" "${base_dir}" "${path}" 2>/dev/null || echo ""
  fi
}
```

**Benefits**:
- Primary: Use `realpath` command (most portable, available on Linux/macOS/BSD)
- Fallback: Use `python3` (always available on macOS/Linux)
- Deterministic: Same resolution on all platforms
- No external dependencies: realpath or python3 (both standard)

### Deterministic HALT Behavior

**Approach**: Per-step violation buffers merged once before HALT.

**Benefits**:
- Deterministic per-step collection (isolated buffers, predictable order)
- Avoid noisy multi-HALTs (single error message with all violations)
- Single cleanup operation (deterministic)
- Clear violation report (all issues shown together)
- Consistent with validation_error cleanup logic

**Pattern**:
```bash
# Step-specific buffers
STEP1_VIOLATIONS=""
STEP2_VIOLATIONS=""
STEP3_VIOLATIONS=""
STEP5_VIOLATIONS=""

# ... collect violations per step ...

# Merge all buffers
ALL_VIOLATIONS=""
ALL_VIOLATIONS+="${STEP1_VIOLATIONS}"
ALL_VIOLATIONS+="${STEP2_VIOLATIONS}"
ALL_VIOLATIONS+="${STEP3_VIOLATIONS}"
ALL_VIOLATIONS+="${STEP5_VIOLATIONS}"

# HALT once with all violations
if [[ -n "${ALL_VIOLATIONS}" ]]; then
  echo "Governance protection violations detected:" >&2
  echo "${ALL_VIOLATIONS}" >&2
  validation_error "Governance protection validation failed (see violations above)" true
fi
```

### Find Command Safety

**Potential issues**:
- Large directory trees (performance)
- Permission errors (unreadable directories)
- Special characters in filenames

**Mitigations**:
- Use `2>/dev/null` to suppress permission errors
- Use `|| true` to prevent find errors from halting script
- Quote variables to handle special characters
- Restrict directory patterns to `-type d` (not `-type f`)
- Restrict contract file patterns to `-maxdepth 1` (root only)

---

## Dependencies

- Issue-009 (end-to-end validation, Check 15 basic docs/system/ validation) ✅

**Integration**: Issue-007 runs after Issue-009 as additional governance protection layer.

---

## Files Likely Touched

- `system/scripts/run-create-project.md` (add comprehensive governance protection validation)

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

**Issue-009** (end-to-end validation - baseline, single source of truth):
- Issue-007 runs after Issue-009 as additional governance protection layer
- Reuses validation_error function with cleanup capability
- **Extends Check 7**: Upgrades governance reference validation from pattern match to canonical path resolution
- **Extends Check 15**: Adds recursive docs/system/ scanning (Issue-009 validates top-level only)
- **No duplication**: Issue-009 remains source of truth for baseline validation

**Issue-006, Issue-008, Issue-011** (file creation):
- Issue-007 validates no additional files created beyond bootstrap artifacts
- Ensures only expected files exist in PROJECT_PATH (recursive verification)

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
