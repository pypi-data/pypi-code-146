################################################################################
# IBM Confidential
# OCO Source Materials
# 5737-H76, 5725-W78, 5900-A1R
# (c) Copyright IBM Corp. 2019, 2022. All Rights Reserved.
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
################################################################################

from copy import copy
import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from autoai_ts_libs.utils.messages.messages import Messages
from autoai_ts_libs.utils.data_helper import DataHelper
from pandas.api.types import is_string_dtype
from autoai_ts_libs.utils.logs import tslogger
from autoai_ts_libs.utils.constants import (
    VERBOSE,
    LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION,
    DataType,
    COLUMN_ROLE_TARGET,
    COLUMN_ROLE_FEATURE,
    COLUMN_ROLE_TIMESTAMP,
    COLUMN_ROLE_ANOMALY_LABEL
)


class DataProcessor:
    def __init__(
            self,
            df=None,
            holdout_param=0.20,
            evaluation_param=0,
            target_columns=[],
            feature_columns=[],
            timestamp_column=None,
            anomaly_label_column=None,
            random_state=20,
            sep="[,|\t]",
            engine="python",
            skiprows=0,
            tshirt_size="L",
            holdout_df=None,
            return_timestamp_column=False,
            learning_type=LEARNING_TYPE_TIMESERIES_ANOMALY_PREDICTION
    ):

        self.df = df
        self.holdout_param = holdout_param
        self.evaluation_param = evaluation_param
        self.sep = sep
        self.engine = engine
        self.skiprows = skiprows
        self.holdout_df = holdout_df
        self.random_state = random_state
        self.tshirt_size = tshirt_size

        self.target_columns = target_columns
        self.feature_columns = feature_columns
        self.lookback_window = None
        self.anomaly_label_column = anomaly_label_column
        self.timestamp_column = timestamp_column
        self.return_timestamp_column = return_timestamp_column

        # self.df_alldata = None
        self.x = None
        self.y = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.x_evaluation = None
        self.y_evaluation = None
        # self.test_perc = self.holdout_param  # 0.20  # % of test size why needs another param?
        self.train_size = None  # Actual number of rows
        self.test_size = None  # Actual number of rows
        self.evaluation_size = None  # Actual number of rows
        self.original_time_values_on_holdout = None
        self.actual_used_feature_names = None
        self.learning_type = learning_type

    def prep_data(self, df, warn_msg=None):
        """
            Function that calls all necessary functions in one place to populate all the objects so class methods can be
        called on to get various splits of data.
        :param df: The dataframe of time series should be in the format:
                timestamp  | target01  | target02... | feature01  | feature02... |anomaly_label
        :return:
            updated x_/y_ for train/test/evaluation sets

        - Example: Let the given time series have 1100 timepoints.
        + if self.evaluation_param = 100, self.holdout_param=0.2, then timepoints of:
            x_train = [0-799], x_test = [800-999], x_evaluation = [1000-1099]
            (assuming that no actual anomalies appeared in x_evaluation)
        + if self.evaluation_param = 0 (by default), self.holdout_param = 300, then timepoints of:
            x_train = [0-799], x_test = [800-1099], x_evaluation = None
        + In both cases, synthetic anomalies will be injected into x_test
        """

        all_df = self.preprocess_data(df, warn_msg=warn_msg)

        # == Extract x,y as 2 sub-dataframes from 'all_df' with different columns:
        # == x is timestamp+data columns and y is timestamp+label column and both remain dataframes
        x, y = self.get_X_Y(all_data=all_df)
        # the above also reindexes the columns!

        if self.holdout_param <= 0:
            raise Exception(Messages.get_message(message_id="AUTOAITSAD0008E"))
        if self.holdout_param >= 1.0:
            df_holdout_len = self.holdout_param
            if self.evaluation_param is not None:
                df_holdout_len += self.evaluation_param
            if df_holdout_len > len(x):
                raise Exception(Messages.get_message(message_id="AUTOAITSAD0043E"))
            else:
                self.holdout_param = int(self.holdout_param)

        '''
        If -ep param is provided, split x/y into 3 sets train/test/evaluation, 
        otherwise only 2 sets of train/test:
        '''
        if self.evaluation_param is not None and self.evaluation_param > 0:
            self.x_train, self.x_evaluation, self.y_train, self.y_evaluation = self.split_test_train(
                x=x, y=y, test_size=self.evaluation_param)
            '''Further split x/y_train into x/y_train and x/y_test:'''
            self.x_train, self.x_test, self.y_train, self.y_test = self.split_test_train(
                x=self.x_train, y=self.y_train, test_size=self.holdout_param)
        else:
            self.x_train, self.x_test, self.y_train, self.y_test = self.split_test_train(
                x=x, y=y, test_size=self.holdout_param)
            self.x_evaluation, self.y_evaluation = None, None

        # convert above dfs to numpy arrays:
        if (
                self.return_timestamp_column
                and self.timestamp_column is not None
                and self.timestamp_column != -1
        ):
            self.x_train = self._reformat_date(
                self.x_train, self.timestamp_column
            ).to_numpy()
            self.x_test = self._reformat_date(
                self.x_test, self.timestamp_column
            ).to_numpy()
            self.y_train = self._reformat_date(self.y_train, 0).to_numpy()
            self.y_test = self._reformat_date(self.y_test, 0).to_numpy()
            if self.y_evaluation is not None:
                self.y_evaluation = self._reformat_date(self.y_evaluation, 0).to_numpy()

            self.x = self._reformat_date(x, self.timestamp_column).to_numpy()
            self.y = self._reformat_date(y, 0).to_numpy()

        else:
            self.x_train = self.x_train.to_numpy()
            self.x_test = self.x_test.to_numpy()
            self.y_train = self.y_train.to_numpy()
            self.y_test = self.y_test.to_numpy()
            if self.x_evaluation is not None:
                self.x_evaluation = self.x_evaluation.to_numpy()
                self.y_evaluation = self.y_evaluation.to_numpy()
            self.x = x.to_numpy()
            self.y = y.to_numpy()

        self.train_size = len(self.x_train)
        self.test_size = len(self.x_test)  # Set actual row numbers
        self.evaluation_size = 0 if (self.x_evaluation is None) else len(self.x_evaluation)  # Set actual row numbers

        return True

    @staticmethod
    def _reformat_date(input, time_column):
        l_func = lambda x: x.to_pydatetime().timestamp()
        if isinstance(input, pd.DataFrame) and pd.api.types.is_datetime64_any_dtype(
                input.iloc[:, time_column]
        ):
            input.iloc[:, time_column] = input.iloc[:, time_column].apply(l_func)
        # elif isinstance(input, np.ndarray):
        #     input[:, time_column] = [l_func(x) for x in input[:, time_column]]
        else:
            ValueError("Unsupported input type in date column conversion")
        return input

    def get_x_y_train(self):
        return self.x_train, self.y_train

    def get_x_y_test(self):
        return self.x_test, self.y_test

    def get_x_y_evaluation(self):
        return self.x_evaluation, self.y_evaluation

    def get_x_y_all(self):
        return self.x, self.y

    def get_x_y_train_hold_data(self, training_data_holdout=0.2):
        """_summary_

        Args:
            training_data_hold_out (float, optional): _description_. Defaults to 0.2.

        Returns:
            _type_: _description_
        """

        return self.split_test_train(
            x=self.x_train, y=self.y_train, test_size=training_data_holdout,
        )

    # incase we need any cleaning of data
    def preprocess_data(self, df, warn_msg=None):
        """
        Except timestamp_column being an INTEGER (or None), other columns (tc, fc, ac) are all a list.
        """
        self.origin_target_columns = self.target_columns
        self.origin_feature_columns = self.feature_columns
        self.origin_anomaly_label_column = self.anomaly_label_column
        self.origin_timestamp_column = self.timestamp_column

        df, self.holdout_df, self.holdout_param, self.target_columns, self.feature_columns, \
        self.timestamp_column, self.anomaly_label_column = DataHelper.process_data(
            df=df,
            learning_type=self.learning_type,
            target_columns=self.target_columns,
            feature_columns=self.feature_columns,
            timestamp_column=self.timestamp_column,
            anomaly_label_column=self.anomaly_label_column,
            holdout_size=self.holdout_param,
            user_holdout_df=self.holdout_df,
            tshirt_size=self.tshirt_size,
            warn_msg=warn_msg
        )

        self.original_time_values_on_holdout = self._get_original_time_values_on_holdout(df)

        return df

    def get_X_Y(self, all_data) -> pd.DataFrame:
        """

        This function returns x, y as dataframes based on parameters passed to constructor, i.e, time stamp col,
        label column, feature column etc.

        :param force_read: Force to read the file provided otherwise it will use file passed in constructor
        :param _file_path: File path only read when force_read is True
        :return: returns x, y split of data in cache or read from file
        """

        # split into x and y
        """
         We leave x as all data for now and pass it down to each estimator along with column indices this way the 
         indices remain consistent otherwise if we split the column indices e.g., feature_column, time stamp etc 
         will not be consistent on subset and we will need the re-indexing 

         Y can contain only label along with timestamp column

         The current implementation has Y in X if we don't want that we need to put strong assumption that target/label 
         column will always be last column in data file this way it does not cause re-indexing of X, then we can easily
         remove the label column and x will have no label column. 
         """

        # find the data columns
        data_cols = self.target_columns
        data_cols.extend(
            [c for c in self.feature_columns if c not in self.target_columns]
        )

        # print(all_data.iloc[:, [self.timestamp_column,self.anomaly_label_column]])
        if (
                self.return_timestamp_column
                and self.timestamp_column is not None
                and self.timestamp_column != -1
        ):
            x_cols = [self.timestamp_column] + data_cols
            y_cols = [self.timestamp_column] + [self.anomaly_label_column]
        # Assumes anomaly_label_column is column contains target/label column
        else:
            x_cols = data_cols

            y_cols = [
                self.anomaly_label_column
            ]  # -- TODO: this returns [nSmp,0] empty dataframe!

        x = all_data.iloc[:, x_cols]
        # x = all_data
        self.actual_used_feature_names = x.columns.tolist()
        y = all_data.iloc[:, y_cols]
        # to be implemented to extract X,Y from get_test_data

        # now, reindex
        # if there is a timestamp, we offset by one (timestamp is first column)

        # make a copy before reindexing
        # note, these are likely different from the other orig_ attributes which handle string names
        self.orig_timestamp_column_idx = copy(self.timestamp_column)
        self.orig_feature_columns_idx = copy(self.feature_columns)
        self.orig_target_columns_idx = copy(self.target_columns)
        self.orig_anomaly_label_column_idx = copy(self.anomaly_label_column)
        self.orig_data_columns_idx = copy(data_cols)

        if (
                self.return_timestamp_column
                and self.timestamp_column is not None
                and self.timestamp_column != -1
        ):
            self.timestamp_column = 0
            offset = 1
        else:
            self.timestamp_column = -1
            offset = 0
        self.target_columns = [
            offset + data_cols.index(tgt) for tgt in self.target_columns
        ]
        self.feature_columns = [
            offset + data_cols.index(fet) for fet in self.feature_columns
        ]

        self.anomaly_label_column = offset

        return x, y  # dataframes

    """
    """

    def read_X_Y_holdout_test(self, holdout_file_path=None):
        """
        Reads X,Y from given file in case we want to specify holdout files for test and train.
        Should not set the df_all or train should just return X, Y based on the input file provided

        :param holdout_file_path: path to hold out file which contains test data
        :return: returns x, y split of test data read from file
        """

        raise NotImplemented("Not implemented")

    # lookback window should be computed outside and set here so it can be used for future data proc functions
    # or lookback will need to be passed to functions needind lookback
    def set_lookback_window(self, lookback_window):
        self.lookback_window = lookback_window

    def get_lookback_window(self):
        return self.lookback_window

    def split_test_train(self, x, y, test_size):
        """
        Function using sklearn to split x,y into TRAIN and TEST set
        based on test_size which can be either a fraction or absolute integer.

        :param x,y: dataframes of same length but different columns
        :param test_size: either a float fraction or int to specify the size of TEST set
        :return:
            TRAIN/TEST sets of x,y as dataframes
        """

        try:
            X_train, X_test, y_train, y_test = train_test_split(
                x, y, test_size=test_size, shuffle=False, random_state=self.random_state
            )
            if VERBOSE:
                tslogger.info(20 * "*" + " SPLITTED X/y_train X/y_test: " + 20 * "*")
                tslogger.info(
                    "== Type of input x/y: %s" % str(str(type(x)) + str(type(y)))
                )
                tslogger.info(
                    "== input x/y.shape: %s test_size: %s"
                    % (
                        str(x.shape)
                        + str(y.shape), str(test_size)
                    )
                )
                tslogger.info("== test_size: %s" % (str(test_size)))
                tslogger.info(
                    "== shape of 4 dataframes X/y_train/test after splitting: %s"
                    % (
                            str(X_train.shape)
                            + str(y_train.shape)
                            + str(X_test.shape)
                            + str(y_test.shape)
                    )
                )
                tslogger.info(70 * "*")
        except Exception as e:
            raise ValueError("\n Error in splitting x,y into Train/Test lists due to: %s" % e)

        return X_train, X_test, y_train, y_test

    def _get_original_time_values_on_holdout(self, df):
        result = None
        if self.timestamp_column is not None and self.timestamp_column != -1 and self.holdout_param > 0:
            all_data_len = len(df)
            if self.holdout_param < 1:
                holdout_len = int(all_data_len * self.holdout_param)
            else:
                holdout_len = int(self.holdout_param)

            ori_time_values = df.iloc[:, self.timestamp_column]
            if self.evaluation_param is not None and self.evaluation_param > 0:
                a = ori_time_values.iloc[:-self.evaluation_param]
                result = a[all_data_len - self.evaluation_param - holdout_len:]
            else:
                result = ori_time_values[all_data_len - holdout_len:]
        return result
