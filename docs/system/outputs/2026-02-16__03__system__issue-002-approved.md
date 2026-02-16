# Issue-002 Proposal — Implement run-create-project Command Scaffolding

**Issue**: Issue-002 — Implement run-create-project Command Scaffolding
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Approved

---

## Objective

Create command entry point with parameter parsing and normalization per P-084 Section 5.

---

## Scope

### In Scope

- ✅ Command-line interface (bash script)
- ✅ Parameter parsing (project-slug, project-name, prefix, parent-dir)
- ✅ Input normalization (flexible interpretation, format conversion)
- ✅ Input validation (basic sanity checks only)
- ✅ Help/usage text

### Out of Scope

- ❌ Path resolution logic (Issue-003)
- ❌ Prefix derivation algorithm (Issue-004)
- ❌ File creation
- ❌ Strict artifact validation (happens at write time in Issue-005, Issue-006, Issue-011)

---

## Acceptance Criteria

- [ ] Command `run-create-project` exists and is executable
- [ ] Parameter: `project-slug` (required, normalized to `^[a-z][a-z0-9-]*[a-z0-9]$`)
  - Accept flexible input: "My-Project", "my_project", "MY PROJECT" → normalize to "my-project"
- [ ] Parameter: `project-name` (required, non-empty string, whitespace trimmed)
- [ ] Parameter: `prefix` (required, normalized to `^[A-Z]{1,4}$`)
  - Accept flexible input: "dg", "Dg", "DG" → normalize to "DG"
  - HALT only if normalized result invalid (e.g., "12DG", "DGXYZ5")
  - Prefix derivation is OUT OF SCOPE (deferred to Issue-004)
- [ ] Optional parameter: `parent-dir` (absolute path, defaults to dirname(BUILDER_ROOT))
- [ ] HALT: "Missing required parameter: --prefix" if prefix omitted
- [ ] HALT: "Invalid slug format after normalization" if project-slug cannot be normalized to valid format
- [ ] HALT: "Invalid prefix format after normalization" if prefix cannot be normalized to valid format
- [ ] Help text documents all parameters, formats, and normalization behavior
- [ ] Normalizes and validates parameters but creates NO files yet
- [ ] Strict format validation deferred to artifact-write time (Issue-005, Issue-006, Issue-011)

---

## Implementation Approach

### Command Location

Create bash script at: `scripts/run-create-project`

### BUILDER_ROOT Definition

`BUILDER_ROOT` = absolute path to the automated-builder repository root directory (the directory containing `.git/`, `templates/`, `prompts/`, etc.).

NOT the umbrella projects directory that contains multiple project repositories.

Example:
- BUILDER_ROOT: `/Users/me/projects/automated-builder`
- Parent directory (umbrella): `/Users/me/projects`

### Parameter Interface

```bash
run-create-project \
  --slug <project-slug> \
  --name "<Project Name>" \
  --prefix <PREFIX> \
  [--parent-dir <path>]
```

### Normalization Logic

1. **Slug normalization**:
   - Convert to lowercase
   - Replace underscores and spaces with hyphens
   - Remove leading/trailing hyphens
   - Validate final format: `^[a-z][a-z0-9-]*[a-z0-9]$`

2. **Name normalization**:
   - Trim leading/trailing whitespace
   - Normalize internal whitespace to single spaces
   - Validate non-empty

3. **Prefix normalization**:
   - Convert to uppercase
   - Trim whitespace
   - Validate final format: `^[A-Z]{1,4}$`

4. **Parent-dir normalization**:
   - Default: `dirname(BUILDER_ROOT)` where BUILDER_ROOT is the automated-builder repository root
   - If provided: expand to absolute path
   - Verify existence (basic check only, full validation in Issue-003)

### Error Handling

- Clear, actionable error messages
- Exit codes: 0 (success), 1 (validation error), 2 (usage error)
- No file creation on error

### Output

On successful validation:
- Print normalized parameter values
- Exit 0 (but do NOT create files yet)

---

## Dependencies

- Issue-001 (templates must exist for future steps)

---

## Files Likely Touched

- `scripts/run-create-project` (create)

---

## Risks / Failure Modes

- Parameter parsing ambiguity (mitigate: clear help text, examples)
- Unclear error messages (mitigate: actionable messages with examples)
- Platform-specific compatibility (mitigate: use POSIX-compliant bash)
- Normalization inconsistency (mitigate: unit tests for edge cases)

---

## Testing Strategy

### Manual Test Cases

1. **Valid minimal invocation**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix MP
   ```
   Expected: Success, normalized values printed

2. **Normalization tests**:
   ```bash
   run-create-project --slug "My_Cool-App" --name "My Cool App" --prefix "dg"
   ```
   Expected: slug → "my-cool-app", prefix → "DG"

3. **Missing required parameter**:
   ```bash
   run-create-project --slug my-project --name "My Project"
   ```
   Expected: HALT with "Missing required parameter: --prefix"

4. **Invalid slug after normalization**:
   ```bash
   run-create-project --slug "123-project" --name "My Project" --prefix MP
   ```
   Expected: HALT with "Invalid slug format after normalization"

5. **Invalid prefix after normalization**:
   ```bash
   run-create-project --slug my-project --name "My Project" --prefix "12DG"
   ```
   Expected: HALT with "Invalid prefix format after normalization"

6. **Help invocation**:
   ```bash
   run-create-project --help
   ```
   Expected: Full usage text with examples

---

## References

- Primary Authority: [P-084 Section 10: Issue-002](2026-02-13__01__system__p-084-inventory-approved.md)
- Input Parameters: P-084 Section 5 (Input Parameters and Resolution Rules)
- Normalization vs Enforcement: P-084 Section "Input Normalization vs Artifact Enforcement"
