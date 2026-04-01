from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Resume Schemas ---
class ResumeResponse(BaseModel):
    id: int
    file_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Analysis Schemas ---
class AnalysisCreate(BaseModel):
    resume_id: int
    company_name: Optional[str] = None
    job_role: Optional[str] = None

class AnalysisResponse(BaseModel):
    id: int
    resume_id: int
    company_name: Optional[str]
    job_role: Optional[str]
    status: str
    ats_score: Optional[int]
    missing_skills: Optional[str]
    project_suggestions: Optional[str]
    certification_suggestions: Optional[str]
    role_suggestions: Optional[str]
    explanation: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class DashboardHistoryResponse(BaseModel):
    total_analyses: int
    recent_analyses: List[AnalysisResponse]
