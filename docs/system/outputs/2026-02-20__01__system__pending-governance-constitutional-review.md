# Constitutional Review — Pending-Items Governance Reconciliation

**Date:** 2026-02-20
**Author:** Claude Code (Planner session)
**Status:** Analysis only. No files modified, no items inserted, no commits.
**Constraints:** P-### identifier system is immutable and unchanged. All constitutional CMS-### references interpreted as P-### for analysis only.

---

## Purpose

Perform a deep structural reconciliation analysis between:

- **A)** The live P-### operational model.
- **B)** The proposed constitutional rule set (interpreting CMS-### as P-###).
- **C)** The current state of `docs/system/pending-items.md`.

Produce a gap analysis, governance debt assessment, a fully drafted proposed pending item, and a timing recommendation.

---

## Source Documents Reviewed

| Document | Path |
|---|---|
| Live active backlog | `docs/system/pending-items.md` |
| Live archive | `docs/system/pending-items-archive.md` |
| Issue resolution entry | `docs/system/issue-resolution.md` |
| Issue resolution rules | `docs/system/issue-resolution-rules.md` |
| Dependency view | `docs/system/pending.md` |
| Constitutional rule set | Provided in session prompt (proposed, not active) |

---

## Part 1 — Structural Divergences

Below, "Constitutional" refers to the proposed rule set. "Live" refers to the operational P-### system as of this analysis.

---

### Divergence 1 — File Architecture

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Structure | Single file: `## PENDING` + `## COMPLETE` | Two-file split: `pending-items.md` (active) + `pending-items-archive.md` (completed) |
| Completion location | `## COMPLETE` block in same file | Entire block moved to archive file |
| Completion annotation | `<!-- STATUS: COMPLETE -->` + `Completed Date:` + `Verification Artifact:` + all ACs → `[x]` | Condensed summary block + `- Verification:` reference line in archive |

**Classification:** Intentional architectural simplification.

The live system split the file to prevent the active view from becoming unmanageable as completed items accumulate. This is a deliberate design decision, not drift. The constitutional model's single-file approach would become unwieldy at 100+ items. The live two-file split is the superior operational model and should be retained as canonical.

**Entropy risk:** Low — the split is consistently applied. However, the archive format is less rigorous than the constitutional model's completion block (no per-criterion `[x]` marks, no formal `Verification Artifact:` field enforcement).

---

### Divergence 2 — Rules Location

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Primary rules location | Defined in the constitutional document (external) | Embedded as `## Rules` header block in `pending-items.md` |
| Lifecycle integration | Issue resolution governed separately (cross-referenced) | Lifecycle rules live in `issue-resolution-rules.md`; `pending-items.md` references it |
| Dependency view | Not mentioned | `pending.md` — external derived view with regeneration instructions |

**Classification:** Intentional separation with some duplication risk.

The live model co-locates governance rules with the file they govern, which improves discoverability. The dependency view (`pending.md`) is an intentional addition not contemplated by the constitutional model — it provides a derived, readable index without embedding logic in the source file. This is additive and sound.

**Entropy risk:** Medium — `pending-items.md` rules block and `issue-resolution-rules.md` cover overlapping ground (completion authority, issue lifecycle integration). No single authoritative source exists for pending-items governance rules specifically.

---

### Divergence 3 — Template Enforcement (Major Governance Debt)

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Required fields | Objective, Scope (In/Out), Acceptance Criteria, Dependencies, Notes | Undefined — informal evolution |
| AC format | All as `- [ ] criterion` checkboxes, split atomic | Mixed: older items use plain summary text; newer items use checkbox format |
| Scope format | Explicit In / Out split | Inconsistent — some have explicit In/Out, some prose, many have none |
| Enforcement | System must reject insertions missing required fields | No enforcement rule exists |

**Classification:** Entropy drift / generational inconsistency — significant governance debt.

The live file shows three observable generations of format quality:

- **Generation 1 (P-003 to ~P-082):** Largely summary-only, no Objective, no Scope, no AC.
- **Generation 2 (P-083 to ~P-095):** Improving — Objective/Scope/AC introduced for some items.
- **Generation 3 (P-096 to P-101):** Full canonical structure emerging, including checkbox ACs.

The constitutional model would require normalizing all ~100 active items — an unbounded retroactive scope. This should be explicitly rejected as a non-goal for the immediate reconciliation work.

**Entropy risk:** High. Items without Acceptance Criteria cannot be deterministically verified for completion. Items without formal Scope cannot be audited for scope creep. This is an active governance liability for any item that enters the execution lifecycle.

---

### Divergence 4 — ID Allocation Rule

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Gap-filling | No — always uses max+1 | Yes — fill lowest missing P-### first; if no gaps, max+1 |
| External ID handling | Ignore external format; preserve optionally in Notes | Not formally defined |
| Collision verification | Required | Not explicitly required (single-user assumption) |

**Classification:** Behavioral divergence with a latent integrity risk.

The live system's gap-filling rule (`lowest missing first`) was designed to prevent sparse numbering after archival. However, the live scan appears to be scoped to `pending-items.md` only — not the archive file. An archived item (e.g., P-037 appears in the archive) looks like a "gap" to a pending-only scan. If the scanner identifies P-037 as missing and re-assigns it, that violates the no-ID-reuse invariant.

The constitutional model's `max+1` approach eliminates this risk entirely.

**Entropy risk:** Medium. In the current single-operator environment the risk is low in practice. As automation expands, this becomes a credible integrity failure condition.

---

### Divergence 5 — Deferred Annotation Style

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Deferred marker | `<!-- STATUS: DEFERRED -->` under heading | `- Deferred until: <condition>` in body |
| Nested variant | Not defined | `  - Deferred until:` inside `- Notes:` block (Rule 8) |
| Deferred item location | Remains in PENDING | Remains in `## Pending Items` |
| Reporting exclusion | Explicit | No explicit rule stated |

**Classification:** Minor stylistic divergence, same intent — but the live model has an internal inconsistency.

Both systems agree: deferred items stay in the active section. The annotation style differs. The live system's `- Deferred until:` notation is more readable in plain text. However, Rule 8 in `pending-items.md` acknowledges a dual-location variant ("if the item has a `- Notes:` block, use it inside"). This creates parsing ambiguity: deferred status can appear at two different locations within the same item.

**Entropy risk:** Low for human operations, medium for any future automated tooling. The dual-location rule will cause false negatives in a deferred-status scan.

---

### Divergence 6 — Post-Insertion Immutability Rule

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Immutable fields | Objective, Scope, Acceptance Criteria | Not defined |
| Amendment mechanism | Create new P-### referencing original | Not defined |
| History protection | Explicit — no rewriting | No formal rule |

**Classification:** Governance gap.

The live system has no formal post-insertion immutability rule for pending items. The constitutional model's immutability rule prevents retroactive scope rewriting and preserves audit integrity. The live system's `issue-resolution-rules.md` enforces immutability on approved Issue-### artifacts, but this protection does not extend to P-### items in `pending-items.md`. A P-### item's Objective or Scope can be silently edited without producing any governance event.

**Entropy risk:** High. Without immutability protection, pending items can drift silently from their original intent. This undermines verification integrity — the ACs at completion time may not match the ACs at insertion time.

---

### Divergence 7 — Acceptance Criteria Validation at Completion

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Completion gate | Every AC must be validated in verification artifact | Verification artifact must exist with "Verdict: PASS" |
| Per-criterion validation | Required — missing validation → reject completion | Not explicitly required at pending-items level |
| AC format at completion | All → `[x]` | No formal checkbox update rule in pending-items |

**Classification:** Governance gap — moderate severity.

The constitutional model requires the verification artifact to explicitly validate each Acceptance Criterion. The live system requires "Verdict: PASS" in a verification artifact but does not mandate per-criterion validation at the `pending-items.md` governance level. In practice, verification templates in `issue-resolution-templates.md` likely enforce per-criterion checks, but this is governed there — not here. If templates change, this protection becomes invisible.

**Entropy risk:** Medium. For Generation 1 items without formal ACs, this is moot. For Generation 3 items with explicit checkbox ACs, the gap is real and growing.

---

### Divergence 8 — Issue-Loop Integration Rule

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Rule location | Embedded in pending-items governance | In `issue-resolution-rules.md` |
| Completion prerequisite | All related Issue-### resolved before P-### completes | Governed by issue-resolution lifecycle separately |
| Cross-reference protocol | P-### may reference Issue-### in Notes | Issue-### identifiers prohibited in pending-items.md body except in specific allowed forms |

**Classification:** Intentional separation with correct integration.

The live system correctly keeps Issue-loop governance in `issue-resolution-rules.md` and pending-items governance in `pending-items.md`, with cross-references only where needed. The constitutional model's co-location of these rules would create duplication. The live system's approach is superior and should be formalized as the canonical pattern.

**Entropy risk:** Low operationally. The separation is clean and consistently applied.

---

### Divergence 9 — Input Normalization and Missing Field Protocol

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Normalization rules | Extensive (field extraction, AC conversion, scope splitting) | None defined |
| Missing field protocol | Insert with placeholders; query user | Not defined |
| Multi-item batch behavior | Insert all first; then ask about missing fields | Not defined |

**Classification:** Governance gap.

The live system has no formal protocol for handling poorly-structured insertions. The current model relies on the inserting agent to structure items correctly at insertion time. As the backlog grows and automation expands, unstructured insertions will accumulate. This is already visible in Generation 1 items.

**Entropy risk:** Medium. Not blocking today; increasingly problematic as automation scope expands.

---

### Divergence 10 — Reporting / Next-5 Algorithm

| Dimension | Constitutional Model | Live Model |
|---|---|---|
| Output rules | Defined in pending-items governance | Externalized to `pending.md` |
| Next-5 algorithm | Selection criteria specified inline | `pending.md` has separate regeneration instructions |
| Deferred exclusion | Explicit | Implied by active-only view; not formally stated |

**Classification:** Intentional externalization — sound design.

The live system's external `pending.md` dependency view is functionally equivalent to the constitutional model's reporting rules, but operationally cleaner. It separates the derived view from the source of truth. This is superior and should be retained and referenced from the governance contract.

**Entropy risk:** Low.

---

## Part 2 — Governance Debt Assessment

### Pending Surface Summary

| Category | Count (approx) | Debt Level |
|---|---|---|
| Active items in `pending-items.md` | ~95 (P-003 to P-101, accounting for gaps) | — |
| Items without formal Objective | ~65 (Generation 1–2) | High |
| Items without Acceptance Criteria | ~65 (Generation 1–2) | High |
| Items with ambiguous deferred annotation (dual-location) | ~10–15 | Medium |
| Items at risk of ID gap-archive collision | Depends on archive content | Medium |
| Items lacking post-insertion immutability protection | All 95 | Medium |
| Items with checkbox-format ACs (Generation 3) | ~10 | Low (governed) |

### Generation Breakdown

| Generation | Range | Format Quality |
|---|---|---|
| Gen 1 | P-003 to ~P-082 | Summary-only. No Objective, no formal Scope, no Acceptance Criteria. |
| Gen 2 | P-083 to ~P-095 | Mixed. Some items have full structure; others remain summary-only. |
| Gen 3 | P-096 to P-101 | Full canonical structure. Objective, Scope In/Out, checkbox ACs, Dependencies. |

### P-101 Relationship

P-101 — *Formalize Pending-Items Governance Contract* — was captured 2026-02-19. Its scope directly overlaps this analysis:

> "Define canonical operational rules, consolidate into `pending-items-rules.md.tmpl`, define required metadata fields, deferral annotation, duplicate/overlap detection, merge/elimination workflow, archive sync, scope evaluation, anti-entropy safeguards."

P-101's scope is largely correct but was captured without the benefit of a constitutional gap analysis. It defines *what* rules are needed without a formal basis for determining *which constitutional provisions to adopt, reject, or adapt*. This analysis provides that missing foundation.

**Relationship decision required:** The proposed item below should either absorb P-101 or explicitly coordinate with it before either executes.

---

## Part 3 — Proposed Pending Item

**NOTE: This is a fully drafted item for human review. It has NOT been inserted into `pending-items.md`.**

---

### DRAFT — P-NNN — Reconcile Pending-Items Governance Model

**Source:** Constitutional review analysis — 2026-02-20
**Captured:** [DATE OF INSERTION]
**Project:** Automated-builder
**Classification:** Regular Issue

---

**Objective:**

Reconcile the structural and procedural gaps between the live P-### operational model and the proposed constitutional rule set. Produce a formally approved governance contract that:

1. Locks in the two-file architecture as canonical.
2. Defines canonical template requirements for new insertions going forward.
3. Fills identified governance gaps (immutability, deferred annotation, ID allocation, completion validation) without retroactive burden on existing items.
4. Coordinates with or absorbs P-101.

---

**Scope (In):**

- Formally document the two-file architecture (`pending-items.md` + `pending-items-archive.md`) as the authoritative canonical model — explicitly rejecting the constitutional single-file `## COMPLETE` approach.
- Define canonical template for **new** pending item insertions only, with required fields: Source, Captured, Project, Classification, Objective, Scope (In / Out), Acceptance Criteria (checkbox format), Dependencies, Notes.
- Define formal post-insertion immutability rule: Objective, Scope, and Acceptance Criteria are locked after insertion; amendments require a new P-### with cross-reference.
- Define canonical deferred annotation: standardize on `- Deferred until: <condition>` at the item body level (not nested inside Notes blocks) — eliminating the dual-location ambiguity in current Rule 8.
- Define the archive synchronization contract: move-to-archive prerequisites (Verification PASS artifact required, "Verdict: PASS" string required), required fields in archive entry, prohibited silent deletion.
- Fix the ID allocation gap-archive collision risk: the gap-filling scan MUST include the archive file (or adopt unconditional max+1 to eliminate the risk entirely — one approach chosen and documented).
- Define the Issue-### integration boundary explicitly within pending-items governance: P-### items may reference Issue-### in Notes as descriptive references only; Issue-### identifiers must never appear as standalone entries or as P-### body items.
- Consolidate the governance contract into a single authoritative rules document at `docs/system/pending-items-rules.md`.
- Resolve P-101: either absorb P-101 into this item (if timing allows), or explicitly coordinate scope so the two items do not produce contradictory governance outputs. One of the following must happen before either executes: (a) P-101 superseded by this item, or (b) scopes divided with no overlap.
- Update the `## Rules` block in `pending-items.md` to reference `pending-items-rules.md` as the authoritative source.

---

**Scope (Out):**

- Retroactive normalization of existing items (P-003 through ~P-095) to canonical template structure — explicitly **not in scope**; treat as a future separate item if operationally justified.
- Changes to the Issue-### execution lifecycle — governed exclusively by `issue-resolution-rules.md` and its companion templates.
- Adopting the constitutional `<!-- STATUS: DEFERRED -->` HTML comment annotation style — the live `- Deferred until:` notation is preferred and is being standardized.
- Adopting the constitutional `## COMPLETE` section within `pending-items.md` — two-file split is retained.
- Adopting or importing the CMS-### identifier system.
- Implementing enforcement tooling or automated validation scripts.
- Input normalization AI behavior (auto-field-inference from unstructured insertions) — governance documentation only; no AI behavior specification.
- Changes to the `pending.md` dependency view structure.

---

**Acceptance Criteria:**

- [ ] Two-file architecture (`pending-items.md` + `pending-items-archive.md`) is formally documented as canonical in `pending-items-rules.md`.
- [ ] Canonical template for new insertions is defined with all required fields specified.
- [ ] Post-insertion immutability rule is written and explicitly listed in `pending-items-rules.md`.
- [ ] Deferred annotation format is standardized at body level (`- Deferred until:`); dual-location variant is removed.
- [ ] Archive synchronization contract defines move-to-archive prerequisites and required archive entry fields.
- [ ] ID allocation rule is unambiguous: one approach (archive-aware gap-fill OR unconditional max+1) is chosen, documented, and applied to the Rules block in `pending-items.md`.
- [ ] Issue-### integration boundary is explicitly stated in `pending-items-rules.md`.
- [ ] `pending-items-rules.md` exists as the single authoritative governance document for pending-items operations.
- [ ] Relationship with P-101 is explicitly resolved: absorbed, coordinated, or superseded — with formal cross-reference.
- [ ] Rules block in `pending-items.md` references `pending-items-rules.md` as the authoritative source.
- [ ] No operational ambiguity remains about how to: insert, defer, complete, or archive a P-### item.

---

**Dependencies:**

- P-101 — Formalize Pending-Items Governance Contract (must coordinate or absorb before either executes)
- P-098 — Harden Issue-Resolution Constitution (must not conflict; read Issue-### integration rules from P-098 output before finalizing the Issue boundary rule in this item)

---

**Risk Analysis:**

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Retroactive normalization scope creep | Medium | High | Explicit Out-of-Scope declaration; no AC references existing items |
| P-101 parallel execution producing conflicting output | High if not coordinated | High | Coordinate before either item executes; absorb or supersede P-101 explicitly |
| ID gap-archive collision during analysis | Low (single-user) | High (ID integrity violation) | Fix allocation rule as part of this item |
| Immutability rule back-applied to informally-modified items | Low | Medium | Immutability applies prospectively only — no retroactive audit required |
| Conflict between pending-items governance and issue-resolution-rules.md completion authority | Medium | Medium | Review P-098 output and align language before finalizing |

---

**Non-Goals:**

- This item does NOT normalize existing pending items.
- This item does NOT implement automated tooling for pending-item validation.
- This item does NOT import the `<!-- STATUS: DEFERRED -->` annotation style.
- This item does NOT introduce a `## COMPLETE` section in `pending-items.md`.
- This item does NOT replace `issue-resolution-rules.md` with pending-items governance.
- This item does NOT adopt the CMS-### identifier system.
- This item does NOT adopt the constitutional input-normalization AI behavior model.

---

## Part 4 — Timing Recommendation

**Recommendation: Stabilize First**

Execute AFTER P-098 (Harden Issue-Resolution Constitution) reaches Verification PASS, but BEFORE Builder v1 is declared complete.

**Rationale:**

**1. P-101 pre-exists with overlapping scope.**
Inserting a new item without first resolving P-101 creates immediate governance debt. The correct sequence: (a) this analysis informs P-101's scope refinement, (b) P-101 executes under the existing governance model with updated scope, or (c) this item supersedes P-101 with human approval. Do not allow both to execute independently.

**2. Active governance hardening (P-098) is in flight.**
Issue-### integration rules are being formalized now. Defining the Issue-boundary rule in pending-items governance before P-098 completes risks producing rules that immediately need revision.

**3. Builder v1 gate includes "no open governance-breaking Issues."**
Pending-items governance gaps are not governance-breaking in the failure-mode sense (the system continues to function), but they are gaps that should be closed before declaring v1 complete. This positions the work as pre-v1-gate but not urgently blocking.

**4. The constitutional model over-specifies in ways that exceed current operational need.**
The full constitutional rule set would require retroactive normalization of ~65 items — not justified by current operational risk. The "Stabilize First" approach preserves execution velocity while closing the real gaps.

| Timing Option | Verdict | Reason |
|---|---|---|
| Immediate | Not recommended | P-098 not complete; P-101 unresolved; risk of governance contradiction |
| Stabilize first (post P-098) | **Recommended** | Closes real gaps; avoids conflict with active lifecycle work |
| Post-v1 | Too late | Builder v1 gate requires "no open governance-breaking issues"; gaps should be formally closed first |
| Conditional | N/A | No ambiguous conditions; timing is deterministic |

---

## Part 5 — Reconciliation Summary Table

| Finding | Classification | Recommended Action |
|---|---|---|
| Two-file architecture | Intentional simplification | Retain and formalize as canonical |
| Rules embedded in pending-items.md | Sound | Retain; reference external rules doc |
| Template heterogeneity (Gen 1 items) | Entropy drift | Forward-only template enforcement; no retroactive fix |
| ID gap-archive collision risk | Integrity gap | Fix in allocation rule |
| Deferred annotation dual-location (Rule 8) | Minor entropy | Standardize on body-level only |
| Missing immutability rule | Governance gap | Add prospective rule |
| Missing per-criterion AC validation at completion | Governance gap | Add to completion contract |
| Missing input normalization protocol | Governance gap | Document basic protocol; defer AI-behavior specification |
| P-101 parallel scope risk | Active risk | Coordinate or absorb before execution |
| Dependency view (`pending.md`) | Sound addition | Retain; reference from governance contract |
| Constitutional single-file `## COMPLETE` model | Rejected | Two-file split is superior |
| Constitutional `<!-- STATUS: DEFERRED -->` | Rejected | Live `- Deferred until:` retained |
| Constitutional input normalization AI behavior | Deferred | Post-v1 consideration only |
| Issue-loop separation (no co-location) | Intentional | Retain; formalize boundary |

---

## Appendix — Constitutional Provisions Disposition

| Constitutional Rule | Status | Notes |
|---|---|---|
| §1 — System separation of concerns | Adopted (live model matches) | P-### vs Issue-### separation is correctly implemented |
| §2 — Core invariants (insert-only, no renumber, no delete) | Adopted | Live rules 1, 5 match; archive model satisfies "no delete" |
| §3 — ID allocation (max+1) | Partially adopted — gap-fill instead | Gap-fill has archive collision risk; needs fix |
| §4 — Insertion protocol (canonical template) | Not adopted for existing items | Adopted prospectively for Gen 3 items only |
| §5 — Input normalization | Not adopted | Deferred; no AI normalization behavior defined |
| §6 — Missing field follow-up rules | Not adopted | Deferred |
| §7 — Status rules (deferred, completed) | Partially adopted | Deferred annotation exists; completion uses archive instead of in-file block |
| §8 — Verification artifact requirements | Adopted (via issue-resolution-rules.md) | Governed there; cross-referenced |
| §9 — Issue loop integration rule | Adopted (separation model) | Issue-### boundary exists; needs formal documentation |
| §10 — Reporting rules | Adopted (via pending.md) | External view superior to inline rules |
| §11 — Immutability rule | Not adopted | Gap — must be added prospectively |
| §12 — Integrity failure conditions | Partially adopted | Some conditions covered; immutability and gap-collision conditions missing |

---

*End of constitutional review output.*
