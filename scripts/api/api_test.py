import requests

tweet_day_of_the_week: int
tweet_hour: int
is_verified: int
followers_count: int

query = {"tweet_day_of_the_week": 2,
         "tweet_hour": 8,
         "is_verified": 0,
         "followers_count": 8590}

url = "http://127.0.0.1:85/predict"

if __name__=="__main__":
    response = requests.post(url=url, json=query)
    print(response.json())
