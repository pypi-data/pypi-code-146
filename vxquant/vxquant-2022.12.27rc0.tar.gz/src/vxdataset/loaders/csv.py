"""CSV格式数据导入"""
import os
import pathlib
import polars as pl
from vxutils import to_datetime, vxtime, logger
from vxdataset.loaders.base import vxDataLoader, Date
from typing import Union, List
from tqdm import tqdm


class vxCSVLoader(vxDataLoader):
    def __init__(self, data_path: Union[str, pathlib.Path]) -> None:
        self._data_path = (
            pathlib.Path(data_path) if isinstance(data_path, str) else data_path
        )
        os.makedirs(self._data_path, exist_ok=True)

    def load_one_df(self, symbol, start_date=None, end_date=None):
        start_date = to_datetime(start_date or "1990-01-01").replace(tzinfo=None)
        end_date = to_datetime(end_date or "2199-12-31").replace(tzinfo=None)

        file = self._data_path.joinpath(f"{symbol}.csv")
        if not file.exists():
            logger.warning(f"{file.as_posix()} 不存在.")
            return None

        data = pl.read_csv(file.as_posix(), parse_dates=True)
        data = data.sort(by="date").with_columns(
            [pl.col("date").apply(lambda x: to_datetime(str(x)))]
        )

        return data.filter(pl.col("date").is_between(start_date, end_date))

    def load(
        self, symbols: List, start_date: Date = None, end_date: Date = None
    ) -> pl.DataFrame:
        return pl.concat(
            [self.load_one_df(symbol, start_date, end_date) for symbol in tqdm(symbols)]
        )


if __name__ == "__main__":
    loader = vxCSVLoader("examples/data/")
    with vxtime.timeit():
        df = loader.load(["sh000300", "sh000905"])

    # print(df)
