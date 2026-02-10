# Output Artifact: Repository Scan Results

**Date**: 2026-02-10  
**Context**: Repository Governance and Workflow Rules Scan  
**Description**: This file summarizes the findings from the targeted scan focused on system rules and governance within the repository.

---

### Summary of Findings
1. **Canonical Files Identified**: A list of files defining the workflow and governance rules:
   - `docs/system/README.md`
   - `docs/system/access.md`
   - `docs/system/pending-items.md`
   - `docs/system/outputs/README.md`
   - `prompts/planner/planner-base.md`
   - `prompts/builder/builder-base.md`
   - `prompts/gatekeeper/gatekeeper-checklist.md`

2. **Derived Artifacts**: Output files saved in `docs/system/outputs/` must adhere to the rules defined in `docs/system/outputs/README.md` regarding long output captures.

3. **Execution Model Overview**:
   - The plan-first methodology allows detailed planning before execution (from `README.md`).
   - Approval by a Gatekeeper is required at each phase, ensuring governance adherence (from `gateway.md` and `planning.md`).
   - Explicit commit points and acceptance criteria must be followed (from `builder.md` and `gateway.md`).
   - Output artifacts are required to document progress and validate alignment with plans (from `outputs/README.md`).
   - Rollback strategies are mandatory for builders (from `builder.md`).
   - Decisions are required to be documented explicitly, involving APPROVE/REVISE/REJECT with the Gatekeeper (from `gatekeeper/gatekeeper-checklist.md`).

---

### Additional Information
- See files reviewed in the scan:
  - `docs/system/README.md`
  - `docs/system/access.md`
  - `docs/system/pending-items.md`
  - `docs/system/outputs/README.md`
  - `prompts/planner/planner-base.md`
  - `prompts/builder/builder-base.md`
  - `prompts/gatekeeper/gatekeeper-checklist.md`

---

**End of Output Artifact**