"""预处理"""


import polars as pl
import numpy as np
from typing import List, Any


class Processor:
    def __init__(self, features: List[str] = None):
        self._features = features

    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        pass


class DropnaProcessor(Processor):
    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        expr = (
            pl.col(self._features).is_not_null()
            if self._features
            else pl.all().is_not_null()
        )
        return datas.filter(expr)


class DrapCol(Processor):
    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        self._features = ["date", "symbol"] + self._features
        cols = [col for col in datas.columns if col not in self._features]
        return datas.select(["date", "symbol"] + cols)


class Fillna(Processor):
    def __init__(self, features: List[str] = None, filled_value: Any = None):
        super().__init__(features)
        self._filled_value = filled_value

    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        return datas.with_columns(pl.col(self._features).fill_nan(self._filled_value))


class MinMaxNorm(Processor):
    def __init__(self, features: List[str] = None, scale=3):
        super().__init__(features)

    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        datas = datas.with_columns(
            [
                pl.col(self._features)
                .when(
                    pl.col(self._features)
                    > (pl.col(self._features).mean() + 3 * pl.col(self._features).std())
                )
                .then(pl.col(self._features).mean() + 3 * pl.col(self._features).std())
                .otherwise(pl.col(self._features))
                .over("date")
            ]
        )
        datas = datas.with_columns(
            [
                pl.col(self._features)
                .when(
                    pl.col(self._features)
                    < (pl.col(self._features).mean() - 3 * pl.col(self._features).std())
                )
                .then(pl.col(self._features).mean() - 3 * pl.col(self._features).std())
                .otherwise(pl.col(self._features))
                .over("date")
            ]
        )
        return datas


class ZScoreNorm(Processor):
    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        return datas.with_columns(
            [
                (
                    pl.col(self._features)
                    - pl.col(self._features).mean() / pl.col(self._features).std()
                ).over("date"),
            ]
        )


x = x - x.median()
mad = x.abs().median()
x = np.clip(x / mad / 1.4826, -3, 3)
if zscore:
    x -= x.mean()
    x /= x.std()


class RobustZScoreNorm(Processor):
    def __call__(self, datas: pl.DataFrame) -> pl.DataFrame:
        x = pl.col(self._features) - pl.col(self._features).median()
        mad = x.abs().median()
        x = np.clip()
        expr = ().abs().median()
