from abc import ABC
from abc import abstractmethod
from typing import Mapping, Optional, Sequence, Union

import pandas as pd

from truera.client.ingestion_client import Table


class DataProfiler(ABC):

    @abstractmethod
    def get_data_quality_metrics(
        self,
        feature_name: Optional[str] = None,
        metric_name: Optional[str] = None,
        comparison_data_splits: Optional[Sequence[str]] = None,
        normalize: bool = False
    ) -> Mapping[str, Union[pd.Series, pd.DataFrame]]:
        """[Alpha] Get data quality metrics for the current data split that is set in the context and the list of splits specified in the `comparison_data_splits` 

        Args:
            feature_name (optional): Filter results to metrics for the given `feature_name`.
            metric_name (optional): Filter results to metrics for the given `metric_name`. Must be one of ["OUT_OF_RANGE", "NEW_CATEGORICAL_VALUES", "MISSING_VALUES", "NAN_VALUES", "INFINITY_VALUES"].
            comparison_data_splits (optional): Get the data quality metrics for the data splits specified in this arguments (in addition to the data split in context).
            normalize: If set to `True`, normalize the results according to the size of the corresponding data splits. Defaults to `False`.

        Returns:
            A dictionary with the data split names as the key and pd.DataFrame or pd.Series as the metric result.
        """
        pass

    @abstractmethod
    def plot_data_quality_metrics(
        self,
        feature_name: str,
        metric_name: str,
        comparison_data_splits: Optional[Sequence[str]] = None,
        normalize: bool = False
    ) -> None:
        """[Alpha] Plot data quality metrics for the current data split that is set in the context and and the list of splits specified in the `comparison_data_splits` 

        Args:
            feature_name (optional): Filter results to metrics for the given `feature_name`.
            metric_name (optional): Filter results to metrics for the given `metric_name`. Must be one of ["OUT_OF_RANGE", "NEW_CATEGORICAL_VALUES", "MISSING_VALUES", "NAN_VALUES", "INFINITY_VALUES"].
            comparison_data_splits (optional): Plot the data quality metrics for the data splits specified in this arguments (in addition to the data split in context).
            normalize: If set to `True`, normalize the results according to the size of the corresponding data splits. Defaults to `False`.
        """
        pass

    @abstractmethod
    def get_data_quality_metrics_definition(
        self,
        feature_name: str,
        metric_name: Optional[str] = None,
    ) -> Union[str, Mapping[str, str]]:
        """[Alpha] Get human readable definition of the data quality metrics for a given feature.

        Args:
            feature_name: Feature of interest.
            metric_name (optional): Filter results to metrics for the given `metric_name`. Must be one of ["OUT_OF_RANGE", "NEW_CATEGORICAL_VALUES", "MISSING_VALUES", "NAN_VALUES", "INFINITY_VALUES"].

        Returns:
            The metric definition (if `metric_name` is provided), or a dictionary containing all metrics for the feature. 
        """
        pass

    @abstractmethod
    def update_data_quality_metric_constraint(
        self,
        feature_name: str,
        metric_name: str,
        *,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        categorical_values: Optional[Sequence] = None
    ) -> None:
        """[Alpha] Update the constraint for a given data quality metric.

        Args:
            feature_name: Feature of interest.
            metric_name: Metric of interest. Must be one of ["OUT_OF_RANGE", "NEW_CATEGORICAL_VALUES"]
            min_value (float): Minimum value (inclusive) of the "OUT_OF_RANGE" metric.
            max_value (float): Maximum value (inclusive) of the "OUT_OF_RANGE" metric.
            categorical_values (list): List of expected categorical values for the feature.  
        """
        pass

    @abstractmethod
    def get_data_quality_rule_threshold_and_operator(
        self,
        feature_name: str,
        metric_name: Optional[str] = None
    ) -> Mapping[str, Mapping[str, str]]:
        """[Alpha] Get the current  data quality metrics threshold and operator for a given feature.

        Args:
            feature_name: Feature of interest.
            metric_name (optional): Filter results to metrics for the given `metric_name`. Must be one of ["OUT_OF_RANGE", "NEW_CATEGORICAL_VALUES", "MISSING_VALUES", "NAN_VALUES", "INFINITY_VALUES"].

        Returns:
            A dictionary containing the data quality rule threshold and operator
        """
        pass

    @abstractmethod
    def update_data_quality_rule_threshold_and_operator(
        self,
        feature_name: str,
        metric_name: str,
        violation_threshold: float,
        operator: str,
        treat_threshold_as_raw_count: bool = False
    ) -> None:
        """[Alpha] Update the threshold and operator for a given data quality metric on a given feature.

        Args:
            feature_name: Feature of interest.
            metric_name: Metric of interest. Must be one of ["OUT_OF_RANGE", "NEW_CATEGORICAL_VALUES", "MISSING_VALUES", "NAN_VALUES", "INFINITY_VALUES"].
            violation_threshold: The new violation threshold.
            operator: Rule operator. Must be one of ["EQUAL", "LESS_THAN", "LESS_THAN_OR_EQUAL", "GREATER_THAN", "GREATER_THAN_OR_EQUAL"]
            treat_threshold_as_raw_count: If set to `True`, treat violation_threshold as raw count. Otherwise, treat it as a ratio (must be between [0.0-1.0]). Defaults to `False`.
        """
        pass

    @abstractmethod
    def initialize_data_quality_constraints_from_data_split(
        self, data_split_name: str, overwrite: bool = False
    ) -> None:
        """[Alpha] Initialize all data quality constraints for the data collection in context using `data_split_name` as a reference.

        Args:
            data_split_name: The data split that we want to set as reference.
            overwrite: If set to `True`, will overwrite existing constraints (if any have been initialized). Defaults to `False`.
        """
        pass

    @abstractmethod
    def compute_feature_drift(
        self,
        comparison_data_splits: Sequence[str],
        feature_names: Optional[Sequence[str]] = None,
        distance_metrics: Optional[Sequence[str]] = None
    ) -> Mapping[str, pd.DataFrame]:
        """ Compute feature drift on metrics specified in `distance_metrics` between the current data split that is set in the context and and the list of splits specified in the `comparison_data_splits`.

        Args:
            comparison_data_splits: Compute drift scores for the data splits specified in this arguments.
            feature_names (optional): Filter results for features spcified in this argument. Otherwise will compute results for all features.
            distance_metrics (optional): The drift metric(s) to be computed. If not specified will compute results for all metrics. Valid metrics for categorical features: ["CATEGORICAL_WASSERSTEIN_UNORDERED", "CATEGORICAL_WASSERSTEIN_ORDERED", "TOTAL_VARIATION_DISTANCE", "CATEGORICAL_JENSEN_SHANNON_DISTANCE", "CHI_SQUARE_TEST", "CATEGORICAL_POPULATION_STABILITY_INDEX", "L1". "L2", "LInfinity"]. For numerical features: ["NUMERICAL_WASSERSTEIN", "DIFFERENCE_OF_MEAN", "NUMERICAL_JENSEN_SHANNON_DISTANCE", "ENERGY_DISTANCE", "KOLMOGOROV_SMIRNOV_STATISTIC", "NUMERICAL_POPULATION_STABILITY_INDEX"].

        Returns:
            A dictionary with the data split names as the key and pd.DataFrame containing the drift scores for each features.
        """
        pass

    @abstractmethod
    def plot_feature_drift(
        self,
        comparison_data_splits: Sequence[str],
        distance_metric: str,
        feature_names: Optional[Sequence[str]] = None,
        minimum_score: int = 0.0
    ) -> None:
        """ Plot feature drift scores between the current data split that is set in the context and and the list of splits specified in the `comparison_data_splits`.

        Args:
            comparison_data_splits: Compute drift scores for the data splits specified in this arguments.
            distance_metric: The drift metric to be computed. Valid metrics for categorical features: ["CATEGORICAL_WASSERSTEIN_UNORDERED", "CATEGORICAL_WASSERSTEIN_ORDERED", "TOTAL_VARIATION_DISTANCE", "CATEGORICAL_JENSEN_SHANNON_DISTANCE", "CHI_SQUARE_TEST", "CATEGORICAL_POPULATION_STABILITY_INDEX", "L1". "L2", "LInfinity"]. For numerical features: ["NUMERICAL_WASSERSTEIN", "DIFFERENCE_OF_MEAN", "NUMERICAL_JENSEN_SHANNON_DISTANCE", "ENERGY_DISTANCE", "KOLMOGOROV_SMIRNOV_STATISTIC", "NUMERICAL_POPULATION_STABILITY_INDEX"].
            feature_names (optional): Filter results for features spcified in this argument. Otherwise will show results for all features.
            minimum_score (optional): Filter out features whose score are less than or equal to what is specified in this argument. Defaults to 0.
        """
        pass

    @abstractmethod
    def get_schema_mismatch_rows_for_split(
        self,
        data_kind_str: str,
        data_split_name: str = None,
        *,
        feature_name: Optional[str] = None
    ) -> pd.DataFrame:
        """ Fetches a pd.DataFrame of all rows where at least one column contained a schema mismatch
            issue, in that its value could not be parsed into the provided datatype of the column.
            These corrupt records are generated during data ingestion.
            If feature name is populated, only rows with schema mismatch for given feature are returned.

        Args:
            data_kind_str: Type of ingested data.
            data_split_name: Split name.
        """
        pass
