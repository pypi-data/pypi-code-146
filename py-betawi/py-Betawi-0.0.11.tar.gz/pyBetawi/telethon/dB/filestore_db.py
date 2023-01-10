from .. import zydB


def get_stored():
    return zydB.get_key("FILE_STORE") or {}


def store_msg(hash, msg_id):
    all = get_stored()
    all.update({hash: msg_id})
    return zydB.set_key("FILE_STORE", all)


def list_all_stored_msgs():
    all = get_stored()
    return list(all.keys())


def get_stored_msg(hash):
    all = get_stored()
    if all.get(hash):
        return all[hash]


def del_stored(hash):
    all = get_stored()
    all.pop(hash)
    return zydB.set_key("FILE_STORE", all)
