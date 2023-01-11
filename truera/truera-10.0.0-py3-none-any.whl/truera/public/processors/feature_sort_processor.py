from __future__ import annotations

import heapq
import sys
from typing import Sequence

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FeatureSortMethod  # pylint: disable=no-name-in-module
from truera.public.processors.processor import FitProcessor


class FeatureSortProcessor(object):

    # using negative of max int (sys.maxsize) instead of sys.float_info.max, because floatmax gets converted to inf in grpc
    _MIN_VALUE = -1 * sys.maxsize

    # using max int (sys.maxsize) instead of sys.float_info.max, because floatmax gets converted to inf in grpc
    # setting to near top (0.99) because some operations do a negation, and we want to disambiguate from _MIN_VALUE
    _MAX_VALUE = sys.maxsize * 0.99

    # Used because polyfit lines have some noise
    _NEAR_ZERO = 0.00000000001

    # Used to prevent divide by zero
    _MIN_DENOM = 0.0001

    _trend_methods = [
        FeatureSortMethod.LINEAR_TREND,
        FeatureSortMethod.CUBIC_TREND,
        FeatureSortMethod.TREND_LOW_RESIDUAL,
        FeatureSortMethod.TREND_OUTLIERS,
        FeatureSortMethod.TREND_R_SQUARED,
    ]

    @classmethod
    def _replace_low_inf_trend_to_min(cls, sort_df, trend_df):
        min_trend_influence = 0.00001
        trend_max = trend_df.abs().max().fillna(0.0)
        for f in sort_df:
            if trend_max[f] < min_trend_influence:
                sort_df[f] = cls._MIN_VALUE

    @classmethod
    def calc_absolute_value_sum(cls, data: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame()
        sort_df = df.append(data.abs().sum(), ignore_index=True)
        return sort_df

    @classmethod
    def calc_absolute_value_sum_mean_corrected(
        cls, data: pd.DataFrame
    ) -> pd.DataFrame:
        df = pd.DataFrame()
        sort_df = df.append((data - data.mean()).abs().sum(), ignore_index=True)
        return sort_df

    @classmethod
    def calc_variance(cls, data: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame()
        sort_df = df.append(data.var(ddof=0), ignore_index=True)
        return sort_df

    @classmethod
    def calc_abs_max(cls, data: pd.DataFrame) -> pd.DataFrame:
        df = pd.DataFrame()
        sort_df = df.append(data.abs().max(), ignore_index=True)
        return sort_df

    @classmethod
    def calc_multi_modal(cls, x: pd.DataFrame, y: pd.DataFrame) -> pd.DataFrame:
        # TODO: implement
        return None

    @classmethod
    def calc_linear_trend(
        cls, y: pd.DataFrame, linear_trend_df: pd.DataFrame,
        cubic_trend_df: pd.DataFrame
    ) -> pd.DataFrame:
        # TODO, expand definition to more multiple trend types
        df = pd.DataFrame()
        lin_residual = (y - linear_trend_df).pow(2).sum()
        cubic_residual = (y - cubic_trend_df).pow(2).sum()
        lin_ratio = cubic_residual / lin_residual
        lin_ratio[lin_residual <= cls._NEAR_ZERO] = cls._MAX_VALUE

        sort_df = df.append(lin_ratio, ignore_index=True)
        return sort_df

    @classmethod
    def calc_cubic_trend(
        cls, y: pd.DataFrame, linear_trend_df: pd.DataFrame,
        cubic_trend_df: pd.DataFrame
    ) -> pd.DataFrame:
        # TODO, expand definition to more multiple trend types
        return cls.calc_linear_trend(y, linear_trend_df, cubic_trend_df) * -1

    @classmethod
    def calc_trend_low_residual(
        cls, y: pd.DataFrame, trend_df: pd.DataFrame
    ) -> pd.DataFrame:
        df = pd.DataFrame()
        residual = (y - trend_df).pow(2).sum()
        residual[residual <= cls._NEAR_ZERO] = 0.0
        sort_df = df.append(-1 * residual, ignore_index=True)
        return sort_df

    @classmethod
    def calc_trend_r_squared(
        cls, y: pd.DataFrame, trend_df: pd.DataFrame
    ) -> pd.DataFrame:
        neg_residual = cls.calc_trend_low_residual(y, trend_df)
        var = cls.calc_variance(y)
        return 1 + neg_residual / var

    @classmethod
    def calc_trend_outliers(
        cls, y: pd.DataFrame, trend_df: pd.DataFrame
    ) -> pd.DataFrame:
        '''
        Compares the influence share increase from the 90th percentile to the maximum percentile for both positve and negative 
        '''
        df = pd.DataFrame()
        residual = (y - trend_df)
        residual[residual.abs() <= cls._NEAR_ZERO] = 0.0
        q1 = residual.quantile(q=0.0)
        q2 = residual.quantile(q=0.1)
        q3 = residual.quantile(q=0.9)
        q4 = residual.quantile(q=1.0)
        center_quantile_range = q3 - q2
        upper_quantile_range = q4 - q3
        lower_quantile_range = q2 - q1

        upper_outlierness = (upper_quantile_range + center_quantile_range
                            ) / (center_quantile_range + cls._MIN_DENOM)
        lower_outlierness = (lower_quantile_range + center_quantile_range
                            ) / (center_quantile_range + cls._MIN_DENOM)

        sort_df = df.append(
            pd.DataFrame([upper_outlierness, lower_outlierness]).max(),
            ignore_index=True
        )

        return sort_df

    @classmethod
    def calc_categorical_outliers(
        cls, x: pd.DataFrame, y: pd.DataFrame
    ) -> pd.DataFrame:
        '''
        Compares the top two absolute value of average influence categories.
        Scale the ratio by the top value to prefer larger influence features.
        (top abs average category)^2 / (second abs average category)
        '''
        sort_df = pd.DataFrame(columns=x.columns)
        min_categories = 4
        max_categories = 20

        for f in x:
            x_vals = x[f]
            y_vals = y[f]
            bucketized = {}
            unique_vals = x_vals.unique()

            if len(unique_vals) < min_categories or (
                is_numeric_dtype(x_vals) and len(unique_vals) > max_categories
            ):
                sort_df[f] = [cls._MIN_VALUE]
            else:
                for i in range(len(x_vals)):
                    x_val = x_vals[i]
                    y_val = y_vals[i]
                    if x_val not in bucketized:
                        bucketized[x_val] = []
                    bucketized[x_val].append(y_val)
                categorical_avgs = []

                for x_val in bucketized:
                    categorical_avgs.append(abs(np.average(bucketized[x_val])))
                top_two = heapq.nlargest(2, categorical_avgs)
                # Scale by the largest influence to give preference to larger outliers
                sort_df[f] = [
                    top_two[0] * top_two[0] / top_two[1]
                    if top_two[1] > cls._NEAR_ZERO else cls._MIN_VALUE
                ]
        return sort_df

    @classmethod
    def get_feature_sort_values(
        cls,
        data: pd.DataFrame,
        infs: pd.DataFrame,
        sort_methods: Sequence[FeatureSortMethod],
        spline_exclude_vals=None
    ) -> pd.DataFrame:
        dfs = []
        trend_check = any(item in cls._trend_methods for item in sort_methods)
        if trend_check:
            data, infs = FitProcessor.remove_spline_exclude_vals(
                data, infs, spline_exclude_vals
            )
            cubic_trend_df = FitProcessor.fit_poly_df(data, infs, poly_order=3)
            if FeatureSortMethod.LINEAR_TREND in sort_methods or FeatureSortMethod.CUBIC_TREND in sort_methods:
                linear_trend_df = FitProcessor.fit_poly_df(
                    data, infs, poly_order=1
                )

        for method in sort_methods:
            if (len(data) == 0):
                score_df = pd.DataFrame(columns=data.columns)
                score_df = score_df.append(
                    pd.Series(cls._MIN_VALUE, index=data.columns),
                    ignore_index=True
                )
            elif method == FeatureSortMethod.ABSOLUTE_VALUE_SUM:
                score_df = cls.calc_absolute_value_sum(infs)
            elif method == FeatureSortMethod.ABSOLUTE_VALUE_SUM_MEAN_CORRECTED:
                score_df = cls.calc_absolute_value_sum_mean_corrected(infs)
            elif method == FeatureSortMethod.VARIANCE:
                score_df = cls.calc_variance(infs)
            elif method == FeatureSortMethod.LINEAR_TREND:
                score_df = cls.calc_linear_trend(
                    infs,
                    linear_trend_df=linear_trend_df,
                    cubic_trend_df=cubic_trend_df
                )
                cls._replace_low_inf_trend_to_min(score_df, linear_trend_df)
            elif method == FeatureSortMethod.CUBIC_TREND:
                score_df = cls.calc_cubic_trend(
                    infs,
                    linear_trend_df=linear_trend_df,
                    cubic_trend_df=cubic_trend_df
                )
                cls._replace_low_inf_trend_to_min(score_df, cubic_trend_df)
            elif method == FeatureSortMethod.TREND_LOW_RESIDUAL:
                score_df = cls.calc_trend_low_residual(
                    infs, trend_df=cubic_trend_df
                )
                cls._replace_low_inf_trend_to_min(score_df, cubic_trend_df)
            elif method == FeatureSortMethod.TREND_R_SQUARED:
                score_df = cls.calc_trend_r_squared(
                    infs, trend_df=cubic_trend_df
                )
                cls._replace_low_inf_trend_to_min(score_df, cubic_trend_df)
            elif method == FeatureSortMethod.TREND_OUTLIERS:
                score_df = cls.calc_trend_outliers(
                    infs, trend_df=cubic_trend_df
                )
            elif method == FeatureSortMethod.MAX_INFLUENCE:
                score_df = cls.calc_abs_max(infs)
            elif method == FeatureSortMethod.MULTI_MODAL:
                score_df = cls.calc_multi_modal(data, infs)
            elif method == FeatureSortMethod.CATEGORICAL_OUTLIERS:
                score_df = cls.calc_categorical_outliers(data, infs)
            dfs.append(score_df.fillna(cls._MIN_VALUE))

        return pd.concat(dfs)
