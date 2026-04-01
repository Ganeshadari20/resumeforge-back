from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Analysis
from app.schemas.schemas import DashboardHistoryResponse
from app.api.dependencies import get_current_user

router = APIRouter()

@router.get("/history", response_model=DashboardHistoryResponse)
def get_dashboard_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analyses = db.query(Analysis).filter(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc()).all()
    
    return {
        "total_analyses": len(analyses),
        "recent_analyses": analyses
    }
