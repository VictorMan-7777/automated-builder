# System Documentation Changelog

**Purpose**: Track changes to system-level documentation and framework rules
**Location**: `docs/system/changelog.md`
**Last Updated**: 2026-02-10

---

## 2026-02-09

### Issue Loop Templates

**Type**: Feature
**Impact**: Minor
**Status**: Complete

**Description**:
Codified the approved loop templates into `docs/system/issues.md`: Proposal
(commit inventory, produce proposal, no implementation, no commit), Approval
(same-session human text, scope definition, unlocks commits), and combined
Deferred / Unapproved + Verification (produce register if applicable, produce
verification, commit, stop).

**Files Affected**:
- `docs/system/issues.md` (v1.1 → v1.2)
- `docs/system/changelog.md` (this entry)

**See**: `docs/system/issues.md`, Loop Templates section

---

### Issue Resolution Loop

**Type**: Feature
**Impact**: Minor
**Status**: Complete

**Description**:
Codified the approved issue resolution loop into `docs/system/issues.md`.
Defines the Inventory → Proposal → Approval → Change → Summary per-issue
cycle, termination conditions, end-of-loop artifact requirements (Deferred /
Unapproved register and Verification), and the post-verification constraint
against new proposals without a new inventory.

**Files Affected**:
- `docs/system/issues.md` (v1.0 → v1.1)
- `docs/system/changelog.md` (this entry)

**See**: `docs/system/issues.md`, Issue Resolution Loop section

---

### Issue Numbering and Severity Scheme

**Type**: Feature
**Impact**: Minor
**Status**: Complete

**Description**:
Codified the approved issue numbering and severity scheme into system
documentation. Defines `Issue-###` format, severity suffixes (C for CRITICAL,
H for HIGH, none for MEDIUM/LOW), placement rules for issue identifiers in
output artifacts, and changelog entry format.

**Files Affected**:
- `docs/system/issues.md` (new)
- `docs/system/README.md` (directory structure updated)
- `docs/system/changelog.md` (this entry)

**See**: `docs/system/issues.md` for full specification

---

### Architecture Review Pass 1 — Fixes A–E

**Type**: Fix
**Impact**: Minor
**Status**: Complete

**Description**:
Five fixes from Architecture Review Pass 1
(`2026-02-09__01__system__architecture-review-pass-1.md`):

- **Fix A** — Define system iterator protocol for output filenames.
  Added "System Iterator" subsection to `docs/system/outputs/README.md`.
- **Fix B** — Resolve NN sequence-number contradiction. Removed
  monotonic-across-repo rule from `docs/system/run-planner.md`; per-day
  rule in `outputs/README.md` is authoritative.
- **Fix C** — Expand CP-2 governance lock list from 4 to 10 files in
  `docs/implementation/system/checkpoint-taxonomy.md`.
- **Fix D** — Clarify operator delegation for planner checkpoint commands.
  Added Section 5.1 to `docs/implementation/system/checkpoint-taxonomy.md`.
- **Fix E** — Add interrupted session protocol. Added Section 3.4 to
  `docs/implementation/system/checkpoint-taxonomy.md`.

**Files Affected**:
- `docs/system/outputs/README.md` (Fix A)
- `docs/system/run-planner.md` (Fix B)
- `docs/implementation/system/checkpoint-taxonomy.md` (Fixes C, D, E)

**See**: `2026-02-09__01__system__architecture-review-pass-1.md` and
individual implementation summaries (output artifacts 03, 05, 07, 09, 11)

---

## 2026-02-07

### Output Requirement Rule Change

**Type**: Feature
**Impact**: Major
**Status**: Complete

**Description**:
Replaced the length-based heuristic ("save outputs only if long") with a
deterministic artifact-type trigger: outputs must be created for any session
producing a reviewable artifact (plans, audits, decisions, governance
guidance), regardless of length.

**Files Affected**:
- `docs/system/access.md` (Output Writes section updated)
- `docs/system/initial-prompt.md` (Cross-Mode Provision updated)

**See**: `2026-02-07__04__system__output-requirement-rule-change.md`

---

### Output Compliance Enforcement

**Type**: Feature
**Impact**: Major
**Status**: Complete

**Description**:
Introduced a mandatory Output Compliance Clause making output artifact
creation a structural precondition for session completion. Enforced at three
layers: authority header (session stop-condition), prompt template (standard
instruction block), and role-specific checklists.

**Files Affected**:
- `docs/system/initial-prompt.md` (v1.0 → v1.1, authority header clause)
- `docs/system/access.md` (compliance clause paragraph)
- `docs/system/prompt-template.md` (v1.0 → v1.1, standard instruction block)
- `prompts/planner/run-planner.md` (Step 7 and checklist updated)
- `prompts/builder/run-builder.md` (checklist updated)

**See**: `2026-02-07__10__system__output-compliance-enforcement.md`

---

### System Builder MVP Plan

**Type**: Feature
**Impact**: Minor
**Status**: Complete

**Description**:
Approved the System Builder MVP plan defining the minimum viable execution
framework for builder sessions.

**Files Affected**:
- Planning artifact only (no system files modified)

**See**: `2026-02-07__07__planner__system-builder-mvp-plan.md`

---

### Checkpoint Taxonomy Execution Contract

**Type**: Feature
**Impact**: Major
**Status**: Complete

**Description**:
Approved the Checkpoint Taxonomy defining the 9-checkpoint execution contract
(CP-1 through CP-9) for all system sessions. Establishes checkpoint ordering,
verification criteria, pass/fail conditions, and 7 invariants.

**Files Affected**:
- `docs/implementation/system/checkpoint-taxonomy.md` (new, APPROVED)

**See**: `2026-02-07__11__builder__checkpoint-taxonomy-execution-contract.md`

---

## 2026-02-05

### Naming Convention Correction

**Type**: Format Standardization
**Impact**: Breaking change for output file naming
**Status**: Complete

**Previous Format**:
```
YYYY-MM-DD-descriptive-name.md
```

**Problem**: Does not support multiple outputs per day with proper ordering

**New Canonical Format**:
```
YYYY-MM-DD__NN__<context>__<short-description>.md
```

**Components**:
- `YYYY-MM-DD`: ISO 8601 date
- `NN`: Zero-padded daily sequence (01, 02, 03, ...)
- `<context>`: planner | builder | gatekeeper | system
- `<short-description>`: Lowercase, hyphen-separated

**Rationale**:
- Enables multiple outputs per day with clear ordering
- Context prefix makes output source immediately clear
- Supports alphabetical sorting within same day
- Aligns with structured data principles

**Files Renamed**:
1. `2026-02-05-reorganization-summary.md`
   → `2026-02-05__01__planner__reorganization-summary.md`

2. `2026-02-05-long-output-capture-implementation.md`
   → `2026-02-05__02__system__long-output-capture-implementation.md`

**Documentation Updated**:
- `planning.md` - Updated Long Output Capture section
- `docs/system/README.md` - Updated directory structure examples
- `docs/system/outputs/README.md` - Complete naming convention rewrite
- `README.md` - Updated Long Output Capture Rule examples

**Migration Guide**:
For existing outputs using old format:
1. Determine context (planner/builder/gatekeeper/system)
2. Assign sequence number (NN) based on creation time
3. Rename: `YYYY-MM-DD-name.md` → `YYYY-MM-DD__NN__<context>__name.md`

**Examples**:
- ✅ `2026-02-05__01__planner__reorganization-summary.md`
- ✅ `2026-02-10__01__builder__phase-001-completion.md`
- ✅ `2026-02-10__02__gatekeeper__phase-001-review.md`
- ❌ `2026-02-05-summary.md` (old format)

---

## 2026-02-05 (Earlier)

### Long Output Capture Rule Implementation

**Type**: New Feature
**Impact**: Framework requirement
**Status**: Complete (with naming correction above)

**Changes**:
- Created `docs/system/outputs/` directory
- Created Long Output Capture rule documentation
- Updated `planning.md` v1.0 → v1.1 (added Long Output section)
- Updated `builder.md` v1.0 → v1.1 (added Long Output section)
- Updated root `README.md` (added Long Output rule)
- Updated `.gitignore` (temp file patterns)

**Rationale**:
- Preserve comprehensive outputs as permanent records
- Reduce chat clutter (summaries in chat, details in files)
- Enable future reference and auditing
- Maintain git history of all outputs

**See**: `2026-02-05__02__system__long-output-capture-implementation.md` for full details

---

## Template for Future Entries

```markdown
## YYYY-MM-DD

### [Change Title]

**Type**: [Feature | Fix | Deprecation | Breaking Change | Refactor]
**Impact**: [None | Minor | Major | Breaking]
**Status**: [Proposed | In Progress | Complete | Deprecated]

**Description**:
[What changed and why]

**Files Affected**:
- file1.md
- file2.md

**Migration Notes** (if applicable):
[How to adapt to this change]

**See**: [Link to related documentation or output file]
```

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2026-02-10 | Add missing entries for 2026-02-07 and 2026-02-09 changes (Issue-004) |
| 1.1 | 2026-02-05 | Added naming convention correction entry |
| 1.0 | 2026-02-05 | Initial changelog created |
