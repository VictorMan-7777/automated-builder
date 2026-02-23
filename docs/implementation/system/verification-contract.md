# Verification Stage Contract

**Version**: 1.0
**Last Updated**: 2026-02-23
**Status**: Draft
**Phase**: builder-v1 Phase 002

---

## Purpose

The Verification stage is the third stage in the Builder v1 lifecycle (Planner → Builder → Verification). Its role is to validate that Builder output satisfies the phase plan's acceptance criteria and produce a deterministic PASS or FAIL verdict.

**What Verification is**:
- An artifact validation stage that evaluates committed Builder outputs against the phase plan
- A quality gate that produces a PASS or FAIL verdict with evidence
- The source of the handoff artifact that triggers Gatekeeper review (on PASS) or Builder re-execution (on FAIL)

**What Verification is NOT**:
- Not a human review — Verification is a structured, automated-equivalent checklist evaluation
- Not a code review — Verification checks for completeness, structure, and governance compliance, not subjective quality
- Not a re-execution of the build — Verification reads committed artifacts; it does not re-run Builder steps
- Not a fixer — Verification documents findings and produces a verdict; it does not correct errors

---

## Inputs

### Input 1: `builder-manifest.yaml`

| Field | Value |
|-------|-------|
| Source | `{project_repo_root}/builder-manifest.yaml` |
| Required fields | `version`, `project.slug`, `paths.phases`, `approval.marker` |
| On-missing | HALT: "builder-manifest.yaml not found at `{project_repo_root}`" |
| On-invalid | HALT: "builder-manifest.yaml invalid: `{specific error}`" |

### Input 2: Phase Plan File

| Field | Value |
|-------|-------|
| Source | `{project_repo_root}/{paths.phases}/{phase_id}-*.md` |
| Required fields | Approval marker, commit points (CP1, CP2, ...) with acceptance criteria |
| On-missing | HALT: "Phase plan not found for phase `{phase_id}`" |
| On-multiple-matches | HALT: "Multiple phase plans match phase `{phase_id}` — ambiguous" |

### Input 3: Build Report

| Field | Value |
|-------|-------|
| Source | `{build_report_path}` (provided at invocation) |
| Required fields | Build context, commits made, verification results, recommendation |
| On-missing | HALT — triggers V-01 FAIL verdict |
| On-invalid-path | HALT: "Build report not found at `{build_report_path}`" |

### Input 4: Committed Artifacts

| Field | Value |
|-------|-------|
| Source | Files declared in the phase plan's commit points; verified via `git log` |
| Required fields | Each file declared in a CP must exist in the repository |
| On-missing | Triggers V-04 FAIL — document specific missing file |

---

## Verification Checks

All checks are evaluated in order. Evaluation continues through all checks even after a BLOCKING failure — the full picture is documented in the verdict.

| Check ID | Description | How to Evaluate | Pass Condition | Fail Condition | Severity |
|----------|-------------|----------------|----------------|----------------|----------|
| V-01 | Build report exists in `docs/system/outputs/` | Confirm file at `{build_report_path}` exists and is readable | File found and readable | File not found or unreadable | BLOCKING |
| V-02 | Build report filename follows canonical format `YYYY-MM-DD__NN__builder__<description>.md` | Parse the filename of the build report | Filename matches pattern | Filename does not match pattern | BLOCKING |
| V-03 | All declared commit points appear as commits in git log | For each CP in the phase plan, search `git log --oneline` for the declared commit message | All CP commit messages found | Any CP commit message missing | BLOCKING |
| V-04 | All files declared in commit points exist in the repository | For each file listed in each CP's `files-to-stage`, confirm it exists on disk | All declared files found | Any declared file missing | BLOCKING |
| V-05 | Build report includes required sections | Grep build report for: Build Context, Commits Made, Verification Results, Recommendation | All required sections present | Any required section missing | BLOCKING |
| V-06 | Build report's recommendation field is APPROVE or REVISE | Read the Recommendation section of the build report | Value is exactly `APPROVE` or `REVISE` | Value is absent, ambiguous, or any other value | BLOCKING |
| V-07 | No stub indicators found in newly created files | Grep all files declared in the phase plan's commit points for: `TODO`, `FIXME`, `HACK`, `placeholder`, `lorem ipsum`, `TBD` | Zero matches across all declared files | One or more matches found | BLOCKING |
| V-08 | No governance files modified during Builder session | Compare `git diff <pre-build-commit>...<post-build-commit> -- <governance-file>` for each file in the CP-2 default governance list | All governance files show no diff | Any governance file shows changes | BLOCKING |
| V-09 | Build report cites commit hashes that exist in git log | For each commit hash in the build report's Commits Made section, verify it exists in `git log` | All cited hashes found in git log | Any cited hash not found | ADVISORY |
| V-10 | Verification artifact does not duplicate a prior Verification artifact for this phase | Search `docs/system/outputs/` for existing verification artifacts for this phase and build report | No prior verification artifact for this exact build report | A prior verification artifact already covers this build report | BLOCKING |

---

## PASS/FAIL Determination

**Rule**:

- **PASS**: All BLOCKING checks (V-01 through V-08, V-10) evaluate to PASS. ADVISORY findings (V-09) are documented but do not change the verdict.
- **FAIL**: One or more BLOCKING checks evaluate to FAIL. The verdict is FAIL regardless of how many checks pass.
- **No partial verdicts**: There is no PASS-WITH-RESERVATIONS or conditional PASS. If all BLOCKING checks pass, the verdict is PASS. If any BLOCKING check fails, the verdict is FAIL.

The verdict MUST be stated as a single word on the `**Verdict**` line of the verification artifact: either `PASS` or `FAIL`. No other value is permitted.

---

## Output Artifact

Every Verification session MUST produce a verification artifact written to `docs/system/outputs/` in the builder repo. The artifact is mandatory — a session that completes without writing this artifact has failed.

The filename follows the canonical format: `YYYY-MM-DD__NN__verification__<description>.md`

The filename MUST be supplied by the system iterator (scanning existing files in `docs/system/outputs/` to determine the next sequence number for the current date). The Verification session must not invent the filename.

### Required Structure

```
# Verification Report — <project-slug> Phase <NNN>

**Date**: YYYY-MM-DD
**Phase**: <phase-id>
**Build Report Reference**: <filename of the build report>
**Verdict**: PASS | FAIL

---

## Check Results

| Check ID | Description | Result | Notes |
|----------|-------------|--------|-------|
| V-01     | ...         | PASS   |       |
| V-02     | ...         | PASS   |       |
| V-03     | ...         | PASS   |       |
| V-04     | ...         | PASS   |       |
| V-05     | ...         | PASS   |       |
| V-06     | ...         | PASS   |       |
| V-07     | ...         | PASS   |       |
| V-08     | ...         | PASS   |       |
| V-09     | ...         | PASS   |       |
| V-10     | ...         | PASS   |       |

---

## Findings

[ADVISORY findings, if any. If none: "No advisory findings."]

---

## Next Step

[If PASS: "Ready for Gatekeeper review. Handoff: this verification artifact."]
[If FAIL: List each failed BLOCKING check. For each: what failed, what evidence was found,
and whether the fix requires Builder re-execution (implementation error) or Planner revision
(plan error). State explicitly which checks must pass in the re-verification.]
```

---

## Iteration Protocol

When Verification produces a FAIL verdict:

1. The FAIL artifact is written and committed. It is immutable — it is never modified after writing.
2. The human reviews the FAIL artifact and decides: fix via Builder re-execution, or escalate to plan revision.
3. If Builder re-execution: the Builder is re-invoked. It addresses only the failed checks. It produces a new build report (new sequence number; new artifact).
4. A new Verification session is invoked against the new build report. It produces a new verification artifact (new sequence number). The previous FAIL artifact is preserved.
5. If the same BLOCKING check fails three consecutive times across separate Verification sessions, the session MUST halt and escalate to the human. Do not initiate a fourth iteration automatically. Document the pattern of recurring failure and request explicit human decision on path forward (plan revision, scope change, or abandonment).

---

## Immutability Rule

A verification artifact is immutable once written and committed. If Verification is re-run after a FAIL + correction, a new artifact with the next sequence number is produced. The previous FAIL artifact remains committed and unchanged.

Re-running Verification against the same build report (same `build_report_path`) is prohibited unless the working tree has changed since the prior verification run. Check V-10 enforces this.

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-23 | Initial verification stage contract — builder-v1 Phase 002 |
