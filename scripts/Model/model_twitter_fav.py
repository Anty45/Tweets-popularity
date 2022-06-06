import lightgbm
import pandas as pd
import optuna
import joblib

from scripts.preprocessor.preprocessor import isolate_target, select_features_and_target
from scripts.fetch_data.save_data import PATH_TO_TRAIN, PATH_TO_VAL, PATH_TO_RT_MODEL, PATH_TO_FAV_MODEL,\
    _LABELS_, TARGETS, PATH_TO_OVERSAMPLED_DATA
from scripts.Model.evaluate import validate_model


def setup_trainer(fav_or_rt_label: int):
    app = pd.read_csv(PATH_TO_OVERSAMPLED_DATA)
    val = pd.read_csv(PATH_TO_VAL)

    app, features_names = select_features_and_target(dataframe=app)
    val, features_names= select_features_and_target(dataframe=val)

    x_train, y_train = isolate_target(app)
    x_val, y_val = isolate_target(val)

    targets = [fav_rt[fav_or_rt_label] for fav_rt in y_train]
    y_val = [fav_rt[fav_or_rt_label] for fav_rt in y_val]

    train_data = lightgbm.Dataset(data=x_train,
                                  label=targets,
                                  feature_name= features_names
                                  )

    return train_data, x_val, y_val


def objective_fav(trial) -> float:
    params_ = {
        "boosting_type": trial.suggest_categorical("boosting_type", ["rf", "gbdt", "dart"]),
        "num_iterations ": trial.suggest_int("num_iterations ",50, 300),
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
    }

    model_fav = lightgbm.LGBMClassifier(**params_).fit(X=train_data_fav.data,
                                                       y=train_data_fav.label)
    val_metric_fav = validate_model(model=model_fav, features=x_val_fav,
                                    labels=y_val_fav)

    return val_metric_fav


def objective_rt(trial) -> float:
    params_ = {
        "boosting_type": trial.suggest_categorical("boosting_type", ["rf", "gbdt", "dart"]),
        "num_leaves":trial.suggest_int("num_leaves", 8,200),
        "lambda_l1": trial.suggest_float("lambda_l1", 1e-8, 10.0, log=True),
        "lambda_l2": trial.suggest_float("lambda_l2", 1e-8, 10.0, log=True),
        "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
        "bagging_fraction": trial.suggest_float("bagging_fraction", 0.4, 1.0),
        "bagging_freq": trial.suggest_int("bagging_freq", 1, 7),
    }

    model_rt = lightgbm.LGBMClassifier(**params_).fit(X=train_data_rt.data,
                                                      y=train_data_rt.label)
    val_metric_rt = validate_model(model=model_rt, features=x_val_rt,
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


def save_model(best_trials_: optuna.trial.FrozenTrial, path_to_save_mode: str) -> None:
    best_params = best_trials_.params
    classifier = lightgbm.LGBMClassifier(**best_params).fit(X=train_data_fav.data,
                                                            y=train_data_fav.label)
    joblib.dump(value=classifier, filename=path_to_save_mode)


if __name__ == "__main__":
    train_data_fav, x_val_fav, y_val_fav = setup_trainer(fav_or_rt_label=_LABELS_["_FAV_LABEL_"])
    train_data_rt, x_val_rt, y_val_rt = setup_trainer(fav_or_rt_label=_LABELS_["_RT_LABEL_"])

    best_model_fav = trainer_fav(n_trials_=100)
    best_model_rt = trainer_rt(n_trials_=100)

    save_model(best_trials_=best_model_fav, path_to_save_mode=PATH_TO_FAV_MODEL)
    save_model(best_trials_=best_model_rt, path_to_save_mode=PATH_TO_RT_MODEL)

    print("fav Value: {}".format(best_model_fav))
    print("rt Value: {}".format(best_model_rt))
