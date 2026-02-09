# Issue Numbering and Severity Scheme

**Version**: 1.1
**Last Updated**: 2026-02-09

---

## Issue Identifiers

Issue identifiers use the format:

```
Issue-###
```

Where `###` is a zero-padded three-digit number (e.g., `001`, `012`, `100`).

---

## Severity Markers

Severity is indicated by appending a single-letter suffix to the identifier:

| Severity | Suffix | Example |
|----------|--------|---------|
| CRITICAL | C | Issue-007C |
| HIGH | H | Issue-012H |
| MEDIUM | *(none)* | Issue-021 |
| LOW | *(none)* | Issue-034 |

Only CRITICAL and HIGH receive a suffix marker. MEDIUM and LOW issues use the
bare identifier with no suffix.

---

## Where Issue Identifiers MUST Appear

Issue identifiers MUST be included in the following output artifact types:

- Proposal output artifacts
- Implementation documentation output artifacts
- Summary output artifacts

---

## Where Issue Identifiers MUST NOT Appear

Issue identifiers MUST NOT appear in:

- Output filenames (other than proposal, implementation, or summary artifacts)
- System or governance file bodies
- Implementation file contents

---

## Changelog Entry Format

If a system file contains a changelog section, each changelog entry that
corresponds to an issue MUST include:

1. Date changed
2. Description
3. Inventory file reference
4. Issue identifier

**Format:**

```
Date — Description — Inventory file — Issue-###(C|H)?
```

**Examples:**

```
2026-02-09 — Fix system iterator definition — 2026-02-09__02__system__fix-a-system-iterator-definition.md — Issue-001C
2026-02-09 — Expand governance lock list — 2026-02-09__06__system__fix-c-governance-lock-list-expansion.md — Issue-003H
2026-02-09 — Clarify commit convention — 2026-02-09__12__system__pass-1-deferred-items-register.md — Issue-015
```

---

## Issue Resolution Loop

Issues are resolved through a repeating loop per issue:

```
Inventory
→ Proposal
→ Approval
→ Change
→ Summary
→ repeat per Issue
→ Deferred / Unapproved + Verification
→ STOP
```

### Termination Conditions

The loop continues until one of the following is true:

1. The inventory is fully resolved (every issue has a completed summary), OR
2. Human intervention explicitly indicates all required issues are resolved.

### End-of-Loop Artifacts

At loop end, both of the following apply:

1. **Deferred / Unapproved register.** If any issues were deferred or
   unapproved during the loop, a Deferred / Unapproved register artifact
   is created and committed.
2. **Verification artifact.** A Verification artifact is always created
   and committed, regardless of whether any issues were deferred.

### Post-Verification Constraint

No new proposals may be started after the Verification artifact is created
without a new inventory.

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-02-09 | Add issue resolution loop and termination rules |
| 1.0 | 2026-02-09 | Initial issue numbering and severity scheme |
