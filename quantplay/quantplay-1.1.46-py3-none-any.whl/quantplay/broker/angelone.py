import json
import time

import pandas as pd
import pyotp
import websocket
from retrying import retry
from smartapi import SmartConnect

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import InvalidArgumentException
from quantplay.utils.constant import Constants
from quantplay.utils.exchange import Market as MarketConstants
import requests
import _thread as thread
import numpy as np


class AngelOne(Broker):

    def __init__(self, order_updates=None, api_key=None, username=None, password=None, totp_key=None):
        self.order_updates = order_updates

        assert api_key != None
        assert username != None
        assert password != None
        assert totp_key != None

        self.api_key = api_key
        self.username = username
        self.totp_key = totp_key

        self.wrapper = SmartConnect(api_key=self.api_key)
        data = self.wrapper.generateSession(username, password, pyotp.TOTP(totp_key).now())

        self.refresh_token = data['data']['refreshToken']
        res = self.wrapper.getProfile(self.refresh_token)
        print(res)

        jwt_token = data['data']['jwtToken'].split(" ")[1]
        self.jwt_token = jwt_token
        self.populate_instrument_data()

    def on_message(self, ws, order):
        try:
            order = json.loads(order)

            order['placed_by'] = self.username
            order['tag'] = self.username
            order['order_id'] = order['orderid']
            order['exchange_order_id'] = order['order_id']
            order['transaction_type'] = order['transactiontype']
            order['quantity'] = int(order['quantity'])
            order['order_type'] = order['ordertype']

            if order['exchange'] == "NFO":
                order["tradingsymbol"] = self.symbol_map[order["tradingsymbol"]]

            if order['order_type'] == "STOPLOSS_LIMIT":
                order['order_type'] = "SL"

            if 'triggerprice' in order and order['triggerprice'] != 0:
                order['trigger_price'] = float(order['triggerprice'])
            else:
                order['trigger_price'] = None

            if order["status"] == "trigger pending":
                order["status"] = "TRIGGER PENDING"
            elif order["status"] == "cancelled":
                order["status"] = "CANCELLED"
            elif order["status"] == "open":
                order["status"] = "OPEN"
            elif order["status"] == "complete":
                order["status"] = "COMPLETE"

            self.order_updates.put(order)
        except Exception as e:
            Constants.logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))
        print(json.dumps(order))

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        def run(*args):
            for i in range(300000):
                time.sleep(1)
                ws.send(json.dumps({
                    "actiontype": "subscribe",
                    "feedtype": "order_feed",
                    "jwttoken": self.jwt_token,
                    "clientcode": self.username,
                    "apikey": self.api_key
                }))
            time.sleep(1)
            ws.close()
            print("thread terminating...")

        thread.start_new_thread(run, ())

    def populate_instrument_data(self):
        symbol_data = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        data = requests.get(symbol_data)
        inst_data = json.loads(data.content)
        self.inst_data = pd.DataFrame(inst_data)
        self.inst_data = self.inst_data[(self.inst_data.exch_seg.isin(["NFO", "MCX", "CDS"])) | (
                (self.inst_data.exch_seg == "NSE") & (self.inst_data.symbol.str.contains("-EQ")))]

        self.initialize_expiry_fields()
        self.add_quantplay_fut_tradingsymbol()
        self.add_quantplay_opt_tradingsymbol()

        self.symbol_map = dict(zip(self.inst_data.symbol, self.inst_data.tradingsymbol))

    def initialize_expiry_fields(self):
        self.inst_data.loc[:, 'tradingsymbol'] = self.inst_data.name
        self.inst_data.loc[:, 'expiry'] = pd.to_datetime(self.inst_data.expiry)
        self.inst_data.loc[:, "expiry_year"] = self.inst_data["expiry"].dt.strftime("%y").astype(str)
        self.inst_data.loc[:, "month"] = self.inst_data["expiry"].dt.strftime("%b").str.upper()

        self.inst_data.loc[:, "month_number"] = self.inst_data["expiry"].dt.strftime("%m").astype(float).astype(str)
        self.inst_data.loc[:, 'month_number'] = np.where(self.inst_data.month_number == 'nan',
                                                         np.nan,
                                                         self.inst_data.month_number.str.split(".").str[0]
                                                         )

        self.inst_data.loc[:, "week_option_prefix"] = np.where(
            self.inst_data.month_number.astype(float) >= 10,
            self.inst_data.month.str[0] + self.inst_data["expiry"].dt.strftime("%d").astype(str),
            self.inst_data.month_number + self.inst_data["expiry"].dt.strftime("%d").astype(str),
        )

        self.inst_data.loc[:, "next_expiry"] = self.inst_data.expiry + pd.DateOffset(days=7)

    def add_quantplay_fut_tradingsymbol(self):
        seg_condition = [
            ((self.inst_data["instrumenttype"].str.contains("FUT")) & (
                    self.inst_data.instrumenttype != "OPTFUT"))
        ]

        tradingsymbol = [
            self.inst_data.tradingsymbol + self.inst_data.expiry_year + self.inst_data.month + "FUT"
        ]

        self.inst_data.loc[:, "tradingsymbol"] = np.select(
            seg_condition, tradingsymbol, default=self.inst_data.tradingsymbol
        )

    def add_quantplay_opt_tradingsymbol(self):
        seg_condition = (self.inst_data["strike"].astype(float) > 0)

        weekly_option_condition = (
                (self.inst_data.expiry.dt.month == self.inst_data.next_expiry.dt.month) & (
            self.inst_data.exch_seg.isin(["NFO", "CDS"])))

        month_option_condition = (self.inst_data.expiry.dt.month != self.inst_data.next_expiry.dt.month)

        self.inst_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.inst_data.tradingsymbol + self.inst_data.expiry_year,
            self.inst_data.tradingsymbol
        )

        self.inst_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & weekly_option_condition,
            self.inst_data.tradingsymbol + self.inst_data.week_option_prefix,
            self.inst_data.tradingsymbol
        )

        self.inst_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & month_option_condition,
            self.inst_data.tradingsymbol + self.inst_data.month,
            self.inst_data.tradingsymbol
        )

        self.inst_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.inst_data.tradingsymbol + self.inst_data.strike.astype(float).astype(str).str.split(".").str[0],
            self.inst_data.tradingsymbol
        )

        self.inst_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.inst_data.tradingsymbol + self.inst_data.symbol.str[-2:],
            self.inst_data.tradingsymbol
        )

    def stream_order_data(self):
        root_url = "smartapisocket.angelbroking.com/websocket"
        ws_url = "wss://{}?jwttoken={}&clientcode={}&apikey={}".format(
            root_url,
            self.jwt_token,
            self.username, self.api_key)

        websocket.enableTrace(False)
        print(ws_url)
        ws = websocket.WebSocketApp(ws_url,
                                    on_message=self.on_message,
                                    on_error=self.on_error)
        ws.on_open = self.on_open
        ws.run_forever()

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_ltp(self, exchange=None, tradingsymbol=None):
        if tradingsymbol in MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP:
            tradingsymbol = MarketConstants.INDEX_SYMBOL_TO_DERIVATIVE_SYMBOL_MAP[tradingsymbol]

        symboltoken = self.get_symbol_token(exchange, tradingsymbol)

        if exchange == "NSE" and tradingsymbol not in ["NIFTY", "BANKNIFTY"]:
            tradingsymbol = "{}-EQ".format(tradingsymbol)

        response = self.wrapper.ltpData(exchange, tradingsymbol, symboltoken)
        if 'status' in response and response['status'] == False:
            raise InvalidArgumentException("Failed to fetch ltp broker error {}".format(response))

        return response['data']['ltp']

    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        order = {}
        order["transactiontype"] = transaction_type

        order["variety"] = "NORMAL"
        order["tradingsymbol"] = tradingsymbol
        if order_type == "SL":
            order["variety"] = "STOPLOSS"

        if exchange == "NSE":
            order["tradingsymbol"] = "{}-EQ".format(tradingsymbol)

        order["triggerprice"] = trigger_price
        order["exchange"] = exchange
        order['symboltoken'] = self.get_symbol_token(exchange, tradingsymbol)

        if order_type == "SL":
            order_type = "STOPLOSS_LIMIT"
        order['ordertype'] = order_type

        if product == "MIS":
            product = "INTRADAY"
        elif product == "NRML":
            product = "CARRYFORWARD"
        order['producttype'] = product

        order['price'] = price
        order['quantity'] = quantity
        order["duration"] = "DAY"

        try:
            print("Placing order {}".format(json.dumps(order)))
            return self.wrapper.placeOrder(order)
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def get_orders(self):
        order_book = self.wrapper.orderBook()
        if order_book['data']:
            return order_book['data']
        else:
            if 'errorcode' in order_book and order_book['errorcode'] == "AB1010":
                Constants.logger.error(
                    "Can't Fetch order book because session got expired")
            else:
                Constants.logger.error(
                    "Unknow error while fetching order book [{}]".format(order_book))

    def modify_orders_till_complete(self, orders_placed):
        modification_count = {}
        while 1:
            time.sleep(10)
            orders = pd.DataFrame(self.get_orders())

            orders = orders[orders.orderid.isin(orders_placed)]
            orders = orders[~orders.orderstatus.isin(["rejected", "cancelled", "complete"])]

            if len(orders) == 0:
                Constants.logger.info("ALL orders have be completed")
                break

            orders = orders.to_dict('records')
            for order in orders:
                order_id = order['orderid']

                ltp = self.get_ltp_by_order(order)
                order['price'] = ltp
                self.modify_order(order)

                if order_id not in modification_count:
                    modification_count[order_id] = 1
                else:
                    modification_count[order_id] += 1

                time.sleep(.1)

                if modification_count[order_id] > 5:
                    order['ordertype'] = "MARKET"
                    order['price'] = 0
                    Constants.logger.info("Placing MARKET order [{}]".format(order))
                    self.modify_order(order)
