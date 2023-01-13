"""Identification of drift between 2 series that should have a linear relation by means of cusum.

<p>This check identifies periods where the values from sensors that are in a linear relationship
start to drift away from their expected values.</p>
<p><img src='../static/images/reporting/sensor_drift.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where  drift is identified. Imagine that 100 points are analyzed in a given time-frame
and that drift is detected for 10 (consecutive) points. The score for this check in that case would be
90% = 1 - 10 / 100. Which means that for 90% of all points no drift occurs.</p>
<div class="ts-check-impact">
<p>Changes in a physical relation between a set of series could indicate process or instrumentation issues.</p>
</div>
"""

import pandas as pd
import numpy as np


from timeseer import (
    AnalysisResult,
    BivariateCheckResult,
    DataType,
    MultivariateAnalysisInput,
    ModuleParameterType,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    get_smape_threshold_based_on_sensitivity,
)


_CHECK_NAME = "redundant sensor drift (smape)"
_EVENT_FRAME_NAME = "redundant sensor drift (smape)"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": 2,
            "max_series": 2,
        },
        {
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
            "helpText": "Sensitivity influences the SMAPE cutoff for redundant sensor smape cusum.",
        },
    ],
    "signature": "bivariate",
}


def _clean_input(inputs):
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
        .interpolate("time")
        .dropna()
        .sort_index()
    )


def _get_smape(concatenated_df):
    series_a = concatenated_df.iloc[:, 0].values
    series_b = concatenated_df.iloc[:, 1].values
    top = np.abs(series_a - series_b)
    denom = np.abs(series_a) + np.abs(series_b)
    return np.divide(top, denom, out=np.zeros_like(top), where=denom != 0)


def _cusum(drift_series, likelihood_function, anomaly_threshold):
    smape = drift_series[0]["drifts"][0]
    s_high = np.zeros_like(smape)
    s_low = np.zeros_like(smape)
    for i in np.arange(1, len(smape)):
        s_high[i] = np.max([0, smape[i] - likelihood_function + s_high[i - 1]])
        s_low[i] = np.max([0, -likelihood_function - smape[i] + s_low[i - 1]])
    anomalies = (s_high > anomaly_threshold) | (s_low > anomaly_threshold)
    return anomalies


def _get_intervals(anomalies, df):
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


def _get_result_per_series(analysis_input, series, df) -> BivariateCheckResult:
    threshold = 0.25
    if "sensitivity" in analysis_input.parameters:
        threshold = get_smape_threshold_based_on_sensitivity(
            analysis_input.parameters["sensitivity"]
        )

    anomalies = _cusum(series, 0.05, threshold)
    intervals = _get_intervals(anomalies, df)
    frames = event_frames_from_dataframe(intervals)

    return BivariateCheckResult(
        _CHECK_NAME,
        series[0]["series_x"],
        series[0]["series_y"],
        event_frames=list(frames),
    )


def _get_individual_difference_series(error, series):
    results = []
    results.append({"series_x": series[0], "series_y": series[1], "drifts": [error]})
    return results


def _is_valid_input(analysis_input: MultivariateAnalysisInput) -> tuple[str, bool]:
    if len(_clean_input(analysis_input.inputs)) == 0:
        return "No data", False
    return "OK", True


def _run_detect_redundant_sensor_cusum(
    analysis_input: MultivariateAnalysisInput,
) -> BivariateCheckResult:
    inputs = analysis_input.inputs

    concatenated_df = _clean_input(inputs)

    error = _get_smape(concatenated_df)

    series = [series.metadata.series for series in inputs]
    individual_difference_series = _get_individual_difference_series(error, series)

    return _get_result_per_series(
        analysis_input, individual_difference_series, concatenated_df
    )


def run(
    analysis_input: MultivariateAnalysisInput,
):  # pylint: disable=missing-function-docstring

    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    results = _run_detect_redundant_sensor_cusum(analysis_input)

    return AnalysisResult(bivariate_check_results=[results])
