from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ResolutionProof, Ticket
from ..schemas import (
    CounterfactualRequest,
    CounterfactualResponse,
    ResolutionProofResponse,
    SafetyChallengeRequest,
    SafetyChallengeResponse,
)
from ..services.novelty import build_or_update_resolution_proof, counterfactual_simulation, run_safety_challenge

router = APIRouter(prefix="/novelty", tags=["novelty"])


@router.post("/proof/{ticket_id}", response_model=ResolutionProofResponse)
def create_proof(ticket_id: int, db: Session = Depends(get_db)) -> ResolutionProofResponse:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.status != "RESOLVED":
        raise HTTPException(status_code=400, detail="Ticket must be RESOLVED before generating proof")

    proof = build_or_update_resolution_proof(db, ticket)
    return ResolutionProofResponse(
        ticket_id=ticket.id,
        evidence_completeness=round(proof.evidence_completeness, 4),
        counterfactual_impact_score=round(proof.counterfactual_impact_score, 4),
        action_trace_hash=proof.action_trace_hash,
        proof_hash=proof.proof_hash,
    )


@router.get("/proof/{ticket_id}", response_model=ResolutionProofResponse)
def get_proof(ticket_id: int, db: Session = Depends(get_db)) -> ResolutionProofResponse:
    proof = db.query(ResolutionProof).filter(ResolutionProof.ticket_id == ticket_id).first()
    if not proof:
        raise HTTPException(status_code=404, detail="Proof not found")

    return ResolutionProofResponse(
        ticket_id=ticket_id,
        evidence_completeness=round(proof.evidence_completeness, 4),
        counterfactual_impact_score=round(proof.counterfactual_impact_score, 4),
        action_trace_hash=proof.action_trace_hash,
        proof_hash=proof.proof_hash,
    )


@router.post("/simulate/{ticket_id}", response_model=CounterfactualResponse)
def simulate_counterfactual(
    ticket_id: int, payload: CounterfactualRequest, db: Session = Depends(get_db)
) -> CounterfactualResponse:
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.status != "RESOLVED":
        raise HTTPException(status_code=400, detail="Ticket must be RESOLVED before simulation")

    result = counterfactual_simulation(db, ticket, payload.dropped_actions)
    return CounterfactualResponse(**result)


@router.post("/challenge/safety", response_model=SafetyChallengeResponse)
def safety_challenge(payload: SafetyChallengeRequest) -> SafetyChallengeResponse:
    result = run_safety_challenge(payload.message)
    return SafetyChallengeResponse(**result)
