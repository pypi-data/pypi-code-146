import logging
from datetime import datetime
from traceback import format_exc
import pytz
from geezlibs import ContinuePropagation, StopPropagation, filters
from geezlibs.enums import ChatMemberStatus, ChatType
from geezlibs.errors.exceptions.bad_request_400 import (
    MessageIdInvalid,
    MessageNotModified,
    MessageEmpty,
    UserNotParticipant
)
from geezlibs.handlers import MessageHandler

from pyBetawi.pyrogram import eor

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


def Geez(
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
                    message, "<code>This Command Only Works, If You Are Admin Of The Chat!</code>"
                )
                return
            if group_only and chat_type != (
                    ChatType.GROUP or ChatType.SUPERGROUP):
                await eor(message, "<code>Are you sure this is a group?</code>")
                return
            if channel_only and chat_type != ChatType.CHANNEL:
                await eor(message, "This Command Only Works In Channel!")
                return
            if pm_only and chat_type != ChatType.PRIVATE:
                await eor(message, "<code>This Cmd Only Works On PM!</code>")
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
        if GEEZ1:
            GEEZ1.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ2:
            GEEZ2.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ3:
            GEEZ3.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ4:
            GEEZ4.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ5:
            GEEZ5.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ6:
            GEEZ6.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ7:
            GEEZ7.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ8:
            GEEZ8.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ9:
            GEEZ9.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ10:
            GEEZ10.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        '''
        if GEEZ11:
            GEEZ11.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ12:
            GEEZ12.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ13:
            GEEZ13.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ14:
            GEEZ14.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ15:
            GEEZ15.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ16:
            GEEZ16.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ17:
            GEEZ17.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ18:
            GEEZ18.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ19:
            GEEZ19.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ20:
            GEEZ20.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ21:
            GEEZ21.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ22:
            GEEZ22.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ23:
            GEEZ23.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ24:
            GEEZ24.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ25:
            GEEZ25.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ26:
            GEEZ26.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ27:
            GEEZ27.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ28:
            GEEZ28.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ29:
            GEEZ29.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ30:
            GEEZ30.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ31:
            GEEZ31.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ32:
            GEEZ32.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ33:
            GEEZ33.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ34:
            GEEZ34.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ35:
            GEEZ35.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ36:
            GEEZ36.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ37:
            GEEZ37.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ38:
            GEEZ38.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ39:
            GEEZ39.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ40:
            GEEZ40.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ41:
            GEEZ41.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ42:
            GEEZ42.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ43:
            GEEZ43.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ44:
            GEEZ44.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ45:
            GEEZ45.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ46:
            GEEZ46.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ47:
            GEEZ47.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ48:
            GEEZ48.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ49:
            GEEZ49.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ50:
            GEEZ50.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ51:
            GEEZ51.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ52:
            GEEZ52.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ53:
            GEEZ53.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ54:
            GEEZ54.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ55:
            GEEZ55.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ56:
            GEEZ56.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ57:
            GEEZ57.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ58:
            GEEZ58.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ59:
            GEEZ59.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ60:
            GEEZ60.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ61:
            GEEZ61.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ62:
            GEEZ62.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ63:
            GEEZ63.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ64:
            GEEZ64.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ65:
            GEEZ65.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ66:
            GEEZ66.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ67:
            GEEZ67.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ68:
            GEEZ68.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ69:
            GEEZ69.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ70:
            GEEZ70.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ71:
            GEEZ71.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ72:
            GEEZ72.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ73:
            GEEZ73.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ74:
            GEEZ74.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ75:
            GEEZ75.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ76:
            GEEZ76.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ77:
            GEEZ77.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ78:
            GEEZ78.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ79:
            GEEZ79.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ80:
            GEEZ80.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ81:
            GEEZ81.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ82:
            GEEZ82.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ83:
            GEEZ83.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ84:
            GEEZ84.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ85:
            GEEZ85.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ86:
            GEEZ86.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ87:
            GEEZ87.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ88:
            GEEZ88.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ89:
            GEEZ89.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ90:
            GEEZ90.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ91:
            GEEZ91.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ92:
            GEEZ92.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ93:
            GEEZ93.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ94:
            GEEZ94.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ95:
            GEEZ95.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ96:
            GEEZ96.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ97:
            GEEZ97.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ98:
            GEEZ98.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ99:
            GEEZ99.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        if GEEZ100:
            GEEZ100.add_handler(
                MessageHandler(
                    wrapper,
                    filters=filter_s),
                group=0)
        '''
        return wrapper

    return decorator


def add_handler(filter_s, func_, cmd):
    if GEEZ1:
        GEEZ1.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ2:
        GEEZ2.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ3:
        GEEZ3.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ4:
        GEEZ4.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ5:
        GEEZ5.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ6:
        GEEZ6.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ7:
        GEEZ7.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ8:
        GEEZ8.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ9:
        GEEZ9.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ10:
        GEEZ10.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    '''
    if GEEZ11:
        GEEZ11.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ12:
        GEEZ12.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ13:
        GEEZ13.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ14:
        GEEZ14.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ15:
        GEEZ15.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ16:
        GEEZ16.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ17:
        GEEZ17.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ18:
        GEEZ18.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ19:
        GEEZ19.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ20:
        GEEZ20.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ21:
        GEEZ21.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ22:
        GEEZ22.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ23:
        GEEZ23.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ24:
        GEEZ24.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ25:
        GEEZ25.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ26:
        GEEZ26.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ27:
        GEEZ27.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ28:
        GEEZ28.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ29:
        GEEZ29.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ30:
        GEEZ30.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ31:
        GEEZ31.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ32:
        GEEZ32.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ33:
        GEEZ33.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ34:
        GEEZ34.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ35:
        GEEZ35.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ36:
        GEEZ36.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ37:
        GEEZ37.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ38:
        GEEZ38.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ39:
        GEEZ39.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ40:
        GEEZ40.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ41:
        GEEZ41.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ42:
        GEEZ42.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ43:
        GEEZ43.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ44:
        GEEZ44.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ45:
        GEEZ45.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ46:
        GEEZ46.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ47:
        GEEZ47.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ48:
        GEEZ48.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ49:
        GEEZ49.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ50:
        GEEZ50.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ51:
        GEEZ51.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ52:
        GEEZ52.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ53:
        GEEZ53.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ54:
        GEEZ54.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ55:
        GEEZ55.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ56:
        GEEZ56.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ57:
        GEEZ57.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ58:
        GEEZ58.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ59:
        GEEZ59.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ60:
        GEEZ60.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ61:
        GEEZ61.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ62:
        GEEZ62.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ63:
        GEEZ63.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ64:
        GEEZ64.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ65:
        GEEZ65.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ66:
        GEEZ66.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ67:
        GEEZ67.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ68:
        GEEZ68.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ69:
        GEEZ69.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ70:
        GEEZ70.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ71:
        GEEZ71.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ72:
        GEEZ72.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ73:
        GEEZ73.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ74:
        GEEZ74.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ75:
        GEEZ75.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ76:
        GEEZ76.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ77:
        GEEZ77.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ78:
        GEEZ78.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ79:
        GEEZ79.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ80:
        GEEZ80.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ81:
        GEEZ81.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ82:
        GEEZ82.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ83:
        GEEZ83.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ84:
        GEEZ84.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ85:
        GEEZ85.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ86:
        GEEZ86.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ87:
        GEEZ87.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ88:
        GEEZ88.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ89:
        GEEZ89.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ90:
        GEEZ90.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ91:
        GEEZ91.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ92:
        GEEZ92.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ93:
        GEEZ93.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ94:
        GEEZ94.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ95:
        GEEZ95.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ96:
        GEEZ96.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ97:
        GEEZ97.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ98:
        GEEZ98.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ99:
        GEEZ99.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    if GEEZ100:
        GEEZ100.add_handler(MessageHandler(func_, filters=filter_s), group=0)
    '''
