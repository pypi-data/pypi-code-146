from .. import zydB


def get_stuff(key="NSFW"):
    return zydB.get_key(key) or {}


def nsfw_chat(chat, action):
    x = get_stuff()
    x.update({chat: action})
    return zydB.set_key("NSFW", x)


def rem_nsfw(chat):
    x = get_stuff()
    if x.get(chat):
        x.pop(chat)
        return zydB.set_key("NSFW", x)


def is_nsfw(chat):
    x = get_stuff()
    if x.get(chat):
        return x[chat]


def profan_chat(chat, action):
    x = get_stuff("PROFANITY")
    x.update({chat: action})
    return zydB.set_key("PROFANITY", x)


def rem_profan(chat):
    x = get_stuff("PROFANITY")
    if x.get(chat):
        x.pop(chat)
        return zydB.set_key("PROFANITY", x)


def is_profan(chat):
    x = get_stuff("PROFANITY")
    if x.get(chat):
        return x[chat]
