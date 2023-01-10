from .. import zydB


def get_stuff():
    return zydB.get_key("GBLACKLISTS") or []


def add_gblacklist(id):
    ok = get_stuff()
    if id not in ok:
        ok.append(id)
        return zydB.set_key("GBLACKLISTS", ok)


def rem_gblacklist(id):
    ok = get_stuff()
    if id in ok:
        ok.remove(id)
        return zydB.set_key("GBLACKLISTS", ok)


def is_gblacklisted(id):
    return id in get_stuff()
