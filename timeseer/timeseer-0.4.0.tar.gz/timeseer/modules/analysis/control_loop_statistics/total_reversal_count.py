"""
Total reversal count
"""

import numpy as np
import pandas as pd


import timeseer
from timeseer import AnalysisInput, AnalysisResult, DataType


META: dict = {
    "statistics": [
        {"name": "Total reversal count"},
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


def _run_total_reversal_count(df: pd.DataFrame) -> int:
    df = _clean_dataframe(df)
    df_diff = df.diff()
    df_diff_sgn = np.sign(df_diff.loc[~(df_diff["value"] == 0)])
    df_diff_sgn_diff = pd.DataFrame(df_diff_sgn).diff().dropna()
    return len(df_diff_sgn_diff.loc[~(df_diff_sgn_diff["value"] == 0)])


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)
    reversals = _run_total_reversal_count(analysis_input.data)
    return timeseer.AnalysisResult(
        statistics=[timeseer.Statistic(META["statistics"][0]["name"], "int", reversals)]
    )
