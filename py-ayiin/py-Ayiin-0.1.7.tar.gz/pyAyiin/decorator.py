import logging
from datetime import datetime
from traceback import format_exc
import pytz
from fipper import ContinuePropagation, StopPropagation, filters
from fipper.enums import ChatMemberStatus, ChatType
from fipper.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from fipper.handlers import MessageHandler

from pyAyiin.pyrogram import eor

from . import DEVS
from .config import Var as Variable
from .Clients import *


Var = Variable()


async def is_admin_or_owner(message, user_id) -> bool:
    """Check If A User Is Creator Or Admin Of The Current Group"""
    if message.chat.type in [ChatType.PRIVATE, ChatType.BOT]:
        # You Are Boss Of Pvt Chats.
        return True
    user_s = await message.chat.get_member(int(user_id))
    if user_s.status in (
            ChatMemberStatus.OWNER,
            ChatMemberStatus.ADMINISTRATOR):
        return True
    return False


def Ayiin(
    cmd: list,
    group: int = 0,
    devs: bool = False,
    pm_only: bool = False,
    group_only: bool = False,
    channel_only: bool = False,
    admin_only: bool = False,
    pass_error: bool = False,
    propagate_to_next_handler: bool = True,
):
    """- Main Decorator To Register Commands. -"""
    if not devs:
        filterm = (
            filters.me
            & filters.command(cmd, Var.HNDLR)
            & ~filters.via_bot
            & ~filters.forwarded
        )
    else:
        filterm = (
            filters.user(DEVS)
            & filters.command(cmd, "")
        )

    def decorator(func):
        async def wrapper(client, message):
            message.client = client
            chat_type = message.chat.type
            if admin_only and not await is_admin_or_owner(
                message, (client.me).id
            ):
                await eor(
                    message, "<code>Perintah Ini Hanya Bisa Digunakan Jika Anda Admin Di Group Ini!</code>"
                )
                return
            if group_only and chat_type != (ChatType.GROUP, ChatType.SUPERGROUP):
                await eor(message, "<code>Apakah Ini Grup Tod?</code>")
                return
            if channel_only and chat_type != ChatType.CHANNEL:
                await eor(message, "Perintah Ini Hanya Bisa Digunakan Di Channel!")
                return
            if pm_only and chat_type != ChatType.PRIVATE:
                await eor(message, "<code>Perintah Ini Hanya Bisa Digunakan Di PM!</code>")
                return
            if pass_error:
                await func(client, message)
            else:
                try:
                    await func(client, message)
                except StopPropagation:
                    raise StopPropagation
                except KeyboardInterrupt:
                    pass
                except MessageNotModified:
                    pass
                except MessageIdInvalid:
                    logging.warning(
                        "Please Don't Delete Commands While it's Processing..."
                    )
                except UserNotParticipant:
                    pass
                except ContinuePropagation:
                    raise ContinuePropagation
                except BaseException:
                    logging.error(
                        f"Exception - {func.__module__} - {func.__name__}"
                    )
                    TZZ = pytz.timezone(Var.TZ)
                    datetime_tz = datetime.now(TZZ)
                    text = "<b>!ERROR - REPORT!</b>\n\n"
                    text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
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
        add_handler(filterm, wrapper, cmd)
        return wrapper

    return decorator


def listen(filter_s):
    """Simple Decorator To Handel Custom Filters"""
    def decorator(func):
        async def wrapper(client, message):
            try:
                await func(client, message)
            except StopPropagation:
                raise StopPropagation
            except ContinuePropagation:
                raise ContinuePropagation
            except UserNotParticipant:
                pass
            except MessageEmpty:
                pass
            except BaseException:
                logging.error(
                    f"Exception - {func.__module__} - {func.__name__}")
                TZZ = pytz.timezone(Var.TZ)
                datetime_tz = datetime.now(TZZ)
                text = "<b>!ERROR WHILE HANDLING UPDATES!</b>\n\n"
                text += f"\n<b>Dari:</b> <code>{client.me.first_name}</code>"
                text += f"\n<b>Trace Back : </b> <code>{str(format_exc())}</code>"
                text += f"\n<b>Plugin Name :</b> <code>{func.__module__}</code>"
                text += f"\n<b>Function Name :</b> <code>{func.__name__}</code> \n"
                text += datetime_tz.strftime(
                    "<b>Date :</b> <code>%Y-%m-%d</code> \n<b>Time :</b> <code>%H:%M:%S</code>"
                )
                try:
                    xx = await tgbot.send_message(Var.LOG_CHAT, text)
                    await xx.pin(disable_notification=False)
                except BaseException:
                    logging.error(text)
            message.continue_propagation()
        if AYIIN1:
            AYIIN1.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN2:
            AYIIN2.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN3:
            AYIIN3.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN4:
            AYIIN4.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN5:
            AYIIN5.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN6:
            AYIIN6.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN7:
            AYIIN7.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN8:
            AYIIN8.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN9:
            AYIIN9.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN10:
            AYIIN10.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        '''
        if AYIIN11:
            AYIIN11.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN12:
            AYIIN12.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN13:
            AYIIN13.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN14:
            AYIIN14.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN15:
            AYIIN15.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN16:
            AYIIN16.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN17:
            AYIIN17.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN18:
            AYIIN18.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN19:
            AYIIN19.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN20:
            AYIIN20.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN21:
            AYIIN21.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN22:
            AYIIN22.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN23:
            AYIIN23.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN24:
            AYIIN24.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN25:
            AYIIN25.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN26:
            AYIIN26.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN27:
            AYIIN27.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN28:
            AYIIN28.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN29:
            AYIIN29.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN30:
            AYIIN30.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN31:
            AYIIN31.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN32:
            AYIIN32.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN33:
            AYIIN33.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN34:
            AYIIN34.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN35:
            AYIIN35.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN36:
            AYIIN36.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN37:
            AYIIN37.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN38:
            AYIIN38.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN39:
            AYIIN39.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN40:
            AYIIN40.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN41:
            AYIIN41.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN42:
            AYIIN42.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN43:
            AYIIN43.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN44:
            AYIIN44.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN45:
            AYIIN45.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN46:
            AYIIN46.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN47:
            AYIIN47.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN48:
            AYIIN48.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN49:
            AYIIN49.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN50:
            AYIIN50.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN51:
            AYIIN51.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN52:
            AYIIN52.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN53:
            AYIIN53.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN54:
            AYIIN54.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN55:
            AYIIN55.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN56:
            AYIIN56.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN57:
            AYIIN57.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN58:
            AYIIN58.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN59:
            AYIIN59.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN60:
            AYIIN60.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN61:
            AYIIN61.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN62:
            AYIIN62.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN63:
            AYIIN63.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN64:
            AYIIN64.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN65:
            AYIIN65.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN66:
            AYIIN66.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN67:
            AYIIN67.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN68:
            AYIIN68.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN69:
            AYIIN69.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN70:
            AYIIN70.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN71:
            AYIIN71.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN72:
            AYIIN72.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN73:
            AYIIN73.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN74:
            AYIIN74.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN75:
            AYIIN75.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN76:
            AYIIN76.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN77:
            AYIIN77.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN78:
            AYIIN78.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN79:
            AYIIN79.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN80:
            AYIIN80.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN81:
            AYIIN81.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN82:
            AYIIN82.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN83:
            AYIIN83.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN84:
            AYIIN84.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN85:
            AYIIN85.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN86:
            AYIIN86.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN87:
            AYIIN87.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN88:
            AYIIN88.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN89:
            AYIIN89.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN90:
            AYIIN90.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN91:
            AYIIN91.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN92:
            AYIIN92.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN93:
            AYIIN93.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN94:
            AYIIN94.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN95:
            AYIIN95.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN96:
            AYIIN96.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN97:
            AYIIN97.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN98:
            AYIIN98.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN99:
            AYIIN99.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if AYIIN100:
            AYIIN100.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        '''
        return wrapper

    return decorator


def add_handler(filter_s, func_, cmd):
    if AYIIN1:
        AYIIN1.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN2:
        AYIIN2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN3:
        AYIIN3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN4:
        AYIIN4.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN5:
        AYIIN5.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN6:
        AYIIN6.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN7:
        AYIIN7.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN8:
        AYIIN8.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN9:
        AYIIN9.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN10:
        AYIIN10.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    '''
    if AYIIN11:
        AYIIN11.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN12:
        AYIIN12.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN13:
        AYIIN13.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN14:
        AYIIN14.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN15:
        AYIIN15.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN16:
        AYIIN16.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN17:
        AYIIN17.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN18:
        AYIIN18.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN19:
        AYIIN19.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN20:
        AYIIN20.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN21:
        AYIIN21.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN22:
        AYIIN22.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN23:
        AYIIN23.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN24:
        AYIIN24.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN25:
        AYIIN25.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN26:
        AYIIN26.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN27:
        AYIIN27.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN28:
        AYIIN28.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN29:
        AYIIN29.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN30:
        AYIIN30.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN31:
        AYIIN31.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN32:
        AYIIN32.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN33:
        AYIIN33.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN34:
        AYIIN34.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN35:
        AYIIN35.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN36:
        AYIIN36.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN37:
        AYIIN37.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN38:
        AYIIN38.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN39:
        AYIIN39.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN40:
        AYIIN40.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN41:
        AYIIN41.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN42:
        AYIIN42.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN43:
        AYIIN43.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN44:
        AYIIN44.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN45:
        AYIIN45.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN46:
        AYIIN46.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN47:
        AYIIN47.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN48:
        AYIIN48.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN49:
        AYIIN49.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN50:
        AYIIN50.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN51:
        AYIIN51.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN52:
        AYIIN52.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN53:
        AYIIN53.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN54:
        AYIIN54.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN55:
        AYIIN55.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN56:
        AYIIN56.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN57:
        AYIIN57.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN58:
        AYIIN58.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN59:
        AYIIN59.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN60:
        AYIIN60.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN61:
        AYIIN61.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN62:
        AYIIN62.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN63:
        AYIIN63.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN64:
        AYIIN64.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN65:
        AYIIN65.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN66:
        AYIIN66.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN67:
        AYIIN67.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN68:
        AYIIN68.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN69:
        AYIIN69.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN70:
        AYIIN70.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN71:
        AYIIN71.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN72:
        AYIIN72.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN73:
        AYIIN73.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN74:
        AYIIN74.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN75:
        AYIIN75.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN76:
        AYIIN76.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN77:
        AYIIN77.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN78:
        AYIIN78.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN79:
        AYIIN79.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN80:
        AYIIN80.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN81:
        AYIIN81.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN82:
        AYIIN82.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN83:
        AYIIN83.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN84:
        AYIIN84.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN85:
        AYIIN85.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN86:
        AYIIN86.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN87:
        AYIIN87.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN88:
        AYIIN88.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN89:
        AYIIN89.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN90:
        AYIIN90.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN91:
        AYIIN91.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN92:
        AYIIN92.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN93:
        AYIIN93.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN94:
        AYIIN94.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN95:
        AYIIN95.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN96:
        AYIIN96.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN97:
        AYIIN97.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN98:
        AYIIN98.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN99:
        AYIIN99.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if AYIIN100:
        AYIIN100.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    '''
