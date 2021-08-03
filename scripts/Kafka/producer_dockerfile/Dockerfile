FROM python:3

RUN apt-get update

RUN mkdir -p ./work

COPY ./requirements.txt ./work
COPY ./scripts/Kafka/run.py ./work/run.py
COPY ./scripts/Kafka/consummer.py ./work/consummer.py
COPY ./scripts/Kafka/api_secret.properties ./work/api_secret.properties
COPY ./scripts/Kafka/producer_dockerfile/producer-consummer_entrypoint.sh ./work/producer-consummer_entrypoint.sh

RUN pip install -r ./work/requirements.txt
RUN chmod +x ./work/producer-consummer_entrypoint.sh

CMD ["./work/producer-consummer_entrypoint.sh"]
