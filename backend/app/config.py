from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "PulsePredict API"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_minutes: int = 1440
    database_url: str = "sqlite:///./pulsepredict.db"
    model_path: str = "./model.joblib"
    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"

settings = Settings()
