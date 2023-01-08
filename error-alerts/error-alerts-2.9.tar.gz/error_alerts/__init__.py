import traceback
from telegram import Bot

class setup:
    def __init__(self, telegram_token, telegram_channel, log=None, full_error=False, raise_error=False, resend_repeat_errors=True):
        self.bot = Bot(token=telegram_token)
        self.channel = telegram_channel
        self.log = log
        self.full_error = full_error
        self.raise_error = raise_error
        self.resend_repeat_errors = resend_repeat_errors
        self.last_error = None
    def send(self, title, exception=None):
        if self.full_error:
            error = traceback.format_exc()
        else:
            error = str(exception)
        message = f'{title}: {error}'
        if error == self.last_error and not self.resend_repeat_errors:
            self.printer(message, level='debug')
        if self.resend_repeat_errors or error != self.last_error:
            self.printer(message, level='error')
            try:
                self.bot.send_message(self.channel, message[:4096])
                self.last_error = error
            except Exception as telegram_error:
                self.printer('Error sending alert message to Telegram:', telegram_error, level='error')
        if self.raise_error:
            raise Exception('Raiser') from exception
    def send_message(self, *messages):
        final_message = ''
        for message in messages:
            final_message += message
            final_message += ' '
        self.printer(final_message)
        try:
            self.bot.send_message(self.channel, final_message[:4096])
        except Exception as telegram_error:
            self.printer('Error sending message to Telegram:', telegram_error, level='error')
    
    def printer(self, *items, level='info'):
        if self.log:
            log(*items, level=level)
            log(level=level)
        elif level != 'debug':
            print(items)
            print()