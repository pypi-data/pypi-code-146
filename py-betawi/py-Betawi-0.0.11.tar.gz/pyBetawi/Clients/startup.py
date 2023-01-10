import logging
import sys

from pyBetawi.config import Var as Variable

from ..methods._database import geezDB
from ..methods.helpers import Helpers
from ..methods.hosting import where_hosted

from .client import *


zydB = geezDB()
logs = logging.getLogger(__name__)
HOSTED_ON = where_hosted()
Var = Variable()
Gz = Helpers()


async def geez_client(client):
    try:
        await client.join_chat("GeezSupport")
        await client.join_chat("ramsupportt")
    except Exception:
        pass


clients = []
client_id = []


async def StartPyrogram():
    try:
        bot_plugins = Gz.import_module(
            "assistant/",
            display_module=False,
            exclude=Var.NO_LOAD,
        )
        logs.info(f"{bot_plugins} Total Plugins Bot")
        plugins = Gz.import_module(
            "geez/",
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
    if GEEZ1:
        try:
            await GEEZ1.start()
            clients.append(1)
            await geez_client(GEEZ1)
            me = await GEEZ1.get_me()
            GEEZ1.id = me.id
            GEEZ1.mention = me.mention
            GEEZ1.username = me.username
            if me.last_name:
                GEEZ1.name = me.first_name + " " + me.last_name
            else:
                GEEZ1.name = me.first_name
            #GEEZ1.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ1 in {GEEZ1.name} | [ {GEEZ1.id} ]"
            )
            client_id.append(GEEZ1.id)
        except Exception as e:
            clients.remove(1)
            client_id.remove(GEEZ1.id)
            logs.info(f"[STRING_1] ERROR: {e}")
    if GEEZ2:
        try:
            await GEEZ2.start()
            clients.append(2)
            await geez_client(GEEZ2)
            me = await GEEZ2.get_me()
            GEEZ2.id = me.id
            GEEZ2.mention = me.mention
            GEEZ2.username = me.username
            if me.last_name:
                GEEZ2.name = me.first_name + " " + me.last_name
            else:
                GEEZ2.name = me.first_name
            #GEEZ2.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ2 in {GEEZ2.name} | [ {GEEZ2.id} ]"
            )
            client_id.append(GEEZ2.id)
        except Exception as e:
            clients.remove(2)
            client_id.remove(GEEZ2.id)
            logs.info(f"[STRING_2] ERROR: {e}")
    if GEEZ3:
        try:
            await GEEZ3.start()
            clients.append(3)
            await geez_client(GEEZ3)
            me = await GEEZ3.get_me()
            GEEZ3.id = me.id
            GEEZ3.mention = me.mention
            GEEZ3.username = me.username
            if me.last_name:
                GEEZ3.name = me.first_name + " " + me.last_name
            else:
                GEEZ3.name = me.first_name
            #GEEZ3.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ3 in {GEEZ3.name} | [ {GEEZ3.id} ]"
            )
            client_id.append(GEEZ3.id)
        except Exception as e:
            clients.remove(3)
            client_id.remove(GEEZ3.id)
            logs.info(f"[STRING_3] ERROR: {e}")
    if GEEZ4:
        try:
            await GEEZ4.start()
            clients.append(4)
            await geez_client(GEEZ4)
            me = await GEEZ4.get_me()
            GEEZ4.id = me.id
            GEEZ4.mention = me.mention
            GEEZ4.username = me.username
            if me.last_name:
                GEEZ4.name = me.first_name + " " + me.last_name
            else:
                GEEZ4.name = me.first_name
            #GEEZ4.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ4 in {GEEZ4.name} | [ {GEEZ4.id} ]"
            )
            client_id.append(GEEZ4.id)
        except Exception as e:
            clients.remove(4)
            client_id.remove(GEEZ4.id)
            logs.info(f"[STRING_4] ERROR: {e}")
    if GEEZ5:
        try:
            await GEEZ5.start()
            clients.append(5)
            await geez_client(GEEZ5)
            me = await GEEZ5.get_me()
            GEEZ5.id = me.id
            GEEZ5.mention = me.mention
            GEEZ5.username = me.username
            if me.last_name:
                GEEZ5.name = me.first_name + " " + me.last_name
            else:
                GEEZ5.name = me.first_name
            #GEEZ5.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ5 in {GEEZ5.name} | [ {GEEZ5.id} ]"
            )
            client_id.append(GEEZ5.id)
        except Exception as e:
            clients.remove(5)
            client_id.remove(GEEZ5.id)
            logs.info(f"[STRING_5] ERROR: {e}")
    if GEEZ6:
        try:
            await GEEZ6.start()
            clients.append(6)
            await geez_client(GEEZ6)
            me = await GEEZ6.get_me()
            GEEZ6.id = me.id
            GEEZ6.mention = me.mention
            GEEZ6.username = me.username
            if me.last_name:
                GEEZ6.name = me.first_name + " " + me.last_name
            else:
                GEEZ6.name = me.first_name
            #GEEZ1.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ6 in {GEEZ6.name} | [ {GEEZ6.id} ]"
            )
            client_id.append(GEEZ6.id)
        except Exception as e:
            clients.remove(6)
            client_id.remove(GEEZ6.id)
            logs.info(f"[STRING_6] ERROR: {e}")
    if GEEZ7:
        try:
            await GEEZ7.start()
            clients.append(7)
            await geez_client(GEEZ7)
            me = await GEEZ7.get_me()
            GEEZ7.id = me.id
            GEEZ7.mention = me.mention
            GEEZ7.username = me.username
            if me.last_name:
                GEEZ7.name = me.first_name + " " + me.last_name
            else:
                GEEZ7.name = me.first_name
            #GEEZ7.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ7 in {GEEZ7.name} | [ {GEEZ7.id} ]"
            )
            client_id.append(GEEZ7.id)
        except Exception as e:
            clients.remove(7)
            client_id.remove(GEEZ7.id)
            logs.info(f"[STRING_7] ERROR: {e}")
    if GEEZ8:
        try:
            await GEEZ8.start()
            clients.append(8)
            await geez_client(GEEZ8)
            me = await GEEZ8.get_me()
            GEEZ8.id = me.id
            GEEZ8.mention = me.mention
            GEEZ8.username = me.username
            if me.last_name:
                GEEZ8.name = me.first_name + " " + me.last_name
            else:
                GEEZ8.name = me.first_name
            #GEEZ8.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ8 in {GEEZ8.name} | [ {GEEZ8.id} ]"
            )
            client_id.append(GEEZ8.id)
        except Exception as e:
            clients.remove(8)
            client_id.remove(GEEZ8.id)
            logs.info(f"[STRING_8] ERROR: {e}")
    if GEEZ9:
        try:
            await GEEZ9.start()
            clients.append(9)
            await geez_client(GEEZ9)
            me = await GEEZ9.get_me()
            GEEZ9.id = me.id
            GEEZ9.mention = me.mention
            GEEZ9.username = me.username
            if me.last_name:
                GEEZ9.name = me.first_name + " " + me.last_name
            else:
                GEEZ9.name = me.first_name
            #GEEZ9.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ9 in {GEEZ9.name} | [ {GEEZ9.id} ]"
            )
            client_id.append(GEEZ9.id)
        except Exception as e:
            clients.remove(9)
            client_id.remove(GEEZ9.id)
            logs.info(f"[STRING_9] ERROR: {e}")
    if GEEZ10:
        try:
            await GEEZ10.start()
            clients.append(10)
            await geez_client(GEEZ10)
            me = await GEEZ10.get_me()
            GEEZ10.id = me.id
            GEEZ10.mention = me.mention
            GEEZ10.username = me.username
            if me.last_name:
                GEEZ10.name = me.first_name + " " + me.last_name
            else:
                GEEZ10.name = me.first_name
            #GEEZ10.has_a_bot = True if tgbot else False
            logs.info(
                f"GEEZ10 in {GEEZ10.name} | [ {GEEZ10.id} ]"
            )
            client_id.append(GEEZ10.id)
        except Exception as e:
            clients.remove(10)
            client_id.remove(GEEZ10.id)
            logs.info(f"[STRING_10] ERROR: {e}")
    logs.info(f"Connecting Database To {zydB.name}")
    if zydB.ping():
        logs.info(f"Succesfully Connect On {zydB.name}")
    logs.info(
        f"Connect On [ {HOSTED_ON} ]\n"
    )
