import pandas as pd
from pathlib import Path
import os

PATH_TO_FULL_RAW_DATA = Path(__file__) / "../../../ressources/raw_data_comple.csv"
PATH_TO_DATA_PREPROCESSED = Path(__file__) / "../../../ressources/data_preprocessed.csv"
PATH_TO_TRAIN = Path(__file__) / "../../../ressources/app.csv"
PATH_TO_VAL = Path(__file__) / "../../../ressources/val.csv"
PATH_TO_TEST = Path(__file__) / "../../../ressources/test.csv"
PATH_TO_PREPROCESSOR = Path(__file__) / "../../../ressources/preprocessor.joblib"


def add_data_to_df(path_to_df: str, df_to_add: pd.DataFrame) -> None:
    if os.path.exists(path_to_df):
        initial_df = pd.read_csv(path_to_df)
        initial_df = initial_df.append(df_to_add)
        initial_df.to_csv(path_to_df, mode="w+", index=False)
    else:
        df_to_add.to_csv(path_to_df, index=False)
    print("data saved")