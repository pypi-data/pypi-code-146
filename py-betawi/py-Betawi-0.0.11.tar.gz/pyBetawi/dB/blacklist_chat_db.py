from .. import zydB


def add_black_chat(chat_id):
    chat = zydB.get_key("BLACKLIST_CHATS") or []
    if chat_id not in chat:
        chat.append(chat_id)
        return zydB.set_key("BLACKLIST_CHATS", chat)


def rem_black_chat(chat_id):
    chat = zydB.get_key("BLACKLIST_CHATS") or []
    if chat_id in chat:
        chat.remove(chat_id)
        return zydB.set_key("BLACKLIST_CHATS", chat)
