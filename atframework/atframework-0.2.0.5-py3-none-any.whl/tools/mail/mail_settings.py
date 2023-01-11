# -*- coding: utf-8 -*-
# @Time : 2021/8/2 18:18
# @Author : Siro
# @File : mail_settings.py
# @Software: PyCharm

class MailSettings(object):

    PORT = 465
    SMTP_SERVER_DOMAIN_NAME = "smtp.gmail.com"
    SENDER_EMAIL = "siro7test@gmail.com"
    SENDER_PASSWORD = "Ss7777777"

    MAIL_HTML_TEMPLATE = """
                    <h1>Test Report for {0}</h1>

                    <p>Hi {1},</p>
                    <p> Have a good day! The automation testing report is generated.</p>
                    <p> <b>Testing type: </b>{2}</p>
                    <p> <b>Testing site: </b>{3}</p>
                    """
    MAIL_SUBJECT = "Automation Test Report of {testing_type}"
    RECEIVER_EMAILS = ['sirodeng@gmail.com', 'siro@foxmail.com']


