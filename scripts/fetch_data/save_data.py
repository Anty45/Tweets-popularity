import pandas as pd
from pathlib import Path
import os

PATH_TO_FULL_RAW_DATA = Path(__file__) / "../../../ressources/raw_data_comple.csv"
PATH_TO_DATA_PREPROCESSED = Path(__file__) / "../../../ressources/data_preprocessed.csv"
PATH_TO_TRAIN = Path(__file__) / "../../../ressources/app.csv"
PATH_TO_VAL = Path(__file__) / "../../../ressources/val.csv"
PATH_TO_TEST = Path(__file__) / "../../../ressources/test.csv"
PATH_TO_PREPROCESSOR = Path(__file__) / "../../../ressources/preprocessor.joblib"
PATH_TO_FAV_MODEL = Path(__file__) / "../../../ressources/model_fav.joblib"
PATH_TO_RT_MODEL = Path(__file__) / "../../../ressources/model_fav.joblib"
PATH_TO_FEATURES_IMP = Path(__file__) / "../../../ressources/features_imp_summary.png"
PATH_TO_DECISION_PLOT = Path(__file__) / "../../../ressources/decision_plot.png"
PATH_TO_HEATMAP = Path(__file__) / "../../../ressources/features_heatmap.png"

_LABELS_ = {"_FAV_LABEL_": 0,
            "_RT_LABEL_": 1}

TARGETS = {"low_level": 0,
           "mid_level": 1,
           "mid_high_level": 2,
           "high_level": 3}


def add_data_to_df(path_to_df: str, df_to_add: pd.DataFrame) -> None:
    if os.path.exists(path_to_df):
        initial_df = pd.read_csv(path_to_df)
        initial_df = initial_df.append(df_to_add)
        initial_df.to_csv(path_to_df, mode="w+", index=False)
    else:
        df_to_add.to_csv(path_to_df, index=False)
    print("data saved")
