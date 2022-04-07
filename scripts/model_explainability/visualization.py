import shap
from scripts.fetch_data.save_data import PATH_TO_FAV_MODEL, PATH_TO_FEATURES_IMP
from scripts.Model.evaluate import setup_test
from matplotlib import pyplot as plt
import random
from typing import List


def visualize_single_pred(explainer: shap.TreeExplainer, features):
    rand_values = random.choice(features)
    rand_ind = features.tolist().index(rand_values.all())
    shap_values = explainer.shap_values(features)
    shap.force_plot(explainer.expected_value[1], shap_values[rand_ind], features[rand_ind])


def visualize_features_importance(explainer: shap.TreeExplainer, features, features_names: List):
    shap_values = explainer.shap_values(features)
    plt.figure(figsize=(20,10))
    shap.summary_plot(shap_values, features=features, feature_names=features_names,show =False)
    plt.savefig(PATH_TO_FEATURES_IMP, bbox_inches='tight')


def visualize_dependency_plot():
    pass


if __name__ == "__main__":
    model_, test_dataset_, features_names_ = setup_test(path_to_model=PATH_TO_FAV_MODEL,
                                                        fav_rt_target="_FAV_LABEL_")

    explainer_ = shap.TreeExplainer(model=model_)
    visualize_features_importance(explainer=explainer_, features=test_dataset_.data, features_names=features_names_)
