
#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages org.apache.spark:spark-streaming-kafka-0-10_2.11:2.4.3 pyspark-shell"
os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.3," \
                                    "org.apache.kafka:kafka-clients:2.4.0 pyspark-shell "



#findspark.init("D:/MS/Spark/spark")

import sys
from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from uuid import uuid1
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.sql import SQLContext,SparkSession
from pyspark.sql.types import StructType,IntegerType,StringType,TimestampType, StructField
from pyspark.sql.functions import col, from_json, udf, struct, window
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import json
import datetime


if __name__ == '__main__':

    def parse_json(df):
        twitterid = str(json.loads(df[0])['user_id'])
        texte = str(json.loads(df[0])['texte'])
        created_at = str(json.loads(df[0])['created_at'])
        followers_count = str(json.loads(df[0])['followers_count'])
        location = str(json.loads(df[0])['location'])
        lang = str(json.loads(df[0])['lang'])
        fav = str(json.loads(df[0])['fav'])
        retweet = str(json.loads(df[0])['retweet'])

        return [twitterid,texte, created_at, followers_count , location ,lang, fav, retweet]


    def convert_twitter_date(timestamp_str):
        output_ts = datetime.datetime.strptime(timestamp_str.replace('+0000 ', ''), '%Y-%m-%d %H:%M:%S')
        return output_ts

    spark = SparkSession \
        .builder \
        .appName("PythonStreamingRecieverKafkaSentiment") \
        .getOrCreate()

    # Pont en Kafka et Spark Streaming


    # Parsing des Tweets

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .option("startingOffsets", "earliest") \
        .load() \
        .selectExpr("CAST(value AS STRING)")
    # .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

    # Definition du schema / Twitter text raw = texte

    json_schema = StructType([
        StructField("user_id", StringType(), True),
        StructField("texte", StringType(), True),
        StructField("created_at", StringType(), True),
        StructField("followers_count", StringType(), True),
        StructField("location", StringType(), True),
        StructField("lang", StringType(), True),
        StructField("fav", StringType(), True),
        StructField("retweet", StringType(), True)
    ])

    udf_parse_json = udf(parse_json, json_schema)
    udf_convert_twitter_date = udf(convert_twitter_date, TimestampType())

    jsonoutput = df.withColumn("parsed_field", udf_parse_json(struct([df[x] for x in df.columns]))).where(
        col("parsed_field").isNotNull()).withColumn("created_at", col("parsed_field.created_at")).withColumn(
        "followers_count", col("parsed_field.followers_count")).withColumn("Twitter Text Raw", col("parsed_field.texte")).withColumn(
        "location", col("parsed_field.location")).withColumn("lang", col("parsed_field.lang")).withColumn(
        "fav", col("parsed_field.fav")).withColumn("lang", col("parsed_field.lang")).withColumn(
        "created_at_ts", udf_convert_twitter_date(col("parsed_field.created_at")))

    windowedCounts = jsonoutput.groupBy(
        window(jsonoutput.created_at_ts, "1 minutes", "45 seconds"),
        jsonoutput.lang
    ).count()

    # Real-Time prediction

    pipeline = PipelineModel.load('./pipeline')
    model = CrossValidatorModel.load('./filRougeModel')
    preprocessing = pipeline.transform(jsonoutput)
    prediction = model.transform(preprocessing)

    #jsonoutput.writeStream.format("console").trigger(continuous='1 second').start()
    prediction.writeStream.format("console").trigger(processingTime='6 seconds').start().awaitTermination()