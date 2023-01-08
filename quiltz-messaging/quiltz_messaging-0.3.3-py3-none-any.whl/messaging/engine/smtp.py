from smtplib import SMTP, SMTPDataError
from email.message import EmailMessage
from quiltz.domain.results import Success, Failure, PartialSuccess
import ssl
import logging


class NoMessageEngine:
    def commit(self, messenger):
        pass


class SMTPBasedMessageEngine:
    @staticmethod
    def from_config(config):
        if config.FOR_TEST:
            return SMTPBasedMessageEngineForTest(config.SMTP_HOST, config.SMTP_PORT, None, None)
        else:
            return SMTPBasedMessageEngine(config.SMTP_HOST, config.SMTP_PORT, config.SMTP_USER, config.SMTP_PASSWORD)
        
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password 
        self.logger = logging.getLogger(self.__class__.__name__)

    def login(self, smtp):
        smtp.login(self.user, self.password)

    def create_ssl_context(self):
        return ssl.create_default_context()

    def commit(self, messenger):
        try:
            with SMTP(self.host, self.port) as smtp:
                smtp.starttls(context=self.create_ssl_context())
                self.login(smtp)
                return self.send(smtp, messenger.messages)
        except ConnectionError as e:
            return Failure(message=str(e))

    def send(self, smtp, messages):
        failed_messages = []
        successful_messages = []
        for message in messages:
            try:
                smtp.send_message(msg=as_smtp_message(message))
                successful_messages.append(message)
            except SMTPDataError as e:
                self.logger.warning('Failed sending message to {}: [{}] {}'.format(message.to.anonymized,
                                                                                   e.smtp_code,
                                                                                   e.smtp_error.decode('utf-8')))
                failed_messages.append(message)
        self.logger.info('Flushed messages to {}'.format(", ".join([m.to.anonymized for m in successful_messages])))
        return self.to_result(successful_messages, failed_messages)

    def to_result(self, successful_messages, failed_messages):
        if len(failed_messages) == 0: return Success()
        message = 'Sending messages failed for: {}'.format(', '.join([m.recipient for m in failed_messages]))
        if len(successful_messages) != 0:
            message += ' and succeeded for: {}'.format(', '.join([m.recipient for m in successful_messages]))
        return PartialSuccess(message=message)


class SMTPBasedMessageEngineForTest(SMTPBasedMessageEngine):
    def login(self, smtp):
        pass

    def create_ssl_context(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context


def as_smtp_message(message):
    email_message = EmailMessage()
    email_message['To'] = message.recipient
    email_message['From'] = message.sender
    email_message['Subject'] = message.subject
    email_message.set_content(message.body)
    return email_message
