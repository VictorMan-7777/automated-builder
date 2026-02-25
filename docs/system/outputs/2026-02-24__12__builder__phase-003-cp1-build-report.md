# Build Report — Phase 003 CP1

**Date**: 2026-02-24
**Project**: devotional-generator-system-a
**Phase**: 003
**Commit Point**: CP1
**Mode**: apply
**Outcome**: CP1 COMPLETE — PASS

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
| pnpm version | 10.28.2 |
| TypeScript version | 5.9.3 (installed) |

---

## Commit Made

| CP | Hash | Message | Result |
|----|------|---------|--------|
| CP1 | `1537d3c` | `feat(phase-003): typescript project scaffold and bundled eb garamond fonts` | SUCCESS |

---

## Files Committed in CP1

| File | Description |
|------|-------------|
| `ui/.gitignore` | Excludes `node_modules/` and `dist/` |
| `ui/package.json` | pnpm package: `pdf-lib ^1.17.1`, `tsx ^4.19.2`, `vitest ^3.0.5`, `typescript ^5.7.3` |
| `ui/tsconfig.json` | TypeScript: strict, ES2022, ESNext modules, bundler resolution |
| `ui/pnpm-lock.yaml` | Dependency lockfile (exact versions pinned) |
| `ui/fonts/EBGaramond-Regular.ttf` | EB Garamond Regular (720K) |
| `ui/fonts/EBGaramond-Bold.ttf` | EB Garamond Bold (774K) |
| `ui/fonts/EBGaramond-Italic.ttf` | EB Garamond Italic (671K) |
| `ui/fonts/LICENSE.md` | Font license summary and KDP compliance note |
| `ui/fonts/OFL.txt` | Full SIL Open Font License 1.1 text |
| `ui/pdf/fonts.ts` | Font loading module: `embedFonts()`, `FONT_SIZES` constants |

---

## Installed Dependencies (resolved versions)

| Package | Resolved Version | Role |
|---------|-----------------|------|
| `pdf-lib` | 1.17.1 | PDF generation engine |
| `tsx` | 4.21.0 | TypeScript subprocess runner (Python integration) |
| `typescript` | 5.9.3 | Type checker |
| `vitest` | 3.2.4 | Test runner |
| `@types/node` | 22.19.11 | Node.js type definitions |

**esbuild note**: esbuild 0.27.3 (transitive dep of vitest) requires a postinstall
build script. Allowed via `pnpm.onlyBuiltDependencies: ["esbuild"]` in `package.json`.
Postinstall completed successfully.

---

## `ui/pdf/fonts.ts` Summary

```typescript
// embedFonts(doc: PDFDocument): Promise<EmbeddedFonts>
// Loads EBGaramond-{Regular,Bold,Italic}.ttf from ui/fonts/
// Embeds with { subset: false } — full embedding for KDP compliance (FR-86)

// FONT_SIZES constants (in points):
// TITLE: 24, SUBTITLE: 16, HEADING: 14, SUBHEADING: 12
// BODY: 11, FOOTNOTE: 9, IMPRINT: 10
```

Fonts loaded via `readFileSync` at runtime from the bundled `ui/fonts/` directory.
`__dirname` resolved via `fileURLToPath(import.meta.url)` for ESM compatibility.

---

## Verification Results

### `pnpm install`

```
pdf-lib 1.17.1 ✓
tsx 4.21.0 ✓
typescript 5.9.3 ✓
vitest 3.2.4 ✓
esbuild postinstall: Done ✓
```

**Result**: PASS — all 62 packages resolved and installed.

### `npx tsc --noEmit`

**Result**: PASS — 0 errors, 0 warnings.

### Font files present

| File | Size |
|------|------|
| `EBGaramond-Regular.ttf` | 720K |
| `EBGaramond-Bold.ttf` | 774K |
| `EBGaramond-Italic.ttf` | 671K |

**Source**: octaviopardo/EBGaramond12 GitHub repository (OFL license)
**License verification**: OFL.txt present; commercial distribution permitted.

### Binaries available

| Binary | Path |
|--------|------|
| `tsx` | `ui/node_modules/.bin/tsx` |
| `vitest` | `ui/node_modules/.bin/vitest` |
| `tsc` | `ui/node_modules/.bin/tsc` |

---

## CP1 Verification Checklist (from phase plan)

- [x] `pnpm install` completes without error
- [x] `npx tsc --noEmit` passes (no type errors in scaffold)
- [x] Font files present in `ui/fonts/`
- [x] Licenses documented in `ui/fonts/LICENSE.md` (+ full OFL.txt)
- [x] `node_modules/` excluded via `ui/.gitignore`
- [x] Working tree clean after commit

---

## Rollback

```bash
git reset --soft HEAD~1
rm -rf ui/node_modules
```

---

## Next Step

**CP2**: Margin calculation (`ui/pdf/margins.ts`) and KDP compliance checker
(`ui/pdf/compliance.ts`) with Vitest tests.
