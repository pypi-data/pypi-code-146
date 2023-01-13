from typing import List, Optional

import telebot
from requests import Response


class BotTelegramPlugin:
    def __init__(self, token: str) -> None:
        """
        BotTelegramPlugin

        Args:
            token (str): Authentication bot token.
        """
        self._bot = telebot.TeleBot(token=token)

    @property
    def bot(self):
        """
        Telegram bot instance.

        Returns:
            bot: The telegram bot instance.
        """
        return self._bot

    def _find_chat_id(self, group: str) -> str:
        objs = self.bot.get_updates()

        for object in objs:
            obj = object.__dict__
            message = obj["message"]
            if message is not None and message.chat is not None:
                if message.chat.title == group:
                    return message.chat.id
        return None

    def _user_for_mentions(self, username: List[str]) -> str or List[str]:
        if not username:
            return ""
        for user in username:
            if user is not None:
                return " ".join(username)

    def send_message(self, text: str, group: str, username: Optional[List[str]] = None) -> Response:
        """
        Sends a message.

        Args:
           text (str): The text of message.
           group (str): Public or private group to send message to.
           username (List[str], optional): The usernames for mentions.

        Returns:
           response: send message response.
        """
        return self.bot.send_message(text=f'{self._user_for_mentions(username=username)} {text}',
                                     chat_id=self._find_chat_id(group=group))

    def edit_message(self, text: str, response: Response, username: Optional[List[str]] = None) -> Response:
        """
        Update the message based on the response passed as argument.

        Args:
            text (str): The new text for message update.
            response (Response): The response of sended message.
            username (List[str], optional): The usernames for mentions.
        Returns:
            response: edit message response.
        """
        return self.bot.edit_message_text(text=f'{self._user_for_mentions(username=username)} {text}',
                                          message_id=response.message_id,
                                          chat_id=self._find_chat_id(group=response.chat.title))

    def delete_message(self, response: Response) -> Response:
        """
        Deletes the message based on the response passed as argument.

        Args:
            response (Response): The response of sended message.
        Returns:
            response: delete message response.
        """
        return self.bot.delete_message(chat_id=self._find_chat_id(group=response.chat.title),
                                       message_id=response.message_id)

    def upload_document(self, document: str, group: str, caption: Optional[str]) -> Response:
        """
        Upload document to group telegram.

        Args:
            document (str): The document path.
            group (str): Public or private group to send message.
            caption (str, optional): the document caption.
        Returns:
            response: upload document response.
        """
        with open(document, "rb") as file:
            return self.bot.send_document(document=file, chat_id=self._find_chat_id(group=group), caption=caption)
