#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
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
from pyspark.sql import SQLContext
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import json


if __name__ == '__main__':

    sc = SparkContext(appName="PythonStreamingRecieverKafkaSentiment")
    sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 60*15)  # Window that we used to pull data
    broker, topic = sys.argv[1:]
    # Pont en Kafka et Spark Streaming
    kvs = KafkaUtils.createStream(ssc, \
                                  broker, \
                                  groupId="my-group", \
                                  topics={'test': 1})

    parsed = kvs.map(lambda v: json.loads(v[1]))
    parsed.map(lambda x: "Input: " + str(x)).pprint()


    ssc.start()
    ssc.awaitTermination()
