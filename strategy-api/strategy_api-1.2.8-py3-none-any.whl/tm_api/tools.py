from strategy_api.tm_api.object import Exchange, Product, OrderType


def symbol_deal(symbol: str, exchange: Exchange) -> str:
    if "-" not in symbol:
        print("错误的标的，主币 与 订价币之间用 - ")
        return symbol

    l = symbol.split('-')
    if exchange == Exchange.BINANCE:
        if "PERP" in l:
            return l[0] + l[1] + "_PERP"
        else:
            return l[0] + l[1]
    elif exchange == Exchange.OKEX:
        if "PERP" in l:
            return symbol.replace("PERP", "SWAP")
        else:
            return symbol + "-SWAP"
    else:
        print("未知交易所")
        return ""


def get_order_type(maker: bool = False, stop_loss: bool = False, stop_profit: bool = False) -> OrderType:
    if maker:
        # 发送限价单
        order_type = OrderType.LIMIT
    else:
        if stop_profit:
            # 发送市价止盈
            order_type = OrderType.TAKE_PROFIT_MARKET
        elif stop_loss:
            # 发送市价止损
            order_type = OrderType.STOP_MARKET
        else:
            # 发送普通市价单
            order_type = OrderType.MARKET
    return order_type
