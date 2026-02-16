# Issue-001 Proposal — Create Template Directory and Base Templates

**Issue**: Issue-001 — Create Template Directory and Base Templates
**Parent**: P-084 — run-create-project Bootstrap Specification
**Artifact Type**: Issue-Proposal
**Date**: 2026-02-16
**Status**: Approved

---

## Objective

Establish canonical template source per Section 2.1 of the P-084 inventory-approved artifact.

---

## Scope

### In Scope

- ✅ Create `automated-builder/templates/project/` directory
- ✅ Create 7 `.tmpl` files with placeholder content per Section 3
- ✅ Create `pending-items-rules.md.tmpl` for project rules pack
- ✅ Create `ai-process.md.tmpl` per Section 4.2

### Out of Scope

- ❌ Placeholder substitution logic
- ❌ Template rendering

---

## Acceptance Criteria

- [ ] Directory `templates/project/` exists at automated-builder root
- [ ] File `templates/project/project.yaml.tmpl` exists with Section 2.4 structure
- [ ] File `templates/project/index.md.tmpl` exists per Section 3.2
- [ ] File `templates/project/prd.md.tmpl` exists per Section 3.3
- [ ] File `templates/project/roadmap.md.tmpl` exists per Section 3.4
- [ ] File `templates/project/iteration-log.md.tmpl` exists per Section 3.5
- [ ] File `templates/project/builder-manifest.yaml.tmpl` exists per Section 3.6
- [ ] File `templates/project/ai-process.md.tmpl` exists per Section 4.2
- [ ] File `templates/project/pending-items-rules.md.tmpl` exists with `{PREFIX}` token
- [ ] All templates contain ONLY allowed tokens: `{project-slug}`, `{Project Slug}`, `{Project Name}`, `{YYYY-MM-DD}`, `{PREFIX}`
- [ ] All templates are readable (644 permissions minimum)

---

## Dependencies

None

---

## Files Likely Touched

- `templates/project/project.yaml.tmpl` (create)
- `templates/project/index.md.tmpl` (create)
- `templates/project/prd.md.tmpl` (create)
- `templates/project/roadmap.md.tmpl` (create)
- `templates/project/iteration-log.md.tmpl` (create)
- `templates/project/builder-manifest.yaml.tmpl` (create)
- `templates/project/ai-process.md.tmpl` (create)
- `templates/project/pending-items-rules.md.tmpl` (create)

---

## Risks / Failure Modes

- Token syntax inconsistency across templates
- Missing required placeholders
- Template content not matching Section 3 specifications exactly

---

## References

- Primary Authority: [docs/system/outputs/2026-02-13__01__system__p-084-inventory-approved.md](2026-02-13__01__system__p-084-inventory-approved.md)
  - Section 2.1: Canonical Template Source-of-Truth
  - Section 2.3: Placeholder Substitution Contract
  - Section 2.4: Project Identity (project.yaml structure)
  - Section 3: Required Files and Contract Mapping
  - Section 4.2: AI Process Contract
  - Section 10: Issue-### Implementation Plan (Issue-001)
