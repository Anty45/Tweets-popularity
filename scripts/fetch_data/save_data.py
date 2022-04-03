import pandas as pd
from pathlib import Path
import os

PATH_TO_FULL_RAW_DATA = Path(__file__) / "../../../ressources/raw_data_comple.csv"


def add_data_to_df(path_to_df: str, df_to_add: pd.DataFrame) -> None:
    if os.path.exists(path_to_df):
        initial_df = pd.read_csv(path_to_df)
        initial_df = initial_df.append(df_to_add)
        initial_df.to_csv(path_to_df, mode="w+")
    else:
        df_to_add.to_csv(path_to_df, index=False)
    print("data saved")