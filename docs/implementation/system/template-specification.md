<!-- STATUS: APPROVED -->

# Bootstrap Template Specification

**Location**: `docs/implementation/system/template-specification.md`
**Status**: Normative — Stable Authority
**Version**: 1.0
**Last Updated**: 2026-02-18

---

## 1. Canonical Template Directory

All project bootstrap templates reside in:

```
templates/project/
```

This is the single authoritative source. No other location is valid.

---

## 2. Required Template Inventory

| Template File | Deploys to (project-relative) |
|---|---|
| `project.yaml.tmpl` | `project.yaml` |
| `index.md.tmpl` | `index.md` |
| `prd.md.tmpl` | `prd.md` |
| `roadmap.md.tmpl` | `roadmap.md` |
| `iteration-log.md.tmpl` | `iteration-log.md` |
| `builder-manifest.yaml.tmpl` | `builder-manifest.yaml` |
| `ai-process.md.tmpl` | `docs/system/ai-process.md` |
| `pending-items-rules.md.tmpl` | `docs/system/pending-items-rules.md` |

All 8 templates MUST be present. Missing templates HALT bootstrap.

---

## 3. Placeholder Token Syntax

**Format**: `{Token}` — curly braces, Title Case or UPPERCASE.

**Allowed tokens and their source**:

| Token | Source |
|---|---|
| `{project-slug}` | Input parameter (lowercase-hyphenated) |
| `{Project Name}` | Input parameter |
| `{PREFIX}` | Input parameter (normalized to UPPERCASE) |
| `{YYYY-MM-DD}` | System date at execution time (ISO 8601) |

**Substitution source**: All token values are read from `project.yaml` (`identity.*` fields). `project.yaml` is created first and is the single source of truth for all substitution operations.

---

## 4. Bootstrap Compliance Rule

After substitution, no `{...}` patterns may remain in any bootstrap output file, excluding content inside code blocks and examples. Unresolved tokens HALT bootstrap.

---

## 5. Gatekeeper Verification Checks

A bootstrapped project is **COMPLIANT** if all four checks pass:

1. **Deployment targets exist** — All 8 project-relative paths from Section 2 are present on disk.
2. **`project.yaml` is valid** — Contains `identity.slug`, `identity.name`, `identity.prefix`, `identity.created`, and `schema_version: 1`.
3. **No unresolved tokens** — No `{...}` patterns in any bootstrap output file (excluding code blocks and examples).
4. **Identity consistency** — All identity values in non-YAML bootstrap files match `project.yaml` exactly.

**Output**: Bootstrap COMPLIANT / NON-COMPLIANT

---

## 6. Authority Rules

- Template files are system-controlled. Changes require a proposal and human approval.
- `run-create-project` may read from `templates/project/` and write only to `../<project-slug>/`.
- This document is the normative source for bootstrap template and substitution rules.
- Do NOT reference `docs/system/outputs/` files as authority for bootstrap compliance.

---

## Document History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-02-18 | Initial normative contract extracted from P-084 inventory evidence |
