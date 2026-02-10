# Issue-001H — Approved: Non-Canonical Context `audit` in Output Filenames

**Date:** 2026-02-09
**Issue:** Issue-001H
**Severity:** HIGH
**Inventory:** `2026-02-09__16__system__output-file-system-inventory.md`

---

## Proposal

Rename the two output files that use the non-canonical context `audit` to use
a canonical context value. No file contents are modified. No new contexts,
rules, or policy changes are introduced.

### Affected Files

| Current Filename | Proposed Filename |
|------------------|-------------------|
| `2026-02-07__03__audit__q1-quote-sourcing.md` | `2026-02-07__03__gatekeeper__q1-quote-sourcing.md` |
| `2026-02-07__05__audit__q1-quote-sourcing.md` | `2026-02-07__05__gatekeeper__q1-quote-sourcing-applied.md` |

### Context Selection

The canonical context `gatekeeper` is selected because both files document
review and audit activities (a consolidated sourcing audit and the application
of audit recommendations). The `gatekeeper` context is defined as covering
"Review/approval outputs" (`docs/system/index.md`, line 82).

### Description Adjustment

The second file's description is changed from `q1-quote-sourcing` to
`q1-quote-sourcing-applied` to resolve the duplicate description slug between
the two files on the same date and context. This is a minimal disambiguation
required by the rename, not a new policy.

---

## Change

The change consists of two `git mv` operations:

```
git mv docs/system/outputs/2026-02-07__03__audit__q1-quote-sourcing.md \
       docs/system/outputs/2026-02-07__03__gatekeeper__q1-quote-sourcing.md

git mv docs/system/outputs/2026-02-07__05__audit__q1-quote-sourcing.md \
       docs/system/outputs/2026-02-07__05__gatekeeper__q1-quote-sourcing-applied.md
```

No other files are created, modified, or deleted. File contents are unchanged.

---

## Rationale

1. The canonical context list (`docs/system/outputs/README.md`, Naming Rules,
   item 3) permits exactly four values: `planner`, `builder`, `gatekeeper`,
   `system`.
2. `audit` is not among them.
3. CP-7 (ARTIFACT-PRODUCE) requires filename compliance with the canonical
   format, including a valid context value.
4. The two affected files are the only files in the directory that fail this
   check.
5. Renaming restores compliance without altering file contents or introducing
   new naming rules.

---

## Verification

After implementation, the following checks confirm resolution:

| Check | Expected Result |
|-------|-----------------|
| No files in `docs/system/outputs/` use context `audit` | True |
| Both renamed files exist at their new paths | True |
| Both renamed files have unchanged content (byte-identical) | True |
| All 31 output artifacts use a canonical context (`planner`, `builder`, `gatekeeper`, `system`) | True |
| Sequence numbers `03` and `05` for 2026-02-07 remain occupied (no gap) | True |
| No other files were modified | True |

---

## Approval Request

Requesting approval to implement Issue-001H as specified above. The scope is
limited to two `git mv` operations. No file contents are modified. No new
rules or contexts are introduced.
