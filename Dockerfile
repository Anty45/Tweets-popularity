FROM openjdk:11.0.10-jre-buster

RUN apt-get update && \
    apt-get install -y curl

ENV KAFKA_VERSION 2.8.0
ENV SCALA_VERSION 2.12

RUN  mkdir /tmp/kafka
RUN  curl "https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_${SCALA_VERSION}-${KAFKA_VERSION}.tgz" \
    -o /tmp/kafka/kafka.tgz
RUN mkdir /kafka && cd /kafka && \
    tar -xvzf /tmp/kafka/kafka.tgz --strip 1

COPY /Kafka/kafka_entry_point/start-kafka.sh  /usr/bin
RUN chmod +x  /usr/bin/start-kafka.sh

CMD ["start-kafka.sh" ]