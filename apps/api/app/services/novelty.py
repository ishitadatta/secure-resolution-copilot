import hashlib
import json

from sqlalchemy.orm import Session

from ..models import ActionLog, ResolutionProof, Ticket


EXPECTED_EVIDENCE_ITEMS = {
    "phishing": 4,
    "account_compromise": 4,
    "malware": 4,
    "other_security": 3,
}

ACTION_IMPACT_WEIGHTS = {
    "disable_user_account": 0.35,
    "revoke_active_tokens": 0.3,
    "force_password_reset": 0.2,
    "block_sender_domain": 0.15,
    "quarantine_email": 0.1,
    "isolate_endpoint": 0.4,
    "block_hash": 0.15,
    "collect_more_context": 0.05,
    "route_to_l2": 0.05,
}

PROMPT_ATTACK_SIGNALS = {
    "ignore previous instructions": "prompt_override_attempt",
    "reveal system prompt": "prompt_exfiltration_attempt",
    "disable security": "safety_bypass_attempt",
    "run without approval": "approval_bypass_attempt",
    "just trust me": "social_engineering_pressure",
}


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_or_update_resolution_proof(db: Session, ticket: Ticket) -> ResolutionProof:
    actions = db.query(ActionLog).filter(ActionLog.ticket_id == ticket.id).order_by(ActionLog.id.asc()).all()
    executed_actions = [a for a in actions if a.executed]

    checklist_count = len([line for line in ticket.evidence_checklist.split("\n") if line.strip()])
    expected = EXPECTED_EVIDENCE_ITEMS.get(ticket.incident_type, 3)
    evidence_completeness = min(checklist_count / expected, 1.0)

    impact_sum = sum(ACTION_IMPACT_WEIGHTS.get(a.action_name, 0.05) for a in executed_actions)
    counterfactual_impact_score = min(impact_sum, 1.0)

    trace_payload = [
        {
            "action": a.action_name,
            "risk": a.risk_level,
            "approved": a.approved,
            "executed": a.executed,
            "result": a.result,
        }
        for a in actions
    ]
    action_trace_hash = _sha256(json.dumps(trace_payload, sort_keys=True))

    proof_payload = {
        "ticket_id": ticket.id,
        "incident_type": ticket.incident_type,
        "severity": ticket.severity,
        "confidence": ticket.confidence,
        "evidence_completeness": round(evidence_completeness, 4),
        "counterfactual_impact_score": round(counterfactual_impact_score, 4),
        "action_trace_hash": action_trace_hash,
    }
    proof_hash = _sha256(json.dumps(proof_payload, sort_keys=True))

    proof = db.query(ResolutionProof).filter(ResolutionProof.ticket_id == ticket.id).first()
    if not proof:
        proof = ResolutionProof(
            ticket_id=ticket.id,
            evidence_completeness=evidence_completeness,
            counterfactual_impact_score=counterfactual_impact_score,
            action_trace_hash=action_trace_hash,
            proof_hash=proof_hash,
        )
        db.add(proof)
    else:
        proof.evidence_completeness = evidence_completeness
        proof.counterfactual_impact_score = counterfactual_impact_score
        proof.action_trace_hash = action_trace_hash
        proof.proof_hash = proof_hash

    db.commit()
    db.refresh(proof)
    return proof


def counterfactual_simulation(db: Session, ticket: Ticket, dropped_actions: list[str]) -> dict[str, object]:
    actions = db.query(ActionLog).filter(ActionLog.ticket_id == ticket.id).all()
    executed_actions = [a for a in actions if a.executed and a.action_name not in dropped_actions]

    retained_impact = sum(ACTION_IMPACT_WEIGHTS.get(a.action_name, 0.05) for a in executed_actions)
    residual_risk_score = round(max(0.0, 1.0 - min(retained_impact, 1.0)), 4)

    high_risk_dropped = [a for a in actions if a.action_name in dropped_actions and a.risk_level == "high"]
    blast_radius_score = round(min(1.0, 0.25 * len(high_risk_dropped)), 4)

    minimum_actions = []
    if ticket.incident_type == "phishing":
        minimum_actions = ["quarantine_email", "force_password_reset"]
    elif ticket.incident_type == "account_compromise":
        minimum_actions = ["disable_user_account", "revoke_active_tokens"]
    elif ticket.incident_type == "malware":
        minimum_actions = ["isolate_endpoint", "block_hash"]
    else:
        minimum_actions = ["collect_more_context", "route_to_l2"]

    return {
        "ticket_id": ticket.id,
        "dropped_actions": dropped_actions,
        "residual_risk_score": residual_risk_score,
        "blast_radius_score": blast_radius_score,
        "recommended_minimum_actions": minimum_actions,
    }


def run_safety_challenge(message: str) -> dict[str, object]:
    lowered = message.lower()
    signals = [label for pattern, label in PROMPT_ATTACK_SIGNALS.items() if pattern in lowered]
    blocked = len(signals) > 0

    if blocked:
        secure_response = (
            "Request blocked by policy. I cannot bypass approval or expose protected instructions. "
            "Please continue via approved SOC workflow."
        )
    else:
        secure_response = (
            "No direct bypass signals detected. Continue with standard intake, evidence capture, and approval gates."
        )

    return {
        "blocked": blocked,
        "risk_signals": signals,
        "secure_response_template": secure_response,
    }
