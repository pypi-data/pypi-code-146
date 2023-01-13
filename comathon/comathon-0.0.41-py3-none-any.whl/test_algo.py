## Load Modules and Packages
import pyupbit
import pandas as pd
import numpy as np
import time
import datetime as dt
import telegram #python-telegram-bot
import comathon as cmt
import seaborn as sns
import matplotlib as plt
import requests


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
    plt.pyplot.title('Ticker 10 min, MA12, MA26')
    plt.pyplot.xlabel('Date')
    plt.pyplot.ylabel('Ticker Price')


    # time_now = dt.datetime.today().strftime('%m-%d-%H-%M')
    file_name = f"test.png"
    # IPydisplay.Image(filename=file_name)
    
    save_img = fig.savefig(file_name)
    bot.sendPhoto(chat_id, photo=open(file_name, 'rb'))

    plt.pyplot.close('all')


## Connect Upbit API (개인 컴퓨터에서 기초개발할때만 사용, 서버에서 돌릴땐 comathon module 사용)
access_key = "DplIC0dHKeVVjr9RtRhJskZD2xVTkxdQtHno6BpO"
secret_key = "6xV4OlFjLv7P8PoHyuOrRgE1Qk1kmnEfB8Mmzmh4"
comathon_ID = 'test001'

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)  # API 로그인 함수 호출
# myAPI #myAPI 라는 UPBIT와 연계된 class instance가 생성됨
# myAPI.ID

## Load Telegram Bot (텔레그램  메세지 연결 모듈)
bot_name = 'Piglet' #Coma or Piglet
bot = load_telegram()

activate_bot = True

chat_id = "@Comathon_coma" #김정 Open Channel
chat_id2 = "1041595364" # 김정 kptib88_bot

if activate_bot:
    bot.sendMessage(chat_id, text =f"{bot_name} : Telegram Bot Activated")


## Get my KRW balance (defensive programming)
while True:
    try:
        KRW_balance = myAPI.get_balance()

        if KRW_balance is None:
            print("UPBIT API Error while executing get_balance() function")
            time.sleep(0.1)
            pass
        else:
            break
    except:
        print("UPBIT API Error while executing get_balance() function")
        time.sleep(0.1)
        pass

KRW_balance
print("My current KRW balance is :", KRW_balance)

Invest_limit = 20000 # Investment Limit, set by user (실제로는 comathon module에서 자동 tracking 으로 업그레이드 예정)
Invest_remain = Invest_limit

ticker_list = ["KRW-ATOM", "KRW-XLM", "KRW-CELO"]
# krw_ticker = 'KRW-ATOM'
msg_update = ("This code will trade the following tickers", ticker_list)
print(msg_update)

if activate_bot:
    bot.sendMessage(chat_id, text = msg_update)      


msg_update = (f"Code Initiated at {dt.datetime.today().strftime('%Y-%m-%d-%HH-%MM')}, GAZUA! \n")
print(msg_update)

if activate_bot:
    bot.sendMessage(chat_id, text = msg_update)      

i = -1
while True:

    ## Check if the connection with the Server is Online
    check_server_url = myAPI.boturl
    response = requests.get(check_server_url).json()
    print(response)

    ## Similar Code to check server connection
    check_server = cmt.server_alive(myAPI)
    print("Server Online : ", check_server)
        
    ## Keep Index  
    
    i += 1
    msg_update = (f"Today is {dt.datetime.today().strftime('%Y-%m-%d-%HH-%MM')}, Index now at {i} \n")
    print(msg_update)


    ## Loop Tickers from here
    for krw_ticker in ticker_list:

        ## Check ticker balance and price
        ticker_balance = myAPI.get_balance(krw_ticker)
        print(f"My {krw_ticker} balance is : ", ticker_balance)

        ticker_price = cmt.get_current_price(krw_ticker)
        print(f"Current {krw_ticker} Price is : ", ticker_price)

        ## Get ticker price data and calculate MA

        while True:
            try:
                df = cmt.get_ohlcv(krw_ticker, count = 200, interval = 'minute10')#####################################################################time
        
                if df is None:
                    print("UPBIT API Error while executing get_ohlcv function")
                    time.sleep(0.5)
                    pass
                else:
                    break

            except:
                print("UPBIT API Error while executing get_ohlcv function")
                time.sleep(0.5)
                pass

        
        df['MA12'] = df['close'].rolling(window= 12, center=False).mean()
        df['MA26'] = df['close'].rolling(window= 26, center=False).mean()
    
        ##----- Plotting ------

        # make_plot(df)
        # plt.pyplot.close('all')

        ##----- Plotting ------

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

            # buy_coin = cmt.buy_market_order(myAPI, 'KRW-BTC', buy_amount_KRW) ## 시장가 매수
            try:
                buy_coin = cmt.buy_market_order(myAPI, krw_ticker, 6000) ## 시장가 매수

            except:
                print("An error occured while executing cmt.buy_market_order function")
                pass
            
            msg_update = (f"Signal : {krw_ticker} Gold Cross Detected, 시장가 매수 진행 \n"
                        f"Current Time : {dt.datetime.today().strftime('%m-%d %H:%M')} \n") 

            print(msg_update)

            if activate_bot:
                bot.sendMessage(chat_id, text = msg_update)       

        elif GC == 0 and DC == 1:

            try:
                ticker_balance = myAPI.get_balance(krw_ticker)

            except:
                print("An error occured while executing myAPI.get_balance(krw_ticker) function")
                pass

            if (ticker_balance is None):
                print(f'{krw_ticker}_balance is NONE, pass')
            else:

                ## 수익율 확인, 2% 이상에서만 매도 진행
                Sell_amount = ticker_balance * ticker_price
                Invest_remain = Invest_remain + Sell_amount
                
                
                try:
                    sell_coin = cmt.sell_market_order(myAPI, krw_ticker, 0.9) ## Sell all balance

                except:
                    print("An error occured while executing cmt.sell_market_order function")
                    pass
                
                ## Tracking remaining investment fund
                
                

                msg_update = (f"Signal : {krw_ticker} Dead Cross Detected, 시장가 매도 진행 \n"
                            f"Current Time : {dt.datetime.today().strftime('%m-%d %H:%M')} \n") 

                print(msg_update)

                if activate_bot:
                    bot.sendMessage(chat_id, text = msg_update)              
        else:
            print('No Signal detected #2')        

    # print('Checkpoint #3')
    ## 6. Sleep until the next round, 10 sec sleep loop until the target_time

    for z in range(10 * 6): # n * 6 --> will pause for n minutes
        time.sleep(10) #seconds

    # time_diff_min = calculate_time_diff()
    # print(time_diff_min,"minutes until the next calculation round")
    # for z in range(time_diff_min * 6): # min * 6 --> in 10 secs
    #     time.sleep(10) #seconds


