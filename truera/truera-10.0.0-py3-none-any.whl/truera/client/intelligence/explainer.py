from __future__ import annotations

from abc import ABC
from abc import abstractmethod
import logging
import shutil
from typing import Mapping, Optional, Sequence, Tuple, TYPE_CHECKING, Union

import numpy as np
import pandas as pd

from truera.client.intelligence.bias import BiasResult
from truera.client.intelligence.spline_fitter import SplineFitter
from truera.client.intelligence.viz import roc_plot
import truera.client.intelligence.viz as viz
from truera.client.util import workspace_validation_utils
from truera.protobuf.public.aiq.accuracy_pb2 import \
    AccuracyType  # pylint: disable=no-name-in-module
from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FeatureSortMethod  # pylint: disable=no-name-in-module
from truera.protobuf.public.data.segment_pb2 import \
    InterestingSegment  # pylint: disable=no-name-in-module
from truera.protobuf.public.qoi_pb2 import \
    ExplanationAlgorithmType  # pylint: disable=no-name-in-module
from truera.public.feature_influence_constants import \
    get_output_type_from_score_type
from truera.public.feature_influence_constants import is_regression_score_type
from truera.public.feature_influence_constants import \
    PREDICTOR_SCORE_TYPE_LOGITS
from truera.public.feature_influence_constants import \
    PREDICTOR_SCORE_TYPE_PROBITS
from truera.public.feature_influence_constants import VALID_MODEL_OUTPUT_TYPES
from truera.utils.accuracy_utils import ACCURACY_METRIC_MAP
from truera.utils.accuracy_utils import BINARY_CLASSIFICATION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import CLASSIFICATION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import \
    MULTICLASS_CLASSIFICATION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import PROBITS_OR_LOGITS_SCORE_ACCURACIES
from truera.utils.accuracy_utils import REGRESSION_SCORE_ACCURACIES
from truera.utils.accuracy_utils import SEGMENT_GENERALIZED_METRICS

if TYPE_CHECKING:
    from truera.client.local.local_artifacts import Cache
    from truera.client.local.local_artifacts import DataCollection
    from truera.client.local.local_artifacts import Model
    from truera.client.local.local_artifacts import Project
    from truera.client.nn.client_configs import AttributionConfiguration


class Explainer(ABC):

    def get_feature_names(self) -> Sequence[str]:
        """Get the feature names associated with the current data-collection.

        Returns:
            Sequence[str]: Feature names.
        """
        return list(self.get_xs(0, 1).columns)

    @property
    @abstractmethod
    def logger(self):
        pass

    def _get_output_classes(self) -> int:
        """Get the number of output classes per model.

        Returns:
            int: The number of output classes
        """
        return 1 if self._get_output_type(
        ) == "regression" else 2  # by default, binary classification

    @abstractmethod
    def _ensure_data_split(self):
        pass

    @abstractmethod
    def _get_score_type(self) -> str:
        pass

    @staticmethod
    def _check_pytorch_rnn_error(err: RuntimeError):
        if str(err).startswith(
            "Cannot get deterministic gradients from RNN's with cudnn."
        ) or str(err).startswith(
            "cudnn RNN backward can only be called in training mode"
        ):
            raise RuntimeError(
                """
                Using TruEra with PyTorch RNN layers may require disabling CUDA or running the model in training mode. 
                Disabling CUDA may slow down calculations. Running with the model in training mode may lead to nondeterministic behavior. 
                To disable CUDA, set use_cuda=False in your AttributionConfiguration.
                To enable training mode, set use_training_mode=True in your AttributionConfiguration. 
                """
            )
        return err

    def _get_output_type(self) -> str:
        return get_output_type_from_score_type(self._get_score_type())

    def _validate_feature_influence_score_type(self, score_type: str):
        workspace_validation_utils.validate_feature_influence_score_type(
            self._get_output_type() == "regression", score_type
        )

    def _validate_comparison_data_splits(
        self,
        available_data_splits: Sequence[str],
        base_data_split_name: str,
        comparison_data_splits: Optional[Sequence[str]] = None,
        use_all_data_splits: bool = False
    ) -> Sequence[str]:
        if not use_all_data_splits and not comparison_data_splits:
            raise ValueError(
                "Either provide `comparison_data_splits` or set `use_all_data_splits` to True"
            )
        if use_all_data_splits and comparison_data_splits:
            self.logger.warning(
                "`use_all_data_splits` is set to True, ignoring `comparison_data_splits`"
            )
        # case 1: asking for all data splits
        if use_all_data_splits:
            available_data_splits.remove(base_data_split_name)
            return sorted(available_data_splits)
        # case 2: validate individual comparison data splits that are requested
        deduped_comparison_data_splits = []
        for split_name in comparison_data_splits:
            if split_name not in available_data_splits:
                raise ValueError(f"No such data split \"{split_name}\"!")
            if split_name in deduped_comparison_data_splits:
                self.logger.warning(
                    f"Split \"{split_name}\" was requested as a duplicate of an existing comparison data split. Ignoring."
                )
            else:
                deduped_comparison_data_splits.append(split_name)
        if base_data_split_name in deduped_comparison_data_splits:
            self.logger.warning(
                f"Split \"{base_data_split_name}\" is already set as the primary split. Ignoring request to set as comparison."
            )
            deduped_comparison_data_splits.remove(base_data_split_name)
        return deduped_comparison_data_splits

    @abstractmethod
    def set_base_data_split(self, data_split_name: str):
        """Set the base data split to use for all operations in the explainer.

        Args:
            data_split_name: Name of the data split.
        """
        pass

    @abstractmethod
    def get_data_collection(self) -> str:
        """Get the data collection name used by explainer."""
        pass

    @abstractmethod
    def set_comparison_data_splits(
        self,
        comparison_data_splits: Optional[Sequence[str]] = None,
        use_all_data_splits: bool = False
    ):
        """Sets comparison data splits to use for all operations in the explainer.

        Args:
            comparison_data_splits: List of data split names for comparison. This is ignored if `use_all_data_split` is set to True. (Optional)
            use_all_data_splits: If set to True, set comparison data splits as all of the data splits in the data collection
                except the base data split. (Optional)
        """
        pass

    @abstractmethod
    def get_base_data_split(self) -> str:
        """Get the base data split used by explainer.

        Returns:
            str: The name of the base data split.
        """
        pass

    @abstractmethod
    def get_comparison_data_splits(self) -> Sequence[str]:
        """Gets the comparison data splits used by the explainer.

        Returns:
            Sequence[str]: The names of the comparison data splits.
        """
        pass

    @abstractmethod
    def get_xs(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        extra_data: bool = False,
        system_data: bool = False
    ) -> pd.DataFrame:
        """Get the inputs/data/x-values.

        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            extra_data: Include extra data columns in the response.
            system_data: Include system data columns (unique ID) in the response.
        Returns:
            pd.DataFrame: The inputs/data/x-values.
        """
        pass

    @abstractmethod
    def get_ys(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False
    ) -> Union[pd.Series, pd.DataFrame]:
        """Get the targets/y-values.

        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            system_data: Include system data columns (unique ID) in the response.
        Returns:
            Union[pd.Series, pd.DataFrame]: The targets/y-values as a pd.Series if one-dimensional, and as a pd.DataFrame if extra columns (e.g. `system_data`) are requested.
        """
        pass

    @abstractmethod
    def get_ys_pred(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> Union[pd.Series, pd.DataFrame]:
        """Get the model predictions.

        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            system_data: Include system data (e.g. timestamps) if available in response. Defaults to False.
            wait: Whether to wait for the job to finish. Defaults to True.

        Returns:
            Union[pd.Series, pd.DataFrame]: The model predictions as a pd.Series by default, and a pd.DataFrame if system data is included.
        """
        pass

    @abstractmethod
    def get_feature_influences(
        self,
        start: Optional[int] = 0,
        stop: Optional[int] = None,
        score_type: Optional[str] = None,
        system_data: bool = False,
        wait: bool = True
    ) -> pd.DataFrame:
        """Get the QIIs/shapley-values for this explainer's currently set data split.

        Args:
            start: The lower bound (inclusive) of the index of points to include. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to include. Defaults to None which is interpreted as the total number of points for local projects and the setting for "Number of default influences" for remote projects.
            score_type: The score type to use when computing influences. If None, defaults to score type of project. Defaults to None.
            system_data: Include system data (e.g. timestamps) if available in response. Defaults to False.
            wait: Whether to wait for the job to finish. Defaults to True.

        Returns:
            pd.DataFrame: The QIIs/shapley-values.
        """
        pass

    @abstractmethod
    def get_feature_influences_for_data(
        self,
        pre_data: pd.DataFrame,
        post_data: Optional[pd.DataFrame] = None,
        ys: Optional[Union[np.ndarray, pd.Series]] = None,
        score_type: Optional[str] = None,
        comparison_post_data: Optional[pd.DataFrame] = None,
        num_internal_qii_samples: int = 1000,
        algorithm: str = "truera-qii"
    ) -> pd.DataFrame:
        """Get the QIIs/shapley-values for the provided data.

        Args:
            pre_data: A pandas DataFrame containing the human-readable data for which to compute influences. If `post_data` is not specified, `pre_data` is assumed to be both human- and model-readable.
            post_data: A pandas DataFrame containing the model-readable post-processed data that is aligned with the pre-processed data. Can be ignored if model-readable pre-processed data is provided. If providing different pre- and post-processed data, be sure the mapping between them adheres to the feature map of the data collection specified during the data collection's creation.
            ys: Labels for which to compute influences if required by the provided `score_type`. Defaults to None.
            score_type: The score type to use when computing influences. If None, defaults to score type of project. Defaults to None.
            comparison_post_data: The comparison data to use when computing influences. If None, defaults to a data split of the data collection of type "all" or "train" and failing that uses the base split currently set in this explainer. Defaults to None.
            num_internal_qii_samples: Number of samples used internally in influence computations.
            algorithm: Algorithm to use during computation. Must be one of ["truera-qii", "tree-shap-tree-path-dependent", "tree-shap-interventional", "kernel-shap"]. Defaults to "truera-qii".

        Returns:
            pd.DataFrame: The QIIs/shapley-values.
        """
        pass

    @abstractmethod
    def set_segment(self, segment_group_name: str, segment_name: str):
        """Sets and applies a segment filter to all explainer operations.

        Args:
            segment_group_name: Name of segment group under which the segment is defined.
            segment_name: Name of the segment.
        """
        pass

    @abstractmethod
    def clear_segment(self):
        """Clears any set segments from all explainer operations.
        """
        pass

    def get_spline_fitter(
        self, start: int = 0, stop: Optional[int] = None
    ) -> SplineFitter:
        """Get the spline-fitter using the provided range of points to fit splines.

        Args:
            start: The lower bound (inclusive) of the index of points to use during spline fitting. Defaults to 0.
            stop: The upper bound (exclusive) of the index of points to use during spline fitting. Defaults to the number of Number of default influences for the project.

        Returns:
            SplineFitter: Spline-fitter.
        """
        qiis = self.get_feature_influences(start, stop)
        stop = start + qiis.shape[0]
        xs = self.get_xs(start, stop)
        ys = self.get_ys(start, stop)
        return SplineFitter(xs, ys, qiis)

    def list_performance_metrics(self) -> Sequence[str]:
        """
        Lists the available metrics that can be supplied to compute_performance.        
        """
        if self._get_output_type() == "classification":
            if self._get_output_classes() >= 2:
                # multiclass classification
                metrics = CLASSIFICATION_SCORE_ACCURACIES + BINARY_CLASSIFICATION_SCORE_ACCURACIES + MULTICLASS_CLASSIFICATION_SCORE_ACCURACIES
            else:
                # binary classification
                metrics = CLASSIFICATION_SCORE_ACCURACIES + BINARY_CLASSIFICATION_SCORE_ACCURACIES

            if self._get_score_type(
            ) == PREDICTOR_SCORE_TYPE_LOGITS or self._get_score_type(
            ) == PREDICTOR_SCORE_TYPE_PROBITS:
                metrics += PROBITS_OR_LOGITS_SCORE_ACCURACIES
            return [
                AccuracyType.Type.Name(metric)
                for metric in metrics
                if metric not in SEGMENT_GENERALIZED_METRICS
            ]

        elif self._get_output_type() == "regression":
            return [
                AccuracyType.Type.Name(metric)
                for metric in REGRESSION_SCORE_ACCURACIES
            ]
        else:
            # This is a future proofing bug protection error.
            # If we ever expand the output types, the performance metrics need to be updated to support that type.
            raise ValueError(
                f"Unsupported model output type {self._get_output_type()}. Supported types: {VALID_MODEL_OUTPUT_TYPES}."
            )

    @abstractmethod
    def compute_performance(self):
        """Computes performance metrics from labels and predictions. To see the list of available metrics, use list_performance_metrics
        """
        pass

    def _compute_performance(
        self, y_true, y_pred, metric_type: str, threshold: float, plot_roc: bool
    ):
        """
        Backend function for performance metric computation on label and predictions. To see the list of available metrics, use list_performance_metrics

        Args:
            metric_type (str): The metric to calculate from list_performance_metrics. If None, it will calculate all metrics. 
            threshold (float): The classification threshold to convert probas. Default is 0.5.
            plot_roc (bool): a flag on whether to plot the roc curve.

        Returns:
            dict: A dict of metric names to metric values
        """
        allowable_performance_metrics = self.list_performance_metrics()
        if metric_type is None:
            metrics = allowable_performance_metrics
        elif metric_type not in allowable_performance_metrics:
            raise ValueError(
                f"Unsupported performance metric {metric_type}. Available metrics: {allowable_performance_metrics}"
            )
        else:
            metrics = [metric_type]

        multi_dim_output = False
        output_type = self._get_output_type()
        if output_type == "classification":
            multi_dim_output = self._get_output_classes() >= 2 and len(
                y_pred.shape
            ) >= 2

        if multi_dim_output:
            y_pred_idx = np.argmax(y_pred, -1).astype("int32")
        else:
            y_pred_idx = (y_pred >= threshold).astype("int32")

        if plot_roc:
            if multi_dim_output:
                raise ValueError(
                    "plot_roc is set to True, but the project is not binary classification."
                )
            elif output_type == "classification":
                roc_plot(ys=y_true, ys_preds=y_pred)
            else:
                raise ValueError(
                    "plot_roc is set to True, but the project score type is not classification."
                )

        return_dict = {}
        for metric in metrics:
            # pylint: disable=E5902
            metric_type_val = AccuracyType.Type.Value(metric)
            metrics_func, _ = ACCURACY_METRIC_MAP[metric_type_val]
            try:
                ys_to_compare = y_pred_idx if metric_type_val in CLASSIFICATION_SCORE_ACCURACIES + BINARY_CLASSIFICATION_SCORE_ACCURACIES + MULTICLASS_CLASSIFICATION_SCORE_ACCURACIES else y_pred
                kwargs = {
                    "binary": self._get_output_classes() <= 2
                } if output_type == "classification" else {}
                return_dict[metric] = metrics_func(
                    y_true, ys_to_compare, **kwargs
                )
            except Exception as e:
                self.logger.error("{}: {}".format(metric, e))

        return return_dict


class TabularExplainer(Explainer):

    @abstractmethod
    def get_partial_dependencies(
        self,
        wait: bool = True
    ) -> Tuple[Sequence[str], Mapping[str, Sequence], Mapping[str, Sequence]]:
        """Get the partial dependencies for all features. Partial dependencies capture the marginal effect of a feature's value on the predicted outcome of the model.

        Args:
            wait: Whether to wait for the job to finish. Defaults to True.

        Returns:
            Tuple[Sequence[str], Mapping[str, Sequence], Mapping[str, Sequence]]:
                The partial dependencies described in a 3-tuple: A list of the features, a mapping from feature to the x-values in a PDP, and a mapping from feature to the y-values in a PDP.
        """
        pass

    @abstractmethod
    def _get_sorted_features_metric_values(
        self,
        sort_method: FeatureSortMethod = FeatureSortMethod.ABSOLUTE_VALUE_SUM,
        wait: bool = True
    ) -> pd.Series:
        pass

    def _get_sorted_features(
        self,
        sort_method: FeatureSortMethod = FeatureSortMethod.ABSOLUTE_VALUE_SUM,
        wait: bool = True
    ) -> pd.Series:
        """Get pre-features sorted by a method in `intelligence_service.proto::FeatureSortMethod`.

        Args:
            sort_method: Method to sort with.
            wait: Whether to wait for the job to finish. Defaults to True.

        Returns:
            pd.Series: A series with the pre-features as the index and the metric corresponding to the provided `sort_method` as the value. The series will be sorted by the value in descending order.
        """
        self._ensure_data_split()
        ret = self._get_sorted_features_metric_values(sort_method, wait)
        ret = ret.T
        ret["column_names"] = ret.index
        ret = ret.sort_values(
            by=[ret.columns[0], "column_names"], ascending=False
        )
        ret = ret[ret.columns[0]]
        ret.index.name = "Feature"
        ret.name = "Metric"
        return ret

    @abstractmethod
    def get_global_feature_importances(
        self,
        score_type: Optional[str] = None,
        wait: bool = True
    ) -> pd.DataFrame:
        """Get the global feature importances (as measured by QIIs) for this explainer's currently set data split.

        Args:
            score_type: The score type to use when computing influences. If None, defaults to score type of project. Defaults to None.
            wait: Whether to wait for the job to finish.

        Returns:
            pd.DataFrame: The normalized global importances for each feature. 
        """
        pass

    @abstractmethod
    def list_performance_metrics(self) -> Sequence[str]:
        """Lists all available performance metrics.

        Returns:
            Sequence[str]: List of performance metric names, which can be provided to `compute_performance`. 
           
        """
        pass

    @abstractmethod
    def compute_fairness(
        self,
        segment_group: str,
        segment1: str,
        segment2: Optional[str] = None,
        fairness_type: Optional[str] = 'DISPARATE_IMPACT_RATIO',
        threshold: Optional[float] = None,
        threshold_score_type: Optional[str] = None,
    ) -> BiasResult:
        """Compares the fairness of outcomes for two segments within a segment group using the provided fairness type.

        Args:
            segment_group: Name of segment group that the two segments are defined under.
            segment1: Name of first segment (must belong to provided segment group). 
            segment2: Name of second segment (must belong to provided segment group). If None, then uses the complement of `segment1`.
            fairness_type: Name of fairness metric. Must be one of the options returned by `list_fairness_metrics`.
            threshold: Optional model threshold for classification models. If None, defaults to pre-configured threshold for the model. Ignored for regression models.
            threshold_score_type: If `threshold` is provided, the score type to apply the threshold to (`probits` or `logits`). If None, defaults to pre-configured score type for the model. Ignored for regression models.

        Returns:
           BiasResult: Computed fairness metric along with information about which group is favored. 
        """
        pass

    @abstractmethod
    def _compute_performance_df(
        self,
        metric_type: str,
        compute_for_comparison_data_splits: bool = True
    ) -> pd.DataFrame:
        """Compute performance metrics for all splits (base and comparison) that are set in the current context. 
        Args:
            metric_type: Name of performance metric. Must be one of the options returned by `list_performance_metrics`.
            compute_for_comparison_data_splits: Whether to report on comparison data splits. Defaults to True.
        Returns:
            pd.DataFrame: Table containing each split name and its performance metric. 
        """
        pass

    @abstractmethod
    def _compute_model_score_instability_df(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        """Compute model score instability from the base split to all comparison splits that are set in the current context. By default, instability is measured using Wasserstein Distance. 
        Args:
            score_type: The score type to use when computing instability. If None, uses default score type of project. Defaults to None.
            use_difference_of_means: If True, measures instability with Difference of Means. Defaults to False.
        Returns:
            pd.DataFrame: Table containing each comparison split name and its model score instability from the base split. 
        """

    def compute_model_score_instability(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False,
        plot: bool = False
    ) -> Union[float, pd.DataFrame]:
        """Compute model score instability from the base split to all comparison splits that are set in the current context. By default, instability is measured using Wasserstein Distance. 
        Args:
            score_type: The score type to use when computing instability. If None, uses default score type of project. Defaults to None.
            use_difference_of_means: If True, measures instability with Difference of Means. Defaults to False.
            plot: If True, plots performances for all base and comparison splits in the current context. 
        Returns:
            Union[float, pd.DataFrame]: The model score instability. If comparison data splits are set, a pd.DataFrame of all splits and their respective score instabilities. Otherwise, a single float metric is returned.
        """
        stability_data = self._compute_model_score_instability_df(
            score_type, use_difference_of_means=use_difference_of_means
        )
        if plot:
            base_split = stability_data["Base Split"].values[0]
            viz.basic_bar_graph(
                stability_data.sort_values(
                    by="Model Score Instability", ascending=False
                ), "Model Score Instability", "Comparison Split",
                f"Model Score Instability from Split {base_split}"
            )
        return stability_data if len(stability_data) > 1 else stability_data[
            "Model Score Instability"].values[0]

    @abstractmethod
    def compute_feature_contributors_to_instability(
        self,
        score_type: Optional[str] = None,
        use_difference_of_means: bool = False
    ) -> pd.DataFrame:
        """Compute feature contributors to model instability from the base split to all comparison splits that are set in the current context. By default, instability is measured using Wasserstein Distance.
        Args:
            score_type: The score type to use when computing instability. If None, uses default score type of project. Defaults to None.
            use_difference_of_means: If True, measures instability with Difference of Means. Defaults to False.
        
        Returns:
            pd.DataFrame: Table of contributions per feature and comparison split. 
        """
        pass

    def compute_performance(self,
                            metric_type: str,
                            plot: bool = False) -> Union[float, pd.DataFrame]:
        """Compute performance metric.
        Args:
            metric_type: Name of performance metric. Must be one of the options returned by `list_performance_metrics`.
            plot: If True, plots performances for all base and comparison splits in the current context. 
        Returns:
            Union[float, pd.DataFrame]: The performance metric. If comparison data splits are set, a pd.DataFrame of all splits and their respective performance. Otherwise, a single float metric is returned. 
        """
        performance_data = self._compute_performance_df(metric_type)
        if plot:
            viz.basic_bar_graph(
                performance_data.sort_values(by=metric_type, ascending=False),
                metric_type, "Split", None
            )
        return performance_data if len(
            performance_data
        ) > 1 else performance_data[metric_type].values[0]

    @abstractmethod
    def rank_performance(
        self, metric_type: str, ascending: bool = False
    ) -> pd.DataFrame:
        """Rank performance of all models in the data collection on the explainer's base data split. If comparison data splits are set, will also show performance of the models on them.
        Args:
            metric_type: Name of performance metric. Must be one of the options returned by `list_performance_metrics`.
            ascending: If True, sort the results in ascending order. Defaults to False.
        Returns:
            pd.DataFrame: The performance score of all models in the data collection.
        """
        pass

    def _validate_suggest_high_error_segments(
        self, segment_type: Optional[str],
        metric_types: Optional[Union[str, Sequence[str]]], score_type: str,
        comparison_data_split_name: Optional[str]
    ) -> Tuple[Sequence[str], int]:
        self._ensure_data_split()
        if not metric_types:
            metric_types = []
        if isinstance(metric_types, str):
            metric_types = [metric_types]
        if is_regression_score_type(score_type):
            default_segment_type = "HIGH_MEAN_ABSOLUTE_ERROR"
            valid_segment_type_to_metric_type = {
                "HIGH_MEAN_ABSOLUTE_ERROR": "MAE",
                "HIGH_MEAN_SQUARED_ERROR": "MSE",
                "HIGH_MEAN_SQUARED_LOG_ERROR": "MSLE"
            }
        else:
            default_segment_type = "LOW_POINTWISE_AUC"
            valid_segment_type_to_metric_type = {
                "LOW_POINTWISE_AUC": "SEGMENT_GENERALIZED_AUC",
                "LOW_CLASSIFICATION_ACCURACY": "CLASSIFICATION_ACCURACY",
            }
        if segment_type is None:
            segment_type = default_segment_type
        if segment_type not in valid_segment_type_to_metric_type:
            raise ValueError(
                f"`segment_type` must be one of {valid_segment_type_to_metric_type.keys()}"
            )
        corresponding_metric_type = valid_segment_type_to_metric_type[
            segment_type]
        metric_types = [corresponding_metric_type] + [
            curr for curr in metric_types if curr != corresponding_metric_type
        ]
        if comparison_data_split_name is not None:
            self._validate_data_split(comparison_data_split_name)
        return metric_types, InterestingSegment.Type.Value(segment_type)

    @abstractmethod
    def _validate_data_split(self, data_split_name: str) -> None:
        pass

    @abstractmethod
    def suggest_high_error_segments(
        self,
        num_features: int = 1,
        max_num_responses: int = 3,
        num_samples: int = 100,
        metric_types: Optional[Union[str, Sequence[str]]] = None,
        minimum_size: int = 50,
        size_exponent: float = 0.25,
        comparison_data_split_name: Optional[str] = None,
        random_state: int = 0,
    ) -> pd.DataFrame:
        """Suggests high error segments for the model for the currently set data split.

        Args:
            num_features: Number of features to use to describe a high error segment. Defaults to 1.
            max_num_responses: Maximum number of high error segments to return. Defaults to 3.
            num_samples: Number of samples to use while attempting to find high error segments. The higher the number of samples the slower the computation, but the better the high error segments are generally. Defaults to 100.
            metric_types: Name of performance metric or list of them to include. Must be one of the options returned by `list_performance_metrics`. Defaults to None.
            minimum_size: Minimum size of a segment. Defaults to 50.
            size_exponent: Exponential factor on size of segment. Should be in [0, 1]. A zero value implies the segment size has no effect. Defaults to 0.25.
            comparison_data_split_name: Comparison data-split to use (e.g. train split for overfitting analysis). If set, we look for segments that are far more problematic in the explainer's data split than the comparison one supplied here.
            random_state: Random seed. Defaults to 0.

        Returns:
            pd.DataFrame: DataFrame describing high error segments. Each row corresponds to a suggested high error segment, with the following columns:
                1. representation: The segment description. This can be ingested via the workspace add_segment_group function.
                2. size: The number of points in this segment in total.
                3. size (%): The percentage of points in this segment.
            There'll also be additional columns corresponding to a metric used to compute the segments along with a column for each metric in `metric_types`.
        """
        pass

    def plot_pdp(
        self,
        feature: str,
        figsize: Optional[Tuple[int, int]] = (700, 500),
        xlim: Optional[Tuple[int, int]] = None
    ) -> None:
        """Plot the partial dependence plot (PDP) of a specific feature.

        Args:
            feature: Feature to plot the PDP of.
            figsize: Size for plot. Defaults to (21, 6).
            xlim: Range for x-axis. Defaults to None, which scales to the size of the data.
        """
        partial_dependencies = self.get_partial_dependencies()
        xs = partial_dependencies[1]
        ys = partial_dependencies[2]
        viz.plot_pdp(feature, xs, ys, figsize, xlim)

    def plot_pdps(
        self,
        features: Optional[Sequence[str]] = None,
        figsize: Optional[Tuple[int, int]] = (700, 500)
    ) -> None:
        """Plot the partial dependence plot (PDP) of a set of features.

        Args:
            features: Features to plot the PDP of. Defaults to None, which is all features.
            figsize: Size for plot. Defaults to (21, 6).
        """
        partial_dependencies = self.get_partial_dependencies()
        all_prefeatures = partial_dependencies[0]
        xs = partial_dependencies[1]
        ys = partial_dependencies[2]
        features = features or all_prefeatures
        for feature in features:
            viz.plot_pdp(feature, xs, ys, figsize, None)

    def plot_isp(
        self,
        feature: str,
        num: Optional[int] = None,
        figsize: Optional[Tuple[int, int]] = (700, 500),
        xlim: Optional[Tuple[int, int]] = None
    ) -> None:
        """Plot the influence sensitivity plot (ISP) of a specific feature.

        Args:
            feature: Feature to plot the ISP of.
            num: Number of points to plot. Defaults to None, which is equivalent to a standard number of points used for calculations.
            figsize: Size for plot in pixels. Defaults to (700, 500).
            xlim: Range for x-axis. Defaults to None, which scales to the size of the data.
        """
        start = 0
        qiis = self.get_feature_influences(start=start, stop=num)
        vals = self.get_xs(start=start, stop=num).head(
            len(qiis)
        )  # may need to slice based on segments
        viz.plot_isp(feature, vals, qiis, figsize, xlim)

    def plot_isps(
        self,
        features: Optional[Sequence[str]] = None,
        num: Optional[int] = None,
        figsize: Optional[Tuple[int, int]] = (700, 500)
    ) -> None:
        """Plot the influence sensitivity plot (ISP) of a set of features.

        Args:
            features: Features to plot the ISP of. Defaults to None, which is all features.
            num: Number of points to plot. Defaults to None, which is equivalent to a standard number of points used for calculations.
            figsize: Size for plot. Defaults to (21, 6).
        """
        start = 0
        qiis = self.get_feature_influences(start=start, stop=num)
        vals = self.get_xs(start=start, stop=num).head(len(qiis))
        if features is None:
            importances = self._get_sorted_features()
            features = importances.index
        for feature in features:
            viz.plot_isp(feature, vals, qiis, figsize, None)

    def _validate_metric_type(self, metric_type: str):
        if metric_type not in self.list_performance_metrics():
            raise ValueError(
                f"Unsupported performance metric {metric_type}. Use `list_performance_metrics()` to see a list of available options."
            )


class NonTabularExplainer(Explainer):

    def __init__(
        self, model: Model, data_collection: DataCollection, data_split: str,
        project: Project, attr_config: AttributionConfiguration,
        explanation_cache: Cache, logger: logging.Logger
    ):

        self._base_data_split = None
        self._project = project
        self._data_collection = data_collection
        self._logger = logger
        self._attr_config = attr_config
        self._model = model
        self._explanation_cache = explanation_cache
        self.set_base_data_split(data_split)

    @property
    def logger(self):
        return self._logger

    def _convert_start_stop(
        self,
        start: Optional[int],
        stop: Optional[int],
        metrics_count: bool = True
    ) -> Tuple[int, int]:
        if start is None:
            start = 0
        if stop is None:
            if hasattr(
                self._attr_config, "n_metrics_records"
            ) and self._attr_config.n_metrics_records:
                if metrics_count:
                    stop = self._attr_config.n_metrics_records
                else:
                    stop = min(
                        self._attr_config.n_metrics_records,
                        self._project.num_default_influences
                    )
            else:
                stop = self._project.num_default_influences

        if start >= stop:
            raise ValueError("`start` must be less than `stop`!")
        return start, stop

    def _set_cache_dir(self, source_cache_dir: str, hash_bg: str) -> None:
        '''
        Changes the cache to a new directory. Will copy files and reset artifact locator metadata.

        Args:
            source_cache_dir: The new cache directory
        '''
        from truera.rnn.general.container.artifacts import ArtifactsContainer
        from truera.rnn.general.service.sync_service import SyncService
        cache_dir = self._explanation_cache.get_temp_dir(
            project_name=self._project.name,
            model_name=self._model.name,
            data_collection_name=self._data_collection.name,
            data_split_name=self._base_data_split.name,
            hash_bg=hash_bg,
            score_type=self._get_score_type(),
            algorithm=ExplanationAlgorithmType.INTEGRATED_GRADIENTS
        )
        shutil.rmtree(cache_dir.name)
        shutil.copytree(source_cache_dir, cache_dir.name)
        # pylint: disable=not-callable
        self.sync_client = SyncService(
            cache_dir.name,
            needs_local_proxy_cache=False,
            local_workspace_mode=True
        )

        # pylint: disable=not-callable
        self._artifacts_container = ArtifactsContainer(
            self.sync_client, locator=self._artifacts_container.locator
        )
