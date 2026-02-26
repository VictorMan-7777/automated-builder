# IRB Tier-1.5 Specification — Repo Hygiene & Competition Safety

**Spec ID:** irb-tier-1.5
**Version:** 1.0.0
**Machine-readable source:** [specs/irb/tier-1.5-spec.yaml](../../specs/irb/tier-1.5-spec.yaml)

---

## Purpose

Tier-1.5 is a hygiene and safety gate — not a style tool. It certifies that the
target repository does not commit machine-local paths, secret-like tokens, or
ephemeral local-state files that would leak environment-specific state or credentials
into version control. Tier-1.5 runs after Tier-1 CERTIFIED; it is a prerequisite
for competition submission.

---

## Blocking vs Advisory

- **Blocking (yes):** A FAIL locks outcome to FAILED.
- **Advisory (no):** A FAIL is recorded with evidence but does not affect CERTIFIED/FAILED.

---

## Evidence-Gated Rule

Every check must collect concrete evidence before evaluating its pass condition. If
evidence collection fails the check is FAIL with `evidence_collected: false`.
**No artifact, no credit.**

---

## Spec Config

| Key | Purpose |
|-----|---------|
| `allow_tracked_outputs_globs` | Glob patterns for permitted tracked files under `outputs/` |
| `forbid_tracked_path_substrings` | Substrings that must not appear in tracked file content |
| `forbid_tracked_secret_markers` | PEM-style private key header strings |
| `forbid_tracked_secret_regexes` | Conservative regex set for secret-like token patterns |

---

## Check Catalog (10 checks)

### HYGIENE (3 checks, all blocking)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T15-HYG-001 | tracked_files_no_home_paths | **yes** | git ls-files + content scan | No forbidden substring in any tracked file |
| T15-HYG-002 | tracked_outputs_allowlist_only | **yes** | git ls-files filtered to `outputs/` | All outputs/ files match allowlist globs |
| T15-HYG-003 | local_state_files_not_tracked | **yes** | git ls-files + denylist match | No local-state file is tracked |

**T15-HYG-001 scan rules:**
- Files > 2 MB are skipped (counted in evidence).
- Files with a NUL byte in the first 4 KB are treated as binary and skipped.
- Matches are redacted in evidence: `/Users/<name>/` → `/Users/<redacted>/`.
- Evidence includes: forbidden substrings list, total match_count, skipped_size, skipped_binary counts, up to 5 samples `path:line:snippet`.

**T15-HYG-002 allowlist (from config):**
- `outputs/reviews/.gitkeep`
- `outputs/reviews/*.md`
- `outputs/reviews/*.json`

**T15-HYG-003 denylist (hardcoded):**
- `.claude/settings.local.json`
- `.DS_Store`
- `node_modules/**`
- `.pytest_cache/**`
- `__pycache__/**`

### SECURITY (2 checks, all blocking)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T15-SEC-001 | tracked_files_no_private_key_markers | **yes** | content scan | No PEM private key marker in any tracked file |
| T15-SEC-002 | tracked_files_no_secret_like_tokens | **yes** | content scan + regex | No secret-like token regex matches (after false-positive filter) |

**T15-SEC-002 false-positive filter:** If the matched line contains `<redacted>`,
`EXAMPLE`, or `fake` (case-insensitive), the match is ignored and counted as
`ignored_count` in evidence.

### QUALITY (3 checks, all advisory)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T15-QA-001 | irb_docs_md040_no_bare_fences | no | file scan | No bare ` ``` ` fence in `docs/irb/*.md` |
| T15-QA-002 | irb_docs_no_absolute_target_examples | no | file scan | No `/Users/` or `C:\Users\` in `docs/irb/*.md` |
| T15-QA-003 | reports_redaction_assertion_present | no | file content | `_sanitize_paths` present in reporter.py; build functions accept path args |

T15-QA-003 `depends_on: T15-HYG-001` — only meaningful if home-path scan is available.

### GUARD (1 check, blocking, always last)

| ID | Name | Blocking | Evidence | Pass Condition |
|----|------|----------|----------|----------------|
| T15-GUARD-001 | repo_mutation_guard | **yes** | before/after git status --porcelain | no delta |

`depends_on: T15-HYG-002` — guard check always runs regardless (executor ensures finally).

---

## Dependency Graph

```text
T15-QA-003   depends_on T15-HYG-001
T15-GUARD-001 depends_on T15-HYG-002  (noted in spec; guard always runs via executor finally)
```

---

## Report Filename Policy

```text
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-1.5__<git-sha-8>.md
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-1.5__<git-sha-8>.json
```

---

## Outcome Determination

| Outcome | Condition |
|---------|-----------|
| `CERTIFIED` | Zero blocking checks have status FAIL |
| `FAILED` | One or more blocking checks have status FAIL |
| `ERROR` | Runner crashed before producing a report (exit code 2) |
