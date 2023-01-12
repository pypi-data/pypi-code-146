# Ayiin - Userbot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/Ayiin-Userbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/Ayiin-Userbot/blob/main/LICENSE/>.
#
# FROM Ayiin-Userbot <https://github.com/AyiinXd/Ayiin-Userbot>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import logging
import sys

from pyAyiin.config import Var as Variable

from ..methods._database import AyiinDB
from ..methods.helpers import Helpers
from ..methods.hosting import where_hosted

from .client import *


adB = AyiinDB()
logs = logging.getLogger(__name__)
HOSTED_ON = where_hosted()
Var = Variable()
Xd = Helpers()


async def ayiin_client(client):
    try:
        await client.join_chat("AyiinChat")
        await client.join_chat("AyiinSupport")
        await client.join_chat("StoryAyiin")
    except Exception:
        pass


clients = []
client_id = []


async def StartPyrogram():
    try:
        bot_plugins = Xd.import_module(
            "assistant/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{bot_plugins} Total Plugins Bot")
        plugins = Xd.import_module(
            "AyiinXd/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{plugins} Total Plugins User")
    except BaseException as e:
        logs.info(e)
        sys.exit()
    if tgbot:
        await tgbot.start()
        me = await tgbot.get_me()
        tgbot.id = me.id
        tgbot.mention = me.mention
        tgbot.username = me.username
        if me.last_name:
            tgbot.name = me.first_name + " " + me.last_name
        else:
            tgbot.name = me.first_name
        logs.info(
            f"TgBot in {tgbot.name} | [ {tgbot.id} ]"
        )
        client_id.append(tgbot.id)
    if AYIIN1:
        try:
            await AYIIN1.start()
            clients.append(1)
            await ayiin_client(AYIIN1)
            me = await AYIIN1.get_me()
            AYIIN1.id = me.id
            AYIIN1.mention = me.mention
            AYIIN1.username = me.username
            if me.last_name:
                AYIIN1.name = me.first_name + " " + me.last_name
            else:
                AYIIN1.name = me.first_name
            #AYIIN1.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN1 in {AYIIN1.name} | [ {AYIIN1.id} ]"
            )
            client_id.append(AYIIN1.id)
        except Exception as e:
            logs.info(f"[STRING_1] ERROR: {e}")
    if AYIIN2:
        try:
            await AYIIN2.start()
            clients.append(2)
            await ayiin_client(AYIIN2)
            me = await AYIIN2.get_me()
            AYIIN2.id = me.id
            AYIIN2.mention = me.mention
            AYIIN2.username = me.username
            if me.last_name:
                AYIIN2.name = me.first_name + " " + me.last_name
            else:
                AYIIN2.name = me.first_name
            #AYIIN2.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN2 in {AYIIN2.name} | [ {AYIIN2.id} ]"
            )
            client_id.append(AYIIN2.id)
        except Exception as e:
            logs.info(f"[STRING_2] ERROR: {e}")
    if AYIIN3:
        try:
            await AYIIN3.start()
            clients.append(3)
            await ayiin_client(AYIIN3)
            me = await AYIIN3.get_me()
            AYIIN3.id = me.id
            AYIIN3.mention = me.mention
            AYIIN3.username = me.username
            if me.last_name:
                AYIIN3.name = me.first_name + " " + me.last_name
            else:
                AYIIN3.name = me.first_name
            #AYIIN3.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN3 in {AYIIN3.name} | [ {AYIIN3.id} ]"
            )
            client_id.append(AYIIN3.id)
        except Exception as e:
            logs.info(f"[STRING_3] ERROR: {e}")
    if AYIIN4:
        try:
            await AYIIN4.start()
            clients.append(4)
            await ayiin_client(AYIIN4)
            me = await AYIIN4.get_me()
            AYIIN4.id = me.id
            AYIIN4.mention = me.mention
            AYIIN4.username = me.username
            if me.last_name:
                AYIIN4.name = me.first_name + " " + me.last_name
            else:
                AYIIN4.name = me.first_name
            #AYIIN4.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN4 in {AYIIN4.name} | [ {AYIIN4.id} ]"
            )
            client_id.append(AYIIN4.id)
        except Exception as e:
            logs.info(f"[STRING_4] ERROR: {e}")
    if AYIIN5:
        try:
            await AYIIN5.start()
            clients.append(5)
            await ayiin_client(AYIIN5)
            me = await AYIIN5.get_me()
            AYIIN5.id = me.id
            AYIIN5.mention = me.mention
            AYIIN5.username = me.username
            if me.last_name:
                AYIIN5.name = me.first_name + " " + me.last_name
            else:
                AYIIN5.name = me.first_name
            #AYIIN5.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN5 in {AYIIN5.name} | [ {AYIIN5.id} ]"
            )
            client_id.append(AYIIN5.id)
        except Exception as e:
            logs.info(f"[STRING_5] ERROR: {e}")
    if AYIIN6:
        try:
            await AYIIN6.start()
            clients.append(6)
            await ayiin_client(AYIIN6)
            me = await AYIIN6.get_me()
            AYIIN6.id = me.id
            AYIIN6.mention = me.mention
            AYIIN6.username = me.username
            if me.last_name:
                AYIIN6.name = me.first_name + " " + me.last_name
            else:
                AYIIN6.name = me.first_name
            #AYIIN1.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN6 in {AYIIN6.name} | [ {AYIIN6.id} ]"
            )
            client_id.append(AYIIN6.id)
        except Exception as e:
            logs.info(f"[STRING_6] ERROR: {e}")
    if AYIIN7:
        try:
            await AYIIN7.start()
            clients.append(7)
            await ayiin_client(AYIIN7)
            me = await AYIIN7.get_me()
            AYIIN7.id = me.id
            AYIIN7.mention = me.mention
            AYIIN7.username = me.username
            if me.last_name:
                AYIIN7.name = me.first_name + " " + me.last_name
            else:
                AYIIN7.name = me.first_name
            #AYIIN7.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN7 in {AYIIN7.name} | [ {AYIIN7.id} ]"
            )
            client_id.append(AYIIN7.id)
        except Exception as e:
            logs.info(f"[STRING_7] ERROR: {e}")
    if AYIIN8:
        try:
            await AYIIN8.start()
            clients.append(8)
            await ayiin_client(AYIIN8)
            me = await AYIIN8.get_me()
            AYIIN8.id = me.id
            AYIIN8.mention = me.mention
            AYIIN8.username = me.username
            if me.last_name:
                AYIIN8.name = me.first_name + " " + me.last_name
            else:
                AYIIN8.name = me.first_name
            #AYIIN8.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN8 in {AYIIN8.name} | [ {AYIIN8.id} ]"
            )
            client_id.append(AYIIN8.id)
        except Exception as e:
            logs.info(f"[STRING_8] ERROR: {e}")
    if AYIIN9:
        try:
            await AYIIN9.start()
            clients.append(9)
            await ayiin_client(AYIIN9)
            me = await AYIIN9.get_me()
            AYIIN9.id = me.id
            AYIIN9.mention = me.mention
            AYIIN9.username = me.username
            if me.last_name:
                AYIIN9.name = me.first_name + " " + me.last_name
            else:
                AYIIN9.name = me.first_name
            #AYIIN9.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN9 in {AYIIN9.name} | [ {AYIIN9.id} ]"
            )
            client_id.append(AYIIN9.id)
        except Exception as e:
            logs.info(f"[STRING_9] ERROR: {e}")
    if AYIIN10:
        try:
            await AYIIN10.start()
            clients.append(10)
            await ayiin_client(AYIIN10)
            me = await AYIIN10.get_me()
            AYIIN10.id = me.id
            AYIIN10.mention = me.mention
            AYIIN10.username = me.username
            if me.last_name:
                AYIIN10.name = me.first_name + " " + me.last_name
            else:
                AYIIN10.name = me.first_name
            #AYIIN10.has_a_bot = True if tgbot else False
            logs.info(
                f"AYIIN10 in {AYIIN10.name} | [ {AYIIN10.id} ]"
            )
            client_id.append(AYIIN10.id)
        except Exception as e:
            logs.info(f"[STRING_10] ERROR: {e}")
    logs.info(f"Connecting Database To {adB.name}")
    if adB.ping():
        logs.info(f"Succesfully Connect On {adB.name}")
    logs.info(
        f"Connect On [ {HOSTED_ON} ]\n"
    )
