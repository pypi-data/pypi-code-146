import pandas as pd

from ..abstract import AbstractNode


class SorterGPS(AbstractNode):
    """
    Module ordering gps records over unixtime
    """

    def __init__(
        self,
        unixtime_column: str,
    ):
        self.unixtime_column = unixtime_column

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X.sort_values(by=[self.unixtime_column], inplace=True)
        X.reset_index(drop=True, inplace=True)
        return X
