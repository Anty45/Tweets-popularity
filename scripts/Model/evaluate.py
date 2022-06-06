import lightgbm
import pandas as pd
from sklearn.metrics import f1_score, classification_report, confusion_matrix
from scripts.fetch_data.save_data import PATH_TO_TEST, PATH_TO_FAV_MODEL, _LABELS_
import joblib

from scripts.preprocessor.preprocessor import select_features_and_target, isolate_target


def validate_model(model: lightgbm.LGBMClassifier, features, labels):
    predictions_raw = model.predict(X=features)
    scores = f1_score(y_true=labels, y_pred=predictions_raw, average="macro")

    return scores


def model_test(model: lightgbm.LGBMClassifier, test_features, test_labels):
    predictions_test = model.predict(X=test_features)
    print(confusion_matrix(y_true=test_labels, y_pred=predictions_test))
    return classification_report(y_true=test_labels, y_pred=predictions_test)


def setup_test(path_to_model: str, fav_rt_target: str):
    model_ = joblib.load(filename=path_to_model)
    test = pd.read_csv(PATH_TO_TEST, index_col=False)
    test, features_names = select_features_and_target(dataframe=test)

    x_test, y_test = isolate_target(test)

    test_targets = [fav_rt[_LABELS_[fav_rt_target]] for fav_rt in y_test]

    test_dataset = lightgbm.Dataset(data=x_test,
                                    label=test_targets,
                                    feature_name=features_names
                                    )
    return model_, test_dataset, features_names


if __name__ == "__main__":
    model_, test_dataset_, features_names_ = setup_test(path_to_model=PATH_TO_FAV_MODEL,
                                                        fav_rt_target="_FAV_LABEL_")
    classif_reports = model_test(model=model_,
                                 test_features=test_dataset_.data,
                                 test_labels=test_dataset_.label
                                 )
    print(classif_reports)
