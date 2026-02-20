# Builder v1 — Remaining Steps and Execution Ordering

**Date:** 2026-02-20
**Author:** Claude Code (Planner session)
**Status:** Analysis only. No files modified, no items inserted, no commits.
**Source:** Deep review of `docs/system/pending-items.md`, `docs/system/pending-items-archive.md`, `docs/system/pending.md`.

---

## Builder v1 Completion Gate Criteria (from P-004 / pending.md)

```
Gate-1  Planner → Builder → Verification lifecycle executes deterministically
        (no manual state repair required)

Gate-2  Issue lifecycle: Proposal → Approved → Implementation → Summary executes cleanly;
        commit grouping deterministic; approval transition removes proposal-only sections;
        no lifecycle blending

Gate-3  Inventory lifecycle: Proposal → Approved → execution → Stage-1 PASS → Stage-2 PASS
        without state ambiguity; Deferred Register functional

Gate-4  pending-items.md remains synchronized with approved artifacts
        without manual correction

Gate-5  run-create-project produces a fully compliant project
        validated by verification rules

Gate-6  No open governance-breaking Issues remain in automated-builder
```

---

## Section 1 — Foundation Already Completed

These items are archived and do not need to be revisited.

| Item | Summary | Gates Satisfied |
|---|---|---|
| P-001 ✅ | Proposal/Approval commit semantics clarification | Gate-2 |
| P-002 ✅ | issue-resolution.md loop semantics corrected | Gate-2 |
| P-012 (v1) ✅ | Automated builder completion definition and guardrails | All |
| P-015 (v1) ✅ | Verification template — Pending item context added | Gate-2, Gate-3 |
| P-016 (v1) ✅ | Enforce output artifact after every Claude iteration | Gate-6 |
| P-016 (v2) ✅ | Stabilize run-create bootstrap validation | Gate-5 |
| P-037 (v1) ✅ | Mac Mini availability date determined | — |
| P-061 (v1) ✅ | Bible study platform survey (superseded by P-031) | — |
| P-083 ✅ | Planner output root relocated to parent projects directory | Gate-1 |
| P-084 ✅ | run-create-project — 11-issue inventory executed and verified | Gate-5 |
| P-085 ✅ | Builder project templates defined and verified | Gate-5 |
| P-098 ✅ | Harden Issue-Resolution Constitution (8 hardening rules) | Gate-2, Gate-3, Gate-6 |

**Observation — ID Reuse:** The gap-fill allocation rule has produced three cases where a previously archived P-### ID was re-assigned to a new item: P-012 (v1 archived → v2 active), P-016 (v1 archived → v2 archived), P-037 (v1 archived → v2 active). This is a live integrity risk documented in the constitutional review output (`2026-02-20__01__system__pending-governance-constitutional-review.md`).

---

## Section 2 — All Remaining Builder v1 Items

Items are drawn exclusively from the active `pending-items.md`. Deferred-to-other-projects items and non-v1 items are excluded and listed separately in Section 4.

### Tier 0 — Meta: Sequencing Authority

| Item | Summary | Gates | Status |
|---|---|---|---|
| P-079 | Identify critical Pending items and define execution sequencing (Inventory) | All | Unblocked |

P-079 is an Inventory item whose output IS the formal critical path artifact. This analysis session (along with this output artifact) constitutes the pre-work that P-079 requires. P-079 should still execute formally through the proposal/approval/verification lifecycle to produce the authoritative sequencing record.

---

### Tier 1 — Governance Rules Foundation

These items define the governance rules that all subsequent work must follow. Executing them first ensures later items are implemented under a stable, formalized framework.

| Item | Summary | Gates | Status |
|---|---|---|---|
| P-061 (v2) | Lifecycle Changelog Rules — define changelog table schema, entry triggers, counter increment rules, immutability | Gate-2 | Unblocked |
| P-101 | Formalize Pending-Items Governance Contract — canonical rules for pending-items lifecycle, archive sync, template, immutability | Gate-4, Gate-6 | Unblocked |
| P-062 | Define formal supersession rule for Pending items — when/how items are superseded, cross-reference format, prohibition of silent deletion | Gate-6 | Unblocked |

**Why first:** P-061 defines how proposal change logs work. Every proposal created in subsequent tiers will immediately need change log entries — the schema must exist first. P-101 defines the pending-items governance rules that P-086 and P-087 (Tier 2) implement. P-062 defines supersession, which is needed before any backlog cleanup in Tier 3.

**Internal ordering within Tier 1:**
```
P-061 → P-101 → P-062
```
P-061 first because its changelog schema is immediately usable. P-101 second because its rules inform Tier 2. P-062 third because supersession rules are referenced but not blocking for the core Tier 2 items.

---

### Tier 2 — Core Lifecycle Governance

These items directly close Gate-2, Gate-3, and Gate-4. They fix specific gaps in the issue, inventory, and pending-items lifecycles. All are unblocked after Tier 1.

| Item | Summary | Gates | Notes |
|---|---|---|---|
| P-003 | Add proposal-artifact reference requirement to Approval template | Gate-2, Gate-6 | Small, targeted approval template fix |
| P-087 | Pending Items "Current Status" field — add Current Status block to pending items for session reorientation | Gate-4 | Must precede P-086 |
| P-086 | Update Issues approval template to enforce pending-items sync — approved revision must update corresponding P-### entry | Gate-4, Gate-6 | Depends on P-087 |
| P-088 | Parallel Issue Execution Grouping Rule — define deterministic output grouping when multiple Issues execute in one session | Gate-2, Gate-6 | Independent |
| P-091 | Formalize Proposal Update vs Approval-with-Changes Rule — define threshold between minor correction and structural update | Gate-2, Gate-6 | Independent |
| P-089 | Inventory Approval Must Declare Issue Sequence Status — require explicit declaration at approval time | Gate-3, Gate-6 | Independent |
| P-090 | Track Deferred Items Within Inventory — Deferred Register concept; append-only deferral record per Inventory P-### | Gate-3, Gate-6 | Should follow P-089 |

**Internal ordering within Tier 2:**
```
P-003
P-087 → P-086
P-088
P-091
P-089 → P-090
```

P-003 is first — it is small, adds a single reference field to the Approval template, and unblocks the approval template from being further modified in a partially-compliant state.

P-087 before P-086: the Current Status field must exist in pending items before the approval template can reference it in a sync requirement.

P-089 before P-090: declaring the sequence status at approval time (P-089) is the prerequisite condition that makes tracking deferrals against a declared sequence (P-090) meaningful.

P-088 and P-091 are independent and can be ordered freely or executed in close sequence.

---

### Tier 3 — Infrastructure and Documentation Cleanup

These items close specific gaps in path determinism, documentation consistency, and usability. All contribute to Gate-1, Gate-5, and Gate-6.

| Item | Summary | Gates | Status |
|---|---|---|---|
| P-096 | Define When Issue-Resolution Requires a New Session — codify session-boundary rules; when new session required vs in-session continuation allowed | Gate-1, Gate-6 | Unblocked |
| P-015 (v2) | Normalize run-* prompt/script locations — canonical filesystem locations for run-create-project, run-planner, run-builder | Gate-1, Gate-5 | Unblocked |
| P-013 | Scan system for documentation inconsistencies — audit repo and docs for inconsistencies or missing documentation | Gate-6 | Unblocked |
| P-037 (v2) | run-create-project interactive prompts for mandatory fields — prompt for slug/name/prefix when flags absent | Gate-5 | **Now unblocked** — P-016 v2 complete |

**Note on P-037 (v2):** This item was deferred pending P-016 completion. P-016 v2 ("Stabilize run-create bootstrap validation") was completed and archived 2026-02-18. P-037 (v2) is therefore now unblocked and should be promoted to active.

**Internal ordering within Tier 3:**
```
P-096
P-015 → (P-037 usable after P-015 paths are canonical)
P-013
P-037
```

P-096 first — session boundary rules affect how all remaining tiers are executed. Knowing when to start a new session before executing Tier 4 is operationally useful. P-015 before P-037 — canonical path definitions should exist before interactive prompt behavior references them. P-013 (documentation scan) is a sweep that should occur after the governance and infrastructure items have settled, so discovered inconsistencies reflect the corrected state.

---

### Tier 4 — Automation Expansion

| Item | Summary | Gates | Status |
|---|---|---|---|
| P-012 (v2) | Automated Mode Expansion — Stage-Level Execution; each of run-create, run-planner, run-builder can run fully automated; HALT-on-question behavior; non-interleaving guardrails | Gate-1 | Unblocked |

**Why last in the pre-gate sequence:** Automation should be added to a lifecycle that is already clean. Running Tier 1 and Tier 2 first ensures the lifecycle P-012 automates is fully correct before automation removes the human checkpoints that catch gaps. Automating a broken lifecycle embeds the breakage.

**Gate-1 interpretation note:** Gate-1 requires "lifecycle executes deterministically without manual state repair." P-012 (Automated Mode) expands this to eliminate human prompts between steps, which is the strongest form of Gate-1 compliance. If Gate-1 is interpreted as "no repair needed (but human interaction is fine)," P-012 could technically be post-v1. The dependency view in `pending.md` explicitly tags it `[V1-GATE-1]`, so it is treated as required.

---

### Tier 5 — Pre-Deploy Gate

| Item | Summary | Gates | Status |
|---|---|---|---|
| P-092 | Builder v1 Edge Case Evaluation — structured edge case test suite across: input normalization, path invariants, symlink behavior, template rendering, governance lifecycle, deferred validation boundary | All | Blocked until Tiers 1–4 complete |

P-092 is the formal gate that authorizes declaring Builder v1 deployable. It cannot execute meaningfully until all governance cleanup, infrastructure normalization, and automation expansion are in place. Any failures found by P-092 spawn formal Issue-### records, which must be resolved before v1 is declared.

---

### Tier 6 — Devotional Generator Alignment

These execute after P-092 PASS and constitute the final validation that Builder v1 works against a real downstream project.

| Item | Summary | Status |
|---|---|---|
| P-093 | Review Devotional Generator Plans for Builder v1 Alignment — audit PRD, roadmap, pending items for governance compatibility | Blocked until P-092 PASS |
| P-094 | Update Devotional Generator Plans for Builder v1 Governance — structural updates to Devotional plans | Blocked until P-093 complete |
| P-095 | Rebuild Devotional Generator Using Builder v1 — re-run bootstrap and build cycle; confirm zero invariant violations | Blocked until P-094 complete |

```
P-092 PASS → P-093 → P-094 → P-095
```

P-095 PASS is the operational proof that Builder v1 works end-to-end against a real project. This closes the loop on Gate-5 at the integration level and validates all six gate criteria in a live execution.

---

## Section 3 — Full Ordered Sequence (Consolidated)

```
═══════════════════════════════════════════════════════
FOUNDATION — COMPLETE
═══════════════════════════════════════════════════════
  P-084 ✅  run-create-project (11-issue inventory)
  P-085 ✅  Builder project templates
  P-083 ✅  Planner output root
  P-098 ✅  Constitution hardening (8 hardening rules)
  P-016 ✅  Stabilize run-create bootstrap validation

═══════════════════════════════════════════════════════
TIER 0 — META / SEQUENCING AUTHORITY
═══════════════════════════════════════════════════════
  P-079    Identify critical items + execution sequencing (Inventory)
           [this analysis + output artifact serves as pre-work;
            formal lifecycle still required]

═══════════════════════════════════════════════════════
TIER 1 — GOVERNANCE RULES FOUNDATION
═══════════════════════════════════════════════════════
  P-061    Lifecycle Changelog Rules
     ↓
  P-101    Formalize Pending-Items Governance Contract
     ↓
  P-062    Define formal supersession rule for Pending items

═══════════════════════════════════════════════════════
TIER 2 — CORE LIFECYCLE GOVERNANCE
═══════════════════════════════════════════════════════
  P-003    Add proposal-artifact reference to Approval template
  P-087    Pending Items "Current Status" field
     ↓
  P-086    Approval template enforce pending-items sync
  P-088    Parallel Issue Execution Grouping Rule
  P-091    Formalize Proposal Update vs Approval-with-Changes
  P-089    Inventory Approval must declare sequence status
     ↓
  P-090    Track Deferred Items Within Inventory

═══════════════════════════════════════════════════════
TIER 3 — INFRASTRUCTURE AND DOCUMENTATION CLEANUP
═══════════════════════════════════════════════════════
  P-096    Define when Issue-Resolution requires new session
  P-015    Normalize run-* prompt/script locations
     ↓
  P-037    run-create-project interactive prompts [NOW UNBLOCKED]
  P-013    Scan system for documentation inconsistencies

═══════════════════════════════════════════════════════
TIER 4 — AUTOMATION EXPANSION
═══════════════════════════════════════════════════════
  P-012    Automated Mode Expansion — Stage-Level Execution

═══════════════════════════════════════════════════════
TIER 5 — PRE-DEPLOY GATE
═══════════════════════════════════════════════════════
  P-092    Builder v1 Edge Case Evaluation
           → Any failures spawn Issue-### and must resolve before v1

═══════════════════════════════════════════════════════
TIER 6 — DEVOTIONAL GENERATOR ALIGNMENT
═══════════════════════════════════════════════════════
  P-093    Review Devotional Generator Plans for Builder v1 Alignment
     ↓
  P-094    Update Devotional Generator Plans for Builder v1 Governance
     ↓
  P-095    Rebuild Devotional Generator Using Builder v1
           → P-095 PASS = Builder v1 operational

═══════════════════════════════════════════════════════
POST-V1 (formally deferred)
═══════════════════════════════════════════════════════
  P-099    Restart Protocol for Interrupted Inventories
  P-100    Normalize Verification Field Names (Verdict → Verification)
  P-097    Automated Retry Logic for Inventory Verification
  P-004    Architecture review — next pass planning
```

**Total remaining items: 20**
- Tier 0: 1
- Tier 1: 3
- Tier 2: 7
- Tier 3: 4
- Tier 4: 1
- Tier 5: 1 (gate)
- Tier 6: 3

---

## Section 4 — Non-v1 Items (Excluded from Ordering)

These items are active in `pending-items.md` but are not on the Builder v1 critical path. They are either explicitly deferred, belong to other projects, or are post-v1 strategic work.

| Category | Items |
|---|---|
| Devotional Generator features (deferred until builder complete) | P-005, P-006, P-007, P-008, P-009, P-010, P-011, P-027, P-028, P-034, P-035, P-036, P-038, P-039, P-040, P-041, P-042 |
| ChMS / business strategy (deferred until ChMS activation) | P-018, P-019, P-020, P-021, P-022, P-025, P-029, P-030, P-031, P-032, P-033, P-043, P-044, P-045, P-046, P-047, P-048, P-049, P-050, P-051, P-052, P-053, P-054, P-055, P-056, P-057, P-058, P-059, P-064, P-065, P-067, P-068, P-069, P-070, P-071, P-072, P-073, P-074, P-075, P-076, P-080 |
| Research / evaluation (deferred until builder core complete) | P-017, P-026 |
| Builder v2 | P-014 |
| Backlog meta-analysis (useful but not v1-blocking) | P-023, P-024, P-060, P-063, P-066, P-077, P-078, P-081, P-082 |
| Post-v1 (formally deferred) | P-097, P-099, P-100 |
| Automation resilience (non-blocking per dependency view) | P-097 |

---

## Section 5 — Gate Satisfaction Map

Which tiers satisfy which gates:

| Gate | Satisfied By |
|---|---|
| Gate-1 (lifecycle deterministic, no repair) | P-096 (Tier 3), P-015 (Tier 3), P-012 (Tier 4), P-092 validation (Tier 5) |
| Gate-2 (issue lifecycle clean) | P-061 (Tier 1), P-003 (Tier 2), P-088 (Tier 2), P-091 (Tier 2), P-092 validation (Tier 5) |
| Gate-3 (inventory lifecycle clean, Deferred Register functional) | P-089 (Tier 2), P-090 (Tier 2), P-092 validation (Tier 5) |
| Gate-4 (pending-items synchronized without manual correction) | P-101 (Tier 1), P-087 (Tier 2), P-086 (Tier 2) |
| Gate-5 (run-create-project produces compliant project) | P-085 ✅ (done), P-015 (Tier 3), P-037 (Tier 3), P-092 validation (Tier 5) |
| Gate-6 (no open governance-breaking issues) | P-062 (Tier 1), P-101 (Tier 1), P-003 (Tier 2), P-086 (Tier 2), P-088 (Tier 2), P-089 (Tier 2), P-090 (Tier 2), P-091 (Tier 2), P-013 (Tier 3), P-092 validation (Tier 5) |

All six gates must pass before Builder v1 is declared operational.

---

## Section 6 — Key Observations

**1. P-037 (v2) is silently unblocked.**
Its stated dependency was "P-016 is complete." P-016 v2 was archived 2026-02-18. No one updated P-037's status. It should be promoted to active immediately.

**2. P-079 is being done informally right now.**
This analysis session constitutes the work P-079 describes. The formal P-079 lifecycle (proposal → approval → verification) still needs to execute to produce an authoritative, governance-compliant artifact. The recommendation is to execute P-079 first in Tier 0 so the sequence produced here can be formally approved.

**3. P-101 and P-062 partially overlap.**
P-101 defines the full governance contract for pending-items (which includes supersession rules). P-062 defines the supersession rule specifically. If P-101 absorbs P-062's scope, P-062 can be superseded by P-101 before or during execution. This should be decided at P-101 proposal time.

**4. Tier 2 is the highest-density governance cleanup tier.**
Seven items. All unblocked. This tier has the most direct impact on Gate-2, Gate-3, and Gate-4. It should be treated as a focused governance sprint — not interleaved with Tier 3 or Tier 4 work.

**5. P-092 (Edge Case Evaluation) is a hard gate, not a soft milestone.**
It produces formal pass/fail evidence. Any failures found must spawn Issue-### records and be resolved. There is no partial credit. Builder v1 cannot be declared operational until P-092 produces a PASS artifact with no unresolved blocking failures.

**6. Three ID reuses exist in the active system.**
P-012, P-016, and P-037 each have an archived version and an active version sharing the same ID. This is a known risk from the gap-fill allocation rule. It does not block v1 but creates confusion in cross-referencing and should be addressed via P-101 (allocation rule fix).

---

*End of Builder v1 remaining steps and ordering analysis.*
