from typing import List
import pandas as pd

from ..abstract import AbstractNode


class UniqueTimestampConstraint(AbstractNode):
    """
    Module validating constrain that timestamp must be unique
    """

    def __init__(
        self,
        source_datetime: str,
    ):
        self.source_datetime = source_datetime

    def fit(self, X, y=None):
        return self

    def __get_mask_of_duplicates(self, X: pd.DataFrame) -> pd.Series:
        return X.duplicated([self.source_datetime])

    def __has_timestamp_duplicate(self, duplicate_mask: pd.Series) -> bool:
        return duplicate_mask.any()

    def __get_duplicated_timestamps(
        self,
        X: pd.DataFrame,
        duplicate_mask: pd.Series,
    ) -> List[str]:
        return X.loc[duplicate_mask, self.source_datetime].tolist()

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        duplicate_mask = self.__get_mask_of_duplicates(X)
        if self.__has_timestamp_duplicate(duplicate_mask):
            timestamps = self.__get_duplicated_timestamps(X=X, duplicate_mask=duplicate_mask)
            message = f"Duplicated timestamps met: {timestamps}"
            raise ValueError(message)
        return X
