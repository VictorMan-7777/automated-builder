# Devotional Generator - Product Requirements Document (PRD)

## Document Information

- **Project**: Devotional Generator
- **Version**: 3.0
- **Date**: 2026-02-07
- **Status**: Planning (Open Questions Resolved)
- **Owner**: Automated Builder Project

## Executive Summary

The Devotional Generator is a system for producing weekly devotional content suitable for self-publishing on Amazon Kindle Direct Publishing (KDP). Each week includes content for 6 days (Monday-Saturday), with each day containing a structured devotional format designed for spiritual reflection.

### Purpose

Generate KDP-ready PDF devotional books with:
- Configurable weekly themes
- Consistent daily structure
- Print-ready formatting for 6x9 inch trim size

### Target Output

A **KDP-ready PDF** that:
- Meets Amazon KDP print book specifications
- Uses 6x9 inch (15.24 x 22.86 cm) trim size
- Includes proper margins, bleed, and formatting
- Is ready for immediate upload to KDP

---

## Problem Statement

### Current Challenges

1. **Manual Devotional Creation** - Writing weekly devotionals is time-consuming
2. **Format Inconsistency** - Manual formatting leads to variations
3. **KDP Compliance** - Ensuring print specifications is tedious and error-prone
4. **Content Organization** - Managing daily elements across a week requires structure
5. **Scalability** - Cannot efficiently produce multiple themed weeks

### User Needs

**Content Creators**:
- Generate themed devotional weeks quickly
- Consistent structure across all days
- Preview before final export

**Self-Publishers**:
- KDP-compliant PDF output
- Correct trim size and margins
- Professional-looking layout

---

## Content Structure

### Daily Devotional Structure

Each day includes these **5 elements** (in order):

| # | Element | Description |
|---|---------|-------------|
| 1 | **Inspirational Quote** | A relevant quote to set the day's tone |
| 2 | **Scripture** | Bible verse(s) related to the theme |
| 3 | **Devotional Reflection** | Prose reflection on the theme and scripture |
| 4 | **Action Steps** | Practical applications (1-3 items) |
| 5 | **Prayer** | Closing prayer for the day |

### Weekly Structure

| Property | Value |
|----------|-------|
| Days per week | 6 (Monday-Saturday, configurable) |
| Theme | One theme per week |
| Continuity | Days should build on each other within the week |

### Example Daily Layout

```
Day 1: Monday

"The only way to do great work is to love what you do."
— Steve Jobs

Scripture
---------
Colossians 3:23-24 (NIV)
"Whatever you do, work at it with all your heart..."

Reflection
----------
[200-400 words of devotional reflection]

Action Steps
------------
1. [Specific action related to theme]
2. [Specific action related to theme]

Prayer
------
[Short closing prayer]
```

---

## System Inputs

### Configurable Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `num_days` | Integer | 6 | Number of days to generate (1-7) |
| `topic` | String | Required | Theme/topic for the week |
| `title` | String | Auto-generated | Book/section title |
| `scripture_version` | String | NASB | Bible translation to use |
| `output_mode` | String | publish-ready | Output mode: `personal` or `publish-ready` |

### Input Example

```yaml
num_days: 6
topic: "Finding Peace in Uncertainty"
title: "A Week of Peace"
scripture_version: "NASB"
output_mode: "publish-ready"
```

---

## Output Specification

### Target Format

**Amazon KDP Print-Ready PDF**

### KDP Requirements

| Specification | Value |
|---------------|-------|
| **Trim Size** | 6 x 9 inches (15.24 x 22.86 cm) |
| **Inside Margins** | 0.375 inches minimum (gutter: 0.5 inches for binding) |
| **Outside Margins** | 0.25 inches minimum |
| **Top/Bottom Margins** | 0.25 inches minimum |
| **Bleed** | None (text-only interior) |
| **Color** | Black & white interior (standard) |
| **Font Size** | 10-12pt body text |
| **Minimum Page Count** | 24 pages (publish-ready output only) |
| **File Format** | PDF/X-1a:2001 or PDF with embedded fonts |

### Page Layout

```
+------------------------------------------+
|              [Top Margin: 0.5"]          |
|  +------------------------------------+  |
|  |  Day 1: Monday                     |  |
|  |                                    |  |
|  |  "Quote text here..."              |  |
|  |  — Attribution                     |  |
|  |                                    |  |
|  |  SCRIPTURE                         |  |
|  |  [Scripture text]                  |  |
|  |                                    |  |
|  |  REFLECTION                        |  |
|  |  [Devotional text...]              |  |
|  |                                    |  |
|  |  ACTION STEPS                      |  |
|  |  1. [Action]                       |  |
|  |  2. [Action]                       |  |
|  |                                    |  |
|  |  PRAYER                            |  |
|  |  [Prayer text]                     |  |
|  +------------------------------------+  |
|              [Bottom Margin: 0.5"]       |
|  [Gutter]                    [Outside]   |
+------------------------------------------+
     6 inches wide
```

---

## Functional Requirements

### FR-1: Content Generation

**FR-1.1**: Accept configurable inputs
- Number of days (default: 6)
- Topic/theme (required)
- Scripture version (default: NIV)

**FR-1.2**: Generate daily content structure
- All 5 elements present for each day
- Elements in correct order
- Theme continuity across days

**FR-1.3**: AI content generation with human approval
- Devotional reflections are AI-generated with expanded references
- All AI-generated content requires human approval before export
- System tracks approval status (pending | approved) per reflection
- No PDF export permitted for unapproved content

**FR-1.4**: Quote Verification Gate
- No publish-ready export permitted unless all quotes have `verification_status = human_approved` and `public_domain = true`

### FR-2: Template System

**FR-2.1**: Weekly template
- Container for 6 daily devotionals
- Theme metadata
- Book metadata (title, author, etc.)

**FR-2.2**: Daily template
- 5-element structure
- Consistent formatting
- Variable placeholders

**FR-2.3**: Template validation
- Ensure all required elements present
- Validate structure before export

### FR-3: PDF Export

**FR-3.1**: KDP-compliant PDF generation
- 6x9 inch page size
- Correct margins (inside/outside/top/bottom)
- Embedded fonts
- No bleed for text-only interior

**FR-3.2**: Professional layout
- Consistent typography
- Section headers
- Page breaks at logical points
- Page numbers

**FR-3.3**: Book components
- Title page (mandatory)
- Copyright page (mandatory)
- Introduction (mandatory; includes Sunday worship guidance when Day 7 is present)
- Table of contents (conditional; include for larger books, e.g., >= 12 days)
- Daily devotional pages

### FR-4: Validation

**FR-4.1**: Pre-export validation
- All content elements populated
- Theme consistency
- Word count within bounds

**FR-4.2**: KDP specification check
- Page dimensions correct
- Margins compliant
- Font embedding verified

---

## Non-Functional Requirements

### NFR-1: Performance
- Generate weekly devotional structure in under 30 seconds
- Export to PDF in under 2 minutes

### NFR-2: Reliability
- 99% export success rate for valid inputs
- Clear error messages for failures
- Rollback capability

### NFR-3: Maintainability
- Modular architecture
- Clear separation between content and formatting
- Template-driven layout

### NFR-4: Extensibility
- Easy to add new content elements
- Configurable page layouts
- Multiple output format support (future)

---

## Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D001 | 6-day default (Mon-Sat); Day 7 = Sunday worship integration | Common devotional pattern; Day 7 guidance in Introduction |
| D002 | 5-element daily structure | Covers quote, scripture, reflection, action, prayer |
| D003 | 6x9 inch trim | Most common KDP devotional size |
| D004 | PDF as primary output | KDP requires PDF for print |
| D005 | NASB as default version | Respected literal translation; web-retrieved |
| D006 | Quote sourcing governed by human-approved author whitelist with public domain verification. AI may not select quotes from memory or uncataloged sources. | Q1 audit (2026-02-07): mitigates copyright, theological drift, and fabrication risks |

---

## Resolved Questions (Q1–Q13)

All open questions were resolved in Planner Iteration 3. See `docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` for full decision rationale.

| # | Question | Decision | Source |
|---|----------|----------|--------|
| Q1 | Source for inspirational quotes | Classical evangelical authors from a **human-approved author whitelist**, sourced from **websites hosting public domain works**. Quotes restricted to **verified public domain editions** for publish-ready output. Turabian attribution required. All quotes require **source-level verification** before export. | Iteration 3 |
| Q2 | Scripture auto-fetched or user-provided? | NASB, retrieved from the web | Iteration 3 |
| Q3 | AI-generated or template reflections? | AI-generated with expanded references; human approval required before export | Iteration 3 |
| Q4 | How many weeks per book? | Variable by day count; publish-ready requires >= 12 days; personal use exempt | Iteration 3 |
| Q5 | Sub-themes or shared theme? | Progressive (days build on weekly theme); optional `day_focus` field | Iteration 3 |
| Q6 | Is a 7th day (Sunday) needed? | Day 7 integrates with Sunday worship; guidance included in Introduction | Iteration 3 |
| Q7 | Front matter requirements | Title, Copyright, Introduction (mandatory); TOC for larger books | Iteration 3 |
| Q8 | Print-only or also ebook? | PDF only | Iteration 3 |
| Q9 | Black & white or color? | Black & white | Iteration 3 |
| Q10 | ISBN and barcode handling | Amazon-provided ISBN; Amazon barcode; Bowker deferred until profitable | Iteration 3 |
| Q11 | One day per page or dynamic? | Each day starts on a new page, may span multiple pages | Iteration 3 |
| Q12 | Font selection | Bundled open-source fonts | Iteration 3 |
| Q13 | Header/footer content | Page numbers only | Iteration 3 |

---

## Assumptions

Resolved per Planner Iteration 3 (Q1–Q13):

1. **Quotes**: Classical evangelical authors from identified open-source websites; Turabian attribution required. Governed by author whitelist (human-verified); publish-ready output restricted to copyright-cleared, source-verified quotes only.
2. **Scripture**: NASB, web-retrieved
3. **Reflections**: AI-generated with expanded references; human approval required before export
4. **Weeks per book**: Variable day count; publish-ready output requires >= 12 days; personal use mode relaxes this
5. **Front matter**: Title, Copyright, Introduction (mandatory); TOC conditional for larger books
6. **Output**: PDF only (no ebook)
7. **Interior**: Black & white
8. **Page breaks**: Each day starts on a new page (may span multiple pages)
9. **Fonts**: Bundled open-source fonts
10. **Headers**: Page numbers only

---

## Out of Scope (v1.0)

Explicitly not included:

- Ebook export (EPUB/MOBI)
- Cover design
- ISBN generation via Bowker (use Amazon-provided ISBN for MVP; Bowker deferred until profitable)
- Print-on-demand integration
- Web-based UI
- Database backend
- Multi-language support

### Reclassified (moved into scope by Iteration 3)

| Item | Previous Status | New Status | Decision |
|------|----------------|------------|----------|
| AI-generated devotional content | Out of scope | In scope | Q3: AI-generated with human approval |
| Scripture API integration | Out of scope | In scope | Q2: NASB web retrieval |
| Multi-week compilation | Out of scope | Partially in scope | Q4: Variable day count across weeks |

---

## Success Criteria

### MVP Criteria

- [ ] Accept topic and num_days inputs
- [ ] Generate 6-day weekly structure
- [ ] Include all 5 daily elements
- [ ] Export KDP-compliant 6x9 PDF
- [ ] Pass basic KDP upload validation

### Quality Metrics

| Metric | Target |
|--------|--------|
| PDF generation success rate | 95%+ |
| KDP validation pass rate | 100% |
| Content structure completeness | 100% |

---

## Constraints

1. **Planning only** - No content generation implementation
2. **KDP compliance** - Must meet Amazon specifications
3. **MVP focus** - Minimal viable structure first
4. **Docs-only stage** - No code in current phase
5. **Quote sourcing** - Quotes must be selected exclusively from the verified Quote Catalog. AI-generated or AI-recalled quotes are prohibited.

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

---

## Related Documents

- [Roadmap](./roadmap.md) - Phased implementation plan
- [Iteration Log](./iteration-log.md) - Planning evolution
- [Phase Plans](./phases/) - Detailed phase documentation

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 3.0 | 2026-02-07 | Claude Code | Applied Iteration 3 decisions (Q1–Q13): resolved all open questions, updated assumptions, decisions, FRs, inputs, out of scope, KDP table |
| 2.0 | 2026-02-06 | Planner | Major revision: Added quote element, weekly structure, KDP specs, open questions |
| 1.0 | 2026-02-05 | Automated Builder | Initial PRD |
