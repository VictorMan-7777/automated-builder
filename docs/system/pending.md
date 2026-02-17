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

### Dependency model through P-086

Legend:
A -> B means A must be completed before B can be meaningfully executed.
(A) means cluster / umbrella dependency
[D] means deferred until <condition>

Core builder readiness
P-012 (Builder completion criteria) -> P-084 (run-create-project spec)
P-083 (Planner output root -> ../<slug>/) -> P-084 (run-create-project spec)

Project bootstrapping
P-084 (run-create-project spec) -> P-085 (template source-of-truth location)
P-085 (templates) -> (run-create-project implemented) -> first planner run

Devotional-generator (all currently [D] until automated builder complete)
P-084 + P-085 + (run-create-project implemented) -> P-005 [D]
P-084 + P-085 + (run-create-project implemented) -> P-006 [D]
P-006 -> P-007 [D] (uniqueness depends on series support)
P-006 -> P-008 [D] (spreadsheet import depends on series plan model)
P-006 -> P-009 [D] (scrivener import depends on series plan model + locking)
P-008 + P-009 -> P-010 [D] (imports + generation workflow)
P-010 -> P-011 [D] (export depends on generated volumes)

Research / comparisons (mostly [D] until automated builder core complete)
(automated builder core complete) -> P-017 [D]
(automated builder core complete) -> P-018 [D]
(automated builder core complete) -> P-019 [D]
(automated builder core complete) -> P-020 [D]
(devotional generator complete) -> P-021 [D]
(devotional generator + openclaw integration complete) -> P-022 [D]

---
