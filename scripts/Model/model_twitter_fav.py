import lightgbm
import pandas as pd
import optuna

from scripts.preprocessor.preprocessor import isolate_target, select_features_and_target, get_num_cat_features
from scripts.fetch_data.save_data import PATH_TO_TRAIN, PATH_TO_VAL, PATH_TO_TEST
from scripts.Model.evaluate import evaluate_model

_LABELS_ = {"_FAV_LABEL_": 0,
            "_RT_LABEL_": 1}

TARGETS = {"low_level": 0,
           "mid_level": 1,
           "gigh_level": 2}


def setup_trainer(fav_or_rt_label: int):
    app = pd.read_csv(PATH_TO_TRAIN)
    val = pd.read_csv(PATH_TO_VAL)

    app = select_features_and_target(dataframe=app)
    val = select_features_and_target(dataframe=val)

    num_features, cat_features = get_num_cat_features(dataframe=app)
    all_features = num_features + cat_features

    # app = map_cat_to_int(dataframe=app)
    # val = map_cat_to_int(dataframe=val)

    x_train, y_train = isolate_target(app)
    x_val, y_val = isolate_target(val)

    targets = [fav_rt[fav_or_rt_label] for fav_rt in y_train]
    y_val = [fav_rt[fav_or_rt_label] for fav_rt in y_val]

    train_data = lightgbm.Dataset(data=x_train,
                                  label=targets,
                                  )

    return train_data, x_val, y_val


def objective_fav(trial) -> (float):
    params_ = {
        "boosting_type": trial.suggest_categorical("boosting_type", ["rf", "gbdt", "dart"]),
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
    }

    model_fav = lightgbm.LGBMClassifier(**params_).fit(X=train_data_fav.data,
                                                       y=train_data_fav.label)
    val_metric_fav = evaluate_model(model=model_fav, features=x_val_fav,
                                    labels=y_val_fav)

    return val_metric_fav


def objective_rt(trial) -> (float):
    params_ = {
        "boosting_type": trial.suggest_categorical("boosting_type", ["rf", "gbdt", "dart"]),
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
    }

    model_rt = lightgbm.LGBMClassifier(**params_).fit(X=train_data_rt.data,
                                                      y=train_data_rt.label)
    val_metric_rt = evaluate_model(model=model_rt, features=x_val_rt,
                                   labels=y_val_rt)

    return val_metric_rt


def trainer_fav(n_trials_: int):
    study = optuna.create_study(direction="maximize")
    study.optimize(objective_fav, n_trials=n_trials_)
    return study.best_trial


def trainer_rt(n_trials_: int):
    study = optuna.create_study(direction="maximize")
    study.optimize(objective_rt, n_trials=n_trials_)
    return study.best_trial


if __name__ == "__main__":
    train_data_fav, x_val_fav, y_val_fav = setup_trainer(fav_or_rt_label=_LABELS_["_FAV_LABEL_"])
    train_data_rt, x_val_rt, y_val_rt = setup_trainer(fav_or_rt_label=_LABELS_["_RT_LABEL_"])

    best_model_fav = trainer_fav(n_trials_=100)
    best_model_rt = trainer_rt(n_trials_=100)

    print("fav Value: {}".format(best_model_fav))
    print("rt Value: {}".format(best_model_rt))
