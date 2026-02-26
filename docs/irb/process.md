# IRB Process — Independent Review Board Lifecycle

**Document ID:** irb-process
**Version:** 1.0.0
**Scope:** All projects under automated-builder governance

---

## Purpose

The Independent Review Board (IRB) is a deterministic, evidence-gated certification
framework. It certifies that a project meets minimum structural, build, and behavioral
requirements at defined milestones before any downstream action is taken.

IRB is not a linting tool or a style guide. It is a gate: a project either meets the
stated invariants or it does not. Outcomes are binary — `CERTIFIED` or `FAILED` — and
are produced by a runner that leaves no room for judgment calls.

---

## Tier Progression Diagram

```
                         ┌─────────────────────────────┐
                         │   Phase 0: External Surface  │
                         │   Review (e.g., CodeRabbit)  │
                         │   OPTIONAL — advisory only   │
                         └──────────────┬──────────────┘
                                        │  (human reviews advisory output)
                                        ▼
                         ┌─────────────────────────────┐
                         │   Tier 1: Core Architecture  │◄─── BLOCKING GATE
                         │   Certification              │     Deterministic runner
                         │   REQUIRED before Tier 2    │     Exit 0 = CERTIFIED
                         └──────────────┬──────────────┘     Exit 1 = FAILED
                                        │  (CERTIFIED required)
                                        ▼
                         ┌─────────────────────────────┐
                         │   Tier 2: Feature Integration│◄─── STAGED FUTURE
                         │   Review                     │     Not yet implemented
                         └──────────────┬──────────────┘
                                        │  (CERTIFIED required)
                                        ▼
                         ┌─────────────────────────────┐
                         │   Tier 3: Adversarial        │◄─── STAGED FUTURE
                         │   Simulation                 │     Not yet implemented
                         └─────────────────────────────┘
```

---

## Phase 0 — External Surface Review

**Status:** Optional, advisory
**Tool examples:** CodeRabbit, manual code review, static analysis

### Purpose

Phase 0 provides a lightweight, human-readable surface scan of a pull request or
branch before IRB tiers run. It is not part of the IRB certification chain and cannot
substitute for any IRB tier.

### What it covers

- Stylistic issues, obvious bugs, missing edge cases
- Documentation gaps
- General code quality observations

### Trigger condition

Invoked at operator discretion — typically on a pull request or at a phase boundary
before Tier-1 is triggered.

### Halt gate

None. Phase 0 output is advisory. A human operator reviews the output and decides
whether to address findings before triggering Tier-1. Proceeding past Phase 0 findings
is a human decision, not an IRB decision.

### Important constraint

**External reviewers (e.g., CodeRabbit) are advisory and are not substitutes for
deterministic IRB tiers.** An "approved" Phase 0 review does not imply or confer
Tier-1 certification. Tier-1 must be run independently and must exit `CERTIFIED` on
its own evidence.

---

## Tier 1 — Core Architecture Certification

**Status:** Required, deterministic, blocking
**Runner:** `scripts/irb/builder review --tier 1 --target <path>`
**Spec:** `specs/irb/tier-1-spec.yaml` (v2.0.0, 23 checks)
**Human spec:** [docs/irb/tier-1-spec.md](tier-1-spec.md)
**Runbook:** [docs/irb/runbook.md](runbook.md)

### Purpose

Tier-1 certifies that a target repository meets minimum structural, build, and artifact
lifecycle requirements. It is the foundation gate: if a project cannot pass Tier-1, no
higher-tier review is attempted.

### What it covers

| Category | Checks | Blocking |
|----------|--------|----------|
| REPO | Git validity, HEAD commit readable, pyproject present, clean tree | Partially |
| ARCH | `src/` layout, required modules, pipeline entry point, hard-halt preserved | All blocking |
| BUILD | Interpreter available, pytest exits zero, test count minimum, zero failures | Mostly blocking |
| ARTIFACT | Store source files, ID policy sources, lifecycle tests (from cached build) | All blocking |
| ARTIFACT (advisory) | Runtime artifact directory and file presence | None |
| GUARD | Repo mutation guard (before/after git status delta) | Blocking |

### Evidence-gated rule

**No artifact, no credit.** Every check must collect concrete evidence before
evaluating its pass condition. If evidence collection fails — command not found, file
unreadable, subprocess error, missing cache — the check status is `FAIL` with
`evidence_collected: false`. Passing a check on absent evidence is never permitted.

### Trigger condition

Tier-1 is triggered by the operator at a defined project milestone (e.g., a completed
phase checkpoint). It must be triggered explicitly — it does not run automatically.

```bash
scripts/irb/builder review --tier 1 --target /path/to/repo
```

### Halt gate

- **Exit 0 (`CERTIFIED`):** All blocking checks passed. Operator may proceed to the
  next authorized action (Phase 014 or Tier-2 when available).
- **Exit 1 (`FAILED`):** One or more blocking checks failed. No downstream action may
  be taken. Operator must investigate, remediate, and re-run Tier-1.
- **Exit 2 (`ERROR`):** Runner crashed before producing a report. Investigate runner
  error before retrying.

**The runner halts after writing its report. It does not initiate any next-phase action,
modify the target repository, or spawn any additional process. Control returns to the
operator.**

### Advisory vs blocking

Non-blocking (advisory) failures are recorded with full evidence but do not affect the
`CERTIFIED`/`FAILED` outcome. Advisory failures are expected on clean clones (e.g.,
runtime artifact directories unpopulated).

### Dependency skip logic

Checks with a `depends_on` field are marked `SKIP` if the dependency did not `PASS`.
`SKIP` on an advisory check does not affect outcome. `SKIP` on a blocking check is
treated conservatively — the dependency failure that caused the skip is itself blocking.

---

## Tier 2 — Feature Integration Review

**Status:** Staged future — not yet implemented

### Anticipated purpose

Tier-2 will verify that newly integrated features satisfy their stated behavioral
contracts. Where Tier-1 certifies structure and build, Tier-2 certifies integration:
that the components wired together produce correct observable outputs.

### Anticipated scope

- End-to-end pipeline correctness checks (not just unit tests)
- Interface contract verification between modules
- Artifact content validation (schema, invariants, non-emptiness)
- Regression guards for previously certified behaviors

### Trigger condition (anticipated)

Tier-2 will require a valid Tier-1 `CERTIFIED` report for the same target HEAD SHA
before it runs. A stale or mismatched Tier-1 report will cause Tier-2 to exit `ERROR`.

### Halt gate (anticipated)

Same exit-code semantics as Tier-1. Tier-2 `CERTIFIED` required before Tier-3 runs.

---

## Tier 3 — Adversarial Simulation

**Status:** Staged future — not yet implemented

### Anticipated purpose

Tier-3 will subject the certified system to adversarial inputs, boundary conditions,
and failure-mode scenarios that are not covered by the standard test suite. It verifies
that the system fails gracefully and that safety invariants hold under stress.

### Anticipated scope

- Malformed inputs at all system boundaries
- Artifact corruption and missing-dependency scenarios
- Hard-halt invariant stress tests (confirm forbidden components cannot be activated)
- Performance boundary checks (within defined tolerances)

### Trigger condition (anticipated)

Tier-3 will require valid Tier-2 `CERTIFIED` for the same HEAD SHA.

### Halt gate (anticipated)

Same exit-code semantics. Tier-3 is the final gate before any production-class
deployment or external release action.

---

## Evidence Retention

Each IRB run produces two report files:

```
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-<N>__<git-sha-8>.md
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-<N>__<git-sha-8>.json
```

Reports are the authoritative record of what was checked, what evidence was collected,
and what outcome was reached. They are committed to the automated-builder repository
and must not be modified after the fact.

---

## Operator Responsibilities

1. **Trigger IRB explicitly** at defined phase milestones — it does not run automatically.
2. **Read the full report** before taking any downstream action, even on `CERTIFIED`.
3. **Investigate advisory failures** — they may indicate conditions that will become
   blocking in future tiers.
4. **Do not begin the next phase or tier** without explicit authorization from the
   report outcome and human review.
5. **Do not attempt to patch around** a `FAILED` outcome by modifying the runner or
   spec. Remediate the target repository and re-run.

---

## Relationship to Build Reports

IRB certification reports (`outputs/reviews/`) are distinct from build reports
(`docs/system/outputs/`). Build reports are narrative records of implementation work.
IRB reports are deterministic evidence records. They serve different purposes and must
not be conflated.
