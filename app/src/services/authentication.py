from src.config import get_settings


def validate_token(token: str):
    return token == get_settings().api_token
