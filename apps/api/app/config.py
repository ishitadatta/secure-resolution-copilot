from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Secure Resolution Copilot"
    api_prefix: str = "/v1"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./secure_resolution.db")


settings = Settings()
