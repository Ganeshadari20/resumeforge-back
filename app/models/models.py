from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    resumes = relationship("Resume", back_populates="owner")
    analyses = relationship("Analysis", back_populates="owner")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_name = Column(String, nullable=False)
    parsed_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="resumes")
    analyses = relationship("Analysis", back_populates="resume")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    
    company_name = Column(String, nullable=True)
    job_role = Column(String, nullable=True)
    status = Column(String, default="pending")  # pending, completed, failed
    
    # Analysis Results (stored as JSON strings for simplicity in SQLite/Postgres across free tiers)
    ats_score = Column(Integer, nullable=True)
    missing_skills = Column(Text, nullable=True)
    project_suggestions = Column(Text, nullable=True)
    certification_suggestions = Column(Text, nullable=True)
    role_suggestions = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
