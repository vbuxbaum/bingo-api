from fastapi import FastAPI

from app.routes import cards_route, rounds_route

app = FastAPI()

app.include_router(cards_route.router)
app.include_router(rounds_route.router)


@app.get("/")
def home():
    """Welcome message to the API"""
    return {
        "message": "Let's play! Visit route /docs for documentation."
    }
