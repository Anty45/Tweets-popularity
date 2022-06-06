import shap
from scripts.fetch_data.save_data import PATH_TO_FAV_MODEL, PATH_TO_FEATURES_IMP, PATH_TO_DECISION_PLOT, PATH_TO_HEATMAP
from scripts.Model.evaluate import setup_test
from matplotlib import pyplot as plt
import random
from typing import List


def visualize_single_pred(explainer: shap.TreeExplainer, features, features_names_: List):
    rand_ind = random.choice(range(0, len(features) - 1))
    shap_values = explainer.shap_values(features)
    shap.force_plot(explainer.expected_value[0], shap_values[0, :], feature_names=features_names_)


def visualize_features_importance(explainer: shap.TreeExplainer, features, features_names: List):
    shap_values = explainer.shap_values(features)
    plt.figure(figsize=(20, 10))
    shap.summary_plot(shap_values, features=features, feature_names=features_names, show=False)
    plt.savefig(PATH_TO_FEATURES_IMP, bbox_inches='tight')


def visualize_decision_plot(explainer: shap.TreeExplainer, features, features_names: List):
    shap_values = explainer.shap_values(features)
    plt.figure(figsize=(20, 15))
    shap.multioutput_decision_plot(explainer.expected_value, shap_values, row_index=1, feature_names=features_names,
                                   link='logit', show=False, legend_location='center left')
    plt.savefig(PATH_TO_DECISION_PLOT, bbox_inches='tight')


def visualize_heatmap_features_imp(model, features, feature_name: list):
    explainer = shap.Explainer(model, features, feature_names=feature_name)
    shap_values = explainer(features[:1000])
    sample_shap_values = shap_values[:]
    plt.figure(figsize=(20, 15))
    shap.plots.heatmap(sample_shap_values, show=False, max_display=12)
    plt.savefig(PATH_TO_HEATMAP, bbox_inches='tight')


if __name__ == "__main__":
    model_, test_dataset_, features_names_ = setup_test(path_to_model=PATH_TO_FAV_MODEL,
                                                        fav_rt_target="_FAV_LABEL_")

    explainer_ = shap.TreeExplainer(model=model_, feature_names=features_names_)
    visualize_decision_plot(explainer=explainer_, features=test_dataset_.data, features_names=features_names_)
    visualize_heatmap_features_imp(model=model_, features=test_dataset_.data, feature_name=features_names_)

    visualize_features_importance(explainer=explainer_, features=test_dataset_.data, features_names=features_names_)
