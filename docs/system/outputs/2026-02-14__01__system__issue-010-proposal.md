# Issue-010 Proposal: Introduce Inventory-Proposal Artifact Type (Governance)

**Issue**: Issue-010 (from P-084 Inventory)
**Type**: Governance
**Date**: 2026-02-14
**Status**: Proposed
**Parent**: P-084 — run-create-project bootstrap specification
**Inventory**: docs/system/outputs/2026-02-13__01__system__p-084-inventory-proposal-approved.md

---

## Objective

Establish inventory-proposal as a formal artifact type with standardized naming convention, validation lookup behavior, and lifecycle contract.

---

## Problem Statement

**Current State**:
- Inventory-proposals exist informally (e.g., P-084 Inventory-Proposal)
- No documented artifact type definition
- No standardized naming convention
- No documented lifecycle contract for how inventories relate to pending items
- Validation lookup behavior undefined
- Input normalization vs artifact enforcement principle undocumented

**Required State**:
- Inventory-proposal formally defined as an artifact type
- Naming convention: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal[-approved].md`
- Inventory Lifecycle Contract documented
- Validation lookup behavior specified
- Input normalization principle documented
- Clear distinction from regular proposals

---

## Proposed Solution

Add inventory-proposal artifact type documentation to governance, defining naming conventions, lifecycle behavior, and validation protocols.

### Approach

**Option A**: Extend `docs/system/outputs/README.md` with new artifact type section
**Option B**: Create new `docs/system/artifact-types.md` file

**Recommended**: Option A (extend existing README.md)
- Keeps artifact documentation centralized
- README.md already documents output artifacts
- Lower maintenance overhead (one file)

---

## Specification

### 1. Artifact Type Definition

**Name**: `inventory-proposal`

**Purpose**: Specification/inventory for implementation; does not execute

**Characteristics**:
- Definition-only artifacts that specify implementation scope
- Contain Issue-### execution slices (implementation plans)
- Do not execute directly
- Approved via rename to `*-approved.md`
- Referenced by parent P-### item in pending-items.md

**Distinction from Regular Proposals**:
- Regular proposals: Single-issue implementation plans
- Inventory-proposals: Multi-issue execution inventories with slice breakdown

### 2. Naming Convention

**Format**: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal.md`

**After Approval**: `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal-approved.md`

**Components**:
- `YYYY-MM-DD`: Date of creation (ISO format)
- `NN`: Sequence number (01, 02, etc.) for same-day artifacts
- `system`: Context identifier
- `<item-id>`: Parent pending item (e.g., `p-084`)
- `-inventory-proposal`: Type identifier
- `-approved`: Approval suffix (added after approval)

**Examples**:
- `2026-02-13__01__system__p-084-inventory-proposal.md` (proposed)
- `2026-02-13__01__system__p-084-inventory-proposal-approved.md` (approved)

### 3. Inventory Lifecycle Contract

When an Inventory-Proposal is approved:

1. **P-### Entry Update**: The corresponding P-### entry in `pending-items.md` MUST be updated to reflect the approved inventory scope in descriptive form.

2. **Execution Slices Only**: Issue-### items defined in the inventory are execution slices only.

3. **No Insertion**: Issue-### items MUST NOT be inserted into `pending-items.md`.

4. **Issue-Resolution Loop**: Execution proceeds through the issue-resolution loop using:
   ```
   Issue-### proposal → approval → implementation → summary
   ```

5. **Two-Stage Validation**:
   - **Primary**: Confirm implemented Issue-### items match the Inventory-Proposal specification
   - **Secondary**: Confirm resulting system state satisfies P-### descriptive requirements

6. **Deferred Issues**: If a deferred Issue-### is required to satisfy P-### requirements, validation MUST fail and P-### cannot be marked complete.

7. **Completion Authorization**: P-### completion is authorized only by successful validation, not by inventory approval.

### 4. Validation Lookup Behavior

**Rule**: Tools and processes MUST reference the most recent inventory-proposal artifact in `docs/system/outputs/` for a given item ID.

**Selection Algorithm**:
1. Scan `docs/system/outputs/` for files matching pattern: `*__system__<item-id>-inventory-proposal-approved.md`
2. Select artifact with highest date (YYYY-MM-DD)
3. If multiple artifacts have same date, select highest sequence number (NN)
4. If no approved inventory found, HALT: "No approved inventory-proposal found for {item-id}"

**Example**:
- For P-084, locate: `*__system__p-084-inventory-proposal-approved.md`
- Most recent: `2026-02-13__01__system__p-084-inventory-proposal-approved.md`

### 5. Input Normalization vs Artifact Enforcement Principle

**Governing Principle**: Rule files enforce deterministic structure and invariants on **system artifacts**, not on **human input**.

**Human Input (Flexible)**:
- Human-provided parameters, instructions, and requests are normalized, not rejected
- Input parsing is interpretive — if intent is understood, proceed
- Format variations are accepted and normalized to canonical form
- Examples:
  - "My Project" → "my-project"
  - "dg" → "DG"
  - "make a new project called foo" → project-slug: "foo"

**System Artifacts (Deterministic)**:
- Enforcement rules apply at **artifact-write time** (not input time)
- Files written to disk MUST conform to strict formats
- Validation failures HALT execution only when writing to artifacts
- Rule files enforce: structure, IDs, ordering, invariants **after artifact write**

**Ambiguity Handling**:
- If input is ambiguous or intent cannot be determined, ask clarifying questions
- Do NOT guess or auto-fix ambiguous input
- Do NOT reject input for minor format variations if intent is clear

---

## Implementation Plan

### Step 1: Update docs/system/outputs/README.md

Add new section titled "Inventory-Proposal Artifacts" with:
- Artifact type definition
- Naming convention
- Purpose and characteristics
- Distinction from regular proposals
- Example filenames

### Step 2: Document Inventory Lifecycle Contract

Add to `docs/system/issue-resolution.md`:
- New section: "Inventory-Proposal Lifecycle"
- 7-point lifecycle contract
- Two-stage validation explanation
- Relationship to pending-items.md

### Step 3: Document Validation Lookup Behavior

Add to `docs/system/issue-resolution.md`:
- Selection algorithm for most recent inventory
- HALT conditions
- Example lookup

### Step 4: Document Input Normalization Principle

Add to appropriate governance file (issue-resolution.md or new section):
- Governing principle statement
- Human input flexibility rules
- System artifact enforcement rules
- Ambiguity handling protocol
- Examples

---

## Acceptance Criteria

- [ ] Artifact type "inventory-proposal" defined in `docs/system/outputs/README.md`
- [ ] Naming convention documented with format and examples
- [ ] Purpose documented: "Specification/inventory for implementation; does not execute"
- [ ] Relationship to Issue-### documented: "Inventory-proposals contain Issue-### implementation plans"
- [ ] Distinction from regular proposals clearly stated
- [ ] Inventory Lifecycle Contract documented in `docs/system/issue-resolution.md` with all 7 points
- [ ] Two-stage validation explained (Issue-### match + P-### requirements)
- [ ] Validation lookup behavior documented with selection algorithm
- [ ] HALT conditions for missing inventory documented
- [ ] Input Normalization vs Artifact Enforcement principle documented
- [ ] Examples provided for input normalization (minimum 3)
- [ ] All documentation uses consistent terminology
- [ ] Cross-references between files are accurate

---

## Files to Modify

1. **docs/system/outputs/README.md**
   - Add: Inventory-Proposal artifact type section
   - Add: Naming convention
   - Add: Example filenames

2. **docs/system/issue-resolution.md**
   - Add: Inventory-Proposal Lifecycle section
   - Add: Validation lookup behavior
   - Add: Input Normalization vs Artifact Enforcement section

---

## Non-Goals

- ❌ Implementation of run-create-project (separate issues)
- ❌ Automated validation tooling
- ❌ Retrospective updates to existing artifacts
- ❌ Changes to pending-items.md format

---

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Inventory lifecycle contract not followed consistently | Clear documentation with examples; reference in issue-resolution.md |
| Confusion between inventory-proposal and regular proposals | Explicit distinction documented; different naming patterns |
| Validation lookup logic not applied correctly | Selection algorithm clearly specified with HALT conditions |
| Input normalization principle misinterpreted | Multiple examples provided; clear boundary between input and artifacts |

---

## Success Criteria

This proposal is complete when:
- [ ] All acceptance criteria met
- [ ] Documentation added to governance files
- [ ] Cross-references accurate and resolvable
- [ ] P-084 inventory used as reference example
- [ ] No conflicts with existing governance rules

---

## References

- [P-084 Approved Inventory](./2026-02-13__01__system__p-084-inventory-proposal-approved.md)
- [P-084 in pending-items.md](../pending-items.md#P-084)
- [docs/system/outputs/README.md](./README.md)
- [docs/system/issue-resolution.md](../issue-resolution.md)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-14 | Initial proposal for Issue-010 |
