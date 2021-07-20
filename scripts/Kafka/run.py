import tweepy
import time
from kafka import KafkaProducer
from datetime import datetime, timedelta
from json import dumps
import secrets
from typing import List
import configparser
import os

if __name__ == '__main__':

    _PATH_TO_CONF_ = os.path.join(os.path.dirname(__file__), "../api_secret.properties")
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


    # Setup producer by rooting it to our bootstrap_servers
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda v: dumps(v).encode(
                                 'utf-8'))  # transformation en json avant de le convertir en utf8)


    def get_trends_by_woeid(woeid: str) -> List[dict]:
        result_request = api.trends_place(id=woeid)
        print(f"Trends from {woeid} fetched...")

        return result_request


    def find_tops_trend_name(trends: List[dict]) -> List[str]:
        trends_attributes = trends[0]["trends"]
        tops_trend_names = [trend_attribute["name"] for trend_attribute in trends_attributes]
        return tops_trend_names


    def get_twitter_data(max_tweet_to_fetch: int, trends: List[dict]) -> None:
        trends_names = find_tops_trend_name(trends)
        random_top_trend_name = secrets.choice(trends_names)
        print(f"Query keyword : {random_top_trend_name}")
        res = api.search(q=random_top_trend_name,
                         lang="fr",
                         result_type="mixed",
                         count=max_tweet_to_fetch)
        if len(res) != 0:
            print("group of tweets fetched")

        for i in res:
            if (not i.retweeted) and ('RT @' not in i.text):
                producer.send(_TOPIC_NAME_, value={'user_id': str(i.user.id_str),
                                                   "texte": str(i.text),
                                                   'created_at': str(normalize_timestamp(str(i.created_at))),
                                                   'followers_count': str(i.user.followers_count),
                                                   'location': str(i.user.location),
                                                   'lang': str(i.lang),
                                                   'fav': str(i.favorite_count),
                                                   'retweet': str(i.retweet_count)})

        producer.send(_TOPIC_TRENDS_, value=trends_names)

    def periodic_work(interval: int):
        while True:
            french_trends = get_trends_by_woeid(woeid=_WOEID_FRANCE_)
            get_twitter_data(max_tweet_to_fetch=_MAX_TWEETS_TO_FETCH_, trends=french_trends)
            # interval should be an integer, the number of seconds to wait
            time.sleep(interval)


    periodic_work(60 * 15)  # get data every 15 minutes
