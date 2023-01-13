"""Distribution of the rate of change per second for a fleet.

<p class="scoring-explanation"></p>

<div class="ts-check-impact">
<p></p>
</div>
"""

import numpy as np

from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    MultivariateAnalysisInput,
    Statistic,
    DataType,
)


_STATISTIC_NAME = "Fleet Dynamics (change per sec)"

META = {
    "run": "before",
    "statistics": [
        {"name": _STATISTIC_NAME},
    ],
    "conditions": [
        {
            "min_series": 2,
            "min_data_points": 1,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64, None],
        }
    ],
    "signature": "multivariate",
}


def _run_fleet_dynamics(inputs: list[AnalysisInput]):
    values: list[float] = []
    for series_input in inputs:
        diff_values = abs(series_input.data["value"].diff())
        diff_times = series_input.data.index.to_series().diff().dt.total_seconds()
        values = np.concatenate([values, (diff_values / diff_times)])

    try:
        hist, bin_edges = np.histogram(
            values,
            range=(np.nanmin(values), np.nanmax(values)),
            bins=20,
        )
        return hist, bin_edges
    except (ValueError, TypeError):
        return None, None


def _are_valid_inputs(
    inputs: list[AnalysisInput],
) -> bool:
    for check_input in inputs:
        if is_string_dtype(check_input.data["value"]):
            return False
    return True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = analysis_input.inputs

    if not _are_valid_inputs(inputs):
        return AnalysisResult()

    hist, bin_edges = _run_fleet_dynamics(inputs)
    if hist is None:
        return AnalysisResult()
    histogram = dict(hist=hist.tolist(), bin_edges=bin_edges.tolist())
    statistic = Statistic(_STATISTIC_NAME, "histogram", histogram)
    return AnalysisResult(statistics=[statistic])
