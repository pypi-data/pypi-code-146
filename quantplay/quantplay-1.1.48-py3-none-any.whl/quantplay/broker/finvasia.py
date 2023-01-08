from quantplay.broker.finvasia_utils.shoonya import ShoonyaApiPy
from quantplay.utils.constant import Constants, OrderType
import pyotp
import io
import os
import zipfile

import pandas as pd
import numpy as np
import requests
from retrying import retry
import time

logger = Constants.logger

class FinvAsia:

    def __init__(self,
                 order_updates=None,
                 api_secret=None,
                 imei=None,
                 password=None,
                 totp_key=None,
                 user_id=None,
                 vendor_code=None):
        self.order_updates = order_updates

        self.api = ShoonyaApiPy()
        totp = pyotp.TOTP(totp_key).now()
        response = self.api.login(userid=user_id,
                             password=password,
                             twoFA=totp,
                             vendor_code=vendor_code,
                             api_secret=api_secret,
                             imei=imei)
        print("finvasia login successful email {} account_id {}".format(response['email'], response['actid']))
        self.load_instrument()
        self.initialize_symbol_data()
        pass

    def initialize_symbol_data(self):
        instruments = self.instrument_data
        instruments = instruments.to_dict('records')
        self.symbol_data = {}
        for instrument in instruments:
            exchange = instrument['Exchange']
            tradingsymbol = instrument['TradingSymbol']
            self.symbol_data["{}:{}".format(exchange, tradingsymbol)] = instrument
            
    def initialize_expiry_fields(self):
        self.instrument_data.loc[:, 'tradingsymbol'] = self.instrument_data.Symbol
        self.instrument_data.loc[:, 'expiry'] = pd.to_datetime(self.instrument_data.Expiry)

        self.instrument_data.loc[:, "expiry_year"] = self.instrument_data["expiry"].dt.strftime("%y").astype(str)
        self.instrument_data.loc[:, "month"] = self.instrument_data["expiry"].dt.strftime("%b").str.upper()

        self.instrument_data.loc[:, "month_number"] = self.instrument_data["expiry"].dt.strftime("%m").astype(
            float).astype(str)
        self.instrument_data.loc[:, 'month_number'] = np.where(self.instrument_data.month_number == 'nan',
                                                                  np.nan,
                                                                  self.instrument_data.month_number.str.split(
                                                                      ".").str[0]
                                                                  )

        self.instrument_data.loc[:, "week_option_prefix"] = np.where(
            self.instrument_data.month_number.astype(float) >= 10,
            self.instrument_data.month.str[0] + self.instrument_data["expiry"].dt.strftime("%d").astype(str),
            self.instrument_data.month_number + self.instrument_data["expiry"].dt.strftime("%d").astype(str),
        )

        self.instrument_data.loc[:, "next_expiry"] = self.instrument_data.expiry + pd.DateOffset(days=7)

    def add_quantplay_fut_tradingsymbol(self):
        seg_condition = [
            ((self.instrument_data["Instrument"].str.contains("FUT")) & (
                        self.instrument_data.Instrument != "OPTFUT"))
        ]

        tradingsymbol = [
            self.instrument_data.tradingsymbol + self.instrument_data.expiry_year + self.instrument_data.month + "FUT"
        ]

        self.instrument_data.loc[:, "tradingsymbol"] = np.select(
            seg_condition, tradingsymbol, default=self.instrument_data.tradingsymbol
        )

    def add_quantplay_opt_tradingsymbol(self):
        seg_condition = (self.instrument_data["StrikePrice"] > 0)
        weekly_option_condition = (
                (self.instrument_data.expiry.dt.month == self.instrument_data.next_expiry.dt.month) & (
                    self.instrument_data.Exchange == "NFO"))
        month_option_condition = (
                (self.instrument_data.expiry.dt.month != self.instrument_data.next_expiry.dt.month) | (
                    self.instrument_data.Exchange == "MCX"))

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.expiry_year,
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & weekly_option_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.week_option_prefix,
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition & month_option_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.month,
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol +
            self.instrument_data.StrikePrice.astype(float).astype(str).str.split(".").str[0],
            self.instrument_data.tradingsymbol
        )

        self.instrument_data.loc[:, "tradingsymbol"] = np.where(
            seg_condition,
            self.instrument_data.tradingsymbol + self.instrument_data.OptionType,
            self.instrument_data.tradingsymbol
        )

    def get_df_from_zip(self, url):
        response = requests.get(url, timeout=10)
        z = zipfile.ZipFile(io.BytesIO(response.content))

        directory = '/tmp/'
        z.extractall(path=directory)
        file_name = url.split(".txt")[0].split("/")[-1]
        os.system('cp /tmp/{}.txt /tmp/{}.csv'.format(file_name, file_name))
        time.sleep(2)
        return pd.read_csv('/tmp/{}.csv'.format(file_name))

    def load_instrument(self):
        instrument_file_EQ = self.get_df_from_zip("https://api.shoonya.com/NSE_symbols.txt.zip")
        instrument_file_FO = self.get_df_from_zip("https://api.shoonya.com/NFO_symbols.txt.zip")
        instrument_file_MCX = self.get_df_from_zip("https://api.shoonya.com/MCX_symbols.txt.zip")

        self.instrument_data = pd.concat([instrument_file_MCX, instrument_file_FO, instrument_file_EQ])

        self.initialize_expiry_fields()
        self.add_quantplay_opt_tradingsymbol()
        self.add_quantplay_fut_tradingsymbol()
        self.fno_symbol_map = dict(zip(self.instrument_data.TradingSymbol, self.instrument_data.tradingsymbol))

    def event_handler_order_update(self, order):
        try:
            order['placed_by'] = order['actid']
            order['tag'] = order['actid']
            order['order_id'] = order['norenordno']
            order['exchange_order_id'] = order['exchordid']
            order['exchange'] = order['exch']

            # TODO translate symbol
            # -EQ should be removed
            # F&O symbol translation
            order['tradingsymbol'] = order['tsym']

            if order['exchange'] == "NSE":
                order['tradingsymbol'] = order['tradingsymbol'].replace("-EQ", "")
            elif order['exchange'] in ["NFO", "MCX"]:
                order["tradingsymbol"] = self.fno_symbol_map[order["tradingsymbol"]]

            order['order_type'] = order['prctyp']
            if order['order_type'] == "LMT":
                order['order_type'] = "LIMIT"
            elif order['order_type'] == "MKT":
                order['order_type'] = "MARKET"
            elif order['order_type'] == "SL-LMT":
                order['order_type'] = "SL"

            if order['trantype'] == "S":
                order['transaction_type'] = "SELL"
            elif order['trantype'] == "B":
                order['transaction_type'] = "BUY"
            else:
                logger.error("[UNKNOW_VALUE] finvasia transaction type {} not supported".format(order['trantype']))

            order['quantity'] = int(order['qty'])

            if 'trgprc' in order:
                order['trigger_price'] = float(order['trgprc'])
            else:
                order['trigger_price'] = None

            order['price'] = float(order['prc'])

            if order["status"] == "TRIGGER_PENDING":
                order["status"] = "TRIGGER PENDING"
            elif order["status"] == "CANCELED":
                order["status"] = "CANCELLED"

            print(f"order feed {order}")
            self.order_updates.put(order)
        except Exception as e:
            logger.error("[ORDER_UPDATE_PROCESSING_FAILED] {}".format(e))

    def place_order(self, tradingsymbol=None, exchange=None, quantity=None, order_type=None, transaction_type=None,
                    tag=None, product=None, price=None, trigger_price=None):
        try:
            if transaction_type == "BUY": buy_or_sell = "B";
            elif transaction_type == "SELL": buy_or_sell = "B";

            if exchange == "NSE": tradingsymbol += "-EQ";

            if product == "NRML": product_type = "M";
            elif product == "CNC": product_type = "C";
            elif product == "MIS": product_type = "I";

            if order_type == OrderType.market: price_type = "MKT";
            elif order_type == OrderType.sl: price_type = "SL-LMT";
            elif order_type == OrderType.slm: price_type = "SL-MKT";
            elif order_type == OrderType.limit: price_type = "LMT";


            response = self.api.place_order(buy_or_sell=buy_or_sell,
                                            product_type=product_type,
                                            exchange=exchange,
                                            tradingsymbol=tradingsymbol,
                                            quantity=quantity,
                                            discloseqty=0,
                                            price_type=price_type,
                                            price=price,
                                            trigger_price=trigger_price,
                                            retention='DAY',
                                            remarks=tag)
            if 'norenordno' in response:
                return response['norenordno']
            else:
                raise Exception(response)
        except Exception as e:
            exception_message = "Order placement failed with error [{}]".format(str(e))
            print(exception_message)

    def get_orders(self):
        return self.api.get_order_book()

    def get_ltp(self, exchange, tradingsymbol):
        token = self.symbol_data["{}:{}".format(exchange, tradingsymbol)]['Token']
        return self.api.get_quotes(exchange, str(token))['lp']

    @retry(wait_exponential_multiplier=3000, wait_exponential_max=10000, stop_max_attempt_number=3)
    def modify_order(self, data):
        try:
            logger.info("Modifying order [{}] new price [{}]".format(data['norenordno'], data['prc']))
            response = self.api.modify_order(orderno=data['norenordno'],
                                             exchange=data['exch'],
                                             tradingsymbol=data['tsym'],
                                             newprice_type=data['prctyp'],
                                             newquantity=data['qty'],
                                             newprice=data['prc'])
            logger.info("[MODIFY_ORDER_RESPONSE] order id [{}] response [{}]".format(data['norenordno'], response))
            return response
        except Exception as e:
            exception_message = "OrderModificationFailed for {} failed with exception {}".format(data['norenordno'], e)
            Constants.logger.error("{}".format(exception_message))

    def modify_orders_till_complete(self, orders_placed, sleep_time=10):
        modification_count = {}
        while 1:
            time.sleep(sleep_time)
            orders = pd.DataFrame(self.get_orders())

            orders = orders[orders.norenordno.isin(orders_placed)]
            orders = orders[~orders.status.isin(["REJECTED", "CANCELED", "COMPLETE"])]

            if len(orders) == 0:
                Constants.logger.info("ALL orders have been completed")
                break

            orders = orders.to_dict('records')
            for order in orders:
                order_id = order['order_id']

                ltp = self.get_ltp(order['exchange'], order['tradingsymbol'])
                order['prc'] = ltp
                self.modify_order(order)

                if order_id not in modification_count:
                    modification_count[order_id] = 1
                else:
                    modification_count[order_id] += 1

                time.sleep(.1)

                if modification_count[order_id] > 5:
                    order['prctyp'] = "MKT"
                    order['prc'] = 0
                    Constants.logger.info("Placing MARKET order [{}]".format(order))
                    self.modify_order(order)

    def stream_order_data(self):
        self.api.start_websocket(order_update_callback=self.event_handler_order_update)

