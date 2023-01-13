from quantplay.utils.constant import Constants
from collections import defaultdict
from quantplay.utils.exchange import Market as MarketConstants
from datetime import timedelta
from quantplay.exception.exceptions import QuantplayOrderPlacementException
import copy
from datetime import datetime
from threading import Lock
import time

logger = Constants.logger

class Broker():

    def __init__(self):
        self.instrument_id_to_symbol_map = dict()
        self.instrument_id_to_exchange_map = dict()
        self.instrument_id_to_security_type_map = dict()
        self.exchange_symbol_to_instrument_id_map = defaultdict(dict)
        self.order_type_sl = "SL"
        self.nfo_exchange = "NFO"
        self.lock = Lock()

    def round_to_tick(self, number):
        return round(number * 20) / 20

    def populate_instruments(self, instruments):
        """Fetches instruments for all exchanges from the broker
        and stores them in the member attributes.
        """
        Constants.logger.info("populating instruments")
        for instrument in instruments:
            exchange, symbol, instrument_id = (
                instrument.exchange,
                instrument.symbol,
                instrument.instrument_id,
            )
            self.instrument_id_to_symbol_map[instrument_id] = symbol
            self.instrument_id_to_exchange_map[instrument_id] = exchange
            self.instrument_id_to_security_type_map[
                instrument_id
            ] = instrument.security_type()
            self.exchange_symbol_to_instrument_id_map[exchange][symbol] = instrument_id

    def execute_order_v2(self, order):
        start_time = datetime.now()
        tradingsymbol = order['tradingsymbol']
        exchange = order['exchange']
        trigger_price = order['trigger_price']
        transaction_type = order['transaction_type']
        if order['validity'] is not None and order['trigger_price'] is not None:
            while True:
                self.lock.acquire()
                try:
                    ltp = self.get_ltp(exchange, tradingsymbol)
                except Exception as e:
                    Constants.logger.error("[GET_LTP_FAILED] with exception {}".format(e))
                time.sleep(.5)
                self.lock.release()
                if (transaction_type == "SELL" and trigger_price > ltp) or (
                        transaction_type == "BUY" and trigger_price < ltp):
                    logger.info("[EXECUTING_ORDER] ltp {} crossed trigger price {} for {}".format(ltp, trigger_price, order))
                    self.execute_order(tradingsymbol=order['tradingsymbol'],
                                       exchange=order['exchange'],
                                       quantity=order['quantity'],
                                       product=order['product'],
                                       tag=order['tag'],
                                       stoploss=order['stoploss'],
                                       transaction_type=order['transaction_type'],
                                       order_type=order['order_type'])
                    return
                current_time = datetime.now()
                if (current_time - start_time).seconds > order['validity']:
                    Constants.logger.info("[ORDER_VALIDITY_EXPIRED] order [{}]".format(order))
                    return

    def execute_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                      stoploss=None, tag=None, product=None, price=None):
        if price is None:
            price = self.get_ltp(exchange=exchange, tradingsymbol=tradingsymbol)
            trade_price = copy.deepcopy(price)
        try:
            if stoploss != None:
                if transaction_type == "SELL":
                    sl_transaction_type = "BUY"
                    sl_trigger_price = self.round_to_tick(price * (1 + stoploss))

                    if exchange == self.nfo_exchange:
                        price = sl_trigger_price * 1.05
                    elif exchange == "NSE":
                        price = sl_trigger_price * 1.01
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                elif transaction_type == "BUY":
                    sl_transaction_type = "SELL"
                    sl_trigger_price = self.round_to_tick(price * (1 - stoploss))

                    if exchange == self.nfo_exchange:
                        price = sl_trigger_price * .95
                    elif exchange == "NSE":
                        price = sl_trigger_price * .99
                    else:
                        raise Exception("{} not supported for trading".format(exchange))

                    sl_price = self.round_to_tick(price)
                else:
                    raise Exception("Invalid transaction_type {}".format(transaction_type))
                stoploss_order_id = self.place_order(tradingsymbol=tradingsymbol,
                                                     exchange=exchange,
                                                     quantity=quantity,
                                                     order_type=self.order_type_sl,
                                                     transaction_type=sl_transaction_type,
                                                     tag=tag, product=product, price=sl_price,
                                                     trigger_price=sl_trigger_price)

                if stoploss_order_id is None:
                    Constants.logger.error(
                        "[ORDER_REJECTED] tradingsymbol {}".format(tradingsymbol))
                    raise QuantplayOrderPlacementException("Order reject for {}".format(tradingsymbol))

            if order_type == "MARKET":
                trade_price = 0

            response = self.place_order(tradingsymbol=tradingsymbol, exchange=exchange, quantity=quantity,
                                        order_type=order_type, transaction_type=transaction_type, tag=tag,
                                        product=product, price=trade_price)
            return response
        except Exception as e:
            raise e

    """
            Input  : quantplay symbol
            Output : broker symbol
        """

    def get_symbol(self, symbol):
        return symbol

    """
        Input  : quantplay exchange
        Output : broker exchange
    """

    def get_exchange(self, exchange):
        return exchange

    def place_order_quantity(self, quantity, tradingsymbol, exchange):
        lot_size = self.get_lot_size(exchange, tradingsymbol)
        quantity_in_lots = int(quantity/lot_size)

        return quantity_in_lots*lot_size

    def get_product(self, product):
        return product

    def get_lot_size(self, exchange, tradingsymbol):
        try:
            return int(self.symbol_data["{}:{}".format(exchange, tradingsymbol)]['lot_size'])
        except Exception as e:
            logger.error("[GET_LOT_SIZE] unable to get lot size for {} {}".format(exchange, tradingsymbol))
            raise e

    def option_symbol(self, underlying_symbol, expiry_date, strike_price, type):
        option_symbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[underlying_symbol]
        option_symbol += expiry_date.strftime('%y')

        month_number = str(int(expiry_date.strftime("%m")))
        monthly_option_prefix = expiry_date.strftime("%b").upper()

        if int(month_number) >= 10:
            week_option_prefix = monthly_option_prefix[0]
        else:
            week_option_prefix = month_number
        week_option_prefix += expiry_date.strftime("%d")

        next_expiry = expiry_date + timedelta(days=7)

        if next_expiry.month != expiry_date.month:
            option_symbol += monthly_option_prefix
        else:
            option_symbol += week_option_prefix

        option_symbol += str(int(strike_price))
        option_symbol += type

        return option_symbol
