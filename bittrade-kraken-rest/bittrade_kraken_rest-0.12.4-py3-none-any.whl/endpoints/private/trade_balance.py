from bittrade_kraken_rest.connection import send_private
from bittrade_kraken_rest.models.private.trade_balance import GetTradeBalanceResult


def get_trade_balance():
    """
    Get trade balances
    :return:
    """
    return send_private(
        url="/0/private/TradeBalance", result_class=GetTradeBalanceResult
    )
