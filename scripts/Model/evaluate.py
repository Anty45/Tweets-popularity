import lightgbm
from sklearn.metrics import roc_auc_score, f1_score
import numpy as np


def evaluate_model(model: lightgbm.LGBMClassifier, features, labels):
    predictions_raw = model.predict(X=features)
    # predictions_classes = np.argmax(predictions_raw, axis=1)
    scores = f1_score(y_true=labels, y_pred=predictions_raw,average="macro")

    return scores
