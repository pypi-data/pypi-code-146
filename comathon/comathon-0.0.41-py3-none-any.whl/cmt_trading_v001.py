import comathon as cmt
import time
import datetime
import telegram
import pyupbit
import threading
import pandas as pd

bot = telegram.Bot('859518036:AAGnIbbetS1Jx5cSNu9dNd-ymoKlqtXJcQo')
access_key = '5uJbvx4hQwArlLbKdxzHjYGWVtEcEaeVKRCIvXXS'  # access key
secret_key = 'jRkeAOYYYOg7sK8PCxG9AFrBKfP4voqVVYg2oyWI'  # secret key
comathon_ID = "test003" #현재 test001, tst002, test003 가 등록되어 있음, 수정요청함

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)  # API 로그인 함수 호

ticker = cmt.get_tickers('KRW')

c3_rate = -0.25
c2_rate = -0.25
target_profit = 1
interval = 'minute15'
trend_interval = 'day'
ret_counts = 3
record_num = '004'
record_sig = 0
forced_sell = 1
ini_bal = 56726


next_t = 0
def get_next_t():
    global interval, next_t
    if interval == 'minute5':
        next_t = 1/12
    elif interval == 'minute15':
        next_t = 1/4
    elif interval == 'minute30':
        next_t = 1/2
    elif interval == 'minute60':
        next_t = 1
    elif interval == 'minute240':
        next_t = 4
    elif interval == 'day':
        next_t = 24
    elif interval == 'week':
        next_t = 168
get_next_t()


now = datetime.datetime.now()
time_set = datetime.datetime(now.year, now.month, now.day)

start = time_set + datetime.timedelta(hours=8, minutes=59, seconds=40)
stop = start + datetime.timedelta(minutes=1)

msg_start = time_set + datetime.timedelta(hours=now.hour)
msg_stop = msg_start + datetime.timedelta(minutes=2)

while True:
    if start < now:
        break
    elif now < start:
        start = start - datetime.timedelta(hours=next_t)
        stop = stop - datetime.timedelta(hours=next_t)
    # print(start, stop)

while True:
    if start > now:
        break
    elif now > start:
        start = start + datetime.timedelta(hours=next_t)
        stop = stop + datetime.timedelta(hours=next_t)
    # print(start,stop)

# 원화잔고 작성
def get_krw_bal():
    try:
        krw_bal = int(myAPI.get_balance())
        return krw_bal
    except:
        pass


bal_dict = {}
bal_ticker = []
def get_coin_bal():
    global bal_dict, ticker, bal_ticker
    bal_dict = {}
    bal_ticker = []
    while True:
        try:
            t_coin_bal = myAPI.get_balances()
            break
        except:
            pass
    for i in range(len(t_coin_bal)):
        if i >= 1:
            while True:
                try:
                    krw_name = 'KRW-' + t_coin_bal[i]['currency']
                    # print(krw_name)
                    if i > 0 and krw_name in ticker:
                        coin_bal = float(t_coin_bal[i]['balance'])
                        now_coin_price = cmt.get_current_price(krw_name)
                        coin_krw_bal = now_coin_price * coin_bal

                        # print(coin_krw_bal)
                        if coin_krw_bal > 10000:
                            bal_dict[krw_name] = coin_bal
                            bal_ticker.append(krw_name)
                    break
                except:
                    pass


def initialize_data(num):
    global record_num
    if num == 1:
        position_list_0 = []
        date_list_0 = []
        ticker_list_0 = []
        price_list_0 = []
        profit_list_0 = []
        retained_0 = []
        interval_0 = []
        pur_0 = []
        pdr_0 = []

        raw_data = {'position': position_list_0,
                    'date': date_list_0,
                    'ticker': ticker_list_0,
                    'price': price_list_0,
                    'profit': profit_list_0,
                    'retained': retained_0,
                    'interval': interval_0,
                    'pur': pur_0,
                    'pdr': pdr_0}

        raw_data = pd.DataFrame(raw_data)
        raw_data.to_excel(excel_writer=record_num+'_data.xlsx')
        print('Data was initialized.')
    elif num != 1:
        print('Data was maintained.')


def record_data(item, status):
    global interval, up_rate, dw_rate
    start = time.time()
    df = pd.read_excel(record_num+'_data.xlsx')

    position_list = df['position'].tolist()
    position = status
    position_list.append(position)
    print(position_list)

    date_list = df['date'].tolist()
    date = datetime.datetime.now()
    date_list.append(date)
    print(date_list)

    ticker_list = df['ticker'].tolist()
    Ticker = item
    ticker_list.append(Ticker)
    print(ticker_list)

    price_list = df['price'].tolist()
    price = cmt.get_current_price(item)
    price_list.append(price)
    print(price_list)

    profit_list = df['profit'].tolist()
    rate = 0
    if len(profit_list) > 0:
        if position_list[-1] == 'BUY':
            rate = 0
        elif position_list[-1] == 'SELL':
            rate = (price_list[-1]/price_list[-2] - 1) * 100
    elif len(profit_list) == 0:
        rate = 0
    profit_list.append(rate)
    print(profit_list)

    retained_list = df['retained'].tolist()
    retained = 0
    if len(retained_list) > 0:
        if position_list[-2] == 'BUY':
            retained = 0
        elif position_list[-2] == 'SELL':
            retained = (date_list[-1] - date_list[-2]).days
    elif len(retained_list) == 0:
        retained = 0
    retained_list.append(retained)
    print(retained_list)

    interval_list = df['interval'].tolist()
    intv = interval
    interval_list.append(intv)
    print(interval_list)

    pur_list = df['pur'].tolist()
    pur = up_rate
    pur_list.append(pur)
    print(pur)

    pdr_list = df['pdr'].tolist()
    pdr = dw_rate
    pdr_list.append(pdr)
    print(pdr)

    raw_data = {'position': position_list,
                'date': date_list,
                'ticker': ticker_list,
                'price': price_list,
                'profit': profit_list,
                'retained': retained_list,
                'interval': interval_list,
                'pur': pur_list,
                'pdr': pdr_list}

    raw_data = pd.DataFrame(raw_data)
    raw_data.to_excel(excel_writer=record_num+'_data.xlsx')

    print('completed')
    end = time.time()
    time_msg = "Processing Time : " + format(end - start, '3.2f') + ' sec'
    print(time_msg)


def get_retained_counts():
    global interval
    df = pd.read_excel(record_num+'_data.xlsx')

    date_list = df['date'].tolist()
    date = datetime.datetime.now()
    if interval == 'day':
        retained_day = (date - date_list[-1]).days
        print(retained_day)
        return retained_day
    elif interval == 'minute15':
        retained_day = (date - date_list[-1]).seconds/60/15
        print(retained_day)
        return retained_day
    elif interval == 'minute30':
        retained_day = (date - date_list[-1]).seconds/60/30
        print(retained_day)
        return retained_day
    elif interval == 'minute240':
        retained_day = (date - date_list[-1]).seconds/60/240
        print(retained_day)
        return retained_day
    elif interval == 'minute60':
        retained_day = (date - date_list[-1]).seconds/60/60
        print(retained_day)
        return retained_day
    elif interval == 'week':
        retained_day = (date - date_list[-1]).days/7
        print(retained_day)
        return retained_day


up_list = []
dw_list = []
zr_list = []
up_rate = 0
zr_rate = 0
dw_rate = 0


buy_list = []
buy_ticker = 0
def get_buy_list():
    global buy_list, ticker, buy_ticker, c3_rate, c2_rate, interval, target_profit
    buy_list = []
    buy_ticker = 0
    start = time.time()
    for i in ticker:
        while True:
            try:
                close = cmt.get_ohlcv(i, interval=interval, count=5)['close'].tolist()
                day_raw = cmt.get_ohlcv(i, interval='day', count=3)
                day_close = day_raw['close'].tolist()
                day_high = day_raw['high'].tolist()
                day_h_profit = (day_high[-1] / day_close[-2] - 1) * 100
                day_c_profit = (day_close[-1] / day_close[-2] - 1) * 100
                # print(day_c_profit, day_h_profit)
                orderbook = cmt.get_orderbook(i)
                # print(orderbook)
                asks_1 = orderbook['orderbook_units'][0]['ask_price']
                # print(asks_1)
                # print(indicator_1, close)
                if day_h_profit > 3 and day_c_profit > 0:
                    if (close[-5] * (100 + c3_rate) / 100 > close[-4]
                        and close[-4] * (100 + c2_rate) / 100 > close[-3]
                        and close[-3] < close[-2]
                        and close[-2] > close[-1]) \
                            and (asks_1 == close[-1]):
                        buy_list.append(i)
                break
            except:
                pass
    ticker_vol = 0

    if len(buy_list) > 0:
        for i in buy_list:
            while True:
                try:
                    value =cmt.get_ohlcv(i, interval=interval, count=1)['value'].tolist()
                    # print('ticker_vol =', ticker_vol)
                    if value[-1] > ticker_vol:
                        buy_ticker = i
                        ticker_vol = value[-1]
                    else:
                        pass
                    break
                except:
                    pass

    end = time.time()
    time_msg = "Processing Time : " + format(end - start, '3.2f') + ' sec'

    signal_msg = ''
    if len(buy_list) == 0:
        signal_msg = signal_msg + '\n0. no signals'
    elif len(buy_list) > 0:
        for i in range(len(buy_list)):
            signal_msg = signal_msg + '\n' + str(i + 1) + '. ' + buy_list[i]

    bot.send_message('@chaesoone', 'Buy Signals : ' + '\n' + signal_msg
                     + '\n\n' + time_msg)


profit = 0
bids_profit = 0
bids_1_size = 0
def get_profit(f_ticker):
    global profit, bids_profit, bids_1_size
    while True:
        try:
            avg_price = myAPI.get_avg_buy_price(f_ticker)
            orderbook = cmt.get_orderbook(f_ticker)
            bids_1 = orderbook['orderbook_units'][0]['bid_price']
            bids_1_size = orderbook['orderbook_units'][0]['bid_size']
            bids_profit = (bids_1 / avg_price - 1) * 100
            h_1min = cmt.get_ohlcv(f_ticker, 'minute1', 2)['high'].tolist()
            profit = (h_1min[-1]/avg_price-1) * 100
            break
        except:
            print('get_profit_error')

initialize_data(record_sig)


count = 0
while True:
    try:
        now = datetime.datetime.now()
        # print(now, '\n', start, '\n', stop)
        t1 = threading.Thread(target=get_coin_bal())
        t1.start()
        t1.join()

        if len(bal_ticker) > 0 and forced_sell == 1:
            cmt.sell_market_order(myAPI, bal_ticker[0], 1)
            bot.send_message('@chaesoone', '[SELL-forced] ' + bal_ticker[0])
            record_data(bal_ticker[0], 'SELL')
            forced_sell = 0
            time.sleep(5)
            get_coin_bal()  # bal_ticker 재작성

###
        if start < now < stop:

            if len(bal_ticker) > 0:
                elapsed_day = get_retained_counts()
                if elapsed_day >= ret_counts:
                    cmt.sell_market_order(myAPI, bal_ticker[0], 1)
                    bot.send_message('@chaesoone', '[SELL-fail] ' + bal_ticker[0])
                    record_data(bal_ticker[0], 'SELL')
                    time.sleep(5)
                    get_coin_bal()  # bal_ticker 재작성

            if len(bal_ticker) == 0:
                krw = get_krw_bal()
                get_buy_list()  # buy_list 재작성
                if krw > 10000 and len(buy_list) != 0:
                    buy_amount = krw * 0.9995
                    cmt.buy_market_order(myAPI, buy_ticker, buy_amount)
                    bot.send_message('@chaesoone', '[BUY] ' + str(buy_ticker))
                    record_data(buy_ticker, 'BUY')
                    time.sleep(5)
                    get_coin_bal()

            start = start + datetime.timedelta(hours=next_t)
            stop = stop + datetime.timedelta(hours=next_t)

        elif now > stop:

            start = start + datetime.timedelta(hours=next_t)
            stop = stop + datetime.timedelta(hours=next_t)
###
        if len(bal_ticker) > 0:  # 실시간 감시
            t2 = threading.Thread(target=get_profit(bal_ticker[0]))
            t2.start()
            t2.join()

            if bids_profit >= target_profit and bids_1_size > bal_dict[bal_ticker[0]]:
                cmt.sell_market_order(myAPI, bal_ticker[0], 1)
                bot.send_message('@chaesoone', '[SELL-success] ' + bal_ticker[0])
                record_data(bal_ticker[0], 'SELL')
                time.sleep(5)
                get_coin_bal()


###
        if msg_start < now < msg_stop:

            if len(bal_ticker) == 0:
                krw = get_krw_bal()
                bot.send_message('@chaesoone', 'Account Profit : '+format((krw/ini_bal-1)*100, '3.2f')+'%')
            msg_start = msg_start + datetime.timedelta(hours=0.5)
            msg_stop = msg_stop + datetime.timedelta(hours=0.5)
        elif now > msg_stop:
            msg_start = msg_start + datetime.timedelta(hours=0.5)
            msg_stop = msg_stop + datetime.timedelta(hours=0.5)

        time.sleep(0.2)

    except:
        print('roof_error')
        pass