# Pending Namespace

`pending` is the global namespace for P-### tracking and dependency planning.

Authoritative files:
- Active pending items (canonical): [docs/system/pending-items.md](pending-items.md)
- Archived pending items: [docs/system/pending-items-archive.md](pending-items-archive.md)

---

## Governance Pointer

Pending-item workflow and completion/verification semantics are governed by:
- [docs/system/issue-resolution.md](issue-resolution.md)
- [docs/system/issue-resolution-rules.md](issue-resolution-rules.md)
- [docs/system/issue-resolution-templates.md](issue-resolution-templates.md)

---

## Dependency Generator (Manual / On-Demand)

Purpose: produce a dependency view to help choose next work from active pending items.

Procedure:
1. Open `docs/system/pending-items.md` and read active P-### entries.
2. Extract prerequisite and ordering relationships from the active item summaries/notes.
3. Regenerate the dependency view in this file under `## Dependency View`.
4. Save this file only when manually refreshed; no automatic update is required.

Note: The dependency view is derived data and is intentionally updated on-demand (not dynamically).

---

## Dependency View

Last refreshed: 2026-02-19

### Legend

```
A -> B        A must be completed before B can begin meaningfully
(cluster)     Umbrella item; all members must clear before downstream
[D]           Deferred until <condition>
[DONE]        Completed and archived
[V1-GATE-N]  Directly satisfies Builder v1 Completion Gate criterion N
```

### Builder v1 Completion Gate Criteria (from P-004)

```
Gate-1  Planner -> Builder -> Verification lifecycle executes deterministically (no manual state repair)
Gate-2  Issue lifecycle: Proposal -> Approved -> Implementation -> Summary clean;
          commit grouping deterministic; approval transition removes proposal-only sections;
          no lifecycle blending
Gate-3  Inventory lifecycle: Proposal -> Approved -> execution -> Stage-1 PASS -> Stage-2 PASS
          without state ambiguity; Deferred Register functional
Gate-4  pending-items.md remains synchronized with approved artifacts without manual correction
Gate-5  run-create-project produces a fully compliant project validated by verification rules
Gate-6  No open governance-breaking Issues remain in automated-builder
```

---

### Declared dependencies (explicit in pending-items.md)

```
P-098 [DONE] -> P-099
P-098 [DONE] -> P-100
```

---

### Core builder readiness chain

```
P-012 (completion criteria) [DONE]
  +
P-083 (Planner output root) [DONE]
  |
  v
P-084 (run-create-project spec + 11-issue inventory) [DONE]
  |
  v
P-085 (templates as source-of-truth) [DONE]
  |
  v
P-098 (Constitution hardening) [DONE]
  |
  +-----------> P-099 (restart protocol)      [V1-GATE-3]
  +-----------> P-100 (normalize Verification field names)  [V1-GATE-1,6]
```

---

### Governance cleanup cluster (all unblocked; no declared deps)

These items directly close gaps in Gate-2, Gate-4, Gate-6:

```
P-003  Add proposal-artifact ref to Approval template    [V1-GATE-2,6]
P-086  Approval template must enforce pending-items sync  [V1-GATE-4,6]
P-087  Pending Items "Current Status" field               [V1-GATE-4]
P-088  Parallel Issue Execution Grouping Rule             [V1-GATE-2,6]
P-089  Inventory Approval must declare sequence status    [V1-GATE-3,6]
P-090  Track Deferred Items within Inventory              [V1-GATE-3,6]
P-091  Formalize Proposal Update vs Approval-with-Changes [V1-GATE-2,6]
P-096  Define when Issue-Resolution requires new session  [V1-GATE-1,6]
```

---

### Infrastructure / path normalization (unblocked)

```
P-015  Normalize run-* prompt/script locations            [V1-GATE-1]
P-013  Scan system for documentation inconsistencies      [V1-GATE-6]
```

---

### Automated mode expansion (unblocked; feeds Gate-1)

```
P-012 [active]  Automated Mode Expansion — Stage-Level Execution  [V1-GATE-1]
```

---

### Pre-deploy gate (depends on governance cluster above)

```
(governance cleanup cluster) -> P-092 (Builder v1 edge case evaluation, Pre-Deploy Gate)
```

---

### Devotional generator alignment (sequenced after P-092)

```
P-092 -> P-093 (review Devotional plans for Builder v1 alignment)
P-093 -> P-094 (update Devotional plans for Builder v1 governance)
P-094 -> P-095 (rebuild Devotional Generator using Builder v1)
```

---

### Automation resilience (post-P-098; non-blocking for V1 deploy gate)

```
P-098 [DONE] -> P-097 (automated retry logic for inventory verification)
```

---

### Devotional-generator feature cascade (all [D] until automated builder complete)

```
P-085 [DONE] + (run-create-project implemented) -> P-005 [D]
P-085 [DONE] + (run-create-project implemented) -> P-006 [D]
P-006 -> P-007 [D]
P-006 -> P-008 [D]
P-006 -> P-009 [D]
P-008 + P-009 -> P-010 [D]
P-010 -> P-011 [D]
```

---

### Research / comparisons (all [D] until automated builder core complete)

```
(automated builder core complete) -> P-017 [D], P-018 [D], P-019 [D], P-020 [D]
(devotional generator complete) -> P-021 [D]
(devotional generator + openclaw complete) -> P-022 [D]
```

---

### Critical path to Builder v1 (summary)

```
[DONE] P-084, P-085, P-098, P-083, P-012(original)

NEXT (all unblocked):
  P-099  Restart Protocol for Interrupted Inventories     [Gate-3]
  P-100  Normalize Verification Field Names               [Gate-1,6]
  P-086  Approval template pending-items sync             [Gate-4,6]
  P-088  Parallel Issue Execution Grouping Rule           [Gate-2,6]
  P-091  Proposal Update vs Approval-with-Changes Rule    [Gate-2,6]

THEN (remaining governance cleanup):
  P-087, P-089, P-090, P-096, P-003, P-015, P-013

GATE:
  P-092  Builder v1 Edge Case Evaluation (Pre-Deploy Gate)

POST-GATE:
  P-093, P-094, P-095 (Devotional Generator alignment)
```

---
