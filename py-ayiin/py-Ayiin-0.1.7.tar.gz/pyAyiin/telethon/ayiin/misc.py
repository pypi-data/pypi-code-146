# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/pyUltroid/blob/main/LICENSE/>.
#
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import base64
import os
import os.path
from io import BytesIO

import aiohttp
from aiohttp import ContentTypeError
from PIL import Image
from telethon.tl import types
from telethon.utils import get_display_name, get_peer_id

DEVS = [1905050903, 1965424892]


_entities = {
    types.MessageEntityPhone: "phone_number",
    types.MessageEntityMention: "mention",
    types.MessageEntityBold: "bold",
    types.MessageEntityCashtag: "cashtag",
    types.MessageEntityStrike: "strikethrough",
    types.MessageEntityHashtag: "hashtag",
    types.MessageEntityEmail: "email",
    types.MessageEntityMentionName: "text_mention",
    types.MessageEntityUnderline: "underline",
    types.MessageEntityUrl: "url",
    types.MessageEntityTextUrl: "text_link",
    types.MessageEntityBotCommand: "bot_command",
    types.MessageEntityCode: "code",
    types.MessageEntityPre: "pre",
}


class Misc_(object):
    async def _format_quote(
        self,
        event,
        reply=None,
        sender=None,
        type_="private"
    ):
        async def telegraph(self, file_):
            file = f"{file_}.png"
            Image.open(file_).save(file, "PNG")
            files = {"file": open(file, "rb").read()}
            uri = (
                "https://telegra.ph"
                + (
                    await self.async_searcher(
                        "https://telegra.ph/upload", post=True, data=files, re_json=True
                    )
                )[0]["src"]
            )
            os.remove(file)
            os.remove(file_)
            return uri

        if reply:
            reply = {
                "name": get_display_name(reply.sender) or "Deleted Account",
                "text": reply.raw_text,
                "chatId": reply.chat_id,
            }
        else:
            reply = {}
        is_fwd = event.fwd_from
        name = None
        last_name = None
        if sender and sender.id not in DEVS:
            id_ = get_peer_id(sender)
            name = get_display_name(sender)
        elif not is_fwd:
            id_ = event.sender_id
            sender = await event.get_sender()
            name = get_display_name(sender)
        else:
            id_, sender = None, None
            name = is_fwd.from_name
            if is_fwd.from_id:
                id_ = get_peer_id(is_fwd.from_id)
                try:
                    sender = await event.client.get_entity(id_)
                    name = get_display_name(sender)
                except ValueError:
                    pass
        if sender and hasattr(sender, "last_name"):
            last_name = sender.last_name
        entities = []
        if event.entities:
            for entity in event.entities:
                if type(entity) in _entities:
                    enti_ = entity.to_dict()
                    del enti_["_"]
                    enti_["type"] = _entities[type(entity)]
                    entities.append(enti_)
        message = {
            "entities": entities,
            "chatId": id_,
            "avatar": True,
            "from": {
                "id": id_,
                "first_name": (name or (sender.first_name if sender else None))
                or "Deleted Account",
                "last_name": last_name,
                "username": sender.username if sender else None,
                "language_code": "en",
                "title": name,
                "name": name or "Unknown",
                "type": type_,
            },
            "text": event.raw_text,
            "replyMessage": reply,
        }
        if event.document and event.document.thumbs:
            file_ = await event.download_media(thumb=-1)
            uri = await self.telegraph(file_)
            message["media"] = {"url": uri}

        return message


    async def create_quotly(
        self,
        event,
        url="https://qoute-api-akashpattnaik.koyeb.app/generate",
        reply={},
        bg=None,
        sender=None,
        file_name="quote.webp",
    ):
        O_API = "https://bot.lyo.su/quote/generate"
        if not isinstance(event, list):
            event = [event]
            url = O_API
        if not bg:
            bg = "#1b1429"
        content = {
            "type": "quote",
            "format": "webp",
            "backgroundColor": bg,
            "width": 512,
            "height": 768,
            "scale": 2,
            "messages": [
                await self._format_quote(message, reply=reply, sender=sender)
                for message in event
            ],
        }
        try:
            request = await self.async_searcher(url, post=True, json=content, re_json=True)
        except ContentTypeError as er:
            if url != O_API:
                return await self.create_quotly(event,
                        url=O_API,
                        bg=bg,
                        sender=sender,
                        reply=reply,
                        file_name=file_name,
                )
            raise er
        if request.get("ok"):
            with open(file_name, "wb") as file:
                image = base64.decodebytes(request["result"]["image"].encode("utf-8"))
                file.write(image)
            return file_name
        raise Exception(str(request))


    async def Carbon(
        self,
        code,
        base_url="https://carbonara-42.herokuapp.com/api/cook",
        file_name="Ayiin-Userbot",
        **kwargs,
    ):
        kwargs["code"] = code
        con = await self.async_searcher(base_url, post=True, json=kwargs, re_content=True)
        file = BytesIO(con)
        file.name = f"{file_name}.jpg"
        return file


    async def animator(
        self,
        media,
        mainevent,
        textevent
    ):
        # Coded by @Jisan7509
        h = media.file.height
        w = media.file.width
        w, h = (-1, 512) if h > w else (512, -1)
        if not os.path.isdir(self.TEMP_DOWNLOAD_DIRECTORY):
            os.makedirs(self.TEMP_DOWNLOAD_DIRECTORY)
        Ayiin = await mainevent.client.download_media(media, self.TEMP_DOWNLOAD_DIRECTORY)
        await textevent.edit("`Converting...`")
        await self.run_cmd(
            f"ffmpeg -ss 00:00:00 -to 00:00:02.900 -i {Ayiin} -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an Video.webm"
        )
        os.remove(Ayiin)
        vid = "Video.webm"
        return vid
