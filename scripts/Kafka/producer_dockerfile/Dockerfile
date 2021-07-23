FROM python:3

RUN apt-get update

RUN mkdir ./work

COPY ./requirements.txt ./work
COPY ./scripts/Kafka/run.py ./work/run.py
COPY ./scripts/Kafka/consummer.py ./work/consummer.py
COPY ./scripts/Kafka/api_secret.properties ./work/api_secret.properties

RUN pip install -r ./work/requirements.txt

CMD ["python", "./work/run.py"]
