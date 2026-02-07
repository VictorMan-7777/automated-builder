# Planner Iteration 3 — Open Questions Q1–Q13

## Document Information

- **Project**: Devotional Generator
- **Iteration**: 3
- **Date**: 2026-02-07
- **Status**: PENDING HUMAN REVIEW
- **Source**: PRD v2.0 (`docs/projects/devotional-generator/prd.md`)
- **Executor**: AI: Claude Code
- **Reviewer**: Human: Barbara

---

## Purpose

This artifact presents proposed decisions for Open Questions Q1–Q13 as defined in the Devotional Generator PRD v2.0. Each entry restates the original question, proposes a decision, and lists tradeoffs and risks.

This document is for human review only. It does not imply approval. No artifacts have been modified.

---

## Content Source Questions

### Q1

**Question:** What is the source for inspirational quotes?

**Options (per PRD):** Public domain, licensed, user-provided

**Proposed Decision:** User-provided

**Tradeoffs:**

- User-provided eliminates all legal/licensing risk and external dependencies.
- User-provided requires manual effort for each day's quote.
- Public domain would enable automation but requires building a quote database and verifying attribution.
- Licensed sources introduce cost and legal review requirements.

**Risks:**

- The data model must include both `quote_text` and `quote_attribution` fields. The PRD does not currently specify whether attribution is required.
- If quotes are user-provided, validation must detect missing quotes before export.

**Affected Artifacts:**

- Phase 001 — daily element schema
- Phase 002 — quote rendering in template
- Phase 004 — quote presence validation

**Status:** RESOLVED

---

### Q2

**Question:** Should scripture text be auto-fetched or user-provided?

**Options (per PRD):** API integration vs manual

**Proposed Decision:** User-provided

**Tradeoffs:**

- User-provided eliminates external API dependency, API key management, and network requirements.
- User-provided requires manual text entry and does not support automatic version switching.
- API integration would automate text retrieval but adds phase complexity and an external dependency.

**Risks:**

- The PRD defines `scripture_version` as a configurable parameter. With user-provided text, this field becomes metadata (labeling what the user pasted), not a functional selector. This distinction must be clarified in the data model.
- Some Bible translations have copyright restrictions on quotation volume in published works. This is a human-only legal concern outside the system's scope.

**Affected Artifacts:**

- Phase 001 — scripture field definitions (`scripture_reference`, `scripture_version`, `scripture_text`)
- Phase 002 — scripture rendering layout
- Phase 004 — scripture completeness checks
- PRD System Inputs table — clarify `scripture_version` role

**Status:** RESOLVED

---

### Q3

**Question:** Will devotional reflections be AI-generated or templates?

**Options (per PRD):** AI (Claude) vs human-written placeholders

**Proposed Decision:** Human-written with structured placeholders

**Tradeoffs:**

- Human-written ensures theological accuracy and authentic voice.
- Placeholders are slower to fill but match the PRD's stated scope ("provides structure, not content").
- AI-generated content would be faster but introduces theological accuracy risk and is explicitly listed as Out of Scope v1.0.

**Risks:**

- Placeholder quality affects usability. Placeholders should include word count guidance and thematic prompts (e.g., `[200-400 word reflection on {topic} connecting to {scripture_reference}]`).
- Validation must distinguish between "placeholder present" and "final content present."

**Affected Artifacts:**

- Phase 001 — reflection field definition and placeholder format
- Phase 002 — placeholder rendering vs final content rendering
- Phase 004 — placeholder vs final content validation logic

**Status:** RESOLVED

---

## Structure Questions

### Q4

**Question:** How many weeks per book?

**Options (per PRD):** Single week vs multi-week compilation

**Proposed Decision:** Single week per generation

**Tradeoffs:**

- Single week is simpler in data model, validation, and generation pipeline.
- Single week may produce only 8–18 pages, potentially below KDP's 24-page minimum for print books.
- Multi-week compilation produces a more substantial product but significantly increases data model and validation complexity.

**Risks:**

- KDP requires a minimum of 24 printed pages for print books. This constraint is not currently captured in the PRD's KDP Requirements table.
- Mitigation: front/back matter, longer reflections, or post-MVP multi-week compilation.
- The data model should be designed so multi-week compilation is a natural future extension.

**Affected Artifacts:**

- Phase 001 — book-level vs week-level data model
- Phase 003 — page count validation against KDP minimum
- Phase 004 — page count check
- PRD KDP Requirements table — add minimum page count constraint

**Status:** RESOLVED

---

### Q5

**Question:** Should days have sub-themes or share the week's theme?

**Options (per PRD):** Unified vs progressive

**Proposed Decision:** Progressive (days build on the weekly theme)

**Tradeoffs:**

- Progressive provides a richer reading experience and narrative arc across the week.
- Progressive requires sub-theme planning and makes day ordering significant.
- Unified is simpler but contradicts the PRD's existing language ("days should build on each other within the week").

**Risks:**

- Each day needs an optional `day_focus` field. If not provided, it defaults to the weekly topic.
- Placeholder generation should suggest a progression arc (e.g., Day 1: Introduction → Day 6: Application/Commitment).

**Affected Artifacts:**

- Phase 001 — add `day_focus` field to daily schema
- Phase 002 — render day focus/sub-theme
- Phase 004 — optional progression validation

**Status:** RESOLVED

---

### Q6

**Question:** Is a 7th day (Sunday) ever needed?

**Options (per PRD):** 6-day only vs configurable 7

**Proposed Decision:** Configurable 1–7 via existing `num_days` parameter, default 6

**Tradeoffs:**

- Configurable supports diverse use cases without increasing complexity significantly.
- The `num_days` parameter (range 1–7) already exists in the PRD, implying this is the intended design.
- Hard-coding 6 days would be simpler but unnecessarily restrictive.

**Risks:**

- Decision D001 ("6-day week Mon–Sat") should be clarified as defining the default, not a hard constraint.
- Day labeling for 7-day case: if `num_days` = 7, Day 7 maps to Sunday. Weekday mapping starts at Monday.

**Affected Artifacts:**

- Phase 001 — input validation range confirmation
- Phase 002 — day labeling logic for 1–7 days
- PRD Decisions table — clarify D001 as default, not constraint

**Status:** RESOLVED

---

## KDP Questions

### Q7

**Question:** Front matter requirements?

**Options (per PRD):** Title only vs full (copyright, TOC, intro)

**Proposed Decision:** Title page + Copyright page for MVP

**Tradeoffs:**

- Title + Copyright is the professional minimum for KDP books.
- Copyright page adds one page toward the 24-page minimum.
- Full front matter (TOC, intro) increases scope beyond MVP needs.
- Title-only may appear unprofessional and could delay KDP review.

**Risks:**

- Copyright page requires `author_name` as a new input field.
- This revises PRD Assumption #5 ("Title page only").
- TOC and Introduction are deferred, not rejected.

**Affected Artifacts:**

- Phase 001 — add `author_name` input field
- Phase 002 — title page and copyright page templates
- Phase 003 — front matter page generation and ordering
- PRD Assumption #5 — revise
- PRD FR-3.3 — mark copyright page as included, not optional

**Status:** RESOLVED

---

### Q8

**Question:** Print-only or also ebook?

**Options (per PRD):** PDF only vs also EPUB/MOBI

**Proposed Decision:** PDF only

**Tradeoffs:**

- PDF only is the simplest pipeline and aligns with the stated project scope.
- Ebook export (EPUB/MOBI) would broaden distribution but adds significant complexity with different formatting rules.

**Risks:**

- None. This is unambiguously stated in the PRD (Out of Scope, Assumption #6, Decision D004).

**Affected Artifacts:**

- None. Existing artifacts already reflect this decision.

**Status:** RESOLVED

---

### Q9

**Question:** Black & white or color interior?

**Options (per PRD):** B&W (cheaper) vs color

**Proposed Decision:** Black & white

**Tradeoffs:**

- B&W has ~6x lower print cost per page than color.
- B&W is standard for text-only devotionals.
- Color would only benefit illustrated content, which is not in scope.

**Risks:**

- None. Already specified in the PRD KDP Requirements table and Assumption #7.

**Affected Artifacts:**

- None. Existing artifacts already reflect this decision.

**Status:** RESOLVED

---

### Q10

**Question:** ISBN and barcode handling?

**Options (per PRD):** System generates vs user provides

**Proposed Decision:** Out of scope for MVP

**Tradeoffs:**

- ISBNs are not required in the interior PDF. KDP handles ISBN assignment during the upload process.
- Barcodes appear on the cover, which is out of scope.
- System-generated ISBNs would require Bowker integration and associated costs.

**Risks:**

- None. Already listed in the PRD's Out of Scope section.

**Affected Artifacts:**

- None. Existing artifacts already reflect this decision.

**Status:** RESOLVED

---

## Design Questions

### Q11

**Question:** One day per page or content-driven page breaks?

**Options (per PRD):** Fixed vs dynamic layout

**Proposed Decision:** Each day starts on a new page, may span multiple pages

**Tradeoffs:**

- Starting each day on a new page provides clean visual separation and professional layout.
- Content may span multiple pages, accommodating varying reflection lengths.
- Fixed one-page-per-day would constrain content length artificially.
- Fully dynamic breaks would allow days to run together, reducing readability.

**Risks:**

- Partial blank pages at the end of shorter days increase page count but may appear as wasted space.
- Interacts with Q4 page count concern: more page breaks means more pages, which helps meet the 24-page minimum but also increases print cost.

**Affected Artifacts:**

- Phase 002 — page break rules between days
- Phase 003 — page break implementation in PDF generation

**Status:** RESOLVED

---

### Q12

**Question:** Font selection?

**Options (per PRD):** System fonts vs bundled fonts

**Proposed Decision:** Bundled open-source fonts

**Tradeoffs:**

- Bundled fonts guarantee consistent rendering and reliable PDF embedding across all platforms.
- System fonts vary by platform and may not embed correctly, risking KDP rejection.
- Bundled fonts add font files to the repository but eliminate platform-dependent behavior.

**Risks:**

- KDP requires embedded fonts (FR-3.1, KDP Requirements table). System fonts may not embed reliably depending on the PDF library and font licensing.
- Specific font choices (e.g., Lora, EB Garamond, Crimson Text for body; Playfair Display for headings) are deferred to the implementation phase. The decision here is the approach: bundled, open-source, embeddable.
- This revises PRD Assumption #9 ("System fonts with fallbacks").

**Affected Artifacts:**

- Phase 002 — font specification in templates
- Phase 003 — font bundling and embedding implementation
- PRD Assumption #9 — revise

**Status:** RESOLVED

---

### Q13

**Question:** Header/footer content?

**Options (per PRD):** Page numbers only vs decorative

**Proposed Decision:** Page numbers only

**Tradeoffs:**

- Page numbers only is clean, standard for devotionals, and simple to implement.
- Decorative headers (book title, section names, ornaments) add polish but increase template complexity.
- Running headers require page-type-aware logic (front matter vs content pages).

**Risks:**

- Front matter pages conventionally use Roman numerals or no page numbers; content pages use Arabic numerals. This distinction needs specification in template design.
- First page of each day/section may suppress page numbers per publishing convention. This adds minor layout complexity.

**Affected Artifacts:**

- Phase 002 — header/footer template definition
- Phase 003 — page numbering implementation

**Status:** RESOLVED

---

## Summary

| # | Question | Proposed Decision | Status |
|---|----------|-------------------|--------|
| Q1 | What is the source for inspirational quotes? | User-provided | RESOLVED |
| Q2 | Should scripture text be auto-fetched or user-provided? | User-provided | RESOLVED |
| Q3 | Will devotional reflections be AI-generated or templates? | Human-written with structured placeholders | RESOLVED |
| Q4 | How many weeks per book? | Single week per generation | RESOLVED |
| Q5 | Should days have sub-themes or share the week's theme? | Progressive (sub-themes under weekly theme) | RESOLVED |
| Q6 | Is a 7th day (Sunday) ever needed? | Configurable 1–7, default 6 | RESOLVED |
| Q7 | Front matter requirements? | Title page + Copyright page | RESOLVED |
| Q8 | Print-only or also ebook? | PDF only | RESOLVED |
| Q9 | Black & white or color interior? | Black & white | RESOLVED |
| Q10 | ISBN and barcode handling? | Out of scope | RESOLVED |
| Q11 | One day per page or content-driven page breaks? | Day starts on new page, may span | RESOLVED |
| Q12 | Font selection? | Bundled open-source fonts | RESOLVED |
| Q13 | Header/footer content? | Page numbers only | RESOLVED |

---

## PRD Revisions Implied

These revisions are identified but **not applied**:

| Item | Current State | Proposed Change |
|------|---------------|-----------------|
| Assumption #5 | Title page only | Title page + Copyright page |
| Assumption #9 | System fonts with fallbacks | Bundled open-source fonts |
| KDP Requirements table | No minimum page count listed | Add 24-page minimum constraint |
| Decision D001 | "6-day week (Mon–Sat)" | Clarify as default, not hard constraint |
| FR-3.3 | Copyright page listed as optional | Mark as included in MVP |
| Decisions table | D001–D005 | Add D006–D018 for resolved questions |

---

## Cross-Cutting Risk

**KDP 24-page minimum:** A single 6-day week with 2 front matter pages may produce only 8–18 pages, below the KDP print minimum of 24. This risk affects Phase 003 and Phase 004 and should be tracked in the roadmap.

---

## End of Output

This artifact is pending human review. No further analysis, artifact modification, or implementation planning will proceed until approval is received.
