import polars as pl
from gm import api as gm_api
from vxdataset.loaders.base import vxDataLoader

INDICATOR_COLUMNS = [
    "date",
    "symbol",
    "frequency",
    "open",
    "high",
    "low",
    "close",
    "yclose",
    "amount",
    "volume",
    "turnoverratio",
    "transactioncount",
    "interest",
    "pct_change",
    "total_capital",
    "flow_capital",
    "pe_ttm",
    "pb",
    "dy",
]


class gmDataLoader(vxDataLoader):
    def __init__(self, gm_token: str = ""):
        """掘进量化数据加载器

        Keyword Arguments:
            gm_token {str} -- 掘进量化数据接口的token (default: {""})
        """
        if gm_token:
            gm_api.set_token(gm_token)

    def load_one_df(self, symbol, start_date, end_date) -> pl.DataFrame:
        indicators = gm_api.get_fundamentals(
            table="trading_derivative_indicator",
            symbols=symbol,
            start_date=start_date,
            end_date=end_date,
            fields="TRADEDATE,DY,TOTMKTCAP,NEGOTIABLEMV,PB,PETTM,TURNRATE",
            df=True,
        )

        indicators.rename(
            columns={
                "end_date": "date",
                "DY": "dy",
                "TOTMKTCAP": "total_capital",
                "NEGOTIABLEMV": "flow_capital",
                "PB": "pb",
                "PETTM": "pe_ttm",
                "TURNRATE": "turnoverratio",
            },
            inplace=True,
        )
        indicators = pl.from_pandas(indicators)

        bars = gm_api.history(symbol, "1d", start_date, end_date, adjust=1, df=True)
        rename_dict = {col: col.lower() for col in bars.columns}
        rename_dict["eob"] = "date"
        rename_dict["pre_close"] = "yclose"
        bars.rename(columns=rename_dict, inplace=True)
        bars = pl.from_pandas(bars)

        return (
            indicators.join(bars, on=["date", "symbol"])
            .with_columns(
                [
                    (pl.col("close") / pl.col("yclose") - 1).alias("pct_change"),
                    pl.lit(0).alias("transactioncount"),
                    pl.lit(0).alias("interest"),
                ]
            )
            .select(INDICATOR_COLUMNS)
        )
