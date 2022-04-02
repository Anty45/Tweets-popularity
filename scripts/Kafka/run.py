import tweepy
import time
from kafka import KafkaProducer
from datetime import datetime, timedelta
from json import dumps
import secrets
from typing import List
import configparser
import os

_PATH_TO_CONF_ = os.path.join(os.path.dirname(__file__), "api_secret.properties")
_MAX_TWEETS_TO_FETCH_ = 50
_WOEID_FRANCE_ = '23424819'
_TOPIC_NAME_ = 'test'
_TOPIC_TRENDS_ = 'trends'

# twitter setup
config = configparser.RawConfigParser()
config.read(_PATH_TO_CONF_)
consumer_key = config.get("ApiSecretsKey", "consumer_key")
consumer_secret = config.get("ApiSecretsKey", "consumer_secret")
access_token = config.get("ApiSecretsKey", "access_token")
access_token_secret = config.get("ApiSecretsKey", "access_token_secret")

# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object by passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True)


def normalize_timestamp(time):
    mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    mytime += timedelta(hours=1)  # the tweets are timestamped in GMT timezone, while I am in +1 timezone
    return mytime.strftime("%Y-%m-%d %H:%M:%S")


def get_trends_by_woeid(woeid: str) -> List[dict]:
    result_request = api.trends_place(id=woeid)
    print(f"Trends from {woeid} fetched...")

    return result_request


def find_tops_trend_name(trends: List[dict]) -> List[tuple]:
    trends_attributes = trends[0]["trends"]
    tops_trend_names = {trend_attribute["name"]: trend_attribute["tweet_volume"]
                        for trend_attribute in trends_attributes
                        if trend_attribute["tweet_volume"] is not None}

    sorted_top_trends = list(sorted(tops_trend_names.items(),
                                    key=lambda name_volume: name_volume[1],
                                    reverse=True))
    return sorted_top_trends


def get_twitter_data(max_tweet_to_fetch: int, trends: List[dict]) -> None:
    trends_names_volumes = find_tops_trend_name(trends)
    top_trends_names = trends_names_volumes[:10]
    random_top_trend = secrets.choice(top_trends_names)
    random_top_trend_name = random_top_trend[0]
    selected_trend_volume = random_top_trend[1]

    print(f"Query keyword : {random_top_trend_name}")
    response = api.search(q=random_top_trend_name,
                          lang="fr",
                          result_type="mixed",
                          count=max_tweet_to_fetch)
    if len(response) != 0:
        print("group of tweets fetched")

    for data in response:
        if not data.retweeted:
            producer.send(_TOPIC_NAME_, value={'user_id': str(data.user.id_str),
                                               "texte": str(data.text),
                                               'created_at': str(normalize_timestamp(str(data.created_at))),
                                               'followers_count': str(data.user.followers_count),
                                               "is_verified": "1" if True == data.user.verified else "0",
                                               'location': str(data.user.location),
                                               'lang': str(data.lang),
                                               'fav': str(data.favorite_count),
                                               'retweet': str(data.retweet_count),
                                               "trend": random_top_trend_name,
                                               "trend_volume": selected_trend_volume})

    print("Data succesfully Send to topic")


def periodic_work(interval: int):
    while True:
        french_trends = get_trends_by_woeid(woeid=_WOEID_FRANCE_)
        get_twitter_data(max_tweet_to_fetch=_MAX_TWEETS_TO_FETCH_, trends=french_trends)
        # interval should be an integer, the number of seconds to wait
        time.sleep(interval)


if __name__ == '__main__':
    # Setup producer by rooting it to our bootstrap_servers
    producer = KafkaProducer(bootstrap_servers=['kafka-1:9092'],
                             api_version=(0, 11, 5),
                             value_serializer=lambda v: dumps(v).encode(
                                 'utf-8'))  # transformation en json avant de le convertir en utf8)

    periodic_work(60 * 15)  # get data every 15 minutes
