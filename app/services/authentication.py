import os


def validate_token(token: str):
    return token == os.getenv("API_TOKEN")
