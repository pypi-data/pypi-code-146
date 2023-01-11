#!/usr/bin/env python3
# -*- coding: utf -*-

import time
from pawnlib.config import pawnlib_config as pawn
from pawnlib.output import file, debug_logging, debug_print
from pawnlib.utils.http import disable_ssl_warnings
from pawnlib.builder import generator
import sys


def all_test():
    from alert_noti import TelegramManager

    # print('''
    #  _____    _                                  _____         _
    # |_   _|__| | ___  __ _ _ __ __ _ _ __ ___   |_   _|__  ___| |_
    #   | |/ _ \ |/ _ \/ _` | '__/ _` | '_ ` _ \    | |/ _ \/ __| __|
    #   | |  __/ |  __/ (_| | | | (_| | | | | | |   | |  __/\__ \ |_
    #   |_|\___|_|\___|\__, |_|  \__,_|_| |_| |_|   |_|\___||___/\__|
    #                  |___/
    # ''')
    print(generator.generate_banner(app_name='TelegramManager', version='0.0.1', description='Telegram test'))
    bot_token = ['5467623732:AAFX2zwHRlrov69IKvsnEG_keQIWGb1FqhA']

    for token in bot_token:
        #TM = TelegramManager(token=token, chat_title='test_il_pubblic', is_debug=False)
        TM = TelegramManager(token=token)

        test_list = [
            {'level': 'info', 'case_num': '01'},
            {'level': 'error', 'case_num': '02'},
            {'level': 'warning', 'case_num': '03'},
            {'level': 'none_test', 'case_num': '04'},
        ]

        for i in test_list:
            test_case = f'case.{i.get("case_num")}'
            test_send_msg = f'send to {i.get("level")} msg and'
            TM.send_telegram(
                f'{test_case}-01] {test_send_msg} title=None, Send_user_name=None, msg_level=\"{i.get("level")}\"',
                msg_level=f'{i.get("level")}'
            )
    sys.exit()

    print('''
     ____  _            _      _____         _
    / ___|| | __ _  ___| | __ |_   _|__  ___| |_
    \___ \| |/ _` |/ __| |/ /   | |/ _ \/ __| __|
     ___) | | (_| | (__|   <    | |  __/\__ \ |_
    |____/|_|\__,_|\___|_|\_\   |_|\___||___/\__|
    ''')
    from alert_noti import SlackManager
    slack_url = "https://hooks.slack.com/services/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"
    SM = SlackManager(url=slack_url)
    SM.send_slack("test slack bot")

    print('''
         __  __       _ _ _____         _
    |  \/  | __ _(_) |_   _|__  ___| |_
    | |\/| |/ _` | | | | |/ _ \/ __| __|
    | |  | | (_| | | | | |  __/\__ \ |_
    |_|  |_|\__,_|_|_| |_|\___||___/\__|
    ''')
    from alert_noti import MailManager
    MM = MailManager(
        smtp_svr='smtp.gmail.com',
        smtp_port=None,
        mail_user='lucktest.kr@gmail.com',
        mail_passwd='owkwodsfquzmgxtl',
        mail_from=None,
        mail_to=None,
        mail_cc=None,
        smtp_ssl=False,
    )

    test_from = "lucktest.kr@gmail.com"
    test_to = "hnsong@iconloop.com"
    MM.send_mail(from_addr=test_from, to_addr=test_to, subject="python Mail Send Test", content="Mail test")


if __name__ == '__main__':
    LOG_DIR = f"{file.get_real_path(__file__)}/logs"
    APP_NAME = 'alert_noti'
    STDOUT = False
    pawn.set(
       PAWN_LOGGER=dict(
            # log_level='DEBUG',
            log_path=LOG_DIR,
            stdout=STDOUT,
            use_hook_exception=False,
        ),
        app_name=APP_NAME,
        version="0.0.1",
        app_data={}
    )

    #pawn.app_logger.info('test')
    #pawn.console.log('ssss console log')

    disable_ssl_warnings()
    all_test()
