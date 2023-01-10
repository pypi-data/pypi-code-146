from .. import zydB


def get_stuff():
    return zydB.get_key("ASST_CMDS") or {}


def add_cmd(cmd, msg, media, button):
    ok = get_stuff()
    ok.update({cmd: {"msg": msg, "media": media, "button": button}})
    return zydB.set_key("ASST_CMDS", ok)


def rem_cmd(cmd):
    ok = get_stuff()
    if ok.get(cmd):
        ok.pop(cmd)
        return zydB.set_key("ASST_CMDS", ok)


def cmd_reply(cmd):
    ok = get_stuff()
    if ok.get(cmd):
        okk = ok[cmd]
        return okk["msg"], okk["media"], okk["button"] if ok.get("button") else None
    return


def list_cmds():
    ok = get_stuff()
    return ok.keys()
