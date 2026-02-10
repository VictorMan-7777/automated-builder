# P-015 Verification — Verification Template Add Pending-Item Context

**Date**: 2026-02-10
**Context**: system
**Pending Item**: P-015
**Verification method**: Dogfood — apply the updated template (v1.9) against P-016

---

## Pending-Item Context (P-015)

- **Pending item ID**: P-015
- **Intent and scope**: Update the verification template in `docs/system/issues.md`
  to include Pending-item context fields (P-###, target file(s), proposal artifact,
  acceptance checks) so verification works for non-inventory changes as well.
- **Acceptance criteria**:
  1. Template requires Pending-item context (P-### ID, intent/scope, acceptance
     criteria) in verification artifacts.
  2. No active language implies that approval moves P-### items to Completed.
  3. Template explicitly states that approval authorizes execution and
     verification authorizes completion.

---

## Dogfood Test — Template Applied to P-016

The following demonstrates that the updated template (v1.9) can be applied to
P-016 without ad-hoc additions. Each required section is populated below.

### 1. Pending-Item Context (P-016)

| Field | Value |
|-------|-------|
| Pending item ID | P-016 |
| Intent and scope | Add/clarify system rule that every Claude iteration must produce an output artifact (`access.md`, `initial-prompt.md`, `prompt-template.md`, `outputs/README.md`) to prevent untracked changes and lost work. |
| Acceptance criteria | Unconditional output rule present in all governance files; no artifact-type gate; compliance clause applies to every session; enforcement is mandatory, not advisory. |

**Result: All three context fields populated from `pending-items.md` and the
execution artifact. No ad-hoc fields needed.**

### 2. Checks (P-016)

| Check | Result | Evidence |
|-------|--------|----------|
| Unconditional rule in all 4 governance files | PASS | Re-verification `__23__`, cross-file consistency table |
| No artifact-type gate remains | PASS | Old conditional language replaced in all files |
| Enforcement is mandatory (not advisory) | PASS | "must"/"MUST" verbs, stop conditions, failure consequences |
| Approval/authorization trail exists | PASS | Retroactive approval `__22__` closes artifact gap |

**Result: Template's "Checks" section accommodated P-016's checks without
modification.**

### 3. Verdict (P-016)

PASS — per re-verification artifact `2026-02-10__23__system__p-016-re-verification.md`.

**Result: Verdict section exercised.**

### 4. Completion Authority (P-016)

Under the updated template, verification — not approval — authorizes completion.
The re-verification (`__23__`) verdict is PASS, so under v1.9 rules, completion
would be authorized by that verification artifact.

Note: P-016 was moved to Completed prior to P-015 via user override, documented
in `pending-items.md` with the note "Completion authorized by user override."
This is a pre-existing state, not a P-015 issue.

**Result: Completion authority section exercised. The template correctly places
the decision at verification, not approval.**

---

## Checks — P-015 Template Change

### Check 1 — Template requires Pending-item context fields

**Result: PASS**

`docs/system/issues.md` lines 261-264 now require:
- Pending item ID (P-###)
- Intent and scope (from the item's Summary in `pending-items.md`)
- Acceptance criteria: what constitutes "done" for this item

The dogfood test above confirms all three fields are fillable for P-016.

### Check 2 — No active language implies approval moves P-items to Completed

**Result: PASS**

Grep for `Completed`, `completion`, and `move.*Pending` in `issues.md` found
these occurrences in active template language:

| Line | Text | Assessment |
|------|------|------------|
| 184 | "It does not authorize marking a P-### item as Completed" | Correct — explicitly denies approval completion authority |
| 186 | "authorizes their completion" | Correct — refers to verification as the authority |
| 271-276 | Completion authority subsection | Correct — places authority at verification |
| 278-282 | Backlog hygiene at verification | Correct — moves items at verification, not approval |

Line 291 (document history, v1.8 entry) references the old rule but is a
historical record, not active template language.

No active language implies that approval moves P-### items to Completed.

### Check 3 — Approval authorizes execution; verification authorizes completion

**Result: PASS**

| Authority | Template location | Language |
|-----------|-------------------|----------|
| Approval → execution | Line 183 | "Approval authorizes execution of the approved change." |
| Approval ≠ completion | Line 184 | "It does not authorize marking a P-### item as Completed." |
| Verification → completion | Lines 271-272 | "Verification — not approval — authorizes marking a P-### item as Completed." |

The separation is explicit and unambiguous.

---

## Verdict: PASS

P-015's template changes satisfy all three acceptance criteria:

1. The verification template now requires Pending-item context fields
   (P-### ID, intent/scope, acceptance criteria).
2. No active language implies that approval moves P-### items to Completed.
3. Approval authorizes execution and verification authorizes completion,
   stated explicitly in both templates.

The dogfood test against P-016 confirms the template is exercisable for
non-inventory changes without ad-hoc additions.

---

## Completion Authority

Per the updated template (v1.9, line 271): verification authorizes completion.

**Completion is authorized for P-015.** All acceptance criteria are met and the
verdict is PASS.

No status changes applied in this artifact per instructions.

---

## Files Examined

| File | Purpose |
|------|---------|
| `docs/system/issues.md` (v1.9) | Updated verification template — target of P-015 |
| `docs/system/pending-items.md` | P-015 and P-016 definitions |
| `docs/system/outputs/2026-02-10__20__system__p-016-execution-output-artifact-every-iteration.md` | P-016 execution artifact |
| `docs/system/outputs/2026-02-10__21__system__p-016-verification.md` | P-016 first verification (FAIL) |
| `docs/system/outputs/2026-02-10__22__system__p-016-retroactive-approval.md` | P-016 retroactive approval |
| `docs/system/outputs/2026-02-10__23__system__p-016-re-verification.md` | P-016 re-verification (PASS) |
| `docs/system/outputs/2026-02-10__24__system__p-015-verification-template-update.md` | P-015 implementation artifact |

---

## Pending Item Status

P-015 remains in **Pending** in `docs/system/pending-items.md`. No status
changes were made per instructions.
