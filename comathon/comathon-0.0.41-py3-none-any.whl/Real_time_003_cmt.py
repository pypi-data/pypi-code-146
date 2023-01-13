import comathon as cmt
import time, datetime, telegram
import pandas as pd

bot = telegram.Bot('859518036:AAGnIbbetS1Jx5cSNu9dNd-ymoKlqtXJcQo')

access_key = '5uJbvx4hQwArlLbKdxzHjYGWVtEcEaeVKRCIvXXS'  # access key
secret_key = 'jRkeAOYYYOg7sK8PCxG9AFrBKfP4voqVVYg2oyWI'  # secret key
comathon_ID = "test003" #현재 test001, tst002, test003 가 등록되어 있음, 수정요청함

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)  # API 로그인 함수 호

print('')

ticker = cmt.get_tickers('KRW')
record_num = 'real_004'
ini_bal = 20000
tar_profit = 2
start_date = '2022-12-18'


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


scr_list = []
def get_scr_list():
    global ticker, scr_list

    period_3 = 'day'
    scr_list = []
    for i in ticker:
        while True:
            try:

                ohlcv_3 = cmt.get_ohlcv(i, interval=period_3, count=2)
                h1_3 = (ohlcv_3['high'].tolist())[-2]
                h0_3 = (ohlcv_3['high'].tolist())[-1]
                c1_3 = (ohlcv_3['close'].tolist())[-2]
                o1_3 = (ohlcv_3['open'].tolist())[-2]
                # if h1_3 > h0_3 and o1_3 * 1.01 <= c1_3 and c1_3 * 1.01 < h1_3:
                if h1_3 > h0_3 and c1_3 > o1_3 * 1.01 and h1_3 > c1_3 * 1.005:
                # if h1_3 > h0_3 and \
                #         ((c1_3 > o1_3 * 1.01 and h1_3 > c1_3 * 1.005) or (c1_3 < o1_3 * 1.01 and h1_3 > o1_3 * 1.005)):
                    scr_list.append(i)
                    break
                else:
                    break

            except:
                # print('get_scr_list_error')
                pass
start = time.time()
get_scr_list()
end = time.time()
time_msg = "↑ get_scr_list >>> Processing Time : " + format(end - start, '3.2f') + ' sec\n'
print(scr_list)
print(time_msg)
t_period = 'day'
msg_interval = 'minute15'


#
now = datetime.datetime.now()
time_set = datetime.datetime(now.year, now.month, now.day)

start_time_get_scr_list = time_set + datetime.timedelta(hours=9, seconds=30)
stop_time_get_scr_list = start_time_get_scr_list + datetime.timedelta(minutes=5)

end_position_start_time = time_set + datetime.timedelta(hours=9, seconds=-30)
end_position_stop_time = end_position_start_time + datetime.timedelta(minutes=5)

scr_list_start_time = time_set + datetime.timedelta(hours=9, minutes=-1)
scr_list_stop_time = scr_list_start_time + datetime.timedelta(minutes=5)


#
start = time.time()
next_t = 0
def get_next_t():
    global msg_interval, next_t
    if msg_interval == 'minute5':
        next_t = 1/12
    elif msg_interval == 'minute15':
        next_t = 1/4
    elif msg_interval == 'minute30':
        next_t = 1/2
    elif msg_interval == 'minute60':
        next_t = 1
    elif msg_interval == 'minute240':
        next_t = 4
    elif msg_interval == 'day':
        next_t = 24
    elif msg_interval == 'week':
        next_t = 168
get_next_t()

start_time_msg = time_set + datetime.timedelta(hours=now.hour, seconds=-2)
stop_time_msg = start_time_msg + datetime.timedelta(minutes=5)

while True:
    if start_time_msg < now:
        break
    elif now < start_time_msg:
        start_time_msg = start_time_msg - datetime.timedelta(hours=next_t)
        stop_time_msg = stop_time_msg - datetime.timedelta(hours=next_t)
    # print(start, stop)
while True:
    if start_time_msg > now:
        break
    elif now > start_time_msg:
        start_time_msg = start_time_msg + datetime.timedelta(hours=next_t)
        stop_time_msg = stop_time_msg + datetime.timedelta(hours=next_t)
end = time.time()
time_msg = "↑ set_msg_time >>> Processing Time : " + format(end - start, '3.2f') + ' sec\n'
print(start_time_msg, stop_time_msg)
print(time_msg)


# 사전실행
get_coin_bal()
krw = get_krw_bal()
buy_amount = krw * 0.9995


# 엑셀 데이터 수집
buy_price = []
stop_price = 0
stop_price2 = 0
avg_price = 0
if len(bal_ticker) == 0:
    avg_price = 0
else:
    avg_price = myAPI.get_avg_buy_price(bal_ticker[0])

#
profit = 0

h1_t = 0
c0_t = 0
h0_t = 0

avg_v = 0
v2_5min = 0
v1_5min = 0
o1_5min = 0
c1_5min = 0
h1_5min = 0

l1_1min = 0

ret_msg = 0
avg_slippage = 0

while True:
    try:
        now = datetime.datetime.now()
        check_server = cmt.server_alive(myAPI)
        print("Server Online : ", check_server)

        if len(bal_ticker) == 0:
            if len(scr_list) > 0:
                for i in scr_list:
                    while True:
                        try:
                            ohlcv_t = cmt.get_ohlcv(i, interval=t_period, count=2)
                            h1_t = (ohlcv_t['high'].tolist())[-2]
                            h0_t = (ohlcv_t['high'].tolist())[-1]
                            c0_t = (ohlcv_t['close'].tolist())[-1]
                            break
                        except:
                            pass
                    if h1_t < c0_t:
                        while True:
                            try:
                                ohlcv_5min = cmt.get_ohlcv(i, interval='minute5', count=6)

                                v_5min = ohlcv_5min['volume'].tolist()
                                sum_v_5min = sum(v_5min[:-1])
                                avg_v = sum_v_5min/5

                                v2_5min = (ohlcv_5min['volume'].tolist())[-2]
                                v1_5min = (ohlcv_5min['volume'].tolist())[-1]
                                o1_5min = (ohlcv_5min['open'].tolist())[-1]
                                c1_5min = (ohlcv_5min['close'].tolist())[-1]
                                h1_5min = (ohlcv_5min['high'].tolist())[-1]
                                # print(i, v0_5min, avg_v, o0_5min, c0_5min)
                                break
                            except:
                                # print('error2', i)
                                pass
                        if avg_v * 3 < v1_5min \
                                and o1_5min < c1_5min < o1_5min * 1.03 \
                                and h1_t < c1_5min < h1_t * 1.01 \
                                and h0_t < h1_t * 1.02 \
                                and v2_5min < v1_5min:
                            krw = get_krw_bal()
                            buy_amount = krw * 0.9995
                            bal_ticker.append(i)
                            buy_price.append(c0_t)
                            myAPI.buy_market_order(i, buy_amount)
                            bot.send_message('@chaesoone', '[BUY] ' + str(i) + ' at ' + str(c0_t))
                            time.sleep(60)
                            avg_price = myAPI.get_avg_buy_price(i)
                            break
                        else:
                            print(i, now)
                            pass
                if scr_list_start_time < now < scr_list_stop_time:
                    bot.send_message('@chaesoone', 'Market closed')
                    scr_list = []
                    scr_list_start_time = scr_list_start_time + datetime.timedelta(hours=24)
                    scr_list_stop_time = scr_list_start_time + datetime.timedelta(minutes=5)
                elif scr_list_stop_time < now:
                    scr_list_start_time = scr_list_start_time + datetime.timedelta(hours=24)
                    scr_list_stop_time = scr_list_start_time + datetime.timedelta(minutes=5)

            elif len(scr_list) == 0:
                if start_time_get_scr_list < now < stop_time_get_scr_list:
                    get_scr_list()
                    bot.send_message('@chaesoone', 'Market started')
                    start_time_get_scr_list = start_time_get_scr_list + datetime.timedelta(hours=24)
                    stop_time_get_scr_list = start_time_get_scr_list + datetime.timedelta(minutes=5)
                elif stop_time_get_scr_list < now:
                    start_time_get_scr_list = start_time_get_scr_list + datetime.timedelta(hours=24)
                    stop_time_get_scr_list = start_time_get_scr_list + datetime.timedelta(minutes=5)

        elif len(bal_ticker) != 0:
            now_price = cmt.get_current_price(bal_ticker[0])
            profit = (now_price/buy_price[0] - 1) * 100
            profit2 = (now_price/avg_price - 1) * 100

            while True:
                try:
                    ohlcv_1min = cmt.get_ohlcv(bal_ticker[0], interval='minute1', count=4)
                    l1_1min = (ohlcv_1min['low'].tolist())[-2]
                    break
                except:
                    pass

            if now_price < l1_1min:
                myAPI.sell_market_order(bal_ticker[0], 1)
                time.sleep(3)


                krw = get_krw_bal()
                r_profit = (krw/ini_bal-1) * 100
                bot.send_message('@chaesoone', '[SELL] ' + bal_ticker[0]  + ' at ' + str(now_price)
                                 + ' (' + format(profit, '3.2f') + '%' + ')')
                get_scr_list()
                bal_ticker = []
                buy_price = []

            elif end_position_start_time < now < end_position_stop_time:
                myAPI.sell_market_order(bal_ticker[0], 1)
                time.sleep(3)

                krw = get_krw_bal()
                r_profit = (krw/ini_bal-1) * 100

                bot.send_message('@chaesoone', '[SELL2] ' + bal_ticker[0] + ' (' + format(profit, '3.2f') + '%' + ')')
                get_scr_list()
                bal_ticker = []
                buy_price = []

                end_position_start_time = end_position_start_time + datetime.timedelta(hours=24)
                end_position_stop_time = end_position_start_time + datetime.timedelta(minutes=5)
            elif end_position_stop_time < now:
                end_position_start_time = end_position_start_time + datetime.timedelta(hours=24)
                end_position_stop_time = end_position_start_time + datetime.timedelta(minutes=5)

        if start_time_msg < now < stop_time_msg:

            if len(bal_ticker) == 0:
                ret_msg = 'empty'
            elif len(bal_ticker) != 0:
                ret_msg = bal_ticker[0] + ' (' + format(profit, '3.2f') + '%' + ')'

            krw = get_krw_bal()
            r_profit = (krw/ini_bal-1) * 100

            bot.send_message('@chaesoone', '[UPBIT] Real-time Trading Report\n' + 'Initiated on ' + start_date + '\n' +
                             '\nReal profit is ' + format(r_profit, '3.2f') + '%' +
                             '\nAvg. slippage is ' + format(avg_slippage, '3.2f') + '%' +
                             '\nRetained item is ' + ret_msg)

            start_time_msg = start_time_msg + datetime.timedelta(hours=next_t)
            stop_time_msg = stop_time_msg + datetime.timedelta(hours=next_t)
        elif stop_time_msg < now:
            start_time_msg = start_time_msg + datetime.timedelta(hours=next_t)
            stop_time_msg = stop_time_msg + datetime.timedelta(hours=next_t)

    except:
        # print('Main Roof Error', now)
        pass