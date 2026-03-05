CREATE TABLE IF NOT EXISTS tickets (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(128) NOT NULL,
  message TEXT NOT NULL,
  incident_type VARCHAR(64) NOT NULL,
  severity VARCHAR(16) NOT NULL,
  confidence FLOAT NOT NULL,
  status VARCHAR(24) NOT NULL DEFAULT 'OPEN',
  evidence_checklist TEXT NOT NULL,
  recommendation TEXT NOT NULL,
  requires_approval BOOLEAN NOT NULL DEFAULT FALSE,
  analyst_override BOOLEAN NOT NULL DEFAULT FALSE,
  reopened BOOLEAN NOT NULL DEFAULT FALSE,
  recurrence_7d BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS action_logs (
  id SERIAL PRIMARY KEY,
  ticket_id INTEGER NOT NULL REFERENCES tickets(id),
  action_name VARCHAR(128) NOT NULL,
  risk_level VARCHAR(16) NOT NULL,
  approved BOOLEAN NOT NULL DEFAULT FALSE,
  executed BOOLEAN NOT NULL DEFAULT FALSE,
  result TEXT NOT NULL DEFAULT 'PENDING',
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS resolution_proofs (
  id SERIAL PRIMARY KEY,
  ticket_id INTEGER NOT NULL UNIQUE REFERENCES tickets(id),
  evidence_completeness FLOAT NOT NULL,
  counterfactual_impact_score FLOAT NOT NULL,
  action_trace_hash VARCHAR(128) NOT NULL,
  proof_hash VARCHAR(128) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
