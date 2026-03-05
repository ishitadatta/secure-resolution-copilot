# Architecture

## Goals
- Prioritize incident resolution quality over simple deflection.
- Enforce guardrails for high-risk remediations.
- Preserve auditable action logs for enterprise governance.

## Components
- `apps/web`: browser-based intake UI for synthetic employee reports.
- `apps/api`: FastAPI backend for triage, ticketing, approvals, execution, and metrics.
- `apps/api` scenario lab module: assurance proof engine, counterfactual simulator, and safety challenge checks.
- `db`: relational schema for tickets and action logs.
- `evals`: benchmark scenarios for regression and quality checks.

## Workflow
1. User submits a security issue in chat-style intake.
2. Triage engine predicts incident type/severity, confidence, and action plan.
3. Ticket record is created and enriched with evidence checklist + recommendations.
4. High-risk actions remain blocked until analyst approval.
5. Approved actions execute through mock connectors with deterministic logs.
6. Resolution Proof endpoint computes evidence completeness, counterfactual impact, and proof hash.
7. Quality metrics endpoint computes reopen, override, recurrence, and containment indicators.

## Guardrail model
- Confidence gating: low-confidence incidents are routed for manual review.
- Approval gating: high-risk remediations require explicit analyst decision.
- Immutable event log: every action is preserved for post-incident audit.
- Adversarial challenge endpoint: detects obvious policy-bypass prompt patterns.
- Counterfactual simulator: estimates residual risk when specific remediations are removed.
