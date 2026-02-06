# Canonical Prompt Template

**Version**: 1.0
**Last Updated**: 2026-02-06

---

## Purpose

This template standardizes the structure of system prompts across roles (Planner, Builder, Gatekeeper, review prompts). It defines **structure**, not policy. Use of this template is recommended but not required.

**Goals**:
- Consistent prompt organization
- Explicit authority and constraints
- Clear stop points for human review
- Predictable prompt behavior

**Non-Goals**:
- Encoding behavioral rules (see identity.md, planning.md, etc.)
- Enforcing specific policies
- Replacing role-specific documentation

---

## Template Structure

### Required Sections

Every system prompt should include:

1. **Identity Loading** — Reference to system identity
2. **MODE Declaration** — What type of operation this is
3. **Objective** — What the prompt accomplishes
4. **Steps / Instructions** — Numbered actions to perform

### Optional Sections

Include when applicable:

- **Authority & Constraints** — Scope boundaries
- **Review / Stop Conditions** — When to pause for human input
- **Commit Instructions** — If the prompt may result in a commit

---

## Canonical Structure

```markdown
Read docs/system/identity.md first.

MODE: <MODE_VALUE>
(<brief clarification if needed>)

Objective:
<What this prompt accomplishes>

------------------------------------------------------------
STEP 1 — <Step Title>
<Instructions for step 1>

------------------------------------------------------------
STEP 2 — <Step Title>
<Instructions for step 2>

------------------------------------------------------------
STEP N — Review pause (STOP HERE)
<Stop conditions and what to show before awaiting approval>

------------------------------------------------------------
STEP N+1 — Commit (ONLY IF APPROVED)
<Commit instructions, if applicable>

END.
```

---

## MODE Values

MODE declares the operational context. Examples:

| MODE | Description |
|------|-------------|
| `PLANNER` | Planning stage, docs-only output |
| `DOCS-ONLY` | Documentation changes only, no execution |
| `COMMIT-ONLY` | Limited to creating a specific commit |
| `REVIEW` | Gatekeeper or review operation |
| `BUILDER` | Execution stage (future) |

MODE values are descriptive, not prescriptive. Choose a value that clearly communicates intent.

---

## Key Principles

### Explicit Authority

State clearly:
- What the prompt is allowed to do
- What the prompt must not do
- What scope boundaries apply

### Explicit Stop Points

Include review pauses:
- Before commits
- Before irreversible actions
- When human judgment is needed
- At task completion

### Human-in-the-Loop

Design prompts to:
- Stop and show work before proceeding
- Await explicit approval for significant actions
- Provide clear summaries for human review

---

## Example: Minimal Prompt

```markdown
Read docs/system/identity.md first.

MODE: DOCS-ONLY

Objective:
Update the README with installation instructions.

------------------------------------------------------------
STEP 1 — Read current README
Read README.md and note what exists.

------------------------------------------------------------
STEP 2 — Add installation section
Add a new "Installation" section with the provided instructions.

------------------------------------------------------------
STEP 3 — Review pause (STOP HERE)
1) Show `git diff --stat`
2) Summarize changes
3) STOP and await approval to commit

------------------------------------------------------------
STEP 4 — Commit (ONLY IF APPROVED)
If approved, create commit:
"docs: add installation instructions to README"

END.
```

---

## Usage Notes

- **Preflight checks** (e.g., `git status`) help establish context
- **Numbered steps** make progress trackable
- **Separator lines** (`----`) improve readability
- **END.** signals prompt completion

---

## Related Documentation

- [docs/system/identity.md](identity.md) — System identity and principles
- [docs/system/index.md](index.md) — System overview

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-06 | Initial prompt template |
