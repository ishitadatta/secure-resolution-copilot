from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ActionLog, Ticket
from ..schemas import ApprovalRequest, ExecuteRequest, TicketSummary
from ..services.mock_actions import execute_mock_action

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("", response_model=list[TicketSummary])
def list_tickets(db: Session = Depends(get_db)) -> list[TicketSummary]:
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    return [
        TicketSummary(
            id=t.id,
            user_id=t.user_id,
            incident_type=t.incident_type,
            severity=t.severity,
            confidence=t.confidence,
            status=t.status,
            requires_approval=t.requires_approval,
        )
        for t in tickets
    ]


@router.post("/{ticket_id}/approve")
def approve_actions(ticket_id: int, payload: ApprovalRequest, db: Session = Depends(get_db)) -> dict[str, str]:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if payload.override_recommendation:
        ticket.analyst_override = True

    high_risk_actions = (
        db.query(ActionLog).filter(ActionLog.ticket_id == ticket_id, ActionLog.risk_level == "high").all()
    )

    for action in high_risk_actions:
        action.approved = payload.approve
        action.result = "APPROVED" if payload.approve else "REJECTED"

    ticket.status = "APPROVED" if payload.approve else "REJECTED"
    db.commit()

    return {"status": ticket.status, "analyst": payload.analyst}


@router.post("/{ticket_id}/execute")
def execute_actions(ticket_id: int, payload: ExecuteRequest, db: Session = Depends(get_db)) -> dict[str, object]:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    actions = db.query(ActionLog).filter(ActionLog.ticket_id == ticket_id).all()
    if not actions:
        raise HTTPException(status_code=400, detail="No actions found")

    executed_results: list[str] = []
    for action in actions:
        if action.risk_level == "high" and not action.approved:
            raise HTTPException(status_code=403, detail=f"High-risk action {action.action_name} requires approval")
        action.executed = True
        action.result = execute_mock_action(action.action_name, ticket_id)
        executed_results.append(action.result)

    ticket.status = "RESOLVED"
    db.commit()

    return {"status": ticket.status, "ticket_id": ticket_id, "executed_by": payload.analyst, "results": executed_results}
