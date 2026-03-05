from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import ActionLog, Ticket


def compute_quality_metrics(db: Session) -> dict[str, float | int]:
    total_tickets = db.query(func.count(Ticket.id)).scalar() or 0
    if total_tickets == 0:
        return {
            "total_tickets": 0,
            "reopen_rate": 0.0,
            "analyst_override_rate": 0.0,
            "recurrence_rate_7d": 0.0,
            "high_risk_containment_rate": 0.0,
        }

    reopened = db.query(func.count(Ticket.id)).filter(Ticket.reopened.is_(True)).scalar() or 0
    overridden = db.query(func.count(Ticket.id)).filter(Ticket.analyst_override.is_(True)).scalar() or 0
    recurring = db.query(func.count(Ticket.id)).filter(Ticket.recurrence_7d.is_(True)).scalar() or 0

    high_risk = db.query(func.count(ActionLog.id)).filter(ActionLog.risk_level == "high").scalar() or 0
    high_risk_executed = (
        db.query(func.count(ActionLog.id))
        .filter(ActionLog.risk_level == "high", ActionLog.executed.is_(True))
        .scalar()
        or 0
    )

    containment_rate = high_risk_executed / high_risk if high_risk else 1.0

    return {
        "total_tickets": total_tickets,
        "reopen_rate": round(reopened / total_tickets, 4),
        "analyst_override_rate": round(overridden / total_tickets, 4),
        "recurrence_rate_7d": round(recurring / total_tickets, 4),
        "high_risk_containment_rate": round(containment_rate, 4),
    }
