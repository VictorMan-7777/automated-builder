# Issue-003 — Approved: Superseded Length-Based Policy in README.md "When to Save" Section

**Date:** 2026-02-10
**Issue:** Issue-003
**Severity:** MEDIUM
**Inventory:** `2026-02-09__16__system__output-file-system-inventory.md`

---

## Proposal

Replace the "When to Save Output to File" and "When NOT to Save" content in
`docs/system/outputs/README.md` (lines 16–52) with text that reflects the
artifact-type-based policy established by the Output Requirement Rule change
(`2026-02-07__04__system__output-requirement-rule-change.md`) and codified in
`docs/system/access.md` (Output Writes section, lines 76–80).

The section heading is also updated from "The Long Output Capture Rule" to
"The Output Capture Rule" since the word "Long" reflects the superseded
length-based framing.

No new rules, formats, or policies are introduced. The replacement text
restates the authoritative policy already in effect.

---

## Affected Section

**File:** `docs/system/outputs/README.md`
**Lines:** 16–52 (section heading through end of "When NOT to Save")

### Current Text (superseded)

```markdown
## The Long Output Capture Rule

### When to Save Output to File

Claude MUST save output to a file in this directory when:

1. **Length Exceeds Chat Readability**
   - Output is > 500 lines
   - Output includes multiple sections with detailed sub-content
   - Scrolling through chat would be cumbersome

2. **Permanent Record Required**
   - Summary of significant work completed
   - Planning phase outputs
   - Gatekeeper review decisions
   - Major milestone completions
   - Iteration summaries

3. **Reference Material**
   - File trees of project structure
   - Comprehensive checklists
   - Detailed status reports
   - Migration or reorganization summaries

4. **User Explicitly Requests**
   - User says "save output to file"
   - User says "send output to temp-output.md" (or similar)
   - User provides specific filename

### When NOT to Save

- Short responses (< 100 lines)
- Interactive Q&A exchanges
- Error messages or debugging output
- Quick status updates
- File content displays (those belong in their proper locations)
```

### Proposed Text

```markdown
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
```

---

## Change

One contiguous text replacement in `docs/system/outputs/README.md`, covering
lines 16–52. No other files are created, modified, or deleted.

### Summary of Differences

| Aspect | Current (superseded) | Proposed |
|--------|---------------------|----------|
| Section heading | "The Long Output Capture Rule" | "The Output Capture Rule" |
| Primary trigger | Length-based (> 500 lines) | Artifact-type-based |
| Artifact types listed | Informal categories (permanent record, reference material) | Closed list from rule change artifact |
| "Short responses (< 100 lines)" exclusion | Present | Removed (length is irrelevant) |
| User-explicit-request trigger | Listed as category 4 | Retained as secondary paragraph |

---

## Rationale

1. The Output Requirement Rule change (`2026-02-07__04__system__output-requirement-rule-change.md`)
   explicitly replaced the length-based heuristic with an artifact-type trigger.
2. The authoritative policy in `docs/system/access.md` (lines 76–80) states:
   "Length is not a factor; the obligation is triggered by artifact type, not size."
3. The README's "When to Save" section still lists "> 500 lines" as the primary
   trigger, directly contradicting the authoritative documents.
4. The "When NOT to Save" list includes "Short responses (< 100 lines)" which
   implies length matters — contradicting the rule change.
5. The proposed text uses the closed reviewable-artifact list from the rule change
   artifact and the expanded list from `access.md`. No new artifact types are added.

---

## Verification

After implementation, the following checks confirm resolution:

| Check | Expected Result |
|-------|-----------------|
| No length-based triggers ("> 500 lines", "< 100 lines") in the "When to Save" or "When NOT to Save" sections | True |
| Section heading no longer says "Long" | True |
| Reviewable artifact list matches authoritative sources | True |
| "When NOT to Save" exclusions match rule change artifact's non-artifact list | True |
| No other sections of README.md were modified | True |
| No other files were modified | True |

---

## Approval Request

Requesting approval to implement Issue-003 as specified above. The scope is
limited to one contiguous text replacement in `docs/system/outputs/README.md`
(lines 16–52). No other files are modified. No new rules or policies are
introduced.
