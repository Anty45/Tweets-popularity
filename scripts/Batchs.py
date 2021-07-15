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


def f1(y_true, y_pred):
    y_pred = K.round(y_pred)
    tp = K.sum(K.cast(y_true*y_pred, 'float'), axis=0)
    # tn = K.sum(K.cast((1-y_true)*(1-y_pred), 'float'), axis=0)
    fp = K.sum(K.cast((1-y_true)*y_pred, 'float'), axis=0)
    fn = K.sum(K.cast(y_true*(1-y_pred), 'float'), axis=0)

    p = tp / (tp + fp + K.epsilon())
    r = tp / (tp + fn + K.epsilon())

    f1 = 2*p*r / (p+r+K.epsilon())
    f1 = tf.where(tf.math.is_nan(f1), tf.zeros_like(f1), f1)
    return K.mean(f1)

conf = SparkConf().set("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.11:2.3.2")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)
df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://127.0.0.1/Twitter.Tennis").load()
df.show()
#FIXME:  Ecrit en dur - Construire un fichier properties pour les repertoires
pipelineModel = PipelineModel.load('C:/Users/koffi/PycharmProjects/Kafka_Twitter_pyth/main/pipeline')
df = df.withColumnRenamed("texte","Twitter Text Raw")
data = pipelineModel.transform(df)
data = data.select("Twitter Text Raw","features","filtered")
# loading
#FIXME:  Ecrit en dur - Construire un fichier properties pour les repertoires
with open('C:/Users/koffi/PycharmProjects/Kafka_Twitter_pyth/main/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
X = tokenizer.texts_to_sequences((data.select("filtered").toPandas())["filtered"].values)
X = pad_sequences(X,maxlen=36) # taille de notre vocabulaire d'entrinement + 1
print(np.shape(X))
# Load Model
#FIXME:  Ecrit en dur - Construire un fichier properties pour les repertoires
cnn = load_model("C:/Users/koffi/PycharmProjects/Kafka_Twitter_pyth/main/cnn_model", custom_objects={'f1':f1})
prediction = cnn.predict_classes(X)
texte = (data.select("Twitter Text Raw").toPandas())["Twitter Text Raw"].values
d = {"texte": texte,"prediction": prediction}
print(pd.DataFrame(d))



