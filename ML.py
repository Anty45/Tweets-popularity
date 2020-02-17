
import nltk
import re
import pymongo
import pandas as pd
from pymongo import MongoClient

import string

"""
    :param text : le tweet en question
    :return : le texte sans les ponctuations
    
    Operation de preprocessing

"""


def remove_punct(text):
    text = "".join([char for char in text if char not in string.punctuation])
    text = re.sub('[0-9]+', '', text)
    return text


"""
    :param text : le tweet en question
    :return : une liste de token
    
    Operation de tokenisation
"""


def tokenization(text):
    text = re.split('\W+', text)
    return text


"""
    :param text : le tweet en question
    :param stopword : la liste de mot  explicitement déclaré qu'on souhaite remplacée 
    
    :return : une liste de token sans les stopwords

    Operation de tokenisation
"""

def remove_stopwords(text,stopword):
    text = [word for word in text if word not in stopword]
    return text


def stemming(text):
    text = [ps.stem(word) for word in text]
    return text

def lemmatizer(text):
    text = [wn.lemmatize(word) for word in text]
    return text


"""
Batch processing : We'll start by write data to  our MongoDB.

"""

connection = MongoClient()
db = connection['Twitter']
input_data = db['Doncic']
data = pd.DataFrame(list(input_data.find()))

# Data fetched are both the tweet and the retweet.

data_uniq = data.drop_duplicates(subset=['texte'], keep="first")  # Remove RT

data = pd.read_csv("./Sentiment.csv",delimiter=',')

X = pd.DataFrame(data[['tweet_id','text']])
Y = data['sentiment']


X['Tweet_punct'] = X['text'].apply(lambda x: remove_punct(x))


X['Tweet_tokenized'] = X['Tweet_punct'].apply(lambda x: tokenization(x.lower()))


stopword = nltk.corpus.stopwords.words('english') + nltk.corpus.stopwords.words('french')
stopword.extend(['rt'])

X['Tweet_nonstop'] = X['Tweet_tokenized'].apply(lambda x: remove_stopwords(x,stopword))

ps = nltk.PorterStemmer()
wn = nltk.WordNetLemmatizer()

X['Tweet_stemmed'] = X['Tweet_nonstop'].apply(lambda x: stemming(x))
X['Tweet_stemmed'] = X['Tweet_nonstop'].apply(lambda x: stemming(x))

