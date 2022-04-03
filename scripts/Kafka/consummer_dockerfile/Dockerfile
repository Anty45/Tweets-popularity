FROM python:3.8

RUN apt-get update

RUN rm -rf ./ressources && \
    mkdir ./ressources && \
    rm -rf ./work && \
    mkdir ./work && \
    pip install openpyxl

COPY ./requirements.txt ./work
COPY ./scripts/ressources/messages.csv ./ressources/messages.csv
COPY ./scripts/ressources/messages_ex.xlsx ./ressources/messages_ex.xlsx
COPY ./scripts/Kafka/consummer.py ./work/consummer.py
COPY ./scripts/Kafka/api_secret.properties ./work/api_secret.properties
COPY ./scripts/Kafka/consummer_dockerfile/consummer_entrypoint.sh ./work/consummer_entrypoint.sh

RUN pip install -r ./work/requirements.txt
RUN chmod +x ./work/consummer_entrypoint.sh

CMD ["./work/consummer_entrypoint.sh"]
