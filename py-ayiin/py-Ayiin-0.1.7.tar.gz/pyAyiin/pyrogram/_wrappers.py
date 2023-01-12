import logging

from asyncio import sleep

from fipper.enums import MessageServiceType
from fipper.errors import MessageDeleteForbidden, MessageNotModified
from fipper.types import Message


LOGS = logging.getLogger(__name__)

"""
servis = (
    MessageServiceType.NEW_CHAT_MEMBERS,
    MessageServiceType.LEFT_CHAT_MEMBERS,
    MessageServiceType.NEW_CHAT_TITLE,
    MessageServiceType.NEW_CHAT_PHOTO,
    MessageServiceType.DELETE_CHAT_PHOTO,
    MessageServiceType.GROUP_CHAT_CREATED,
    MessageServiceType.CHANNEL_CHAT_CREATED,
    MessageServiceType.MIGRATE_TO_CHAT_ID,
    MessageServiceType.MIGRATE_FROM_CHAT_ID,
    MessageServiceType.PINNED_MESSAGE,
    MessageServiceType.GAME_HIGH_SCORE,
    MessageServiceType.VIDEO_CHAT_STARTED,
    MessageServiceType.VIDEO_CHAT_ENDED,
    MessageServiceType.VIDEO_CHAT_SCHEDULED,
    MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED,
)
"""

async def eor(message, text=None, **args):
    time = args.get("time", None)
    edit_time = args.get("edit_time", None)
    if "edit_time" in args:
        del args["edit_time"]
    if "time" in args:
        del args["time"]
    if "link_preview" not in args:
        args["disable_web_page_preview"] = False
    args["reply_to_message_id"] = message.reply_to_message or message
    if message.outgoing:
        if edit_time:
            await sleep(edit_time)
        if "file" in args and args["file"] and not message.media:
            await message.delete()
            ok = await message.client.send_message(message.chat.id, text, **args)
        else:
            try:
                try:
                    del args["reply_to_message_id"]
                except KeyError:
                    pass
                ok = await message.edit(text, **args)
            except MessageNotModified:
                ok = message
    else:
        ok = await message.client.send_message(message.chat.id, text, **args)

    if time:
        await sleep(time)
        return await ok.delete()
    return ok


async def eod(message, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(message, text, **kwargs)


async def _try_delete(message):
    try:
        return await message.delete()
    except (MessageDeleteForbidden):
        pass
    except BaseException as er:
        LOGS.error("Error while Deleting Message..")
        LOGS.exception(er)


setattr(Message, "eor", eor)
setattr(Message, "try_delete", _try_delete)
