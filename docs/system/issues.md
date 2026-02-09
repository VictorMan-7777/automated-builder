# Issue Numbering and Severity Scheme

**Version**: 1.0
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

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-09 | Initial issue numbering and severity scheme |
