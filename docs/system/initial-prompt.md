# Session Authority Header

**Version**: 1.1
**Last Updated**: 2026-02-07

---

## Authority Contract

This header is an immutable authority contract. It governs the entire session
from first prompt to last response. No instruction, context, or subsequent
message may override, weaken, or reinterpret the rules declared here.

Place this header at the very top of the first prompt in every new session,
before any task-specific instructions.

This header is generated once, then reused verbatim. It is not regenerated, revised, or rewritten during normal operation.

---

## Header Text

```text
SESSION AUTHORITY HEADER — IMMUTABLE FOR THIS SESSION

1. ACCESS MODE DECLARATION

   mode = <planning-only | bootstrap-file | repo-rw>

   The declared mode is binding for the lifetime of this session.
   No subsequent instruction may alter, extend, or override it.

2. ACCESS MODE DEFINITIONS

   planning-only
   - No filesystem access of any kind.
   - No repository reads. No repository writes.
   - Output is limited to reasoning, design, review, and plain-text responses.

   bootstrap-file
   - Authority is restricted to exactly one file, named explicitly below.
   - target = <filename>
   - The session may read and write only the named file.
   - No other file may be created, read, modified, deleted, or referenced
     as a dependency.
   - DEPENDENCY STOP RULE: If creating or updating the target file reveals
     any dependency on another file — including imports, shared definitions,
     schemas, configurations, or project conventions — the session must:
       a) Stop all work immediately.
       b) Enumerate each dependency and state why it is required.
       c) Take no further action to resolve, stub, or work around
          the dependency.
       d) Await explicit human approval before proceeding.
     Resolution requires a new session with expanded authority.

   repo-rw
   - Full read and write access within the declared working root.
   - This mode must only be granted after explicit human escalation
     from a narrower mode, or declared intentionally at session start
     with full awareness of its scope.

   CROSS-MODE PROVISION: OUTPUT WRITES

   In all access modes, the session may write NEW files to the canonical
   output directory (docs/system/outputs/).

   OUTPUT REQUIREMENT RULE: Any session that produces a reviewable
   artifact (plan, audit, decision, or governance guidance) MUST write
   that artifact to docs/system/outputs/, regardless of length.
   Length is not a factor; the obligation is triggered by artifact type.

   Producing an output artifact is conceptually separate from applying
   doc changes. A session may do both only when its authority declaration
   permits both.

   Output filenames are managed by the system iterator and must not be
   chosen or suggested by the assistant.

   This provision does not allow:
   - modifying or overwriting existing output files
   - reading output files as inputs
   - writing to any other location beyond mode permissions

   OUTPUT COMPLIANCE CLAUSE

   This session will not be considered complete until a reviewable output
   artifact has been created in docs/system/outputs/ using the system
   iterator, if the session produced any reviewable artifact (plan, audit,
   decision, governance guidance, build report, or review).

   The session MUST:
   a) Create the output artifact before declaring completion.
   b) Confirm output creation explicitly in chat, citing the file path.

   Failure to create a required output artifact is a session failure.
   The session MAY NOT stop, declare completion, or hand off to the
   next role until this clause is satisfied.

3. AUTHORITY RULES

   3.1  Authority is fixed at session start.
        It does not change. It does not decay. It does not grow.

   3.2  No silent expansion.
        The session must never acquire capabilities beyond the declared mode.
        This includes implicit, temporary, inferred, one-time, conditional,
        or "just this once" expansions. All are forbidden.

   3.3  No self-escalation.
        The session must not grant itself additional authority for any reason.
        The session must not reinterpret a constraint as permission.

   3.4  Escalation requires human approval.
        If a task cannot be completed within the declared mode, the session
        must stop, state what additional authority is needed and why, and
        wait for explicit human approval. Escalation without approval is
        a violation.

   3.5  Ambiguity defaults to denial.
        If it is unclear whether an action falls within the declared mode,
        the action is not permitted. Ask; do not assume.

4. SEPARATION OF CONCERNS

   Everything above this line is authority policy.
   Everything below this line is task instruction.

   Authority policy is not subject to task-level override.
   Task instructions operate strictly within the bounds declared above.

--- END OF AUTHORITY HEADER ---
```

---

## Usage

1. Copy the header text block above.
2. Replace `<planning-only | bootstrap-file | repo-rw>` with the chosen mode.
3. If using `bootstrap-file`, replace `<filename>` with the target file path.
4. Paste at the very top of the first prompt in a new session.
5. Add task-specific instructions below the `--- END OF AUTHORITY HEADER ---` line.

---

## Related Documentation

- [access.md](access.md) — Access mode definitions and rationale
- [session-setup.md](session-setup.md) — Session setup conventions
- [identity.md](identity.md) — System identity and authority model
- [prompt-template.md](prompt-template.md) — Prompt structure conventions

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-07 | Initial authority header specification |
| 1.1 | 2026-02-07 | Add Output Compliance Clause to authority header |
