import logging
from datetime import datetime
from traceback import format_exc
import pytz
from geezlibs import filters
from geezlibs.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    UserNotParticipant
)
from geezlibs.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from geezlibs.handlers import CallbackQueryHandler, InlineQueryHandler

from .config import Var as Variable
from .decorator import is_admin_or_owner
from .Clients import *


Var = Variable()


async def list_all_client():
    cli = []
    if GEEZ1:
        me1 = await GEEZ1.get_me()
        cli.append(me1.id)
    if GEEZ2:
        me2 = await GEEZ2.get_me()
        cli.append(me2.id)
    if GEEZ3:
        me3 = await GEEZ3.get_me()
        cli.append(me3.id)
    if GEEZ4:
        me4 = await GEEZ4.get_me()
        cli.append(me4.id)
    if GEEZ5:
        me5 = await GEEZ5.get_me()
        cli.append(me5.id)
    if GEEZ6:
        me6 = await GEEZ6.get_me()
        cli.append(me6.id)
    if GEEZ7:
        me7 = await GEEZ7.get_me()
        cli.append(me7.id)
    if GEEZ8:
        me8 = await GEEZ8.get_me()
        cli.append(me8.id)
    if GEEZ9:
        me9 = await GEEZ9.get_me()
        cli.append(me9.id)
    if GEEZ10:
        me10 = await GEEZ10.get_me()
        cli.append(me6.id)
    
    return cli


MSG_IN = """
**Geez Pyro**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{}](tg://user?id={})
**Support**: @GeezSupport

**Buat Ubot Anda Sendiri Di** @GeezSupport
➖➖➖➖➖➖➖➖➖➖
"""    


IN_BTTS = [
    [
        InlineKeyboardButton(
            "Geez Support",
            url="https://t.me/GeezSupport",
        ),
        InlineKeyboardButton(
            "RAM Support", 
            url="https://t.me/ramsupportt"),
    ]
]



def inline(
    pattern: str = None,
    group: int = 0,
    client_only: bool = False,
):
    """- Main Decorator To Register Commands. -"""
    filterm = (
        filters.regex(pattern=pattern)
    )

    def izzyxd(func):
        async def wrapper(tgbot, iq):
            me = await GEEZ1.get_me()
            OWNER = me.first_name + " " + me.last_name if me.last_name else ""
            OWNER_ID = me.id
            if client_only and iq.from_user.id not in client_id:
                results=[
                    (
                        InlineQueryResultArticle(
                            title="Geez Pyro!",
                            reply_markup=InlineKeyboardMarkup(IN_BTTS),
                            input_message_content=InputTextMessageContent(MSG_IN.format(OWNER, OWNER_ID)),
                        )
                    )
                ],
                await iq.answer(
                    results,
                    switch_pm_text=f"🤖: Assistant of {OWNER}",
                    switch_pm_parameter="start",
                )
                return
            try:
                await func(tgbot, iq)
            except BaseException:
                logging.error(
                    f"Exception - {func.__module__} - {func.__name__}"
                )
                TZZ = pytz.timezone(Var.TZ)
                datetime_tz = datetime.now(TZZ)
                text = "<b>!ERROR - REPORT!</b>\n\n"
                text += f"\n<b>Dari:</b> <code>{OWNER}</code>"
                text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                text += f"\n<b>Plugin-Name :</b> <code>{func.__module__}</code>"
                text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                text += datetime_tz.strftime(
                    "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                )
                try:
                    xx = await tgbot.send_message(Var.LOG_CHAT, text)
                    await xx.pin(disable_notification=False)
                except BaseException:
                    logging.error(text)
        add_handler(filterm, wrapper, pattern, group)
        return wrapper

    return izzyxd


def add_handler(filter_s, func_, pattern, group):
    if tgbot:
        tgbot.add_handler(InlineQueryHandler(func_, filters=filter_s), group=group)


def callback(
    pattern: str = None,
    group: int = 0,
    from_users: list = [],
    client_only: bool = False,
    admins: bool = False,
):
    """- Main Decorator To Register Commands. -"""
    filterm = (
        filters.regex(pattern=pattern)
    )

    def izzyxd(func):
        async def wrapper(tgbot, cq):
            me = await GEEZ1.get_me()
            OWNER = me.first_name + " " + me.last_name if me.last_name else ""
            OWNER_ID = me.id
            if "me" in from_users:
                from_users.remove("me")
                for bot in Bots:
                    mebot = await bot.get_me()
                    from_users.append(mebot.id)
            if client_only and cq.from_user.id not in client_id:
                return await cq.answer(
                    "Ini Bukan Userbot Anda, Silahkan Buat Userbot Anda Di @GeezSupport",
                    show_alert=True,
                )
            if admins and not await is_admin_or_owner(
                cq.message, from_users
            ):
                return await cq.answer(
                    "Lu Bukan Admin Di Gc Ini...",
                    show_alert=True,
                )
            try:
                await func(tgbot, cq)
            except MessageNotModified:
                    pass
            except MessageIdInvalid:
                logging.warning(
                    "Please Don't Delete Commands While it's Processing..."
                )
            except UserNotParticipant:
                pass
            except BaseException:
                logging.error(
                    f"Exception - {func.__module__} - {func.__name__}"
                )
                TZZ = pytz.timezone(Var.TZ)
                datetime_tz = datetime.now(TZZ)
                text = "<b>!ERROR - REPORT!</b>\n\n"
                text += f"\n<b>Dari:</b> <code>{OWNER}</code>"
                text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                text += f"\n<b>Plugin-Name :</b> <code>{func.__module__}</code>"
                text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                text += datetime_tz.strftime(
                    "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                )
                try:
                    xx = await tgbot.send_message(Var.LOG_CHAT, text)
                    await xx.pin(disable_notification=False)
                except BaseException:
                    logging.error(text)
        add2_handler(filterm, wrapper, pattern, group)
        return wrapper

    return izzyxd


def add2_handler(filter_s, func_, pattern, group):
    if tgbot:
        tgbot.add_handler(CallbackQueryHandler(func_, filters=filter_s), group=group)
