# Phase 003: KDP PDF Export

## Phase Information

- **Phase**: 003
- **Name**: KDP PDF Export
- **Status**: Not Started
- **Dependencies**: Phase 002 complete

## Objective

Generate a KDP-compliant 6x9 inch PDF with proper margins, fonts, and layout for Amazon print publishing.

---

## Scope

### In Scope

- Page layout system (6x9 with KDP margins)
- PDF generation engine
- Bundled open-source font embedding
- Front matter page generation: title page, copyright page, Introduction, conditional TOC
- Page numbering (Roman/suppressed for front matter; Arabic for content)
- Page break logic (each day starts on new page)
- Scripture web retrieval (NASB) — or designated as new phase
- AI content generation pipeline (reflections with expanded references) — or designated as new phase
- Conditional KDP validation based on output mode (publish-ready vs personal)

### Out of Scope

- Full validation logic (Phase 004)
- Cover design
- Bowker ISBN integration (use Amazon-provided ISBN for MVP)
- Multi-format export

---

## KDP Specifications

### Page Dimensions

| Specification | Value |
|---------------|-------|
| Trim Size | 6 x 9 inches (15.24 x 22.86 cm) |
| PDF Size | Same as trim (no bleed for text-only) |

### Margins

| Margin | Minimum | Recommended | Notes |
|--------|---------|-------------|-------|
| Inside (Gutter) | 0.375" | 0.5" | Binding side; increases with page count |
| Outside | 0.25" | 0.5" | Opposite binding |
| Top | 0.25" | 0.5" | Header space if used |
| Bottom | 0.25" | 0.5" | Footer/page number space |

### Font Requirements

- Bundled open-source fonts must be embedded in PDF
- Specific font choices deferred to implementation (candidates: Lora, EB Garamond, Crimson Text for body; Playfair Display for headings)
- Body text: 10-12pt
- Headings: 14-18pt

### PDF Format

- PDF/X-1a:2001 (preferred for print)
- OR standard PDF with all fonts embedded

---

## Commit Points

### CP5: Page Layout and Margins

**Goal**: Define 6x9 page layout with KDP-compliant margins

**Deliverables**:
- `layout/page-config.yaml` - Page dimension and margin configuration
- `layout/page-template.css` - Print-ready CSS for layout

**Page Configuration**:
```yaml
page:
  width: 6in
  height: 9in

margins:
  inside: 0.5in   # Gutter for binding
  outside: 0.5in
  top: 0.5in
  bottom: 0.5in

content_area:
  width: 5in      # 6 - 0.5 - 0.5
  height: 8in     # 9 - 0.5 - 0.5
```

**CSS Layout**:
```css
@page {
  size: 6in 9in;
  margin: 0.5in;
}

@page :left {
  margin-right: 0.5in;  /* Outside margin */
  margin-left: 0.5in;   /* Gutter */
}

@page :right {
  margin-left: 0.5in;   /* Outside margin */
  margin-right: 0.5in;  /* Gutter */
}
```

**Files to Stage**:
- `layout/page-config.yaml`
- `layout/page-template.css`

**Commit Command**:
```bash
git add layout/
git commit -m "feat(devotional-generator): add 6x9 page layout with KDP margins (CP5)"
```

**Verification**:
- [ ] Page size is exactly 6x9 inches
- [ ] Margins meet KDP minimums
- [ ] Content area calculated correctly

**Rollback**:
```bash
git reset --soft HEAD~1
rm -rf layout/
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | M (Medium) |
| AI Mitigation | Provide: diff summary, explicit margin values, visual margin check |
| Elevated Check | Verify margins against KDP spec table before approval |

---

### CP6: PDF Generation with Fonts

**Goal**: Generate PDF from templates with embedded fonts

**Deliverables**:
- `export/pdf-generator.py` - PDF generation module
- `export/fonts/` - Bundled fonts (if needed)
- Font embedding verification

**PDF Generation Options**:

| Library | Pros | Cons |
|---------|------|------|
| WeasyPrint | HTML/CSS to PDF, consistent with templates | System dependencies (Cairo, Pango) |
| ReportLab | Python-native, no system deps | More complex layout code |
| wkhtmltopdf | Mature, reliable | Binary dependency |

**Recommended**: WeasyPrint (with ReportLab as fallback)

**Font Strategy**:
- Primary: Bundled open-source fonts (specific selection deferred to implementation)
- Candidate body fonts: Lora, EB Garamond, Crimson Text, Source Serif
- Candidate heading fonts: Playfair Display
- Font files included in repository under `export/fonts/`
- Verify embedding with PDF reader inspection

**Files to Stage**:
- `export/pdf-generator.py`
- `export/fonts/` (if using bundled fonts)
- `requirements.txt` (updated with WeasyPrint)

**Commit Command**:
```bash
git add export/ requirements.txt
git commit -m "feat(devotional-generator): add PDF generation with font embedding (CP6)"
```

**Verification**:
- [ ] PDF generates without errors
- [ ] Fonts display correctly in PDF
- [ ] Font embedding verified (check PDF properties)
- [ ] Page dimensions correct in PDF reader

**Rollback**:
```bash
git reset --soft HEAD~1
rm -rf export/
# Revert requirements.txt changes
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | M (Medium) |
| AI Mitigation | Provide: diff summary, font embedding verification command output |
| Elevated Check | Open PDF in reader, verify fonts show "Embedded" in properties |
| AI Weakness Note | Claude Code may not catch system-specific font issues; manual verification required |

---

### CP7: Front Matter and Page Numbers

**Goal**: Add front matter pages (title, copyright, introduction, conditional TOC) and page numbering

**Deliverables**:
- `templates/title-page.html` - Title page template
- `templates/copyright-page.html` - Copyright page template
- `templates/introduction-page.html` - Introduction template (includes Sunday worship guidance when Day 7 present)
- `templates/toc-page.html` - Table of contents template (conditional)
- Page numbering in footer
- Page break logic (new day starts new page)

**Front Matter Pages** (in order):
1. **Title page**: Book title, topic, author name
2. **Copyright page**: Author, year, rights statement
3. **Introduction**: Book purpose, how to use the devotional, Sunday worship instructions (when Day 7 present)
4. **Table of Contents** (conditional): Include when day count >= threshold (e.g., 12 days)

**Page Numbering**:
- Front matter pages: Roman numerals or no page numbers
- Content pages: Arabic numerals, bottom center, starting from 1
- First page of each day/section: page number may be suppressed per publishing convention

**Page Break Rules**:
- Each day starts on a new page
- Each front matter page is standalone
- No blank pages unless needed for left/right alignment

**Files to Stage**:
- `templates/title-page.html`
- Updated `export/pdf-generator.py`
- `examples/sample-output.pdf`

**Commit Command**:
```bash
git add templates/title-page.html export/pdf-generator.py examples/sample-output.pdf
git commit -m "feat(devotional-generator): add title page and page numbering (CP7)"
```

**Verification**:
- [ ] Title page renders correctly
- [ ] Page numbers appear on content pages
- [ ] Each day starts on new page
- [ ] No page number on title page

**Rollback**:
```bash
git reset --soft HEAD~1
# Revert specific file changes
```

**Execution Attribution**:
| Field | Value |
|-------|-------|
| Executor | AI: Claude Code |
| Verifier | Human: Barbara |
| Risk | L (Low) |
| AI Mitigation | Provide: diff summary, sample PDF with title page |

---

## Acceptance Criteria

### Phase Complete When:

- [ ] PDF is exactly 6x9 inches
- [ ] Margins meet KDP specifications
- [ ] Bundled open-source fonts embedded in PDF
- [ ] Front matter pages render correctly: title, copyright, Introduction
- [ ] Conditional TOC renders when enabled
- [ ] Introduction includes Sunday worship guidance when Day 7 is present
- [ ] Page numbers: Roman/suppressed for front matter, Arabic for content
- [ ] Each day starts on new page
- [ ] PDF opens correctly in standard readers
- [ ] Sample PDF can be uploaded to KDP for preview
- [ ] Publish-ready output meets 24-page minimum (or warns if below)

---

## Gatekeeper Checklist

**Executor**: AI: Claude Code
**Verifier**: Human: Barbara

### Human Review Required

- [ ] PDF layout looks professional
- [ ] Margins are comfortable for reading
- [ ] Font choices are appropriate
- [ ] Title page design is acceptable

### Verification Reference

See `docs/system/ai.md` for AI executor output requirements.

### KDP Verification

- [ ] Upload sample PDF to KDP print previewer
- [ ] No margin/bleed warnings
- [ ] Text is readable in preview
- [ ] Page count as expected

---

## Technical Notes

### WeasyPrint Installation

**macOS**:
```bash
brew install cairo pango gdk-pixbuf libffi
pip install weasyprint
```

**Ubuntu/Debian**:
```bash
sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0
pip install weasyprint
```

**Windows**:
- Use pip-installable version or ReportLab alternative

### Verifying Font Embedding

1. Open PDF in Adobe Reader or Preview
2. File > Properties > Fonts
3. Verify all fonts show "Embedded" or "Embedded Subset"

### Common PDF Issues

| Issue | Solution |
|-------|----------|
| Fonts not embedded | Use WeasyPrint's font configuration |
| Wrong page size | Check @page CSS rule |
| Margins off | Verify @page margin values |
| Blurry text | Ensure PDF is generated at print resolution |

---

## Resolved Questions Affecting This Phase

| Question | Decision | Impact on Phase 003 |
|----------|----------|---------------------|
| Q2 | NASB, web-retrieved | Scripture web retrieval implementation (API or scraping); error handling for network failures |
| Q3 | AI-generated reflections; human approval | AI content generation pipeline; no export without approval |
| Q4 | Variable day count; dual output modes | Conditional KDP validation based on `output_mode`; 24-page minimum warning for publish-ready |
| Q7 | Title, Copyright, Introduction mandatory; conditional TOC | Front matter page generation, ordering, and conditional TOC logic |
| Q10 | Amazon-provided ISBN; Bowker deferred | No ISBN implementation needed for MVP |
| Q11 | Day starts on new page | Page break implementation confirmed |
| Q12 | Bundled open-source fonts | Font bundling and embedding; specific fonts deferred to implementation |
| Q13 | Page numbers only | Page numbering: Roman/suppressed for front matter, Arabic for content |

**Decisions Applied**:
- Each day starts on a new page (may span multiple pages)
- Bundled open-source fonts (no system font dependency)
- Front matter: title, copyright, introduction (mandatory); TOC (conditional for larger books)

---

**Previous Phase**: [002-template-system.md](./002-template-system.md)
**Next Phase**: [004-validation-preview.md](./004-validation-preview.md)
