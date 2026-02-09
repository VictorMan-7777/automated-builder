# Fix B Proposal — Pending Approval

**Date:** 2026-02-09
**Status:** Pending approval
**Source:** Architecture Review Pass 1 (`2026-02-09__01__system__architecture-review-pass-1.md`), Finding 4
**Scope:** Single-file documentation fix

---

## Problem

Two documents define the scoping rule for the sequence number (`NN`) in output filenames. They contradict each other.

**Document A — `docs/system/run-planner.md` (lines 361-371):**

> "The sequence number (`NN`) is **monotonic across the repository**, not scoped to a single date."
>
> "Scan all existing files in `docs/system/outputs/` and use the next available number, regardless of date."

Under this rule, if the highest `NN` across all files is `11` (from any date), the next output on any date must use `12`.

**Document B — `docs/system/outputs/README.md` (lines 147-150):**

> "Starts at 01 each day"
>
> "Increments for each new output on same day"

Under this rule, `NN` resets to `01` on each new date and increments only within that date.

These rules are mutually exclusive. A filename cannot comply with both simultaneously when a new date begins.

---

## Which Rule Should Win

**The per-day rule (`outputs/README.md`) should be authoritative.** Three reasons:

1. **Existing practice.** All 11+ output files in the repository follow the per-day convention. On 2026-02-07, files restart at `01` despite files from 2026-02-05 and 2026-02-06 existing with higher numbers. The convention is established and unbroken.

2. **Canonical location.** `docs/system/outputs/README.md` is the dedicated document for output naming rules. It is referenced by `access.md`, `initial-prompt.md`, the checkpoint taxonomy, and both invocation prompts as the authoritative source for output conventions. `docs/system/run-planner.md` is a planner-specific operational guide, not the naming authority.

3. **Fix A alignment.** The System Iterator definition just committed (Fix A, `b677369`) defines the algorithm as: "For today's date, find the highest existing `NN`... If no files exist for today's date, `NN` = `01`." This is the per-day rule. The monotonic-across-repo rule in `run-planner.md` now contradicts both `outputs/README.md` and the iterator definition.

---

## Affected Files

**Primary change:**
- `docs/system/run-planner.md` — Remove or replace the "Output Immutability" section (lines 355-374) that states the monotonic-across-repo rule.

**No changes required to:**
- `docs/system/outputs/README.md` — Already states the correct rule. Already contains the System Iterator definition (Fix A).
- All other documents — No other document references or restates the monotonic-across-repo rule.

---

## Rule-Level Change

In `docs/system/run-planner.md`, the "Output Immutability" section (lines 355-374) contains three claims:

1. *"Planner outputs are append-only artifacts."* — **Keep.** This is correct and not contradicted elsewhere.
2. *"A planner iteration MUST NOT overwrite an existing output file."* — **Keep.** This is correct and aligns with `access.md` ("modifying or overwriting existing output files" is prohibited).
3. *"The sequence number (NN) is monotonic across the repository, not scoped to a single date."* and *"Scan all existing files in docs/system/outputs/ and use the next available number, regardless of date."* — **Remove.** Replace with a reference to the authoritative naming rules in `docs/system/outputs/README.md`, specifically the System Iterator subsection.

The section titled "Determining the Next Sequence Number" (lines 369-371) should be replaced with a pointer: the algorithm is defined in `outputs/README.md` under "System Iterator" and should not be restated here.

---

## Acceptance Criteria

1. The monotonic-across-repo rule no longer appears in any document.
2. `docs/system/run-planner.md` defers to `docs/system/outputs/README.md` for sequence number determination.
3. The append-only / no-overwrite rules are preserved.
4. All existing output files comply with the surviving per-day rule (they already do).
5. No contradictions exist between `run-planner.md`, `outputs/README.md`, and the System Iterator definition.

---

## Proposed Commit Message

```
docs(system): resolve NN sequence-number contradiction in run-planner
```

Single-purpose commit. One file modified (`docs/system/run-planner.md`).
