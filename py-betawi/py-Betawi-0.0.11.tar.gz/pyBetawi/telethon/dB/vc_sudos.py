from .. import zydB


def get_vcsudos():
    return zydB.get_key("VC_SUDOS") or []


def is_vcsudo(id):
    return id in get_vcsudos()


def add_vcsudo(id):
    sudos = get_vcsudos()
    sudos.append(id)
    return zydB.set_key("VC_SUDOS", sudos)


def del_vcsudo(id):
    if is_vcsudo(id):
        sudos = get_vcsudos()
        sudos.remove(id)
        return zydB.set_key("VC_SUDOS", sudos)
