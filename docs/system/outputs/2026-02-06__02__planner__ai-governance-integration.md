# Planner Output: AI Governance Integration

**Date**: 2026-02-06
**Output**: 02
**Context**: Planner
**Description**: AI Governance Integration for Devotional Generator

---

## Gatekeeper-Style Summary

### What Changed and Why

I analyzed all planning artifacts for the Devotional Generator project against the new canonical `docs/system/ai.md` policy. The analysis reveals that **existing artifacts lack explicit executor/verifier attribution**, which creates ambiguity about who performs work and who validates it.

**Key Gap**: Current phase plans have "Gatekeeper Checklist" sections that mention "Human Review Required" but do not specify:
- **Which** human (Barbara vs Professional Reviewer)
- **Which** AI executor (Claude Code, Codex, etc.)
- Risk levels that would trigger elevated review
- AI-specific mitigations for known weaknesses

---

## Artifacts Requiring Updates

| Artifact | Current State | Required Changes |
|----------|---------------|------------------|
| `prd.md` | No executor/verifier | Add execution section referencing ai.md |
| `roadmap.md` | Generic "Gatekeeper Reviews" | Add Executor/Verifier per CP + risk levels |
| `phases/001-data-model-inputs.md` | "Human Review Required" (unspecified) | Name executor, verifier, risk level per CP |
| `phases/002-template-system.md` | Same | Same |
| `phases/003-kdp-pdf-export.md` | Same | Same + elevated review for PDF logic |
| `phases/004-validation-preview.md` | Same | Same |
| `iteration-log.md` | No attribution in decision log | Add executor column to decision log |

---

## Proposed Changes by Document

### 1. PRD (prd.md)

**Add new section before "Related Documents":**

```markdown
## Execution Governance

This project follows `docs/system/ai.md` for executor/verifier assignments.

**Default Assignments**:
- **Executor**: AI: Claude Code (for all implementation phases)
- **Verifier**: Human: Barbara (for all CPs)
- **Elevated Review**: Professional Code Reviewer (for Phase 003 PDF logic)

All executor and verifier assignments are documented in the phase plans.
```

### 2. Roadmap (roadmap.md)

**Replace "Gatekeeper Reviews" section with:**

```markdown
## Execution & Verification

Per `docs/system/ai.md`, every commit point has an assigned executor and verifier.

### Commit Point Attribution

| CP | Executor | Verifier | Risk | Notes |
|----|----------|----------|------|-------|
| CP1 | AI: Claude Code | Human: Barbara | L | Schema work; low risk |
| CP2 | AI: Claude Code | Human: Barbara | L | Data models; low risk |
| CP3 | AI: Claude Code | Human: Barbara | L | Template structure |
| CP4 | AI: Claude Code | Human: Barbara | L | Template elements |
| CP5 | AI: Claude Code | Human: Barbara | M | KDP margins—verify spec compliance |
| CP6 | AI: Claude Code | Human: Barbara | M | PDF generation; verify fonts |
| CP7 | AI: Claude Code | Human: Barbara | L | Title page/numbering |
| CP8 | AI: Claude Code | Human: Barbara | L | Validation rules |
| CP9 | AI: Claude Code | Human: Barbara | M | KDP compliance—test upload |

### High-Risk Triggers

Per ai.md, the following require elevated review:
- **CP6** (PDF generation): Font embedding is system-dependent
- **CP9** (KDP validation): Final gate before upload

**Mitigation**: Run KDP preview upload as verification step.
```

### 3. Phase Plans (001-004)

**Add to each CP section (example for CP1):**

```markdown
**Execution**:
- Executor: AI: Claude Code
- Verifier: Human: Barbara
- Risk: L (Low)
- AI Mitigation: Provide diff summary + files touched per ai.md
```

**For Phase 003 (CP5, CP6, CP7):**

```markdown
**Execution**:
- Executor: AI: Claude Code
- Verifier: Human: Barbara
- Risk: M (Medium)
- AI Mitigation:
  - Weakness: May over-optimize structure
  - Mitigation: Narrow scope; explicit KDP specs as acceptance criteria
  - Optional: Second-pass by AI: Codex for mechanical verification
```

### 4. Iteration Log

**Update Decision Log table to include Executor column:**

```markdown
| ID | Date | Decision | Executor | Rationale | Status |
|----|------|----------|----------|-----------|--------|
```

---

## Open Questions

The following executor/verifier assignments could not be safely determined:

| Item | Question | Proposed Default |
|------|----------|------------------|
| **Content creation** | Who writes actual devotional content? | TBD—not in scope for v1.0 (placeholders only) |
| **Font selection** | Is font bundling an AI or human decision? | Human: Barbara (design decision) |
| **KDP upload test** | Who performs the actual KDP preview upload? | Human: Barbara (requires Amazon account) |
| **Open Questions (Q1-Q13)** | Who answers the 13 open PRD questions? | Human: Barbara (product decisions) |

---

## Recommendations (Planning-Only)

1. **Immediate**: Add the Execution Governance section to PRD with a reference to `docs/system/ai.md`

2. **Before Phase 001 Execution**: Update each phase plan with explicit Executor/Verifier/Risk per CP

3. **Before Phase 003**: Consider designating Professional Code Reviewer for CP6 (PDF generation) given system-level dependencies

4. **Process**: Add a standard template section for all future phase plans:
   ```markdown
   ## Execution
   - Executor: [Name per ai.md]
   - Verifier: [Name per ai.md]
   - Risk: L | M | H
   - AI Mitigation: [If AI executor]
   ```

5. **Do NOT Duplicate**: Reference `docs/system/ai.md` for AI capability details; do not copy weakness/mitigation text into phase plans

---

## Canonical References

- `docs/system/ai.md` — AI Delegation & Review Policy (single source of truth)
- `docs/system/identity.md` — System Identity and authority model
- `docs/system/prompt-template.md` — Prompt structure template

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-06 | Initial planning output |
