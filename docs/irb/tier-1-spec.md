# IRB Tier-1 Specification — Structural, Build, and Lifecycle Integrity

**Spec ID:** irb-tier-1
**Version:** 2.0.0
**Machine-readable source:** [specs/irb/tier-1-spec.yaml](../../specs/irb/tier-1-spec.yaml)

---

## Purpose

Tier-1 certifies that a target repository meets minimum structural, build, and
artifact lifecycle requirements before any higher-tier review is attempted.
Evidence-gated: each check must collect concrete evidence before evaluating its
pass condition. "No artifact, no credit."

---

## Blocking vs Advisory

- **Blocking (yes):** A FAIL on this check sets outcome to FAILED. The runner
  continues to evaluate all remaining checks for complete evidence, but the
  outcome is locked to FAILED.
- **Advisory (no):** A FAIL is recorded with full evidence but does not affect
  the CERTIFIED/FAILED outcome. FAIL on advisory checks is expected on clean clones.

---

## Evidence-Gated Rule

Every check must collect evidence before evaluating its pass condition. If
evidence collection itself fails (command not found, file unreadable, subprocess
error, missing cache), the check status is FAIL with `evidence_collected: false`.
No evidence = automatic FAIL regardless of pass condition.

---

## Spec Config

| Key | Value | Purpose |
|-----|-------|---------|
| `minimum_passed_tests` | 549 | Minimum Python test count for BUILD-003 |

---

## Check Catalog (23 checks)

### REPO (4 checks)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T1-REPO-001 | git_repo_valid | **yes** | `git rev-parse --is-inside-work-tree` | exit code 0 |
| T1-REPO-002 | head_commit_readable | **yes** | `git log -1 --format=%H` | 40-char SHA |
| T1-REPO-003 | pyproject_toml_present | no | path exists | `pyproject.toml` present |
| T1-REPO-004 | working_tree_clean | no (advisory) | `git status --porcelain` | empty output |

### ARCH (4 checks)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T1-ARCH-001 | src_directory_exists | **yes** | path is_dir | `src/` is a directory |
| T1-ARCH-002 | required_src_modules_present | **yes** | `src/` listing | all 9 modules present¹ |
| T1-ARCH-003 | pipeline_entry_point_present | **yes** | path exists | `src/api/generation_pipeline.py` |
| T1-ARCH-004 | hard_halt_preserved | **yes** | file content (R4) | 6 forbidden patterns absent² |

¹ Required: `api, generation, validation, models, grounding_store, prayer_trace_store, llm, rag, interfaces`

² R4 precision: per forbidden symbol, separate import-statement and instantiation-call
regexes. Comment lines excluded (`lstrip().startswith("#")`). Forbidden symbols:
`LLMExpositionGenerator`, `LLMPrayerGenerator`, `DeterministicRealSectionGenerator`.

### BUILD (4 checks)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T1-BUILD-001 | interpreter_available | no (advisory, R2) | `<python> -m pytest --version` | pytest importable |
| T1-BUILD-002 | pytest_exits_zero | **yes** | subprocess `-v --tb=short`; output cached (TWEAK 1) | exit code 0 |
| T1-BUILD-003 | python_test_count_minimum | **yes** | cached stdout parse (R3) | `N passed` ≥ 549 |
| T1-BUILD-004 | zero_test_failures | **yes** | cached stdout parse | 0 failures + 0 errors |

BUILD-003 and BUILD-004 use `depends_on: T1-BUILD-002` to share the cached pytest output.
If BUILD-002 fails, BUILD-003 and BUILD-004 are SKIP.

### ARTIFACT — Code Lifecycle (6 checks, all blocking)

R1 revision: lifecycle invariants verified via (a) source file + required symbols,
and (b) test suite output from the cached BUILD-002 run. No runtime artifact presence required.

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T1-ARTI-001 | grounding_map_store_source | **yes** | `src/grounding_store/store.py` | contains `GroundingMapStore` |
| T1-ARTI-002 | grounding_map_id_policy_source | **yes** | `src/grounding_store/id_policy.py` | contains `create_grounding_map_id` |
| T1-ARTI-003 | prayer_trace_map_store_source | **yes** | `src/prayer_trace_store/store.py` | contains `PrayerTraceMapStore` |
| T1-ARTI-004 | prayer_trace_map_id_policy_source | **yes** | `src/prayer_trace_store/id_policy.py` | contains `create_prayer_trace_map_id` |
| T1-ARTI-005 | grounding_store_lifecycle_tests | **yes** | cached BUILD-002 output filtered for `tests/grounding_store` (TWEAK 1) | all matching tests PASSED, count ≥ 1 |
| T1-ARTI-006 | prayer_trace_store_lifecycle_tests | **yes** | cached BUILD-002 output filtered for `tests/prayer_trace_store` (TWEAK 1) | all matching tests PASSED, count ≥ 1 |

ARTI-005 depends_on ARTI-001; ARTI-006 depends_on ARTI-003.

### ARTIFACT — Advisory Runtime Presence (4 checks, non-blocking)

Explicitly labeled advisory. FAIL here is expected on a clean clone.
These checks do not constitute lifecycle invariants.

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T1-ARTI-007 | advisory_grounding_maps_runtime_dir | no | path exists | `data/artifacts/grounding_maps/` |
| T1-ARTI-008 | advisory_grounding_maps_runtime_files | no | file count | ≥ 1 `.json` file |
| T1-ARTI-009 | advisory_prayer_trace_maps_runtime_dir | no | path exists | `data/artifacts/prayer_trace_maps/` |
| T1-ARTI-010 | advisory_prayer_trace_maps_runtime_files | no | file count | ≥ 1 `.json` file |

ARTI-008 depends_on ARTI-007; ARTI-010 depends_on ARTI-009.

### GUARD (1 check, blocking)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T1-GUARD-001 | repo_mutation_guard | **yes** | before/after `git status --porcelain` (R5, TWEAK 2) | no delta |

The executor captures pre-run status before the check loop and post-run status in a
`finally` block. Guard always runs with both values available.

---

## Report Filename Policy

```text
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-<N>__<git-sha-8>.md
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-<N>__<git-sha-8>.json
```

- `project-slug`: `pyproject.toml project.name` (fallback: target dir basename)
- `git-sha-8`: first 8 chars of target HEAD SHA (from T1-REPO-002)
- Date: runner execution date (UTC)

---

## Outcome Determination

| Outcome | Condition |
|---------|-----------|
| `CERTIFIED` | Zero blocking checks have status FAIL |
| `FAILED` | One or more blocking checks have status FAIL |
| `ERROR` | Runner crashed before producing a report (exit code 2) |

## Dependency Handling

Checks with `depends_on: <ID>` are marked SKIP if the dependency did not PASS.
SKIP is recorded in the report. SKIP of a non-blocking check does not affect outcome.
