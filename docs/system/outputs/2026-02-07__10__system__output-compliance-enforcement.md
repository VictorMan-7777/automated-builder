# Output Compliance Enforcement — Governance Update

**Date**: 2026-02-07
**Context**: system
**Session Type**: Governance update (system fix)

---

## Problem

The system rule "always produce outputs for any reviewable artifact" existed but was not reliably enforced at session boundaries. Sessions could complete without producing an output artifact, requiring human intervention to detect and correct the omission.

The root cause: the rule was aspirational ("MUST write"), not procedural. Nothing blocked session completion when the output was missing. Additionally, the Planner prompt gated output creation on artifact length ("if output is lengthy"), allowing shorter artifacts to skip output creation entirely.

---

## Solution

Introduced a mandatory **Output Compliance Clause** that makes output artifact creation a structural precondition for session completion, enforced at three layers.

---

## Changes Applied

### 1. Authority Header — `docs/system/initial-prompt.md` (v1.0 → v1.1)

**What**: Added OUTPUT COMPLIANCE CLAUSE to the immutable authority header, between the existing CROSS-MODE PROVISION and AUTHORITY RULES sections.

**Effect**: Every session using the authority header is now bound by the clause. The session MAY NOT stop, declare completion, or hand off to the next role until the output artifact exists. Failure is classified as a "session failure."

**Key language**:
> "This session will not be considered complete until a reviewable output artifact has been created in docs/system/outputs/ using the system iterator, if the session produced any reviewable artifact."

### 2. Access Mode Documentation — `docs/system/access.md`

**What**: Added "Output compliance clause" paragraph under Cross-Mode Permissions > Output Writes, linking the procedural stop-condition to the authority header.

**Effect**: The human-facing access documentation now reflects both the obligation (output requirement rule) and the enforcement mechanism (output compliance clause).

### 3. Prompt Template — `docs/system/prompt-template.md` (v1.0 → v1.1)

**What**: Added "Output Compliance (All Modes)" as a Standard Instruction Block, alongside the existing "Planner Output Behavior" block.

**Effect**: All prompts that follow the canonical template and produce reviewable artifacts must include the OUTPUT COMPLIANCE block. This is mode-agnostic — applies to PLANNER, BUILDER, REVIEW, and any future mode.

### 4. Planner Entry Prompt — `prompts/planner/run-planner.md`

**What**:
- Replaced Step 7 "Apply Long Output Rule" (conditional on length) with "Create Output Artifact (MANDATORY)" (unconditional).
- Updated Completion Checklist: replaced "Long output saved to file (if applicable)" with "Output artifact created in docs/system/outputs/ (mandatory — not conditional on length)" and added "Output creation confirmed in chat with file path cited."

**Effect**: Planner sessions can no longer skip output creation based on artifact length.

### 5. Builder Entry Prompt — `prompts/builder/run-builder.md`

**What**:
- Added output compliance preamble to Completion Checklist section.
- Added "Output creation confirmed in chat with file path cited" to both Dry-Run and Apply mode checklists.

**Effect**: Builder sessions have explicit output compliance language at the checklist level, consistent with the authority header clause.

---

## Enforcement Mechanism (Three Layers)

| Layer | Location | Mechanism |
|-------|----------|-----------|
| Root authority | `initial-prompt.md` Authority Header | OUTPUT COMPLIANCE CLAUSE — session-level stop condition |
| Template guidance | `prompt-template.md` Standard Instruction Blocks | OUTPUT COMPLIANCE block — prompt-level instruction |
| Role-specific checklists | `run-planner.md`, `run-builder.md` | Mandatory checklist items — execution-level verification |

---

## Design Properties

- **Procedural, not aspirational**: Uses stop-condition language ("MAY NOT stop", "session failure"), not guidance language ("should", "is recommended").
- **Does not rely on filename conventions**: References `docs/system/outputs/` and the system iterator without specifying naming patterns.
- **Uses the system iterator implicitly**: Output filenames are managed by the iterator, not chosen by the session.
- **No external-platform identifiers**: All references are system-internal.
- **Minimal and auditable**: Five targeted edits across five files, all within system governance and prompt templates.

---

## Confirmation

- No code changes were made.
- No filesystem reorganization was performed.
- All edits were within system governance documents and prompt templates.
- No output artifacts were created for past sessions.
