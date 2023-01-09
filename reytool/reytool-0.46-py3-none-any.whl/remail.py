# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:10:19
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's E-mail type
"""


from typing import Dict, Iterable, Optional, Union
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .rbasic import get_first_notnull


class REmail(object):
    """
    Rey's E-mail type.
    """

    def __init__(
        self,
        email_user: Optional[str] = None,
        email_password: Optional[str] = None,
        title: Optional[str] = None,
        text: Optional[str] = None,
        attachment: Optional[Dict[str, Union[str, bytes]]] = None,
        to_email: Optional[Union[str, Iterable]] = None,
        cc_email: Optional[Union[str, Iterable]] = None,
        display_from_email: Optional[str] = None,
        display_to_email: Optional[Union[str, Iterable]] = None,
        display_cc_email: Optional[Union[str, Iterable]] = None
    ) -> None:
        """
        Set E-mail attribute.
        """

        self.email_user = email_user
        self.email_password = email_password
        self.title = title
        self.text = text
        self.attachment = attachment
        self.to_email = to_email
        self.cc_email = cc_email
        self.display_from_email = display_from_email
        self.display_to_email = display_to_email
        self.display_cc_email = display_cc_email

    def create_email(
        self,
        title: Optional[str] = None,
        text: Optional[str] = None,
        attachment: Optional[Dict[str, Union[str, bytes]]] = None,
        display_from_email: Optional[str] = None,
        display_to_email: Optional[Union[str, Iterable]] = None,
        display_cc_email: Optional[Union[str, Iterable]] = None
    ) -> str:
        """
        Create string in E-mail format.
        """

        title = get_first_notnull(title, self.title)
        text = get_first_notnull(text, self.text)
        attachment = get_first_notnull(attachment, self.attachment)
        display_from_email = get_first_notnull(display_from_email, self.display_from_email, self.email_user)
        display_to_email = get_first_notnull(display_to_email, self.display_to_email, self.to_email)
        display_cc_email = get_first_notnull(display_cc_email, self.display_cc_email, self.cc_email)
        mime = MIMEMultipart()
        if title != None:
            mime["subject"] = title
        if text != None:
            mime_text = MIMEText(text)
            mime.attach(mime_text)
        if attachment != None:
            for file_name, file_data in attachment.items():
                if type(file_data) == str:
                    with open(file_data, "rb") as f:
                        file_data = f.read()
                mime_file = MIMEText(file_data, _charset="utf-8")
                mime_file.add_header("content-disposition", "attachment", filename=file_name)
                mime.attach(mime_file)
        if display_from_email != None:
            mime["from"] = display_from_email
        if display_to_email != None:
            if type(display_to_email) == str:
                mime["to"] = display_to_email
            else:
                mime["to"] = ",".join(display_to_email)
        if display_cc_email != None:
            if type(display_cc_email) == str:
                mime["cc"] = display_cc_email
            else:
                mime["cc"] = ",".join(display_cc_email)
        email_str = mime.as_string()
        return email_str
        
    def send_email(
        self,
        email_user: Optional[str] = None,
        email_password: Optional[str] = None,
        title: Optional[str] = None,
        text: Optional[str] = None,
        attachment: Optional[Dict[str, Union[str, bytes]]] = None,
        to_email: Optional[Union[str, Iterable]] = None,
        cc_email: Optional[Union[str, Iterable]] = None,
        display_from_email: Optional[str] = None,
        display_to_email: Optional[Union[str, Iterable]] = None,
        display_cc_email: Optional[Union[str, Iterable]] = None
    ) -> None:
        """
        Send E-mail.
        """

        email_user = get_first_notnull(email_user, self.email_user, default="error")
        email_password = get_first_notnull(email_password, self.email_password, default="error")
        title = get_first_notnull(title, self.title)
        text = get_first_notnull(text, self.text)
        attachment = get_first_notnull(attachment, self.attachment)
        to_email = get_first_notnull(to_email, self.to_email, default="error")
        cc_email = get_first_notnull(cc_email, self.cc_email)
        display_from_email = get_first_notnull(display_from_email, self.display_from_email, email_user)
        display_to_email = get_first_notnull(display_to_email, self.display_to_email, to_email)
        display_cc_email = get_first_notnull(display_cc_email, self.display_cc_email, cc_email)
        
        if type(to_email) == str:
            to_email = [to_email]
        if cc_email != None:
            if type(cc_email) == str:
                to_email.append(cc_email)
            else:
                to_email.extend(cc_email)
        email_str = self.create_email(title, text, attachment, display_from_email, display_to_email, display_cc_email)
        server_domain_name = email_user.split("@")[-1]
        server_host = "smtp." + server_domain_name
        server_port = 25
        smtp = SMTP(server_host, server_port)
        smtp.login(email_user, email_password)
        smtp.sendmail(email_user, to_email, email_str)
        smtp.quit()