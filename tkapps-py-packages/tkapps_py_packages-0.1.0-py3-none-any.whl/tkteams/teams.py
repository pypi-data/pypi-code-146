import os
import requests
from .message import Message

class Teams():
    def __init__(self, webhook_url=None):
        """
        :param webhook_url: The Webhook url from the teams
        """
        if webhook_url is None:
            try:
                webhook_url = os.environ["WEBHOOK_URL"]
            except Exception:
                raise ValueError("WEBHOOK_URL is missing in both ENV Variable and constructor params.")
        self.webhook_url = webhook_url
        self.http_timeout = 60

    def change_webhook(self, new_webhook):
        """
        :param new_webhook: the new webhook that will replace the older webhook
        :return: none
        """
        self.webhook_url = new_webhook

    def send_to_multiple_channels(self, webhooks_list, message):
        """
        :param webhooks_list: The list of webhooks where the message will be sent.
        :param message: The message that will be posted across all the channels.
        :return: None
        """
        for webhook_url in webhooks_list:
            self.webhook_url = webhook_url
            self.send_message(message)

    def _validate_message(self, message):
        """
        :param message: The message that is to be sent to the teams channel should be of type Message
        :return: Boolean
        """
        if type(message) != type(Message()):
            raise ValueError("Object not of type Message")
        if 'text' not in message.data:
            raise ValueError("Message is empty!")
        return True

    def send_message(self, message):
        """
        :param message: The message that is to be sent to the teams channel should be of type Message
        :return: Boolean (Status of message)
        """
        # self._validate_message(message)
        headers = {"Content-Type": "application/json"}
        r = requests.post(
            self.webhook_url,
            json=message.message,
            headers=headers,
            timeout=self.http_timeout,
        )
        self.last_http_response = r
        if r.status_code == requests.codes.ok:  # pylint: disable=no-member
            return True
        else:
            print(r.text)
            raise r.raise_for_status()