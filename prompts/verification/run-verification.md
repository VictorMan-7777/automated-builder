# Run Verification — Entry Prompt

**Version**: 1.0
**Purpose**: Canonical invocation template for Verification sessions
**Last Updated**: 2026-02-23

---

## Invocation Parameters

Before proceeding, confirm all three parameters are present in the session prompt.
If any parameter is missing, **stop and ask the human**.

| Parameter | Format | Description |
|-----------|--------|-------------|
| `project_repo_root` | Absolute path | Root directory of the target project repository |
| `phase_id` | NNN (three-digit) | Phase number to verify (e.g., `001`) |
| `build_report_path` | Relative path from builder repo root | Path to the build report in `docs/system/outputs/` |

### Two-Repo Context

This session operates across two repositories:

| Repo | Path | Role | Write Scope |
|------|------|------|-------------|
| **Builder repo** | `automated-builder` (this repository) | Governance, contracts, verification artifacts | Verification artifact to `docs/system/outputs/` only |
| **Project repo** | `{project_repo_root}` | Phase plans, manifest | Read-only |

**Rule**: The Verification session reads from both repositories. It writes only the verification artifact to the builder repo. No mutations to the project repo are permitted.

---

## Read Order

Read these documents **in this exact order** before running any checks.
Do not proceed until you have read and understood each document.

1. [docs/system/identity.md](../../docs/system/identity.md) — System identity and principles
2. [docs/implementation/system/verification-contract.md](../../docs/implementation/system/verification-contract.md) — Verification role, checks, and output requirements
3. `{project_repo_root}/builder-manifest.yaml` — Project manifest (read-only)
4. Build report at `{build_report_path}` — The Builder session output to verify
5. Phase plan: `{project_repo_root}/{paths.phases}/{phase_id}-*.md` — The approved plan that was executed

After reading the manifest (step 3), resolve all paths before reading further project files.

---

## Execution Steps

Follow these steps in exact order. Do not skip, reorder, or combine steps.

### Step 1: Validate Invocation Parameters

Confirm all three parameters are present and valid:
- `project_repo_root` — directory exists and contains `builder-manifest.yaml`
- `phase_id` — three-digit format (e.g., `001`)
- `build_report_path` — file exists in `docs/system/outputs/`

If any parameter is missing or invalid, **halt**: state the specific missing or invalid parameter.

### Step 2: Read Manifest and Resolve Paths

Read `{project_repo_root}/builder-manifest.yaml`.

Validate:
- `version` equals `1`
- `project.slug` is present
- `paths.phases` is present and resolves to an existing directory
- `approval.marker` is present

Resolve:
- Phases directory: `{project_repo_root}/{paths.phases}`

If manifest is invalid: **halt**: "builder-manifest.yaml is invalid: `{specific error}`"

### Step 3: Locate Phase Plan

Search `{project_repo_root}/{paths.phases}` for a file matching `{phase_id}-*.md`.
- Exactly one file must match.
- Zero matches: **halt**: "Phase plan not found for phase `{phase_id}`"
- Multiple matches: **halt**: "Multiple phase plans match phase `{phase_id}` — ambiguous"

### Step 4: Read Build Report

Read the build report at `{build_report_path}`. Confirm the file is readable and non-empty.

If unreadable or empty: **halt** — this triggers V-01 FAIL.

### Step 5: Run Checks V-01 through V-10

Run all 10 checks in order as defined in `docs/implementation/system/verification-contract.md`.

- Evaluate every check, even if prior checks have failed.
- Record the result (PASS or FAIL) and any relevant notes for each check.
- Do not skip checks.
- Do not fix issues encountered — document them.

### Step 6: Determine Verdict

Apply the PASS/FAIL rule from `verification-contract.md`:

- **PASS**: All BLOCKING checks pass.
- **FAIL**: One or more BLOCKING checks fail.

### Step 7: Produce Verification Artifact

Invoke the system iterator to determine the next filename:
- Scan `docs/system/outputs/` for files matching `{today's date}__NN__*.md`
- Increment to produce the next sequence number
- Filename format: `YYYY-MM-DD__NN__verification__<phase-id>-<project-slug>.md`

Write the verification artifact to `docs/system/outputs/` using the required structure from `verification-contract.md`.

The artifact is mandatory — this session may not declare completion until the artifact exists and has been committed.

Stage and commit the verification artifact:

```bash
git add docs/system/outputs/<filename>
git commit -m "docs(system): Add verification report — phase <phase_id> <verdict>"
```

### Step 8: Report Verdict in Chat

State the verdict in chat. Cite the full path to the verification artifact.

If **PASS**: "Verification PASS. Artifact: `docs/system/outputs/<filename>`. Ready for Gatekeeper review."

If **FAIL**: "Verification FAIL. Artifact: `docs/system/outputs/<filename>`. Failed checks: `{list}`. See artifact for remediation path."

---

## Prohibited Actions

The following actions are unconditionally prohibited during any Verification session. No exception.

| # | Prohibited Action | Reason |
|---|-------------------|--------|
| 1 | Modify the build report | Input artifact is read-only |
| 2 | Modify the phase plan | Approved artifact is immutable |
| 3 | Modify any project repo files | Verification is read-only for the project repo |
| 4 | Execute git commands against the project repo | No mutations permitted |
| 5 | Re-run Builder steps | Verification verifies; it does not execute |
| 6 | Produce a PASS verdict under uncertainty | If a check cannot be evaluated, it must be treated as FAIL |
| 7 | Skip a check | All V-01 through V-10 checks must be evaluated |
| 8 | Modify a prior verification artifact | Output artifacts are immutable once written |
| 9 | Push to remote | Requires explicit human instruction per session |
| 10 | Invent the output filename | Filename must be sourced from the system iterator |

---

## Completion Checklist

Before declaring the session complete, verify all items.

**Output compliance**: This session may not stop or declare completion until the verification artifact exists in `docs/system/outputs/` and has been committed. The session must confirm artifact creation explicitly in chat, citing the file path.

- [ ] All three invocation parameters validated
- [ ] Manifest read and all paths resolved
- [ ] Phase plan located (exactly one match)
- [ ] Build report read
- [ ] All checks V-01 through V-10 evaluated
- [ ] Verdict determined: PASS or FAIL
- [ ] Verification artifact written to `docs/system/outputs/` with iterator-sourced filename
- [ ] Verification artifact committed to builder repo
- [ ] Verdict and artifact path confirmed in chat
- [ ] No project repo files modified
- [ ] No git commands executed against project repo

---

## Stop-and-Escalate

If at any point during this session you encounter any of the following, stop immediately and report to the human with specifics:

- Any invocation parameter is missing or ambiguous
- Manifest is invalid or required paths cannot be resolved
- Build report is missing or unreadable
- A check cannot be evaluated due to ambiguity in the phase plan or build report
- A prohibited action appears necessary to continue
- Any situation not explicitly covered by this prompt

When escalating, provide:
1. What went wrong (specific error or ambiguity)
2. Where it happened (step or check number)
3. What you need from the human to proceed
4. What options exist (if any)

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-23 | Initial run-verification prompt — builder-v1 Phase 002 |
