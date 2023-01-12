"""同花顺ifind数据接口"""

import polars as pl
import requests
from itertools import product
from concurrent.futures import ThreadPoolExecutor as Executor, as_completed
from functools import partial, lru_cache
from collections import defaultdict
from vxquant.model.exchange import vxTick
from vxquant.model.nomalize import to_symbol, normalize_freq
from vxquant.model.preset import vxMarketPreset
from vxquant.model.contants import SecType
from vxutils import vxtime, to_timestamp, vxDataConvertor, to_timestring
from typing import Tuple, Dict, Any

REFLASH_TOKEN = """eyJzaWduX3RpbWUiOiIyMDIzLTAxLTA0IDA5OjM2OjMyIn0=.eyJ1aWQiOiI2NTg2MzQyMzEifQ==.E4135F388BC621D395F5290DBD760E7C00ED8CDD2F0A1CCB320B77D0CA926761"""

TICK_FIELDS = [
    "preClose",
    "open",
    "high",
    "low",
    "latest",
    "amount",
    "volume",
    "turnoverRatio",
]

tick_indicators = {
    "preClose": "yclose",
    "open": "open",
    "high": "high",
    "low": "low",
    "lastest_price": "lasttrade",
    "amount": "amount",
    "volume": "volume",
    "ask1": "ask1_p",
    "ask2": "ask2_p",
    "ask3": "ask3_p",
    "ask4": "ask4_p",
    "ask5": "ask5_p",
    "askSize1": "ask1_v",
    "askSize2": "ask2_v",
    "askSize3": "ask3_v",
    "askSize4": "ask4_v",
    "askSize5": "ask5_v",
    "bid1": "bid1_p",
    "bid2": "bid2_p",
    "bid3": "bid3_p",
    "bid4": "bid4_p",
    "bid5": "bid5_p",
    "bidSize1": "bid1_v",
    "bidSize2": "bid2_v",
    "bidSize3": "bid3_v",
    "bidSize4": "bid4_v",
    "bidSize5": "bid5_v",
    "turnoverRatio": "turnoverratio",
    "tradeStatus": "status",
}

ths_status_map = {"交易": "NORMAL", None: ""}

thsTickConvertor = vxDataConvertor(vxTick)


def get_thscol(thsdata, col):
    return thsdata["table"][col][0]


for ths_col, target_col in tick_indicators.items():
    thsTickConvertor.add_convertors(target_col, partial(get_thscol, col=ths_col))


thsTickConvertor.add_convertors("symbol", lambda x: x["thscode"])

thsTickConvertor.add_convertors(
    "status", lambda x: ths_status_map[get_thscol(x, "tradeStatus")]
)
thsTickConvertor.add_convertors("created_dt", lambda x: to_timestamp(x["time"][0]))
thsTickConvertor.add_convertors("updated_dt", lambda x: to_timestamp(x["time"][0]))


class thsAPIException(Exception):
    def __init__(self, error_code, error_message):
        super().__init__(f"{error_code:6d} -- {error_message}")


def to_thscode(symbol) -> str:
    if vxMarketPreset(symbol).security_type == SecType.ETFLOF:
        exchange, code = "OF", symbol[-6:]
    else:
        exchange, code = symbol.split(".")
    return f"{code}.{exchange[:2]}"


stock_bars_indicators = {
    "preClose": "yclose",
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
    "changeRatio": "pct_change",
    "volume": "volume",
    "amount": "amount",
    "turnoverRatio": "turnoverratio",
    "transactionAmount": "transactioncount",
    "totalCapital": "total_capital",
    "floatCapitalOfAShares": "float_capital",
    "pe_ttm": "pe_ttm",
    "pb": "pb",
    "ths_af_stock": "factor",
}
thsStockBarsConvertor = vxDataConvertor(vxTick)

for ths_col, target_col in stock_bars_indicators.items():
    thsStockBarsConvertor.add_convertors(target_col, partial(get_thscol, col=ths_col))

index_bars_indicators = {
    "preClose": "yclose",
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
    "changeRatio": "pct_change",
    "volume": "volume",
    "amount": "amount",
    "turnoverRatio": "turnoverratio",
    # "transactionAmount": "transactioncount",
    "floatCapital": "float_capital",
    "pe_ttm_index": "pe_ttm",
    "pb_mrq": "pb",
}

thsIndexBarsConvertor = vxDataConvertor(vxTick)

for ths_col, target_col in index_bars_indicators.items():
    thsIndexBarsConvertor.add_convertors(target_col, partial(get_thscol, col=ths_col))


class thsHQAPI:
    __api_version__ = "v1"
    __serverpath__ = "https://quantapi.51ifind.com/api"

    def __init__(self, reflash_token: str) -> None:
        self._reflash_token = reflash_token
        self._access_token = ""
        self._expired_at = 0
        self._executor = Executor()

    @property
    def access_token(self):
        if not self._access_token:
            self._access_token, self._expired_at = self._get_access_token(
                created_new=False
            )

        if self._expired_at + 30 < vxtime.now():
            self._access_token, self._expired_at = self._get_access_token(
                created_new=True
            )

        return self._access_token

    def request(
        self,
        method,
        params=None,
        headers=None,
    ):
        if headers is None:
            headers = {
                "Content-Type": "application/json",
                "access_token": self.access_token,
            }
        if params is None:
            params = {}

        url = self._get_api(method)
        resp = requests.post(url, headers=headers, json=params)
        resp.raise_for_status()
        reply = resp.json()
        return self._check_reply(reply)

    def _get_access_token(self, created_new=False) -> Tuple[str, float]:
        headers = {
            "Content-Type": "application/json",
            "refresh_token": self._reflash_token,
        }
        method = "update_access_token" if created_new else "get_access_token"
        data = self.request(method, headers=headers)
        return data["access_token"], to_timestamp(data["expired_time"])

    def _get_api(self, method) -> str:
        return f"{self.__serverpath__}/{self.__api_version__}/{method}"

    def _check_reply(self, reply):
        if reply["errorcode"] != 0:
            raise thsAPIException(reply["errorcode"], reply["errmsg"])

        return reply["data"] if "data" in reply else reply["tables"]

    def hq(self, *symbols) -> Dict[str, Any]:
        """实时行情数据"""
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        params = {
            "codes": ",".join([to_thscode(symbol) for symbol in symbols]),
            "indicators": ",".join(tick_indicators.keys()),
        }
        data = self.request("real_time_quotation", params=params)
        return pl.DataFrame(
            list(map(lambda line: thsTickConvertor(line).message, data))
        )

    def index_bars(self, symbols, freq: str = "1d", start_date=None, end_date=None):
        start_date = (
            to_timestring(start_date, "%Y-%m-%d") if start_date else "1990-01-01"
        )

        end_date = to_timestring(end_date or vxtime.today(), "%Y-%m-%d")

        _cnt, _freq = normalize_freq(freq)
        if _freq not in ("day", "minite") or _cnt > 1:
            raise ValueError(f"{freq} is not supported.")
        start = int(start_date[:4])
        end = int(end_date[:4]) + 1

        data = [
            self._cmd_history_quotation(symbol, year)
            for symbol, year in product(symbols, range(start, end))
        ]

        return (
            pl.concat(data)
            .filter(
                pl.col("date").is_between(start_date, end_date, include_bounds=True)
            )
            .select(["date", "symbol"] + list(index_bars_indicators.values()))
        )

    def _cmd_history_quotation(self, symbol: str, year: int):
        params = {
            "codes": to_thscode(symbol),
            "indicators": ",".join(index_bars_indicators.keys()),
            "startdate": f"{year}-01-01",
            "enddate": f"{year}-12-31",
            "functionpara": {
                "Interval": "D",
                "CPS": "2",
            },
        }
        data = self.request("cmd_history_quotation", params=params)[0]

        return (
            pl.DataFrame(data["table"])
            .with_columns(
                [
                    pl.lit(pl.Series("date", data["time"])).alias("date"),
                    pl.lit(to_symbol(data["thscode"])).alias("symbol"),
                    pl.col(list(index_bars_indicators.keys())).cast(pl.Float64),
                ]
            )
            .rename(index_bars_indicators)
            .select(["date", "symbol"] + list(index_bars_indicators.values()))
        )


if __name__ == "__main__":
    api = thsHQAPI(REFLASH_TOKEN)
    print(api.access_token)
    params = {"codes": "300033.SZ,000001.SZ", "indicators": ""}

    cash_symbols = list(
        {
            "SZSE.159980",
            "SZSE.159981",
            "SHSE.518880",
            "SZSE.161226",
            "SZSE.159985",
            "SHSE.513500",
            "SHSE.513100",
            "SZSE.164824",
            "SHSE.513080",
            "SHSE.513030",
            "SHSE.513520",
            "SHSE.601398",
            "SHSE.601288",
            "SHSE.601328",
            "SHSE.601939",
            "SHSE.601988",
            "SHSE.601658",
            "SHSE.600941",
            "SHSE.601728",
            "SHSE.600050",
        }
    )
    with vxtime.timeit():
        bars = api.index_bars(
            ["SHSE.000905", "SHSE.000852"],
            start_date="2018-02-01",
            end_date="2019-12-31",
        )
        # bars = api.hq(cash_symbols)
        print(bars)
