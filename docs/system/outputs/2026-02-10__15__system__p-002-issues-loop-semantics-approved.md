# P-002 Proposal — issues.md Corrected Loop Semantics

**Pending item**: P-002 — issues.md Requires Diff to Reflect Corrected Loop Semantics
**Target file**: `docs/system/issues.md`
**Baseline version**: 1.6
**Proposed version**: 1.7

---

## Context

`issues.md` defines the issue resolution loop and its templates. After the
v1.4 approval-template rewrite, the loop diagram and surrounding text still
used flat, undifferentiated step labels that obscured two critical semantics:

1. **Proposal pauses for human review** — the loop does not flow automatically
   from Proposal to Approval.
2. **Approval is the execution trigger** — Change and Summary are execution
   substeps initiated by approval, not independent loop steps.

Additionally, no rule prevented silent post-commit modification of approved
artifacts, which would undermine their role as the authoritative record.

---

## Proposed Changes

1. **Loop intro text** — replace "repeating loop per issue" with language that
   names the three phases (proposal, approval, execution) and states they
   complete before the next issue begins.
2. **Loop diagram** — annotate `Proposal` with `→ STOP (await human review)`,
   annotate `Approval` with `(execution trigger)`, indent `Change` and
   `Summary` as substeps of execution.
3. **Approved artifact immutability** — add a new constraint paragraph after the
   existing artifact-requirement paragraph: once committed, approved artifacts
   MUST NOT be modified.
4. **Version bump and changelog** — 1.6 → 1.7 with a descriptive entry.

---

## Unified Diff (v1.6 → v1.7, issues.md only)

```diff
--- a/docs/system/issues.md (v1.6)
+++ b/docs/system/issues.md (v1.7)
@@ -1,6 +1,6 @@
 # Issue Numbering and Severity Scheme

-**Version**: 1.6
+**Version**: 1.7
 **Last Updated**: 2026-02-10

 ---
@@ -88,15 +88,16 @@

 ## Issue Resolution Loop

-Issues are resolved through a repeating loop per issue:
+Issues are resolved through a repeating loop. Each issue passes through
+proposal, approval, and execution before the next issue begins:

 ```
 Inventory
-→ Proposal
-→ Approval
-→ Change
-→ Summary
-→ repeat per Issue
+→ Proposal → STOP (await human review)
+→ Approval (execution trigger)
+  → Change
+  → Summary
+→ repeat for next issue
 → Deferred / Unapproved + Verification
 → STOP
 ```
@@ -203,6 +204,10 @@
 (the renamed `*-approved.md` file). The approved artifact is the
 authoritative record of what was approved.

+**Approved artifact immutability.** Once an approved artifact is committed,
+it MUST NOT be modified. The committed artifact is the permanent record of
+what was authorized.
+
 ---

 ### Deferred / Unapproved + Verification
@@ -250,6 +255,7 @@

 | Version | Date | Changes |
 |---------|------|---------|
+| 1.7 | 2026-02-10 | Correct loop diagram to show pause-for-review and execution-trigger semantics; add approved artifact immutability rule |
 | 1.6 | 2026-02-10 | Add deferred-item disposition rules and example to verification template |
 | 1.5 | 2026-02-10 | Add proposal artifact prerequisite to approval template |
```

---

## Notes / Assumptions

- The v1.6 baseline (deferred-item disposition) is treated as already present;
  this proposal layers on top of it.
- The approval template body (lines 146–207) already correctly states "Approval
  is the execution trigger" and "Verification is NEVER part of approval." Those
  lines are not modified.
- "Approved with updates" follows the same execution sequence (lines 171–181)
  and is unaffected by these edits.
- No new workflow concepts, automation, or discovery behavior is introduced.
