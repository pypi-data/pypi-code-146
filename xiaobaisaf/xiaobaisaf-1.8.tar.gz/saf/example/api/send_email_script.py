#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : send_email_script.py
'''

from xiaobaiauto2.utils.xiaobaiauto2Email import xemail
from saf.example.api.Config.config import email


user = xemail(smtp_server=email.smtp(),
               smtp_port=email.port(),
               username=email.username(),
               password=email.password())

user.send(to=email.to(),
          subject=email.subject(),
          content=email.content(),
          files=email.files())