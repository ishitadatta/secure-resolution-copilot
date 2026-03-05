from dataclasses import dataclass


@dataclass
class TriageResult:
    incident_type: str
    severity: str
    confidence: float
    evidence_checklist: list[str]
    recommended_actions: list[dict[str, str]]
    requires_approval: bool


PHISHING_KEYWORDS = {"phish", "suspicious email", "credential", "link", "invoice", "spoof"}
ACCOUNT_COMPROMISE_KEYWORDS = {"impossible travel", "unauthorized login", "mfa", "compromise", "locked out"}
MALWARE_KEYWORDS = {"malware", "ransom", "encrypt", "virus", "endpoint", "trojan"}


def classify_incident(message: str) -> TriageResult:
    lowered = message.lower()

    if any(k in lowered for k in PHISHING_KEYWORDS):
        return TriageResult(
            incident_type="phishing",
            severity="high",
            confidence=0.86,
            evidence_checklist=[
                "Raw email headers captured",
                "Suspicious sender/domain extracted",
                "Clicked URL status captured",
                "Mailbox trace and recipient scope recorded",
            ],
            recommended_actions=[
                {"name": "quarantine_email", "risk_level": "medium"},
                {"name": "block_sender_domain", "risk_level": "high"},
                {"name": "force_password_reset", "risk_level": "high"},
            ],
            requires_approval=True,
        )

    if any(k in lowered for k in ACCOUNT_COMPROMISE_KEYWORDS):
        return TriageResult(
            incident_type="account_compromise",
            severity="critical",
            confidence=0.9,
            evidence_checklist=[
                "Authentication logs linked",
                "MFA challenge status verified",
                "Privileged access scope identified",
                "Token/session inventory captured",
            ],
            recommended_actions=[
                {"name": "disable_user_account", "risk_level": "high"},
                {"name": "revoke_active_tokens", "risk_level": "high"},
                {"name": "force_password_reset", "risk_level": "high"},
            ],
            requires_approval=True,
        )

    if any(k in lowered for k in MALWARE_KEYWORDS):
        return TriageResult(
            incident_type="malware",
            severity="critical",
            confidence=0.83,
            evidence_checklist=[
                "Host indicators captured",
                "EDR alert correlation attached",
                "Lateral movement indicators reviewed",
                "File hash and process tree recorded",
            ],
            recommended_actions=[
                {"name": "isolate_endpoint", "risk_level": "high"},
                {"name": "block_hash", "risk_level": "medium"},
            ],
            requires_approval=True,
        )

    return TriageResult(
        incident_type="other_security",
        severity="medium",
        confidence=0.58,
        evidence_checklist=[
            "Reporter context captured",
            "Affected systems identified",
            "Initial timeline attached",
        ],
        recommended_actions=[
            {"name": "collect_more_context", "risk_level": "low"},
            {"name": "route_to_l2", "risk_level": "low"},
        ],
        requires_approval=False,
    )
