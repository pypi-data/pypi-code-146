"""数据指标计算器"""
import re
import polars as pl
from pathlib import Path
from vxutils import vxtime
from vxdataset.expr.ops import *
from typing import List
from vxutils import logger, to_datetime, vxWrapper
from vxquant.model.nomalize import to_symbol
from tqdm import tqdm


class vxDataHandler:
    def __init__(
        self, datas: pl.DataFrame, date_col: str = "date", symbol_col: str = "symbol"
    ):
        cols = [col for col in datas.columns if col not in [date_col, symbol_col]]
        self._datas = datas.with_columns(
            [
                pl.col(date_col).cast(str).apply(to_datetime).alias("date"),
                pl.col(symbol_col).cast(str).apply(to_symbol).alias("symbol"),
            ]
        ).select(["date", "symbol"] + list(cols))
        logger.info(f"加载数据{self._datas.shape[0]}条，数据基础指标:{cols}")
        desp = self._datas.groupby("symbol").agg(
            [
                pl.col("date").min().alias("start_date"),
                pl.col("date").max().alias("end_date"),
                pl.col("date").count().alias("count"),
            ]
        )
        logger.info(f"数据详情: {desp}")

    @classmethod
    def from_polars(cls, pldf: pl.DataFrame, date_col="date", symbol_col="symbol"):
        return cls(pldf)

    @classmethod
    def from_csv(cls, csv_path: str, date_col="date", symbol_col="symbol"):
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise OSError(f"csv_path({csv_path.as_posix()}) 不存在")

        if csv_path.is_dir():
            csv_files = csv_path.glob("*.[csv,txt]")
        elif csv_path.is_file() and Path(csv_path).suffix in (".csv", ".txt"):
            csv_files = [csv_path]
        else:
            raise OSError(f"csv_path({csv_path.as_posix()}) 文件格式不符合要求")

        data_list = []
        for csv_file in csv_files:
            try:
                df = pl.read_csv(csv_file)
                data_list.append(df)
            except Exception as e:
                logger.info(f"加载{csv_file}错误. {e}")
        datas = pl.concat(data_list)
        return cls(datas, date_col, symbol_col)

    @classmethod
    def from_parquet(cls, parquet_file: str):
        datas = pl.read_parquet(parquet_file)
        return cls(datas)

    def _parser_expr(self, name: str, feature: str) -> pl.Expr:
        # Following patterns will be matched:
        # - $close -> Feature("close")
        # - $close5 -> Feature("close5")
        # - $open+$close -> Feature("open")+Feature("close")
        # TODO: this maybe used in the feature if we want to support the computation of different frequency data
        # - $close@5min -> Feature("close", "5min")

        if not isinstance(feature, str):
            feature = str(feature)
        # Chinese punctuation regex:
        # \u3001 -> 、
        # \uff1a -> ：
        # \uff08 -> (
        # \uff09 -> )
        chinese_punctuation_regex = r"\u3001\uff1a\uff08\uff09"
        for pattern, new in [
            (
                rf"\$\$([\w{chinese_punctuation_regex}]+)",
                r'PFeature("\1")',
            ),  # $$ must be before $
            (rf"\$([\w{chinese_punctuation_regex}]+)", r'Feature("\1")'),
            # (r"(\w+\s*)\(", r"Operators.\1("),
        ]:  # Features  # Operators
            feature = re.sub(pattern, new, feature)

        return eval(feature).over("symbol").alias(name)

    def to_pandas(self):
        df = self._datas.to_pandas()
        return df.set_index(["date", "symbol"])

    def to_polars(self):
        return self._datas

    def to_csv(self, filename):
        with open(filename, "w") as f:
            self._datas.write_csv(f)

    def build_features(self, features) -> "vxDataHandler":
        with vxtime.timeit(f"build features: {list(features.keys())}"):
            exprs = [
                self._parser_expr(name, feature) for name, feature in features.items()
            ]
            self._datas = self._datas.sort(by="date").with_columns(exprs)
        return self

    def run_processors(self, processors: List) -> "vxDataHandler":
        processors = list(map(vxWrapper.init_by_config, processors))

    def dropna(self, features: List[str] = None) -> "vxDataHandler":
        with vxtime.timeit(f"dronna: {features or []}"):
            expr = (
                pl.col(features).is_not_null() if features else pl.all().is_not_null()
            )
            self._datas = self._datas.filter(expr)
        return self

    def dropcol(self, features: List[str]) -> "vxDataHandler":
        if not features:
            return self

        with vxtime.timeit(f"dropcol: {features}"):
            features = ["date", "symbol"] + features
            cols = [col for col in self._datas.columns if col not in features]
            self._datas = self._datas.select(["date", "symbol"] + cols)
            return self

    def tanh(self, features: List[str]) -> "vxDataHandler":
        pass


if __name__ == "__main__":
    features = {
        "high": "$high",
        "mom20": "Ref($close, 20)/$close",
        "ret": "$close/Ref($close,1)-1",
        "roc20": "Rank($high,252)",
    }
    # handler = vxDataHandler.from_parquet(
    #    "/Users/libao/src/开源代码/vxquant/examples/data/data.parquet"
    # )
    handler = vxDataHandler.from_csv(
        "/Users/libao/src/开源代码/vxquant/examples/data/sh000300.csv", symbol_col="code"
    )
    ds = handler.build_features(features).dropna().dropcol(["amount"]).to_polars()
    print(ds)
    # print(ds.filter(pl.col(["mom20", "roc20"]).is_not_null()))
