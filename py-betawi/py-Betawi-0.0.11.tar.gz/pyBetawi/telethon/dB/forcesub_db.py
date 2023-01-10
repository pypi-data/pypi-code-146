from .. import zydB


def get_chats():
    return zydB.get_key("FORCESUB") or {}


def add_forcesub(chat_id, chattojoin):
    omk = get_chats()
    omk.update({chat_id: chattojoin})
    return zydB.set_key("FORCESUB", omk)


def get_forcesetting(chat_id):
    omk = get_chats()
    if chat_id in omk.keys():
        return omk[chat_id]


def rem_forcesub(chat_id):
    omk = get_chats()
    if chat_id in omk.keys():
        try:
            del omk[chat_id]
            return zydB.set_key("FORCESUB", omk)
        except KeyError:
            return False
