from app.config import settings


def validate_token(token: str):
    return token == settings.api_token
