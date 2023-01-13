"""Identification of sensor difference outliers between series.

<p>This check identifies periods where for redundant sensors the typical
difference is significantly altered compared to normal.</p>
<p><img src='../static/images/reporting/sensor_outlier.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where sensor drift is identified. Imagine that 100 points are analyzed in a given time-frame
and that drift is detected for 10 (consecutive) points. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no drift occurs.</p>
<div class="ts-check-impact">
<p>Changes in a physical relation between a set of series could indicate process or instrumentation issues.</p>
</div>
"""

import pandas as pd
import numpy as np

from pandas.api.types import is_string_dtype
from scipy.stats import zscore

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    MultivariateAnalysisInput,
    ModuleParameterType,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    get_mad_threshold_based_on_sensitivity,
)


_CHECK_NAME = "Sensor profile outlier"
_EVENT_FRAME_NAME = "Sensor profile outlier"
_MIN_SERIES = 2

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": _MIN_SERIES,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        },
    ],
    "parameters": [
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": """Sensitivity influences the median absolute deviation cutoff for
                           multivariate redundant sensor outliers.""",
        },
    ],
    "signature": "multivariate",
}


def _cusum(
    series: np.ndarray, threshold: float, anomaly_threshold: float
) -> np.ndarray:
    series = zscore(series, nan_policy="omit")
    series[np.isnan(series)] = 0
    positive_cusum = (series * 0).copy()
    negative_cusum = positive_cusum.copy()
    for i in np.arange(series.shape[0]):
        if i == 0:
            positive_cusum[i, :] = series[i, :]
            negative_cusum[i, :] = series[i, :]
        else:
            positive_cusum[i, :] = np.maximum(
                0, series[i, :] - threshold + positive_cusum[i - 1, :]
            )
            negative_cusum[i, :] = np.maximum(
                0, -threshold - series[i, :] + negative_cusum[i - 1, :]
            )
    anomalies = (positive_cusum > anomaly_threshold) | (
        negative_cusum > anomaly_threshold
    )
    return np.any(anomalies, axis=1)


def _get_intervals(df: pd.DataFrame, anomalies: pd.Series) -> pd.DataFrame:
    anomalies = pd.Series(data=anomalies, index=df.index)
    interval_grp = (anomalies != anomalies.shift().bfill()).cumsum()

    intervals = (
        df.assign(interval_grp=interval_grp)[anomalies]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = _EVENT_FRAME_NAME

    return intervals


def _make_diff_array(df: pd.DataFrame) -> np.ndarray:
    diff_array = np.zeros((df.shape[0], int(df.shape[1] * (df.shape[1] - 1) / 2)))
    idx = 0
    for i in range(df.shape[1] - 1):
        for j in range(i + 1, df.shape[1]):
            diff_array[:, idx] = df.iloc[:, i] - df.iloc[:, j]
            idx = idx + 1
    return diff_array


def _profile_outlier(
    analysis_input: MultivariateAnalysisInput, concatenated_df: pd.DataFrame
) -> np.ndarray:
    diff_array = _make_diff_array(concatenated_df)

    threshold = 3
    if "sensitivity" in analysis_input.parameters:
        threshold = get_mad_threshold_based_on_sensitivity(
            analysis_input.parameters["sensitivity"]
        )
    return _cusum(diff_array, 0.5, threshold)


def _clean_input(inputs: list[AnalysisInput], selected_index: int) -> pd.DataFrame:
    index = inputs[selected_index].data.index
    return (
        pd.concat(
            [
                series.data["value"][
                    ~series.data["value"].index.duplicated(keep="first")
                ]
                for series in inputs
            ],
            axis=1,
            sort=False,
        )
        .reindex(index)
        .interpolate("time")
        .dropna()
        .sort_index()
    )


def _get_median_archival_step(df: pd.DataFrame):
    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times.dropna()
    return pd.Timedelta(np.median(diff_times)).total_seconds()


def _run_mv_redundant_sensor_outlier(
    analysis_input: MultivariateAnalysisInput,
) -> list[EventFrame]:
    inputs = analysis_input.inputs
    selected_index = np.argmax(
        [_get_median_archival_step(inputs[i].data) for i in range(len(inputs))]
    )
    concatenated_df = _clean_input(inputs, int(selected_index))
    if len(concatenated_df) < 30:
        return []

    anomalies = _profile_outlier(analysis_input, concatenated_df)
    intervals = _get_intervals(concatenated_df, anomalies)

    frames = event_frames_from_dataframe(intervals)

    return list(frames)


def _filter_invalid_inputs(
    inputs: list[AnalysisInput],
) -> list[AnalysisInput]:
    valid_inputs = []
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            continue
        if check_input.data["value"].isnull().all():
            continue
        valid_inputs.append(check_input)
    return valid_inputs


def run(
    analysis_input: MultivariateAnalysisInput,
):  # pylint: disable=missing-function-docstring
    inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(inputs) < _MIN_SERIES:
        return AnalysisResult()

    frames = _run_mv_redundant_sensor_outlier(analysis_input)
    return AnalysisResult(event_frames=frames)
