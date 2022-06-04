from fastapi import FastAPI

app = FastAPI()

@app.get("/predict")
async def root():
    return {"popularity_score": 0}
