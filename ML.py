

"""
Batch processing : We'll start by load data from
 our MongoDB.

"""

import pymongo
import pandas as pd
from pymongo import MongoClient
connection = MongoClient()
db = connection['Twitter']
input_data = db['Doncic']
data = pd.DataFrame(list(input_data.find()))

# Data fetched are both the tweet and the retweet.

data_uniq = data.drop_duplicates(subset=['texte'], keep="first") # Remove RT
