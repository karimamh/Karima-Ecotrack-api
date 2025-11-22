u200B
u200B
 
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EcoTrack"
    api_prefix: str = "/api/v1"
    jwt_secret: str = Field("change-me", alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str = Field("sqlite:///./data/ecotrack.db", alias="DATABASE_URL")
    cors_origins: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    openaq_api_key: str | None = Field(default=None, alias="OPENAQ_API_KEY")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore", populate_by_name=True)


settings = Settings()



