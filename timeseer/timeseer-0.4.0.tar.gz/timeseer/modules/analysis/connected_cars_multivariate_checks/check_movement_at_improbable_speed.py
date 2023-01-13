"""Check for movements at improbable speeds"""

from typing import Optional
import pandas as pd

from pandas.api.types import is_string_dtype
from geopy import distance

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    BivariateCheckResult,
    DataType,
    EventFrame,
    MultivariateAnalysisInput,
)

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_separate_active_intervals,
)

_CHECK_NAME = "Movement at improbable speed"
_EVENT_FRAME_NAME = "Movement at improbable speed"
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
            "min_data_points": 3,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64, DataType.CATEGORICAL],
        }
    ],
    "signature": "bivariate",
}


def _sort_positions(
    inputs: list[AnalysisInput],
) -> tuple[dict, dict]:
    df_dict = {}
    names_dict = {}
    for column in inputs:
        position = column.metadata.get_field_by_name("connected car")
        df = column.data
        df = df.rename({"value": position}, axis="columns")
        df_dict[position] = df
        names_dict[position] = column.metadata.series
    return df_dict, names_dict


def _match_ts_merge(df_dict: dict) -> Optional[pd.DataFrame]:
    if "Latitude" not in df_dict or "Longitude" not in df_dict:
        return None
    df = df_dict["Latitude"].join(df_dict["Longitude"], how="inner")
    return df


def _clean_dataframe(df):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _get_active_points(df):
    df["f-Lat"] = df["Latitude"].shift()
    df["f-Lon"] = df["Longitude"].shift()
    df["hours"] = (df.index.to_series().diff()).dt.total_seconds() / 3600
    clean_df = _clean_dataframe(df)
    clean_df["distance"] = clean_df.apply(
        lambda row: distance.distance(
            (row["Latitude"], row["Longitude"]), (row["f-Lat"], row["f-Lon"])
        ).kilometers,
        axis=1,
    )
    clean_df["avg-speed"] = clean_df["distance"] / clean_df["hours"]
    active_index = clean_df[clean_df["avg-speed"] > 200].index
    active_points = pd.Series(index=df.index, data=False)
    active_points.loc[active_index] = True
    return active_points


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


def _run_improbable_dislocation(
    inputs: list[AnalysisInput],
) -> tuple[list[EventFrame], dict, Optional[pd.Timestamp]]:
    df_dict, names_dict = _sort_positions(inputs)
    df = _match_ts_merge(df_dict)
    if df is None:
        return [], {}, None
    active_points = _get_active_points(df)

    intervals = get_separate_active_intervals(df, active_points, _CHECK_NAME)
    intervals = handle_open_intervals(df, intervals)
    last_analyzed_point = df.index[-1]
    frames = event_frames_from_dataframe(process_open_intervals(intervals))
    return list(frames), names_dict, last_analyzed_point


def run(  # pylint: disable=missing-function-docstring
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = _filter_invalid_inputs(analysis_input.inputs)

    if len(inputs) < _MIN_SERIES:
        return AnalysisResult()

    event_frames, names_dict, last_analyzed_point = _run_improbable_dislocation(inputs)

    results = [
        BivariateCheckResult(
            _CHECK_NAME,
            names_dict.get("Latitude"),
            names_dict.get("Longitude"),
            event_frames=event_frames,
        )
    ]

    if last_analyzed_point:
        last_analyzed_point = last_analyzed_point.to_pydatetime()
    return AnalysisResult(
        bivariate_check_results=results,
        last_analyzed_point=last_analyzed_point,
    )
