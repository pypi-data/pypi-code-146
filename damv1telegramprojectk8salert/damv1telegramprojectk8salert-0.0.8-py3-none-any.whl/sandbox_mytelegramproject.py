import requests as requests
import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q

class sanbox():
  def sendmessage_telegram(self,_telemsg=None):
      resp_msg = None
      try:
        resp_msg = requests.post(env.sandbox_telegram.apiURL.value, json={"parse_mode": "MarkdownV2",'chat_id': env.sandbox_telegram.chatID.value, 'text': _telemsg})
        if '<Response [200]>' in resp_msg:
          Q.logger(time7.currentTime7(),f'             {str(resp_msg)}')
        else:
          Q.logger(time7.currentTime7(),f'             {str(resp_msg)} - Successfully send message to Telegram ( せいこうした )')
      except Exception as e:
        Q.logger(time7.currentTime7(),'Fail of function "sendmessage_telegram"')  
        Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
      return resp_msg
