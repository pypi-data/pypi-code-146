import pyupbit
import datetime
import time
import numpy as np
import pandas as pd
import threading
import comathon as cmt
import requests


###### Create UPBIT API Class Instance (업로드 시 삭제) ######
access_key = "PBJJMdbWmo1r58HTbiwDMfoYjft1f49Mb7KYlpTZ"
secret_key = "nkN6sMNqUE7rj0WfLIjnY9XCXx5yCfQFvwCcuD3c"
comathon_ID = "test002"

## myAPI = cmt.Upbit(access_key, secret_key)  # API 로그인 함수 호출
## myAPI #myAPI 라는 instance가 생성됨

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)
myAPI.get_balance("KRW-ATOM")


###### Quotation 코드 ######
# cmt.get_ohlcv("KRW-ATOM", "day")
# cmt.get_current_price("KRW-ATOM")
# cmt.get_tickers("KRW")


###### Exchange 코드 ######
## 시장가 매수 코드 (API, Ticker, KRW Amount)
# cmt.buy_market_order(myAPI, "KRW-ATOM", 5000)

## 시장가 매도 코드 (API, Ticker, Fraction between 0 and 1)
# cmt.sell_market_order(myAPI, "KRW-ATOM", 1)


###### Basic Pyupbit Functions ######
def current_time():
    ct = datetime.datetime.now()
    return ct


####### Variables ######
time_delay = 60         ## delaying the loop by input time
time_instant = 0.02     ## delaying the data call from upbit
profit_rate = 1.02      ## profit rate
minimum_balance = 2000  ## minimum account balance to purchase coin
for_loop = 10000
buy_log = [0]
sell_log = [0]
ticker = ['KRW-ATOM']
##  day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
##  open  high  low  close  volume  value
candle = 5
itv = 'minute5'    ## interval


###### Log function ######
def log(n):     ## 0 : check log, 1 : sell, 2 : buy, 3 : everything
    print('check log history : ', 'sell log :', sell_log, 'buy log :', buy_log)
    if n == 0:
        print('sell log : ', sell_log, 'last item is :', sell_log[-1])
        return sell_log[-1]

    elif n == 1:
        print('sell log : ', sell_log, 'last item is :', sell_log[-1])
        sell_history_price = cmt.get_current_price(ticker[0])
        sell_log.append(sell_history_price)
        print('sell log append : ', sell_log, 'last item is :', sell_log[-1])

        sell_log5 = pd.DataFrame({'Price': [sell_log[-1]], 'Time': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')]})
        sell_log5.to_csv(r'sell_log5.csv', mode='a', index=False, header=False)
        return sell_log[-1]

    elif n == 2:
        print('buy log : ', buy_log, 'last item is :', buy_log[-1])
        buy_log_price = cmt.get_current_price(ticker[0])
        buy_log.append(buy_log_price)
        print('buy log append : ', buy_log, 'last item is :', buy_log[-1])

        buy_log5 = pd.DataFrame({'Price': [buy_log[-1]], 'Time': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')]})
        buy_log5.to_csv(r'buy_log5.csv', mode='a', index=False, header=False)
        return buy_log[-1]

    elif n == 3:
        current_log = pd.DataFrame({'Price': [cmt.get_current_price(ticker[0])], 'Time': [datetime.datetime.now().strftime('%Y-%m-%d %H:%M')]})
        current_log.to_csv(r'current_price_log.csv', mode='a', index=False, header=False)

    else:
        print('log error')


###### Buy Signals ######
def buying_signal_01(data):
    cpo = data['open']
    cpc = data['close']
    cpavg = (cpo+cpc)/2

    if cpavg[6] > cpavg[7] > cpavg[8] > cpavg[9]:
        print('Activate Signal 1')
        return 1
    else:
        print('    No signals to activate')


###### Selling Signals ######
def ma(data):
    cma_open = data['open']
    cma_close = data['close']
    cma_avg = np.around((cma_open + cma_close)/2, 1)
    cma_list = [cma_avg[0], cma_avg[1], cma_avg[2], cma_avg[3], cma_avg[4], cma_avg[5], cma_avg[6], cma_avg[7], cma_avg[8], cma_avg[9]]
    # print('cma_list : ', cma_list)

    numbers = cma_list
    window_size = 6

    numbers_series = pd.Series(numbers)
    windows = numbers_series.rolling(window_size)
    moving_averages = windows.mean()
    moving_averages_list = moving_averages.tolist()
    without_nans = moving_averages_list[window_size - 1:]

    print('    MA : ', np.around(without_nans, 1))
    ma_last = without_nans[-1]
    ma_last2 = without_nans[-2]
    slope = (ma_last - ma_last2)/15
    print('    slope : ', np.around(slope, 2))

    if slope > 0:
        print('positive slope')
    else:
        print('negative slope')

    return slope


###### Trading Function ######
def trading_coins():
    for i in range(for_loop):
        url = 'http://121.137.95.97:8889/Botalive?botid=Bot002'
        response = requests.get(url).json()
        print(response)

        try:
            for coin_name in ticker:
                current_data = pyupbit.get_ohlcv(ticker[0], interval=itv, count=10)

                if (i+9) % candle == 0:
                    print('      BUYING LOOP')
                    if buying_signal_01(current_data) == 1:
                        print(f'Activate Signal, {coin_name}')

                        if myAPI.get_balance(coin_name) * cmt.get_current_price(coin_name) > 5000:
                            print('  already have this coin')

                        elif myAPI.get_balance('KRW') > minimum_balance:

                            print('check the current price with last sell price')
                            if (log(0) == 0) or (log(0) > cmt.get_current_price(coin_name)):
                                buy_price = cmt.get_current_price(coin_name)
                                buy_amount = (np.round(myAPI.get_balance(ticker='KRW'), 0) - 2000)

                                print('--------------------------')
                                print(coin_name, ', BUY, Price :', buy_price, ', Time :', current_time())
                                print(cmt.buy_market_order(myAPI, coin_name, buy_amount))
                                print('--------------------------')

                            else:
                                print('last sale price is higher than current price')
                                pass
                        else:
                            print('Account has less than minimum balance')
                    else:
                        print(f'  Signal - Not Activated, {coin_name}')
                else:
                    print('skip to selling')

                time.sleep(time_instant)

                print('      SELLING LOOP')
                if myAPI.get_balance(coin_name) * cmt.get_current_price(coin_name) > 5000:
                    print(f'  trying to sell {coin_name}')

                    if (float(cmt.get_current_price(coin_name)) > 10000) & (ma(current_data) < 0):
                        time.sleep(time_instant)
                        sell_price = cmt.get_current_price(coin_name)

                        print('--------------------------')
                        print('Meet the profit rate and MA is negative slope')
                        print(coin_name, ', SELL, Price : ', sell_price, ', Time : ', current_time())
                        print(cmt.sell_market_order(myAPI, coin_name, 1))
                        print('--------------------------')

                    elif (float(cmt.get_current_price(coin_name)) > 10000) & (ma(current_data) >= 0):
                        print('Meet the profit rate but MA is positive slope')

                    else:
                        print(f'  {coin_name} does not meet the profit rate')
                else:
                    print(f'    No crypto to sell')
                    continue

            print(f'Loop Counter :', i)
            time.sleep(time_delay)

        except:
            print('Running Error')
            time.sleep(time_delay)
            continue


###### Multi-Threading ######
trading = threading.Thread(target = trading_coins)
trading.start()