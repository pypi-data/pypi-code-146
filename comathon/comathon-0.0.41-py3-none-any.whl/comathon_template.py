import comathon as cmt
import requests


## Create UPBIT API Class Instance (업로드 시 삭제)------------------

access_key = "DplIC0dHKeVVjr9RtRhJskZD2xVTkxdQtHno6BpO"
secret_key = "6xV4OlFjLv7P8PoHyuOrRgE1Qk1kmnEfB8Mmzmh4"
comathon_ID = "test001" #현재 test001, tst002, test003 가 등록되어 있음, 수정요청함

# myAPI = cmt.Upbit(access_key, secret_key)  # API 로그인 함수 호출
# myAPI #myAPI 라는 instance가 생성됨

myAPI = cmt.Upbit(access_key, secret_key, comathon_ID)  # API 로그인 함수 호출
myAPI #myAPI 라는 instance가 생성됨
myAPI.get_balance("KRW")
##-------------------------------------------------------------------



## Quotation 코드----------------------------------------------
cmt.get_ohlcv("KRW-ATOM", "day")
cmt.get_current_price("KRW-ATOM")
cmt.get_tickers("KRW")
## -----------------------------------------------------------



## Exchange 코드-----------------------------------------------
#시장가 매수 코드 (API, Ticker, KRW Amount)
cmt.buy_market_order(myAPI, "KRW-ATOM", 5000)

#시장가 매도 코드 (API, Ticker, Fraction between 0 and 1)
cmt.sell_market_order(myAPI, "KRW-ATOM", 1)

##-------------------------------------------------------------


while True:

    check_server = cmt.server_alive(myAPI)
    print("Server Online : ", check_server)


    for z in range(10 * 6): # n * 6 --> will pause for n minutes
        time.sleep(10) #seconds
    # check_profit(myAPI)