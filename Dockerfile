FROM python:3.8

WORKDIR /app

COPY scripts/api/ ./
COPY scripts/api/ressources_api/model_fav.joblib ./ressources_api/model_fav.joblib
COPY scripts/api/requirements_api.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
ENTRYPOINT python -m uvicorn twitter_model_api:app --host 0.0.0.0 --port 80
