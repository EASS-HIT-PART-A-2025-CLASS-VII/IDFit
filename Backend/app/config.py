from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# מצביע על תיקיית fastapi_project/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    mongodb_url: str
    db_name: str
    openrouter_api_key: str
    react_app_api_url: str
    resend_api_key: str

    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        env_prefix="",  # <-- חשוב מאוד
    )


settings = Settings()