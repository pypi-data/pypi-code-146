""" Calculate the distributed quantile sketch of the time series. """

from typing import Optional

import jsonpickle
import pandas as pd
import numpy as np

from ddsketch.ddsketch import DDSketch
from pandas.api.types import is_string_dtype

import timeseer

from timeseer import DataType


META: dict = {
    "statistics": [
        {"name": "Archival Sketch"},
        {"name": "Extremes Archival Sketch"},
        {"name": "Base Archival Sketch"},
        {"name": "Archival time mean"},
        {"name": "Archival time min"},
        {"name": "Archival time max"},
        {"name": "Archival time median"},
        {"name": "Archival Histogram"},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
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


def _get_up_quantiles_and_iqr_from_values(
    values: pd.Series,
) -> tuple[Optional[float], Optional[float], Optional[float]]:
    rel_values = values[values > 0]
    if len(rel_values) == 0:
        return None, None, None
    q25, q75 = np.nanquantile(rel_values, [0.25, 0.75])
    iqr = q75 - q25
    return q25, q75, iqr


def _get_down_quantiles_and_iqr_from_values(
    values: pd.Series,
) -> tuple[Optional[float], Optional[float], Optional[float]]:
    rel_values = values[values < 0]
    if len(rel_values) == 0:
        return None, None, None
    q25, q75 = np.nanquantile(rel_values, [0.25, 0.75])
    iqr = q75 - q25
    return q25, q75, iqr


def _get_quantiles_and_iqr_from_sketch(sketch: DDSketch) -> tuple[float, float, float]:
    q25, q75 = [sketch.get_quantile_value(q) for q in [0.25, 0.75]]
    iqr = q75 - q25
    return q25, q75, iqr


def _get_diff_times(df: pd.DataFrame) -> pd.Series:
    meas_times = df.index.to_series()
    return (meas_times - meas_times.shift()).dt.total_seconds()


def _get_extremes_archival_sketch(
    diff_times: pd.Series,
    diff_values: pd.Series,
    extremes_archival_sketch: DDSketch,
    jump_up_sketch: DDSketch,
    jump_down_sketch: DDSketch,
) -> DDSketch:
    if extremes_archival_sketch is None:
        extremes_archival_sketch = DDSketch(0.001)

    if jump_up_sketch is None:
        _, up_q75, up_iqr = _get_up_quantiles_and_iqr_from_values(diff_values)
    if jump_up_sketch is not None:
        _, up_q75, up_iqr = _get_quantiles_and_iqr_from_sketch(jump_up_sketch)
    if jump_down_sketch is None:
        down_q25, _, down_iqr = _get_down_quantiles_and_iqr_from_values(diff_values)
    if jump_down_sketch is not None:
        down_q25, _, down_iqr = _get_quantiles_and_iqr_from_sketch(jump_down_sketch)

    ups = np.array([False] * len(diff_values))
    downs = np.array([False] * len(diff_values))

    if up_q75 is not None and up_iqr is not None:
        ups = np.array(diff_values > (up_q75 + 3 * up_iqr))
    if down_q25 is not None and down_iqr is not None:
        downs = np.array(diff_values < (down_q25 - 3 * down_iqr))

    extremes = ups | downs

    for v in diff_times[extremes]:
        if not np.isnan(v):
            extremes_archival_sketch.add(v)

    return extremes_archival_sketch


# pylint: disable=too-many-locals
def _get_base_archival_sketch(
    diff_times: pd.Series,
    diff_values: pd.Series,
    base_archival_sketch: DDSketch,
    jump_up_sketch: DDSketch,
    jump_down_sketch: DDSketch,
):
    if base_archival_sketch is None:
        base_archival_sketch = DDSketch(0.001)

    if jump_up_sketch is None:
        up_q25, up_q75, _ = _get_up_quantiles_and_iqr_from_values(diff_values)
    if jump_up_sketch is not None:
        up_q25, up_q75, _ = _get_quantiles_and_iqr_from_sketch(jump_up_sketch)
    if jump_down_sketch is None:
        down_q25, down_q75, _ = _get_down_quantiles_and_iqr_from_values(diff_values)
    if jump_down_sketch is not None:
        down_q25, down_q75, _ = _get_quantiles_and_iqr_from_sketch(jump_down_sketch)

    ups = np.array([False] * len(diff_values))
    downs = np.array([False] * len(diff_values))

    if up_q75 is not None:
        ups = np.array(diff_values <= up_q75) & np.array(diff_values >= up_q25)
    if down_q25 is not None:
        downs = np.array(diff_values <= down_q75) & np.array(diff_values >= down_q25)

    bases = ups | downs

    for v in diff_times[bases]:
        if not np.isnan(v):
            base_archival_sketch.add(v)

    return base_archival_sketch


def _get_archival_sketch(diff_times: pd.Series, archival_sketch: DDSketch) -> DDSketch:
    if archival_sketch is None:
        archival_sketch = DDSketch(0.001)

    for v in diff_times:
        if not np.isnan(v):
            archival_sketch.add(v)

    return archival_sketch


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


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].sort_index()


# pylint: disable=too-many-arguments
def _run_get_sketch(
    analysis_input: timeseer.AnalysisInput,
    archival_sketch: DDSketch,
    extremes_archival_sketch: DDSketch,
    base_archival_sketch: DDSketch,
    jump_up_sketch: DDSketch,
    jump_down_sketch: DDSketch,
) -> tuple[DDSketch, DDSketch, DDSketch]:
    df = _clean_dataframe(analysis_input.data)

    diff_times = _get_diff_times(df)
    diff_values = df["value"] - df["value"].shift()

    archival_sketch = _get_archival_sketch(diff_times, archival_sketch)
    extremes_archival_sketch = _get_extremes_archival_sketch(
        diff_times,
        diff_values,
        extremes_archival_sketch,
        jump_up_sketch,
        jump_down_sketch,
    )
    base_archival_sketch = _get_base_archival_sketch(
        diff_times, diff_values, base_archival_sketch, jump_up_sketch, jump_down_sketch
    )

    return archival_sketch, extremes_archival_sketch, base_archival_sketch


def _get_relevant_statistic(
    analysis_input: timeseer.AnalysisInput, stat_name: str
) -> Optional[DDSketch]:
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


def _is_valid_input(analysis_input: timeseer.AnalysisInput) -> tuple[str, bool]:
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    return "OK", True


def _get_previous_values(
    analysis_input: timeseer.AnalysisInput,
) -> tuple[
    DDSketch | None, DDSketch | None, DDSketch | None, DDSketch | None, DDSketch | None
]:
    archival_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")
    extremes_archival_sketch = _get_relevant_statistic(
        analysis_input, "Extremes Archival Sketch"
    )
    base_archival_sketch = _get_relevant_statistic(
        analysis_input, "Base Archival Sketch"
    )
    jump_up_sketch = _get_relevant_statistic(analysis_input, "Jump Up Sketch")
    jump_down_sketch = _get_relevant_statistic(analysis_input, "Jump Down Sketch")
    return (
        archival_sketch,
        extremes_archival_sketch,
        base_archival_sketch,
        jump_up_sketch,
        jump_down_sketch,
    )


def _get_archival_stats(archival_sketch: DDSketch) -> list[timeseer.Statistic]:
    statistics = []
    if archival_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][0]["name"],
                "sketch",
                jsonpickle.encode(archival_sketch),
            )
        )
        archival_mean = archival_sketch.avg
        statistics.append(
            timeseer.Statistic(
                META["statistics"][3]["name"],
                "hidden",
                archival_mean,
            )
        )

        archival_min = archival_sketch.min
        statistics.append(
            timeseer.Statistic(
                META["statistics"][4]["name"],
                "hidden",
                archival_min,
            )
        )
        archival_max = archival_sketch.max
        statistics.append(
            timeseer.Statistic(
                META["statistics"][5]["name"],
                "hidden",
                archival_max,
            )
        )
        archival_median = archival_sketch.get_quantile_value(0.5)
        if archival_sketch.min == archival_sketch.max:
            archival_median = archival_sketch.max
        statistics.append(
            timeseer.Statistic(
                META["statistics"][6]["name"],
                "hidden",
                archival_median,
            )
        )
        values = [
            ("Min", float(archival_min)),
            ("Max", float(archival_max)),
            ("Mean", float(archival_mean)),
            ("Median", float(archival_median)),
        ]
        table_statistics = timeseer.Statistic(
            "Archival statistics (sec)", "table", values
        )
        statistics.append(table_statistics)
    return statistics


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return timeseer.AnalysisResult(condition_message=message)

    (
        archival_sketch,
        extremes_archival_sketch,
        base_archival_sketch,
        jump_up_sketch,
        jump_down_sketch,
    ) = _get_previous_values(analysis_input)

    archival_sketch, extremes_archival_sketch, base_archival_sketch = _run_get_sketch(
        analysis_input,
        archival_sketch,
        extremes_archival_sketch,
        base_archival_sketch,
        jump_up_sketch,
        jump_down_sketch,
    )

    statistics = _get_archival_stats(archival_sketch)

    if extremes_archival_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][1]["name"],
                "sketch",
                jsonpickle.encode(extremes_archival_sketch),
            )
        )
    if base_archival_sketch is not None:
        statistics.append(
            timeseer.Statistic(
                META["statistics"][2]["name"],
                "sketch",
                jsonpickle.encode(base_archival_sketch),
            )
        )

    hist, bin_edges = _get_histogram(archival_sketch)
    if hist is not None:
        histogram = dict(hist=hist.tolist(), bin_edges=bin_edges.tolist())
        statistics.append(
            timeseer.Statistic(META["statistics"][7]["name"], "histogram", histogram)
        )

    if len(statistics) == 0:
        return timeseer.AnalysisResult(condition_message="No statistics")

    return timeseer.AnalysisResult(
        statistics=statistics,
        last_analyzed_point=analysis_input.data.index[-2].to_pydatetime(),
    )
