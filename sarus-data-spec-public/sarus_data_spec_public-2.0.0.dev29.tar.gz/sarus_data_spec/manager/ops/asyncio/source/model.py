from __future__ import annotations

from typing import Any, Dict
import logging
import pickle as pkl
import typing as t

from sarus_data_spec.manager.ops.asyncio.base import BaseScalarOp
import sarus_data_spec.protobuf as sp

logger = logging.getLogger(__name__)

try:
    import xgboost  # type: ignore[import]
except ModuleNotFoundError:
    logger.info("XGBoost not installed, XGBoost models not available.")

try:
    from sklearn import (
        cluster,
        decomposition,
        ensemble,
        model_selection,
        preprocessing,
        svm,
    )
except ModuleNotFoundError:
    logger.info("sklearn not installed, sklearn models not available.")


class Model(BaseScalarOp):
    async def value(self) -> t.Any:
        model_spec = self.scalar.protobuf().spec.model
        model_code_name = sp.Scalar.Model.ModelClass.Name(
            model_spec.model_class
        )

        args = pkl.loads(model_spec.arguments)
        kwargs = pkl.loads(model_spec.named_arguments)

        if model_code_name.startswith("SK_"):
            model_mapping: Dict[str, Any] = {
                "SK_SVC": svm.SVC,
                "SK_ONEHOT": preprocessing.OneHotEncoder,
                "SK_LABEL_ENCODER": preprocessing.LabelEncoder,
                "SK_PCA": decomposition.PCA,
                # cluster
                "SK_AFFINITY_PROPAGATION": cluster.AffinityPropagation,
                "SK_AGGLOMERATIVE_CLUSTERING": cluster.AgglomerativeClustering,
                "SK_BIRCH": cluster.Birch,
                "SK_DBSCAN": cluster.DBSCAN,
                "SK_FEATURE_AGGLOMERATION": cluster.FeatureAgglomeration,
                "SK_KMEANS": cluster.KMeans,
                "SK_MINIBATCH_KMEANS": cluster.MiniBatchKMeans,
                "SK_MEAN_SHIFT": cluster.MeanShift,
                "SK_OPTICS": cluster.OPTICS,
                "SK_SPECTRAL_CLUSTERING": cluster.SpectralClustering,
                "SK_SPECTRAL_BICLUSTERING": cluster.SpectralBiclustering,
                "SK_SPECTRAL_COCLUSTERING": cluster.SpectralCoclustering,
                # ensemble
                "SK_ADABOOST_CLASSIFIER": ensemble.AdaBoostClassifier,
                "SK_ADABOOST_REGRESSOR": ensemble.AdaBoostRegressor,
                "SK_BAGGING_CLASSIFIER": ensemble.BaggingClassifier,
                "SK_BAGGING_REGRESSOR": ensemble.BaggingRegressor,
                "SK_EXTRA_TREES_CLASSIFIER": ensemble.ExtraTreesClassifier,
                "SK_EXTRA_TREES_REGRESSOR": ensemble.ExtraTreesRegressor,
                "SK_GRADIENT_BOOSTING_CLASSIFIER": ensemble.GradientBoostingClassifier,
                "SK_GRADIENT_BOOSTING_REGRESSOR": ensemble.GradientBoostingRegressor,
                "SK_ISOLATION_FOREST": ensemble.IsolationForest,
                "SK_RANDOM_FOREST_CLASSIFIER": ensemble.RandomForestClassifier,
                "SK_RANDOM_FOREST_REGRESSOR": ensemble.RandomForestRegressor,
                "SK_RANDOM_TREES_EMBEDDING": ensemble.RandomTreesEmbedding,
                "SK_STACKING_CLASSIFIER": ensemble.StackingClassifier,
                "SK_STACKING_REGRESSOR": ensemble.StackingRegressor,
                "SK_VOTING_CLASSIFIER": ensemble.VotingClassifier,
                "SK_VOTING_REGRESSOR": ensemble.VotingRegressor,
                "SK_HIST_GRADIENT_BOOSTING_CLASSIFIER": ensemble.HistGradientBoostingClassifier,
                "SK_HIST_GRADIENT_BOOSTING_REGRESSOR": ensemble.HistGradientBoostingRegressor,
                # model_selection
                "SK_REPEATED_STRATIFIED_KFOLD": model_selection.RepeatedStratifiedKFold,
                "SK_KFOLD": model_selection.KFold,
            }
        elif model_code_name.startswith("XGB_"):
            model_mapping = {
                "XGB_CLASSIFIER": xgboost.XGBClassifier,
            }
        else:
            raise ValueError(
                f"Model {model_code_name} is not supported by sarus."
            )

        ModelClass = model_mapping[model_code_name]
        return ModelClass(*args, **kwargs)
