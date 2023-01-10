################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2019, 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

import pandas as pd
import numpy as np
from typing import Union
from autoai_ts_libs.utils.messages.messages import Messages
from fractions import Fraction
from autoai_ts_libs.utils.constants import (
    DataType,
    COLUMN_ROLE_TARGET, COLUMN_ROLE_FEATURE,
    COLUMN_ROLE_SUPPORTING_FEATURE, COLUMN_ROLE_TIMESTAMP, COLUMN_ROLE_ANOMALY_LABEL,
    MIN, MAX, COLUMN, ROW, THRESHOLD, HOLDOUT_MAX_RATIO, HOLDOUT_MIN, HOLDOUT_MAX,
    INPUT_DATA_LIMITATION,
    LEARNING_TYPE_TIMESERIES_FORECASTING,
    LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION,
    TSHIRT_SIZE_SMALL, TSHIRT_SIZE_MEDIUM, TSHIRT_SIZE_LARGE, TSHIRT_SIZE_EXTRA_LARGE
)


class DataHelper:

    @staticmethod
    def process_data(
            df: pd.DataFrame,
            learning_type: str,
            target_columns: Union[list, int, str],
            feature_columns: Union[list, int, str],
            timestamp_column: Union[int, float, str],
            anomaly_label_column: Union[int, float, str],
            holdout_size: Union[float, int],
            user_holdout_df: pd.DataFrame,
            tshirt_size: str,
            warn_msg: list
    ):
        """
        Function that processes the input data for supported various learning tpyes. Mainly it does:
        1) validate input specifications, raise errors for the severe ones and pop up warnings for the mild ones
        2) validate the user holdout data's metadata and data length if it's specified
        3) figure out all the used columns' indexes no matter how they specified originally
        4) validate the total number of the target and feature columns to ensure them not
           exceed the pre-defined thresholds against various t-shirt sizes.
        5) validate the timestamp column not be specified in target/feature columns list
        6) validate the anomaly label column not be specified as the timestamp column and not be
           in target/feature columns list
        7) parse the columns' values from str to float to ensure this kind of input data that has numeric
           values but its metadata is string still can work.
        8) process the input data by the timestamp column and the user holdout data:
           a) validate the timestamp column has no duplicated values
           b) parse the timestamp column and convert it to unix timestamp. Try again by stripping '\"'
              if the first try is failed.
           c) ensure data sorted by the time column
           d) validate time interval be equal space after above sorted
           e) validate the user holdout data must be newer than training
           f) validate the user holdout data len to ensure only the threshold rows will be used if it exceeds
           g) concat the training data with the user holdout as the entire input data
        9) validates the input training data length to ensure only the latest N rows will be used
           for model building if the data length exceeds the pre-defined maximum.
        ----------
        df: Dataframe, Required
            The entire data when the user holdout data - holdout_df is none. Otherwise, the training data.
        learning_type: str, Required
            "forecasting" or "timeseries_anomaly_prediction".
        target_columns: Union[list, int, str], Required if the learning_type is "forecasting"
            Index or names of target time series in df and holdout_df
        feature_columns: Union[list, int, str], Required if the learning_type is "timeseries_anomaly_prediction", Optional if "forecasting".
            Index or names of features in df and holdout_df
        timestamp_column: int or str, Required
            Index or name of timestamp column in df and holdout_df
        anomaly_label_column: int or str, Required
            Index or name of anomaly label column in df and holdout_df
        holdout_size: float or int, Required
            If float, between 0 and 1, indicates the radio of the holdout dataset to the entire data. If int, represents the
            absolute number of holdout samples.
        holdout_df: Dataframe, Required
            The user holdout data.
        tshirt_size: str. "S","M","L" or "XL", optional
            Default "M".
        warn_msg: list, optional
            Default empty list, collection of warning messages popped up during execution
        Returns
        ----------
        df, user_holdout_df,
        holdout_size,
        target_column_indexs, feature_column_indexs, timestamp_column_idx, anomaly_label_column_idx
        """
        # =======STEP 1: validate input parameters======
        dataHelper = DataHelper()
        dataHelper.validate_input_params(learning_type, target_columns, feature_columns, user_holdout_df, tshirt_size)

        if not isinstance(target_columns, list):
            if target_columns != -1:
                target_columns = [target_columns]
            else:
                target_columns = []

        if not isinstance(feature_columns, list):
            if feature_columns != -1:
                feature_columns = [feature_columns]
            else:
                feature_columns = []

        # =======STEP 2: validate input data======
        holdout_size = dataHelper.validate_input_data(df, learning_type, holdout_size, user_holdout_df)

        # =======STEP 3: Get indexes of the target/feature columns and ensure the total number of the target
        # and feature columns NOT exceed the pre-defined thresholds against various t-shirt sizes======
        target_column_indexs = dataHelper.get_cols_idx(df, target_columns, COLUMN_ROLE_TARGET,
                                                       learning_type)
        feature_column_indexs = dataHelper.get_cols_idx(df, feature_columns, COLUMN_ROLE_FEATURE,
                                                        learning_type)

        dataHelper.validate_input_data_col_num(learning_type, tshirt_size, target_column_indexs, feature_column_indexs)

        # =======STEP 4: Get indexes of the timestamp column and the anomaly label column======
        timestamp_column_idx = -1
        if timestamp_column is not None and timestamp_column != -1:
            timestamp_column_idx = dataHelper.get_cols_idx(df, [timestamp_column], COLUMN_ROLE_TIMESTAMP, learning_type)
        timestamp_column_name = None
        if timestamp_column_idx != -1:
            timestamp_column_name = df.columns[timestamp_column_idx]
            # Ensure timestamp column NOT be specified twice in either target columns or feature columns.
            dataHelper.check_time_col_specified_twice(timestamp_column_idx, timestamp_column_name, target_column_indexs,
                                                      COLUMN_ROLE_TARGET)
            dataHelper.check_time_col_specified_twice(timestamp_column_idx, timestamp_column_name,
                                                      feature_column_indexs,
                                                      COLUMN_ROLE_FEATURE)

        anomaly_label_column_idx = -1
        if anomaly_label_column is not None and anomaly_label_column != -1 and \
                learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION:
            anomaly_label_column_idx = dataHelper.get_cols_idx(df, [anomaly_label_column], COLUMN_ROLE_ANOMALY_LABEL,
                                                               learning_type)
        if anomaly_label_column_idx != -1:
            # TODO: validate anomaly_label_column_idx ensure it's not equal to timestamp_column_idx and not in
            # target_column_indexs or target_column_indexs.
            pass

        # =======STEP 5: Parse the columns' values from str to float because sometimes the input data is from DB,
        # the original numerical data type could be an actual string.======
        dataHelper.str2float(df, target_column_indexs, COLUMN_ROLE_TARGET)
        feat_column_indexs = []
        for x in feature_column_indexs:
            if x not in target_column_indexs:
                feat_column_indexs.append(x)
        dataHelper.str2float(df, feat_column_indexs, COLUMN_ROLE_FEATURE)
        if anomaly_label_column_idx != -1:
            dataHelper.str2float(df, [anomaly_label_column_idx], COLUMN_ROLE_ANOMALY_LABEL)

        # =======STEP 6: Process data by the timestamp column and concat training data with the user holdout
        # data as the entire input data.======
        df, user_holdout_df, holdout_size = dataHelper.process_data_by_time_col(df, user_holdout_df,
                                                                                timestamp_column_name,
                                                                                learning_type,
                                                                                holdout_size, warn_msg)

        # =======STEP 7: Validate data length against the entire input data.======
        df = dataHelper.validate_data_len(df, learning_type, tshirt_size, warn_msg)

        return df, user_holdout_df, holdout_size, \
            target_column_indexs, feature_column_indexs, timestamp_column_idx, anomaly_label_column_idx

    def validate_input_data_col_num(
            self,
            learning_type: str,
            tshirt_size: str,
            target_columns: list = None,
            feature_columns: list = None,
    ):
        """
        Function that checks whether the total number of the input columns
        specified as various column roles for a certain learning type not exceed the supported maximum.
        Raises an error when this check is failed.
        Parameters
        ----------
        learning_type: str, Required
            "forecasting" or "timeseries_anomaly_prediction".
        tshirt_size: str, Required
            "S","M","L" or "XL"
        target_columns: list, Required if the learning_type is "forecasting"
            Index or names of target time series in the input training data
        feature_columns: list, Required if the learning_type is "timeseries_anomaly_prediction", Optional if "forecasting".
            Index or names of features in the input training data
        """
        col_role = []
        col_num = 0
        if learning_type == LEARNING_TYPE_TIMESERIES_FORECASTING and target_columns is not None:
            col_role.append(COLUMN_ROLE_TARGET)
            col_num = len(target_columns)
            if len(feature_columns) > len(target_columns):
                col_role.append(COLUMN_ROLE_SUPPORTING_FEATURE)
                col_num = len(feature_columns)
        elif learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and feature_columns is not None:
            col_role.append(COLUMN_ROLE_FEATURE)
            col_num = len(feature_columns)

        if learning_type in INPUT_DATA_LIMITATION and tshirt_size in INPUT_DATA_LIMITATION[learning_type]:
            col_max = INPUT_DATA_LIMITATION[learning_type][tshirt_size][COLUMN][MAX]
            if col_num > col_max:
                if len(col_role) == 1:
                    col_role_str = col_role[0]
                elif len(col_role) == 2:
                    col_role_str = col_role[0] + " and " + col_role[1]
                raise Exception(
                    Messages.get_message(
                        col_role_str, str(col_max), message_id="AUTOAITSLIBS0093E"
                    )
                )

    def parse_time_col(self, data_df: pd.DataFrame, time_col: str, data_type: DataType):
        """
        Function that attempts to parse the timestamp column string with stripping '\"' into a :class:`datetime.datetime`.
        First try through calling <https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse>
        If failed, try again through calling <https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.isoparse>.
        Raises an error when it eventually failed.
        Parameters
        ----------
        data_df: Dataframe, Required
            The input data that could be training data or holdout data or the entire input data.
        time_col: str, Required
            Name of timestamp column in data_df
        data_type: DataType, Required
            One of the pre-defined data types.
        """
        if pd.api.types.is_numeric_dtype(data_df[time_col]):
            # nothing to do, assuming unix timestamp
            pass
        elif pd.api.types.is_string_dtype(data_df[time_col]):
            # check string format, and convert to unix timestamp
            try:
                from dateutil.parser import parse

                data_df[time_col] = data_df[time_col].map(
                    lambda ts: parse((str(ts)).strip('\"'), fuzzy=False)
                )
            except Exception as e:
                try:
                    from dateutil.parser import isoparser, isoparse
                    data_df[time_col] = data_df[time_col].map(
                        lambda ts: isoparse((str(ts)).strip('\"'))
                    )
                except Exception as ex:
                    raise Exception(Messages.get_message(time_col, " in the " + str(data_type) + "data",
                                                         message_id='AUTOAITSLIBS0076E'))

        else:
            raise Exception(Messages.get_message(" in the " + str(data_type) + "data", message_id='AUTOAITSLIBS0077E'))

    def validate_time_interval(self, df: pd.DataFrame, time_col: str, warn_msg: list,
                               data_type: DataType):
        """
        Function that validates the time interval in the input time series data exist as expected
        through checking the threshold: 100 times the ratio of the mean and the standard deviation of time differences.
        Raises an error if the mean of time differences is 0.
        Pops up a warning if the threshold is larger than 20.
        Parameters
        ----------
        df: Dataframe, Required
            The input data that could be training data or holdout data or the entire input data.
        time_col: str, Required
            Name of timestamp column in df
        warn_msg: list, Required
            Default empty list, collection of warning messages popped up during execution
        data_type: DataType, Required
            One of the pre-defined data types.
        """
        # calculate relative standard deviation (in seconds) of successive timestamp deltas
        timestamps = df[time_col].to_list()
        timedeltas = []
        for i in range(1, len(timestamps)):
            diff = timestamps[i] - timestamps[i - 1]
            if type(diff) == pd._libs.tslibs.timedeltas.Timedelta:
                timedeltas.append(diff.total_seconds())
            else:
                timedeltas.append(diff)
        import statistics

        m = statistics.mean(timedeltas)
        s = statistics.stdev(timedeltas)
        if m == 0:
            raise Exception(
                Messages.get_message(time_col, " in the " + str(data_type) + " data", message_id='AUTOAITSLIBS0071E'))

        r = 100.0 * s / m
        if r > 20.0:
            warn_msg.append(Messages.get_message(" in the " + str(data_type) + " data", message_id='AUTOAITSLIBS0004W'))

    def check_user_holdout_newer(self, train_df: pd.DataFrame, holdout_df: pd.DataFrame, time_col: str):
        """
        Function that checks the user holdout data must be newer than the training data.
        Raises an error if the check is failed.
        Parameters
        ----------
        train_df: Dataframe, Required
            The training data.
        holdout_df: Dataframe, Required
            The user holdout data.
        time_col: str, Required
            Name of timestamp column in the train_df and holdout_df.
        """
        if train_df[time_col].iat[-1] > holdout_df[time_col].iat[0]:
            raise Exception(Messages.get_message(message_id='AUTOAITSLIBS0087E'))

    def validate_data_len(self, df: pd.DataFrame, learning_type: str, tshirt_size: str, warn_msg: list):
        """
        Function that validates the input training data length:
            1) Raises an error if the data length is smaller than the minimum requirement.
            2) Pops up a warning if the data length is smaller than a threshold that could make some pipelines run improperly.
            3) Only the latest N rows will be used for model building if the data length exceeds the pre-defined maximum.
               Meanwhile, pops up a warning accordingly.
        Parameters
        ----------
        df: Dataframe, Required
            The input training data.
        learning_type: str, Required
            "forecasting" or "timeseries_anomaly_prediction".
        tshirt_size: str, Required
            "S","M","L" or "XL"
        warn_msg: list, Required
            Default empty list, collection of warning messages popped up during execution
        """
        df_len = len(df)
        if learning_type in INPUT_DATA_LIMITATION:
            row_min = INPUT_DATA_LIMITATION[learning_type][ROW][MIN]
            if learning_type == LEARNING_TYPE_TIMESERIES_FORECASTING and df_len < row_min:
                raise Exception(Messages.get_message(str(row_min), message_id='AUTOAITSLIBS0084E'))

            if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and df_len < row_min:
                raise Exception(
                    Messages.get_message(str(row_min), message_id="AUTOAITSLIBS0096E"))

            if learning_type == LEARNING_TYPE_TIMESERIES_FORECASTING and df_len <= \
                    INPUT_DATA_LIMITATION[learning_type][ROW][THRESHOLD]:
                warn_msg.append(Messages.get_message(message_id='AUTOAITSLIBS0007W'))

            if tshirt_size in INPUT_DATA_LIMITATION[learning_type]:
                row_max = INPUT_DATA_LIMITATION[learning_type][tshirt_size][ROW][MAX]
                if df_len > row_max:
                    df = df.tail(row_max)
                    warn_msg.append(Messages.get_message(str(row_max),
                                                         message_id='AUTOAITSLIBS0005W'))
        return df

    def validate_user_holdout_len(self, train_df: pd.DataFrame, holdout_df: pd.DataFrame,
                                  learning_type: str,
                                  holdout_size: Union[int, float],
                                  warn_msg: list):
        """
        Function that validates the user holdout data length that only the threshold number of records will be used
        if it exceeds the pre-defined threshold.
        Parameters
        ----------
        train_df: Dataframe, Required
            The training data.
        holdout_df: Dataframe, Required
            The user holdout data that should be sorted in ascending order by the timestamp column already.
        learning_type: str, Required
            "forecasting" or "timeseries_anomaly_prediction".
        holdout_size: float or int, Required
            If float, between 0 and 1, indicates the radio of the holdout dataset to the entire data. If int, represents the
            absolute number of holdout samples.
        warn_msg: list, Required
            Default empty list, collection of warning messages popped up during execution
        """
        if learning_type in INPUT_DATA_LIMITATION:
            ratio_threshold = INPUT_DATA_LIMITATION[learning_type][ROW][HOLDOUT_MAX_RATIO]
            len_threshold = (len(train_df) + len(holdout_df)) * float(ratio_threshold)
            if (holdout_size < 1 and holdout_size > ratio_threshold) or \
                    (holdout_size > len_threshold):
                if holdout_size < 1:
                    holdout_size = ratio_threshold
                    holdout_df = holdout_df.head(int(len_threshold))
                else:
                    holdout_size = len_threshold
                    holdout_df = holdout_df.head(int(len_threshold))

                warn_msg.append(
                    Messages.get_message(self._frac2words(ratio_threshold), message_id='AUTOAITSLIBS0006W'))
        return holdout_df, holdout_size

    def _frac2words(self, ratio: Fraction) -> str:
        if ratio == Fraction(1, 3):
            return "one third"

    def check_user_holdout_metadata(self, train_df: pd.DataFrame, holdout_df: pd.DataFrame):
        """
        Function that checks to see if the user holdout data has the same data type and column names with the training data.
        Raises an error if either of checks failed.
        Parameters
        ----------
        train_df: Dataframe, Required
            The training data.
        holdout_df: Dataframe, Required
            The user holdout data.
        """
        if train_df.shape[1] != holdout_df.shape[1]:
            raise Exception(
                Messages.get_message(holdout_df.shape[1], train_df.shape[1], message_id='AUTOAITSLIBS0081E'))
        if list(train_df.columns) != list(holdout_df.columns):
            raise Exception(Messages.get_message(
                list(holdout_df.columns), list(train_df.columns), message_id='AUTOAITSLIBS0082E'))

    def check_missing(self, X: np.ndarray, column, missing_value=np.NaN):
        """Check whether input matrix include missing values.
           If the input include missing value, raise an error

        Args:
            X (np.ndarray): Input data
            missing_value ([type], optional): Specifies which value to count as missing.
                Useful for applying function on a boolean mask matrix. Defaults to np.NaN.

        """
        if missing_value is np.NaN:
            missing_num = np.isnan(X).sum(axis=0)
        else:
            missing_num = (X == missing_value).sum(axis=0)
        if missing_num > 0:
            raise Exception(
                Messages.get_message(
                    column, message_id="AUTOAITSLIBS0091E"
                )
            )

    def validate_input_params(self,
                              learning_type: str,
                              target_columns: Union[list, int, str],
                              feature_columns: Union[list, int, str],
                              user_holdout_df: pd.DataFrame,
                              tshirt_size: str
                              ):
        """
        Function that validates the input parameters.
        Raises an error if the input ``learning_type`` parameter is invalid.
        Raises an error if the input ``learning_type`` parameter is forecasting but ``target_columns`` parameter is None.
        Raises an error if the input ``learning_type`` parameter is timeseries_anomaly_prediction but
        ``feature_columns`` parameter is None.
        Raises an error if the input ``learning_type`` parameter is timeseries_anomaly_prediction but
        ``user_holdout_df`` parameter is NOT None.
        Raises an error if the input ``tshirt_size`` parameter is invalid.
        Parameters
        ----------
        learning_type: str, Required
            "forecasting" or "timeseries_anomaly_prediction".
        target_columns: Union[list, int, str], Required if the learning_type is "forecasting"
            Index or names of target time series in df and holdout_df
        feature_columns: Union[list, int, str], Required if the learning_type is "timeseries_anomaly_prediction",
            Optional if "forecasting".
            Index or names of features in df and holdout_df
        user_holdout_df: Dataframe, Required
            The user holdout data.
        tshirt_size: str, Required
            "S","M","L" or "XL"
        """
        if learning_type not in (LEARNING_TYPE_TIMESERIES_FORECASTING, LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION):
            raise Exception(
                Messages.get_message(
                    LEARNING_TYPE_TIMESERIES_FORECASTING + ' or ' + LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION,
                    learning_type,
                    message_id='AUTOAITSLIBS0068E'))

        if learning_type == LEARNING_TYPE_TIMESERIES_FORECASTING and target_columns is None:
            raise Exception(
                Messages.get_message(COLUMN_ROLE_TARGET, COLUMN_ROLE_TARGET, message_id="AUTOAITSLIBS0092E"))

        if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and feature_columns is None:
            raise Exception(
                Messages.get_message(COLUMN_ROLE_FEATURE, COLUMN_ROLE_FEATURE, message_id="AUTOAITSLIBS0092E"))

        # TSAP doesn't support the functionality of the user holdout data set for MVP release, should be supported later.
        if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and user_holdout_df is not None:
            raise Exception(Messages.get_message(message_id='AUTOAITSLIBS0094E'))

        if tshirt_size not in (TSHIRT_SIZE_SMALL, TSHIRT_SIZE_MEDIUM, TSHIRT_SIZE_LARGE, TSHIRT_SIZE_EXTRA_LARGE):
            tshirt_size_str = '[' + TSHIRT_SIZE_SMALL + ', ' \
                              + TSHIRT_SIZE_MEDIUM + ', ' \
                              + TSHIRT_SIZE_LARGE + ', ' \
                              + TSHIRT_SIZE_EXTRA_LARGE + ']'
            raise Exception(Messages.get_message(tshirt_size, tshirt_size_str, message_id='AUTOAITSLIBS0103E'))

    def validate_input_data(self, df: pd.DataFrame, learning_type: str, holdout_size: Union[float, int],
                            holdout_df: pd.DataFrame = None) -> int:
        """
        Function that validates the input training data and the user holdout data.
        Raises an error if the entire/training data doesn't exist.
        Raises an error if the metadata of the user holdout data is inconsistent with the training data's.
        Raises an error if the holdout data length exceeds the pre-defined maximum.
        Parameters
        ----------
        df: Dataframe, Required
            The entire data when the user holdout data - holdout_df is none. Otherwise, the training data.
        learning_type: str, Required
            "forecasting" or "timeseries_anomaly_prediction".
        holdout_size: float or int, Required
            If float, between 0 and 1, indicates the radio of the holdout dataset to the entire data. If int, represents the
            absolute number of holdout samples.
        holdout_df: Dataframe, Optional
            The user holdout data.
        Returns
        ----------
        int: The length of the user holdout data if it's not NONE. Otherwise, holdout_size is returned.
        """
        if df is None:
            raise Exception(Messages.get_message(message_id='AUTOAITSLIBS0069E'))

        n_samples = len(df)
        # If there is no the user holdout data, validating holdout_size by the pre-defined max ratio/size.
        if holdout_df is None:
            if learning_type in INPUT_DATA_LIMITATION:
                ratio_threshold = INPUT_DATA_LIMITATION[learning_type][ROW][HOLDOUT_MAX_RATIO]
                len_threshold = n_samples * float(ratio_threshold)
                if holdout_size <= 0:
                    raise Exception(
                        Messages.get_message(holdout_size, message_id='AUTOAITSLIBS0095E'))
                if holdout_size > len_threshold:
                    raise Exception(
                        Messages.get_message(holdout_size, int(len_threshold), ratio_threshold,
                                             message_id='AUTOAITSLIBS0101E'))
                if (holdout_size < 1) and (holdout_size > ratio_threshold):
                    raise Exception(
                        Messages.get_message(holdout_size, ratio_threshold,
                                             message_id='AUTOAITSLIBS0102E'))

                if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION:
                    holdout_min_num = INPUT_DATA_LIMITATION[LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION][ROW][
                        HOLDOUT_MIN]
                    holdout_max_num = INPUT_DATA_LIMITATION[LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION][ROW][
                        HOLDOUT_MAX]

                    if holdout_size >= 1.0:
                        if holdout_size < holdout_min_num:
                            raise Exception(
                                Messages.get_message(holdout_size, holdout_min_num,
                                                     message_id="AUTOAITSLIBS0097E"))
                        elif holdout_size > holdout_max_num:
                            raise Exception(
                                Messages.get_message(holdout_size, holdout_max_num,
                                                     message_id="AUTOAITSLIBS0099E"))
                    else:
                        df_holdout_len = int(holdout_size * n_samples)
                        if df_holdout_len < holdout_min_num:
                            raise Exception(
                                Messages.get_message(holdout_size, round(float(holdout_min_num) / n_samples, 3),
                                                     message_id="AUTOAITSLIBS0098E"))
                        elif df_holdout_len > holdout_max_num:
                            raise Exception(
                                Messages.get_message(holdout_size, round(float(holdout_max_num) / n_samples, 3),
                                                     message_id="AUTOAITSLIBS0100E"))


        # If there has the user holdout data, NOT validate the length of holdout_df by the pre-defined max ratio/size.
        # Instead, in another place with a proper timing later, will validate through calling validate_user_holdout_len function.
        else:
            self.check_user_holdout_metadata(df, holdout_df)
            holdout_size = len(holdout_df)
            if holdout_size == 0:
                raise Exception(Messages.get_message(holdout_size, n_samples, message_id='AUTOAITSLIBS0070E'))

        holdout_len_type = np.asarray(holdout_size).dtype.kind
        holdout_size = int(n_samples * holdout_size) if (holdout_len_type == 'f' and holdout_size < 1) else int(
            holdout_size)

        return holdout_size

    def get_cols_idx(self, df: pd.DataFrame, cols: list, col_role: str, learning_type: str) -> Union[list, int]:
        df_columns = df.columns.to_list()
        col_idx = []
        for col in cols:
            if isinstance(col, int) and col >= 0 and col < len(df.columns):
                col_idx.append(col)
                if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and col_role in (
                        COLUMN_ROLE_TARGET, COLUMN_ROLE_FEATURE):
                    col_name = df_columns[col]
                    self.check_missing(X=df[col_name], column=str(col))
            elif isinstance(col, str) and col in df_columns:
                col_idx.append(df_columns.index(col))
                if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and col_role in (
                        COLUMN_ROLE_TARGET, COLUMN_ROLE_FEATURE):
                    self.check_missing(X=df[col], column=col)
            elif isinstance(col, float) and int(col) >= 0 and int(col) < len(df.columns):
                col_idx.append(int(col))
                if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION and col_role in (
                        COLUMN_ROLE_TARGET, COLUMN_ROLE_FEATURE):
                    col_name = df_columns[int(col)]
                    self.check_missing(X=df[col_name], column=str(col))

        if col_role == COLUMN_ROLE_TARGET:
            # if learning type is forecasting, target column(s) must be specified.
            # And it should raise an error if all specified doesn't exist.
            if learning_type == LEARNING_TYPE_TIMESERIES_FORECASTING:
                if len(col_idx) == 0:
                    raise Exception(
                        Messages.get_message(col_role, [str(x) for x in cols],
                                             message_id="AUTOAITSLIBS0072E"))
            # TODO: need a good explanation for why need a sort here
            if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION:
                col_idx.sort()
        elif col_role == COLUMN_ROLE_FEATURE:
            # If learning type is timeseries_anomaly_prediction, feature column(s) must be specified.
            # And it should raise an error if all specified doesn't exist.
            if learning_type == LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION:
                if len(col_idx) == 0:
                    raise Exception(
                        Messages.get_message(col_role, [str(x) for x in cols],
                                             message_id="AUTOAITSLIBS0072E"))
                col_idx.sort()
        elif col_role == COLUMN_ROLE_TIMESTAMP or col_role == COLUMN_ROLE_ANOMALY_LABEL:
            if len(col_idx) == 0:
                raise Exception(
                    Messages.get_message(col_role, [str(x) for x in cols],
                                         message_id="AUTOAITSLIBS0072E"))
            # NOTE: only support one timestamp column, one anomaly label column.
            col_idx = col_idx[0]

        return col_idx

    def check_time_col_specified_twice(self, time_col_idx: int, time_col_name: str, other_col_idx: list,
                                       col_role: str):
        if time_col_idx in other_col_idx:
            raise Exception(Messages.get_message(str(time_col_name), col_role, message_id="AUTOAITSLIBS0074E"))

    def str2float(self, df: pd.DataFrame, col_idx: list, col_role: str):
        for i in col_idx:
            if pd.api.types.is_string_dtype(df.dtypes[i]):
                try:
                    col_name = df.columns[i]
                    df[col_name] = df[col_name].map(
                        lambda tar: str(tar).strip('\"')
                    )
                    df[col_name] = df[col_name].map(
                        lambda x: float(x) if len(x) != 0 else float('nan')
                    )
                except Exception as ex:
                    raise Exception(Messages.get_message(col_role, col_name, str(ex), message_id='AUTOAITSLIBS0073E'))
        return df

    def process_data_by_time_col(self, df: pd.DataFrame, holdout_df: pd.DataFrame, time_col: str, learning_type: str,
                                 holdout_size: Union[int, float], warn_msg: list) -> pd.DataFrame:
        if time_col is not None:
            if True in df.duplicated(subset=[time_col]).to_list():
                raise Exception(Messages.get_message(message_id="AUTOAITSLIBS0075E"))

            if holdout_df is not None:
                self.parse_time_col(df, time_col, DataType.TRAINING)
                self.parse_time_col(holdout_df, time_col, DataType.HOLDOUT)
            else:
                self.parse_time_col(df, time_col, DataType.INPUT)

            # ensure data sorted by the time column
            df = df.sort_values(by=time_col)

            # ensure time interval be equal space after above sorted
            self.validate_time_interval(df, time_col, warn_msg, DataType.INPUT)

            # If there have both the user holdout data and the time column, do the following 5 things in order:
            # 1) sort it by the time column; 2) check it must be newer than training;
            # 3) ensure time interval be equal space; 4) validate its len; 5) concat training data with it
            if holdout_df is not None:
                holdout_df = holdout_df.sort_values(by=time_col)
                self.check_user_holdout_newer(df, holdout_df, time_col)
                self.validate_time_interval(
                    holdout_df, time_col, warn_msg, DataType.HOLDOUT
                )
                holdout_df, holdout_size = self.validate_user_holdout_len(df, holdout_df,
                                                                          learning_type,
                                                                          holdout_size, warn_msg)
                df = pd.concat([df, holdout_df], ignore_index=True, sort=False)
        else:
            # If there has only the user holdout data but without the time column, do the following 2 things in order:
            # 1) validate its len; 2) concat training data with it
            if holdout_df is not None:
                holdout_df, holdout_size = self.validate_user_holdout_len(df, holdout_df,
                                                                          learning_type,
                                                                          holdout_size, warn_msg)
                df = pd.concat([df, holdout_df], ignore_index=True, sort=False)

        return df, holdout_df, holdout_size
