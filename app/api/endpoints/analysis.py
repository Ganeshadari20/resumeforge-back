import json
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Analysis, Resume
from app.schemas.schemas import AnalysisCreate, AnalysisResponse
from app.api.dependencies import get_current_user
from app.services.ai_pipeline import trigger_multi_agent_pipeline

router = APIRouter()

def run_analysis_task(analysis_id: int, db: Session):
    trigger_multi_agent_pipeline(analysis_id, db)

@router.post("/start", response_model=AnalysisResponse)
def start_analysis(
    req: AnalysisCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == req.resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
        
    analysis = Analysis(
        user_id=current_user.id,
        resume_id=resume.id,
        company_name=req.company_name,
        job_role=req.job_role,
        status="pending"
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    
    # Run the pipeline asynchronously
    background_tasks.add_task(run_analysis_task, analysis.id, db)
    
    return analysis

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis_result(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id, Analysis.user_id == current_user.id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    
    return analysis
