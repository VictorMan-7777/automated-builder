# Devotional Generator - Project Index

## Overview

The Devotional Generator produces weekly devotional content suitable for self-publishing on Amazon KDP. Each week contains 6 days (Monday-Saturday) of structured devotional content, exported as a KDP-ready 6x9 inch PDF.

## Project Status

- **Current Phase**: Planning
- **Last Updated**: 2026-02-07
- **Status**: Planning Complete (Iteration 3 — Open Questions Resolved)
- **Version**: 3.0

---

## Navigation

### Core Documents

- **[Product Requirements (PRD)](./prd.md)** - Requirements, content structure, KDP specs
- **[Roadmap](./roadmap.md)** - Four-phase milestone plan with 9 commit points
- **[Iteration Log](./iteration-log.md)** - Progress tracking and decision history

### Phase Documentation

1. **[Phase 001: Data Model & Inputs](./phases/001-data-model-inputs.md)** - Input schema, data structures
2. **[Phase 002: Template System](./phases/002-template-system.md)** - Weekly/daily templates
3. **[Phase 003: KDP PDF Export](./phases/003-kdp-pdf-export.md)** - 6x9 PDF generation
4. **[Phase 004: Validation & Preview](./phases/004-validation-preview.md)** - Quality assurance

---

## Key Specifications

### Content Structure

Each **day** includes 5 elements:
1. Inspirational Quote
2. Scripture
3. Devotional Reflection
4. Action Steps
5. Prayer

Each **week** contains:
- 6 days (Monday-Saturday, default); Day 7 = Sunday worship integration
- One unified theme with progressive sub-themes per day
- Days build on each other

### Inputs

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_days` | 6 | Days to generate (1-7) |
| `topic` | Required | Theme for the week |
| `scripture_version` | NASB | Bible translation (web-retrieved) |
| `output_mode` | publish-ready | `personal` or `publish-ready` |

### Output

- **Format**: PDF
- **Trim Size**: 6 x 9 inches
- **Target**: Amazon KDP print compliance

---

## Quick Links

### For Reviewers

- Start with [PRD](./prd.md) for requirements
- Check [Open Questions](./prd.md#open-questions) for decisions needed
- Review [Roadmap](./roadmap.md) for phase structure

### For Gatekeeper

- Verify commit points in [Roadmap](./roadmap.md)
- Check acceptance criteria in phase plans
- Review [Iteration Log](./iteration-log.md) for decisions

---

## Resolved Questions Summary

All 13 open questions (Q1–Q13) resolved in Planner Iteration 3. Key decisions:

| # | Decision | Impact |
|---|----------|--------|
| Q1 | Classical evangelical authors; Turabian attribution | Quote data model, rendering |
| Q2 | NASB, web-retrieved | Scripture pipeline, new dependency |
| Q3 | AI-generated reflections; human approval | Content pipeline, approval workflow |
| Q4 | Variable day count; dual output modes | Validation rules, page count |
| Q7 | Title, Copyright, Introduction; conditional TOC | Front matter scope |
| Q12 | Bundled open-source fonts | Font embedding strategy |

See [Iteration 3 artifact](../../system/outputs/2026-02-07__02__planner__open-questions-q1-q13-final.md) for full decisions.

---

## Document Version

- **Version**: 3.0
- **Last Updated**: 2026-02-07
- **Changes**: Applied Iteration 3 decisions (Q1–Q13); all open questions resolved
