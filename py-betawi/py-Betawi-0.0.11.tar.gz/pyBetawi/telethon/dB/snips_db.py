from .. import zydB


def get_all_snips():
    return zydB.get_key("SNIP") or {}


def add_snip(word, msg, media, button):
    ok = get_all_snips()
    ok.update({word: {"msg": msg, "media": media, "button": button}})
    zydB.set_key("SNIP", ok)


def rem_snip(word):
    ok = get_all_snips()
    if ok.get(word):
        ok.pop(word)
        zydB.set_key("SNIP", ok)


def get_snips(word):
    ok = get_all_snips()
    if ok.get(word):
        return ok[word]
    return False


def list_snip():
    return "".join(f"👉 ${z}\n" for z in get_all_snips())
