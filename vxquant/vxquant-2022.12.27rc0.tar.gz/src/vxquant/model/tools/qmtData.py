""" QMT数据转换vxFinDataModel数据的转换器 """

from vxutils import combine_datetime, to_timestring, vxtime, vxDataConvertor, to_text

from vxquant.model.exchange import (
    vxCashPosition,
    vxTick,
    vxBar,
    vxPosition,
    vxOrder,
    vxTrade,
    vxAccountInfo,
)
from vxquant.model.preset import vxMarketPreset
from vxquant.model.nomalize import to_symbol

"""
量
openInt:持仓量
stockStatus:股票状态
lastSettlementPrice:最新结算价
open:开盘价
high:最高价
low:最低价
settlementPrice:结算价
lastClose:收盘价
askPrice:列表,卖价五档
bidPrice:列表,买价五档
askVol:列表,卖量五档
bidVol:列表,买量五档

"""

TICK_TRANS = {
    # 最近成交价
    "lasttrade": "lastPrice",
    # 昨日收盘价
    "yclose": "lastClose",
    # 持仓量
    "interest": "openInt",
    # 停牌状态
    "status": "stockStatus",
}

for 

qmtTickConvter = vxDataConvertor(vxTick, TICK_TRANS)
