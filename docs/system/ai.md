# AI Delegation & Review Policy

<!-- STATUS: DRAFT -->

## Purpose

This document defines **who is allowed to execute work**, **who must verify it**, and **how weaknesses in AI systems are mitigated**.

It exists to:
- prevent silent delegation decisions
- make AI use explicit, reviewable, and reversible
- ensure humans retain final authority over scope, intent, and approval

This document is **canonical**. Other planning artifacts must reference it, not restate it.

---

## Core Principles

1. **Every task has an Executor and a Verifier**
2. **If an AI executes, verification is mandatory**
3. **Product intent, scope, and approval are always human-owned**
4. **AI is a tool, not an authority**

---

## Approved Executors

### Human Executors
- **Human: Barbara** — primary decision-maker and final approver
- **Human: Professional Code Reviewer** — external reviewer for high-risk changes

### AI Executors
- **AI: Claude Code**
- **AI: Open Claw**
- **AI: Codex**
- **AI: Other (explicitly named and justified)**

Unlisted AIs may not execute work without being added here.

---

## Executor Capability & Risk Matrix

### Claude Code
**Strengths**
- Strong reasoning and planning alignment
- Good at refactors, test-driven changes, spec adherence

**Weaknesses**
- Can overreach scope if boundaries are unclear
- May optimize structure beyond intent

**Mitigations**
- Narrow scope and explicit acceptance criteria
- Require: diff summary + list of files touched
- Verifier: Human (Barbara)
- Optional second-pass review by another AI for consistency

---

### Open Claw
**Strengths**
- Persistent, automatable, good for repeatable bounded tasks

**Weaknesses**
- Persistence amplifies mistakes
- Higher risk of unintended side effects

**Mitigations**
- Use only for small, reversible tasks
- Explicit dry-run expectations
- Always require human verification
- Professional reviewer recommended for high-risk steps

---

### Codex
**Strengths**
- Strong at mechanical implementation
- Can run commands, tests, and report results
- Good “implementation worker”

**Weaknesses**
- May pass tests while violating product intent
- Less sensitive to business or domain nuance

**Mitigations**
- Treat as execution-only, not decision-making
- Require: commands run + results + diff summary
- Verifier: Human (Barbara)
- Optional Claude review for spec alignment

---

### Human: Barbara
**Strengths**
- Full context, product intent, and authority

**Weaknesses**
- Time and energy constraints

**Mitigations**
- Delegate drafts and mechanical work to AI
- Reserve approvals and high-risk decisions for human review

---

### Professional Code Reviewer
**Strengths**
- Independent, experienced, risk-focused

**Weaknesses**
- Cost and limited domain context

**Mitigations**
- Provide identity.md + PRD excerpt
- Give explicit review focus areas

---

## Task Assignment Rules

- Every task MUST specify:
  - **Executor**
  - **Verifier**
- If Executor is AI → Verifier MUST be named
- If Verifier is AI → add a human spot-check trigger
- High-risk tasks require stronger verification (see below)

---

## Human-Only Task Categories

The following may NOT be executed by AI without explicit exception approval:
- Authentication and authorization logic
- Billing, payments, subscriptions
- Destructive database operations
- Production configuration or secrets
- Security-sensitive logic

---

## High-Risk Triggers (Require Elevated Review)

Any task touching:
- auth / permissions
- database schema or migrations
- financial or billing logic
- broad refactors across modules

**Required mitigation:**  
Human verification, and professional review if complexity is high.

---

## Verification Expectations (AI-Executed Work)

At minimum, AI executors must provide:
1. What changed
2. Why it changed
3. Files touched
4. Commands/tests run and results
5. Known uncertainties or assumptions

---

## Approval Semantics

- Draft artifacts may be revised freely
- Approved artifacts require proposed revisions only
- Approval is signaled **only** by:

```html
<!-- STATUS: APPROVED -->
