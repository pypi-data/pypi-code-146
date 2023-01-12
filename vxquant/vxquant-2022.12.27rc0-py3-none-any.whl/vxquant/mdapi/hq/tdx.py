"""tdx行情"""

import time
import json
from enum import Enum
from itertools import chain
from functools import reduce
from contextlib import suppress, contextmanager
from pathlib import Path
from pytdx.hq import TdxHq_API, TDXParams
from pytdx.config.hosts import hq_hosts
from vxutils import logger, vxtime
from concurrent.futures import ThreadPoolExecutor, as_completed
from vxquant.model.preset import vxMarketPreset
from vxquant.model.contants import SecType
from vxquant.model.tools.tdxData import (
    tdxETFLOFTickConvter,
    tdxStockTickConvter,
    tdxConBondTickConvter,
)

from queue import PriorityQueue, Queue, Empty


class TDXExchange(Enum):
    SHSE = TDXParams.MARKET_SH
    SZSE = TDXParams.MARKET_SZ


def to_tdx_symbol(symbol):
    """转成tdx的symbol格式: (market,code)

    Arguments:
        symbol {_type_} -- symbol
    """
    market, code = symbol.split(".")
    return (TDXExchange[market].value, code)


def parser_tdx_symbol(market, code):
    """将tdx的symbol格式转化成symbol："SHSE.0000001"

    Arguments:
        market {_type_} -- tdx 的market代码
        code {_type_} -- 证券代码
    """
    return f"{TDXExchange(market).name}.{code}"


def parser_tdx_tick(tdxtick, key=""):
    """转化为vxtick格式

    Arguments:
        tdxtick {_type_} -- tdx tick格式
    """
    try:
        symbol = parser_tdx_symbol(tdxtick["market"], tdxtick["code"])
        _preset = vxMarketPreset(symbol)

        if _preset.security_type in (
            SecType.BOND_CONVERTIBLE,
            SecType.BOND,
            SecType.REPO,
        ):
            return tdxConBondTickConvter(tdxtick, key="symbol")
        elif _preset.security_type in (SecType.ETFLOF, SecType.CASH):
            return tdxETFLOFTickConvter(tdxtick, key="symbol")
        else:
            return tdxStockTickConvter(tdxtick, key="symbol")
    except Exception as e:
        logger.error(e)


class TdxAPIPool:
    def __init__(
        self, pool_size: int = 5, host_file: str = "etc/tdxhosts.json"
    ) -> None:
        self._host_file = host_file
        self.__hosts__ = PriorityQueue()
        self._apis = PriorityQueue()
        self._last_reflash_dt = 0
        self._executor = ThreadPoolExecutor()

        if self.__hosts__.qsize() <= 10 and Path(self._host_file).exists():
            self.load_hosts()

        self.reflash_hosts()
        while self._apis.qsize() < pool_size:
            api = self.do_connect()
            self._apis.put((vxtime.now(), api))

    def do_connect(self) -> TdxHq_API:
        while not self.__hosts__.empty():
            _, host, port = self.__hosts__.get_nowait()
            api = TdxHq_API()
            if api.connect(host, port, time_out=1):
                return api

    def do_heartbeat(self):
        while True:
            self.reflash_hosts()

            while not self._apis.empty() and self._apis.queue[0][0] + 60 > vxtime.now():
                api = self._apis.get_nowait()
                if not api.do_heartbeat():
                    api = self.get_api()
                self._apis.put((vxtime.now(), api))
            vxtime.sleep(1)

    def _run_api_method(
        self,
        method: str,
        *args,
    ):
        with self() as api:
            return getattr(api, method)(*args)

    def reflash_hosts(self) -> None:
        if (
            self.__hosts__.qsize() > 10
            and self._last_reflash_dt + 24 * 60 * 60 > vxtime.now()
        ):
            return

        logger.info("开始更新hosts连通性测试...")
        tdxapi = TdxHq_API()
        cnt = 0
        for server_name, host, port in hq_hosts:
            start = time.perf_counter()
            if tdxapi.connect(host, port, time_out=0.5):
                cnt += 1
                cost = (time.perf_counter() - start) * 1000
                self.__hosts__.put_nowait((cost, host, port))
                logger.debug(
                    f"测试链接: {server_name}({host}:{port} 成功{cnt}个: {cost:.4f}ms"
                )
                tdxapi.disconnect()

            else:
                logger.debug(f"测试链接: {server_name}({host}:{port} 超时")

        try:
            with open(self._host_file, "w", encoding="utf-8") as fp:
                data = {"reflash_dt": vxtime.now(), "hosts": self.__hosts__.queue}
                self._last_reflash_dt = data["reflash_dt"]
                json.dump(data, fp, indent=4)
            logger.info(f"更新{len(data['hosts'])}个hosts")
        except OSError as err:
            logger.warning(f"{self._host_file}不存在，没有保存hosts信息: {err}")

    def load_hosts(self, host_file: str = "etc/tdxhosts.json"):
        with open(host_file, "r") as fp:
            tdxhosts = json.load(fp)

        if tdxhosts["reflash_dt"] + 60 * 60 * 24 <= vxtime.now():
            logger.warning(f"{host_file}文件内容已超过1天，需要重新更新.")
            return

        [self.__hosts__.put(host_config) for host_config in tdxhosts["hosts"]]
        self._last_reflash_dt = tdxhosts["reflash_dt"]

    @contextmanager
    def __call__(self):
        try:
            _, api = self._apis.get()
            yield api
            self._apis.put((vxtime.now(), api))
        except Exception as e:
            logger.error(f"调用发生错误: {e}")
            while self.__hosts__.qsize() > 10:
                _, host, port = self.__hosts__.get_nowait()
                api = TdxHq_API()
                if api.connect(host, port):
                    self._apis.put((vxtime.now(), api))
                    break

    def require_api(self) -> TdxHq_API:
        pass

    def __getattr__(self, __name: str):
        def methods(*args, **kwargs):
            r = self._executor.submit(self._run_api_method, __name, *args)
            return r.result()

        return methods

    def get_security_quotes(self, tdxsymbols):
        rets = []
        tdxticks = []
        for i in range(0, len(tdxsymbols), 50):
            r = self._executor.submit(
                self._run_api_method, "get_security_quotes", tdxsymbols[i : i + 50]
            )
            r.add_done_callback(lambda x: tdxticks.extend(x.result()))
            rets.append(r)
        list(as_completed(rets))
        return tdxticks


class vxHqAPI:
    def __init__(self, host_file="etc/tdxhosts.json"):
        self._apipool = TdxAPIPool(host_file=host_file)
        self._cache = {}
        self._last_cache_dt = 0

    def __getitem__(self, symbol):
        if symbol in self._cache and (self._last_cache_dt + 3 <= vxtime.now()):
            return self._cache[symbol]

        cached_symbols = set(self._cache.keys())
        cached_symbols.add(symbol)
        self.__call__(*cached_symbols)
        return self._cache[symbol]

    def __call__(self, *symbols):
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        if self._last_cache_dt + 3 > vxtime.now():
            tdx_symbols = list(
                map(to_tdx_symbol, set(symbols).union(set(self._cache.keys())))
            )
            self._last_cache_dt = vxtime.now()
        else:
            tdx_symbols = list(
                map(to_tdx_symbol, set(symbols).difference(set(self._cache.keys())))
            )
        if tdx_symbols:
            tdxticks = self._apipool.get_security_quotes(tdx_symbols)
            self._cache.update(map(parser_tdx_tick, tdxticks))

        return {symbol: self._cache[symbol] for symbol in symbols}


if __name__ == "__main__":
    import polars as pl

    hq_api = vxHqAPI()
    # data = api_pool.get_security_quotes([(0, "000001"), (1, "600000")])
    # print(data)
    # for d in data:
    #    d["reversed_bytes4"] = d["reversed_bytes4"][0]

    # df = pl.DataFrame(data)
    # print(df)

    # print(data)
    data = hq_api(
        "SHSE.600000",
        "SZSE.000001",
        "SHSE.000001",
        "SHSE.000688",
        "SHSE.511880",
        "SHSE.510300",
        "SHSE.511990",
        "SHSE.511660",
        "SHSE.204001",
        "SZSE.399001",
        "SZSE.399673",
        "SZSE.159001",
        "SZSE.159919",
        "SZSE.159915",
        "SZSE.159937",
        "SZSE.131810",
    )

    with vxtime.timeit("Hit Cache", show_title=True):
        print(hq_api["SHSE.000001"])

    with vxtime.timeit("Not Hit CACHE", show_title=True):
        print(hq_api["SZSE.159916"])
