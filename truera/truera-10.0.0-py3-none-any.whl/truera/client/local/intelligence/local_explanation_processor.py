from __future__ import annotations

import logging
from typing import (
    Callable, Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union
)

import numpy as np
import pandas as pd

from truera.client.client_utils import STR_TO_EXPLANATION_ALGORITHM_TYPE
from truera.client.util.absolute_progress_bar import AbsoluteProgressBar
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.public import feature_influence_constants as fi_constants
from truera.utils.error_utils import SCORE_TYPE_TO_ERROR_FN

if TYPE_CHECKING:
    from truera.client.local.local_artifacts import Model


class LocalExplanationProcessor:
    SUPPORTED_TREESHAP_SCORE_TYPES = ["probits", "regression", "log_loss"]

    def __init__(
        self,
        *,
        model: Model,
        score_type: str,
        comparison_data: pd.DataFrame,
        feature_map: Optional[Mapping[str, Sequence[str]]] = None,
        num_internal_qii_samples: int = 1000,
        logger: Optional[logging.Logger] = None
    ):
        self._model = model
        self.score_type = score_type
        self.comparison_data = comparison_data
        self.feature_map = feature_map
        self.num_internal_samples = num_internal_qii_samples
        self.logger = logger if logger is not None else logging.getLogger(
            __name__
        )

    def _validate_score_type_for_tree_shap(
        self, is_path_dependent: bool = False
    ):
        if self._model.is_regression:
            if self.score_type != fi_constants.PREDICTOR_SCORE_TYPE_REGRESSION:
                raise ValueError(
                    "Only \"regression\" score type is supported for regression models using the TreeSHAP algorithm!"
                )
        elif self.score_type not in [
            fi_constants.PREDICTOR_SCORE_TYPE_PROBITS,
            fi_constants.PREDICTOR_SCORE_TYPE_LOG_LOSS
        ]:
            raise ValueError(
                "Only \"probits\" and \"logloss\" score types are supported for classification models using the TreeSHAP algorithm!"
            )

        if is_path_dependent and self.score_type != fi_constants.PREDICTOR_SCORE_TYPE_REGRESSION:
            raise ValueError(
                "Path-dependent TreeSHAP values can only be computed for regression models!"
            )

    @staticmethod
    def get_explainer_scorer_from_score_type(
        model: Model, score_type: str, has_labels: bool
    ) -> Callable:
        if score_type not in fi_constants.MODEL_ERROR_SCORE_TYPES:
            return lambda xs, ys=None: model.predict(xs, score_type=score_type)
        if not has_labels:
            raise ValueError(
                f"Error score type \"{score_type}\" requires that the data split has labels!"
            )
        error_fn = SCORE_TYPE_TO_ERROR_FN[score_type]
        predict_score_type = fi_constants.MODEL_ERROR_SCORE_TYPE_TO_MODEL_OUTPUT_SCORE_TYPE[
            score_type]
        return lambda xs, ys: error_fn(
            ys, model.predict(xs, predict_score_type)
        )

    @staticmethod
    def validate_feature_influence_algorithm(algorithm: str):
        if algorithm not in STR_TO_EXPLANATION_ALGORITHM_TYPE:
            raise ValueError(
                f"`algorithm` must be one of {list(STR_TO_EXPLANATION_ALGORITHM_TYPE.keys())}, but given \"{algorithm}\"!"
            )
        return STR_TO_EXPLANATION_ALGORITHM_TYPE.get(algorithm)

    def _recover_pre_influences_if_necessary(
        self, post_infs: pd.DataFrame
    ) -> pd.DataFrame:
        # devnote: this is not the "proper" way to do things
        # but is a way of supporting feature transforms for SHAP-based explanations.
        if not self.feature_map:
            return post_infs
        pre_infs = pd.DataFrame(columns=list(self.feature_map.keys()))
        for pre_col, post_cols in self.feature_map.items():
            pre_infs[pre_col] = post_infs[post_cols].sum(axis=1)
        return pre_infs

    def _get_feature_map_for_explainer(
        self
    ) -> Optional[Mapping[str, Sequence[int]]]:
        if not self.feature_map:
            return None
        output_features = self.comparison_data.columns
        if self._model.transform_obj:
            transformed_data = self._model.transform(
                self.comparison_data.iloc[:10]
            )
            output_features = transformed_data.columns
        post_col_to_index = {c: i for i, c in enumerate(output_features)}
        return {
            pre_col: [
                post_col_to_index[post_col]
                for post_col in self.feature_map[pre_col]
            ] for pre_col in self.feature_map
        }

    def _compute_feature_influences_via_truera_qii(
        self, xs: pd.DataFrame, ys: Optional[Union[np.ndarray, pd.Series]]
    ) -> pd.DataFrame:
        if self.feature_map:
            pre_cols = list(self.feature_map.keys())
        else:
            pre_cols = list(xs.columns)
        from truera_qii.qii.explainers.explainer import \
            Explainer  # pylint: disable=import-error
        model_func = LocalExplanationProcessor.get_explainer_scorer_from_score_type(
            self._model, self.score_type, ys is not None and len(ys) > 0
        )
        with AbsoluteProgressBar() as progress_bar:
            explainer = Explainer(
                data=self._model.transform(self.comparison_data),
                model=self._model.model_obj,
                model_func=model_func,
                model_func_uses_y=self.score_type
                in fi_constants.MODEL_ERROR_SCORE_TYPES,
                pretransform_features=pre_cols,
                feature_map=self._get_feature_map_for_explainer(),
                model_output=fi_constants.SCORE_TYPE_TO_MODEL_OUTPUT[
                    self.score_type],
                validate_function=True,
                allow_pandas_dataframe=True,
                use_ndarray_if_possible=True,
                disable_prometheus=True,
                report_progress_func=progress_bar.set_percentage,
            )

            qiis_np = explainer.truera_qii_values(
                xs, y=ys, num_samples=self.num_internal_samples
            )
            return pd.DataFrame(data=qiis_np, columns=pre_cols)

    def _compute_feature_influences_via_tree_shap_tree_path_dependent(
        self, xs: pd.DataFrame, ys: Optional[Union[np.ndarray, pd.Series]]
    ) -> pd.DataFrame:
        self._validate_score_type_for_tree_shap(is_path_dependent=True)
        from shap import \
            TreeExplainer  # TODO: (AB#5613) Broken for random forest and decision tree models.
        self.logger.warning(
            "Ignoring background/comparison data set and internal sampling parameters."
        )
        post_infs = TreeExplainer(
            self._model.model_obj,
            model_output="raw",
            feature_perturbation="tree_path_dependent",
        ).shap_values(xs, ys, check_additivity=False)
        if isinstance(post_infs, list):  # classification scenario
            post_infs = post_infs[
                1]  # get infs corresponding to output class of 1
        post_infs = pd.DataFrame(data=post_infs, columns=xs.columns)
        return self._recover_pre_influences_if_necessary(post_infs)

    def _compute_feature_influences_via_tree_shap_interventional(
        self, xs: pd.DataFrame, ys: Optional[Union[np.ndarray, pd.Series]]
    ) -> pd.DataFrame:
        self._validate_score_type_for_tree_shap()
        from shap import \
            TreeExplainer  # TODO: (AB#5613) Broken for random forest and decision tree models.
        post_infs = TreeExplainer(
            self._model.model_obj,
            data=self.comparison_data.to_numpy(),
            model_output=fi_constants.SCORE_TYPE_TO_MODEL_OUTPUT[self.score_type
                                                                ],
            feature_perturbation="interventional",
        ).shap_values(xs, ys, check_additivity=False)
        if isinstance(post_infs, list):  # classification scenario
            post_infs = post_infs[
                1]  # get infs corresponding to output class of 1
        post_infs = pd.DataFrame(data=post_infs, columns=xs.columns)
        return self._recover_pre_influences_if_necessary(post_infs)

    def _compute_feature_influences_via_kernel_shap(
        self, xs: pd.DataFrame, ys: Optional[Union[np.ndarray, pd.Series]]
    ) -> pd.DataFrame:
        if self.score_type in fi_constants.MODEL_ERROR_SCORE_TYPES:
            raise ValueError(
                f"KernelSHAP values cannot be computed for specified score type: {self.score_type}"
            )
        model_func = LocalExplanationProcessor.get_explainer_scorer_from_score_type(
            self._model, self.score_type, ys is not None and len(ys) > 0
        )
        from shap import KernelExplainer
        post_infs = KernelExplainer(
            model_func, self.comparison_data.to_numpy()
        ).shap_values(xs, nsamples=self.num_internal_samples)
        post_infs = pd.DataFrame(data=post_infs, columns=xs.columns)
        return self._recover_pre_influences_if_necessary(post_infs)

    def get_feature_influences_for_data(
        self,
        pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame] = None,
        ys: Optional[Union[np.ndarray, pd.Series]] = None,
        algorithm: ExplanationAlgorithmType = ExplanationAlgorithmType.
        TRUERA_QII
    ) -> pd.DataFrame:
        if self.feature_map and post_data is None:
            raise ValueError(
                "Cannot compute explanations if feature map is present but post data is not!"
            )
        xs = post_data if post_data is not None else pre_data
        xs = self._model.transform(xs)
        ys = ys.to_numpy().ravel() if isinstance(ys, pd.Series) else ys

        ret = {
            ExplanationAlgorithmType.TRUERA_QII:
                self._compute_feature_influences_via_truera_qii,
            ExplanationAlgorithmType.TREE_SHAP_PATH_DEPENDENT:
                self.
                _compute_feature_influences_via_tree_shap_tree_path_dependent,
            ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL:
                self._compute_feature_influences_via_tree_shap_interventional,
            ExplanationAlgorithmType.KERNEL_SHAP:
                self._compute_feature_influences_via_kernel_shap
        }[algorithm](xs, ys)
        ret = ret[list(pre_data.columns)]
        return ret

    def get_feature_influences_for_data_infer_algorithm(
        self,
        pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame] = None,
        ys: Optional[Union[np.ndarray, pd.Series]] = None,
        use_qii: bool = True
    ) -> Tuple[pd.DataFrame, str]:
        if not use_qii:
            try:
                return self.get_feature_influences_for_data(
                    pre_data,
                    post_data=post_data,
                    ys=ys,
                    algorithm=ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL
                ), ExplanationAlgorithmType.TREE_SHAP_INTERVENTIONAL
            except Exception as e:
                self.logger.warning(
                    "Failed to use TreeSHAP for this model. Defaulting to KernelSHAP..."
                )
                if isinstance(e, ValueError):
                    self.logger.warning(e)
                else:
                    self.logger.debug(e)
                return self.get_feature_influences_for_data(
                    pre_data,
                    post_data=post_data,
                    ys=ys,
                    algorithm=ExplanationAlgorithmType.KERNEL_SHAP
                ), ExplanationAlgorithmType.KERNEL_SHAP

        return self.get_feature_influences_for_data(
            pre_data,
            post_data=post_data,
            ys=ys,
            algorithm=ExplanationAlgorithmType.TRUERA_QII
        ), ExplanationAlgorithmType.TRUERA_QII
