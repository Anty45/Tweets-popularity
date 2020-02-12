

from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))  # transformation en json avant de le convertir en utf8

for e in range(10):
    data = {'number' : (e+1000)}
    producer.send('test', value=data)
    sleep(5)





