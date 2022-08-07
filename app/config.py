from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Bingo API"
    mongodb_url: str = ""
    api_token: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
