import requests
import time
import platform
import os
from flask import Flask,render_template
from threading import Thread
import datetime
api_url = "https://alice-api.space"
member_view = 0
time_online = 0

def print_notice(text):
  print(f"[Alice Notice] {text}")

def clear_console():
  if platform.system() == 'Windows':
    os.system("cls")
    print("Cleared console")
  else:
    os.system("clear")
    print("Cleared console")
import time, threading

StartTime=time.time()

class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()

    def cancel(self) :
        self.stopEvent.set()


class host:
  def run():
    app = Flask('')
    
    @app.route('/')
    def home():
      global member_view, time_online
      
      member_view = member_view+1
      return f"Alice Host Status: Visitor: {member_view} Time: {str(datetime.timedelta(seconds=time_online))}"

    print_notice("Host is opening..")
    def run():
      def add_timeonline():
        global member_view, time_online
        time_online = time_online+1
        time.sleep(1.0)
        
      setInterval(1.0, add_timeonline)
      app.run(host='0.0.0.0',port=8080)
    
    run()
    



class sms:
  def send(phone, amount):
    global api_url

    print_notice("Connecting to gateway")
    gateway = requests.get(f"{api_url}/api/status").json()
    time.sleep(1.0)
    if gateway['status'] == 'busy':
      print_notice("Gateway is busy, please try again later.")
    else:
      print_notice("Gateway is ready!, sending request to api!")
      
      if amount.isnumeric() and int(amount) < 20:
        if phone.isnumeric():
          print_notice("Receiving gateway...")
          time.sleep(2.5)

          i = 0
          while i < int(amount):
            result = get_gateway(f"sms/{phone}").json()
            if result['Status:'] == "Attack done !!":
              i = i+1
              amount_removed = int(amount)-i

              print_notice(f"Sended request to api! | {amount_removed} more remaining")
            else:
              amount_removed = int(amount)-i

              print_notice(f"Error request to api! | {amount_removed} more remaining")
          print_notice("Gateway said success send, now gateway is ready!")
          print_notice("Disconnecting gateway...")
          time.sleep(3.0)
          print_notice("Goodbye!")
          time.sleep(3.0)
          clear_console()
        else:
          print_notice("Receiving gateway...")
          time.sleep(2.5)
          print_notice("Gateway is error, phone is incorrect! please check your phone number and do it again later.")
          print_notice("Disconnecting gateway...")
          time.sleep(3.0)
          print_notice("Goodbye!")
          time.sleep(3.0)
          clear_console()
      else:
        print_notice("Receiving gateway...")
        time.sleep(2.5)
        print_notice("Gateway is error, amount to send is incorrect! please check your amount to send and do it again later.")
        print_notice("Disconnecting gateway...")
        time.sleep(3.0)
        print_notice("Goodbye!")
        time.sleep(3.0)
        clear_console()

def find_truewalletgift(string):
    if string.startswith("https://gift.truemoney.com/campaign/?v=") or string.startswith("https://gift.truemoney.com/campaign/?v="):
      return True
    else:
      return False

class truewallet:
  def send(phone, link):
    if phone.isnumeric() and len(phone) == 10:
      if find_truewalletgift(link):
        link_gift = link.replace("https://gift.truemoney.com/campaign/?v=", "")
        json_gift = {
          "mobile": f"{phone}",
          "voucher": f"{link_gift}"
        }
        headers = {
          "Content-Type": "application/json",
          "User-Agent": "multilabxxxxxxxx"
        }
        response = requests.post("https://voucher.meowcdn.xyz/api", headers=headers, json=json_gift)
        
        try:
          return response.json()
        except:
          return {'status': {'message': "Voucher doesn't exist.", 'code': 'VOUCHER_NOT_FOUND'}, 'data': None}
      else:
        return {'status': {'message': "Voucher gift is incorrect.", 'code': 'VOUCHER_GIFT_INCORRECT'}, 'data': None}
    else:
     return {'status': {'message': "Phone number is incorrect.", 'code': 'PHONEN_INCORRECT'}, 'data': None}