FROM python:3.8

RUN apt-get update



COPY ./requirements.txt ./
COPY ./scripts/Kafka/run.py ./run.py
COPY ./scripts/Kafka/consummer.py ./consummer.py
COPY ./scripts/Kafka/api_secret.properties ./api_secret.properties
COPY ./scripts/Kafka/producer_dockerfile/producer-consummer_entrypoint.sh ./producer-consummer_entrypoint.sh

RUN pip install -r ./requirements.txt
RUN chmod +x ./producer-consummer_entrypoint.sh

CMD ["./producer-consummer_entrypoint.sh"]
