from fastapi import FastAPI

from .routes import cards_route

app = FastAPI()


@app.get("/")
async def home():
    """Welcome message to the API"""
    return {
        "message": "Let's play! Visit route /card for a random classic card."
    }


app.include_router(cards_route.router)
