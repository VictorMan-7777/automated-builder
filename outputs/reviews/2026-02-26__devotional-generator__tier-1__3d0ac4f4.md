# IRB Tier-1 Certification Report

**Outcome:** `CERTIFIED`  
**Project:** devotional-generator  
**Git SHA:** `3d0ac4f4`  
**Timestamp:** 2026-02-26T22:50:53Z  
**Spec:** irb-tier-1 v2.0.0  
**Slug source:** fallback_regex  

## Summary

| Metric | Count |
|--------|-------|
| Total checks | 23 |
| Passed | 20 |
| Failed | 2 |
| Skipped | 1 |
| Blocking failed | 0 |

## Check Results

| ID | Name | Status | Blocking | Evidence | Failure Reason |
|----|------|--------|----------|----------|----------------|
| T1-REPO-001 | git_repo_valid | PASS | yes | yes |  |
| T1-REPO-002 | head_commit_readable | PASS | yes | yes |  |
| T1-REPO-003 | pyproject_toml_present | PASS | no | yes |  |
| T1-REPO-004 | working_tree_clean | PASS | no | yes |  |
| T1-ARCH-001 | src_directory_exists | PASS | yes | yes |  |
| T1-ARCH-002 | required_src_modules_present | PASS | yes | yes |  |
| T1-ARCH-003 | pipeline_entry_point_present | PASS | yes | yes |  |
| T1-ARCH-004 | hard_halt_preserved | PASS | yes | yes |  |
| T1-BUILD-001 | interpreter_available | PASS | no | yes |  |
| T1-BUILD-002 | pytest_exits_zero | PASS | yes | yes |  |
| T1-BUILD-003 | python_test_count_minimum | PASS | yes | yes |  |
| T1-BUILD-004 | zero_test_failures | PASS | yes | yes |  |
| T1-ARTI-001 | grounding_map_store_source | PASS | yes | yes |  |
| T1-ARTI-002 | grounding_map_id_policy_source | PASS | yes | yes |  |
| T1-ARTI-003 | prayer_trace_map_store_source | PASS | yes | yes |  |
| T1-ARTI-004 | prayer_trace_map_id_policy_source | PASS | yes | yes |  |
| T1-ARTI-005 | grounding_store_lifecycle_tests | PASS | yes | yes |  |
| T1-ARTI-006 | prayer_trace_store_lifecycle_tests | PASS | yes | yes |  |
| T1-ARTI-007 | advisory_grounding_maps_runtime_dir | PASS | no | yes |  |
| T1-ARTI-008 | advisory_grounding_maps_runtime_files | **FAIL** | no | yes | 0 files matching '*.json' in data/artifacts/grounding_maps |
| T1-ARTI-009 | advisory_prayer_trace_maps_runtime_dir | **FAIL** | no | yes | Runtime path not found: data/artifacts/prayer_trace_maps (expected on clean clone) |
| T1-ARTI-010 | advisory_prayer_trace_maps_runtime_files | **SKIP** | no | **NO** | dependency 'T1-ARTI-009' did not PASS |
| T1-GUARD-001 | repo_mutation_guard | PASS | yes | yes |  |

## Evidence Detail

### REPO

**T1-REPO-001** — git_repo_valid
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: exit_code=0; stdout='true'

**T1-REPO-002** — head_commit_readable
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: sha=3d0ac4f4...; len=40

**T1-REPO-003** — pyproject_toml_present
- Status: PASS
- Blocking: False
- Evidence collected: True
- Evidence: path=pyproject.toml; exists=True

**T1-REPO-004** — working_tree_clean
- Status: PASS
- Blocking: False
- Evidence collected: True
- Evidence: dirty_files=0

### ARCH

**T1-ARCH-001** — src_directory_exists
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: path=src/; is_dir=True

**T1-ARCH-002** — required_src_modules_present
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: required=9; found=9; missing=[]

**T1-ARCH-003** — pipeline_entry_point_present
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: path=src/api/generation_pipeline.py; exists=True

**T1-ARCH-004** — hard_halt_preserved
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: file=src/api/generation_pipeline.py; total_lines=160; non_comment_lines=157; patterns_checked=6; violations=0

### BUILD

**T1-BUILD-001** — interpreter_available
- Status: PASS
- Blocking: False
- Evidence collected: True
- Evidence: python_exe=$TARGET_ROOT/.venv/bin/python3; python_version=3.9.6; pytest_available=True; pytest_version='pytest 9.0.2'

**T1-BUILD-002** — pytest_exits_zero
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: exit_code=0; stdout_lines=560; cmd=$TARGET_ROOT/.venv/bin/python3 -m pytest tests/...

**T1-BUILD-003** — python_test_count_minimum
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: parsed_count=549; minimum=549; sufficient=True

**T1-BUILD-004** — zero_test_failures
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: failed=0; errors=0

### ARTIFACT

**T1-ARTI-001** — grounding_map_store_source
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: file=src/grounding_store/store.py; symbols_required=['GroundingMapStore']; symbols_missing=[]

**T1-ARTI-002** — grounding_map_id_policy_source
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: file=src/grounding_store/id_policy.py; symbols_required=['create_grounding_map_id']; symbols_missing=[]

**T1-ARTI-003** — prayer_trace_map_store_source
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: file=src/prayer_trace_store/store.py; symbols_required=['PrayerTraceMapStore']; symbols_missing=[]

**T1-ARTI-004** — prayer_trace_map_id_policy_source
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: file=src/prayer_trace_store/id_policy.py; symbols_required=['create_prayer_trace_map_id']; symbols_missing=[]

**T1-ARTI-005** — grounding_store_lifecycle_tests
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: test_path=tests/grounding_store; passed=50; failed=0; sample_tests=['test_returns_list', 'test_returns_validator_assessments', 'test_contains_grounding_map_check', 'test_valid_map_assessment_passes', 'test_only_grounding_check_returned']; source=BUILD-002-cache

**T1-ARTI-006** — prayer_trace_store_lifecycle_tests
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: test_path=tests/prayer_trace_store; passed=22; failed=0; sample_tests=['test_same_input_returns_same_id', 'test_deterministic_across_multiple_calls', 'test_empty_string_is_stable', 'test_different_ids_for_different_inputs', 'test_ordering_matters']; source=BUILD-002-cache

**T1-ARTI-007** — advisory_grounding_maps_runtime_dir
- Status: PASS
- Blocking: False
- Evidence collected: True
- Evidence: path=data/artifacts/grounding_maps; exists=True

**T1-ARTI-008** — advisory_grounding_maps_runtime_files
- Status: FAIL
- Blocking: False
- Evidence collected: True
- Evidence: path=data/artifacts/grounding_maps; pattern=*.json; count=0
- Failure: 0 files matching '*.json' in data/artifacts/grounding_maps

**T1-ARTI-009** — advisory_prayer_trace_maps_runtime_dir
- Status: FAIL
- Blocking: False
- Evidence collected: True
- Evidence: path=data/artifacts/prayer_trace_maps; exists=False
- Failure: Runtime path not found: data/artifacts/prayer_trace_maps (expected on clean clone)

**T1-ARTI-010** — advisory_prayer_trace_maps_runtime_files
- Status: SKIP
- Blocking: False
- Evidence collected: False
- Evidence: 
- Failure: dependency 'T1-ARTI-009' did not PASS

### GUARD

**T1-GUARD-001** — repo_mutation_guard
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: no_delta=True; before=''; after=''
