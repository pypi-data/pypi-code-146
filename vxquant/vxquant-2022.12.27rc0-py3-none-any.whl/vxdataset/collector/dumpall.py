"""下载全部基础数据"""

import logging
import tushare as ts
import polars as pl
from pathlib import Path
from tqdm import tqdm
from vxutils import logger, to_datetime
from vxquant.model.nomalize import to_symbol
from vxdataset.datasource.ifind import thsHQAPI

root = logging.getLogger("")
for hdl in root.handlers:
    root.removeHandler(hdl)

ts.set_token("854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c")
REFLASH_TOKEN = """eyJzaWduX3RpbWUiOiIyMDIzLTAxLTA0IDA5OjM2OjMyIn0=.eyJ1aWQiOiI2NTg2MzQyMzEifQ==.E4135F388BC621D395F5290DBD760E7C00ED8CDD2F0A1CCB320B77D0CA926761"""
ths_api = thsHQAPI(REFLASH_TOKEN)

HQ_COLUMNS = [
    "symbol",
    "date",
    "open",
    "high",
    "low",
    "close",
    "yclose",
    "volume",
    "amount",
    "pct_chg",
]

IND_COLUMNS = [
    "turnover_rate",
    "turnover_rate_f",
    "volume_ratio",
    "pe",
    "pe_ttm",
    "pb",
    "ps",
    "ps_ttm",
    "dv_ratio",
    "dv_ttm",
    "total_share",
    "float_share",
    "free_share",
    "total_mv",
    "circ_mv",
]

IND_COLUMNS_INDEX = [
    "total_mv",
    "float_mv",
    "total_share",
    "float_share",
    "free_share",
    "turnover_rate",
    "turnover_rate_f",
    "pe",
    "pe_ttm",
    "pb",
]


def dump_allstock(data_path):
    pro = ts.pro_api()
    df = pro.trade_cal(
        exchange="", start_date="19900101", end_date="21991231", is_open=1
    )

    start_date = df["cal_date"].iloc[0]
    end_date = df["cal_date"].iloc[-1]
    ts_codes = []
    for lstatus in ["L", "D", "P"]:
        df = pro.stock_basic(list_status=lstatus, fields="ts_code")
        logger.info(f"股票状态 {lstatus}: {df.shape[0]}只股票")
        ts_codes.extend(df["ts_code"])

    datas = []

    for code in tqdm(ts_codes):
        hq = ts.pro_bar(
            code, start_date=start_date, end_date=end_date, asset="E", adj="qfq"
        )
        if hq.empty:
            logger.warning(f"{code} 无数据，跳过.")
            continue

        hq = pl.from_pandas(hq)
        ind = ts.pro_api().daily_basic(
            ts_code=code,
            start_date=start_date,
            end_date=end_date,
            fields=",".join(["trade_date", "ts_code"] + IND_COLUMNS),
        )
        ind = pl.from_pandas(ind)
        ind = ind.with_columns([pl.col(IND_COLUMNS).cast(pl.Float64)])
        df = hq.join(ind, on=["trade_date", "ts_code"])
        datas.append(df)

    data = pl.concat(datas)
    data = (
        data.with_columns(
            [
                pl.col("ts_code")
                .apply(lambda x: f"{x[-2:]}SE.{x.split('.')[0]}")
                .alias("symbol"),
                pl.col("trade_date").apply(to_datetime).alias("date"),
                pl.col("pre_close").alias("yclose"),
                pl.col("vol").alias("volume"),
                (pl.col("amount") * 1000).alias("amount"),
            ]
        )
        .sort(by="date")
        .select(HQ_COLUMNS + IND_COLUMNS)
    )

    data.write_parquet("examples/data/allstock.parquet")
    logger.info(
        f"保存数据文件: {Path(data_path,'allstock.parquet').as_posix()}, {data.shape[0]}条数据"
    )


def dump_allindex(data_path):
    pro = ts.pro_api()
    df = pro.trade_cal(
        exchange="", start_date="19900101", end_date="21991231", is_open=1
    )

    start_date = df["cal_date"].iloc[0]
    end_date = df["cal_date"].iloc[-1]

    markets = ["SSE", "SZSE"]
    indexes = []
    for market in markets:
        index_df = ts.pro_api().index_basic(market=market)
        indexes.extend(index_df["ts_code"])
        logger.info(f"市场{market} 共有指数: {index_df.shape[0]}个")
    indexes = [ind for ind in indexes if ind[:3] in ["000", "399"] and len(ind) <= 9]
    logger.info(f"剔除无效指数，剩余指数{len(indexes)}个.")

    datas = []
    for code in tqdm(indexes):
        try:
            hq = ts.pro_api().index_daily(
                ts_code=code, start_date=start_date, end_date=end_date
            )
            if hq.empty:
                logger.warning(f"{code} 没有数据，跳过")
                continue
            datas.append(pl.from_pandas(hq))
        except Exception as e:
            logger.info(f"{code} 获取数据失败: {e}")
    data = pl.concat(datas)
    data = (
        data.with_columns(
            [
                pl.col("ts_code")
                .apply(lambda x: f"{x[-2:]}SE.{x.split('.')[0]}")
                .alias("symbol"),
                pl.col("trade_date").apply(to_datetime).alias("date"),
                pl.col("pre_close").alias("yclose"),
                pl.col("vol").alias("volume"),
                (pl.col("amount") * 1000).alias("amount"),
            ]
        )
        .sort("date")
        .select(HQ_COLUMNS)
    )
    data.write_parquet("examples/data/allindex.parquet")
    logger.info(
        f"保存数据文件: {Path(data_path,'allindex.parquet').as_posix()}, {data.shape[0]}条数据"
    )


def dump_allcbond(data_path):
    pro = ts.pro_api()
    df = pro.cb_basic()
    df = pl.from_pandas(df)
    print(
        df.sort("list_date").filter(pl.col("list_date").is_null()).select(["stk_code"])
    )


if __name__ == "__main__":
    dump_allindex("data/")
    # data = pl.read_parquet("examples/data/allindex.parquet")
    # print(data.sort("date"))
    # print(data.groupby("symbol").agg([
    #    pl.col("date").min().alias("start_date"),
    #    pl.col("date").max().alias("end_date"),
    # ]))
    # print(data['symbol'].unique())
