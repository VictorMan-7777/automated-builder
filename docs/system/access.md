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
