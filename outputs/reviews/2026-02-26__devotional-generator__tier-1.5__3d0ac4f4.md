# IRB Tier-1.5 Certification Report

**Outcome:** `CERTIFIED`  
**Project:** devotional-generator  
**Git SHA:** `3d0ac4f4`  
**Timestamp:** 2026-02-26T23:24:11Z  
**Spec:** irb-tier-1.5 v1.0.0  
**Slug source:** fallback_regex  

## Summary

| Metric | Count |
|--------|-------|
| Total checks | 9 |
| Passed | 7 |
| Failed | 2 |
| Skipped | 0 |
| Blocking failed | 0 |

## Check Results

| ID | Name | Status | Blocking | Evidence | Failure Reason |
|----|------|--------|----------|----------|----------------|
| T15-HYG-001 | tracked_files_no_home_paths | PASS | yes | yes |  |
| T15-HYG-002 | tracked_outputs_allowlist_only | PASS | yes | yes |  |
| T15-HYG-003 | local_state_files_not_tracked | PASS | yes | yes |  |
| T15-SEC-001 | tracked_files_no_private_key_markers | PASS | yes | yes |  |
| T15-SEC-002 | tracked_files_no_secret_like_tokens | PASS | yes | yes |  |
| T15-QA-001 | irb_docs_md040_no_bare_fences | **FAIL** | no | yes | 3 bare ``` fence(s) found in docs/irb/*.md |
| T15-QA-002 | irb_docs_no_absolute_target_examples | **FAIL** | no | yes | Machine-local path substring found in docs/irb/*.md: ['docs/irb/runbook.md:87', 'docs/irb/runbook.md |
| T15-QA-003 | reports_redaction_assertion_present | PASS | no | yes |  |
| T15-GUARD-001 | repo_mutation_guard | PASS | yes | yes |  |

## Evidence Detail

### HYGIENE

**T15-HYG-001** — tracked_files_no_home_paths
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: tracked_files=129; file_list_hash=fdbd056282aa8a6c; forbidden_substrings_count=2; match_count=0; skipped_size=0; skipped_binary=3

**T15-HYG-002** — tracked_outputs_allowlist_only
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: outputs_tracked=0; allowed=0; disallowed=0; allow_globs=['outputs/reviews/.gitkeep', 'outputs/reviews/*.md', 'outputs/reviews/*.json']

**T15-HYG-003** — local_state_files_not_tracked
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: tracked_files=129; denylist={'exact': ['.claude/settings.local.json'], 'dir_components': ['.pytest_cache', '__pycache__', 'node_modules'], 'filenames': ['.DS_Store']}; offending_count=0

### SECURITY

**T15-SEC-001** — tracked_files_no_private_key_markers
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: tracked_files=129; file_list_hash=fdbd056282aa8a6c; markers_checked=6; match_count=0; skipped_size=0; skipped_binary=3

**T15-SEC-002** — tracked_files_no_secret_like_tokens
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: tracked_files=129; file_list_hash=fdbd056282aa8a6c; patterns_checked=5; match_count=0; ignored_count=0; skipped_size=0; skipped_binary=3

### QUALITY

**T15-QA-001** — irb_docs_md040_no_bare_fences
- Status: FAIL
- Blocking: False
- Evidence collected: True
- Evidence: md_files_scanned=4; bare_fence_occurrences=3; locations=['docs/irb/process.md:23', 'docs/irb/process.md:217', 'docs/irb/tier-1-spec.md:126']
- Failure: 3 bare ``` fence(s) found in docs/irb/*.md

**T15-QA-002** — irb_docs_no_absolute_target_examples
- Status: FAIL
- Blocking: False
- Evidence collected: True
- Evidence: md_files_scanned=4; forbidden_count=2; occurrences=6; locations=['docs/irb/runbook.md:87', 'docs/irb/runbook.md:149', 'docs/irb/runbook.md:149', 'docs/irb/tier-1.5-spec.md:58', 'docs/irb/tier-1.5-spec.md:89', 'docs/irb/tier-1.5-spec.md:89']
- Failure: Machine-local path substring found in docs/irb/*.md: ['docs/irb/runbook.md:87', 'docs/irb/runbook.md:149', 'docs/irb/runbook.md:149', 'docs/irb/tier-1.5-spec.md:58', 'docs/irb/tier-1.5-spec.md:89', 'docs/irb/tier-1.5-spec.md:89']

**T15-QA-003** — reports_redaction_assertion_present
- Status: PASS
- Blocking: False
- Evidence collected: True
- Evidence: required_tokens=['_sanitize_paths', 'build_md_report', 'build_json_report', 'builder_root']; missing=[]; reporter_size_bytes=7582

### GUARD

**T15-GUARD-001** — repo_mutation_guard
- Status: PASS
- Blocking: True
- Evidence collected: True
- Evidence: no_delta=True; before=''; after=''
