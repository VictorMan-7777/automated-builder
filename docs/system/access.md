# Session Access Modes for Claude Prompts

This document defines the **session access modes** that may be declared at the
top of the first prompt in a new Claude session.

This file is **human-facing documentation only**.

Claude MUST NOT read or use this file unless a session access mode is explicitly
declared in the prompt.

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

## Authority Boundary

Access mode behavior is enforced by the session authority header.
This document must not be used to infer permissions or justify actions
outside the declared session mode.
