from pathlib import Path
import pandas as pd
from fastapi import FastAPI
import joblib
from pydantic import BaseModel

PATH_TO_FAV_MODEL = (Path(__file__) / "../model_fav.joblib").resolve()
print(PATH_TO_FAV_MODEL)

class Features_twitter_fav(BaseModel):
    tweet_quarter: int
    tweet_day_of_the_week: int
    tweet_hour: int
    trend_volume: int
    is_verified: int
    followers_count: int


app = FastAPI()
model = joblib.load(filename=PATH_TO_FAV_MODEL)


@app.post("/predict/")
async def root(features: Features_twitter_fav):
    features_parsed = features.dict()
    df_feats = pd.DataFrame(features_parsed, index=[0])

    popularity_predict = model.predict(X=df_feats.values)
    return {"popularity_score": popularity_predict.tolist()}
