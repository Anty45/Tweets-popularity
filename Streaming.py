#import findspark
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.3.2 pyspark-shell"


#findspark.init("D:/MS/Spark/spark")

import sys
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidatorModel

if __name__ == '__main__':
    sc = SparkContext(appName="PythonStreamingRecieverKafkaWordCount")
    ssc = StreamingContext(sc, 5)  # 5 second window
    broker, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, \
                                  broker, \
                                  "Streaming-Tweets", \
                                  {topic: 1})

    # Chargement du modele
    cvModel = CrossValidatorModel.load(os.path.join(sys.argv[1], 'C:/Users/koffi/PycharmProjects/Kafka_Twitter_pyth/main/filRougeModel'))

    # prediction
    ssc.start()
    ssc.awaitTermination()
