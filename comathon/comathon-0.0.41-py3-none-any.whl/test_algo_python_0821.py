## Load Modules and Packages
import pyupbit
import pandas as pd
import numpy as np
import time
import datetime as dt
import telegram
import comathon as cm
import seaborn as sns
import matplotlib as plt


## Connect Upbit API (개인 컴퓨터에서 기초개발할때만 사용, 서버에서 돌릴땐 comathon module 사용)
access_key = "DplIC0dHKeVVjr9RtRhJskZD2xVTkxdQtHno6BpO"
secret_key = "6xV4OlFjLv7P8PoHyuOrRgE1Qk1kmnEfB8Mmzmh4"

upbit = pyupbit.Upbit(access_key, secret_key)  # API 로그인 함수 호출
upbit #upbit 라는 instance가 생성됨


## Load Telegram Bot (텔레그램  메세지 연결 모듈)
bot_name = 'Piglet' #Coma or Piglet
bot = load_telegram()

activate_bot = True

chat_id = "@Comathon_coma" #김정 Open Channel
chat_id2 = "1041595364" # 김정 kptib88_bot

if activate_bot:
    bot.sendMessage(chat_id, text =f"{bot_name} : Telegram Bot Activated")


## Get my KRW balance
KRW_balance = upbit.get_balance()
# KRW_balance
print("My current KRW balance is :", KRW_balance)

Invest_limit = 100000 # Investment Limit, set by user (실제로는 comathon module에서 자동 tracking 으로 업그레이드 예정)
Invest_remain = Invest_limit

krw_ticker = 'KRW-BTC'



msg_update = (f"Code Initiated at {dt.datetime.today().strftime('%Y-%m-%d-%HH-%MM')}, GAZUA! \n")
print(msg_update)

if activate_bot:
    bot.sendMessage(chat_id, text = msg_update)      

i = -1
while True:

    ## Keep Index  

    i += 1
    msg_update = (f"Today is {dt.datetime.today().strftime('%Y-%m-%d-%HH-%MM')}, Index now at {i} \n")
    print(msg_update)


    ## Check BTC balance and price
    BTC_balance = upbit.get_balance('KRW-BTC')
    # print("My Current BTC balance is : ", BTC_balance)

    BTC_price = pyupbit.get_current_price('KRW-BTC')
    # print("Current BTC Price is : ", BTC_price)

    ## Get BTC price data and calculate MA
    df = pyupbit.get_ohlcv("KRW-BTC", count = 200, interval = 'minute1')
    df['MA12'] = df['close'].rolling(window= 12, center=False).mean()
    df['MA26'] = df['close'].rolling(window= 26, center=False).mean()
   
    make_plot(df)
    matplotlib.pyplot.close('all')

    ## Check Signal (GC or DC)
    GC = 0
    DC = 0
    # print('Checkpoint #1')
    if df['MA12'][-2] < df['MA26'][-2] and df['MA12'][-1] > df['MA26'][-1]:
        print('A Gold Cross has been detected')
        GC = 1
        DC = 0
    elif df['MA12'][-2] > df['MA26'][-2] and df['MA12'][-1] < df['MA26'][-1]:
        print('A Dead Cross has been detected')
        GC = 0
        DC = 1
    else:
        print('No Signal Detected')
        GC = 0
        DC = 0

    # print('Checkpoint #2')

    ## Make Trades, keep track of the remaining investment fund
    if GC == 1 and DC == 0:
        ## Tracking remaining investment fund
        buy_amount_KRW = Invest_remain * 0.1
        Invest_remain = Invest_remain - buy_amount_KRW

        buy_coin = upbit.buy_market_order('KRW-BTC', buy_amount_KRW) ## 시장가 매수
        
        msg_update = (f"Signal : Gold Cross Detected, 시장가 매수 진행 \n"
                      f"Current Time : {dt.datetime.today().strftime('%m-%d %H:%M')} \n") 

        print(msg_update)

        if activate_bot:
            bot.sendMessage(chat_id, text = msg_update)       

    elif GC == 0 and DC == 1:
        BTC_balance = upbit.get_balance('KRW-BTC')

        if (BTC_balance is None):
            print('BTC_balance is NONE, pass')
        else:

            ## 수익율 확인, 2% 이상에서만 매도 진행
            Sell_amount = BTC_balance * BTC_price
            Invest_remain = Invest_remain + Sell_amount
            
            
            sell_coin = upbit.sell_market_order('KRW-BTC', BTC_balance) ## Sell all balance
            
            ## Tracking remaining investment fund
            
            

            msg_update = (f"Signal : Dead Cross Detected, 시장가 매도 진행 \n"
                        f"Current Time : {dt.datetime.today().strftime('%m-%d %H:%M')} \n") 

            print(msg_update)

            if activate_bot:
                bot.sendMessage(chat_id, text = msg_update)              
    else:
        print('No Signal detected #2')        

    # print('Checkpoint #3')
    ## 6. Sleep until the next round, 10 sec sleep loop until the target_time

    for z in range(1 * 6): # min * 6 --> in 10 secs
        time.sleep(10) #seconds

    # time_diff_min = calculate_time_diff()
    # print(time_diff_min,"minutes until the next calculation round")
    # for z in range(time_diff_min * 6): # min * 6 --> in 10 secs
    #     time.sleep(10) #seconds





## 추가로 작성해서 사용하는 function들 
def load_telegram():
    ## Load Telegram Bot
    chat_id = "@Comathon_coma" #김정 Open Channel
    chat_id2 = "1041595364" # 김정 kptib88_bot (practice)
    
    token = '1017063622:AAG3GAU-mPyGFqpPN_MneEvLKoLMBH4BmqE' #김정

    bot = telegram.Bot(token) #Open Channel

#     bot.sendMessage(chat_id2, text ="COMA : Trading Bot Initiated")
#     bot.sendMessage(chat_id2, text = "COMA2 : Trading Bot Initiated")

    return bot

def calculate_time_diff():

    ## 정확히 정각에서 3분 이후에 매매해야함
    ## ohlcv는 정각 데이터를 가져옴
    ## Calculate current time, estimate the next hour

    c_time = dt.datetime.today()
    # print(c_time)

    target_time = c_time + dt.timedelta(hours = 1)
    # print(target_time)
    target_time = target_time.replace(minute = 3, second = 0, microsecond = 0) #매 시간 3분에 계산 진행
    # print(target_time)

    ## Calculate the time difference from that date to now
    time_diff = target_time - c_time
    time_diff_min = int(time_diff.total_seconds()/60)
    print(time_diff_min,"minutes until the next calculation round")

    return time_diff_min

def make_plot(df):

    x = df.index
    y = df.close
    fig, ax = plt.pyplot.subplots() 
    
    
    sns.lineplot(ax = ax, x = df.index, y = df.close)
    sns.lineplot(ax = ax, x = df.index, y = df.MA12)
    sns.lineplot(ax = ax, x = df.index, y = df.MA26)

    plt.pyplot.xticks(rotation=40)
    plt.pyplot.grid(True)
    plt.pyplot.title('BTC 10 min, MA12, MA26')
    plt.pyplot.xlabel('Date')
    plt.pyplot.ylabel('BTC Price')


    # time_now = dt.datetime.today().strftime('%m-%d-%H-%M')
    file_name = f"test.png"
    # IPydisplay.Image(filename=file_name)
    
    save_img = fig.savefig(file_name)
    bot.sendPhoto(chat_id, photo=open(file_name, 'rb'))

    plt.pyplot.close('all')

def get_balance():
    ## Get My Upbit Balance

    balance = upbit.get_balances()
    time.sleep(0.1)

    df_balance = pd.DataFrame(
        columns=['currency', 'balance', 'avg_buy_price', 'KRW_avg_buy_price', 'current_price', 'KRW_current_balance',
                 'Current_Profit(%)', 'KRW_total_balance', 'KRW_total_profit(%)'])
    pd.options.display.float_format = '{:,.2f}'.format

    # Loop through each item in the balance
    for i in range(len(balance[0])):

        coin = balance[0][i]
#         print(coin)

        ## If the item 'KRW', then skip
        if coin['currency'] == 'KRW':
            df_balance = df_balance.append(coin, ignore_index=True)

        ## Loop through other coins, calculate the current balance and profit (some random coins in my balance, I must generalize this.. )
        elif coin['currency'] == 'HORUS' or coin['currency'] == 'ADD' or coin['currency'] == 'MEETONE' or coin['currency'] == 'CHL' or coin['currency'] == 'BLACK' or coin['currency'] == 'JST' or coin['currency'] == 'WIN' :
            pass
        else:
            coin['KRW_avg_buy_price'] = float(coin['balance']) * float(coin['avg_buy_price'])

            coin['current_price'] = pyupbit.get_current_price('KRW-' + coin['currency'])
            time.sleep(0.1)

            ## Many times current_price returns TypeError, this code handles it
            if coin['current_price'] == None:
                coin['KRW_current_balance'] = 1
                coin_name = coin['currency']

            else:
                coin['KRW_current_balance'] = float(coin['balance']) * float(coin['current_price'])

            ## Prevent division by zero
            if coin['KRW_avg_buy_price'] == None:
                coin['Current_profit(%)'] == None

            else:
                try:
                    coin['Current_Profit(%)'] = (coin['KRW_current_balance'] - coin['KRW_avg_buy_price']) / coin[
                        'KRW_avg_buy_price'] * 100
                    df_balance = df_balance.append(coin, ignore_index=True)
                except:
                    pass

    df_upbit_balance = df_balance.copy()

    return df_upbit_balance
    