# Long Output Capture Directory

**Location**: `docs/system/outputs/`
**Purpose**: Canonical storage for lengthy Claude Code outputs that exceed chat readability
**Version**: 1.0
**Last Updated**: 2026-02-05

---

## Overview

This directory stores formal, permanent records of Claude Code outputs that are too long for comfortable chat consumption. When Claude generates comprehensive summaries, planning artifacts, or detailed reports, those outputs must be saved here for permanent record.

---

## The Output Capture Rule

### When to Save Output to File

Claude MUST save output to a file in this directory when the session produces
a **reviewable artifact**. Length is not a factor; the obligation is triggered
by artifact type, not size.

Reviewable artifacts:

- **Plans** — iteration plans, phase plans, implementation plans
- **Audits** — compliance checks, rule audits, quote-sourcing audits
- **Decisions** — rule changes, scope rulings, governance clarifications
- **Governance guidance** — policy interpretations, process documentation
- **Build reports** — phase completion reports, commit point summaries
- **Reviews** — gatekeeper review decisions, milestone gate decisions
- **Interruption reports** — session interruption artifacts
- **Gap reports** — gap analysis and diagnostic artifacts

Additionally, Claude saves to this directory when the user explicitly
requests it (e.g., "save output to file").

### When NOT to Save

- Interactive Q&A exchanges
- Error messages or debugging output
- Quick status updates
- File content displays (those belong in their proper locations)

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
- Individual project PRDs → `docs/projects/<slug>/prd.md`
- Phase plans → `docs/projects/<slug>/phases/`
- Roadmaps → `docs/projects/<slug>/roadmap.md`
- Iteration logs → `docs/projects/<slug>/iteration-log.md`

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

### Permanent Storage

Files in this directory are **permanent records**:
- Committed to git
- Part of repository history
- Not deleted unless explicitly outdated/superseded

### When to Archive

If a file becomes obsolete:
1. Create `docs/system/outputs/archive/` directory
2. Move old file to archive with note
3. Document in commit message why archived

Example:
```bash
mkdir -p docs/system/outputs/archive
git mv docs/system/outputs/2026-01-15__01__planner__old-plan.md \
       docs/system/outputs/archive/2026-01-15__01__planner__old-plan.md
git commit -m "docs: archive superseded planning output"
```

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
- Save planning summary to `docs/system/outputs/YYYY-MM-DD__NN__planner__<description>.md`
- Include: files created, structure, commit points identified, next steps

### Builder

When phase completes:
- Save phase completion report to `docs/system/outputs/YYYY-MM-DD__NN__builder__<description>.md`
- Include: commits made, verification results, issues encountered

### Gatekeeper

When review completes:
- Save review decision to `docs/system/outputs/YYYY-MM-DD__NN__gatekeeper__<description>.md`
- Include: checklist results, decision, rationale, required changes

---

## Directory Organization

### Current Structure

```
docs/system/outputs/
├── README.md (this file)
├── 2026-02-05__01__planner__reorganization-summary.md
├── 2026-02-05__02__system__long-output-capture-implementation.md
└── (future outputs...)
```

### Future Structure (with archives)

```
docs/system/outputs/
├── README.md
├── archive/
│   └── (superseded outputs)
├── 2026-02-05__01__planner__reorganization-summary.md
├── 2026-02-05__02__system__long-output-capture-implementation.md
├── 2026-02-10__01__planner__planning-phase-complete.md
├── 2026-02-10__02__builder__phase-001-complete.md
└── (ongoing outputs...)
```

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
| 1.0 | 2026-02-05 | Initial long output capture rule documentation |
