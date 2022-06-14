from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hello World"}


@app.get("/card")
async def get_card():
    return {
        "card_type": "jk_classic",
        "card_columns": [[1, 5, 3, 7, 9], [1, 5, 3, 7, 9], [1, 5, 3, 7, 9]],
    }
