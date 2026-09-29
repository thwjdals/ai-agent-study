from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """환경변수 설정. 3주 의존성 주입 연습의 시작점."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="STAGE00_")

    app_name: str = "stage00-python-backend"


@lru_cache
def get_settings() -> Settings:
    return Settings()
