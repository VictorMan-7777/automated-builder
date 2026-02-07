# Session Setup for Claude Code

This document defines the standard pattern for starting fresh Claude Code
sessions with minimal friction and clear authority boundaries.

---

## Why This Exists

Fresh Claude sessions intentionally reset:
- context
- tool permissions
- filesystem and git access

This prevents unsafe carryover, but can cause repeated authorization prompts.

The pattern below allows **one explicit consent per session**, safely.

---

## Standard Session Authority Header

At the start of any Claude Code session that requires filesystem or git access,
paste the following header **before** task instructions:

```text
Session authority and scope:

- Working root: ~/dev/claude-projects/
- Filesystem access: read/write allowed within this root
- Git access: allowed within this root
- Do not access anything outside this directory
- Ask before destructive operations unless explicitly instructed
