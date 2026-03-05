from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import QualityMetrics
from ..services.metrics import compute_quality_metrics

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/quality", response_model=QualityMetrics)
def quality_metrics(db: Session = Depends(get_db)) -> QualityMetrics:
    return QualityMetrics(**compute_quality_metrics(db))
