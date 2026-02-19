# Output Capture Directory

**Location**: `docs/system/outputs/`
**Purpose**: Evidence artifacts and long captures from Claude sessions
**Version**: 1.3
**Last Updated**: 2026-02-18

---

## Evidence, Not Authority

**outputs/ is an evidence store, not a normative authority.**

- Files here capture what happened in a session (plans drafted, decisions made, verification results).
- They MUST NOT be referenced as the canonical source for rules, contracts, or specifications.
- Normative contracts belong in `docs/implementation/` (stable, non-archived).

**Prohibition**: No document, prompt, or specification may cite a file in `docs/system/outputs/` as the authoritative source for a rule or contract. If an outputs file contains a normative statement, that statement must be extracted into a stable location before it can be referenced.

---

## Monthly Archive Convention

On the **5th of each month**, move all files dated in the prior calendar month into:

```
docs/system/outputs-archive/YYYY-MM/
```

`outputs/` retains only the **current month's** evidence files. `outputs-archive/` accumulates prior months.

**Example** (archiving on 2026-03-05):
```bash
mkdir -p docs/system/outputs-archive/2026-02
git mv docs/system/outputs/2026-02-*.md docs/system/outputs-archive/2026-02/
git commit -m "docs: archive 2026-02 session outputs"
```

README.md and any other non-dated index files remain in `outputs/` permanently.

---

## Overview

This directory stores evidence artifacts from Claude Code sessions. Every Claude iteration must produce an output artifact saved here as a session record.

---

## The Output Capture Rule

### When to Save Output to File

Every Claude iteration must produce an output artifact saved to
`docs/system/outputs/`.

---

## What Belongs in This Directory

### ✅ BELONGS HERE

**Planning Phase Outputs:**
- Planning summaries and status reports
- Iteration completion summaries
- Phase planning reviews
- Roadmap snapshots

**Build Phase Outputs:**
- Build completion summaries
- Commit point summaries
- Verification result compilations
- Build phase reviews

**Gatekeeper Outputs:**
- Formal review decisions
- Approval/rejection documentation
- Multi-phase review summaries
- Milestone gate decisions

**System Outputs:**
- Reorganization summaries
- Migration reports
- Cleanup logs
- System state snapshots

**Reference Outputs:**
- Project file trees
- Comprehensive status reports
- Cross-project comparisons
- Archive records

### ❌ DOES NOT BELONG HERE

**Project-Specific Planning:**
- Individual project PRDs → `../<slug>/prd.md`
- Phase plans → `../<slug>/phases/`
- Roadmaps → `../<slug>/roadmap.md`
- Iteration logs → `../<slug>/iteration-log.md`

**Project-Specific Workflow Artifacts:**
- Project proposals, approvals, verifications → `../<slug>/docs/system/outputs/`
- Project implementation summaries → `../<slug>/docs/system/outputs/`
- Project run reports → `../<slug>/docs/system/outputs/`

**Code and Implementation:**
- Source code → project directories (outside this repo)
- Scripts → `scripts/` (if manual utility scripts)
- Configuration → project root or appropriate subdirs

**Temporary Files:**
- Draft notes → local workspace (not committed)
- Scratch work → local workspace (not committed)
- Debug output → console or local files

**System Documentation:**
- Requirements docs → root level (`planning.md`, `builder.md`, `gateway.md`)
- System prompts → `prompts/planner/`, `prompts/builder/`, `prompts/gatekeeper/`
- General docs → `docs/system/` (this directory's sibling)

---

## Naming Convention

### Canonical Format

```
YYYY-MM-DD__NN__<context>__<short-description>.md
```

**Components:**
- `YYYY-MM-DD`: ISO 8601 date
- `NN`: Zero-padded daily sequence number (01, 02, 03, ...)
- `<context>`: Output context (planner | builder | gatekeeper | system)
- `<short-description>`: Brief descriptive name (lowercase, hyphen-separated)

### Examples

**Good:**
- `2026-02-05__01__planner__reorganization-summary.md`
- `2026-02-05__02__system__long-output-capture-implementation.md`
- `2026-02-10__01__builder__phase-001-completion.md`
- `2026-02-10__02__gatekeeper__phase-001-review.md`
- `2026-02-15__01__planner__iteration-2-complete.md`

**Bad:**
- `2026-02-05-output.md` (missing NN and context)
- `2026-02-05__1__planner__summary.md` (NN not zero-padded)
- `2026-02-05__01__random__summary.md` (invalid context)
- `2026-02-05__01__planner__Summary.md` (not lowercase)
- `output.md` (no date, NN, or context)

### Naming Rules

1. **Date**: Always `YYYY-MM-DD` (ISO 8601 date, e.g., 2026-02-05)
2. **Sequence**: Zero-padded daily counter `NN` (01, 02, 03, ...)
   - Starts at 01 each day
   - Increments for each new output on same day
   - Enables chronological ordering of same-day outputs
3. **Context**: One of four canonical contexts:
   - `planner` - Planning phase outputs
   - `builder` - Build phase outputs
   - `gatekeeper` - Review/approval outputs
   - `system` - System-level outputs (reorganizations, framework changes)
4. **Description**: Lowercase, hyphen-separated, concise (max 50 chars)
5. **Separators**: Use double underscores `__` between components
6. **Extension**: Always `.md` (markdown)

### System Iterator

The **system iterator** is the deterministic application of the naming convention
rules defined above. It is not a tool, not a human action, and not an external
service. Other documents that reference "the system iterator" refer to this
protocol.

**Algorithm:**

1. Scan all existing files in `docs/system/outputs/`.
2. For today's date (`YYYY-MM-DD`), find the highest existing `NN`.
3. The next filename uses `NN + 1` (zero-padded to two digits).
4. If no files exist for today's date, `NN` = `01`.
5. Context is determined by the session's role (`planner`, `builder`,
   `gatekeeper`, or `system`).
6. Description is determined by the session's task (lowercase,
   hyphen-separated, max 50 chars).

**Who executes it:** The session (assistant) applies the algorithm directly.
No human confirmation of the filename is required. No external tool is invoked.

**Verification (CP-7):** A filename is compliant if it was produced by this
algorithm — correct date, correct next `NN` for that date, valid context, and
valid description format. "Supplied by the system iterator" means "produced by
following this algorithm," not "provided by an external source."

---

## Artifact Types

### Inventory-Proposal Artifacts

**Name**: `inventory-proposal`

**Purpose**: Specification/inventory for implementation; does not execute.

**Characteristics**:
- Definition-only artifacts that specify implementation scope
- Contain Issue-### execution slices (implementation plans)
- Do not execute directly — implementation happens through Issue-### resolution loop
- Approved via rename to `*-approved.md`
- Referenced by parent P-### item in `pending-items.md`

**Naming Convention**:

```
YYYY-MM-DD__NN__system__<item-id>-inventory-proposal.md        (proposed)
YYYY-MM-DD__NN__system__<item-id>-inventory-proposal-approved.md  (approved)
```

**Components**:
- `YYYY-MM-DD`: Date of creation (ISO format)
- `NN`: Sequence number (01, 02, etc.) for same-day artifacts
- `system`: Context identifier
- `<item-id>`: Parent pending item ID (e.g., `p-084`)
- `-inventory-proposal`: Type identifier
- `-approved`: Approval suffix (added after approval)

**Examples**:
- `2026-02-13__01__system__p-084-inventory-proposal.md` (proposed)
- `2026-02-13__01__system__p-084-inventory-proposal-approved.md` (approved)

**Distinction from Regular Proposals**:
- **Regular proposals**: Single-issue implementation plans (Issue-###)
- **Inventory-proposals**: Multi-issue execution inventories with slice breakdown for P-### items

**Lifecycle**:

See [docs/system/issue-resolution.md](../issue-resolution.md) for the complete Inventory-Proposal Lifecycle Contract.

---

## Chat vs Repository Relationship

### Chat Output (Ephemeral)

**Purpose**: Real-time communication and interaction
**Audience**: User, immediate consumption
**Content**:
- Summaries (high-level)
- Quick status updates
- Interactive responses
- Guidance and explanations

**Example**:
```
✅ Reorganization complete!

Created 16 new files in correct structure.
See detailed output: docs/system/outputs/2026-02-05__01__planner__reorganization-summary.md
```

### Repository Output (Permanent)

**Purpose**: Formal record and future reference
**Audience**: Future readers, auditors, team members
**Content**:
- Detailed breakdowns
- Complete file listings
- Comprehensive checklists
- Full verification results

**Example**: The full 13,000-character reorganization summary with:
- Every file created, moved, deleted
- Complete structure diagrams
- Full compliance checklists
- Detailed next steps

### Relationship

**Chat → Repository**:
- Chat provides summary + pointer to file
- Repository file contains full detail
- User can read detail when needed, not forced to scroll

**Best Practice**:
1. Claude generates comprehensive output
2. Claude saves to `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md`
3. Claude responds in chat with summary + file path
4. User reads summary, clicks file path if detail needed

---

## File Retention

### Committed to Git

All files in this directory are committed to git and part of repository history. They are not deleted.

### Archiving

Follow the monthly archive convention described at the top of this document. Prior-month files move to `docs/system/outputs-archive/YYYY-MM/` on the 5th. This keeps the active `outputs/` directory scoped to current-month evidence only.

---

## Usage Examples

### Example 1: Planning Phase Complete

**Claude Action**:
```markdown
# Save to: docs/system/outputs/2026-02-05__01__planner__planning-phase-complete.md
[Comprehensive planning summary with all details...]
```

**Chat Response**:
```
✅ Planning phase complete!

Summary:
- 9 planning documents created
- 5 phases defined (CP1-CP11)
- All requirements met

Full details: docs/system/outputs/2026-02-05__01__planner__planning-phase-complete.md
```

### Example 2: Gatekeeper Review

**Claude Action**:
```markdown
# Save to: docs/system/outputs/2026-02-10__01__gatekeeper__review-phase-001.md
[Complete review with checklist, findings, decision, rationale...]
```

**Chat Response**:
```
🔄 Gatekeeper Review Complete

Decision: REVISE
Critical Issues: 2
Recommendations: 3

Full review: docs/system/outputs/2026-02-10__01__gatekeeper__review-phase-001.md
```

### Example 3: User Requests Output File

**User**: "send output to file"

**Claude Action**:
1. Determine appropriate filename based on context
2. Save to `docs/system/outputs/YYYY-MM-DD__NN__<context>__<description>.md`
3. Respond with confirmation and file path

---

## Integration with Workflow

### Planner

When planning phase completes:
- Save planning summary to `../<slug>/docs/system/outputs/YYYY-MM-DD__NN__planner__<description>.md`
- Include: files created, structure, commit points identified, next steps

### Builder

When phase completes:
- Save phase completion report to `../<slug>/docs/system/outputs/YYYY-MM-DD__NN__builder__<description>.md`
- Include: commits made, verification results, issues encountered

### Gatekeeper

When review completes:
- Save review decision to `../<slug>/docs/system/outputs/YYYY-MM-DD__NN__gatekeeper__<description>.md`
- Include: checklist results, decision, rationale, required changes

### System (automated-builder)

System-level artifacts about automated-builder itself continue to be saved here:
- Save to `docs/system/outputs/YYYY-MM-DD__NN__system__<description>.md`
- Include: issue resolutions, architecture reviews, verification artifacts

---

## Directory Organization

### Current Structure

The authoritative directory listing is the filesystem itself. Run
`ls docs/system/outputs/` or check the repository for the current file
inventory. Static file trees in this section are not maintained because
the directory changes frequently.

---

## Compliance

All outputs in this directory MUST:

1. ✅ Follow naming convention (YYYY-MM-DD__NN__<context>__<description>.md)
2. ✅ Be markdown format
3. ✅ Contain permanent, reference-quality content
4. ✅ Include date and context
5. ✅ Be committed to git (not temporary)

All outputs MUST NOT:

1. ❌ Contain sensitive data (credentials, keys, etc.)
2. ❌ Be temporary drafts (those stay local)
3. ❌ Duplicate project-specific planning (belongs in projects/)
4. ❌ Be generated by automation (docs-only principle)

---

## Related Documentation

- [planning.md](../../../planning.md) - Planning requirements (includes output rules)
- [builder.md](../../../builder.md) - Builder requirements (includes output rules)
- [gateway.md](../../../gateway.md) - Gatekeeper requirements (includes output rules)
- [docs/system/README.md](../README.md) - System documentation index

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2026-02-18 | Add "Evidence, Not Authority" policy; add monthly archive convention; update retention section (P-085 hygiene) |
| 1.2 | 2026-02-12 | Update project-specific paths from `docs/projects/<slug>/` to `../<slug>/`; direct project workflow artifacts to `../<slug>/docs/system/outputs/` (P-083) |
| 1.1 | 2026-02-10 | Replace stale file trees with filesystem-is-source-of-truth note; update header (Issue-005). Incorporates prior changes: canonical format references (Issue-002H), output capture rule replacement (Issue-003) |
| 1.0 | 2026-02-05 | Initial long output capture rule documentation |
