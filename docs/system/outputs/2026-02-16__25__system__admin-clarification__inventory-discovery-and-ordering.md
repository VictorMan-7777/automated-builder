# Admin Clarification — Inventory Discovery and Verification Ordering

**Type**: Administrative Clarification
**Date**: 2026-02-16
**Purpose**: Prevent verification/discovery failures caused by legacy filename references, output numbering conflicts, and ordering assumptions

---

## A. Inventory Artifact Discovery Rule

**Primary Authority**: The most recent matching `*-inventory-approved.md` artifact on disk.

**Legacy Compatibility**: Historical references to `inventory-proposal-approved` inside other documents are NON-authoritative and reflect legacy naming conventions.

**Discovery Protocol**:
1. Search for `YYYY-MM-DD__NN__system__<item-id>-inventory-approved.md` (current pattern)
2. If not found, search for `YYYY-MM-DD__NN__system__<item-id>-inventory-proposal-approved.md` (legacy pattern)
3. If multiple matches exist, select most recent by filename prefix (YYYY-MM-DD__NN)
4. Discovery MUST prefer `-inventory-approved` when both patterns exist for same item-id

**Rationale**: Naming conventions evolved from `inventory-proposal-approved` to `inventory-approved` during lifecycle standardization. Discovery must support both patterns but prioritize current naming.

**Example**:
- Current: `2026-02-13__01__system__p-084-inventory-approved.md`
- Legacy: `2026-02-13__01__system__p-084-inventory-proposal-approved.md` (if it existed)
- Discovery: Select `p-084-inventory-approved` (current pattern preferred)

---

## B. Verification Ordering Rule

**Core Principle**: Issues are a SET, not a SEQUENCE.

**Verification Requirements**:
1. Inventory Stage-1 verification MUST treat Issue-### items as an unordered set
2. Verification MUST NOT assume Issues are completed in numerical order
3. Verification MUST NOT assume Issues are completed in chronological commit order
4. Evidence for Issue-### completion:
   - Presence of `*-issue-NNN-approved.md` artifact, OR
   - Presence of `*-issue-NNN-implementation-summary.md` artifact, OR
   - Explicit deferral documented in inventory-approved artifact

**Search Pattern**: For Issue-NNN, search for:
- `*__issue-NNN-approved.md` (approved artifact)
- `*__issue-NNN-implementation-summary.md` (implementation summary)
- Either artifact proves Issue-NNN was addressed

**Anti-Pattern**: Assuming Issue-001 must exist before Issue-005, or that Issue-005 must be committed before Issue-007.

**Rationale**: Implementation order may differ from definition order due to dependencies, consolidation, or practical considerations. Verification must be evidence-based, not assumption-based.

**Example**:
- P-084 defines Issue-001, Issue-002, Issue-003, Issue-004, Issue-005, Issue-006, Issue-007, Issue-008, Issue-009, Issue-010, Issue-011
- Implementation may complete: Issue-001, Issue-005 (consolidates 002/003/004), Issue-006, Issue-011, Issue-008, Issue-009, Issue-007
- Verification must discover Issue-005 completion even if Issue-002/003/004 artifacts don't exist as separate items

---

## C. Output Numbering Conflict Note

**Conflict Scenario**: Multiple artifacts created on same date may require renumbering to resolve sequence collisions.

**Discovery Requirements**:
1. Discovery MUST rely on filenames present on disk (authoritative)
2. Discovery MUST NOT assume sequence numbers remain stable across artifact lifecycle
3. Discovery MUST extract issue identifiers from artifact filenames and/or content
4. If artifact was renamed due to numbering conflict, discovery must find it by issue identifier, not original sequence number

**Search Strategy**:
- Primary: Filename pattern match on issue identifier (e.g., `*issue-007*`)
- Secondary: Content-based identifier extraction if filename pattern fails
- Fallback: Manual inventory of docs/system/outputs/ directory

**Example**:
- Original: `2026-02-16__20__system__issue-009-proposal.md`
- After conflict: `2026-02-16__22__system__issue-009-proposal.md` (renumbered)
- Discovery: Must find via pattern `*issue-009-proposal.md`, not by sequence number 20

**Rationale**: Sequence numbers are organizational aids, not immutable identifiers. Issue identifiers (issue-NNN) are stable across renames.

---

## D. Evidence-Based Verification Protocol

**Verification Steps**:
1. Read inventory-approved artifact to extract Issue-### list
2. For each Issue-###:
   - Search: `find docs/system/outputs/ -name "*issue-###-approved.md"`
   - Search: `find docs/system/outputs/ -name "*issue-###-implementation-summary.md"`
   - Result: FOUND / NOT FOUND with exact file path or "not found" evidence
3. Classify findings:
   - **Complete**: Both approved + summary exist
   - **Approved only**: Approved exists, summary missing (implementation in progress or consolidated)
   - **Summary only**: Summary exists, approved missing (unexpected, investigate)
   - **Not Found**: Neither exists (deferred, consolidated, or missing)
4. For "Not Found" cases, check inventory-approved artifact for explicit deferral or consolidation notes

**No Speculation**: Every verification claim must be backed by:
- Exact file path (for FOUND)
- Exact search command + empty result (for NOT FOUND)
- Explicit reference to inventory-approved content (for deferral/consolidation)

---

## E. Application to P-084 Stage-1 Verification

**Inventory**: P-084 defines Issue-001 through Issue-011 (11 issues)

**Discovery Requirements**:
1. Find P-084 inventory-approved artifact (not legacy inventory-proposal-approved)
2. Extract Issue-### list from Section 10
3. Search for each Issue-### artifact independently (not sequentially)
4. Report findings with evidence (file paths or "not found" with search pattern)
5. Classify completion status (complete, partial, deferred, consolidated, missing)

**Expected Patterns**:
- Some Issues may be consolidated (e.g., Issue-002/003/004 into Issue-005)
- Some Issues may be implemented out of order (e.g., Issue-011 before Issue-008)
- Some Issues may be governance-only (e.g., Issue-010) without implementation artifacts

**Verification Outcome**: Stage-1 passes if all non-deferred Issues have evidence of completion (approved or summary artifacts exist).

---

## References

- P-084 Inventory: [2026-02-13__01__system__p-084-inventory-approved.md](2026-02-13__01__system__p-084-inventory-approved.md)
- P-084 Section 6.1: Inventory Lifecycle Contract
- Issue Resolution: [docs/system/issue-resolution.md](../issue-resolution.md)
