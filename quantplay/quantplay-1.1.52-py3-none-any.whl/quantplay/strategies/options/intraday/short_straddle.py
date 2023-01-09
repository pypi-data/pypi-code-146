from quantplay.service import market

market.broker.execute_order(tradingsymbol="SBIN",
                            exchange="NSE",
                            quantity=1,
                            order_type="MARKET",
                            transaction_type="BUY",
                            stoploss=0.03,
                            tag='straddle',
                            product="MIS")
