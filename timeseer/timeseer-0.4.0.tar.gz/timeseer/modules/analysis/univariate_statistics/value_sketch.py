""" Calculate the distributed quantile sketch of the time series. """

import jsonpickle
import pandas as pd
import numpy as np

from ddsketch.ddsketch import DDSketch
from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType


META: dict = {
    "statistics": [
        {"name": "Value Sketch"},
        {"name": "Mean"},
        {"name": "Min"},
        {"name": "Max"},
        {"name": "Median"},
        {"name": "Standard Deviation"},
        {"name": "Value histogram"},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64, None],
        }
    ],
    "signature": "univariate",
}


def _get_bucket_intervals(
    bucket_index_list: list[int], gamma: float
) -> list[list[float]]:
    return [
        [gamma ** (bucket_index - 1), gamma**bucket_index]
        for bucket_index in bucket_index_list
    ]


def _get_sketch_summary_negative(sketch: DDSketch) -> pd.DataFrame:
    gamma = (1 + sketch.relative_accuracy) / (1 - sketch.relative_accuracy)

    bucket_offset = sketch.negative_store.offset
    bucket_counts = sketch.negative_store.bins
    sketch_summary_df = pd.DataFrame({"Bucket counts": bucket_counts})
    sketch_summary_df.index = sketch_summary_df.index + bucket_offset
    bucket_intervals = _get_bucket_intervals(list(sketch_summary_df.index), gamma)
    sketch_summary_df["Bucket intervals"] = [[-i[0], -i[1]] for i in bucket_intervals]
    quantile_values = [
        -2 * gamma**i / (gamma + 1) for i in list(sketch_summary_df.index)
    ]
    sketch_summary_df["Quantile values"] = quantile_values
    return sketch_summary_df


def _get_sketch_summary_positive(sketch: DDSketch) -> pd.DataFrame:
    gamma = (1 + sketch.relative_accuracy) / (1 - sketch.relative_accuracy)

    bucket_offset = sketch.store.offset
    bucket_counts = sketch.store.bins
    sketch_summary_df = pd.DataFrame({"Bucket counts": bucket_counts})
    sketch_summary_df.index = sketch_summary_df.index + bucket_offset
    bucket_intervals = _get_bucket_intervals(list(sketch_summary_df.index), gamma)
    sketch_summary_df["Bucket intervals"] = bucket_intervals
    quantile_values = [
        2 * gamma**i / (gamma + 1) for i in list(sketch_summary_df.index)
    ]
    sketch_summary_df["Quantile values"] = quantile_values

    return sketch_summary_df


def _get_sketch_summary(sketch: DDSketch) -> pd.DataFrame:
    return pd.concat(
        [
            _get_sketch_summary_negative(sketch).reset_index(),
            _get_sketch_summary_positive(sketch).reset_index(),
        ],
        axis=0,
    ).rename(columns={"index": "Bucket index"})


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_get_sketch(
    analysis_input: timeseer.AnalysisInput, previous_sketch: DDSketch
) -> DDSketch:
    df = _clean_dataframe(analysis_input.data)
    if len(df) == 0:
        return previous_sketch

    if previous_sketch is None:
        previous_sketch = DDSketch(0.001)

    for v in df["value"]:
        previous_sketch.add(v)

    return previous_sketch


def _is_valid_input(analysis_input: timeseer.AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    return "OK", True


def _get_approx_std(sketch: DDSketch) -> float:
    sketch_summary_df = _get_sketch_summary(sketch)
    total_count = sketch.zero_count + sketch_summary_df["Bucket counts"].sum()
    sketch_mean = (
        sketch_summary_df["Bucket counts"] * sketch_summary_df["Quantile values"]
    ).sum() / total_count
    return np.sqrt(
        (
            (
                sketch_summary_df["Bucket counts"]
                * ((sketch_summary_df["Quantile values"] - sketch_mean) ** 2)
            ).sum()
        )
        / (total_count - 1)
    )


def _get_histogram(sketch: DDSketch, number_of_bins: int = 20):
    sketch_summary_df = _get_sketch_summary(sketch)
    quantile_value_list_for_histogram: list = []
    for _, row in sketch_summary_df.iterrows():
        quantile_value_list_for_histogram = quantile_value_list_for_histogram + (
            [row["Quantile values"]] * int(row["Bucket counts"])
        )
    quantile_value_list_for_histogram = quantile_value_list_for_histogram + int(
        sketch.zero_count
    ) * [0]
    counts, edges = np.histogram(quantile_value_list_for_histogram, bins=number_of_bins)
    return counts, edges


def _get_relevant_statistic(
    analysis_input: timeseer.AnalysisInput, stat_name: str
) -> DDSketch | None:
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


def _get_previous_values(analysis_input: timeseer.AnalysisInput) -> DDSketch:
    sketch = _get_relevant_statistic(analysis_input, "Value Sketch")
    return sketch


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    previous_sketch = _get_previous_values(analysis_input)
    sketch = _run_get_sketch(analysis_input, previous_sketch)
    if sketch is None:
        return timeseer.AnalysisResult(condition_message="No sketch")

    statistics = []
    statistics.append(
        timeseer.Statistic(
            META["statistics"][0]["name"], "sketch", jsonpickle.encode(sketch)
        )
    )
    stat_mean = sketch.avg
    statistics.append(
        timeseer.Statistic(META["statistics"][1]["name"], "hidden", stat_mean)
    )
    stat_min = sketch.min
    statistics.append(
        timeseer.Statistic(META["statistics"][2]["name"], "hidden", sketch.min)
    )
    stat_max = sketch.max
    statistics.append(
        timeseer.Statistic(META["statistics"][3]["name"], "hidden", stat_max)
    )
    stat_median = sketch.get_quantile_value(0.5)
    if sketch.min == sketch.max:
        stat_median = sketch.max
    statistics.append(
        timeseer.Statistic(META["statistics"][4]["name"], "hidden", stat_median)
    )
    stat_std = _get_approx_std(sketch)
    statistics.append(
        timeseer.Statistic(META["statistics"][5]["name"], "hidden", stat_median)
    )
    values = [
        ("Min", stat_min),
        ("Max", stat_max),
        ("Mean", stat_mean),
        ("Median", stat_median),
        ("Std", stat_std),
    ]
    statistics.append(timeseer.Statistic("Value statistics", "table", values))

    hist, bin_edges = _get_histogram(sketch)
    if hist is not None:
        histogram = dict(hist=hist.tolist(), bin_edges=bin_edges.tolist())
        statistics.append(
            timeseer.Statistic(META["statistics"][6]["name"], "histogram", histogram)
        )

    return timeseer.AnalysisResult(
        statistics=statistics,
        last_analyzed_point=analysis_input.data.index[-1].to_pydatetime(),
    )
