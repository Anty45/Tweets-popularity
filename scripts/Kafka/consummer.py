import pandas as pd
import pymongo
from kafka import KafkaConsumer, TopicPartition
from pymongo import MongoClient
from json import loads
from multiprocessing import Process
from pathlib import Path
import time
from typing import List


class Consumer:
    def __init__(self, db_name: str, collection_name: str):
        self.messages, self.messages_trends = [], []
        # self._PATH_TO_CSV_ = os.path.join(os.path.dirname(__file__), ".." ,"ressources", "messages.csv")
        self._PATH_TO_CSV_ = "./ressources/messages.csv"
        # self._PATH_TO_XLSX_ = os.path.join(os.path.dirname(__file__),".." , "ressources", "messages_ex.xlsx")
        self._PATH_TO_XLSX_ = "./ressources/messages_ex.xlsx"
        # self._PATH_TO_TRENDS_XLSX_ = os.path.join(os.path.dirname(__file__), "..","/ressources", "trends.xlsx")
        self._PATH_TO_TRENDS_XLSX_ = "./ressources/trends.xlsx"
        self._XLSX_FILENAME_ = "messages_ex.xlsx"
        self._XLSX_TRENDS_FILENAME_ = "trends.xlsx"

        try:
            client = MongoClient()
            db = client[db_name]
            print("Connected")
            self.collection = db[collection_name]

        except pymongo.errors.ConnectionFailure as e:
            print(f'Could not connect to server: %s {e}')

    def spawn_consummer(self, group_id: str, consummer_name: str) -> None:
        consumer_object = KafkaConsumer(
            bootstrap_servers=['kafka-1:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=group_id,
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        setattr(self, consummer_name, consumer_object)

    def consume_in_mongo(self, consummer_object: KafkaConsumer) -> None:
        for message in consummer_object:
            try:
                message = message.value
                result = self.collection.insert_one(message)
                print('{} added to {}'.format(message, self.collection))
                print(result)
            except:
                print("Can not write in Mongo.")

    def convert_csv_to_xl(self, df_csv: pd.DataFrame, path: str) -> None:
        writer = pd.ExcelWriter(path)
        df_csv.to_excel(writer, index=False)
        writer.save()

    def save_trends_to_excel(self, messages: list, path: str) -> None:
        df_trends = pd.DataFrame({"trends": messages})
        print(df_trends.head())
        df_trends.to_excel(path)

    def concurrent_save_csv_xlsx(self, messages: List[dict]):

        df_messages = pd.DataFrame(messages)
        print(df_messages.tail())
        with open(self._PATH_TO_CSV_, 'a', encoding="utf-8") as f:
            df_messages.to_csv(f, header=f.tell() == 0)

    def tearDownConsummer(self, consummer_object: KafkaConsumer, topic: str):
        tp = TopicPartition(topic, 0)
        # register to the topic
        consummer_object.assign([tp])

        # obtain the last offset value
        consummer_object.seek_to_end(tp)
        lastOffset = consummer_object.position(tp)

        consummer_object.seek_to_beginning(tp)
        return consummer_object, lastOffset

    def consume_in_csv(self, consummer_object: KafkaConsumer, topic: str):
        consummer_object, lastOffset = self.tearDownConsummer(consummer_object, topic)
        print("starting consume...")
        for message_dict in consummer_object:
            message = message_dict.value
            self.messages.append(message)
            if message_dict.offset == lastOffset - 1:
                print("Consuming finished")
                break

    def consume_trends(self, consummer_trends: KafkaConsumer, topic: str) -> None:
        consummer_object, lastOffset = self.tearDownConsummer(consummer_trends, topic)
        print("Consuming Trends")
        for message_dict in consummer_trends:
            message = message_dict.value
            self.messages_trends.append(message)
            if message_dict.offset == lastOffset - 1:
                print("Consuming finished")
                break


if __name__ == '__main__':

    _MINUTE_ = 60
    starttime = time.time()
    while True:
        consumer = Consumer(db_name='Twitter', collection_name='test')
        excel_msgs_exists = Path(consumer._PATH_TO_XLSX_)
        if not excel_msgs_exists.is_file():
            consumer.convert_csv_to_xl(
                pd.read_csv(consumer._PATH_TO_CSV_, error_bad_lines=False),
                path=consumer._PATH_TO_XLSX_
            )
        consumer.spawn_consummer(group_id="my-group",
                                 consummer_name="consummer_messages")

        process_consumer_msg = Process(target=consumer.consume_in_csv(consummer_object=consumer.consummer_messages,
                                                                      topic="test")
                                       )

        consumer.spawn_consummer(group_id="trends-group",
                                 consummer_name="consummer_trends")

        process_consumer_trends = Process(
            target=consumer.consume_trends(
                consumer.consummer_trends,
                topic="trends"
            )
        )
        process_save_msg_csv = Process(target=consumer.concurrent_save_csv_xlsx(messages=consumer.messages))
        process_save_trends_xlsx = Process(target=consumer.save_trends_to_excel(messages=consumer.messages_trends,
                                                                                path=consumer._PATH_TO_TRENDS_XLSX_)
                                           )
        process_consumer_msg.start()
        process_consumer_trends.start()
        process_save_trends_xlsx.start()
        process_save_msg_csv.start()
        time.sleep(60 * 15)
