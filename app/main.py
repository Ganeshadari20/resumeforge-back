from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import Base, engine
from app.api.endpoints import auth, resume, analysis, dashboard, metadata

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for RESUMEFORGE.AI Multi-Agent Recruitment Pipeline"
)

# Add CORS Middleware to allow requests from your Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for Hackathon MVP
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "RESUMEFORGE.AI Backend is running smoothly."}

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(resume.router, prefix=f"{settings.API_V1_STR}/resume", tags=["Resume"])
app.include_router(analysis.router, prefix=f"{settings.API_V1_STR}/analysis", tags=["Analysis"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_STR}/dashboard", tags=["Dashboard"])
app.include_router(metadata.router, prefix=f"{settings.API_V1_STR}/metadata", tags=["Metadata"])

