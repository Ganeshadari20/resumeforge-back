from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RESUMEFORGE.AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # IMPORTANT: Set SECRET_KEY as an environment variable in production. Never hardcode this.
    SECRET_KEY: str = "change-this-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # API Keys
    GEMINI_API_KEY: str = ""

    # Database (Default to SQLite for simple local dev, can be replaced with Supabase connection string)
    DATABASE_URL: str = "sqlite:///./resumeforge.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
