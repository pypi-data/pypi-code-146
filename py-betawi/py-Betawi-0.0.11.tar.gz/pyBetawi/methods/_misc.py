from time import time
from datetime import datetime

from geezlibs import __version__ as geezlibs_ver, Client
from geezlibs.enums import ParseMode
from geezlibs.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InlineQueryResultPhoto,
    InputTextMessageContent,
)
from platform import python_version

from ..config import Var as Variable
from ..Clients import *

from ._database import geezDB
from .hosting import where_hosted

zydB = geezDB()
var = Variable()
HOSTED_ON = where_hosted()


class _Misc(object):
    async def alive(self, cb: str):
        from pyBetawi import __version__, geez_ver
        from pyBetawi import CMD_HELP
        
        output = (
            f"**[Geez-Pyro](https://github.com/hitokizzy/Geez-Pyro)**\n\n"
            f"**{var.ALIVE_TEXT}**\n\n"
            f"---------------------\n"
            f"**Database:** •[{zydB.name}]•\n"
            f"**Modules :** `{len(CMD_HELP)} Modules` \n"
            f"**Python:** `{python_version()}`\n"
            f"**Geez-Libs :** `{geezlibs_ver}`\n"
            f"**Unicorn version:** `{__version__}`\n"
            f"**Geez Pyro Version:** `{geez_ver}` [{HOSTED_ON}]\n"
            "------------------------\n\n"
        )
        buttons = [
            [
                InlineKeyboardButton("Help", callback_data=cb),
            ]
        ]
        results=[
            (
                InlineQueryResultPhoto(
                    photo_url=Var.ALIVE_PIC,
                    title="Alive",
                    description="inline Geez-Pyro.",
                    caption=output,
                    reply_markup=InlineKeyboardMarkup(
                        buttons
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
            )
        ]
        return results
    
    async def info_inline_func(self, client: Client, answers, peer):
        not_found = InlineQueryResultArticle(
            title="PEER NOT FOUND",
            input_message_content=InputTextMessageContent("PEER NOT FOUND"),
        )
        try:
            user = await client.get_users(peer)
            caption, _ = await self.get_user_info(user, True)
        except IndexError:
            try:
                chat = await client.get_chat(peer)
                caption, _ = await self.get_chat_info(chat, True)
            except Exception:
                return [not_found]
        except Exception:
            return [not_found]

        answers.append(
            InlineQueryResultArticle(
                title="Found Peer.",
                input_message_content=InputTextMessageContent(
                    caption, disable_web_page_preview=True
                ),
            )
        )
    
    
