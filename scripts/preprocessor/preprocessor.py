import pandas as pd
import numpy as np
from typing import List
from scripts.fetch_data.save_data import PATH_TO_FULL_RAW_DATA, PATH_TO_DATA_PREPROCESSED, PATH_TO_PREPROCESSOR
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
TARGETS = ["fav", "retweet"]


def remove_duplicates_row(df: pd.DataFrame):
    return df.drop_duplicates(subset=["texte"])


def process_tweet_date(df: pd.DataFrame, ) -> pd.DataFrame:
    df["tweet_hour"] = df.created_at.apply(lambda tweet_date: tweet_date.hour)
    df["tweet_day_of_the_week"] = df.created_at.apply(lambda tweet_date: tweet_date.day_of_week)
    df["tweet_quarter"] = df.created_at.apply(lambda tweet_date: tweet_date.quarter)
    return df


def isolate_target(data: pd.DataFrame) -> (np.ndarray, np.ndarray):
    targets = list(zip(data.fav.values.tolist(),
                       data.retweet.values.tolist()))
    data.drop(labels=TARGETS, axis=1, inplace=True)
    features = data.values
    return features, targets


def select_features_and_target(dataframe: pd.DataFrame) -> pd.DataFrame:
    features_selected = ["tweet_quarter",
                         "tweet_day_of_the_week",
                         "tweet_hour",
                         "trend_volume",
                         # "trend",
                         "is_verified",
                         "followers_count",
                         # "location",
                         "fav",
                         "retweet"]
    return dataframe[features_selected]


def map_cat_to_int(dataframe: pd.DataFrame) -> pd.DataFrame:
    d = defaultdict(LabelEncoder)
    label_encoder = dataframe.apply(lambda x: d[x.name].fit_transform(x))
    np.save(PATH_TO_PREPROCESSOR, label_encoder.classes_)
    return dataframe


def get_num_cat_features(dataframe: pd.DataFrame) -> (List, List):
    """
    :dataframe:
    return
    """
    cat_cols = dataframe.select_dtypes(["object", "category"]).columns.tolist()
    num_cols = [col for col in dataframe.columns.values if col not in cat_cols]
    return num_cols, cat_cols


def bucketize_target(fav_rt: int) -> int:
    if fav_rt < 100:
        return 0
    elif 100 <= fav_rt < 200:
        return 1
    elif 200 <= fav_rt < 1000:
        return 2
    else:
        return 3


if __name__ == "__main__":
    df_raw = pd.read_csv(PATH_TO_FULL_RAW_DATA)
    df_raw.drop_duplicates(subset=["texte"], inplace=True)
    df_raw["created_at"] = df_raw.created_at.apply(lambda x: pd.to_datetime(x, format=DATE_FORMAT))
    df_raw["fav"] = df_raw.fav.apply(lambda x: bucketize_target(x))
    df_raw["retweet"] = df_raw.retweet.apply(lambda x: bucketize_target(x))
    df_raw = process_tweet_date(df_raw)
    df_raw.to_csv(PATH_TO_DATA_PREPROCESSED, index=False)
