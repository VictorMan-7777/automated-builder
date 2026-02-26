# IRB Runner — Operator Runbook

**Version:** 1.1.0 (Tier 1 spec v2.0.0 · Tier 1.5 spec v1.0.0)
**Framework:** IRB v1 (Integration Review Board)
**Tiers covered:** 1, 1.5

---

## Prerequisites

1. **Python 3.11+** available in PATH (for `tomllib` stdlib support).
2. **PyYAML** installed in the Python interpreter running the runner:
   ```bash
   pip install pyyaml
   # or: python3 -m pip install pyyaml
   ```
3. **Target repository** has tests runnable via `python3 -m pytest tests/`.
   - The runner uses its own interpreter (`sys.executable`) by default.
   - To use a specific interpreter (e.g., target's venv): `--python /path/to/python`.
4. **automated-builder** root must contain `specs/irb/tier-1-spec.yaml`.

---

## Primary Invocation (R6 — Builder CLI)

```bash
# From automated-builder root:
scripts/irb/builder review --tier 1 \
  --target /path/to/devotional-generator-system-a
```

`scripts/irb/builder` is a thin bash wrapper using `exec` to preserve exit codes.

---

## Direct Python Invocation

```bash
python3 scripts/irb/runner.py review --tier 1 \
  --target /path/to/devotional-generator-system-a
```

---

## All Flags

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--tier N` | yes | — | Tier number (1) |
| `--target PATH` | yes | — | Absolute path to target repo |
| `--output-dir PATH` | no | `outputs/reviews/` | Where to write .md + .json reports |
| `--spec PATH` | no | `specs/irb/tier-<N>-spec.yaml` | Custom spec YAML path |
| `--python PATH` | no | `sys.executable` | Interpreter for running pytest |
| `--pytest-args "..."` | no | `""` | Extra pytest arguments |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | `CERTIFIED` — all blocking checks pass |
| 1 | `FAILED` — at least one blocking check failed |
| 2 | `ERROR` — runner crashed before producing a report |

```bash
scripts/irb/builder review --tier 1 --target /path/to/repo
echo "Exit: $?"
```

---

## Expected Output Files

```text
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-1__<sha8>.md
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-1__<sha8>.json
```

**Example for devotional-generator at HEAD 96656218:**
```text
outputs/reviews/2026-02-26__devotional-generator__tier-1__96656218.md
outputs/reviews/2026-02-26__devotional-generator__tier-1__96656218.json
```

**Path redaction:** Report artifacts have machine-local absolute paths replaced with
portable tokens (`$TARGET_ROOT`, `$BUILDER_ROOT`, `/Users/<redacted>/`). Reports are
safe to commit to the repository.

---

## Expected Outcome — devotional-generator-system-a (Phase 013 CP1)

Given the target at Phase 013 CP1 (clean clone, no committed artifact JSON):

| Check | Expected | Notes |
|-------|----------|-------|
| T1-REPO-001..004 | PASS | Git valid, clean |
| T1-ARCH-001..004 | PASS | src/ modules present, hard-halt preserved |
| T1-BUILD-001 | PASS | pytest available |
| T1-BUILD-002..004 | PASS | 549+ tests, 0 failures |
| T1-ARTI-001..004 | PASS | Store + ID policy sources present |
| T1-ARTI-005..006 | PASS | grounding_store + prayer_trace_store tests pass |
| T1-ARTI-007 | PASS | `data/artifacts/grounding_maps/` exists |
| T1-ARTI-008 | FAIL (advisory) | 0 JSON files in grounding_maps/ (runtime only) |
| T1-ARTI-009 | FAIL (advisory) | `prayer_trace_maps/` dir absent (runtime only) |
| T1-ARTI-010 | SKIP | depends on ARTI-009 which fails |
| T1-GUARD-001 | PASS | No repo modifications |
| **Outcome** | **CERTIFIED** | blocking_failed = 0 |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'yaml'`**
→ `pip install pyyaml`

**`ERROR: target path does not exist`**
→ Verify `--target` is an absolute path to an existing directory.

**`ERROR: spec not found`**
→ Confirm `specs/irb/tier-1-spec.yaml` exists in automated-builder.

**T1-BUILD-002 FAIL: pytest exits non-zero**
→ Run `.venv/bin/pytest tests/ -q` in the target repo manually and inspect failures.

**T1-ARTI-005 or T1-ARTI-006 FAIL: "No pytest output found for test path"**
→ BUILD-002 must have run with `-v` flag. Confirm BUILD-002 passed first.
→ If overriding with `--pytest-args`, ensure it does not suppress verbose output.

**T1-GUARD-001 FAIL: "Target repo was modified during check run"**
→ Investigate which files changed. The runner should not modify the target.
→ Likely cause: pytest created `__pycache__` in an unexpected location, or
  a test wrote to the repo (should not happen in a well-behaved test suite).

---

---

## Tier 1.5 — Repo Hygiene & Competition Safety

Tier 1.5 enforces hygiene and safety invariants on the **target repository's
version-controlled content**. It does not run the test suite.

### What Tier 1.5 checks

| Category | Check | Blocking |
|----------|-------|----------|
| hygiene | No tracked file contains `/Users/` or `C:\Users\` | yes |
| hygiene | All tracked `outputs/` files match the allowlist | yes |
| hygiene | No local-state files (`.DS_Store`, `__pycache__/`, etc.) are tracked | yes |
| security | No tracked file contains a PEM private-key header | yes |
| security | No tracked file contains a secret-like token (GitHub PAT, AWS key, etc.) | yes |
| quality | No bare ` ``` ` fences in `docs/irb/*.md` (MD040) | advisory |
| quality | No machine-local example paths in `docs/irb/*.md` | advisory |
| quality | Reporter path-redaction wiring is present in `reporter.py` | advisory |
| guard | Repo not modified during check run | yes |

### Invocation

```bash
# From automated-builder root:
scripts/irb/builder review --tier 1.5 \
  --target /path/to/devotional-generator-system-a
```

The `--python` flag is not used by Tier 1.5 (no test suite is run).

### Expected output files

```text
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-1.5__<sha8>.md
outputs/reviews/YYYY-MM-DD__<project-slug>__tier-1.5__<sha8>.json
```

### Expected outcome — devotional-generator-system-a (clean clone)

| Check | Expected | Notes |
|-------|----------|-------|
| T15-HYG-001 | PASS | No home paths in tracked files |
| T15-HYG-002 | PASS | outputs/ files match allowlist |
| T15-HYG-003 | PASS | No local-state files tracked |
| T15-SEC-001 | PASS | No private key markers |
| T15-SEC-002 | PASS | No secret-like tokens |
| T15-QA-001 | PASS | No bare fences in docs/irb/*.md |
| T15-QA-002 | PASS | No machine-local paths in docs |
| T15-QA-003 | PASS | Redaction wiring present in reporter.py |
| T15-GUARD-001 | PASS | No repo mutation |
| **Outcome** | **CERTIFIED** | blocking_failed = 0 |

### Troubleshooting

**T15-HYG-001 FAIL: home path in tracked file**
→ Find matches in evidence_summary (samples show redacted path:line:snippet).
→ Replace literal paths with `$TARGET_ROOT` or a relative path before committing.

**T15-HYG-002 FAIL: disallowed outputs/ file tracked**
→ Check which files under `outputs/` are not in the allowlist.
→ Either add to allowlist (if intentional) or remove from git tracking.

**T15-SEC-002 FAIL: secret-like token**
→ Check evidence for which regex matched and which file.
→ Remove or rotate the credential. Use `<redacted>` placeholders in docs.

---

## HALT Reminder

The runner halts after producing its report. It does not:
- Initiate any next-phase action
- Modify the target repository
- Spawn any additional process

After the report is written, control returns to the operator. Outcome
must be reviewed by a human before any downstream action is taken.

**Do NOT begin Phase 014 or Phase 015 work without explicit operator authorization.**
