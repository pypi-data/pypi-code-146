"""QMT下单接口封装"""
from typing import Dict
from vxquant.model.exchange import vxTick
from vxquant.tdapi.base import vxTdAPIBase


class vxQMTTdAPI(vxTdAPIBase):
    def __init__(self, qmtcontext):
        self._qmtcontext = qmtcontext

    def get_ticks(self, *symbols) -> Dict[str, vxTick]:
        """"""
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        qmt_symbols = [f"{symbol[-6:]}.{symbol[:2]}" for symbol in symbols]
        qmttick = self._qmtcontext.get_full_tick(qmt_symbols)
