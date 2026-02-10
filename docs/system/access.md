# Session Access Modes for Claude Prompts

This document defines the **session access modes** that may be declared at the
top of the first prompt in a new Claude session.

This file is **human-facing documentation only**.

Claude MUST NOT read or use this file unless a session access mode is explicitly
declared in the prompt.

This file is governance-locked by default under CP-2 (see
`docs/implementation/system/checkpoint-taxonomy.md`). Sessions read this file
for integrity baselining; this does not constitute behavioral use.

Prompts declare access by **reference**, not by restating rules.

---

## How to Declare Access in a Prompt

At the very top of the first prompt in a new session, include a
**Session Access Declaration**:

```text
Session Access Declaration:
mode = <mode-name>

## Access Modes

This document defines the available session access modes and their intended use.
It does not define enforcement behavior.

The authoritative behavioral rules for each access mode — including permissions,
constraints, stop conditions, and escalation requirements — are defined exclusively
in the session authority header (`initial-prompt.md`).

This separation is intentional to prevent duplication and rule drift.

### planning-only

Used for design, reasoning, review, and decision-making.

This mode is appropriate when:
- no filesystem interaction is required
- no repository inspection or modification is intended
- the session outcome is conceptual or textual

### bootstrap-file

Used to create or update a single, explicitly scoped file during initial system
bootstrap or foundational setup.

This mode is appropriate when:
- exactly one file must be introduced or modified
- the work is expected to be self-contained
- discovery of dependencies should halt progress rather than expand scope

### repo-rw

Used for implementation work requiring read and write access across the repository.

This mode is appropriate when:
- multiple files are expected to change
- dependency resolution is intentional
- the full system context is required

---

## Cross-Mode Permissions

### Output Writes

Writing **new** files to `docs/system/outputs/` is permitted in all access modes.
This is the canonical output directory for all reviewable artifacts.

**Output requirement rule.** Every Claude iteration must produce an output
artifact saved to `docs/system/outputs/`. This obligation is unconditional — it
is not gated by artifact type, length, or session mode. The output artifact
documents the work performed during the iteration and prevents untracked changes
and lost work.

**Output compliance clause.** A session may not be considered complete until its
output artifact exists in `docs/system/outputs/`. The session must confirm
output creation explicitly in chat before stopping. Failure to do so is a
session failure.

For interrupted sessions — sessions that terminate before CP-9 records a
PASS — the output obligation is satisfied via the exception path defined in the
checkpoint taxonomy (Section 3.4). An interrupted session that produces an
interruption artifact via CP-7 out-of-order satisfies this clause.
Post-termination recovery artifacts are governed by Section 3.4.2 of the
checkpoint taxonomy and are not subject to in-session confirmation.

This is enforced by the session authority header (see `initial-prompt.md`).

Producing an output artifact is conceptually separate from applying doc changes.
A session may do both only when its authority declaration permits both.

Output filenames are managed by the system iterator (defined in
`docs/system/outputs/README.md`) and must not be chosen or suggested by the
assistant.

This permission does not allow:
- modifying or overwriting existing output files
- reading output files as inputs
- writing to any other directory beyond mode permissions

---

## Authority Boundary

Access mode behavior is enforced by the session authority header
(`docs/system/initial-prompt.md`). The session lifecycle — including checkpoint
ordering, governance locking, artifact production, and commit validation — is
governed by the checkpoint taxonomy
(`docs/implementation/system/checkpoint-taxonomy.md`).

This document must not be used to infer permissions or justify actions
outside the declared session mode.
