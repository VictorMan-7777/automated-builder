# Gateway (Gatekeeper) Requirements

**Version**: 1.0
**Last Updated**: 2026-02-05

---

## Overview

This document defines requirements and criteria for the **Gatekeeper** role in the Planner-Builder-Gatekeeper workflow.

**Gatekeeper Role**: Review and approve/reject work before it proceeds to the next stage.

---

## Gatekeeper Responsibilities

### Core Duties

1. **Review**: Examine planning artifacts or implementation outputs
2. **Validate**: Verify compliance with requirements and standards
3. **Decide**: Make explicit APPROVE/REVISE/REJECT decision
4. **Document**: Record rationale for decisions
5. **Ensure Quality**: Maintain project standards and integrity

### Not Responsible For

- Implementation (that's Builder's role)
- Planning (that's Planner's role)
- Fixing issues (recommends fixes, doesn't make them)

---

## Review Types

### Planning Review

**When**: After Planner produces planning artifacts

**Reviews**:
- PRD completeness and clarity
- Roadmap feasibility
- Phase plans detail and accuracy
- Commit points properly identified
- Rollback procedures documented
- Verification steps concrete

**Outcome**: Plan APPROVED for Builder / REVISE / REJECT

---

### Phase Review

**When**: After Builder completes a phase

**Reviews**:
- All steps executed per plan
- All commit points completed
- Verification results valid
- Acceptance criteria met
- Quality standards maintained
- No scope creep

**Outcome**: Phase APPROVED / REVISE / REJECT

---

### Milestone Review

**When**: After major milestone completion

**Reviews**:
- All phases in milestone complete
- Integration successful
- No blocking issues
- Documentation current
- Ready for next milestone

**Outcome**: Milestone APPROVED / REVISE / REJECT

---

## Approval Criteria

### Planning Approval

Plan is **APPROVED** if:

- [ ] All required documents present (index, PRD, roadmap, iteration-log, phases)
- [ ] Project slug follows conventions (lowercase, hyphen-separated)
- [ ] Files in correct location (`docs/projects/<slug>/`)
- [ ] Phase files numbered correctly (001, 002, etc.)
- [ ] Commit points explicitly identified in each phase
- [ ] Acceptance criteria are measurable (not vague)
- [ ] Rollback procedures documented (per-step and per-commit)
- [ ] Verification steps include commands and expected output
- [ ] Gatekeeper checklists present in phase plans
- [ ] No ambiguous or unclear language
- [ ] Scope is reasonable for MVP
- [ ] Dependencies identified
- [ ] Risks acknowledged

---

### Phase Approval

Phase is **APPROVED** if:

- [ ] All steps from plan executed
- [ ] All commit points completed in order
- [ ] Git history matches planned commits
- [ ] Working tree clean (no uncommitted changes)
- [ ] All verification commands passed
- [ ] Acceptance criteria met (100%)
- [ ] No scope creep (only planned work done)
- [ ] Quality standards maintained
- [ ] Documentation updated/accurate
- [ ] Rollback tested or documented confidence in it
- [ ] No known blocking issues
- [ ] Gatekeeper checklist completed honestly

---

### Milestone Approval

Milestone is **APPROVED** if:

- [ ] All constituent phases approved
- [ ] Integration between phases successful
- [ ] End-to-end workflow tested (if applicable)
- [ ] All acceptance criteria for milestone met
- [ ] Documentation complete and accurate
- [ ] Git history clean and traceable
- [ ] No technical debt introduced (or documented)
- [ ] Ready to proceed to next milestone

---

## Rejection Criteria

### When to REJECT

Reject if:

- **Critical errors**: Fundamental flaws that can't be fixed with minor revisions
- **Wrong approach**: Solution doesn't match requirements
- **Insufficient quality**: Multiple quality issues across the board
- **Security concerns**: Vulnerabilities or unsafe practices
- **Cannot verify**: Verification steps fail repeatedly

### When to Request REVISE

Revise if:

- **Minor gaps**: Missing documentation or steps
- **Unclear language**: Ambiguity that needs clarification
- **Incomplete**: Some criteria met, others not
- **Quality issues**: Fixable problems (typos, formatting, etc.)
- **Verification failures**: Specific steps failed but fixable

---

## Review Process

### Step-by-Step Review

1. **Read Plan/Output**: Thoroughly review all artifacts
2. **Check Structure**: Verify file locations, naming, organization
3. **Validate Completeness**: All required sections/steps present
4. **Test Verification**: Run verification commands (if applicable)
5. **Assess Quality**: Check clarity, accuracy, thoroughness
6. **Check Compliance**: Verify against planning.md, builder.md, CLAUDE.md
7. **Fill Checklist**: Complete gatekeeper checklist honestly
8. **Make Decision**: APPROVE / REVISE / REJECT
9. **Document Rationale**: Explain decision clearly
10. **Communicate**: Return to Planner/Builder with feedback

---

## Decision Documentation

### Approval Template

```markdown
## Gatekeeper Decision

**Reviewer**: [Name/ID]
**Date**: [YYYY-MM-DD]
**Review Type**: [Planning / Phase / Milestone]
**Artifact**: [Plan name / Phase ID]

**Decision**: ✅ APPROVED

**Rationale**:
- All criteria met
- Quality standards maintained
- Ready to proceed

**Notes**: [Any observations or recommendations]

**Signature**: [Initials/Sign-off]
```

### Revision Request Template

```markdown
## Gatekeeper Decision

**Reviewer**: [Name/ID]
**Date**: [YYYY-MM-DD]
**Review Type**: [Planning / Phase / Milestone]
**Artifact**: [Plan name / Phase ID]

**Decision**: 🔄 REVISE

**Issues Found**:
1. [Specific issue with location/reference]
2. [Specific issue with location/reference]
3. [Specific issue with location/reference]

**Required Changes**:
1. [Exact change needed]
2. [Exact change needed]
3. [Exact change needed]

**Recommendation**: [Guidance for fixing]

**Signature**: [Initials/Sign-off]
```

### Rejection Template

```markdown
## Gatekeeper Decision

**Reviewer**: [Name/ID]
**Date**: [YYYY-MM-DD]
**Review Type**: [Planning / Phase / Milestone]
**Artifact**: [Plan name / Phase ID]

**Decision**: ❌ REJECT

**Critical Issues**:
1. [Fundamental problem]
2. [Fundamental problem]

**Rationale**: [Why rejection vs revision]

**Recommendation**: [Suggested next steps]

**Signature**: [Initials/Sign-off]
```

---

## Quality Standards

### Planning Quality

Plans must be:
- **Clear**: No ambiguity, anyone can understand
- **Complete**: All required sections present
- **Concrete**: Specific instructions, not vague guidance
- **Consistent**: Naming, formatting, style uniform
- **Correct**: No errors, inaccuracies, or omissions

### Implementation Quality

Implementations must be:
- **Faithful**: Matches approved plan
- **Functional**: Works as intended
- **Verified**: All checks passed
- **Clean**: No clutter, unused files, or cruft
- **Documented**: Changes reflected in docs

---

## Independence

Gatekeeper MUST be independent from Planner/Builder.

### Independence Requirements

- Different entity/agent/human from Planner/Builder
- No bias toward approving own work
- Objective review based on criteria
- Willing to reject/revise when needed

### Self-Review Exception

If Gatekeeper and Builder are same entity:
- Be extra critical
- Use checklists rigorously
- Document honestly
- Seek external review for major decisions

---

## Escalation

When Gatekeeper is uncertain or blocked.

### When to Escalate

- Criteria unclear or conflicting
- Major deviation from plan needed
- Security or risk concerns
- Disagreement with Planner/Builder
- Outside expertise needed

### Escalation Process

1. Document the issue clearly
2. Tag for human review
3. Provide recommendation
4. Wait for guidance
5. Proceed based on decision

---

## Iteration Support

Gatekeeper supports iterative improvement.

### Iterative Review

- First iterations may be REVISE more often
- Later iterations should improve
- Document patterns of issues for learning
- Update criteria if needed (with approval)

### Feedback Quality

Provide actionable feedback:
- Specific (not "improve quality")
- Located (file, line, section)
- Actionable (how to fix)
- Prioritized (critical vs nice-to-have)

---

## Gatekeeper Checklist Template

Use this template for all reviews:

```markdown
# Gatekeeper Checklist

**Artifact**: _______________
**Reviewer**: _______________
**Date**: _______________

---

## Structural Review

- [ ] Files in correct location
- [ ] Naming conventions followed
- [ ] All required documents present
- [ ] Organization logical and clear

## Completeness Review

- [ ] All required sections included
- [ ] No placeholders or TODOs (unless acceptable)
- [ ] Commit points identified (if applicable)
- [ ] Acceptance criteria defined
- [ ] Rollback procedures documented

## Quality Review

- [ ] Language is clear and unambiguous
- [ ] Instructions are concrete and actionable
- [ ] Examples provided where helpful
- [ ] No spelling or grammar errors
- [ ] Formatting consistent

## Compliance Review

- [ ] Complies with planning.md (if planning)
- [ ] Complies with builder.md (if implementation)
- [ ] Complies with CLAUDE.md conventions
- [ ] Complies with approved plan (if implementation)

## Verification Review

- [ ] Verification steps included
- [ ] Expected outputs documented
- [ ] Actual results match expected (if tested)

---

## Decision

**Overall Assessment**:
- [ ] **APPROVED** - Ready to proceed
- [ ] **REVISE** - Changes needed (see notes)
- [ ] **REJECT** - Fundamental issues

**Critical Issues** (if any):
1. _______________
2. _______________

**Recommendations**:
1. _______________
2. _______________

**Reviewer Signature**: _______________
**Approval Date**: _______________
```

---

## Constraints Summary

Gatekeeper MUST:
1. ✅ Review all artifacts thoroughly
2. ✅ Use objective criteria
3. ✅ Make explicit decisions
4. ✅ Document rationale
5. ✅ Provide actionable feedback
6. ✅ Maintain independence
7. ✅ Support quality standards

Gatekeeper MUST NOT:
1. ❌ Approve without review
2. ❌ Implement fixes themselves
3. ❌ Skip checklist items
4. ❌ Give vague feedback
5. ❌ Approve non-compliant work

---

## Compliance

All Gatekeeper reviews MUST comply with:

1. This document (gateway.md)
2. Project conventions (CLAUDE.md)
3. Planning requirements (planning.md) - for planning reviews
4. Builder requirements (builder.md) - for implementation reviews

---

## TBD: Future Sections

The following sections will be added in future versions:

### Security Review Criteria
- TBD: Specific security checks
- TBD: Vulnerability assessment process
- TBD: Risk scoring methodology

### Performance Criteria
- TBD: Performance benchmarks
- TBD: Scalability considerations
- TBD: Resource usage thresholds

### Integration Testing
- TBD: Integration test requirements
- TBD: Cross-phase compatibility checks
- TBD: End-to-end workflow validation

---

## Document History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-05 | Initial gatekeeper requirements |
