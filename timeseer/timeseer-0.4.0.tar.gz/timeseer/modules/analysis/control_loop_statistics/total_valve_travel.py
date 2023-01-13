"""
Total valve travel
"""

import pandas as pd


import timeseer
from timeseer import AnalysisInput, AnalysisResult, DataType


META: dict = {
    "statistics": [
        {"name": "Total valve travel"},
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    position = analysis_input.metadata.get_field_by_name("control loop")
    if position not in ["OP", "MV"]:
        return "Only applicable to OP or MV", False
    return "OK", True


def _run_total_valve_travel(df: pd.DataFrame) -> float:
    df = _clean_dataframe(df)
    total_travel = df.diff().dropna().abs().sum()
    return total_travel["value"]


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)
    total_valve_travel = _run_total_valve_travel(analysis_input.data)
    return timeseer.AnalysisResult(
        statistics=[
            timeseer.Statistic(
                META["statistics"][0]["name"], "float", total_valve_travel
            )
        ]
    )
