# System Documentation Changelog

**Purpose**: Track changes to system-level documentation and framework rules
**Location**: `docs/system/changelog.md`
**Last Updated**: 2026-02-05

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
| 1.1 | 2026-02-05 | Added naming convention correction entry |
| 1.0 | 2026-02-05 | Initial changelog created |
