# Issue-005 — Approved: "Current Structure" Section Frozen at Initial State

**Date:** 2026-02-10
**Issue:** Issue-005
**Severity:** LOW
**Inventory:** `2026-02-09__16__system__output-file-system-inventory.md`

---

## Proposal

Replace the static "Current Structure" file tree in
`docs/system/outputs/README.md` with a note that the directory listing is
the source of truth. Update the file header (Version, Last Updated) and
Document History to reflect accumulated changes.

No new rules, formats, or policies are introduced.

---

## Problem

The "Current Structure" tree (lines 335–341) shows only two files from
2026-02-05. The directory now contains 30+ artifacts. The static tree went
stale immediately after the first new output was created and will go stale
again if updated with a new snapshot.

The file header still reads `Version: 1.0, Last Updated: 2026-02-05` despite
multiple changes to the file since then (Issue-002H canonical format
references, Issue-003 output capture rule replacement).

---

## Changes

### Change 1 — Replace "Current Structure" tree (lines 333–341)

```
Before:
### Current Structure

` ` `
docs/system/outputs/
├── README.md (this file)
├── 2026-02-05__01__planner__reorganization-summary.md
├── 2026-02-05__02__system__long-output-capture-implementation.md
└── (future outputs...)
` ` `

After:
### Current Structure

The authoritative directory listing is the filesystem itself. Run
`ls docs/system/outputs/` or check the repository for the current file
inventory. Static file trees in this section are not maintained because
the directory changes frequently.
```

### Change 2 — Remove "Future Structure" tree (lines 343–355)

The "Future Structure (with archives)" subsection contains the same stale
two-file listing and speculates about an `archive/` directory that does not
exist. Remove the entire subsection. If archival is adopted in the future,
it will be documented at that time.

### Change 3 — Update file header (lines 5–6)

```
Before:
**Version**: 1.0
**Last Updated**: 2026-02-05

After:
**Version**: 1.1
**Last Updated**: 2026-02-10
```

### Change 4 — Update Document History (line 391)

```
Before:
| 1.0 | 2026-02-05 | Initial long output capture rule documentation |

After:
| 1.1 | 2026-02-10 | Replace stale file trees with filesystem-is-source-of-truth note; update header (Issue-005). Incorporates prior changes: canonical format references (Issue-002H), output capture rule replacement (Issue-003) |
| 1.0 | 2026-02-05 | Initial long output capture rule documentation |
```

---

## Rationale

1. A static file tree goes stale as soon as a new output artifact is created.
   The directory changes on every session that produces an artifact.
2. The inventory itself notes this is "cosmetic drift rather than a behavioral
   risk" — the real directory listing is the source of truth.
3. Replacing the static tree with a pointer to the filesystem eliminates the
   maintenance burden without losing information.
4. The "Future Structure" subsection is speculative and contains the same
   stale listing. Removing it avoids maintaining a second stale tree.
5. The header version and Document History have not been updated through
   any prior changes to this file.

---

## Verification

After implementation, the following checks confirm resolution:

| Check | Expected Result |
|-------|-----------------|
| No static file tree listing output artifacts in "Directory Organization" section | True |
| "Current Structure" subsection contains filesystem-as-source-of-truth note | True |
| "Future Structure" subsection removed | True |
| Header shows Version 1.1, Last Updated 2026-02-10 | True |
| Document History contains v1.1 entry | True |
| No other sections of README.md were modified | True |
| No other files were modified | True |

---

## Approval Request

Requesting approval to implement Issue-005 as specified above. The scope is
limited to four edits in `docs/system/outputs/README.md` (replace static
tree, remove speculative tree, update header, update history). No other files
are modified. No new rules or policies are introduced.
