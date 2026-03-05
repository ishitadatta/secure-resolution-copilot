from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    incident_type: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(16), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="OPEN", nullable=False)
    evidence_checklist: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    analyst_override: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reopened: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_7d: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)

    actions: Mapped[list["ActionLog"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")
    proof: Mapped[Optional["ResolutionProof"]] = relationship(
        back_populates="ticket", cascade="all, delete-orphan", uselist=False
    )


class ActionLog(Base):
    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), nullable=False, index=True)
    action_name: Mapped[str] = mapped_column(String(128), nullable=False)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    approved: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    executed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    result: Mapped[str] = mapped_column(Text, default="PENDING", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    ticket: Mapped[Ticket] = relationship(back_populates="actions")


class ResolutionProof(Base):
    __tablename__ = "resolution_proofs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"), unique=True, nullable=False, index=True)
    evidence_completeness: Mapped[float] = mapped_column(Float, nullable=False)
    counterfactual_impact_score: Mapped[float] = mapped_column(Float, nullable=False)
    action_trace_hash: Mapped[str] = mapped_column(String(128), nullable=False)
    proof_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    ticket: Mapped[Ticket] = relationship(back_populates="proof")
