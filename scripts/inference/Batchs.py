from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark.ml import PipelineModel
from keras.preprocessing.sequence import pad_sequences
import pickle
from keras.models import load_model
from keras import backend as K
import tensorflow as tf

import numpy as np
import pandas as pd
import os


class Batchs_prediction:

    def __init__(self):
        self.conf = SparkConf().set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.3.2")
        self.sc = SparkContext(conf=self.conf)
        self.sqlContext = SQLContext(self.sc)
        self.df = self.sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri",
                                                                                            "mongodb://127.0.0.1/Twitter.Tennis").load()

        self._PATH_TO_PIPELINE_ = os.path.join(os.path.dirname(__file__), "../ressources", "pipeline")
        self._PATH_TO_TOKENIZER_ = os.path.join(os.path.dirname(__file__), "../ressources", "tokenizer.pickle")
        self._PATH_TO_MODEL_ = os.path.join(os.path.dirname(__file__), "../ressources", "cnn_model")
        self._VOCAB_LEN_ = 36

    def f1(self, y_true, y_pred):
        y_pred = K.round(y_pred)
        tp = K.sum(K.cast(y_true * y_pred, 'float'), axis=0)
        # tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
        fp = K.sum(K.cast((1 - y_true) * y_pred, 'float'), axis=0)
        fn = K.sum(K.cast(y_true * (1 - y_pred), 'float'), axis=0)

        p = tp / (tp + fp + K.epsilon())
        r = tp / (tp + fn + K.epsilon())

        f1 = 2 * p * r / (p + r + K.epsilon())
        f1 = tf.where(tf.math.is_nan(f1), tf.zeros_like(f1), f1)
        return K.mean(f1)

    def pipeline_load(self):
        return PipelineModel.load(self._PATH_TO_PIPELINE_)

    def load_data(self):
        pipelineModel = self.pipeline_load()
        df = self.df.withColumnRenamed("texte", "Twitter Text Raw")
        data = pipelineModel.transform(df)
        data = data.select("Twitter Text Raw", "features", "filtered")
        return data

    def load_tokenizer(self):
        with open(self._PATH_TO_TOKENIZER_, 'rb') as handle:
            tokenizer = pickle.load(handle)
        return tokenizer

    def padding_tokenized_data(self, tokenizer, data):
        X = tokenizer.texts_to_sequences((data.select("filtered").toPandas())["filtered"].values)
        X = pad_sequences(X, maxlen=self._VOCAB_LEN_)
        print(np.shape(X))
        return X

    def make_batch_predictions(self, X, data):
        cnn = load_model(self._PATH_TO_MODEL_, custom_objects={'f1': self.f1})
        prediction = cnn.predict_classes(X)
        texte = (data.select("Twitter Text Raw").toPandas())["Twitter Text Raw"].values
        text_pred_dict = {"texte": texte, "prediction": prediction}
        df_pred = pd.DataFrame(text_pred_dict)
        print(df_pred)
        return df_pred
