import logging
from datetime import datetime
from traceback import format_exc
import pytz
from fipper import filters
from fipper.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    UserNotParticipant
)
from fipper.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent
)

from fipper.handlers import CallbackQueryHandler, InlineQueryHandler

from .config import Var as Variable
from .decorator import is_admin_or_owner
from .Clients import *


Var = Variable()


async def list_all_client():
    cli = []
    if AYIIN1:
        me1 = await AYIIN1.get_me()
        cli.append(me1.id)
    if AYIIN2:
        me2 = await AYIIN2.get_me()
        cli.append(me2.id)
    if AYIIN3:
        me3 = await AYIIN3.get_me()
        cli.append(me3.id)
    if AYIIN4:
        me4 = await AYIIN4.get_me()
        cli.append(me4.id)
    if AYIIN5:
        me5 = await AYIIN5.get_me()
        cli.append(me5.id)
    if AYIIN6:
        me6 = await AYIIN6.get_me()
        cli.append(me6.id)
    if AYIIN7:
        me7 = await AYIIN7.get_me()
        cli.append(me7.id)
    if AYIIN8:
        me8 = await AYIIN8.get_me()
        cli.append(me8.id)
    if AYIIN9:
        me9 = await AYIIN9.get_me()
        cli.append(me9.id)
    if AYIIN10:
        me10 = await AYIIN10.get_me()
        cli.append(me6.id)
    
    return cli


MSG_IN = """
**Ayiin - UBot**
➖➖➖➖➖➖➖➖➖➖
**Owner**: [{}](tg://user?id={})
**Support**: @AyiinChat

**Buat Ubot Anda Sendiri Di** @AyiinChat
➖➖➖➖➖➖➖➖➖➖
"""    


IN_BTTS = [
    [
        InlineKeyboardButton(
            "Repository",
            url="https://github.com/AyiinXd/AyiinUbot",
        ),
        InlineKeyboardButton(
            "Support", 
            url="https://t.me/AyiinChat"),
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

    def yinsxd(func):
        async def wrapper(tgbot, iq):
            me = await AYIIN1.get_me()
            OWNER = me.first_name + " " + me.last_name if me.last_name else ""
            OWNER_ID = me.id
            if client_only and iq.from_user.id not in client_id:
                results=[
                    (
                        InlineQueryResultArticle(
                            title="Ayiin Ubot!",
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

    return yinsxd


def add_handler(filter_s, func_, pattern, group):
    if tgbot:
        tgbot.add_handler(InlineQueryHandler(func_, filters=filter_s), group=group)


def callback(
    pattern: str = None,
    group: int = 0,
    from_users: list = [],
    client_only: bool = False,
    users: bool = False,
    admins: bool = False,
):
    """- Main Decorator To Register Commands. -"""
    filterm = (
        filters.regex(pattern=pattern)
    )

    def yinsxd(func):
        async def wrapper(tgbot, cq):
            me = await AYIIN1.get_me()
            OWNER = me.first_name + " " + me.last_name if me.last_name else ""
            OWNER_ID = me.id
            if "me" in from_users:
                from_users.remove("me")
                for bot in Bots:
                    mebot = await bot.get_me()
                    from_users.append(mebot.id)
            if client_only and cq.from_user.id not in client_id:
                return await cq.answer(
                    "Ini Bukan Userbot Anda, Silahkan Buat Userbot Anda Di @AyiinChat",
                    show_alert=True,
                )
            if admins and not await is_admin_or_owner(
                cq.message, from_users
            ):
                return await cq.answer(
                    "Lu Bukan Admin Di Gc Ini Tod...",
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

    return yinsxd


def add2_handler(filter_s, func_, pattern, group):
    if tgbot:
        tgbot.add_handler(CallbackQueryHandler(func_, filters=filter_s), group=group)
