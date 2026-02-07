# Phase 002: Template System

## Phase Information

- **Phase**: 002
- **Name**: Template System
- **Status**: Not Started
- **Dependencies**: Phase 001 complete

## Objective

Create templates for weekly and daily devotional structure with clear placeholders for content.

---

## Scope

### In Scope

- Weekly template (container structure)
- Daily template (5-element layout with Turabian quote attribution, day focus/sub-theme)
- Front matter templates: title page, copyright page, Introduction, conditional TOC
- Placeholder system for content (draft/preview and approved states)
- Template rendering engine
- Font specification for bundled open-source fonts
- Header/footer template (page numbers only)
- Page break rules (each day starts on a new page)

### Out of Scope

- PDF generation (Phase 003)
- Content creation/population (AI generation pipeline — Phase 003 or new phase)
- Validation logic (Phase 004)

---

## Commit Points

### CP3: Weekly Template Structure

**Goal**: Define the weekly container template

**Deliverables**:
- `templates/weekly-template.json` - Weekly structure definition
- Template includes: title, theme, days placeholder

**Weekly Template Structure**:
```
Weekly Devotional Template
==========================
Title: {{title}}
Theme: {{topic}}
Days: {{num_days}}

---

{{#each days}}
  [Day {{day_number}} content here]
{{/each}}

---
Generated: {{generation_date}}
```

**Template Variables**:
| Variable | Source | Description |
|----------|--------|-------------|
| `{{title}}` | Input or auto-generated | Book/section title |
| `{{topic}}` | Input (required) | Week's theme |
| `{{num_days}}` | Input (default: 6) | Number of days |
| `{{days}}` | Generated | Array of daily content |
| `{{generation_date}}` | System | When generated |

**Files to Stage**:
- `templates/weekly-template.json`
- `templates/weekly-template.md` (Markdown version)

**Commit Command**:
```bash
git add templates/weekly-template.*
git commit -m "feat(devotional-generator): add weekly template structure (CP3)"
```

**Verification**:
- [ ] Template loads without errors
- [ ] All placeholders documented
- [ ] Template renders with sample data

**Rollback**:
```bash
git reset --soft HEAD~1
rm templates/weekly-template.*
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, files touched, template render test |

---

### CP4: Daily Template with 5 Elements

**Goal**: Define the daily devotional template with all 5 elements

**Deliverables**:
- `templates/daily-template.json` - Daily structure definition
- `templates/daily-template.md` - Markdown rendering template

**Daily Template Structure**:
```
## Day {{day_number}}: {{day_name}}

{{#if day_focus}}
### Focus: {{day_focus}}
{{/if}}

### Inspirational Quote

> "{{quote.text}}"
> — {{quote.attribution_formatted}}

---

### Scripture

**{{scripture.reference}}** ({{scripture.version}})

> {{scripture.text}}

---

### Reflection {{#if reflection.approval_status}}[{{reflection.approval_status}}]{{/if}}

{{reflection.content}}

{{#if reflection.expanded_references}}
**Further Reading**: {{#each reflection.expanded_references}}{{this}}; {{/each}}
{{/if}}

---

### Action Steps

{{#each action_steps.items}}
{{@index}}. {{this}}
{{/each}}

---

### Prayer

{{prayer.content}}

---
```

**5 Daily Elements**:

| # | Element | Placeholder | Required |
|---|---------|-------------|----------|
| 1 | Quote | `{{quote.text}}`, `{{quote.attribution_formatted}}` (Turabian format) | Yes |
| 2 | Scripture | `{{scripture.reference}}`, `{{scripture.text}}` (NASB, web-retrieved) | Yes |
| 3 | Reflection | `{{reflection.content}}`, `{{reflection.approval_status}}`, `{{reflection.expanded_references}}` | Yes |
| 4 | Action Steps | `{{action_steps.items}}` | Yes |
| 5 | Prayer | `{{prayer.content}}` | Yes |

**Additional Daily Fields**:

| Field | Placeholder | Required |
|-------|-------------|----------|
| Day Focus | `{{day_focus}}` | Optional (defaults to weekly topic) |

**Files to Stage**:
- `templates/daily-template.json`
- `templates/daily-template.md`
- `examples/sample-day-rendered.md`

**Commit Command**:
```bash
git add templates/daily-template.* examples/sample-day-rendered.md
git commit -m "feat(devotional-generator): add daily template with 5 elements (CP4)"
```

**Verification**:
- [ ] Template has all 5 elements
- [ ] Elements in correct order
- [ ] Placeholders render with sample data
- [ ] Output is well-formatted

**Rollback**:
```bash
git reset --soft HEAD~1
rm templates/daily-template.* examples/sample-day-rendered.md
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, sample rendered output |

---

## Acceptance Criteria

### Phase Complete When:

- [ ] Weekly template contains theme and days placeholder
- [ ] Daily template has all 5 elements in order (with Turabian attribution, approval status, expanded references)
- [ ] Daily template renders `day_focus` when present
- [ ] Front matter templates: title page, copyright page, Introduction render correctly
- [ ] Conditional TOC template renders when enabled
- [ ] Introduction includes Sunday worship guidance when Day 7 is present
- [ ] All placeholders are clearly marked
- [ ] Templates render correctly with sample data
- [ ] Markdown output is clean and readable
- [ ] Font specification documented for bundled open-source fonts
- [ ] Page break rules enforce new page per day

---

## Gatekeeper Checklist

**Executor**: AI: Claude Code
**Verifier**: Human: Barbara

### Human Review Required

- [ ] Template structure matches daily devotional format
- [ ] Element order is correct (quote, scripture, reflection, action, prayer)
- [ ] Formatting is visually appealing

### Verification Reference

See `docs/system/ai.md` for AI executor output requirements.

### Verification Steps

1. Render weekly template with sample inputs
2. Render daily template with sample day
3. Verify all 5 elements appear in output
4. Check placeholder markers are replaced

---

## Template Rendering Notes

### Placeholder Syntax Options

| Option | Example | Pros | Cons |
|--------|---------|------|------|
| Mustache | `{{variable}}` | Simple, widely known | Limited logic |
| Jinja2 | `{{ variable }}` | Powerful, Python-native | More complex |
| Custom | `[[variable]]` | Full control | Non-standard |

**Decision**: Use Mustache/Handlebars-style `{{variable}}` for simplicity.

### Content Markers

For unfilled placeholders, use clear markers:
- `[QUOTE TEXT HERE]`
- `[SCRIPTURE REFERENCE]`
- `[REFLECTION CONTENT - 200-400 WORDS]`
- `[ACTION STEP 1]`
- `[PRAYER TEXT]`

---

## Notes

### Resolved Questions Affecting This Phase

| Question | Decision | Impact on Phase 002 |
|----------|----------|---------------------|
| Q1 | Turabian attribution | Quote rendering must format attribution in Turabian style |
| Q5 | Progressive sub-themes | Render `day_focus` sub-theme per day |
| Q6 | Day 7 = Sunday worship | Introduction template must include Sunday worship instructions when Day 7 present |
| Q7 | Title, Copyright, Introduction mandatory; conditional TOC | Front matter templates: title page, copyright page, Introduction, conditional TOC |
| Q11 | Day starts on new page | Page break rules: each day starts on a new page |
| Q12 | Bundled open-source fonts | Font specification in templates (specific font choices deferred to implementation) |
| Q13 | Page numbers only | Header/footer template: page numbers only; Roman/no numbers for front matter |

### Design Decisions

- Templates are separate from content (templates provide structure only)
- Templates must support both draft/preview (pending approval) and approved states
- Support both JSON (data) and Markdown (display) formats
- Front matter page numbering: Roman numerals or suppressed; content pages: Arabic numerals
- First page of each day/section may suppress page numbers per publishing convention

---

**Previous Phase**: [001-data-model-inputs.md](./001-data-model-inputs.md)
**Next Phase**: [003-kdp-pdf-export.md](./003-kdp-pdf-export.md)
