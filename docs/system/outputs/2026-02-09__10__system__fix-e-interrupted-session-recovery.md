# Fix E Proposal — Pending Approval

**Date:** 2026-02-09
**Status:** Pending approval
**Source:** Architecture Review Pass 1 (`2026-02-09__01__system__architecture-review-pass-1.md`), Finding 9
**Severity:** MEDIUM
**Scope:** Single-file addition to an APPROVED document

---

## 1) Definition of "Interrupted Session"

A session is **interrupted** if it terminates before CP-9 (POSTCHECK) records
a PASS.

This includes:

| Cause | Example |
|-------|---------|
| HARD checkpoint failure with abandonment | CP-5 work fails; human decides to abandon rather than retry. |
| Context exhaustion | Session reaches context window limit before completing CP-8 or CP-9. |
| Operator termination | Human ends the session early (closes window, issues stop command). |
| System failure | Crash, network loss, or platform interruption. |

A session that pauses at a SOFT stop (CP-5) and later resumes is NOT
interrupted — it is paused. Interruption means the session will not resume.

---

## 2) The Problem

The taxonomy's ordering rule (Section 3.2, rule 2) states:

> "A checkpoint MUST NOT be entered until all prior checkpoints have passed."

INV-7 (Section 4.3) states:

> "Every session produces a reviewable artifact."

These conflict when a session is interrupted before CP-7. If CP-5 fails and
the session is abandoned, CP-7 cannot be entered (ordering rule), so no
artifact is produced (INV-7 violated). The session leaves behind:

- Possible commits in the project repo with no corresponding report.
- Possible untracked artifacts on disk (written but never committed).
- No record in the builder/planner repo of what happened.

The `run-builder.md` prompt informally handles one case (CP verification
failure → "Write an error report"), but the taxonomy has no formal exception
path, and no document addresses the recovery of uncommitted artifacts left
by a terminated session.

---

## 3) Mandatory Recovery Protocol

### 3a. In-session interruption artifact (session still active)

When a session is being abandoned (human decides not to retry after a HARD
stop or unrecoverable error), and the session is still active:

1. **CP-7 may be entered out of order** for the sole purpose of producing an
   interruption report. This is the only permitted violation of the checkpoint
   ordering rule.
2. The interruption artifact MUST clearly identify itself as an interruption
   report (not a success artifact). It must document:
   - Which checkpoints passed (with evidence).
   - Which checkpoint failed and why.
   - What state was left behind (commits made, files on disk, partial work).
   - Whether recovery is needed by a subsequent session or operator.
3. **CP-8 may then be entered** to commit the interruption artifact. The
   commit message must indicate it is an interruption record, not a normal
   session completion.
4. CP-9 is skipped (the session did not complete normally; recording a
   POSTCHECK would be misleading).

### 3b. Post-termination recovery (session is gone)

When a session terminated without producing or committing its artifact
(context exhaustion, crash, operator abort), recovery falls to the **next
session operator or the human**:

**Detection:** At the start of a new session, or during routine operator
inspection, check for evidence of a prior interrupted session:

- Untracked files in `docs/system/outputs/` that were not committed.
- Uncommitted modifications in the working tree.
- Commits in a project repo that have no corresponding report in the
  builder repo's `docs/system/outputs/`.

**Recovery commit:** If orphaned artifacts are found on disk:

1. Review the artifact content for correctness and completeness.
2. If the artifact is a valid record of the interrupted session's work,
   commit it with the message format:
   `outputs: recover interrupted session artifact from YYYY-MM-DD`
3. If the artifact is incomplete or corrupt, either complete it manually
   with available information (session transcript, git log) and commit, or
   delete it and document the gap in a new interruption report.

**Abandon without recovery:** If no artifacts exist on disk and the session
transcript is unavailable, the interruption is unrecoverable. The operator
should create a brief interruption report documenting:
- That a session was interrupted.
- The date and approximate scope.
- That no artifacts could be recovered.
- Commit this report to preserve the audit trail gap as a known gap rather
  than an invisible one.

### 3c. When to abandon vs recover

| Situation | Action |
|-----------|--------|
| Artifact exists on disk, content is complete | Recover: commit as-is. |
| Artifact exists on disk, content is partial | Recover: complete from transcript/logs if possible, then commit. |
| No artifact on disk, transcript available | Recover: create interruption report from transcript, commit. |
| No artifact on disk, no transcript | Abandon: create a gap report, commit. |
| Commits in project repo with no builder report | Recover: create retrospective interruption report documenting the orphaned commits, commit to builder repo. |

---

## 4) Where This Protocol Should Be Specified

**Primary change:**
- `docs/implementation/system/checkpoint-taxonomy.md` — Add a new Section 3.4 "Interrupted Sessions" after Section 3.3 (Checkpoint Definitions) and before Section 4 (Execution Contract).

This is the right location because:
- The protocol is an exception to the ordering rules defined in Section 3.2.
- It governs checkpoint behavior, not output formatting or naming.
- It directly modifies how INV-7 is satisfied under failure conditions.

**No changes required to:**
- `docs/system/outputs/README.md` — Interrupted session artifacts are still output artifacts. They follow the same naming rules, the same System Iterator protocol, and the same retention policy. No lifecycle change is needed.
- Checkpoint definitions (CP-1 through CP-9) — Their individual verification criteria are unchanged. The exception path permits entering CP-7 and CP-8 out of order; it does not alter what those checkpoints verify.
- INV-7 — The invariant text remains "Every session produces a reviewable artifact." The new section clarifies *how* this is satisfied when normal ordering breaks, not whether it applies.

---

## 5) Rule-Level Description of Changes

Add Section 3.4 to the checkpoint taxonomy containing:

1. **Definition:** What constitutes an interrupted session (terminated before CP-9 PASS; distinct from a SOFT-stop pause).

2. **In-session exception path:** When the session is still active but being abandoned, CP-7 and CP-8 may be entered out of order to produce and commit an interruption artifact. CP-9 is skipped. The artifact must self-identify as an interruption report and document checkpoint status, failure cause, and residual state.

3. **Post-termination recovery protocol:** When a session terminated without committing its artifact, the next operator detects orphaned artifacts or orphaned commits and performs a recovery commit. Format specified for the recovery commit message.

4. **Abandon criteria:** When no recovery is possible, the operator creates a gap report to make the audit trail gap visible rather than invisible.

No other section of the taxonomy is modified. No new invariants, no new checkpoints, no new mechanisms.

---

## 6) Acceptance Criteria

1. The taxonomy defines "interrupted session" with clear boundaries (terminated before CP-9; distinct from pause).
2. A session that is abandoned after a HARD stop can produce an interruption artifact without violating the taxonomy (CP-7 exception path is explicit).
3. A session that terminates without committing has a defined recovery path for the next operator.
4. The recovery protocol covers all five situations in the abandon-vs-recover table.
5. INV-7 ("every session produces a reviewable artifact") is satisfiable for interrupted sessions, either via the in-session exception path or via post-termination recovery.
6. No existing checkpoint definitions, invariants, or evidence requirements are modified.
7. The audit trail for interrupted sessions is unambiguous — either an interruption artifact exists, or a gap report exists. Silent gaps are eliminated.

---

## 7) Proposed Commit Message

```
docs(implementation): add interrupted session protocol to checkpoint taxonomy
```

Single-purpose commit. One file modified (`docs/implementation/system/checkpoint-taxonomy.md`).
