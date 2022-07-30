import os


def validation(token: str):
    return token == os.getenv("API_TOKEN")
