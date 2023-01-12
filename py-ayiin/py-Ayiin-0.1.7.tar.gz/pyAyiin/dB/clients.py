import random

from .. import *
#from ..Clients import 


assistantdict = {}


async def get_client(assistant: int):
    if int(assistant) == 1:
        return AYIIN1
    elif int(assistant) == 2:
        return AYIIN2
    elif int(assistant) == 3:
        return AYIIN3
    elif int(assistant) == 4:
        return AYIIN4
    elif int(assistant) == 5:
        return AYIIN5


async def set_assistant(chat_id):    
    ran_assistant = random.choice(clients)
    assistantdict[chat_id] = ran_assistant
    if not assistantdict.get("CLIENT"):
        try:
            assistantdict[chat_id].update({'assistant':  ran_assistant})
        except Exception:
            assistantdict.update({chat_id: {'assistant': ran_assistant}})
    '''
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    '''
    userbot = await get_client(ran_assistant)
    return userbot


async def get_assistant(chat_id: int) -> str:
    assistant = assistantdict.get(chat_id)
    if assistant:
        if assistant in clients:
            userbot = await get_client(assistant)
            return userbot
        else:
            userbot = await set_assistant(chat_id)
            return userbot


async def set_calls_assistant(chat_id):
    ran_assistant = random.choice(clients)
    assistantdict[chat_id] = ran_assistant
    if not assistantdict.get("CLIENT"):
        try:
            assistantdict[chat_id].update({'assistant':  ran_assistant})
        except Exception:
            assistantdict.update({chat_id: {'assistant': ran_assistant}})
    '''
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    '''
    return ran_assistant


async def group_assistant(chat_id: int) -> int:
    assistant = assistantdict.get(chat_id)
    if assistant:
        if assistant in clients:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)
    if int(assis) == 1:
        return AYIIN1
    elif int(assis) == 2:
        return AYIIN2
    elif int(assis) == 3:
        return AYIIN3
    elif int(assis) == 4:
        return AYIIN4
    elif int(assis) == 5:
        return AYIIN5
