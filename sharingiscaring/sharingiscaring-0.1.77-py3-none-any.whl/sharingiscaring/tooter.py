from apprise import Apprise
from enum import Enum
import json
from urllib.request import Request
import requests

class TooterType(Enum):
    INFO = "info"
    GRAPHQL_ERROR = "graphql error"
    MONGODB_ERROR = "mongodb error"
    REQUESTS_ERROR = "requests error"
    BOT_MAIN_LOOP_ERROR = "bot_main_loop_error"
    

class TooterChannel(Enum):
    BOT = 'bot'
    NOTIFIER = 'notifier'

class Tooter:
    def __init__(self, environment: str, branch: str, 
            NOTIFIER_API_TOKEN: str, BOT_API_TOKEN: str, FASTMAIL_TOKEN: str
            ) -> None:
        # self.appriser           = appriser
        self.environment        = environment
        self.branch             = branch
        self.NOTIFIER_API_TOKEN = NOTIFIER_API_TOKEN
        self.BOT_API_TOKEN      = BOT_API_TOKEN
        self.FASTMAIL_TOKEN     = FASTMAIL_TOKEN
        self.url                = "https://tooter.concordium-explorer.nl/notify/"
        self.email_part_1       = "mailto://fastmail.com/?to="
        self.email_part_2       = f"&user=sdr@16april1973.nl&pass={FASTMAIL_TOKEN}&from=Concordium Explorer Bot&from=bot@concordium-explorer.nl"

    def email(self, title: str, body: str, email_address: str, value=None, error=None):
        payload = {
            'urls': f"{self.email_part_1}{email_address}{self.email_part_2 }",
            'title': title,
            'body': body,
        }
        r = requests.post(self.url, json=payload)
        
    
    def relay(self, 
        channel: TooterChannel, 
        body: str, 
        notifier_type: TooterType, 
        title: str, 
        chat_id: int=None, 
        value=None, 
        error=None, 
        bcc = False
        ):
        API_TO_USE = self.BOT_API_TOKEN if channel == TooterChannel.BOT else self.NOTIFIER_API_TOKEN
        chat_id = '913126895' if channel == TooterChannel.NOTIFIER else chat_id

        payload = {
            'urls': f'tgram://{API_TO_USE}/{chat_id}',
            'title': title,
            'body': body,
            'format': 'html'
        }
        r = requests.post(self.url, json=payload)

        if bcc:
            payload = {
                'urls': f'tgram://{self.NOTIFIER_API_TOKEN}/913126895',
                'title': f"{title} | to: {chat_id}",
                'body': body,
                'format': 'html'
            }
            r = requests.post(self.url, json=payload)
    
        
    def send(self, channel: TooterChannel, message: str, notifier_type: TooterType, chat_id: int=None, value=None, error=None):
        API_TO_USE = self.BOT_API_TOKEN if channel == TooterChannel.BOT else self.NOTIFIER_API_TOKEN
        chat_id = '913126895' if channel == TooterChannel.NOTIFIER else chat_id

        title   = f"t: {notifier_type.value} | e: {self.environment} | b: {self.branch}"
        body    = message
        if value:
            body += '| value: {value} '
        if error:
            body += '| error: {error}.' 

        payload = {
            'urls': f'tgram://{API_TO_USE}/{chat_id}',
            'title': title,
            'body': body,
            'format': 'html'
        }
        r = requests.post(self.url, json=payload)
        