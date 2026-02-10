# Issue-002H — Approved: Old-Format Filename References in README.md

**Date:** 2026-02-10
**Issue:** Issue-002H
**Severity:** HIGH
**Inventory:** `2026-02-09__16__system__output-file-system-inventory.md`

---

## Proposal

Update six locations in `docs/system/outputs/README.md` that reference the
superseded `YYYY-MM-DD-name.md` filename format. Each reference is replaced
with the canonical `YYYY-MM-DD__NN__<context>__<description>.md` format
already defined in the same file (lines 118–184). No new rules, formats, or
policies are introduced.

### Affected Locations

| # | Section | Line | Current (old format) | Proposed (canonical format) |
|---|---------|------|----------------------|----------------------------|
| 1 | Best Practice | 233 | `docs/system/outputs/YYYY-MM-DD-name.md` | `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md` |
| 2 | Example 3 | 312 | `docs/system/outputs/YYYY-MM-DD-context-name.md` | `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md` |
| 3 | Integration / Planner | 322 | `YYYY-MM-DD-planning-<project>-iteration-N.md` | `YYYY-MM-DD__NN__planner__<description>.md` |
| 4 | Integration / Builder | 328 | `YYYY-MM-DD-build-phase-NNN.md` | `YYYY-MM-DD__NN__builder__<description>.md` |
| 5 | Integration / Gatekeeper | 334 | `YYYY-MM-DD-gate-<phase-or-milestone>.md` | `YYYY-MM-DD__NN__gatekeeper__<description>.md` |
| 6 | Compliance checklist | 371 | `YYYY-MM-DD-name.md` | `YYYY-MM-DD__NN__<context>__<description>.md` |

---

## Change

Six text replacements in `docs/system/outputs/README.md`. No other files are
created, modified, or deleted. The surrounding prose for each location is
adjusted minimally to remain coherent with the updated format references.

### Change 1 — Best Practice (line 233)

```
Before:
2. Claude saves to `docs/system/outputs/YYYY-MM-DD-name.md`

After:
2. Claude saves to `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md`
```

### Change 2 — Example 3 (line 312)

```
Before:
2. Save to `docs/system/outputs/YYYY-MM-DD-context-name.md`

After:
2. Save to `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md`
```

### Change 3 — Integration / Planner (line 322)

```
Before:
- Save planning summary to `docs/system/outputs/YYYY-MM-DD-planning-<project>-iteration-N.md`

After:
- Save planning summary to `docs/system/outputs/YYYY-MM-DD__NN__planner__<description>.md`
```

### Change 4 — Integration / Builder (line 328)

```
Before:
- Save phase completion report to `docs/system/outputs/YYYY-MM-DD-build-phase-NNN.md`

After:
- Save phase completion report to `docs/system/outputs/YYYY-MM-DD__NN__builder__<description>.md`
```

### Change 5 — Integration / Gatekeeper (line 334)

```
Before:
- Save review decision to `docs/system/outputs/YYYY-MM-DD-gate-<phase-or-milestone>.md`

After:
- Save review decision to `docs/system/outputs/YYYY-MM-DD__NN__gatekeeper__<description>.md`
```

### Change 6 — Compliance checklist (line 371)

```
Before:
1. ✅ Follow naming convention (YYYY-MM-DD-name.md)

After:
1. ✅ Follow naming convention (YYYY-MM-DD__NN__<context>__<description>.md)
```

---

## Rationale

1. The canonical format `YYYY-MM-DD__NN__<context>__<description>.md` is
   defined in the same file (Naming Convention section, lines 118–184).
2. The six old-format references predate the canonical format and were not
   updated when the Naming Convention section was added.
3. A session reading this README receives conflicting format instructions
   within a single document.
4. All six replacements align each reference with the format already defined
   as authoritative in the same file.
5. No new rules, contexts, or naming conventions are introduced.

---

## Verification

After implementation, the following checks confirm resolution:

| Check | Expected Result |
|-------|-----------------|
| No references to `YYYY-MM-DD-name.md` pattern remain in README.md | True |
| No references to `YYYY-MM-DD-context-name.md` pattern remain in README.md | True |
| No references to `YYYY-MM-DD-planning-` pattern remain in README.md | True |
| No references to `YYYY-MM-DD-build-phase-` pattern remain in README.md | True |
| No references to `YYYY-MM-DD-gate-` pattern remain in README.md | True |
| All six updated lines reference the canonical format | True |
| No other files were modified | True |
| Naming Convention section (lines 118–184) is unchanged | True |

---

## Approval Request

Requesting approval to implement Issue-002H as specified above. The scope is
limited to six text replacements in `docs/system/outputs/README.md`. No other
files are modified. No new rules or formats are introduced.
