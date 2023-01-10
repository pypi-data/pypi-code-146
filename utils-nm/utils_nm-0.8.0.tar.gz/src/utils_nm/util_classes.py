# util_classes.py
# -*- coding: utf-8 -*-

"""
Classes which serve for general purposes
"""

import time

import logging

import ssl
import smtplib
from email.message import EmailMessage


# ______________________________________________________________________________________________________________________


class StartTime:
    called = False

    @classmethod
    def show(cls, logger: logging.Logger) -> None:
        if not cls.called:
            logger.info('____________________________________________________________')
            logger.info(f'>> Execution started at {time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())} <<')
            cls.called = True
        return None


# ______________________________________________________________________________________________________________________


class Email:
    def __init__(self, server: str, port: int, address: str, password: str | None, logger: logging.Logger):
        self.server = server
        self.port = port
        self.address = address
        self.password = password
        self.logger = logger

    def send_email(
            self, mail_to: str | list, subject: str, body: str, html: bool = False, use_ssl: bool = True
    ) -> None:
        """
        sending the email

        Args:
            mail_to: receiver, can be a list of strings
            subject: the subject of the email
            body: the body of the email
            html: whether the body is formatted with html or not
            use_ssl: whether to use a secure ssl connection and authentication

        Returns:
            None
        """
        if not isinstance(mail_to, str):
            mail_to = ', '.join(mail_to)

        if self.server == 'localhost':
            with smtplib.SMTP(self.server, self.port) as server:
                message = f'Subject: {subject}\n\n{body}'
                try:
                    server.sendmail(self.address, mail_to, message)
                    return None
                except smtplib.SMTPException as ex:
                    self.logger.exception('an error occurred!')
                    raise ex
        else:
            mail = EmailMessage()
            mail['Subject'] = subject
            mail['From'] = self.address
            mail['To'] = mail_to
            if html:
                mail.add_alternative(body, subtype='html')
            else:
                mail.set_content(body)

        if use_ssl:
            with smtplib.SMTP_SSL(self.server, self.port, context=ssl.create_default_context()) as server:
                server.login(self.address, self.password)
                server.send_message(mail)
        else:
            with smtplib.SMTP(self.server, self.port) as server:
                server.send_message(mail)

        return None


# ______________________________________________________________________________________________________________________
