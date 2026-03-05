from pydantic import BaseModel, Field


class IntakeRequest(BaseModel):
    user_id: str = Field(min_length=2, max_length=128)
    message: str = Field(min_length=4)


class ActionRecommendation(BaseModel):
    name: str
    risk_level: str


class IntakeResponse(BaseModel):
    ticket_id: int
    incident_type: str
    severity: str
    confidence: float
    evidence_checklist: list[str]
    recommended_actions: list[ActionRecommendation]
    requires_approval: bool


class ApprovalRequest(BaseModel):
    analyst: str = Field(min_length=2)
    approve: bool = True
    override_recommendation: bool = False


class ExecuteRequest(BaseModel):
    analyst: str = Field(min_length=2)


class TicketSummary(BaseModel):
    id: int
    user_id: str
    incident_type: str
    severity: str
    confidence: float
    status: str
    requires_approval: bool


class QualityMetrics(BaseModel):
    total_tickets: int
    reopen_rate: float
    analyst_override_rate: float
    recurrence_rate_7d: float
    high_risk_containment_rate: float


class ResolutionProofResponse(BaseModel):
    ticket_id: int
    evidence_completeness: float
    counterfactual_impact_score: float
    action_trace_hash: str
    proof_hash: str


class CounterfactualRequest(BaseModel):
    dropped_actions: list[str] = []


class CounterfactualResponse(BaseModel):
    ticket_id: int
    dropped_actions: list[str]
    residual_risk_score: float
    blast_radius_score: float
    recommended_minimum_actions: list[str]


class SafetyChallengeRequest(BaseModel):
    message: str = Field(min_length=4)


class SafetyChallengeResponse(BaseModel):
    blocked: bool
    risk_signals: list[str]
    secure_response_template: str


class DemoScenario(BaseModel):
    id: str
    title: str
    description: str
    message: str
    expected_incident_type: str


class DemoRunResponse(BaseModel):
    scenario_id: str
    ticket_id: int
    incident_type: str
    severity: str
    confidence: float
    status: str
    mission_report: dict[str, object]
