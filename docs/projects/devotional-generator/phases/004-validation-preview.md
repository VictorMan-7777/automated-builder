# Phase 004: Validation & Preview

## Phase Information

- **Phase**: 004
- **Name**: Validation & Preview
- **Status**: Not Started
- **Dependencies**: Phase 003 complete

## Objective

Ensure devotional content is complete and PDF meets KDP requirements before export.

---

## Scope

### In Scope

- Structure validation (all 5 elements present, including Turabian attribution completeness)
- Content completeness checks
- Quote attribution completeness validation (Turabian fields)
- Scripture retrieval validation (fetched text matches reference; flag retrieval failures)
- Reflection approval enforcement (no export without human approval)
- Output-mode-aware validation (publish-ready vs personal)
- Page count warning for publish-ready output below 24-page KDP minimum
- Front matter validation (Introduction includes Sunday worship guidance when Day 7 present)
- Optional progression validation (day_focus sub-themes)
- KDP compliance validation (margins, fonts, dimensions)
- Preview capability
- Validation reporting

### Out of Scope

- Content quality scoring (AI-based)
- Spell checking
- Multi-format preview

---

## Commit Points

### CP8: Structure Validation

**Goal**: Validate that all content elements are present and populated

**Deliverables**:
- `validators/structure-validator.py` - Content structure checks
- Validation report format

**Validation Rules**:

| Rule | Check | Severity | Notes |
|------|-------|----------|-------|
| V001 | All days present for num_days | Error | |
| V002 | Each day has quote element | Error | |
| V003 | Each day has scripture element | Error | |
| V004 | Each day has reflection element | Error | |
| V005 | Each day has action_steps element | Error | |
| V006 | Each day has prayer element | Error | |
| V007 | Quote has text and Turabian attribution fields (author, source_title) | Error | Q1: structured attribution required |
| V008 | Scripture has reference and text; text matches reference | Error | Q2: validate fetched text |
| V009 | Action steps has at least 1 item | Warning | |
| V010 | Reflection content not empty | Error | |
| V011 | Prayer content not empty | Error | |
| V012 | Reflection approval_status = approved (publish-ready mode) | Error | Q3: no export without approval |
| V013 | Reflection approval_status = approved (personal mode) | Warning | Q3: warn but allow for personal use |
| V014 | Scripture retrieval succeeded (no fetch failures) | Error | Q2: flag retrieval failures |
| V015 | Day count >= 12 for publish-ready output | Warning | Q4: recommend minimum for KDP |
| V016 | Introduction includes Sunday worship guidance when Day 7 present | Error | Q6: content dependency |
| V017 | Front matter complete (title, copyright, introduction) | Error | Q7: mandatory front matter |
| V018 | Day focus progression logical (optional) | Info | Q5: optional progression check |

**Validation Report Format**:
```
Devotional Validation Report
============================
Date: 2026-02-06
Topic: Finding Peace

Overall Status: PASS | FAIL

Structure Checks:
[✓] V001: All 6 days present
[✓] V002: All days have quote
[!] V009: Day 3 has 0 action steps (warning)
[✗] V010: Day 5 reflection is empty (error)

Errors: 1
Warnings: 1
```

**Files to Stage**:
- `validators/structure-validator.py`
- `validators/validation-rules.yaml`

**Commit Command**:
```bash
git add validators/
git commit -m "feat(devotional-generator): add structure validation (CP8)"
```

**Verification**:
- [ ] Validator catches missing elements
- [ ] Validator catches empty content
- [ ] Report clearly shows pass/fail
- [ ] Error vs warning severity works

**Rollback**:
```bash
git reset --soft HEAD~1
rm -rf validators/
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, validation test results on valid/invalid inputs |

---

### CP9: KDP Compliance and Preview

**Goal**: Validate PDF meets KDP specs and provide preview capability

**Deliverables**:
- `validators/kdp-validator.py` - KDP compliance checks
- `preview/preview-generator.py` - Preview capability

**KDP Validation Rules**:

| Rule | Check | Requirement | Mode |
|------|-------|-------------|------|
| K001 | Page size | Exactly 6x9 inches | Both |
| K002 | Inside margin | >= 0.375 inches | Both |
| K003 | Outside margin | >= 0.25 inches | Both |
| K004 | Top margin | >= 0.25 inches | Both |
| K005 | Bottom margin | >= 0.25 inches | Both |
| K006 | Fonts embedded | All bundled fonts embedded | Both |
| K007 | PDF format | Valid PDF structure | Both |
| K008 | Page count | >= 24 pages (publish-ready only) | Publish-ready only (warning) |

**KDP Validation Report**:
```
KDP Compliance Report
=====================
File: output/devotional.pdf

Dimensions:
[✓] K001: Page size 6x9 inches (PASS)

Margins:
[✓] K002: Inside margin 0.5in >= 0.375in (PASS)
[✓] K003: Outside margin 0.5in >= 0.25in (PASS)
[✓] K004: Top margin 0.5in >= 0.25in (PASS)
[✓] K005: Bottom margin 0.5in >= 0.25in (PASS)

Fonts:
[✓] K006: All fonts embedded (PASS)
  - Georgia (Embedded Subset)
  - Times New Roman (Embedded Subset)

Format:
[✓] K007: Valid PDF structure (PASS)

KDP Status: READY FOR UPLOAD
```

**Preview Capability**:
- Generate low-resolution preview PDF
- Display first few pages in terminal (text summary)
- Show page count and structure overview

**Preview Output**:
```
Preview Summary
===============
Title: A Week of Peace
Topic: Finding Peace
Days: 6

Page Structure:
  Page 1: Title Page
  Page 2-3: Day 1 (Monday)
  Page 4-5: Day 2 (Tuesday)
  ...
  Page 12-13: Day 6 (Saturday)

Total Pages: 13
Estimated Print Cost: $X.XX (based on page count)
```

**Files to Stage**:
- `validators/kdp-validator.py`
- `preview/preview-generator.py`
- `examples/sample-validation-report.txt`

**Commit Command**:
```bash
git add validators/kdp-validator.py preview/ examples/sample-validation-report.txt
git commit -m "feat(devotional-generator): add KDP validation and preview (CP9)"
```

**Verification**:
- [ ] KDP validator checks all specs
- [ ] Invalid margins are flagged
- [ ] Missing font embedding is flagged
- [ ] Preview shows structure overview
- [ ] Page count is accurate

**Rollback**:
```bash
git reset --soft HEAD~1
rm validators/kdp-validator.py
rm -rf preview/
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | M (Medium) |
| AI Mitigation | Provide: diff summary, KDP validation report output |
| Elevated Check | Upload sample PDF to KDP preview before final approval |
| Note | Actual KDP upload is Human: Barbara only (account action) |

---

## Acceptance Criteria

### Phase Complete When:

- [ ] Structure validator catches all missing elements (including Turabian attribution fields)
- [ ] Structure validator reports errors vs warnings correctly
- [ ] Structure validator enforces reflection approval status (error for publish-ready, warning for personal)
- [ ] Structure validator flags scripture retrieval failures
- [ ] Structure validator checks front matter completeness (title, copyright, introduction)
- [ ] Structure validator checks Introduction includes Sunday worship guidance when Day 7 present
- [ ] KDP validator checks page dimensions
- [ ] KDP validator checks margins
- [ ] KDP validator checks bundled font embedding
- [ ] KDP validator warns when page count < 24 for publish-ready output
- [ ] Validation rules differ correctly by output mode (personal vs publish-ready)
- [ ] Preview shows structure summary
- [ ] Preview shows page count
- [ ] All validators produce clear reports

---

## Gatekeeper Checklist

**Executor**: AI: Claude Code
**Verifier**: Human: Barbara

### Human Review Required

- [ ] Validation rules are appropriate (not too strict)
- [ ] Reports are easy to read
- [ ] Preview is useful for quick checks

### Verification Reference

See `docs/system/ai.md` for AI executor output requirements.

### Verification Steps

1. Run structure validator on complete devotional - should PASS
2. Run structure validator on incomplete devotional - should FAIL
3. Run KDP validator on correct PDF - should PASS
4. Run KDP validator on wrong-size PDF - should FAIL
5. Generate preview and verify accuracy

---

## Integration Notes

### Validation Workflow

```
Input Data
    ↓
Structure Validation
    ↓ (if PASS)
Template Rendering
    ↓
PDF Generation
    ↓
KDP Validation
    ↓ (if PASS)
Preview
    ↓
Final Export
```

### CLI Usage Example

```bash
# Validate content before generation
python validate.py --content input.json --structure

# Validate PDF after generation
python validate.py --pdf output/devotional.pdf --kdp

# Generate preview
python preview.py output/devotional.pdf

# Full workflow with validation
python generate.py --input input.json --validate --preview
```

---

## Error Messages

### User-Friendly Messages

| Code | Message |
|------|---------|
| V001 | "Missing days: expected 6, found 4. Add content for days 5 and 6." |
| V010 | "Day 5 reflection is empty. Please add reflection content." |
| K001 | "Page size is 8.5x11 inches, expected 6x9 inches. Check page configuration." |
| K006 | "Font 'CustomFont' is not embedded. Use standard fonts or embed the font." |

---

## Notes

### Resolved Questions Affecting This Phase

| Question | Decision | Impact on Phase 004 |
|----------|----------|---------------------|
| Q1 | Turabian attribution | Validate quote presence and attribution completeness (author, source_title required) |
| Q2 | NASB, web-retrieved | Validate fetched text matches reference; flag retrieval failures |
| Q3 | AI-generated; human approval | Enforce approval before export (error for publish-ready, warning for personal) |
| Q4 | Variable day count; dual output modes | Validation rules split by output mode; page count warning for publish-ready below threshold |
| Q5 | Progressive sub-themes | Optional progression validation (info-level) |
| Q6 | Day 7 = Sunday worship | Validate Introduction includes Sunday guidance when Day 7 present |
| Q7 | Mandatory front matter | Validate front matter completeness (title, copyright, introduction) |

### Design Decisions

- Separate structure and KDP validation for clarity
- Run structure validation before PDF generation (fail fast)
- Run KDP validation on generated PDF (verify output)
- Validation severity differs by output mode: publish-ready is strict, personal is relaxed
- Validation rules are configurable (severity can be adjusted)
- Preview is text-based (no GUI in MVP)

---

**Previous Phase**: [003-kdp-pdf-export.md](./003-kdp-pdf-export.md)
**Next Phase**: Project Complete
