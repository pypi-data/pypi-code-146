################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2021, 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

from typing import Tuple, Union
from autoai_ts_libs.utils.messages.messages import Messages
from autoai_ts_libs.utils.data_processor import DataProcessor
from autoai_ts_libs.utils.data_helper import DataHelper
from autoai_ts_libs.utils.pipeline_utils import PipelineUtils
from autoai_ts_libs.utils.constants import (
    DataType,
    GLOBAL_DEFAULT_SEED, COLUMN_ROLE_TIMESTAMP,
    LEARNING_TYPE_TIMESERIES_FORECASTING,
    LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION,
    COLUMN_ROLE_TARGET,
    COLUMN_ROLE_FEATURE
)

import pandas as pd
import numpy as np
from numpy import array
import logging

tslogger = logging.getLogger(__name__)


def make_holdout_split(
        dataset: pd.DataFrame,
        target_columns: Union[list, int, str] = None,
        learning_type: str = LEARNING_TYPE_TIMESERIES_FORECASTING,
        test_size: Union[float, int] = 20,
        feature_columns: Union[list, int, str] = None,
        timestamp_column: Union[int, float, str] = None,
        lookback_window: int = 0,
        return_only_holdout: bool = False,
        test_dataset: pd.DataFrame = None,
        tshirt_size: str = "L",
        warn_msg: list = [],
        return_indices: bool = True
) -> Union[Tuple[array, array, array, array], Tuple[array, array, array, array, array, array, array, array]]:
    """
        This function is dedicated to split data into both training and holdout for time series
    Parameters
    ----------
    dataset: DataFrame, required
        A pandas dataframe
    target_columns: int or str, required
        Index or names of target time series in df
    learning_type: str
        Default "forecasting". Only "forecasting" is supported currently.
    test_size: float or int, optional
        Default 20. If float, between 0 and 1, indicates the radio of houldout dataset to the entire data. If int, represents the
        absolute number of houldout samples.
    feature_columns: int or str, optional
        Index or names of features in df
    timestamp_column: int or str, optional
        Index or name of timestamp column in df
    lookback_window: int, optional
        Default 0. The past date/time range to train the model and generate pipelines.
    return_only_holdout: bool, optional
        Default False. If set to True it will return only holdout dataset and indices but without training dataset and indices.
    test_dataset: DataFrame, Optional
        Default None, only used for providing user customized holdout dataset.
    tshirt_size: str. "S","M","L" or "XL", optional
        Default "M".
    warn_msg: list, optional
        Default empty list, collection of warning messages popped up during execution
    return_indices: bool, optional
        Default True, indicator of result including indices of training and holdout
    Returns
    -------
    Numpy arrays:
        x_train, x_holdout,
        y_train, y_holdout,
        x_train_indices, x_holdout_indices,
        y_train_indices, y_holdout_indices
        if return_only_holdout:
            x_holdout, y_holdout,
            x_holdout_indices, y_holdout_indices
    """

    if learning_type == LEARNING_TYPE_TIMESERIES_FORECASTING:
        return _split_data_4ts(dataset, target_columns, learning_type, test_size, feature_columns, timestamp_column,
                               lookback_window, return_only_holdout, test_dataset, tshirt_size, warn_msg,
                               return_indices)
    elif learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION:
        return _split_data_4tsad(dataset, learning_type, test_size, feature_columns, timestamp_column,
                                 lookback_window, return_only_holdout, test_dataset, tshirt_size, warn_msg,
                                 return_indices)


def _split_data_4ts(
        dataset: pd.DataFrame,
        target_columns: Union[list, int, str] = None,
        learning_type: str = LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION,
        holdout_size: Union[float, int] = 20,
        feature_columns: Union[list, int, str] = None,
        timestamp_column: Union[int, float, str] = None,
        lookback_window: int = 0,
        return_only_holdout: bool = False,
        test_dataset: pd.DataFrame = None,
        tshirt_size: str = "L",
        warn_msg: list = [],
        return_indices: bool = True
):
    df = dataset
    holdout_df = test_dataset

    df, holdout_df, holdout_size, target_columns, feature_columns, timestamp_column, _ = DataHelper.process_data(
        df=df,
        learning_type=learning_type,
        target_columns=target_columns,
        feature_columns=feature_columns,
        timestamp_column=timestamp_column,
        anomaly_label_column=None,
        holdout_size=holdout_size,
        user_holdout_df=holdout_df,
        tshirt_size=tshirt_size,
        warn_msg=warn_msg
    )

    tgt_cols = [df.columns.to_list()[i] for i in target_columns]

    fet_cols = []
    if len(feature_columns) > 0:
        fet_cols = [df.columns.to_list()[i] for i in feature_columns]

    # prepare data_cols and all_cols (= data_cols + time)
    data_cols = []
    for item in fet_cols:
        data_cols.append(item)
    for item in tgt_cols:
        if item not in data_cols:
            data_cols.append(item)

    timestamp_column_name = None
    if timestamp_column != -1:
        timestamp_column_name = df.columns[timestamp_column]

    if timestamp_column_name is not None:
        used_cols = [timestamp_column_name] + data_cols
    else:
        used_cols = data_cols

    # prepare data for training and testing
    loaded_data = df[used_cols]
    X_ = loaded_data[data_cols].to_numpy()
    y_ = loaded_data[tgt_cols].to_numpy()

    X, y = (
        X_.astype(float).reshape(-1, max(1, len(data_cols))),
        y_.astype(float).reshape(-1, max(1, len(tgt_cols))),
    )

    training_size = len(X_) - holdout_size
    data = {}
    data["X_train"], data["y_train"] = (
        X[: training_size, :],
        y[: training_size, :],
    )
    data["X_train_indices"], data["y_train_indices"] = (
        np.array(range(0, training_size)),
        np.array(range(0, training_size))
    )

    data["X_test"], data["y_test"] = (
        X[training_size - lookback_window:, :],
        y[training_size:, :],
    )
    data["X_test_indices"], data["y_test_indices"] = (
        np.array(range(training_size - lookback_window, len(X))),
        np.array(range(training_size, len(y)))
    )

    if return_only_holdout:
        if return_indices:
            return data["X_test"], data["y_test"], \
                   data["X_test_indices"], data["y_test_indices"]
        else:
            return data["X_test"], data["y_test"]
    else:
        if return_indices:
            return data["X_train"], data["X_test"], \
                   data["y_train"], data["y_test"], \
                   data["X_train_indices"], data["X_test_indices"], \
                   data["y_train_indices"], data["y_test_indices"]
        else:
            return data["X_train"], data["X_test"], \
                   data["y_train"], data["y_test"]


def _split_data_4tsad(
        dataset: pd.DataFrame,
        learning_type: str = LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION,
        holdout_size: Union[float, int] = 0.2,
        feature_columns: Union[list, int, str] = None,
        timestamp_column: Union[int, float, str] = None,
        lookback_window: int = 0,
        return_only_holdout: bool = False,
        test_dataset: pd.DataFrame = None,
        tshirt_size: str = "L",
        warn_msg: list = [],
        return_indices: bool = True
):
    data_processor = DataProcessor(
        df=dataset,
        holdout_param=holdout_size,
        evaluation_param=None,
        target_columns=feature_columns,
        feature_columns=feature_columns,
        timestamp_column=timestamp_column,
        anomaly_label_column=-1,
        random_state=GLOBAL_DEFAULT_SEED,
        sep="[,|\t]",
        engine="python",
        skiprows=0,
        tshirt_size=tshirt_size,
        holdout_df=test_dataset,
        return_timestamp_column=False,
        learning_type=learning_type
    )

    data_processor.prep_data(dataset, warn_msg=warn_msg)

    # x_train/test/validation as np array:
    x_train, y_train = data_processor.get_x_y_train()
    x_test, y_test = data_processor.get_x_y_test()

    data = {}
    data["X_train"], data["y_train"] = (
        x_train,
        y_train,
    )
    data["X_train_indices"], data["y_train_indices"] = (
        np.array(range(0, len(x_train))),
        np.array(range(0, len(y_train)))
    )

    data["X_test"], data["y_test"] = (
        x_test,
        y_test,
    )
    data["X_test_indices"], data["y_test_indices"] = (
        np.array(range(len(x_train), len(x_train) + len(x_test))),
        np.array(range(len(y_train), len(y_train) + len(y_test))),
    )

    if return_only_holdout:
        if return_indices:
            return data["X_test"], data["y_test"], \
                   data["X_test_indices"], data["y_test_indices"]
        else:
            return data["X_test"], data["y_test"]
    else:
        if return_indices:
            return data["X_train"], data["X_test"], \
                   data["y_train"], data["y_test"], \
                   data["X_train_indices"], data["X_test_indices"], \
                   data["y_train_indices"], data["y_test_indices"]
        else:
            return data["X_train"], data["X_test"], \
                   data["y_train"], data["y_test"]
