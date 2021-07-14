from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from json import loads

if __name__ == '__main__':

    consumer = KafkaConsumer(
        'test',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    # Connexion à une collection mongo appellée Twitter

    try:
        client = MongoClient()
        db = client['Twitter']
        print("Connected")
        collection = db["Tennis"]
    except:
        print("Unable to connect to Mongo")

    # Consommation des messages

    for message in consumer:
        print("ok")
        try:
            message = message.value
            result = collection.insert_one(message)
            print('{} added to {}'.format(message, collection))
            print(result)
        except:
            print("Can not write in Mongo.")
