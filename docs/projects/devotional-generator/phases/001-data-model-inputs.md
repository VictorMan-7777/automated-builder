# Phase 001: Data Model & Inputs

## Phase Information

- **Phase**: 001
- **Name**: Data Model & Inputs
- **Status**: Not Started
- **Dependencies**: None

## Objective

Define input parameters and data structures for weekly devotional generation.

---

## Scope

### In Scope

- Input schema definition (num_days, topic, title, scripture_version, output_mode)
- Weekly data model (container for days, variable day count, week-boundary logic)
- Daily data model (5-element structure with Turabian attribution, NASB scripture, approval status, day_focus)
- Configuration file format

### Out of Scope

- Content generation
- Template rendering
- PDF export

---

## Commit Points

### CP1: Input Schema and Configuration

**Goal**: Define how users specify what to generate

**Deliverables**:
- `config/input-schema.json` - JSON Schema for inputs
- `config/default.yaml` - Default configuration values

**Input Schema**:
```json
{
  "num_days": {
    "type": "integer",
    "minimum": 1,
    "maximum": 7,
    "default": 6
  },
  "topic": {
    "type": "string",
    "required": true
  },
  "title": {
    "type": "string",
    "default": "auto-generated from topic"
  },
  "author_name": {
    "type": "string",
    "required": true,
    "description": "Author name for copyright page"
  },
  "scripture_version": {
    "type": "string",
    "default": "NASB",
    "enum": ["NASB", "NIV", "ESV", "KJV", "NKJV", "NLT"]
  },
  "output_mode": {
    "type": "string",
    "default": "publish-ready",
    "enum": ["personal", "publish-ready"],
    "description": "personal = relaxed validation; publish-ready = KDP compliance enforced, >= 12 days recommended"
  }
}
```

**Files to Stage**:
- `config/input-schema.json`
- `config/default.yaml`

**Commit Command**:
```bash
git add config/input-schema.json config/default.yaml
git commit -m "feat(devotional-generator): add input schema and config (CP1)"
```

**Verification**:
- [ ] Schema validates sample inputs
- [ ] Default config loads without errors
- [ ] Invalid inputs rejected with clear message

**Rollback**:
```bash
git reset --soft HEAD~1
rm -rf config/
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, files touched, validation test results |

---

### CP2: Weekly and Daily Data Models

**Goal**: Define data structures for devotional content

**Deliverables**:
- Weekly model schema
- Daily model schema (5 elements)
- Sample data file

**Weekly Model**:
```json
{
  "weekly": {
    "title": "string",
    "topic": "string",
    "author_name": "string",
    "scripture_version": "string (default: NASB)",
    "output_mode": "string (personal | publish-ready)",
    "introduction_content": "string (book purpose, how-to, Sunday worship guidance if Day 7 present)",
    "include_toc": "boolean (conditional; true when day count >= threshold, e.g., 12)",
    "days": ["DailyModel", "..."]
  }
}
```

**Week Boundary Logic**: Days are organized into 6-day blocks (Mon–Sat). A 7th day (Sunday) is a worship integration day. Multi-week books consist of consecutive 6-day (or 7-day) blocks under the same topic.

**Daily Model** (5 elements):
```json
{
  "daily": {
    "day_number": "integer (1-7)",
    "day_name": "string (Monday-Sunday)",
    "day_focus": "string (optional; sub-theme for this day; defaults to weekly topic)",
    "is_worship_day": "boolean (true for Day 7/Sunday; triggers worship integration)",
    "quote": {
      "text": "string",
      "attribution": {
        "author": "string (required)",
        "source_title": "string (required)",
        "publication_year": "string (optional)",
        "page_or_url": "string (optional)"
      },
      "attribution_formatted": "string (Turabian format, auto-generated from fields)"
    },
    "scripture": {
      "reference": "string (e.g., 'John 3:16')",
      "text": "string (auto-populated via web retrieval)",
      "version": "string (default: NASB)"
    },
    "reflection": {
      "content": "string (AI-generated)",
      "expanded_references": ["string (additional scripture cross-references or citations)"],
      "approval_status": "string (pending | approved)"
    },
    "action_steps": {
      "items": ["string", "..."]
    },
    "prayer": {
      "content": "string"
    }
  }
}
```

**Files to Stage**:
- `schemas/weekly-model.json`
- `schemas/daily-model.json`
- `examples/sample-week.json`

**Commit Command**:
```bash
git add schemas/ examples/sample-week.json
git commit -m "feat(devotional-generator): add weekly and daily data models (CP2)"
```

**Verification**:
- [ ] Weekly model contains days array
- [ ] Daily model has all 5 elements
- [ ] Sample week validates against schema

**Rollback**:
```bash
git reset --soft HEAD~1
rm -rf schemas/ examples/sample-week.json
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, files touched, sample data validation |

---

## Acceptance Criteria

### Phase Complete When:

- [ ] Input schema validates user inputs (including `output_mode` and `author_name`)
- [ ] Invalid inputs produce clear error messages
- [ ] Weekly model can hold variable day count (1-7 per week, multi-week for larger books)
- [ ] Daily model has all 5 elements (quote with Turabian attribution, scripture with NASB default, reflection with approval status, action_steps, prayer)
- [ ] Daily model supports `day_focus` and `is_worship_day` fields
- [ ] Quote attribution supports structured Turabian fields (author, source_title, publication_year, page_or_url)
- [ ] Reflection tracks `approval_status` (pending | approved)
- [ ] Weekly model includes `introduction_content` and conditional `include_toc`
- [ ] Sample data file demonstrates full structure
- [ ] Default configuration works out of box (NASB default, publish-ready default)

---

## Gatekeeper Checklist

**Executor**: AI: Claude Code
**Verifier**: Human: Barbara

### Human Review Required

- [ ] Data model captures all content requirements
- [ ] Input defaults are sensible
- [ ] Structure supports future extensibility

### Verification Reference

See `docs/system/ai.md` for AI executor output requirements.

### Verification Steps

1. Load default config, verify no errors
2. Validate sample input against schema
3. Verify sample week has correct structure

---

## Notes

### Resolved Questions Affecting This Phase

| Question | Decision | Impact on Phase 001 |
|----------|----------|---------------------|
| Q1 | Classical evangelical authors; Turabian attribution | Quote fields: structured attribution (author, source_title, publication_year, page_or_url) |
| Q2 | NASB, web-retrieved | Scripture version default: NASB; `scripture_text` auto-populated |
| Q3 | AI-generated reflections; human approval | Reflection field: `approval_status` (pending \| approved), `expanded_references` |
| Q4 | Variable day count; dual output modes | `output_mode` parameter; variable-length `days` array; week-boundary logic |
| Q5 | Progressive (days build on theme) | `day_focus` field per day |
| Q6 | Day 7 = Sunday worship integration | `is_worship_day` flag; Introduction content includes worship guidance |
| Q7 | Title, Copyright, Introduction mandatory; conditional TOC | `author_name`, `introduction_content`, `include_toc` fields in weekly model |

### Decisions Made

- num_days defaults to 6 (Monday-Saturday); Day 7 supported as Sunday worship integration
- Scripture version is configurable, defaults to NASB
- Output mode defaults to publish-ready

---

**Next Phase**: [002-template-system.md](./002-template-system.md)
