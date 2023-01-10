from .. import zydB


def get_approved():
    return zydB.get_key("PMPERMIT") or []


def approve_user(id):
    ok = get_approved()
    if id in ok:
        return True
    ok.append(id)
    return zydB.set_key("PMPERMIT", ok)


def disapprove_user(id):
    ok = get_approved()
    if id in ok:
        ok.remove(id)
        return zydB.set_key("PMPERMIT", ok)


def is_approved(id):
    return id in get_approved()
