# Secure Resolution Copilot

Open-source fullstack reference project for **enterprise cybersecurity incident resolution quality**.

It simulates:
- Moveworks-style conversational intake
- ServiceNow-style incident lifecycle
- AI triage + evidence checklist + remediation recommendations
- Human approval gating for high-risk actions
- Resolution-quality metrics (reopen rate, analyst override rate, recurrence, containment)

## Why this project exists
Most enterprise assistants optimize for deflection. This project optimizes for **correct, safe, auditable incident resolution**.

## Features
- FastAPI backend with incident triage and playbook orchestration
- Approval gate for high-risk remediations (`disable_user_account`, `revoke_active_tokens`, `isolate_endpoint`)
- Mock connector execution logs for deterministic offline demos
- Web intake UI for end-to-end flow testing
- Eval harness for scenario pass rate checks

## Monorepo layout
- `apps/api`: backend API and tests
- `apps/web`: static web app for intake simulation
- `docs`: architecture and guardrails
- `db`: SQL schema
- `evals`: test scenarios for triage quality
- `scripts`: synthetic seed scripts
- `resources.md`: deep scan of relevant primary resources

## Quickstart (local, no enterprise access required)

### 1. Run API
```bash
cd secure-resolution-copilot/apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 2. Run Web UI
```bash
cd secure-resolution-copilot/apps/web
python -m http.server 3000
```
Open: `http://localhost:3000`

### 3. Example API flow
```bash
curl -s -X POST http://localhost:8000/v1/chat/intake \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"employee-001","message":"Suspicious email asked for credentials"}' | python -m json.tool
```

Then approve + execute high-risk actions:
```bash
curl -s -X POST http://localhost:8000/v1/tickets/1/approve \
  -H 'Content-Type: application/json' \
  -d '{"analyst":"soc-1","approve":true,"override_recommendation":false}' | python -m json.tool

curl -s -X POST http://localhost:8000/v1/tickets/1/execute \
  -H 'Content-Type: application/json' \
  -d '{"analyst":"soc-1"}' | python -m json.tool
```

### 4. Run evals
```bash
curl -s -X POST http://localhost:8000/v1/evals/run | python -m json.tool
```

## Docker deployment
```bash
cd secure-resolution-copilot
docker compose up --build
```

## Quality metrics endpoint
`GET /v1/metrics/quality`

Returned fields:
- `reopen_rate`
- `analyst_override_rate`
- `recurrence_rate_7d`
- `high_risk_containment_rate`

## What to build next
- Real ServiceNow connector (Table API + Incident API)
- Real chat connector (Slack/Teams bot)
- LLM function-calling with policy checks and confidence calibration
- RBAC + SSO + immutable audit signing
- Benchmark suite with larger phishing/account-compromise corpora

## License
MIT
