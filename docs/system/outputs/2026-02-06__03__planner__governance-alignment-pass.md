# Planner Iteration 2: Execution Governance Alignment

**Date**: 2026-02-06
**Output**: 03
**Context**: Planner
**Iteration**: 2
**Title**: Governance Alignment Pass (No Product Decisions)

---

## Gatekeeper-Style Summary

### What This Iteration Does

This iteration applies the AI Delegation & Review Policy (`docs/system/ai.md`) to all Devotional Generator planning artifacts. It adds explicit Executor/Verifier/Risk attribution to every commit point without changing product scope, intent, or direction.

### Key Findings

1. **Gap Identified**: Current artifacts have "Human Review Required" but do not name which human or which AI executor
2. **Attribution Proposed**: All 9 CPs assigned to AI: Claude Code (executor) with Human: Barbara (verifier)
3. **Elevated Risk**: CP5, CP6, CP9 flagged as Medium risk requiring additional verification steps
4. **TBD Items**: 4 items require human decision before resolution

### Compliance Status

| Check | Status |
|-------|--------|
| All CPs have Executor/Verifier | ✓ Proposed |
| AI not assigned product authority | ✓ Compliant |
| ai.md referenced, not duplicated | ✓ Compliant |
| Approval semantics unchanged | ✓ Compliant |

---

## Artifacts Affected (Planning-Only)

All changes are **proposed only**. No artifacts have been modified.

| Artifact | Location | Proposed Change |
|----------|----------|-----------------|
| PRD | `prd.md` | Add Execution Governance section |
| Roadmap | `roadmap.md` | Replace "Gatekeeper Reviews" with CP attribution table |
| Phase 001 | `phases/001-data-model-inputs.md` | Add Execution Attribution to CP1, CP2 |
| Phase 002 | `phases/002-template-system.md` | Add Execution Attribution to CP3, CP4 |
| Phase 003 | `phases/003-kdp-pdf-export.md` | Add Execution Attribution to CP5, CP6, CP7 (elevated) |
| Phase 004 | `phases/004-validation-preview.md` | Add Execution Attribution to CP8, CP9 (elevated) |
| Iteration Log | `iteration-log.md` | Add Executor column to Decision Log |

All paths relative to `docs/projects/devotional-generator/`.

---

## Scope Confirmation

**In Scope**:
- Adding Executor/Verifier/Risk to all CPs and tasks
- Referencing `docs/system/ai.md` canonically
- Flagging TBDs where assignment cannot be inferred

**Explicitly Out of Scope**:
- Answering Q1-Q13 (product decisions)
- Changing content structure or scope
- Implementing or proposing automation

---

## Governance Alignment: Artifact-by-Artifact

### 1. PRD (prd.md)

**Current State**: No execution governance section.

**Proposed Addition** (before "Related Documents"):

```markdown
---

## Execution Governance

Execution assignments follow `docs/system/ai.md`. This document does not duplicate AI capability rules.

### Default Assignments

| Role | Assigned To |
|------|-------------|
| Executor (all phases) | AI: Claude Code |
| Verifier (all CPs) | Human: Barbara |
| Elevated Review | See phase plans for M/H risk CPs |

### Human-Only Tasks (per ai.md)

The following remain human-only:
- Answering open questions Q1-Q13 (product intent)
- Final KDP upload and account actions
- Approval of all CPs

### Reference

See `docs/system/ai.md` for executor capabilities, weaknesses, and mitigations.
```

**Risk Assessment**: PRD itself is a planning artifact, not executed code. No CP-level risk applies.

---

### 2. Roadmap (roadmap.md)

**Current State**: Has "Gatekeeper Reviews" section but no Executor/Verifier/Risk per CP.

**Proposed Replacement** (replace "Gatekeeper Reviews" section):

```markdown
---

## Execution & Verification

Per `docs/system/ai.md`, every commit point has an assigned Executor and Verifier.

### Commit Point Attribution

| CP | Phase | Executor | Verifier | Risk | Mitigation |
|----|-------|----------|----------|------|------------|
| CP1 | 001 | AI: Claude Code | Human: Barbara | L | Standard diff review |
| CP2 | 001 | AI: Claude Code | Human: Barbara | L | Standard diff review |
| CP3 | 002 | AI: Claude Code | Human: Barbara | L | Standard diff review |
| CP4 | 002 | AI: Claude Code | Human: Barbara | L | Standard diff review |
| CP5 | 003 | AI: Claude Code | Human: Barbara | M | Verify KDP margin specs exactly |
| CP6 | 003 | AI: Claude Code | Human: Barbara | M | Verify font embedding manually |
| CP7 | 003 | AI: Claude Code | Human: Barbara | L | Standard diff review |
| CP8 | 004 | AI: Claude Code | Human: Barbara | L | Standard diff review |
| CP9 | 004 | AI: Claude Code | Human: Barbara | M | Test KDP upload before approval |

### Risk Legend

- **L (Low)**: Standard human review sufficient
- **M (Medium)**: Additional verification step required (noted in Mitigation)
- **H (High)**: Professional reviewer or elevated process (none currently)

### High-Risk Triggers (per ai.md)

None of the current CPs touch:
- Auth / permissions
- Database schema or migrations
- Financial / billing logic

**Note**: CP6 and CP9 require elevated attention due to external system dependencies (PDF tooling, KDP platform).

### Human-Only Checkpoints

Per ai.md and identity.md, the following are human-only:
- Answering open questions (Q1-Q13)
- CP approval decisions
- KDP account operations
```

---

### 3. Phase 001: Data Model & Inputs

**Current State**: Has "Gatekeeper Checklist" with "Human Review Required" but no named executor.

**Proposed Addition** (add after each CP's "Rollback" section):

**For CP1:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, files touched, validation test results |
```

**For CP2:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, files touched, sample data validation |
```

**Gatekeeper Checklist Update**:
```markdown
### Gatekeeper Checklist

**Executor**: AI: Claude Code
**Verifier**: Human: Barbara

#### Human Review Required
- [ ] Data model captures all content requirements
- [ ] Input defaults are sensible
- [ ] Structure supports future extensibility

#### Verification Reference
See `docs/system/ai.md` for AI executor output requirements.
```

---

### 4. Phase 002: Template System

**Proposed Addition** (same pattern):

**For CP3:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, files touched, template render test |
```

**For CP4:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, sample rendered output |
```

---

### 5. Phase 003: KDP PDF Export

**This phase has elevated risk due to PDF generation complexity.**

**For CP5:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | M (Medium) |
| AI Mitigation | Provide: diff summary, explicit margin values, visual margin check |
| Elevated Check | Verify margins against KDP spec table before approval |
```

**For CP6:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | M (Medium) |
| AI Mitigation | Provide: diff summary, font embedding verification command output |
| Elevated Check | Open PDF in reader, verify fonts show "Embedded" in properties |
| AI Weakness Note | Claude Code may not catch system-specific font issues; manual verification required |
```

**For CP7:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, sample PDF with title page |
```

---

### 6. Phase 004: Validation & Preview

**For CP8:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, validation test results on valid/invalid inputs |
```

**For CP9:**
```markdown
**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | M (Medium) |
| AI Mitigation | Provide: diff summary, KDP validation report output |
| Elevated Check | Upload sample PDF to KDP preview before final approval |
| Note | Actual KDP upload is Human: Barbara only (account action) |
```

---

### 7. Iteration Log (iteration-log.md)

**Proposed Update** to Decision Log table header:

```markdown
| ID | Date | Decision | Executor | Verifier | Rationale | Status |
|----|------|----------|----------|----------|-----------|--------|
```

**For existing decisions**, executor defaults to **TBD (retrospective)** since they were made before ai.md existed.

---

## Open Executor/Verifier Questions (TBD Items)

| Item | Question | Proposed Resolution |
|------|----------|---------------------|
| Superseded file cleanup | Who removes old phase files? | TBD—likely Human: Barbara (file deletion is reversible but destructive) |
| Font bundling decision (if needed) | Who selects/licenses fonts? | Human: Barbara (design + licensing decision) |
| KDP account upload | Who performs actual upload? | Human: Barbara (requires account credentials) |
| Q1-Q13 answers | Who answers product questions? | Human: Barbara (product intent per ai.md) |

---

## Consistency Check

| Check | Status | Notes |
|-------|--------|-------|
| AI assigned authority over product intent? | NO | Q1-Q13 remain human-only |
| AI executes prohibited tasks per ai.md? | NO | No auth, billing, or destructive ops |
| Approval semantics unchanged? | YES | All CPs require Human: Barbara approval |
| ai.md referenced, not duplicated? | YES | Proposed text references ai.md |

---

## What Changed (This Iteration)

1. **Added**: Executor/Verifier/Risk attribution table for all 9 CPs
2. **Added**: Execution Governance section proposed for PRD
3. **Added**: Execution Attribution blocks for each CP in phase plans
4. **Updated**: Gatekeeper Checklist sections to name executor/verifier
5. **Identified**: 4 TBD items requiring human decision
6. **Flagged**: CP5, CP6, CP9 as Medium risk with elevated checks

## What Did NOT Change

1. **Product scope**: No changes to requirements or content structure
2. **Open questions**: Q1-Q13 remain unanswered (out of scope)
3. **Phase structure**: Still 4 phases, 9 CPs
4. **Approval semantics**: Human: Barbara remains sole approver
5. **ai.md content**: No changes proposed to canonical policy

---

## Risks / Discomfort

1. **Retrospective attribution**: Existing decisions in iteration-log have no executor recorded; marking as "TBD (retrospective)" is accurate but awkward
2. **Font selection**: Currently listed as Human: Barbara, but if AI is asked to recommend fonts, that's borderline product decision—flagged as TBD
3. **Medium risk CPs**: CP5, CP6, CP9 all involve external dependencies; may warrant Professional Reviewer if scope expands

---

## Next Steps (Pending Approval)

1. Apply proposed changes to PRD
2. Apply proposed changes to roadmap
3. Apply proposed changes to phase plans (001-004)
4. Update iteration-log with this iteration
5. Resolve TBD items with Human: Barbara

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-06 | Initial governance alignment pass |

---

PAUSE FOR HUMAN REVIEW

No artifacts have been modified in this iteration.
All changes are proposed only.

Awaiting explicit instruction to:
- Proceed with applying changes to artifacts
- Request clarification on TBD items
- Advance to Planner Iteration 3 (Q1–Q13)
---
