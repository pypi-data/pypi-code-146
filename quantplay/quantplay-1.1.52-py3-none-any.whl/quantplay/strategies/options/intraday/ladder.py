from quantplay.service import market
import pandas as pd
import time
from quantplay.broker.client import broker_client

backtest_date = "2022-01-20"

def load_data(data_date):
    # Load data
    data = market.data(interval="minute", symbols_by_security_type={"EQ": ["NIFTY BANK"]})
    data = data[data.date > "{} 08:15:00".format(data_date)]
    data = data[data.date < "{} 15:15:00".format(data_date)]
    data.loc[:, "day_of_week"] = data.date.dt.day_name()
    data = data[data.date.dt.hour < 17]

    # Add additional attributes
    data = market.add_expiry(data, security_type="OPT", days_offset=0)

    return data

data = load_data(backtest_date)

data_seq = data.to_dict('records')

for d in data_seq:
    timestamp = d['date']
    broker_client.ping(timestamp)
    ltp = d['open']
    strike_gap = d['strike_gap']
    expiry = d['expiry_date']
    if timestamp.hour == 9 and timestamp.minute < 30:
        print("waiting for market to cool down")
        continue

    if timestamp.hour > 13:
        print("market is about to close, let's not place any orders")
        continue

    orders = broker_client.orders(tag="ladder")

    if len(orders) == 0:
        atm = int(round(ltp / strike_gap) * strike_gap)
        pe_symbol = broker_client.option_symbol("NIFTY BANK", expiry, atm, "PE")
        ce_symbol = broker_client.option_symbol("NIFTY BANK", expiry, atm, "CE")

        broker_client.execute_order(
            tradingsymbol=pe_symbol,
            exchange="NSE",
            quantity=100,
            order_type='MARKET',
            transaction_type='SELL',
            stoploss=0.8,
            tag="ladder",
            product="NRML"
        )
        broker_client.execute_order(
            tradingsymbol=ce_symbol,
            exchange="NSE",
            quantity=100,
            order_type='MARKET',
            transaction_type='SELL',
            stoploss=0.8,
            tag="ladder",
            product="NRML"
        )