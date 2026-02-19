# P-085 — Verification

**Item**: P-085 — Builder Project Templates
**Artifact Type**: Verification
**Date**: 2026-02-19
**Verdict**: PASS

---

## Pending-Item Context

**ID**: P-085
**Intent**: Define a canonical location and rules for storing project seed/template files inside the automated-builder repo so `run-create-project` can copy/modify them to bootstrap a new project.
**Scope**: Choose and document the canonical template directory; define what belongs in templates; define placeholder substitution rules; define authority rules.

**Acceptance Criteria (from P-085 Definition of Done)**:
1. Canonical template directory exists and is referenced from system docs
2. Template contents cover the required project scaffold
3. Substitution rules are explicit and testable
4. Gatekeeper can verify a created project matches the template + substitutions

---

## Checks

### Check 1 — Canonical template directory referenced from system docs

**Criterion**: `docs/system/index.md` has a "Bootstrap Templates" subsection under "Where Things Live" stating `templates/project/` as canonical directory.

**Evidence**:
- `docs/system/index.md` line 211: `### Bootstrap Templates`
- Line 213: `**Location**: \`templates/project/\``
- Line 236–237: authority rule present — "Template files are system-controlled. Changes require a proposal and approval."
- 8-entry template table present (lines 220–229)

**Result**: PASS

---

### Check 2 — Template contents cover the required project scaffold

**Criterion**: All required template files exist at `templates/project/`.

**Evidence**:

| Template | Present |
|---|---|
| `project.yaml.tmpl` | ✅ |
| `index.md.tmpl` | ✅ |
| `prd.md.tmpl` | ✅ |
| `roadmap.md.tmpl` | ✅ |
| `iteration-log.md.tmpl` | ✅ |
| `builder-manifest.yaml.tmpl` | ✅ |
| `ai-process.md.tmpl` | ✅ |
| `pending-items-rules.md.tmpl` | ✅ |

All 8 templates present. Table in `docs/system/index.md` matches.

**Result**: PASS

---

### Check 3 — Substitution rules explicit and testable

**Criterion**: Placeholder token contract is documented in a stable, referenceable location — not embedded in an outputs artifact.

**Evidence**:
- `docs/implementation/system/template-specification.md` created (commit `386fb0a`) as normative substitution contract
- `docs/system/index.md` line 234: `**Normative spec**: [docs/implementation/system/template-specification.md](...)`
- `prompts/gatekeeper/gatekeeper-checklist.md` line 70: `**Spec**: [docs/implementation/system/template-specification.md](...)`

**Result**: PASS

---

### Check 4 — Gatekeeper can verify a bootstrapped project

**Criterion**: `prompts/gatekeeper/gatekeeper-checklist.md` has a Bootstrap Verification section with explicit checks.

**Evidence**:
- Line 66: `### Bootstrap Verification`
- Check 1 (line 72): all 8 deployment targets exist at expected paths
- Check 2 (line 75): `project.yaml` is valid YAML with required fields
- Check 3 (line 77): no unresolved `{...}` tokens
- Check 4 (line 79): identity values in non-YAML files match `project.yaml`
- Output verdict defined: `Bootstrap COMPLIANT / NON-COMPLIANT`

**Result**: PASS

---

## Verdict

**Verdict: PASS**

All four P-085 Definition of Done criteria are satisfied:

1. ✅ `templates/project/` documented in `docs/system/index.md` under "Where Things Live"
2. ✅ All 8 templates present and inventoried
3. ✅ Substitution contract in stable `docs/implementation/system/template-specification.md`
4. ✅ Bootstrap Verification checklist in `prompts/gatekeeper/gatekeeper-checklist.md`

---

## Completion Authority

Verification PASS authorizes moving P-085 from `docs/system/pending-items.md` to `docs/system/pending-items-archive.md`. Completion date: 2026-02-19.
