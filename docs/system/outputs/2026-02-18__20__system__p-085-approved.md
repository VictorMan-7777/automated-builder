# P-085 — Proposal: Builder Project Templates

**Item**: P-085 — Builder Project Templates: Define Where to Store `<slug>` Seed Files for `run-create-project`
**Artifact Type**: Proposal
**Date**: 2026-02-18
**Status**: APPROVED
**Iteration**: 3

---

## Scope

Two targeted edits to existing files. No new files created.

### Edit 1 — `docs/system/index.md`

Add a "Bootstrap Templates" subsection under "Where Things Live".

**Content to add**:

```markdown
### Bootstrap Templates

**Location**: `templates/project/`

**Purpose**: Canonical template source-of-truth for `run-create-project`. All project bootstrap
files are generated from these templates with placeholder substitution.

**Templates**:

| Template | Deploys to (project-relative) |
|---|---|
| `project.yaml.tmpl` | `project.yaml` |
| `index.md.tmpl` | `index.md` |
| `prd.md.tmpl` | `prd.md` |
| `roadmap.md.tmpl` | `roadmap.md` |
| `iteration-log.md.tmpl` | `iteration-log.md` |
| `builder-manifest.yaml.tmpl` | `builder-manifest.yaml` |
| `ai-process.md.tmpl` | `docs/system/ai-process.md` |
| `pending-items-rules.md.tmpl` | `docs/system/pending-items-rules.md` |

**Placeholder syntax**: `{Token}` — e.g. `{project-slug}`, `{Project Name}`, `{PREFIX}`, `{YYYY-MM-DD}`.
For full substitution contract see: [docs/implementation/system/template-specification.md](../../implementation/system/template-specification.md)

**Authority**: Template files are system-controlled. Changes require a proposal and approval.
`run-create-project` may read templates and write only to `../<project-slug>/`.
```

### Edit 2 — `prompts/gatekeeper/gatekeeper-checklist.md`

Add a "Bootstrap Verification" review type after the existing "Phase Review" section.

**Content to add**:

```markdown
### Bootstrap Verification

Review a project bootstrapped by `run-create-project` for template compliance:

- [ ] All 8 deployment targets exist at the expected project-relative paths
  (project.yaml, index.md, prd.md, roadmap.md, iteration-log.md,
  builder-manifest.yaml, docs/system/ai-process.md, docs/system/pending-items-rules.md)
- [ ] `project.yaml` is valid YAML containing `identity.slug`, `identity.name`,
  `identity.prefix`, `identity.created`, and `schema_version: 1`
- [ ] No file in the bootstrap output contains unresolved `{...}` tokens
  (excluding code blocks and examples)
- [ ] All identity values in non-YAML bootstrap files match `project.yaml` exactly

**Output**: Bootstrap COMPLIANT / NON-COMPLIANT
```

---

## Non-Goals

- No `run-create-project` script changes
- No template file content changes
- No new files
- No other changes to `docs/system/index.md` or `prompts/gatekeeper/gatekeeper-checklist.md`

---

## Acceptance Criteria

- [ ] `docs/system/index.md` has "Bootstrap Templates" subsection under "Where Things Live"
- [ ] Subsection contains the template table (all 8 entries)
- [ ] Subsection states `templates/project/` as canonical directory
- [ ] Subsection states authority rule (system-controlled, changes require proposal/approval)
- [ ] `prompts/gatekeeper/gatekeeper-checklist.md` has "Bootstrap Verification" review type
- [ ] Checklist contains all 4 template compliance checks
- [ ] No new files created
- [ ] No other files modified

---

## Definition of Done Mapping

| DoD Item | Satisfied By |
|---|---|
| Canonical template directory exists and is referenced from system docs | Edit 1 (index.md) |
| Template contents cover the required project scaffold | Pre-existing — P-084 delivery; confirmed by template table in Edit 1 |
| Substitution rules are explicit and testable | Edit 1 references `docs/implementation/system/template-specification.md` as the normative substitution contract |
| Gatekeeper can verify a created project matches template + substitutions | Edit 2 (gatekeeper checklist) |

---

## Change Log

| Version | Date | Trigger | Review Count | Summary | Reason | Sections Impacted |
|---|---|---|---|---|---|---|
| 1.0 | 2026-02-18 | Initial draft | 1 | Inventory proposal with 3 Issues including template-specification.md creation | Initial | All |
| 2.0 | 2026-02-18 | Human revision instruction | 2 | Converted to Regular proposal; removed Issue-001 and template-specification.md; flattened to 2 file edits; removed Inventory classification | template-specification.md creates no enforceable invariant; all DoD items satisfy with targeted edits to existing files | All |
| 3.0 | 2026-02-18 | Authority layering hardening | 4 | Fix substitution contract reference from P-084 outputs artifact to stable `docs/implementation/system/template-specification.md` | outputs/ must not be referenced as normative authority | Edit 1, DoD mapping |

---

