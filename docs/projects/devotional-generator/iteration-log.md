# Devotional Generator - Iteration Log

## Document Information

- **Project**: Devotional Generator
- **Version**: 3.0
- **Started**: 2026-02-05
- **Last Updated**: 2026-02-07

## Purpose

This log tracks planning iterations, decisions, and changes throughout the Devotional Generator project. It serves as a historical record and reference for future work.

---

## Iterations

### Iteration 3: Documentation Update (Q1–Q13 Applied)

**Date**: 2026-02-07
**Phase**: Planning
**Status**: Completed

#### Objectives

- [x] Apply all approved Iteration 3 decisions to project documentation
- [x] Update PRD: assumptions, decisions, FRs, inputs, out of scope, KDP table
- [x] Update all four phase plans (001–004) with resolved question impacts
- [x] Update roadmap: deliverables, dependencies, risks, post-MVP list
- [x] Update project index: status, key specs, resolved questions
- [x] Update iteration log with Iteration 2 and 3 entries

#### Changes Made

**PRD (v2.0 → v3.0)**:
- Resolved all 13 open questions (Q1–Q13) — replaced Open Questions section with Resolved Questions table
- Updated 6 of 10 assumptions (#1, #2, #3, #4, #5, #9)
- Updated decisions D001 (Day 7 worship integration) and D005 (NASB default)
- Updated FR-1.3 (AI content generation with approval) and FR-3.3 (mandatory front matter)
- Updated System Inputs: `scripture_version` default to NASB, added `output_mode` parameter
- Updated Out of Scope: removed 3 items now in scope, clarified ISBN approach
- Added 24-page minimum to KDP Requirements table

**Phase 001 (updated)**:
- Input schema: added `output_mode`, `author_name`; changed `scripture_version` default to NASB
- Daily model: Turabian attribution fields, `day_focus`, `is_worship_day`, `approval_status`, `expanded_references`
- Weekly model: `introduction_content`, `include_toc`, `output_mode`

**Phase 002 (updated)**:
- Scope expanded: front matter templates, font specification, page break/numbering rules
- Daily template: Turabian attribution rendering, day_focus, approval status display
- Notes: resolved questions table replacing open questions

**Phase 003 (updated)**:
- Scope expanded: scripture web retrieval, AI pipeline, conditional KDP validation, bundled fonts
- CP7 renamed to "Front Matter and Page Numbers" with expanded deliverables
- Updated font strategy, acceptance criteria, risks

**Phase 004 (updated)**:
- Scope expanded: Turabian validation, approval enforcement, output-mode-aware rules, scripture retrieval validation, front matter validation
- Added 7 new validation rules (V012–V018) and 1 new KDP rule (K008)
- Validation rules split by output mode

**Roadmap (v2.0 → v3.0)**:
- Updated all phase deliverables and key decisions
- Added 3 new technical dependencies (Bible API, Claude API, bundled fonts)
- Added 4 new risks (NASB copyright, AI theological accuracy, scripture retrieval, quote source availability)
- Updated post-MVP list (removed items now in scope)
- Replaced open questions section with resolved questions

**Index (v2.0 → v3.0)**:
- Status updated to "Planning Complete (Iteration 3)"
- Key specifications updated (inputs table, weekly structure)
- Open Questions Summary replaced with Resolved Questions Summary

#### Source Artifact

`docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md`

---

### Iteration 2: Open Questions Q1–Q13

**Date**: 2026-02-07
**Phase**: Planning
**Status**: Completed (Approved by Human)

#### Objectives

- [x] Produce Planner Iteration 3 artifact addressing all 13 open questions
- [x] Record human-provided decisions for each question
- [x] Identify tradeoffs, risks, and affected artifacts per decision
- [x] Produce final artifact for human review

#### Summary

All 13 open questions from PRD v2.0 were addressed. Human (Barbara) provided authoritative decisions for each question. Two artifacts were produced:

1. `docs/system/outputs/2026-02-07__01__planner__open-questions-q1-q13.md` — Initial draft with AI-proposed decisions
2. `docs/system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md` — Final version with human-provided decisions replacing AI proposals

#### Key Decisions (Human)

| # | Decision |
|---|----------|
| Q1 | Classical evangelical authors from open-source websites; Turabian attribution |
| Q2 | NASB, retrieved from the web |
| Q3 | AI-generated with expanded references; human approval required |
| Q4 | Variable day count; published >= 12 days; personal use exempt |
| Q5 | Progressive (days build on weekly theme) |
| Q6 | Day 7 integrates with Sunday worship; guidance in Introduction |
| Q7 | Title, Copyright, Introduction; TOC for larger books |
| Q8 | PDF only |
| Q9 | Black & white |
| Q10 | Amazon-provided ISBN; Amazon barcode; Bowker deferred |
| Q11 | Each day starts on new page, may span |
| Q12 | Bundled open-source fonts |
| Q13 | Page numbers only |

#### Scope Changes

Three PRD Out of Scope items moved into scope:
- AI-generated devotional content (Q3)
- Scripture API integration (Q2)
- Multi-week compilation (Q4, partially)

#### Next Steps

- [x] Apply decisions to all project documentation (Iteration 3)

---

### Iteration 1: Requirements Alignment

**Date**: 2026-02-06
**Phase**: Planning
**Status**: Completed

#### Objectives

- [x] Align PRD with user requirements
- [x] Add missing content element (Inspirational Quote)
- [x] Define weekly structure (6 days, Monday-Saturday)
- [x] Add configurable inputs (num_days, topic)
- [x] Add KDP-specific requirements (6x9, margins)
- [x] Surface open questions explicitly
- [x] Revise roadmap to 4-phase KDP-focused pipeline

#### Changes Made

**PRD (v1.0 → v2.0)**:
- Added "Inspirational Quote" as first daily element (5 elements total)
- Defined weekly structure: 6 days (Monday-Saturday), one theme
- Added input parameters: num_days (default 6), topic (required)
- Added KDP specifications: 6x9 trim, margins, font requirements
- Added Open Questions section with 13 questions
- Added Assumptions section
- Revised Out of Scope list

**Roadmap (v1.0 → v2.0)**:
- Reduced from 5 phases to 4 phases (MVP focus)
- Reduced from 11 commit points to 9
- Renamed phases for KDP-specific pipeline:
  - Phase 001: Data Model & Inputs
  - Phase 002: Template System
  - Phase 003: KDP PDF Export
  - Phase 004: Validation & Preview
- Removed generic content library phase (deferred)
- Added KDP-specific deliverables in Phase 003

**Index (v1.0 → v2.0)**:
- Updated to reflect new 4-phase structure
- Added Key Specifications section
- Added Open Questions summary

#### Decisions Made

| ID | Decision | Rationale |
|----|----------|-----------|
| D006 | 5-element daily structure | User requirement: quote, scripture, reflection, action, prayer |
| D007 | 4-phase roadmap | MVP focus; content library deferred |
| D008 | Surface open questions | Per user constraint: don't guess, surface questions |
| D009 | KDP compliance as non-negotiable | Target output is KDP-ready PDF |

#### Open Questions Identified

13 open questions documented in PRD covering:
- Content sources (quotes, scripture, reflections)
- Structure decisions (weeks per book, day themes)
- KDP specifics (front matter, ebook, color)
- Design choices (page breaks, fonts, headers)

#### Rollback

If this iteration is rejected:
- Revert to v1.0 of PRD, roadmap, index
- `git checkout HEAD~1 -- docs/projects/devotional-generator/`

#### Next Steps

- [ ] Human review of revised planning artifacts
- [ ] Gatekeeper review for plan approval
- [ ] Answer open questions before implementation
- [ ] Create detailed phase plans (001-004)

---

### Iteration 0: Initial Planning

**Date**: 2026-02-05
**Phase**: Planning
**Status**: Superseded by Iteration 1

#### Summary

Initial planning created a generic devotional generator with:
- 5 phases, 11 commit points
- Focus on template system and content library
- Multi-format export (MD, HTML, PDF, JSON)
- No weekly structure
- Missing: inspirational quote element
- Missing: KDP-specific requirements

#### Outcome

Requirements did not match user needs. Superseded by Iteration 1.

---

## Decision Log

| ID | Date | Decision | Executor | Rationale | Status |
|----|------|----------|----------|-----------|--------|
| D001 | 2026-02-05 | Five-phase structure | — | Balanced delivery | Superseded |
| D002 | 2026-02-05 | JSON for templates | — | Standard format | Active |
| D003 | 2026-02-05 | Python 3.11+ | — | Rich ecosystem | Active |
| D004 | 2026-02-05 | Local file storage | — | Simplicity | Active |
| D005 | 2026-02-05 | Four export formats | — | Cover channels | Superseded |
| D006 | 2026-02-06 | 5-element daily structure | Human: Barbara | User requirement | Active |
| D007 | 2026-02-06 | 4-phase roadmap | Human: Barbara | MVP focus | Active |
| D008 | 2026-02-06 | Surface open questions | Human: Barbara | Don't assume | Completed |
| D009 | 2026-02-06 | KDP compliance first | Human: Barbara | Target output | Active |
| D010 | 2026-02-07 | Q1: Turabian attribution for quotes | Human: Barbara | Credibility, structured citations | Active |
| D011 | 2026-02-07 | Q2: NASB, web-retrieved | Human: Barbara | Literal translation, automation | Active |
| D012 | 2026-02-07 | Q3: AI-generated reflections, human approval | Human: Barbara | Scale + quality control | Active |
| D013 | 2026-02-07 | Q4: Variable day count, dual output modes | Human: Barbara | Flexibility for personal + published | Active |
| D014 | 2026-02-07 | Q5: Progressive sub-themes | Human: Barbara | Richer reading experience | Active |
| D015 | 2026-02-07 | Q6: Day 7 = Sunday worship integration | Human: Barbara | Natural weekly rhythm | Active |
| D016 | 2026-02-07 | Q7: Full front matter (title, copyright, intro) | Human: Barbara | Professional, KDP-ready | Active |
| D017 | 2026-02-07 | Q10: Amazon-provided ISBN; Bowker deferred | Human: Barbara | No upfront cost for MVP | Active |
| D018 | 2026-02-07 | Q12: Bundled open-source fonts | Human: Barbara | Consistent rendering, reliable embedding | Active |

---

## Version Summary

| Version | Date | Major Changes |
|---------|------|---------------|
| 3.0 | 2026-02-07 | Iteration 2–3: All Q1–Q13 resolved; docs updated with approved decisions |
| 2.0 | 2026-02-06 | Iteration 1: KDP focus, 4 phases, 5 daily elements |
| 1.0 | 2026-02-05 | Iteration 0: Initial generic planning |

---

## Related Documents

- [Project Index](./index.md)
- [PRD](./prd.md)
- [Roadmap](./roadmap.md)
- [Phase Plans](./phases/)
