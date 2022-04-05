import pandas as pd
from sklearn.model_selection import train_test_split
from scripts.fetch_data.save_data import PATH_TO_DATA_PREPROCESSED, PATH_TO_VAL, PATH_TO_TEST, PATH_TO_TRAIN


def train_test_split_(df_preprocessed: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    """
    take the data preprocessed as input
    :df_preprocessed:
    :return: train, validation, test data
    """
    train, test = train_test_split(df_preprocessed, test_size=0.2, random_state=42)
    app, val = train_test_split(train, test_size=0.2, random_state=112)
    return app, val, test


if __name__ == "__main__":
    preprocessed_df = pd.read_csv(PATH_TO_DATA_PREPROCESSED)
    app_, val_, test_ = train_test_split_(df_preprocessed=preprocessed_df)
    app_.to_csv(PATH_TO_TRAIN)
    val_.to_csv(PATH_TO_VAL)
    test_.to_csv(PATH_TO_TEST)
