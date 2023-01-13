"""Distribution of the range for a fleet.

<p class="scoring-explanation"></p>

<div class="ts-check-impact">
<p></p>
</div>
"""

import numpy as np

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    MultivariateAnalysisInput,
    Statistic,
    DataType,
)


_STATISTIC_NAME = "Fleet Range"

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


def _run_fleet_range(inputs: list[AnalysisInput]):
    values: list[float] = []
    for series_input in inputs:
        values = np.concatenate([values, series_input.data["value"].to_numpy()])

    try:
        hist, bin_edges = np.histogram(
            values,
            range=(np.nanmin(values), np.nanmax(values)),
            bins=20,
        )
        return hist, bin_edges
    except (ValueError, TypeError):
        return None, None


# pylint: disable=missing-function-docstring
def run(
    analysis_input: MultivariateAnalysisInput,
) -> AnalysisResult:
    inputs = analysis_input.inputs

    hist, bin_edges = _run_fleet_range(inputs)
    if hist is None:
        return AnalysisResult()
    histogram = dict(hist=hist.tolist(), bin_edges=bin_edges.tolist())
    statistic = Statistic(_STATISTIC_NAME, "histogram", histogram)
    return AnalysisResult(statistics=[statistic])
