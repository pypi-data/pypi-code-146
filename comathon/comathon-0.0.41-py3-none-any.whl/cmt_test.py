import requests
import pyupbit


## Checking code_status
import socket 

def code_status():
    
    is_server = False

    my_IP = socket.gethostbyname(socket.gethostname())
    print("my IP address : ", my_IP)

    server_IP = '121.137.95.97'
    dev_IP = '175.207.155.229'
    dev_IP_laptop = '192.168.213.94'

    if my_IP == server_IP or my_IP == dev_IP_laptop or my_IP == dev_IP:
        print("The code is being run by the server or Jeong's computer")
        is_server = True
    
    else:
        print("The code is being run on a personal computer")
        print("is_server variable : ", is_server)

    return is_server


def bot_mapping(API):
    ## Bot List
    url = "http://121.137.95.97:8889/BotList"
    response = requests.get(url)
    response = response.json()
    print(response)

    ## Find the botid that matches my ID
    ## Then create a string url using that botid

    get_bots = list(response.items())[2][1]
    get_bots

    num_bots = len(get_bots)
    print("Number of active bots : ", num_bots)
    print("my user ID is :", API.ID)
    for i in get_bots:
        save_ID = i['makerid']
        save_botid = i['botid']

        print(save_ID, save_botid)

        if save_ID == API.ID:
            bot_connect = save_botid
            print("the user will be mapped to the bot : ", bot_connect)
            url = "http://121.137.95.97:8889/BotWithinUserList?botid=" + bot_connect
            print(url)
        else:
            print("not this bot")

    return url

## Buy Function
def buy_market_order(API, ticker, amount):
    ## API = Upbit API instance --> need it to map to the dedicated BOT

    print("Buy Function Activated")    
    is_server = code_status()
    
    ## If the code is being run on a PC, then proceed as normal
    if is_server == False:
        print("is_server is False, hence buy only user's")
        KRW_balance = API.get_balance()
        print("Balance : ", KRW_balance)
        API.buy_market_order_single(ticker, amount) ## This needs separate treatment
        print("ticker : ", ticker, "Purchased Amount : ", amount)

    ## If the code is being run on the server
    else:
        print("is_server is True, hence run through all the users in the server")

        ## This is where we need to map USER to the BOT Name

        ## find the bot that is mapped to the user API.ID
        # url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
        url = bot_mapping(API)
        response = requests.get(url)
        response = response.json()
        # response

        ## List of users in [2] followed by [1] index, spit out a list
        get_users = list(response.items())[2][1]

        num_users = len(get_users)
        print("Number of Users : ", num_users)

        for i in get_users:
            print("User ID : ", i['userid'])
            print("Access Key : ", i['apikey'])
            print("Secret Key : ", i['securitykey'])
            access_key = i['apikey']
            secret_key = i['securitykey']

            user_upbit = pyupbit.Upbit(access_key, secret_key)  # cmt과 다른 모듈이 필요
            
            KRW_balance = user_upbit.get_balance("KRW")
            print(i['userid'], "Balance : ", KRW_balance)

            user_upbit.buy_market_order(ticker, amount)
            print(i['userid'], "ticker : ", ticker, "Purchased Amount : ", amount)
               

    return None


def sell_market_order(API, ticker, fraction):

    ## API = Upbit API instance --> need it to map to the dedicated BOT

    print("Sell Function Activated")
    is_server = code_status()

        ## If the code is being run on a PC, then proceed as normal
    if is_server == False:
        print("is_server is False, hence buy only user's")
        coin_balance = API.get_balance(ticker)
        print("ticker :", ticker, "ticker Balance : ", coin_balance)
        
        ## coin_balance가 None일때 exception 처리 필요
        if coin_balance == None:
            print("Coin Balance is None, cannot proceed")
        else:
            API.sell_market_order_single(ticker, coin_balance * fraction) ## This may need separate treatment
            print("ticker : ", ticker, "Sold Amount : ", coin_balance * fraction)

    ## If the code is being run on the server
    else:
        print("is_server is True, hence run through all the users in the server")

        ## This is where we need to map USER to the BOT Name
        ## find the bot that is mapped to the user API.ID
        # url = "http://121.137.95.97:8889/BotWithinUserList?botid=BOT002"
        url = bot_mapping(API)
        response = requests.get(url)
        response = response.json()
        # response

        ## List of users in [2] followed by [1] index, spit out a list
        get_users = list(response.items())[2][1]

        num_users = len(get_users)
        print("Number of Users : ", num_users)

        for i in get_users:
            print("User ID : ", i['userid'])
            print("Access Key : ", i['apikey'])
            print("Secret Key : ", i['securitykey'])
            access_key = i['apikey']
            secret_key = i['securitykey']

            user_upbit = pyupbit.Upbit(access_key, secret_key)  # API 로그인 함수 호출
            # KRW_balance = user_upbit.get_balance()
                            
            coin_balance = user_upbit.get_balance(ticker)
            print(i['userid'], "ticker : ", ticker, "ticker Balance : ", coin_balance)
            if coin_balance == None:
                print("Coin Balance is None, cannot proceed")
            else:
                ## coin_balance가 None일때 exception 처리 필요
                user_upbit.sell_market_order(ticker, coin_balance * fraction) ## Sell total_balance * fraction
                # upbit.sell_market_order(ticker, coin_balance) ## Sell total_balance * fraction
                
                coin_balance_updated = user_upbit.get_balance(ticker)

                print(i['userid'], "ticker : ", ticker, "new ticker Balance : ", coin_balance_updated)


    return None



