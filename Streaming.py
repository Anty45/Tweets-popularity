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


if __name__ == '__main__':
    sc = SparkContext(appName="PythonStreamingRecieverKafkaSentiment")
    sqlContext = SQLContext(sc)
    ssc = StreamingContext(sc, 5)  # 5 second window
    broker, topic = sys.argv[1:]
    # Pont en Kafka et Spark Streaming
    kvs = KafkaUtils.createStream(ssc, \
                                  broker, \
                                  "Streaming-Tweets", \
                                  {topic: 1})

    # Chargement du modele
    cvModel = CrossValidatorModel.load(os.path.join(sys.argv[1], 'C:/Users/koffi/PycharmProjects/Kafka_Twitter_pyth/main/filRougeModel'))
    pipeline = PipelineModel.load("C:/Users/koffi/PycharmProjects/Kafka_Twitter_pyth/main/pipeline")
    # Chargement des données

    lines = kvs.map(lambda x: x[1])
    df = lines.foreachRDD(lambda rdd: rdd.toDF())

    # pipeline de preproccessing
    datasetTest = pipeline.transform(df)

    # prediction
    testPredictions = cvModel.transform(datasetTest)

    #Evaluation

    evaluatorTest = MulticlassClassificationEvaluator(predictionCol="prediction", labelCol="label", metricName="f1")
    result = evaluatorTest.evaluate(testPredictions)
    result.pprint()

    ssc.start()
    ssc.awaitTermination()
