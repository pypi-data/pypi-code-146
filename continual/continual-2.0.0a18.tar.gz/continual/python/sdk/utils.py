from typing import List, Union, Optional
import pandas as pd
from pandas.api.types import (
    is_numeric_dtype,
    is_string_dtype,
    is_bool_dtype,
    is_categorical_dtype,
)
from datetime import datetime
import numpy as np
from collections import Counter
from continual.python.sdk.model_versions import ModelVersion
from sklearn.metrics import confusion_matrix
from sklearn.utils import Bunch

from continual.python.sdk.metadata import Metadata


def _get_non_unique_index_count(df, index_col="ID", time_index_col=None):
    if index_col is not None and index_col in df.columns:
        if time_index_col is not None and time_index_col in df.columns:
            return int(df[[index_col, time_index_col]].duplicated().sum())
        else:
            return int(df[[index_col]].duplicated().sum())
    else:
        return None


def _get_feature_analysis(
    data: pd.DataFrame,
    datetime_columns: List[str],
    index_column: str,
):
    # this function will return count, mean, std, min, Q1, Q2, Q3, and max of all the features in the df
    timestamp_list = []
    numerical_list = []
    string_list = []
    categorical_list = []

    for col in data.columns:
        if datetime_columns is not None and col in datetime_columns:
            null_count = None
            temp_timecol_stats = None
            min_dt_ = None  # Likely to run into "ERROR    NaTType does not support utctimetuple" if these are not separately obtained.
            max_dt_ = None
            if data[col].isna().all():
                temp_timecol = data[col]
                null_count = len(data[col])
                temp_timecol = pd.to_datetime(temp_timecol.fillna("01-01-1970"))
                print("All NaT detected - using epoch start time for data statistics")
                temp_timecol_stats = temp_timecol.describe(
                    datetime_is_numeric=True
                ).to_dict()
                min_dt_ = temp_timecol_stats["min"]
                max_dt_ = temp_timecol_stats["max"]

            data_tcol = pd.to_datetime(data[col], utc=True).dt.tz_localize(None)
            return_dict_ = (
                temp_timecol_stats
                if temp_timecol_stats
                else data_tcol.describe(datetime_is_numeric=True).to_dict()
            )

            return_dict_["column_name"] = str(col)
            return_dict_["distinct_values"] = len(data[col].unique())

            return_dict_["null_count"] = (
                null_count if null_count else int(data_tcol.isnull().sum())
            )

            return_dict_["min"] = min_dt_ if min_dt_ else data_tcol.min()
            return_dict_["max"] = max_dt_ if max_dt_ else data_tcol.max()
            return_dict_.pop("25%")
            return_dict_.pop("50%")
            return_dict_.pop("75%")
            return_dict_.pop("count")
            return_dict_.pop("mean")

            histogram_ = {}
            histogram_["num_undefined"] = return_dict_["null_count"]
            return_histo_ = []

            counts_, bins_ = np.histogram(
                pd.to_datetime(data_tcol.dropna()).astype(int) // 10 ** 9
            )
            bins_ = list(zip(bins_.tolist(), bins_.tolist()[1:]))
            for i, (count_, bin_) in enumerate(zip(counts_, bins_)):
                low_dt = datetime.fromtimestamp(bin_[0])
                high_dt = datetime.fromtimestamp(bin_[1])
                return_histo_.append(
                    {
                        "low_value": low_dt,
                        "high_value": high_dt,
                        "sample_count": int(count_),
                    }
                )
            histogram_["buckets"] = return_histo_
            return_dict_["timestamp_histogram"] = histogram_
            for k, v in return_dict_.items():
                if type(v) == float and np.isnan(v):
                    return_dict_[k] = 0.0
            timestamp_list.append(return_dict_)
            continue

        if col == index_column:
            col_type = _get_column_type(data, col, threshold=0)
        else:
            col_type = _get_column_type(data, col)

        if is_numeric_dtype(col_type):
            temp_col_stats = None
            if data[col].isna().all():
                temp_data = data[col]
                temp_data = temp_data.fillna(0)
                if temp_data.dtype.kind != "f":
                    temp_data = temp_data.astype(float)
                temp_col_stats = temp_data.describe().to_dict()
            return_dict_ = (
                temp_col_stats
                if temp_col_stats
                else pd.to_numeric(data[col]).describe().to_dict()
            )

            return_dict_["column_name"] = str(col)
            return_dict_["percentile25"] = return_dict_.pop("25%")
            return_dict_["percentile50"] = return_dict_.pop("50%")
            return_dict_["percentile75"] = return_dict_.pop("75%")
            return_dict_["count"] = int(return_dict_.pop("count"))
            return_dict_["sd"] = return_dict_.pop("std")
            return_dict_["num_nan"] = int(data[col].isna().sum())
            return_dict_["null_count"] = int(data[col].isnull().sum())
            return_dict_["distinct_values"] = len(data[col].unique())

            # getting histograms
            counts_, bins_ = np.histogram(data[col].dropna().to_list())
            bins_ = list(zip(bins_.tolist(), bins_.tolist()[1:]))

            histogram_ = {}
            histogram_["num_nan"] = return_dict_["num_nan"]
            histogram_["num_undefined"] = return_dict_["null_count"]
            return_histo_ = []
            for i, (count_, bin_) in enumerate(zip(counts_, bins_)):
                return_histo_.append(
                    {
                        "low_value": bin_[0],
                        "high_value": bin_[1],
                        "sample_count": int(count_),
                    }
                )
            histogram_["buckets"] = return_histo_
            return_dict_["num_values_histogram"] = histogram_
            for k, v in return_dict_.items():
                if type(v) == float and np.isnan(v):
                    return_dict_[k] = 0.0
            numerical_list.append(return_dict_)

        elif is_string_dtype(col_type):
            return_dict_ = {
                "column_name": str(col),
                "distinct_values": len(data[col].unique()),  # this is risky!
                "null_count": int(data[col].isna().sum()),
                "min_length": 0,
                "max_length": 0,
            }
            if not data[col].isna().all():
                return_dict_["min_length"] = min(data[col].dropna().str.len())
                return_dict_["max_length"] = max(data[col].dropna().str.len())
            string_list.append(return_dict_)
        elif is_categorical_dtype(col_type) or is_bool_dtype(col_type):
            unique_ = data[col].unique()
            return_dict_ = {
                "column_name": str(col),
                "distinct_values": len(unique_),
                "null_count": data[data[col].isna()].shape[0],
                "categorical_distribution": None,
            }
            counts_ = Counter(data[col].dropna().to_list())
            cd_ = []
            category_count = 0
            histogram_max_size = 30
            remaining_count_name = "Additional Categories"
            remaining_count_sum = 0
            sorted_counts_ = dict(
                sorted(counts_.items(), key=lambda item: item[1], reverse=True)
            )

            for k, v in sorted_counts_.items():
                if category_count > histogram_max_size:
                    remaining_count_sum += v
                else:
                    cd_.append(
                        {
                            "label": str(k),
                            "sample_count": v,
                        }
                    )
                category_count += 1

            if remaining_count_sum > 0:
                cd_.append(
                    {
                        "label": remaining_count_name,
                        "sample_count": remaining_count_sum,
                    }
                )
            if return_dict_["null_count"] > 0:
                cd_.append(
                    {
                        "label": "null",
                        "sample_count": return_dict_["null_count"],
                    }
                )
            return_dict_["categorical_distribution"] = {"categories": cd_}
            categorical_list.append(return_dict_)
    return numerical_list, string_list, categorical_list, timestamp_list


def _get_correlation_matrix(df):
    # this will give a dictionary of dictionaries accessible by res[feat_1][feat_2]
    tmp_df = df.corr().to_dict()
    cm = {
        "display_names": [],
        "rows": [],
    }
    display_names_ = []
    for k, t in tmp_df.items():
        kcol_type = _get_column_type(df, k)
        if not kcol_type:
            continue
        display_names_.append(k)
        t_ = []
        for k2, t2 in t.items():
            col_type = _get_column_type(df, k2)
            if not col_type:
                continue
            # golang json marshalling doesn't support NaN of Inf so replace with 0
            # TODO: may want to create custom golang marshaler to handle.
            if pd.isna(t2):
                t2 = 0
            t_.append(t2)
        cm["rows"].append({"correlations": t_})
    cm["display_names"] = display_names_
    return cm


def _get_column_type(df, col, threshold=150):
    """Returns column type from pandas dataframe"""
    unique_ = df[col].unique()
    if df[col].shape[0] >= threshold:
        if df[col].dtype != "object" and len(unique_) >= threshold:
            return df[col].dtype
        elif df[col].dtype == "object" and len(unique_) >= threshold:
            return pd.StringDtype()
        elif len(unique_) < threshold:
            return pd.CategoricalDtype(categories=unique_, ordered=False)
        else:
            raise NotImplementedError
    else:
        return _get_column_type(df, col, threshold // 2)


def _get_dataset_ranges(
    data: pd.DataFrame,
    columns: List[str],
):
    ranges = []
    for col in columns:
        if not data[col].isna().all():
            data_tcol = pd.to_datetime(data[col]).dt.tz_localize(None)
            start_dt = data_tcol.min()
            end_dt = data_tcol.max()
            ranges.append({"name": col, "start_time": start_dt, "end_time": end_dt})
    return ranges


def create_sklearn_confusion_matrix(
    model_version: ModelVersion,
    display_name: str,
    group_name: str,
    y_true: list,
    y_pred: list,
    labels: list = None,
    sample_weight: list = None,
    normalize: bool = None,
) -> Metadata:
    """Creates confusion matrix metadata on this model version.

    Arguments:
        model_version: The model version to create the confusion matrix on
        display_name: The display name of the confusion matrix
        group_name: A label associated with the group of the confusion matrix
        y_true: Ground truth labels
        y_pred: Predictions from a model version
        labels: Labels
        sample_weight: Optional sample weights
        normalize: Whether to normalize.

    Returns:
        Confusion matrix type metadata

    Examples:
        >>> from continual.python.utils import create_sklearn_confusion_matrix
        >>> ... # Assume continual client is initialized
        >>> run = client.runs.create(description="An example run")
        >>> model_version = run.models.create("example_model").model_versions.create()
        >>> y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
        >>> y_pred = ["ant", "ant", "cat", "cat", "ant", "cat"]
        >>> labels = ["ant", "bird", "cat"]
        >>> create_sklearn_confusion_matrix(
        ...     model_version=model_version,
        ...     display_name="example_confusion_matrix",
        ...     group_name="test",
        ...     y_true=y_true,
        ...     y_pred=y_pred,
        ...     labels=labels,
        ... )
        <Metadata object {'name': 'projects/delgado_inc/environments/production/models/test_model/versions/cemaiqa5lsrtm2p150j0/metadata/cemaiqa5lsrtm2p150kg',
        'key': 'example_confusion_matrix', 'create_time': '2022-12-28T20:39:05.344420Z', 'update_time': '2022-12-28T20:39:05.344420Z',
        'data': '{"rows": [[2, 0, 0], [0, 0, 1], [1, 0, 2]], "display_name": "example_confusion_matrix"}', 'type': 'CONFUSION_MATRIX', 'group_name': 'test'}>
    """
    matrix = confusion_matrix(
        y_true=y_true,
        y_pred=y_pred,
        labels=labels,
        sample_weight=sample_weight,
        normalize=normalize,
    )
    return model_version.metadata.create(
        key=display_name,
        type="CONFUSION_MATRIX",
        data=dict(display_name=display_name, rows=matrix.astype(np.uint).tolist()),
        group_name=group_name,
    )


def feature_importance_from_sklearn(
    model_version: ModelVersion,
    display_name: str,
    feature_names: List[str],
    importance_result: Union[Bunch, dict],
    dataset_version_names: Optional[List[str]] = None,
) -> Metadata:
    """Creates feature importance metadata from sklearn result.

    Arguments:
        model_version: The model version on which to create the feature importance.
        display_name: The display name of the feature importance.
        feature_names: The names of the features in the order that the importancs are in.
        dataset_version_names: The name of the dataset version on which the feature importance was computed.
        importance_result: The result from sklearn's inspection.permutation_importance method.

    Returns:
        Feature importance type metadata

    Examples:
        >>> from continual.python.utils import feature_importance_from_sklearn
        >>> ... # Assume continual client is initialized
        >>> run = client.runs.create(description="An example run")
        >>> model_version = run.models.create("example_model").model_versions.create()
        >>> dataset_version = run.datasets.create("example_dataset").dataset_versions.create()
        >>> X = [[1, 9, 9], [1, 9, 9], [1, 9, 9], [0, 9, 9], [0, 9, 9], [0, 9, 9]]
        >>> y = [1, 1, 1, 0, 0, 0]
        >>> clf = LogisticRegression().fit(X, y)
        >>> result = permutation_importance(clf, X, y, n_repeats=10, random_state=0)
        >>> feature_importance_from_sklearn(
        ...     model_version=model_version,
        ...     display_name="example_feature_importance",
        ...     feature_names=["feature1", "feature2", "feature3"],
        ...     dataset_version_names=[dataset_version.name],
        ...     importance_result=result,
        ... )
        <Metadata object {'name': 'projects/johnson_mcbride_and_wilk/environments/production/models/test_model/versions/cemakbq5lsrtm2p150sg/metadata/cemakbq5lsrtm2p150u0',
        'key': 'example_feature_importance', 'create_time': '2022-12-28T20:42:23.815825Z', 'update_time': '2022-12-28T20:42:23.815825Z',
        'data': '{"importances": {"feature1": [0.33333333333333337, 0.6666666666666667, 0.33333333333333337, 0.33333333333333337, 0.6666666666666667, 1.0, 0.33333333333333337, 0.33333333333333337, 0.33333333333333337, 0.33333333333333337],
        "feature2": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "feature3": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, "dataset_version_name": "test_dataset_version_name"}', 'type': 'FEATURE_IMPORTANCE', 'group_name': ''}>
    """

    return model_version.metadata.create(
        key=display_name,
        type="FEATURE_IMPORTANCE",
        data={
            "dataset_version_names": dataset_version_names,
            "importances": {
                feature_names[i]: importance_result["importances"].tolist()[i]
                for i in range(len(feature_names))
            },
        },
    )
