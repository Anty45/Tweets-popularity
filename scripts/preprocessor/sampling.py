from scripts.fetch_data.save_data import PATH_TO_TRAIN, features_selected, PATH_TO_OVERSAMPLED_DATA
import pandas as pd
from imblearn.over_sampling import SMOTE


def over_sampling_minority_class(data: pd.DataFrame):
    X, Y = data[features_selected + ["retweet"]], data["fav"]
    sampler = SMOTE(sampling_strategy="not majority", k_neighbors=10)
    x_resampled, y_resampled = sampler.fit_resample(X, Y)
    x_resampled["fav"] = y_resampled.values
    print(f"new distribution: {x_resampled['fav'].value_counts()}")
    return x_resampled


if __name__ == "__main__":
    train_data = pd.read_csv(PATH_TO_TRAIN)
    resampled_df_ = over_sampling_minority_class(data=train_data)
    resampled_df_.to_csv(PATH_TO_OVERSAMPLED_DATA, index = False)
