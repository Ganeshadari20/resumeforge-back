from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Resume
from app.schemas.schemas import ResumeResponse
from app.api.dependencies import get_current_user
from app.services.resume_parser import parse_resume_file

router = APIRouter()

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    valid_extensions = ["pdf", "doc", "docx"]
    ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""
    if ext not in valid_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF or DOCX.")
    
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    
    parsed_text = parse_resume_file(file.filename, content)
    if not parsed_text:
         raise HTTPException(status_code=400, detail="Could not extract text from file")
    
    db_resume = Resume(
        user_id=current_user.id,
        file_name=file.filename,
        parsed_text=parsed_text
    )
    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    
    return db_resume
