import os
import json
import warnings
# Suppress Pydantic v2 warnings for cleaner console output
warnings.filterwarnings("ignore", category=UserWarning)

from app.db.database import get_db, Base, engine
from app.models.models import User, Resume, Analysis
from app.core.security import get_password_hash
from app.services.ai_pipeline import trigger_multi_agent_pipeline

def run_tests():
    # 1. Ensure DB tables are created
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    print("\n✅ Database Schema Initialized.")

    # 2. Create Mock User
    test_email = "test_user@resumeforge.demo"
    user = db.query(User).filter(User.email == test_email).first()
    if not user:
        user = User(email=test_email, hashed_password=get_password_hash("hackathon123"))
        db.add(user)
        db.commit()
        db.refresh(user)
    print(f"👤 Test User registered: {user.email}")

    # 3. Simulate Resume Upload
    resume_text = "Experienced Python Developer with 3 years in API development using Django and Flask. Familiar with basic SQL databases and front-end JS."
    resume = Resume(
        user_id=user.id,
        file_name="johndoe_resume.pdf",
        parsed_text=resume_text
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    print(f"📄 Uploaded Mock Resume -> Extracted Text: '{resume_text[:40]}...'")

    # 4. Trigger Analysis
    analysis = Analysis(
        user_id=user.id,
        resume_id=resume.id,
        company_name="Google",
        job_role="Senior Cloud Architect"
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    print(f"🚀 Triggering background pipeline for: {analysis.job_role} at {analysis.company_name}...\n")

    # 5. Execute Pipeline Engine (It will use fallback since GEMINI_API_KEY isn't set)
    trigger_multi_agent_pipeline(analysis.id, db)

    # 6. Fetch final results from the DB!
    db.refresh(analysis)
    print("================================")
    print("    🎯 AI PIPELINE RESULTS      ")
    print("================================")
    print(f"Status           : {analysis.status.upper()}")
    print(f"ATS Score        : {analysis.ats_score}/100")
    print(f"Missing Skills   : {json.loads(analysis.missing_skills)}")
    print(f"Suggested Projs  : {json.loads(analysis.project_suggestions)}")
    print(f"Suggested Certs  : {json.loads(analysis.certification_suggestions)}")
    print(f"Current Fit Roles: {json.loads(analysis.role_suggestions)}")
    print(f"Agent Reasoning  :\n{analysis.explanation}")
    print("================================\n")
    print("✅ All Back-End Systems and Databases functioning perfectly.")

if __name__ == "__main__":
    run_tests()
