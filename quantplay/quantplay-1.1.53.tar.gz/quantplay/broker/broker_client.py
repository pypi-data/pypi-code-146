from quantplay.service import market
from uuid import uuid4
from quantplay.broker.generics.broker import Broker

class BrokerClient(Broker):
    def __init__(self):
        self.market_data = {}
        self.current_tick = None
        self.client_orders = {}
        self.client_positions = {}

    def get_holding(self):
        return {}

    def positions(self):
        return self.client_positions

    def orders(self, tag=None):
        orders = list(self.client_orders.values())

        if tag:
            orders = [a for a in orders if a['tag'] == tag]

        return orders

    def ping(self, timestamp):
        self.current_tick = timestamp

        overall_pnl = 0
        for tradingsymbol in self.client_positions:
            ltp = self.ltp(tradingsymbol)
            high = self.tick_high(tradingsymbol)

            position_data = self.client_positions[tradingsymbol]
            quantity = position_data['quantity']
            avg_price = position_data['avg_price']

            self.client_positions[tradingsymbol]['ltp'] = ltp
            self.client_positions[tradingsymbol]['pnl'] = quantity*(ltp*100-avg_price*100)
            overall_pnl += self.client_positions[tradingsymbol]['pnl']

        print("overall pnl at {} is {}".format(timestamp, overall_pnl))

    def load_data(self, symbol):
        if symbol in self.market_data:
            return
        data = market.data(interval="minute", symbols_by_security_type={"OPT": [symbol]})
        self.market_data[symbol] = data.set_index(["symbol", "date"])

    def ltp(self, tradingsymbol):
        return self.market_data[tradingsymbol].loc[(tradingsymbol, self.current_tick)]['close']

    def tick_high(self, tradingsymbol):
        return self.market_data[tradingsymbol].loc[(tradingsymbol, self.current_tick)]['high']

    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        ltp = self.ltp(tradingsymbol)

        if order_type == 'MARKET':
            if tradingsymbol in self.client_positions:
                raise Exception("Adding position on symbol {} is not allowed".format(tradingsymbol))

            if transaction_type == 'SELL':
                quantity = - quantity

            self.client_positions[tradingsymbol] = {
                'quantity' : quantity,
                'avg_price' : ltp,
                'exchange' : exchange,
                'product' : product
            }
        elif order_type == "SL":
            if transaction_type == "BUY":
                assert trigger_price is not None
                self.client_orders[str(uuid4())] = {
                    'symbol' : tradingsymbol,
                    'quantity' : quantity,
                    'type' : transaction_type,
                    'trigger_price' : trigger_price,
                    'price' : price,
                    'tag' : tag,
                    'side' : transaction_type
                }
            else:
                raise Exception("{} not supported for SL orders")
        else:
            raise Exception("order type {} not supported".format(order_type))

    def execute_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                      stoploss=None, tag=None, product=None):
        self.load_data(tradingsymbol)
        ltp = self.ltp(tradingsymbol)
        super().execute_order(tradingsymbol=tradingsymbol, exchange=exchange, quantity=quantity, order_type=order_type,
                              transaction_type=transaction_type, stoploss=stoploss, tag=tag, product=product,
                              price=ltp)


