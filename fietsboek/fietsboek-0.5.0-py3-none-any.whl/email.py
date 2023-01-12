"""Utility functions for email sending."""
import logging
import smtplib
import sys
from email.message import EmailMessage
from typing import Optional
from urllib.parse import urlparse

LOGGER = logging.getLogger(__name__)


def prepare_message(sender: str, addr_to: str, subject: str) -> EmailMessage:
    """Prepares an email message with the right headers.

    The body of the message can be set by using
    :meth:`~email.message.EmailMessage.set_content` on the returned message.

    :param sender: The email sender.
    :param addr_to: Address of the recipient.
    :param subject: Subject of the message.
    :return: A prepared message.
    """
    message = EmailMessage()
    message["To"] = addr_to
    if "<" not in sender and ">" not in sender:
        message["From"] = f"Fietsboek <{sender}>"
    else:
        message["From"] = sender
    message["Subject"] = subject
    return message


def send_message(
    server_url: str, username: Optional[str], password: Optional[str], message: EmailMessage
):
    """Sends an email message using the STMP server configured in the settings.

    The recipient is taken from the 'To'-header of the message.

    :param server_url: The URL of the server for mail sending.
    :param username: The username to authenticate, can be ``None`` or empty.
    :param password: The password to authenticate, can be ``None`` or empty.
    :param message: The message to send.
    """
    parsed_url = urlparse(server_url)
    if parsed_url.scheme == "debug":
        print(message, file=sys.stderr)
        return
    hostname = parsed_url.hostname if parsed_url.hostname is not None else "localhost"
    try:
        # Use 0 to let smtplib pick the default port
        if parsed_url.scheme == "smtp":
            client = smtplib.SMTP(hostname, parsed_url.port or 0)
        elif parsed_url.scheme == "smtp+ssl":
            client = smtplib.SMTP_SSL(hostname, parsed_url.port or 0)
        elif parsed_url.scheme == "smtp+starttls":
            client = smtplib.SMTP(hostname, parsed_url.port or 0)
            client.starttls()
        if username and password:
            client.login(username, password)
        client.send_message(message)
        client.quit()
    except smtplib.SMTPException:
        LOGGER.error("Error when sending an email", exc_info=sys.exc_info())
