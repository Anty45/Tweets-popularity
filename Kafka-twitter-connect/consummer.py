import pandas as pd
import pymongo
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import os
from multiprocessing import Process


class Consumer:
    def __init__(self, db_name: str, collection_name: str):
        self.messages = []
        self.consumer_object = KafkaConsumer(
            'test',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my-group',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

        self._PATH_TO_CSV_ = os.path.join(os.path.dirname(__file__), "ressources", "messages.csv")
        try:
            client = MongoClient()
            db = client[db_name]
            print("Connected")
            self.collection = db[collection_name]

        except pymongo.errors.ConnectionFailure as e:
            print(f'Could not connect to server: %s {e}')

    def consume_in_mongo(self, ):
        for message in self.consumer_object:
            try:
                message = message.value
                result = self.collection.insert_one(message)
                print('{} added to {}'.format(message, self.collection))
                print(result)
            except:
                print("Can not write in Mongo.")

    def concurrent_save_csv(self, ):

        dict_for_df_creation = {"messages": self.messages}
        df_messages = pd.DataFrame(dict_for_df_creation)
        print(df_messages.head())
        df_messages.to_csv(self._PATH_TO_CSV_, mode="a")

    def consume_in_csv(self):
        print("starting consume...")
        for message in self.consumer_object:
            print("Reading messages...")
            message = message.value
            print(message)
            self.messages.append(message)
            process_save = Process(target=consumer.concurrent_save_csv())
            process_save.start()


if __name__ == '__main__':
    consumer = Consumer(db_name='Twitter', collection_name='test')
    process_consumer = Process(target=consumer.consume_in_csv())
    process_consumer.start()