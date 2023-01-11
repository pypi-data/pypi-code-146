import requests
import json
import re
import base64
from uuid import uuid4
from pathlib import Path
from loguru import logger
from typing import Union

from .utils.ut import Utils

class Email:

    def __init__(self, core: object) -> None:
        global client
        client = core

        self.raiseException = client.raiseException
        self.defaults = core.defaults
        self.structure = core.structure
        self.scheme = core.scheme

        self.header = {
            'Authorization': f'Bearer {client.accessToken}',
            'AcceptEncoding': 'deflate',
            'Accept': 'application/json',
            'Content-type': 'application/json',
            }

        self.baseUrl = f'https://{client.host}/emailservice/Email'

        return

    def sendMail(
        self,
        to:Union[str,list],
        cc:Union[str,list]=None,
        bcc:Union[str,list]=None,
        subject:str=None,
        textBody:str=None,
        htmlBody:str=None,
        attachments:Union[str,list]=None
        ) -> None:
        """
        Sends an email via the TechStack email service.

        Parameters:
        ----------
        to: str|list
            One or more recipient addresses.
        cc: str|list = None
            One or more recipient addresses in CC.
        bcc: str|list = None
            One or more recipient addresses in BCC.
        subject: str = None
            The email subject.
        textBody: str = None
            The text body of the email.
        htmlBody: str = None
            A HTML body of the email. Not, if both textBody and htmlBody are used,
            only the htmlBody will be sent.
        attachments: str|list = None
            Provide one or more file paths to attach files to the email.

        Examples:
        >>> sendMail('gustav@mail.com', cc=['annette@mail.com', carl@mail.com], subject='Hello', textBody=text)
        >>> sendMail('gustav@mail.com', attachments=['report.pdf', 'data.xlsx']
        """

        correlationId = str(uuid4())

        if isinstance(to, str): to = [to]
        if isinstance(cc, str): cc = [cc]
        if isinstance(bcc, str): bcc = [bcc]
        if isinstance(attachments, str): attachments = [attachments]

        address_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        for group in [to, cc, bcc]:
            if not group: continue
            for address in group:
                if not re.fullmatch(address_regex, address):
                  Utils._error(self, f"Invalid email address '{address}'.", correlationId)
                  return

        _attachments = []
        if attachments:
            for filepath in attachments:
                if not Path(filepath).exists():
                    Utils._error(self, f"File path '{filepath}' is not correct.", correlationId)
                    return
                with open(Path(filepath), 'rb') as file:
                  content = base64.b64encode(file.read()).decode('utf-8')
                  _attachments.append({'filename':Path(filepath).name, 'content':content})

        data = {
            'to': to,
            'subject': subject,
            'textBody': textBody,
            'htmlBody': htmlBody,
            'cc': cc,
            'bcc': bcc,
            'attachments': _attachments
            }

        data=json.dumps(data)

        with logger.contextualize(correlation_id=correlationId):
            response = requests.post(url=self.baseUrl, headers=self.header, data=data)
            if response.status_code > 400:
                logger.info(f'Email service not available. Response status {response.status}.')
            if response.status_code == 200:
                logger.info(f'Email sent to {to}.')

        return
