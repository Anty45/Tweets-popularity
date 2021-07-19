import pandas as pd
import pymongo
from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
import os
from multiprocessing import Process
from pathlib import Path


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

        self._PATH_TO_CSV_ = os.path.join(os.path.dirname(__file__), "../ressources", "messages.csv")
        self._PATH_TO_XLSX_ = os.path.join(os.path.dirname(__file__), "../ressources", "messages_ex.xlsx")
        self._XLSX_FILENAME_ = "messages_ex.xlsx"

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

    def convert_csv_to_xl(self, df_csv: pd.DataFrame) -> None:
        writer = pd.ExcelWriter(self._PATH_TO_XLSX_)
        df_csv.to_excel(writer, index=False)
        writer.save()

    def concurrent_save_csv_xlsx(self, ):

        df_messages = pd.DataFrame(self.messages)
        print(df_messages.tail())
        with open(self._PATH_TO_CSV_, 'a', encoding="utf-8") as f:
            df_messages.to_csv(f, header=f.tell() == 0)


    def consume_in_csv(self):
        print("starting consume...")
        for message in self.consumer_object:
            print("Reading messages...")
            message = message.value
            print(message)
            self.messages.append(message)
            process_save = Process(target=consumer.concurrent_save_csv_xlsx())
            process_save.start()


if __name__ == '__main__':

    consumer = Consumer(db_name='Twitter', collection_name='test')
    excel_msgs_exists = Path(consumer._PATH_TO_XLSX_)
    if not excel_msgs_exists.is_file():
        consumer.convert_csv_to_xl(
            pd.read_csv(consumer._PATH_TO_CSV_, error_bad_lines=False)
        )
    process_consumer = Process(target=consumer.consume_in_csv())
    process_consumer.start()
