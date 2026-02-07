# Devotional Generator - Project Roadmap

## Document Information

- **Project**: Devotional Generator
- **Version**: 3.0
- **Date**: 2026-02-07
- **Status**: Planning (Open Questions Resolved)

## Overview

This roadmap defines the four-phase implementation plan for producing KDP-ready devotional PDFs. Each phase builds incrementally toward a complete production pipeline, with clear commit points, acceptance criteria, and rollback procedures.

**Target**: Generate a 6x9 inch KDP-compliant PDF containing themed devotional content (variable day count; 6-day default with optional Day 7 Sunday worship integration). Supports personal use and publish-ready output modes.

---

## Roadmap Principles

### Incremental Development

- Each phase delivers working functionality
- Commit points enable rollback to stable states
- No phase depends on incomplete future work

### Quality Gates

- Acceptance criteria at each phase
- Human/AI review checkpoints
- Validation before proceeding

### MVP Focus

- Implement minimum viable features first
- KDP compliance is non-negotiable
- Defer complexity until core pipeline works

---

## Phase Overview

| Phase | Name | Commit Points | Description |
|-------|------|---------------|-------------|
| 001 | Data Model & Inputs | CP1-CP2 | Input schema, weekly/daily data structures |
| 002 | Template System | CP3-CP4 | Weekly container, 5-element daily template |
| 003 | KDP PDF Export | CP5-CP7 | 6x9 layout, margins, fonts, PDF generation |
| 004 | Validation & Preview | CP8-CP9 | Pre-export checks, KDP compliance validation |

**Total Commit Points**: 9

---

## Phase Details

### Phase 001: Data Model & Inputs

**Goal**: Define input parameters and data structures for devotionals

**Deliverables**:
- Input schema (num_days, topic, title, scripture_version, output_mode, author_name)
- Weekly data model (variable day count, introduction content, conditional TOC)
- Daily data model (5-element structure with Turabian attribution, NASB scripture, approval status, day_focus)
- Configuration system

**Commit Points**:
- **CP1**: Input schema and configuration
- **CP2**: Weekly and daily data models

**Key Decisions**:
- num_days defaults to 6 (Monday-Saturday); Day 7 = Sunday worship integration
- topic is required, title is auto-generated if not provided
- Daily structure: quote (Turabian attribution), scripture (NASB default, web-retrieved), reflection (AI-generated, approval tracking), action_steps, prayer
- output_mode: personal vs publish-ready
- day_focus: optional progressive sub-theme per day

**Dependencies**: None

**See**: [phases/001-data-model-inputs.md](./phases/001-data-model-inputs.md)

---

### Phase 002: Template System

**Goal**: Create templates for weekly and daily devotional structure

**Deliverables**:
- Weekly template (title, theme, days container)
- Daily template (5 elements with Turabian quote attribution, day focus, approval status)
- Front matter templates (title page, copyright page, Introduction, conditional TOC)
- Template rendering engine
- Placeholder system for content (draft/preview and approved states)
- Font specification for bundled open-source fonts
- Page break and numbering rules

**Commit Points**:
- **CP3**: Weekly template structure
- **CP4**: Daily template with 5 elements

**Key Decisions**:
- Templates define structure, not content
- Templates support draft/preview (pending approval) and approved states
- Front matter: title, copyright, Introduction (mandatory); TOC (conditional)
- Introduction includes Sunday worship guidance when Day 7 present
- Page numbers: Roman/suppressed for front matter, Arabic for content

**Dependencies**: Phase 001 complete

**See**: [phases/002-template-system.md](./phases/002-template-system.md)

---

### Phase 003: KDP PDF Export

**Goal**: Generate KDP-compliant 6x9 inch PDF with full front matter

**Deliverables**:
- Page layout system (6x9 with margins)
- PDF generation engine
- Bundled open-source font embedding
- Page numbering (Roman for front matter, Arabic for content)
- Front matter generation (title, copyright, Introduction, conditional TOC)
- Scripture web retrieval (NASB) — or designated as new phase
- AI content generation pipeline — or designated as new phase
- Conditional KDP validation based on output mode

**Commit Points**:
- **CP5**: Page layout and margins (6x9, KDP specs)
- **CP6**: PDF generation with bundled fonts
- **CP7**: Front matter and page numbers

**KDP Specifications**:
- Trim: 6 x 9 inches
- Inside margin (gutter): 0.5 inches
- Outside margin: 0.25 inches
- Top/bottom margins: 0.5 inches
- Embedded fonts required
- PDF/X-1a or embedded fonts

**Dependencies**: Phase 002 complete

**See**: [phases/003-kdp-pdf-export.md](./phases/003-kdp-pdf-export.md)

---

### Phase 004: Validation & Preview

**Goal**: Ensure output quality and KDP compliance before final export

**Deliverables**:
- Pre-export validation (structure completeness, Turabian attribution, approval status)
- Output-mode-aware validation (publish-ready vs personal)
- KDP compliance checker (margins, fonts, dimensions, page count)
- Scripture retrieval validation (fetched text matches reference)
- Front matter validation (completeness, Sunday guidance when Day 7 present)
- Preview capability (view before export)
- Validation reporting

**Commit Points**:
- **CP8**: Structure validation (all elements present, approval enforcement)
- **CP9**: KDP compliance validation and preview

**Validation Checks**:
- All 5 daily elements populated (including Turabian attribution fields)
- Reflection approval_status = approved (error for publish-ready, warning for personal)
- Scripture retrieval success
- Front matter completeness
- All days present for num_days
- Page dimensions correct
- Margins meet KDP minimums
- Bundled fonts embedded correctly
- Page count >= 24 for publish-ready (warning)

**Dependencies**: Phase 003 complete

**See**: [phases/004-validation-preview.md](./phases/004-validation-preview.md)

---

## Commit Point Summary

| ID | Phase | Description | Files |
|----|-------|-------------|-------|
| CP1 | 001 | Input schema and configuration | config/, schema/ |
| CP2 | 001 | Weekly and daily data models | models/ |
| CP3 | 002 | Weekly template structure | templates/ |
| CP4 | 002 | Daily template with 5 elements | templates/ |
| CP5 | 003 | Page layout (6x9, margins) | layout/ |
| CP6 | 003 | PDF generation with fonts | export/ |
| CP7 | 003 | Title page and page numbers | export/ |
| CP8 | 004 | Structure validation | validators/ |
| CP9 | 004 | KDP compliance and preview | validators/, preview/ |

---

## Critical Path

The following sequence represents the critical path:

```
CP1 (Input Schema)
 └──> CP2 (Data Models)
       └──> CP3 (Weekly Template)
             └──> CP4 (Daily Template)
                   └──> CP5 (Page Layout)
                         └──> CP6 (PDF Generation)
                               └──> CP7 (Title/Pages)
                                     └──> CP8 (Validation)
                                           └──> CP9 (KDP Check)
```

All phases are sequential; each depends on the previous.

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

---

## Success Metrics by Phase

### Phase 001
- [ ] Input schema accepts num_days and topic
- [ ] Weekly model contains days array
- [ ] Daily model has all 5 elements

### Phase 002
- [ ] Weekly template renders with theme
- [ ] Daily template shows all 5 elements
- [ ] Placeholders clearly marked

### Phase 003
- [ ] PDF is 6x9 inches
- [ ] Margins meet KDP specs
- [ ] Fonts embedded correctly
- [ ] Page numbers present

### Phase 004
- [ ] Validation catches missing elements
- [ ] KDP checker flags margin violations
- [ ] Preview shows formatted output

---

## Dependencies

### Technical Dependencies

| Dependency | Purpose | Phase |
|------------|---------|-------|
| PDF library (WeasyPrint or ReportLab) | PDF generation | 003 |
| JSON Schema | Input validation | 001 |
| Jinja2 or similar | Template rendering | 002 |
| Bible API or web source | NASB scripture retrieval (Q2) | 003 |
| Claude API or AI model | Reflection generation (Q3) | 003 |
| Bundled open-source fonts | Font embedding (Q12) | 003 |

### System Dependencies (for PDF)

- WeasyPrint requires: Cairo, Pango
- ReportLab: No system dependencies

---

## Resolved Questions Affecting Roadmap

All 13 open questions (Q1–Q13) were resolved in Planner Iteration 3. Key impacts:

| Decision | Impact on Roadmap |
|----------|-------------------|
| Q1: Turabian attribution | Phase 001 schema, Phase 002 rendering, Phase 004 validation |
| Q2: NASB web retrieval | Phase 003 scope expanded (scripture retrieval); new dependency |
| Q3: AI-generated reflections | Phase 003 scope expanded (AI pipeline); Phase 004 approval enforcement |
| Q4: Variable day count, dual output modes | All phases: output_mode parameter, conditional validation |
| Q6: Day 7 Sunday worship | Phase 001 model, Phase 002 Introduction template, Phase 004 validation |
| Q7: Full front matter | Phase 003 CP7 expanded: title, copyright, Introduction, conditional TOC |
| Q12: Bundled open-source fonts | Phase 003 CP6: font bundling replaces system fonts |

See `docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` for full decisions.

---

## Risk Management

### High-Priority Risks

1. **PDF Generation Complexity**
   - **Mitigation**: Test WeasyPrint early; have ReportLab as fallback
   - **Trigger**: CP6 exceeds time budget

2. **KDP Rejection**
   - **Mitigation**: Build validation into CP9; test upload early
   - **Trigger**: PDF fails KDP preview

3. **Font Embedding Issues**
   - **Mitigation**: Use bundled open-source fonts; test embedding
   - **Trigger**: Fonts not displaying correctly

4. **NASB Copyright Restrictions** (Q2)
   - **Mitigation**: Human-only legal review required before publication; track Lockman Foundation quotation limits
   - **Trigger**: Published output exceeds NASB usage limits

5. **AI Theological Accuracy** (Q3)
   - **Mitigation**: Mandatory human approval gate; no export without approval
   - **Trigger**: AI-generated reflection contains theological errors

6. **Scripture Retrieval Failures** (Q2)
   - **Mitigation**: Graceful error handling; clear failure messages; validation catches missing text
   - **Trigger**: Network or API issues block generation

7. **Quote Source Availability** (Q1)
   - **Mitigation**: Verify source list in `projects/inactive-projects`; consider pre-caching quote catalog
   - **Trigger**: Open-source websites become unavailable

---

## Post-MVP Enhancements

After core pipeline works:

- Ebook export (EPUB/MOBI)
- Cover design integration
- Content library (pre-cataloged quotes from identified websites)
- Bowker ISBN integration (deferred until profitable)
- Multi-language support

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.0 | 2026-02-07 | Claude Code | Applied Iteration 3 decisions: updated deliverables, dependencies, risks, post-MVP list |
| 2.0 | 2026-02-06 | Planner | Major revision: 4-phase KDP-focused roadmap |
| 1.0 | 2026-02-05 | Automated Builder | Initial 5-phase roadmap |
