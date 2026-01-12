from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Bingo API"
    api_token: str = ""
    mongodb_url: str

    class Config:
        env_file = ".env"
        secrets_dir = '/var/run'


@lru_cache
def get_settings() -> Settings:
    return Settings()
