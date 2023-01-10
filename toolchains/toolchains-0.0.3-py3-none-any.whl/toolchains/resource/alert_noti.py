#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
# import yaml
import inspect
import requests
# from termcolor import cprint

# pip install python-telegram-bot==13.13
# pip install pawnlib
import telegram

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# toolchain 넣을때 남기고
from pawnlib.config.globalconfig import pawnlib_config as pawn
from pawnlib.resource import net
from pawnlib.typing import date_utils
from pawnlib.output import *


def p_log(text, level='info', is_view=False, logging=True):
    cf = inspect.currentframe()
    line_number = cf.f_back.f_lineno
    func_name = cf.f_back.f_code.co_name

    print_color = {
        "info": "green",
        "error": "red",
        "warning": "magenta",
        "debug": "yellow",
    }

    log_text = f'{func_name}.{line_number} | {text}'
    if is_view:
        cprint(log_text, color=print_color[level.lower()])

    if logging:
        if level.lower() == 'info' and pawn.app_logger:
            pawn.app_logger.info(log_text)

        if level.lower() == 'debug' and pawn.app_logger:
            pawn.app_logger.debug(log_text)

        if level.lower() == 'error' and pawn.error_logger:
            pawn.error_logger.error(log_text)


class TelegramManager:
    def __init__(self,
                 token,
                 chat_id=None,
                 chat_title=None,
                 chat_type=None,
                 api_url=f'https://api.telegram.org',
                 conf_path=f"{file.get_real_path(__file__)}/conf",
                 conf_file=f'tm_config.yml'
                 ):
        """
        This class send to telegram messenger

        :param token: Bot Access the Http API token (required)
        :param chat_id: Chatting id ( ex: 123456789 or -100123456789 ) (default: None)
        :param chat_title: Chatting room Title or Name
        :param chat_type: chatting type
        :param api_url: telegram api address

        Example:

            .. code-block:: python
                from alert_noti import TelegramManager

                # If the chat room is Public group, the chat_type is group
                TM = TelegramManager(token=bot_token, chat_type='group')

                # If the chat room is Private group, the chat_type is supergroup
                TM = TelegramManager(token=bot_token, chat_type='supergroup')

                # If the chat room is bot vs user(1:1 chat), the chat_type is private
                TM = TelegramManager(token=bot_token, chat_type='private')

                # If the chat room is channel, the chat_type is channel
                TM = TelegramManager(token=bot_token, chat_type='channel')

                # If you know the chat_id, then chat_type is None and chat_id={chat_id}
                TM = TelegramManager(token=bot_token, chat_id={chat_id}, chat_type=None)

                # Send Message to Telegram
                TM.send_telegram(msg, title=None, send_user_name=None, msg_level=None)
        """

        self.token = token
        self.chat_id = chat_id
        self.chat_title = chat_title
        self.api_url = api_url
        self.conf_path = conf_path
        self.get_updates = None
        self.get_userinfo = None
        self.bot_name = None
        self.user_name = None
        self.request_timeout = 5
        self.chat_type_dict = {
            "group": True,
            "supergroup": True,
            "private": True,
            "channel": True,
        }

        if chat_type:
            self.chat_type = chat_type.lower()
            self.chat_type_check()
        else:
            self.chat_type = None

        self.bot = telegram.Bot(token=self.token) if self.token else None

        if os.path.split(conf_file)[0]:
            if not os.path.isdir(os.path.split(conf_path)[0]):
                os.mkdir(os.path.split(conf_path)[0])
            self.conf_file = conf_file
        else:
            if not os.path.isdir(self.conf_path):
                os.mkdir(self.conf_path)
            self.conf_file = os.path.join(self.conf_path, conf_file)
        p_log(f'config file path : {self.conf_file}', level='debug')

        self.get_config()

    def chat_type_check(self):
        if self.chat_type_dict.get(self.chat_type):
            p_log(f'get chat type : {self.chat_type_dict.get(self.chat_type)}', level='debug')
            return True
        else:
            msg = f'Check please!\n - Telegram type choice the {list(self.chat_type_dict.keys())}' \
                  f'\n - Input chat_type is "{self.chat_type}"'
            p_log(msg, level='error')
            raise ValueError(f"Telegram Chatting Room Type Check Error")

    def get_config(self,):
        is_token_ok = False
        is_title_ok = True
        is_type_ok = True
        config_update = False

        p_log(f'Load to config file : {self.conf_file}', level='debug')
        if not is_file(self.conf_file):
            p_log(f'The config file could not be found, so a new config file is created: {self.conf_file}',
                  level="info")
            self.config_create()

        yaml_config_data = open_yaml_file(filename=self.conf_file)
        for config in yaml_config_data['tm_config']:
            p_log(f'{config}', level='debug')
            if config.get('token') == self.token:
                is_token_ok = True
                for chat_list in config.get('chat_list'):
                    if self.chat_title:
                        is_title_ok = True if chat_list.get('title') == self.chat_title else False
                        p_log(f'chat_title check | {is_title_ok}', level='debug')
                    if self.chat_type:
                        is_type_ok = True if chat_list.get('type') == self.chat_type else False
                        p_log(f'chat_type check | {is_type_ok}', level='debug')
            else:
                is_token_ok = False

        if not is_token_ok:
            p_log(f'The config token value was not found, it is appended to the config token value : {self.token}',
                  level='info')
            self.config_update(add_token=self.token)
            yaml_config_data = open_yaml_file(filename=self.conf_file)

        if not is_title_ok:
            config_update = True

        if not is_type_ok:
            config_update = True

        if config_update:
            p_log(f'\nconfig_update check | {config_update} '
                  f'\n - is_title_ok : {is_title_ok}'
                  f'\n - is_type_ok: {is_type_ok}',
                  level='debug')
            self.config_update(update_chat_list=self.config_create(chat_list_update=True))
            yaml_config_data = open_yaml_file(filename=self.conf_file)

        p_log(f'{yaml_config_data}', level='debug')
        return yaml_config_data

    def config_create(self, token_update=False, chat_list_update=False):
        if not token_update and not chat_list_update:
            p_log(f'Initialize config create...', level='info')

        duplicate_id = False
        bot_name, bot_username = self.get_sender_info()
        p_log(f'Bot_name : {bot_name}, Bot_Username : {bot_username}', level='info')
        chat_list = []
        for i, p_chat in enumerate(self.get_update_info()):
            p_log(f'{p_chat}', level='debug')
            if 'title' in p_chat['chat']:
                title_name = p_chat['chat']['title']
            else:
                title_name = f"{p_chat['chat']['first_name']},{p_chat['chat']['last_name']}"

            for item in chat_list:
                if item['id'] == p_chat['chat']['id']:
                    duplicate_id = True

            if not duplicate_id:
                chat_list.append(
                    {
                        'id': p_chat['chat']['id'],
                        'title': f'{title_name}',
                        'type': p_chat['chat']['type'],
                    }
                )
            duplicate_id = False

        if token_update:
            p_log(f'Add to Token config', level="info")
            update_config = {
                'token': f'{self.token}',
                'user_info': [
                    {'bot_name': f'{bot_name}'},
                    {'user_name': f'{bot_username}'}
                ],
                'chat_list': chat_list
            }
            p_log(f'Add to Token config : {self.token}\n{yaml.dump(update_config)}', level='debug')
            return update_config

        if chat_list_update:
            p_log(f'Update chat_list config : {self.token}\n{yaml.dump(chat_list)}', level='debug')
            return chat_list

        if not token_update and not chat_list_update:
            config_data = {
                'tm_config': [
                    {
                        'token': f'{self.token}',
                        'user_info': [
                            {'bot_name': f'{bot_name}'},
                            {'user_name': f'{bot_username}'}
                        ],
                        'chat_list': chat_list
                    }
                ]
            }

            p_log(yaml.dump(config_data), level='debug')
            write_yaml(self.conf_file, config_data)

    def config_update(self, add_token=None, update_chat_list=None):
        p_log(f'update config....', level='info')
        yaml_config_data = open_yaml_file(filename=self.conf_file)
        if update_chat_list:
            p_log(f'update chat list : {update_chat_list}', level='debug')
            for idx, tm_data in enumerate(yaml_config_data['tm_config']):
                if self.token == tm_data.get('token'):
                    tm_data['chat_list'] = update_chat_list
                    break
        if add_token:
            p_log(f'Add to Telegram Token : {add_token}', level='debug')
            update_config = self.config_create(token_update=True)
            yaml_config_data['tm_config'].append(update_config)

        p_log(yaml_config_data, level='debug')
        write_yaml(self.conf_file, yaml_config_data)

    def get_sender_info(self,):
        try:
            self.get_userinfo = self.bot.getMe()
            p_log(f'Bot module: {self.get_userinfo}', level='debug')
        except telegram.error.NetworkError:
            telegram_api_url = f'{self.api_url}/bot{self.token}/getMe'
            p_log(f'Request URL : {telegram_api_url}', level='debug')
            res = requests.get(telegram_api_url, verify=False, timeout=self.request_timeout)
            self.get_userinfo = res.json()['result']
            p_log(f'Request module: {self.get_userinfo}', level='debug')
            del telegram_api_url

        self.bot_name = self.get_userinfo['first_name']
        self.user_name = self.get_userinfo['username']
        p_log(f'Return Result: Bot name - {self.bot_name} / Bot Username - {self.user_name}', level='debug')
        return self.bot_name, self.user_name

    def get_update_info(self,):
        imsi_dict = None
        get_update_list = []
        try:
            get_update_result = self.bot.getUpdates()
            p_log(get_update_result, level='debug')
            for u in get_update_result:
                if u.message:
                    imsi_dict = eval(f'{u.message}')
                if u.my_chat_member:
                    imsi_dict = eval(f'{u.my_chat_member}')
                if u.channel_post:
                    imsi_dict = eval(f'{u.channel_post}')
                p_log(imsi_dict, level='debug')
                get_update_list.append(imsi_dict)
                del imsi_dict
            p_log(f'Bot Module: {self.get_updates}', level='debug')
        except telegram.error.NetworkError:
            telegram_api_url = f'{self.api_url}/bot{self.token}/getUpdates'
            res = requests.get(telegram_api_url, verify=False, timeout=self.request_timeout)
            get_update_result = res.json()['result']
            for u in get_update_result:
                if u.get('message'):
                    imsi_dict = eval(f'{u.get("message")}')
                if u.get('my_chat_member'):
                    imsi_dict = eval(f'{u.get("my_chat_member")}')
                if u.get('channel_post'):
                    imsi_dict = eval(f'{u.get("channel_post")}')
                p_log(imsi_dict, level='debug')
                get_update_list.append(imsi_dict)
                del imsi_dict
            p_log(f'Requests Module: {self.get_updates}', level='debug')
            del telegram_api_url
        finally:
            p_log(f'\n\n{print_json(get_update_list)}\n', level='debug')
            self.get_updates = get_update_list

        return self.get_updates

    def parser_chat_id(self, data=None):
        chatroom_id = None
        chatroom_title = None
        chatroom_type = None
        is_break = False
        p_log(f'self.chat_title : {self.chat_title} ,self.chat_type : {self.chat_type}', level='debug')

        for p_i, p_data in enumerate(data['tm_config']):
            p_log(p_data, level='debug')
            if p_data['token'] == self.token:
                for c_i, c_data in enumerate(p_data['chat_list']):
                    if self.chat_title == c_data['title'] \
                            or self.chat_type == c_data['type']:
                        chatroom_id = c_data['id']
                        chatroom_title = c_data['title']
                        chatroom_type = c_data['type']
                        is_break = True
                    p_log(f'{chatroom_id}, {chatroom_title}, {chatroom_type}', level='debug')

                    if is_break:
                        break

                if not self.chat_title and not self.chat_type:
                    chatroom_id = p_data['chat_list'][-1]['id']
                    chatroom_title = p_data['chat_list'][-1]['title']
                    chatroom_type = p_data['chat_list'][-1]['type']
                    is_break = True
                    p_log(f'{chatroom_id}, {chatroom_title}, {chatroom_type}', level='debug')

            if is_break:
                break

        p_log(f'return value : {chatroom_id}, {chatroom_title}, {chatroom_type}', level='debug')
        return chatroom_id, chatroom_title, chatroom_type

    def get_chat_id(self, chat_id=None, chat_title=None, chat_type=None):

        chat_room_title = None
        chat_room_type = None

        self.chat_id = chat_id if chat_id else self.chat_id
        self.chat_title = chat_title if chat_title else self.chat_title
        self.chat_type = chat_type if chat_type else self.chat_type

        if self.chat_id:
            chat_room_id = self.chat_id
        else:
            chat_room_id, chat_room_title, chat_room_type = self.parser_chat_id(self.get_config())

        p_log(f'chat_room_id : {chat_room_id}'
              f'/ chat_room_title : {chat_room_title}'
              f'/ chat_room_type : {chat_room_type}',
              level='debug')

        if not chat_room_id:
            p_log(f'Not found is Send chat id', level='error')
            raise ValueError(f'Not found Chat_id')

        return chat_room_id, chat_room_title

    def send_telegram(self, msg_text, title=None, send_user_name=None, msg_level='warning'):
        send_module = None
        msg_title = title if title else msg_text
        send_msg_skip = False
        send_bot = None

        msg_level_dict = {
            # imoji unicode url : https://unicode.org/emoji/charts/full-emoji-list.html
            # green circle
            'info': '\U0001F7E2',
            # orange circle
            'warning': '\U0001F7E0',
            # red circle + police light
            "error": '\U0001F534 \U0001F6A8',
            "none_level": '\U00002754 ' + msg_level
        }
        select_imoji = f'{msg_level_dict.get(msg_level, msg_level_dict.get("none_level"))}'

        if not send_user_name:
            bot_name, bot_username = self.get_sender_info()
            send_user_name = f'bot-name({bot_name}) / bot-username({bot_username})'
            p_log(f'Not found send_user_name & changed \"{send_user_name}\"', level='debug')

        send_chat_id, chat_room_name = self.get_chat_id()
        send_host = f'{net.get_hostname()}, {net.get_public_ip()}'
        send_date = (date_utils.todaydate(date_type='ms'))

        send_msg = f'{select_imoji}** Title: {msg_title}\n' \
                   f'{"+ [SENDER]":12s}{":":^3s}{send_user_name}\n' \
                   f'{"+ [HOST]":12s}{":":^3s}{send_host}\n' \
                   f'{"+ [DATE]":12s}{":":^3s}{send_date}\n' \
                   f'{"+ [DESC]":12s}{":":^3s}{msg_text}'
        try:
            send_module = f"telegram bot module Send"
            send_bot = True
            self.bot.sendMessage(chat_id=send_chat_id, text=send_msg)
        except telegram.error.NetworkError:
            send_module = f"request module Send"
            send_bot = False
            telegram_api_url = f'{self.api_url}/bot{self.token}/sendMessage'
            payload = {'chat_id': send_chat_id, 'text': send_msg}
            post_result = requests.post(telegram_api_url, json=payload, verify=False)
            del telegram_api_url

            if post_result and post_result.status_code == 200 and post_result.json()['ok']:
                return True
            else:
                p_log(f"status={post_result.status_code}, text={post_result.text}", level='error')
                return False
        except telegram.error.ChatMigrated as e:
            chg_chat_id = str(e)
            p_log(f"changed chat_id {send_chat_id} => {chg_chat_id.split(' ')[-1]}", level='debug')
            send_chat_id = chg_chat_id.split(' ')[-1]
            p_log(f"{chg_chat_id}", level='debug')
            p_log(f"Changed chat room id : {send_chat_id}", level='debug')
            try:
                if send_bot:
                    self.bot.sendMessage(chat_id=send_chat_id, text=send_msg)
                else:
                    telegram_api_url = f'{self.api_url}/bot{self.token}/sendMessage'
                    payload = {'chat_id': send_chat_id, 'text': send_msg}
                    requests.post(telegram_api_url, json=payload, verify=False)
            except telegram.error.Unauthorized as e:
                chat_skip_result = str(e)
                send_msg_skip = True
        finally:
            if send_msg_skip:
                p_log(send_msg, level='error', is_view=True, logging=False)
                p_log(f'Send msg skip !!!\n Remove or Not found chat\nSkip result : {chat_skip_result}', level='error')
            else:
                p_log(send_msg, level='info')
                p_log(f'\n- {send_module}\n* Sender MSG Info'
                      f'\n{"-":>4s} chat_id : {send_chat_id}'
                      f'\n{"-":>4s} chat_name : {chat_room_name}'
                      f'\n{"-":>4s} Send text --  \n{send_msg}', level='debug')


class SlackManager:
    def __init__(self, url=None, send_user_name="SlackBot", ):
        self.webhook_url = url
        self.send_user_name = send_user_name

        self.msg_text = None
        self.p_color = None
        self.msg_title = None

        """
        This class send to slack Messenger
        
        :param url: slack Webhook URL
        :param send_user_name: Sender Name
        
        Example:
            .. code-block:: python
              from alert_noti import SlackManager
              
              SM = SlackManager(url={slack_webhook_url}, send_user_name={name})
              SM.send_slack(msg, url=None, title=None, send_user_name=None, msg_level='info')
        """

    @staticmethod
    def get_level_color(level):
        default_color = "5be312"
        return dict(
            info="5be312",
            warn="f2c744",
            warning="f2c744",
            error="f70202",
        ).get(level, default_color)

    def set_payload(self,):
        # https://app.slack.com/block-kit-builder
        sender_ip = net.get_public_ip() if net.get_public_ip() else net.get_local_ip()
        send_host = f'{net.get_hostname()}, {sender_ip}'
        send_date = (date_utils.todaydate(date_type='ms'))

        payload = {
            "username": self.send_user_name,
            "text": self.msg_title,
            "blocks": [{"type": "divider"}],
            "attachments": [
                {
                    "color": "#" + self.p_color,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": f'Job Title : {self.msg_title}'
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": f'{"+ [HOST]":^12s} : {send_host}'
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": f'{"+ [DATE]":^12s} : {send_date}'
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": f'{"+ [DESC]":^12s} : {self.msg_text}'
                            }
                        }
                    ]
                }
            ]
        }
        p_log(f'Send Payload data\n {payload}', level='debug')
        return payload

    def send_slack(self, msg_text, url=None, title=None, send_user_name=None, msg_level='info'):
        if url is None:
            url = self.webhook_url
            if url is None:
                err_msg = f'No Slack Webhook Address'
                raise EnvironmentError(err_msg)

        self.msg_title = title if title else f'{msg_text[:30]}...'
        self.msg_text = msg_text
        self.send_user_name = send_user_name if send_user_name else self.send_user_name
        self.p_color = SlackManager.get_level_color(msg_level.lower())
        p_log(f'\n\t- Send to slack url : {url}'
              f'\n\t- Send to user name : {send_user_name}'
              f'\n\t- Send to message : {msg_text}',
              level='info')

        post_result = requests.post(url, json=self.set_payload(), verify=False)
        if post_result and post_result.status_code == 200 and post_result.text == "ok":
            p_log(f'Send slack result\n- status_code:{post_result.status_code}', level='debug')
            return True
        else:
            # TODO logging
            p_log(f'send slack fail\n- result : {post_result.json()}', level='error')
            p_log(f"status={post_result.status_code}, text={post_result.text}", level='error')
            return False


class MailManager:
    def __init__(self,
                 smtp_svr=None, smtp_port=None, smtp_ssl=False,
                 mail_user=None, mail_passwd=None,
                 mail_from=None, mail_to=None, mail_cc=None,
                 ):
        """
        This class send to E-Mail

        :param smtp_svr: SMTP server url (ex. smtp.gmail.com)
        :param smtp_port: SMTP port (default: 587 (TLS port))
        :param smtp_ssl: Send to SSL type True (default: False)
        :param mail_user: SMTP server login user address
        :param mail_passwd: SMTP server login user password(or APP password)
        :param mail_from: sender mail address (default: mail_user)
        :param mail_to: recipient user mail address
        :param mail_cc: Cc(CarbonCopy) User mail address

        Example:
            .. code-block:: python
              from alert_noti import MailManager

              MM = MailManager( smtp_svr='smtp.gmail.com', smtp_port=None, smtp_ssl=False,
                    mail_user='{SMTP_LOG_USER}', mail_passwd='{SMTP_LOGIN_PASSWORD}',
                    mail_from=None, mail_to=None, mail_cc=None,
                )
              MM.send_mail(from_addr='test_sender@gmail.com',
                           to_addr='rcpt_user@gmail.com',
                           subject="python Mail Send Test",
                           content="Mail test")
        """

        # smtp_info = {
        #     'gmail.com': ('smtp.gmail.com', 587),
        #     'naver.com': ('smtp.naver.com', 587),
        #     'daum.net': ('smtp.daum.net', 465),
        #     'hanmail.net': ('smtp.daum.net', 465),
        #     'nate.com': ('smtp.mail.nate.com', 465),
        #     'outlook.com': ('smtp.outlook.com', 587),
        # }
        self.smtp_svr = smtp_svr
        if not smtp_port:
            if smtp_ssl:
                self.smtp_port = 465
            else:
                self.smtp_port = 587
        else:
            self.smtp_port = smtp_port

        self.smtp_ssl = smtp_ssl

        if self.smtp_port == 465:
            self.smtp_ssl = True

        self.mail_user = mail_user
        self.mail_passwd = mail_passwd
        self.mail_from = mail_from if mail_from else mail_user
        self.mail_to = mail_to
        self.mail_cc = mail_cc

        self.smtp = None

    def smtp_connect(self,):
        if self.smtp_ssl:
            p_log(f'Connection to SMTP_SSL type', level='info')
            self.smtp = smtplib.SMTP_SSL(self.smtp_svr, self.smtp_port)
            self.smtp.ehlo()
        else:
            p_log(f'Connection to SMTP_TLS type', level='info')
            self.smtp = smtplib.SMTP(self.smtp_svr, self.smtp_port)
            self.smtp.ehlo()
            self.smtp.starttls()

        p_log(f'Login To SMTP server => ID: {self.mail_user} / PW: *************', level='info')
        login_result = self.smtp.login(self.mail_user, self.mail_passwd)
        return login_result[1]

    def smtp_close(self,):
        if self.smtp is not None:
            self.smtp.close()

    @staticmethod
    def str_convert(address):
        if isinstance(address, str):
            return ",".join(address.replace(' ', ',').split(','))
        elif isinstance(address, list):
            return ",".join(address)

    def mail_msg(self,
                 mail_from_addr=None, mail_to_addrs=None, mail_cc_addr=None,
                 subject=None, content=None,
                 ):

        send_text = None
        send_msg = MIMEMultipart('alternative')
        # 제목
        send_msg['Subject'] = subject
        # 발신자
        send_msg['From'] = mail_from_addr if mail_from_addr else self.mail_from
        # 수신자
        if mail_to_addrs:
            send_msg['To'] = MailManager.str_convert(mail_to_addrs)
        else:
            if self.mail_to:
                send_msg['To'] = self.mail_to
            else:
                err_msg = 'No recipient address!'
                p_log(f'{err_msg}', level="error")
                raise ValueError(f'{err_msg}')
        # 참조
        if mail_cc_addr:
            send_msg['Cc'] = MailManager.str_convert(mail_cc_addr)

        try:
            send_text = MIMEText(content.get('html', content.get('plain')), list(content.keys())[0])
        except AttributeError:
            send_text = MIMEText(content)
        finally:
            send_msg.attach(send_text)

        p_log(f'{send_msg.as_string()}', level='debug')

        return send_msg.as_string()

    def send_mail(self,
                  from_addr=None, to_addr=None, cc_addr=None,
                  subject=None, content=None, content_type='plain',
                  send_user_name=None, msg_level='warning',
                  ):

        sender_ip = net.get_public_ip() if net.get_public_ip() else net.get_local_ip()
        send_host = f'{net.get_hostname()}, {sender_ip}'
        send_date = (date_utils.todaydate(date_type='ms'))

        if not subject:
            subject = f'[Notify System!] - {send_host}'
        else:
            subject = f'[Notify System!] - {subject}'

        if not send_user_name:
            send_user_name = f'Notify Manager'

        msg_level_dict = {
            # green circle
            'info': '\U0001F7E2',
            # orange circle
            'warning': '\U0001F7E0',
            # red circle + police light
            "error": '\U0001F534 \U0001F6A8',
            "none_level": '\U00002754 ' + msg_level
        }
        select_imoji = f'{msg_level_dict.get(msg_level, msg_level_dict.get("none_level"))}'

        if content_type.lower() == "plain":
            content = {
                'plain': f'\nALRAM : {select_imoji} {subject}\n\n'
                         f'\n + [SENDER] : {send_user_name}'
                         f'\n + [HOST]   : {send_host}'
                         f'\n + [DATE]   : {send_date}'
                         f'\n + [DESC]   : {content}'
            }
        elif content_type.lower() == "html":
            content = {
                'html': f"""
                <html>
                  <head></head>
                  <body>
                    <h1>ALARM : {select_imoji}{subject}</h1><br>
                    <p>
                      <h3>
                        + [SENDER] : {send_user_name}<br>
                        + [HOST]   : {send_host}<br>
                        + [DATE]   : {send_date}<br>
                        + [DESC]   : {content}<br>
                      </h3>
                    </p><br>
                  </body>
                </html>"""
            }
        else:
            content = content

        sm_conn_result = self.smtp_connect()
        p_log(f'SMTP login status : {sm_conn_result}', level='debug')

        if sm_conn_result.decode().split(' ')[1].lower() == "accepted":
            p_log(f'SMTP User login Success! ({self.mail_user})', level='debug')
            send_msg = self.mail_msg(
                mail_from_addr=from_addr,
                mail_to_addrs=to_addr,
                mail_cc_addr=cc_addr if cc_addr else None,
                subject=f'<No-Reply> {select_imoji} {subject}',
                content=content
            )
            self.smtp.sendmail(from_addr, to_addr, send_msg)
            self.smtp_close()


# It sends a message to Discord.
class DiscordManager:
    def __init__(self, url=None, send_user_name="Discord-Bot", ):
        """
        This function is used to initialize the class

        :param url: The webhook URL required parameter
        :param send_user_name: The name of the user who will send the message, defaults to Discord-Bot (optional)
        :param is_debug: If True, the message will be sent to the console instead of Discord, defaults to False (optional)

        Example:
            .. code-block:: python
              from alert_noti import DiscordManager

              DM = DiscordManager(url={discord_webhook_url}, send_user_name={str(name)})
              DM.send_discord("{Send MessageText}", [title="title_name"], [msg_level="error"]

        """
        self.webhook_url = url
        self.send_user_name = send_user_name
        self.msg_title = None
        self.msg_text = None
        self.p_color = None

        if self.webhook_url is None:
            err_msg = f"Send discord webhook URL is None"
            raise ValueError(err_msg)

    @staticmethod
    def get_level_color(level):
        default_color = "65280"
        return dict(
            info="65280",
            warn="16744192",
            warning="16744192",
            error="16711680",
        ).get(level, default_color)

    def set_payload(self,):
        send_host = f'{net.get_hostname()}, {net.get_public_ip()}'
        send_date = (date_utils.todaydate(date_type='ms'))

        payload = {
            "username": self.send_user_name,
            "embeds": [{
                "fields": [
                    {
                        "name": f'{"+ [HOST]":^12s}',
                        "value": f'{send_host} :wave:',
                        "inline": "true"
                    },
                    {
                        "name": f'{"+ [DATE]":^12s}',
                        "value": f'{send_date}',
                        "inline": "true"
                    },
                    {
                        "name": f'{"+ [DESC]":^12s}',
                        "value": f'{self.msg_text}',
                        "inline": "false"
                    },
                ],
                "color": self.p_color
            }],
            "content": self.msg_title
        }
        p_log(f'Send Payload data\n {payload}', level='debug')
        return payload

    def send_discord(self, msg_text, url=None, title=None, send_user_name=None, msg_level='info'):
        """
        It sends a message to Discord.

        :param msg_text: The text of the message you want to send
        :param url: The webhook URL
        :param title: The title of the message
        :param send_user_name: The name of the user who sent the message
        :param msg_level: The level of the message. This is used to determine the color of the message, defaults to info
        (optional)
        :return: The return value is a string containing the response body, which is the result of the request.
        """
        if url is None:
            url = self.webhook_url
            if url is None:
                err_msg = f'No Discord Webhook Address'
                raise EnvironmentError(err_msg)


        self.msg_title = title if title else f'{msg_text[:30]}...'
        self.msg_text = msg_text
        self.send_user_name = send_user_name if send_user_name else self.send_user_name
        self.p_color = DiscordManager.get_level_color(msg_level.lower())
        p_log(f'\n\t- Send to Discord url : {url}'
              f'\n\t- Send to user name : {self.send_user_name}'
              f'\n\t- Send to message : {self.msg_text}',
              level='info')

        post_result = requests.post(url, json=self.set_payload(), verify=False)
        if post_result and post_result.status_code == 200 and post_result.text == "ok":
            p_log(f'Send discord webhook result\n- status_code:{post_result.status_code}', level="info")
            return True
        elif post_result.status_code == 204:
            p_log(f"Send to DISCORD message is OK! status={post_result.status_code} (No return Content)", level='info')
            return True
        else:
            p_log(f"Send discord webhook fail\n "
                  f"-status={post_result.status_code}, text={post_result.text}", level='error')
            return False


if __name__ == "__main__":
    LOG_DIR = f"{file.get_real_path(__file__)}/logs"
    APP_NAME = 'alert_noti'
    STDOUT = True
    pawn.set(
        # PAWN_APP_LOGGER=app_logger,
        # PAWN_ERROR_LOGGER=error_logger,
        PAWN_LOGGER=dict(
            log_level='debug',
            log_path=LOG_DIR,
            stdout=STDOUT,
            use_hook_exception=True,
        ),
        app_name=APP_NAME,
        version="0.0.1",
        app_data={}
    )
