from sqlalchemy.orm import Session

from ..models import ActionLog, Ticket


def create_action_logs(db: Session, ticket: Ticket, recommended_actions: list[dict[str, str]]) -> None:
    for action in recommended_actions:
        db.add(
            ActionLog(
                ticket_id=ticket.id,
                action_name=action["name"],
                risk_level=action["risk_level"],
                approved=False,
                executed=False,
                result="PENDING_APPROVAL" if action["risk_level"] == "high" else "READY",
            )
        )
    db.commit()
