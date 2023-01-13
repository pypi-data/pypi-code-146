"""Identification of spikes in consecutive values.
"""

from datetime import timedelta

import pandas as pd
import numpy as np

from timeseer import AnalysisInput, AnalysisResult

from timeseer import DataType
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
)

META = {
    "checks": [
        {
            "name": "Spikes (upwards)",
            "event_frames": ["Spike outlier (upwards)"],
        },
        {
            "name": "Spikes (downwards)",
            "event_frames": ["Spike outlier (downwards)"],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _get_intervals(outliers, df, event_type):
    if outliers is None:
        return pd.DataFrame()
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _spread_active_points(active_series):
    ilocs = np.array(
        [active_series.index.get_loc(ind) for ind in active_series[active_series].index]
    )
    neighbor_ilocs = np.concatenate((ilocs - 1, ilocs + 1, ilocs), axis=None)
    result_series = active_series.copy()
    result_series.iloc[neighbor_ilocs] = True
    return result_series


def _is_valid_input(analysis_input) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    if not np.issubdtype(_clean_dataframe(analysis_input.data)["value"], float):
        return "Invalid data type", False
    return "OK", True


# pylint: disable=too-many-arguments
def _find_spikes(
    df,
    median_archival_step,
    isolation_threshold,
    asymmetry_threshold,
    window_size,
    strictness,
):
    time_threshold = timedelta(seconds=(median_archival_step * isolation_threshold))
    df["diff_B"] = df["value"].diff().bfill()
    df["diff_F"] = df["value"].diff().shift(-1).ffill()
    df["ts_diff_B"] = df.index.to_series().diff().bfill()
    df["ts_diff_F"] = df.index.to_series().diff().shift(-1).ffill()
    df["diff_abs"] = df["diff_B"].abs()
    df["q25"] = (
        df["diff_abs"].rolling(window_size, min_periods=1, center=True).quantile(0.25)
    )
    df["q75"] = (
        df["diff_abs"].rolling(window_size, min_periods=1, center=True).quantile(0.75)
    )
    df["iqr"] = df["q75"] - df["q25"]
    df["upper bound"] = df["q75"] + strictness * df["iqr"]
    df["peak"] = (
        (df["diff_B"] * df["diff_F"] < 0)
        & (df["diff_B"] > df["upper bound"])
        & (df["diff_F"] < -df["upper bound"])
    )
    df["valley"] = (
        (df["diff_B"] * df["diff_F"] < 0)
        & (df["diff_B"] < -df["upper bound"])
        & (df["diff_F"] > df["upper bound"])
    )
    df["spike"] = (df["peak"].isin([True])) | (df["valley"].isin([True]))
    df["symmetrical"] = (
        (df["spike"].isin([True]))
        & (abs(df["diff_F"] / df["diff_B"]) < (1 + asymmetry_threshold))
        & (abs(df["diff_F"] / df["diff_B"]) > (1 - asymmetry_threshold))
    )
    df["zigzag"] = (
        (df["spike"].isin([True])) & (df["spike"].shift(-1).isin([True]))
    ) | ((df["spike"].isin([True])) & (df["spike"].shift(1).isin([True])))
    df["isolated_spike"] = (
        (df["spike"].isin([True]))
        & (df["ts_diff_B"] > time_threshold)
        & (df["ts_diff_F"] > time_threshold)
    )
    df["up_spikes"] = (
        (df["peak"].isin([True]))
        & (df["symmetrical"].isin([True]))
        & (df["zigzag"].isin([False]))
        & (df["isolated_spike"].isin([False]))
    )
    df["down_spikes"] = (
        (df["valley"].isin([True]))
        & (df["symmetrical"].isin([True]))
        & (df["zigzag"].isin([False]))
        & (df["isolated_spike"].isin([False]))
    )
    return df["up_spikes"], df["down_spikes"]


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
def _run_spikes_check(
    analysis_input: AnalysisInput,
    median_archival_step,
    isolation_threshold=5,
    asymmetry_threshold=0.2,
    window_size=300,
    strictness=3,
):
    df = _clean_dataframe(analysis_input.data)

    active_points_upwards, active_points_downwards = _find_spikes(
        df,
        median_archival_step,
        isolation_threshold,
        asymmetry_threshold,
        window_size,
        strictness,
    )

    active_points_upwards = _spread_active_points(active_points_upwards)
    active_points_downwards = _spread_active_points(active_points_downwards)
    df = _clean_dataframe(analysis_input.data)

    intervals_downwards = _get_intervals(
        active_points_downwards, df, "Spike outlier (downwards)"
    )
    intervals_downwards = handle_open_intervals(df, intervals_downwards)

    intervals_upwards = _get_intervals(
        active_points_upwards, df, "Spike outlier (upwards)"
    )
    intervals_upwards = handle_open_intervals(df, intervals_upwards)

    all_intervals = pd.concat([intervals_downwards, intervals_upwards])

    frames = event_frames_from_dataframe(process_open_intervals(all_intervals))

    last_analyzed_point = None
    if len(df) > 1:
        last_analyzed_point = df.index[-2].to_pydatetime()

    return list(frames), last_analyzed_point


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    median_archival_step = _get_relevant_statistic(
        analysis_input, "Archival time median"
    )

    if median_archival_step is None:
        return AnalysisResult(condition_message="No median archival step")

    event_frames, last_analyzed_point = _run_spikes_check(
        analysis_input, median_archival_step
    )

    return AnalysisResult(
        event_frames=event_frames,
        last_analyzed_point=last_analyzed_point,
    )
