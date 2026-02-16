# Issue-004 Proposal — Verify Prefix Determination (Required by Default)

**Issue**: Issue-004 — Verify Prefix Determination (Required by Default)
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Approved

---

## Objective

Verify that prefix determination implementation satisfies P-084 Section 5.1 namespace conversion contract with required prefix input (no automatic derivation).

---

## Context

**Issue-002 already implemented**:
- Required `--prefix` parameter (no derivation)
- Prefix normalization (uppercase conversion, whitespace trimming)
- Prefix validation (`^[A-Z]{1,4}$` format)

**P-084 original scope for Issue-004**:
- Validate explicit prefix format ✅ (done in Issue-002)
- Optional derivation algorithm ❌ (removed from scope per Issue-002 simplification)
- Storage in project.yaml ❌ (deferred to Issue-005)

**This Issue-004 proposal scope**:
- Verify Issue-002 implementation satisfies P-084 Section 5.1 requirements
- Document prefix determination contract
- Confirm no gaps in validation

---

## Scope

**VERIFICATION-ONLY**: No code changes. No changes outside docs/system/outputs (and any required references).

### In Scope

- ✅ Verify explicit prefix format validation (`^[A-Z]{1,4}$`)
- ✅ Verify prefix normalization (uppercase conversion, whitespace trimming)
- ✅ Document prefix determination contract per P-084 Section 5.1
- ✅ Confirm HALT behavior when prefix is invalid
- ✅ Create verification documentation artifact only

### Out of Scope

- ❌ Code changes to scripts/run-create-project (verification only)
- ❌ Prefix derivation algorithm (removed from scope, not implemented)
- ❌ Storage in project.yaml (Issue-005)
- ❌ Collision detection (no prefix registry exists)

---

## Acceptance Criteria

- [ ] Verify `--prefix` parameter is required (HALT if omitted)
- [ ] Verify prefix normalization converts to uppercase
- [ ] Verify prefix normalization trims whitespace
- [ ] Verify prefix validation enforces `^[A-Z]{1,4}$` format
- [ ] Verify HALT: "Missing required parameter: --prefix" if prefix omitted
- [ ] Verify HALT: "Invalid prefix format after normalization" if format invalid
- [ ] Document prefix determination contract per P-084 Section 5.1
- [ ] Confirm no automatic derivation occurs (explicit requirement)

---

## Verification Approach

### Code Review

Review `scripts/run-create-project` to confirm:

1. **Required parameter check**:
   ```bash
   [[ -z "${PREFIX}" ]] && usage_error "Missing required parameter: --prefix"
   ```

2. **Normalization function** (lines 132-140):
   ```bash
   normalize_prefix() {
     local input="$1"
     # Trim whitespace
     local normalized="${input#"${input%%[![:space:]]*}"}"
     normalized="${normalized%"${normalized##*[![:space:]]}"}"
     # Convert to uppercase (bash 3.2 compatible)
     normalized="$(echo "$normalized" | tr '[:lower:]' '[:upper:]')"
     echo "${normalized}"
   }
   ```

3. **Validation check** (lines 169-172):
   ```bash
   if [[ ! "${NORMALIZED_PREFIX}" =~ ^[A-Z]{1,4}$ ]]; then
     validation_error "Invalid prefix format after normalization: '${NORMALIZED_PREFIX}' (expected: 1-4 uppercase letters, got '${PREFIX}' → '${NORMALIZED_PREFIX}')"
   fi
   ```

### Test Cases

Verify existing test cases from Issue-002:

1. **Valid prefix**: `--prefix MP` → normalized to `MP` ✅
2. **Lowercase input**: `--prefix "dg"` → normalized to `DG` ✅
3. **Missing prefix**: omitting `--prefix` → HALT with required parameter error ✅
4. **Invalid format**: `--prefix "12DG"` → HALT with format error ✅
5. **Too long**: `--prefix "TOOLONG"` → HALT with format error ✅

---

## P-084 Section 5.1 Requirements

### Prefix Determination Rules (Simplified)

**Explicit Prefix** (Issue-002 implementation):
- Use the provided prefix value directly
- Normalize: uppercase conversion, whitespace trimming
- Validate: MUST be 1-4 uppercase letters (A-Z only)
- HALT if invalid after normalization

**Derived Prefix** (NOT IMPLEMENTED):
- Original P-084 included derivation algorithm with `--derive-prefix` flag
- Removed from scope during Issue-002 simplification
- Prefix is now REQUIRED input with no derivation option

### Namespace Mapping Rules

Once prefix is determined (validated from input):

| Source Identifier | Project Identifier | Example (prefix=DG) |
|-------------------|-------------------|---------------------|
| P-001 | {PREFIX}-001 | DG-001 |
| P-042 | {PREFIX}-042 | DG-042 |
| P-999 | {PREFIX}-999 | DG-999 |

**Enforcement**:
- All project-specific pending items MUST use `{PREFIX}-###` format
- Project MUST NOT reference automated-builder `P-###` identifiers directly
- Prefix MUST be stored in `project.yaml` as the authoritative source (Issue-005)

---

## Documentation Updates

Create verification artifact documenting:

1. **Prefix determination contract**: Required input, normalization, validation
2. **P-084 Section 5.1 compliance**: Explicit prefix path satisfied
3. **Deviation from P-084**: Derivation algorithm removed (documented decision)
4. **Test results**: All prefix validation test cases verified

---

## Dependencies

- Issue-002 (prefix validation implementation)

---

## Files Likely Touched

- None (verification only, no code changes expected)
- Documentation artifact created in `docs/system/outputs/`

---

## Implementation Notes

**Expected outcome**: Issue-004 will likely be a **verification-only issue** with no code changes required, since Issue-002 already implements the required prefix determination logic.

The approval and implementation steps will:
1. Review existing code
2. Verify test cases
3. Document compliance with P-084 Section 5.1
4. Create implementation summary confirming requirements met

---

## References

- Primary Authority: [P-084 Section 10: Issue-004](2026-02-13__01__system__p-084-inventory-approved.md)
- Namespace Conversion: P-084 Section 5.1
- Issue-002 Implementation: [scripts/run-create-project](../../../scripts/run-create-project)
- Issue-002 Summary: [2026-02-16__04__system__issue-002-implementation-summary.md](2026-02-16__04__system__issue-002-implementation-summary.md)
