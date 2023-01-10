from .. import zydB


def night_grps():
    return zydB.get_key("NIGHT_CHATS") or []


def add_night(chat):
    chats = night_grps()
    if chat not in chats:
        chats.append(chat)
        return zydB.set_key("NIGHT_CHATS", chats)
    return


def rem_night(chat):
    chats = night_grps()
    if chat in chats:
        chats.remove(chat)
        return zydB.set_key("NIGHT_CHATS", chats)
