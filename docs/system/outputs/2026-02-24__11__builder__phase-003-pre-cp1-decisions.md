# Build Report — Phase 003 Pre-CP1 Decisions

**Date**: 2026-02-24
**Project**: devotional-generator-system-a
**Phase**: 003
**Commit Point**: Pre-CP1 (Decision Gate)
**Mode**: plan
**Outcome**: OPERATOR APPROVED — all three decisions confirmed; Phase 003 execution authorized

---

## Build Context

| Field | Value |
|-------|-------|
| Project slug | devotional-generator-system-a |
| Project repo | `/Users/tradingwithpython/dev/claude-projects/projects/devotional-generator-system-a` |
| Phase ID | 003 |
| Phase plan file | `phases/003-kdp-pdf-export.md` |
| Session date | 2026-02-24 |
| Node.js runtime | Node.js 24.12.0 |
| TypeScript package manager | pnpm 10.28.2 |

---

## Decision Gate

Phase 003 required operator sign-off on three decisions before any code was written.
All three decisions are one-way doors within this phase. Operator provided answers
via structured prompt. No spike test was required — operator confirmed the Builder's
recommendations directly.

---

## Decision 1: PDF Library

**Question**: `pdf-lib` or `@react-pdf/renderer`?

**Operator decision**: `pdf-lib` ✓

**Rationale recorded:**
- Full layout control required for footnote-at-page-bottom (FR-63): footnote must appear
  at the bottom of the page the quote is on, not at document end. `pdf-lib` operates
  at the primitive level (x/y coordinates per page), making this feasible.
- Two-pass margin calculation (FR-85) requires knowing final page count before setting
  margins. `pdf-lib` renders pages imperatively, making first-pass → count → recalculate
  → second-pass straightforward. `@react-pdf/renderer` auto-pagination makes this
  significantly more complex.
- TypeScript native. No React dependency needed for a CLI/subprocess PDF engine.

**Library version**: `pdf-lib` (latest stable at install time; version pinned in `package.json`)

---

## Decision 2: Font Selection

**Question**: EB Garamond, Libre Baskerville, or Lora?

**Operator decision**: EB Garamond ✓

**Fonts to bundle:**

| Role | Font | Weight/Style | Source |
|------|------|-------------|--------|
| Body text | EB Garamond | Regular | Google Fonts (OFL) |
| Headings | EB Garamond | Bold | Google Fonts (OFL) |
| Emphasis / italics | EB Garamond | Italic | Google Fonts (OFL) |

**License**: SIL Open Font License 1.1 — compatible with commercial PDF distribution.

**Bundling requirement**: Font TTF files downloaded and committed to `ui/fonts/` at CP1.
Not fetched at runtime. License documented in `ui/fonts/LICENSE.md`.

**Rationale recorded:**
- Classical serif; strong at 10–12pt for long-form reading
- Appropriate register for devotional content
- OFL confirms commercial distribution compatibility

---

## Decision 3: TypeScript Invocation Method

**Question**: `tsx` (no compile step) or pre-compiled `dist/`?

**Operator decision**: `tsx` ✓

**Integration pattern (CP5):**

```python
# Python subprocess call (src/api/pdf_export.py)
import subprocess, json

def export_pdf(document_repr: DocumentRepresentation) -> bytes:
    payload = document_repr.model_dump_json().encode()
    result = subprocess.run(
        ['npx', 'tsx', 'ui/pdf/engine.ts'],
        input=payload,
        capture_output=True,
        check=True,
    )
    return result.stdout
```

**Rationale recorded:**
- No build step required before invocation — Python can call TypeScript directly
- Simpler CI and local development: no `pnpm build` prerequisite
- Consistent with development-phase tooling: `tsx` is already a dev dependency for testing

**Constraint**: `tsx` must be in `devDependencies` in `ui/package.json`. The Python
subprocess call uses `npx tsx` so `npx` resolves it from `node_modules/.bin`.

---

## Decisions Summary

| Decision | Selected | One-way door risk |
|----------|----------|------------------|
| PDF library | `pdf-lib` | High — replacing library mid-phase is expensive but contained |
| Fonts | EB Garamond (Regular/Bold/Italic) | Medium — font swap is a CP1 re-do |
| TS invocation | `tsx` subprocess | Low — can swap to pre-compiled `dist/` later |

---

## Phase 003 CP Sequence (confirmed)

| CP | Commit Message | Build Report |
|----|---------------|--------------|
| Pre-CP1 | This document | `__11__` (this report) |
| CP1 | TypeScript scaffold + EB Garamond fonts | `__12__` |
| CP2 | Margin calculation + compliance checker | `__13__` |
| CP3 | Block-type renderers | `__14__` |
| CP4 | PDF engine end-to-end | `__15__` |
| CP5 | Python-TypeScript integration + `constitution.md` v1.3 | `__16__` |

---

## Authorization

**Operator approved all three decisions: 2026-02-24.**
**Phase 003 execution authorized. Proceed to CP1.**
