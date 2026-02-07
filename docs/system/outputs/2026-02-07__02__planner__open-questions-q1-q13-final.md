# Planner Iteration 3 — Open Questions Q1–Q13 (Final)

## Document Information

- **Project**: Devotional Generator
- **Iteration**: 3 (Final)
- **Date**: 2026-02-07
- **Status**: PENDING FINAL HUMAN REVIEW
- **Source**: PRD v2.0 (`docs/projects/devotional-generator/prd.md`)
- **Prior Artifact**: `docs/system/outputs/2026-02-07__01__planner__open-questions-q1-q13.md`
- **Executor**: AI: Claude Code
- **Reviewer**: Human: Barbara
- **Note**: All decisions in this artifact reflect authoritative human answers provided by Barbara. AI-proposed decisions from the prior artifact have been replaced.

---

## Purpose

This artifact finalizes Open Questions Q1–Q13 for the Devotional Generator PRD v2.0. Each question restates the original PRD text, records the human-provided decision, and identifies tradeoffs, risks, and affected artifacts.

This document is for final human review. It does not imply approval of downstream changes. No existing artifacts have been modified.

---

## Content Source Questions

### Q1

**Question:** What is the source for inspirational quotes?

**Options (per PRD):** Public domain, licensed, user-provided

**Decision (Human):** Classical evangelical authors sourced from open-source websites identified in the devotional-generator project (`projects/inactive-projects`). Attribution is required and must be in Turabian format.

**Tradeoffs:**

- Sourcing from identified open-source websites provides a curated, theologically aligned quote pool without licensing cost.
- Turabian attribution format is a recognized academic/publishing standard, adding credibility to the published output.
- This approach requires building or referencing a quote catalog from the specified websites.
- Automation potential: quotes could be pre-cataloged or fetched from identified sites, reducing per-day manual effort compared to fully user-provided.

**Risks:**

- The open-source websites in `projects/inactive-projects` must be verified as still accessible and correctly identified. If those references are outdated, the source list needs updating.
- "Open-source websites" does not guarantee public domain. Usage terms for each site must be verified (human-only legal concern).
- The data model must support structured attribution fields compatible with Turabian format (author, title, publication, date, etc.), not just a free-text attribution string.
- Classical evangelical authors narrows the quote pool. The system should validate that a quote source is provided for each day.
- **Audit note (2026-02-07):** The personal-use output (Jan 2026) demonstrated that without an enforced whitelist, the AI selects authors outside the intended scope — including copyrighted, non-evangelical, and unverified sources. The Q1 decision requires operationalization through an author whitelist and quote catalog, not just a policy statement.

**Affected Artifacts:**

- Phase 001 — daily element schema: quote fields must support Turabian-structured attribution (author, source title, publication year, page/URL as applicable)
- Phase 002 — quote rendering must format attribution in Turabian style
- Phase 004 — validation must check quote presence and attribution completeness
- PRD Assumption #1 — revise from "User-provided or placeholder text" to reflect this decision
- `projects/inactive-projects` — referenced as source for website list (must be verified, not modified)
- New artifact required: `author-whitelist.csv` (human-verified)
- New artifact required: `quote-catalog.csv` (pre-verified quotes with Turabian metadata)
- Phase 004 validation must enforce whitelist and catalog compliance

**Status:** APPROVED (Human)

---

### Q2

**Question:** Should scripture text be auto-fetched or user-provided?

**Options (per PRD):** API integration vs manual

**Decision (Human):** Scripture should be NASB and retrieved from the web.

**Tradeoffs:**

- Web retrieval automates scripture text entry, reducing manual effort and transcription errors.
- NASB (New American Standard Bible) is a respected literal translation well-suited to devotional study.
- Web retrieval introduces an external dependency (network access, source website availability).
- Fetching from the web requires identifying a reliable, permissible scripture source (API or scraping target).

**Risks:**

- NASB text is copyrighted by the Lockman Foundation. Published use has quotation limits (typically 500 verses or 25% of a book, whichever is less, without written permission). This is a human-only legal concern that must be tracked.
- The PRD's `scripture_version` parameter default changes from NIV to NASB. This affects PRD Decision D005.
- A reliable web source for NASB text must be identified. Options include public Bible APIs (e.g., API.Bible, Bible Gateway) or designated websites. API key management may be required.
- Network failures during scripture retrieval need graceful handling (clear error, not silent omission).
- This reverses the PRD's Out of Scope item "Scripture API integration" — that item must be removed or reclassified.

**Affected Artifacts:**

- Phase 001 — scripture fields: `scripture_reference`, `scripture_version` (default: NASB), `scripture_text` (auto-populated)
- Phase 002 — scripture rendering layout (unchanged structurally)
- Phase 003 or new phase — scripture web retrieval implementation
- Phase 004 — validation must verify fetched text matches reference; flag retrieval failures
- PRD Decision D005 — change default from NIV to NASB
- PRD Assumption #2 — revise from "User-provided with reference" to "NASB, web-retrieved"
- PRD Out of Scope — remove or reclassify "Scripture API integration"
- PRD System Inputs table — update `scripture_version` default to NASB

**Status:** APPROVED (Human)

---

### Q3

**Question:** Will devotional reflections be AI-generated or templates?

**Options (per PRD):** AI (Claude) vs human-written placeholders

**Decision (Human):** Reflections should be AI-generated with expanded references. All reflections require human approval before publication.

**Tradeoffs:**

- AI generation enables rapid content production at scale, supporting the project's automation goals.
- Expanded references enrich the devotional quality and provide readers with further study material.
- Mandatory human approval mitigates theological accuracy and tone risks inherent in AI-generated spiritual content.
- This approach creates a two-stage workflow: generate then review/approve.

**Risks:**

- AI-generated devotional content carries theological accuracy risk. The human approval gate is the primary mitigation.
- "Expanded references" needs definition: does this mean additional scripture cross-references, citations of theological works, or both? This should be clarified in the content specification.
- The system must clearly mark AI-generated content as unapproved until human review is completed. Validation (FR-4) must distinguish "generated, pending approval" from "approved, ready for export."
- This reverses the PRD's Out of Scope item "AI-generated devotional content" — that item must be removed or reclassified.
- API cost for AI generation should be considered but is likely minor for weekly devotional volumes.

**Affected Artifacts:**

- Phase 001 — reflection field: add approval status tracking (e.g., `approval_status: pending | approved`)
- Phase 002 — template must support both draft/preview and approved states
- Phase 003 or new phase — AI content generation pipeline implementation
- Phase 004 — validation must enforce human approval before PDF export; must distinguish generated-pending from approved
- PRD Assumption #3 — revise from "Placeholder text for human editing" to "AI-generated with human approval"
- PRD Out of Scope — remove or reclassify "AI-generated devotional content"
- PRD FR-1.3 — update to reflect AI generation with approval workflow

**Status:** APPROVED (Human)

---

## Structure Questions

### Q4

**Question:** How many weeks per book?

**Options (per PRD):** Single week vs multi-week compilation

**Decision (Human):** Number of weeks depends on number of days provided. Published devotionals must meet page requirements (generally days >= 12). Some devotionals are for personal use and not published.

**Tradeoffs:**

- Variable week count based on day count provides maximum flexibility for both personal and published use.
- The 12-day minimum for published works provides a practical threshold aligned with KDP page count requirements.
- Supporting both personal-use and publication-ready outputs introduces two quality tiers with different validation rules.
- This is more flexible than the original single-week assumption but avoids the complexity of a rigid multi-week compilation system.

**Risks:**

- The system must distinguish between "personal use" and "publish-ready" output modes. Validation rules differ: publish-ready enforces KDP page minimums and all compliance checks; personal use may relax these.
- "Generally days >= 12" implies the threshold is a guideline, not a hard rule. The system should warn (not block) when published output falls below the threshold.
- The data model must support an arbitrary number of days organized into weeks. Week boundaries need definition: are weeks always 6-day blocks, or can partial weeks exist?
- This revises PRD Assumption #4 and partially reverses the Out of Scope item "Multi-week compilation."

**Affected Artifacts:**

- Phase 001 — data model: support variable day count; add output mode field (personal vs publish-ready); define week-boundary logic
- Phase 003 — conditional KDP validation based on output mode
- Phase 004 — validation rules split by output mode; page count warning for publish-ready below threshold
- PRD Assumption #4 — revise from "Single week per generation" to reflect variable day count and dual output modes
- PRD Out of Scope — reclassify "Multi-week compilation" (now partially in scope)
- PRD System Inputs — `num_days` semantics may need expansion or a new `output_mode` parameter

**Status:** APPROVED (Human)

---

### Q5

**Question:** Should days have sub-themes or share the week's theme?

**Options (per PRD):** Unified vs progressive

**Decision (Human):** Approved as previously proposed — Progressive (days build on the weekly theme).

**Tradeoffs:**

- Progressive provides a richer reading experience and narrative arc across the week.
- Progressive requires sub-theme planning and makes day ordering significant.
- Unified is simpler but contradicts the PRD's existing language ("days should build on each other within the week").

**Risks:**

- Each day needs an optional `day_focus` field. If not provided, it defaults to the weekly topic.
- Placeholder or AI-generated content should suggest a progression arc (e.g., Day 1: Introduction through Day 6: Application/Commitment).

**Affected Artifacts:**

- Phase 001 — add `day_focus` field to daily schema
- Phase 002 — render day focus/sub-theme
- Phase 004 — optional progression validation

**Status:** APPROVED (Human)

---

### Q6

**Question:** Is a 7th day (Sunday) ever needed?

**Options (per PRD):** 6-day only vs configurable 7

**Decision (Human):** Day 7 integrates with Sunday worship. Instructions should be included in the Introduction.

**Tradeoffs:**

- Integrating Day 7 with Sunday worship gives the devotional a natural weekly rhythm tied to congregational practice.
- Placing instructions in the Introduction keeps the daily content structure clean while providing guidance for Sunday use.
- This is more purposeful than generic "configurable 7" — Day 7 has a distinct character.

**Risks:**

- The Introduction (confirmed in Q7) must include Sunday worship integration instructions. This creates a content dependency between Q6 and Q7.
- Day 7 content structure may differ from Days 1–6 if it is worship-oriented rather than following the standard 5-element format. This needs clarification: does Day 7 use the same 5 elements, or a modified structure? For now, assume same structure with worship-oriented content unless specified otherwise.
- `num_days` = 7 must trigger inclusion of Sunday worship guidance in the Introduction.

**Affected Artifacts:**

- Phase 001 — Day 7 definition; flag or metadata indicating worship integration
- Phase 002 — Introduction template must include Sunday worship instructions when `num_days` includes Day 7
- Phase 004 — validate Introduction includes Sunday guidance when Day 7 is present
- PRD Decision D001 — update to reflect Day 7 as Sunday worship integration

**Status:** APPROVED (Human)

---

## KDP Questions

### Q7

**Question:** Front matter requirements?

**Options (per PRD):** Title only vs full (copyright, TOC, intro)

**Decision (Human):** Include Title page, Copyright page, and Introduction. Table of Contents may be included for larger books.

**Tradeoffs:**

- Title + Copyright + Introduction provides a professional, complete front matter set.
- Introduction serves double duty: book overview and Sunday worship instructions (per Q6).
- Conditional TOC for larger books avoids unnecessary bulk in short devotionals while providing navigation for longer ones.
- More front matter pages contribute toward KDP's 24-page minimum for published works.

**Risks:**

- "Larger books" needs a threshold definition for TOC inclusion. Possible rule: include TOC when day count exceeds a threshold (e.g., >= 12 days or >= 2 weeks). This can be a configurable parameter or a fixed rule.
- Introduction content must be defined: at minimum, book purpose, how to use the devotional, and Sunday worship instructions (per Q6). Whether the Introduction is user-written, AI-generated, or templated needs specification.
- Three mandatory front matter pages (title, copyright, introduction) adds 3+ pages toward page count.

**Affected Artifacts:**

- Phase 001 — add Introduction content field; add `author_name` for copyright page; add TOC toggle or threshold parameter
- Phase 002 — title page, copyright page, Introduction, and conditional TOC templates
- Phase 003 — front matter page generation, ordering, and conditional TOC logic
- Phase 004 — validate front matter completeness; validate Introduction includes Sunday guidance when applicable
- PRD Assumption #5 — revise from "Title page only" to "Title, Copyright, Introduction; TOC for larger books"
- PRD FR-3.3 — update to reflect mandatory front matter set

**Status:** APPROVED (Human)

---

### Q8

**Question:** Print-only or also ebook?

**Options (per PRD):** PDF only vs also EPUB/MOBI

**Decision (Human):** Approved as previously proposed — PDF only.

**Tradeoffs:**

- PDF only is the simplest pipeline and aligns with the stated project scope.
- Ebook export (EPUB/MOBI) would broaden distribution but adds significant complexity with different formatting rules.

**Risks:**

- None. This is unambiguously stated in the PRD (Out of Scope, Assumption #6, Decision D004).

**Affected Artifacts:**

- None. Existing artifacts already reflect this decision.

**Status:** APPROVED (Human)

---

### Q9

**Question:** Black & white or color interior?

**Options (per PRD):** B&W (cheaper) vs color

**Decision (Human):** Approved as previously proposed — Black & white.

**Tradeoffs:**

- B&W has ~6x lower print cost per page than color.
- B&W is standard for text-only devotionals.
- Color would only benefit illustrated content, which is not in scope.

**Risks:**

- None. Already specified in the PRD KDP Requirements table and Assumption #7.

**Affected Artifacts:**

- None. Existing artifacts already reflect this decision.

**Status:** APPROVED (Human)

---

### Q10

**Question:** ISBN and barcode handling?

**Options (per PRD):** System generates vs user provides

**Decision (Human):** Initially use Amazon-provided ISBN and always use Amazon barcode. If publications become profitable, integrate with Bowker later.

**Tradeoffs:**

- Amazon-provided free ISBN eliminates upfront cost and integration complexity for MVP.
- Amazon barcode is automatic with KDP publishing — no system action needed.
- Bowker integration deferred until profitability justifies the investment ($125+ per ISBN).
- Amazon-provided ISBNs are KDP-exclusive (cannot be used on other platforms). This is acceptable given PDF-only, KDP-focused scope.

**Risks:**

- Amazon-provided ISBNs lock distribution to KDP. If multi-platform distribution is ever desired, Bowker ISBNs would be needed. This is a known, accepted constraint for now.
- No system implementation is needed for MVP — ISBN and barcode are handled entirely within KDP's upload workflow.
- Bowker integration is a future consideration, not a current requirement. No design accommodation is needed now.

**Affected Artifacts:**

- PRD Out of Scope — update "ISBN generation" to clarify: "Use Amazon-provided ISBN for MVP; Bowker integration deferred"
- No phase plan changes needed for MVP

**Status:** APPROVED (Human)

---

## Design Questions

### Q11

**Question:** One day per page or content-driven page breaks?

**Options (per PRD):** Fixed vs dynamic layout

**Decision (Human):** Approved as previously proposed — Each day starts on a new page, may span multiple pages.

**Tradeoffs:**

- Starting each day on a new page provides clean visual separation and professional layout.
- Content may span multiple pages, accommodating varying reflection lengths.
- Fixed one-page-per-day would constrain content length artificially.
- Fully dynamic breaks would allow days to run together, reducing readability.

**Risks:**

- Partial blank pages at the end of shorter days increase page count but may appear as wasted space.
- More page breaks means more pages, which helps meet KDP page minimums for published output.

**Affected Artifacts:**

- Phase 002 — page break rules between days
- Phase 003 — page break implementation in PDF generation

**Status:** APPROVED (Human)

---

### Q12

**Question:** Font selection?

**Options (per PRD):** System fonts vs bundled fonts

**Decision (Human):** Approved as previously proposed — Bundled open-source fonts.

**Tradeoffs:**

- Bundled fonts guarantee consistent rendering and reliable PDF embedding across all platforms.
- System fonts vary by platform and may not embed correctly, risking KDP rejection.
- Bundled fonts add font files to the repository but eliminate platform-dependent behavior.

**Risks:**

- KDP requires embedded fonts (FR-3.1, KDP Requirements table). System fonts may not embed reliably depending on the PDF library and font licensing.
- Specific font choices (e.g., Lora, EB Garamond, Crimson Text for body; Playfair Display for headings) are deferred to the implementation phase.
- This revises PRD Assumption #9 ("System fonts with fallbacks").

**Affected Artifacts:**

- Phase 002 — font specification in templates
- Phase 003 — font bundling and embedding implementation
- PRD Assumption #9 — revise

**Status:** APPROVED (Human)

---

### Q13

**Question:** Header/footer content?

**Options (per PRD):** Page numbers only vs decorative

**Decision (Human):** Approved as previously proposed — Page numbers only.

**Tradeoffs:**

- Page numbers only is clean, standard for devotionals, and simple to implement.
- Decorative headers add polish but increase template complexity.
- Running headers require page-type-aware logic.

**Risks:**

- Front matter pages conventionally use Roman numerals or no page numbers; content pages use Arabic numerals. This distinction needs specification in template design.
- First page of each day/section may suppress page numbers per publishing convention.

**Affected Artifacts:**

- Phase 002 — header/footer template definition
- Phase 003 — page numbering implementation

**Status:** APPROVED (Human)

---

## Summary

| # | Question | Decision (Human) | Status |
|---|----------|------------------|--------|
| Q1 | What is the source for inspirational quotes? | Classical evangelical authors from identified open-source websites; Turabian attribution | APPROVED (Human) |
| Q2 | Should scripture text be auto-fetched or user-provided? | NASB, retrieved from the web | APPROVED (Human) |
| Q3 | Will devotional reflections be AI-generated or templates? | AI-generated with expanded references; human approval required | APPROVED (Human) |
| Q4 | How many weeks per book? | Variable by day count; published >= 12 days; personal use exempt | APPROVED (Human) |
| Q5 | Should days have sub-themes or share the week's theme? | Progressive (days build on weekly theme) | APPROVED (Human) |
| Q6 | Is a 7th day (Sunday) ever needed? | Day 7 integrates with Sunday worship; guidance in Introduction | APPROVED (Human) |
| Q7 | Front matter requirements? | Title, Copyright, Introduction; TOC for larger books | APPROVED (Human) |
| Q8 | Print-only or also ebook? | PDF only | APPROVED (Human) |
| Q9 | Black & white or color interior? | Black & white | APPROVED (Human) |
| Q10 | ISBN and barcode handling? | Amazon-provided ISBN; Amazon barcode; Bowker deferred | APPROVED (Human) |
| Q11 | One day per page or content-driven page breaks? | Day starts on new page, may span | APPROVED (Human) |
| Q12 | Font selection? | Bundled open-source fonts | APPROVED (Human) |
| Q13 | Header/footer content? | Page numbers only | APPROVED (Human) |

---

## PRD Revisions Implied

These revisions are identified but **not applied**:

| Item | Current State | Required Change |
|------|---------------|-----------------|
| Assumption #1 | User-provided or placeholder text | Classical evangelical authors from open-source websites; Turabian attribution |
| Assumption #2 | User-provided with reference | NASB, web-retrieved |
| Assumption #3 | Placeholder text for human editing | AI-generated with expanded references; human approval required |
| Assumption #4 | Single week per generation | Variable day count; publish-ready >= 12 days; personal use mode |
| Assumption #5 | Title page only | Title, Copyright, Introduction; conditional TOC |
| Assumption #9 | System fonts with fallbacks | Bundled open-source fonts |
| Decision D001 | 6-day week (Mon–Sat) | Day 7 = Sunday worship integration; 6-day default preserved |
| Decision D005 | NIV as default version | NASB as default version |
| FR-1.3 | Placeholders or future generation | AI-generated with human approval gate |
| FR-3.3 | Copyright page optional, TOC optional | Copyright and Introduction mandatory; TOC conditional |
| Out of Scope | AI-generated devotional content | Remove — now in scope with approval workflow |
| Out of Scope | Scripture API integration | Remove — now in scope (NASB web retrieval) |
| Out of Scope | Multi-week compilation | Reclassify — partially in scope (variable day count) |
| Out of Scope | ISBN generation | Clarify — Amazon-provided for MVP; Bowker deferred |
| KDP Requirements table | No minimum page count | Add 24-page minimum for publish-ready output |
| System Inputs | `scripture_version` default: NIV | Change default to NASB |
| System Inputs | (none) | Add `output_mode` parameter (personal vs publish-ready) |

---

## New Concepts Introduced by Human Decisions

The following concepts were not present in the prior AI-proposed artifact and arise directly from Barbara's answers:

1. **Dual output modes** (Q4): personal use vs publish-ready, with different validation rules.
2. **AI content generation pipeline** (Q3): AI-generated reflections with mandatory human approval gate.
3. **Scripture web retrieval** (Q2): external dependency for NASB text, requiring source identification and error handling.
4. **Turabian attribution** (Q1): structured citation format requiring specific data model fields beyond free-text.
5. **Sunday worship integration** (Q6): Day 7 has distinct purpose; Introduction must contain worship guidance.
6. **Conditional TOC** (Q7): front matter varies by book size.
7. **Profitability-gated Bowker integration** (Q10): future ISBN strategy tied to business outcome.

These concepts expand project scope beyond the original PRD assumptions and will require corresponding updates to phase plans and the roadmap.

---

## Cross-Cutting Risks

| Risk | Source | Impact | Mitigation |
|------|--------|--------|------------|
| NASB copyright restrictions | Q2 | Published use has quotation limits (Lockman Foundation) | Human-only legal review required before publication |
| KDP 24-page minimum | Q4 | Short devotionals may not meet print threshold | Enforce >= 12 days for publish-ready; warn during validation |
| AI theological accuracy | Q3 | Generated reflections may contain errors | Mandatory human approval gate; no export without approval |
| Open-source website availability | Q1 | Quote sources may become unavailable | Verify source list; consider pre-caching quote catalog |
| Scripture retrieval failures | Q2 | Network or API issues block generation | Graceful error handling; clear failure messages |
| Scope expansion | Q2, Q3, Q4 | Three Out of Scope items moved into scope | Phase plans and roadmap must be updated to accommodate |
| Unverified quotes in output | Q1 | Fabricated or misattributed quotes undermine credibility | Quote Catalog with mandatory source verification; export gate on verification_status |
| Copyright violation from post-1928 authors | Q1 | Legal liability, KDP account risk | Author whitelist with PD status; publish-ready restricted to PD-confirmed quotes |

---

## End of Artifact

This is the finalized Planner Iteration 3 output incorporating all human-provided decisions for Q1–Q13. All questions are marked APPROVED (Human).

This artifact is pending final human review. No existing artifacts have been modified. No implementation planning has been initiated.
