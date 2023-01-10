import os
import sys
from re import sub
from time import time

from geezlibs import Client, enums

admins_in_chat = {}


class Misc(object):
    async def list_admins(client: Client, chat_id: int):
        global admins_in_chat
        if chat_id in admins_in_chat:
            interval = time() - admins_in_chat[chat_id]["last_updated_at"]
            if interval < 3600:
                return admins_in_chat[chat_id]["data"]
    
        admins_in_chat[chat_id] = {
            "last_updated_at": time(),
            "data": [
                member.user.id
                async for member in client.get_chat_members(
                    chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
                )
            ],
        }
        return admins_in_chat[chat_id]["data"]
    
    
    async def extract_userid(message, text: str):
        def is_int(text: str):
            try:
                int(text)
            except ValueError:
                return False
            return True
    
        text = text.strip()
    
        if is_int(text):
            return int(text)
    
        entities = message.entities
        app = message._client
        if len(entities) < 2:
            return (await app.get_users(text)).id
        entity = entities[1]
        if entity.type == "mention":
            return (await app.get_users(text)).id
        if entity.type == "text_mention":
            return entity.user.id
        return None
    
    
    async def extract_user_and_reason(self, message, sender_chat=False):
        args = message.text.strip().split()
        text = message.text
        user = None
        reason = None
        if message.reply_to_message:
            reply = message.reply_to_message
            if not reply.from_user:
                if (
                    reply.sender_chat
                    and reply.sender_chat != message.chat.id
                    and sender_chat
                ):
                    id_ = reply.sender_chat.id
                else:
                    return None, None
            else:
                id_ = reply.from_user.id
    
            if len(args) < 2:
                reason = None
            else:
                reason = text.split(None, 1)[1]
            return id_, reason
    
        if len(args) == 2:
            user = text.split(None, 1)[1]
            return await self.extract_userid(message, user), None
    
        if len(args) > 2:
            user, reason = text.split(None, 2)[1:]
            return await self.extract_userid(message, user), reason
    
        return user, reason
    
    
    async def extract_user(self, message):
        return (await self.extract_user_and_reason(message))[0]
    
    
    async def extract_args(message, html=True):
        if not (message.text or message.caption):
            return ""
    
        text = message.text or message.caption
    
        text = text.html if html else text
        if " " not in text:
            return ""
    
        text = sub(r"\s+", " ", text)
        text = text[text.find(" "):].strip()
        return text
    
    
    async def extract_args_arr(self, message, html=True):
        return self.extract_args(message, html).split()
