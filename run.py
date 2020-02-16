import tweepy
import time
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime, timedelta
from json import dumps

if __name__ == '__main__':

    # twitter setup
    consumer_key = "kc17v5bzrUypcf6zH2pr3wegZ"
    consumer_secret = "4yhDcoBvtG5FEOG0y2ETfozAnq6qL3orn0RACdIjAzAZe4DAO1"
    access_token = "3395703293-clKkQY8wxu0MOunjRpzT9p4ZQv7Q3zCHTUO1g7s"
    access_token_secret = "bw3zH1XTqO9dSPTzBIN5M7qlqOQO78urcdOGZ05Y3blfk"
    # Creating the authentication object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Setting your access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # Creating the API object by passing in auth information
    api = tweepy.API(auth,wait_on_rate_limit=True)

    def normalize_timestamp(time):
        mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        mytime += timedelta(hours=1)  # the tweets are timestamped in GMT timezone, while I am in +1 timezone
        return (mytime.strftime("%Y-%m-%d %H:%M:%S"))

    # Setup producer by rooting it to our bootstrap_servers
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda v: dumps(v).encode('utf-8'))  # transformation en json avant de le convertir en utf8)
    topic_name = 'test'

    # Script to get Data related to NBA
    def get_twitter_data():
        res = api.search("Gordon",lang = "fr")
        for i in res:
            # Excluce Retwwet :

            if (not i.retweeted) and ('RT @' not in i.text):
                producer.send(topic_name, value={'user_id': str(i.user.id_str),
                                                 "texte": str(i.text),
                                                 'created_at': str(normalize_timestamp(str(i.created_at))),
                                                 'followers_count': str(i.user.followers_count),
                                                 'location': str(i.user.location),
                                                 'lang' : str(i.lang),
                                                 'fav': str(i.favorite_count),
                                                 'retweet': str(i.retweet_count)})

    # Get Data
    get_twitter_data()

    def periodic_work(interval):
        while True:
            get_twitter_data()
            # interval should be an integer, the number of seconds to wait
            time.sleep(interval)

    periodic_work(60*15)  # get data every minute
