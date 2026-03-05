from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Ticket
from ..schemas import ActionRecommendation, IntakeRequest, IntakeResponse
from ..services.playbooks import create_action_logs
from ..services.triage import classify_incident

router = APIRouter(prefix="/chat", tags=["intake"])


@router.post("/intake", response_model=IntakeResponse)
def intake(payload: IntakeRequest, db: Session = Depends(get_db)) -> IntakeResponse:
    triage = classify_incident(payload.message)
    ticket = Ticket(
        user_id=payload.user_id,
        message=payload.message,
        incident_type=triage.incident_type,
        severity=triage.severity,
        confidence=triage.confidence,
        evidence_checklist="\n".join(triage.evidence_checklist),
        recommendation="\n".join([f"{a['name']} ({a['risk_level']})" for a in triage.recommended_actions]),
        requires_approval=triage.requires_approval,
        status="OPEN",
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    create_action_logs(db, ticket, triage.recommended_actions)

    return IntakeResponse(
        ticket_id=ticket.id,
        incident_type=triage.incident_type,
        severity=triage.severity,
        confidence=triage.confidence,
        evidence_checklist=triage.evidence_checklist,
        recommended_actions=[ActionRecommendation(**a) for a in triage.recommended_actions],
        requires_approval=triage.requires_approval,
    )
