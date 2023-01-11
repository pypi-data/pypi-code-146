import traceback
from telegram import Bot

class telegram:
    def __init__(self, token=None, channel=None, log=None, full_error=False, raise_error=False, resend_repeat_errors=True):
        if token:
            self.bot = Bot(token=token)
        self.channel = channel
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
            if self.channel:
                try:
                    self.bot.send_message(self.channel, message[:4096])
                except Exception as telegram_error:
                    self.printer('Error sending alert message to Telegram:', telegram_error, level='error')
            self.last_error = error
        if self.raise_error:
            raise Exception('Raiser') from exception
    def send_message(self, *messages):
        final_message = ''
        for message in messages:
            final_message += message
            final_message += ' '
        self.printer(final_message)
        if self.channel:
            try:
                self.bot.send_message(self.channel, final_message[:4096])
            except Exception as telegram_error:
                self.printer('Error sending message to Telegram:', telegram_error, level='error')
    
    def printer(self, *items, level='info'):
        if self.log:
            self.log(*items, level=level)
            self.log(level=level)
        elif level != 'debug': # Don't print debug only messages
            print(items)
            print()