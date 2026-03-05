from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Ticket

SAMPLES = [
    {
        "user_id": "employee-001",
        "message": "Suspicious email asked me to reset password.",
        "incident_type": "phishing",
        "severity": "high",
        "confidence": 0.84,
        "status": "RESOLVED",
        "evidence_checklist": "headers\nsender\nurl",
        "recommendation": "quarantine_email\nforce_password_reset",
        "requires_approval": True,
        "analyst_override": False,
        "reopened": False,
        "recurrence_7d": False,
    },
    {
        "user_id": "employee-002",
        "message": "I got locked out with unknown login from new country.",
        "incident_type": "account_compromise",
        "severity": "critical",
        "confidence": 0.91,
        "status": "RESOLVED",
        "evidence_checklist": "auth_logs\nsessions",
        "recommendation": "disable_user_account\nrevoke_active_tokens",
        "requires_approval": True,
        "analyst_override": True,
        "reopened": False,
        "recurrence_7d": False,
    },
]


def main() -> None:
    db: Session = SessionLocal()
    try:
        for payload in SAMPLES:
            db.add(Ticket(**payload))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
