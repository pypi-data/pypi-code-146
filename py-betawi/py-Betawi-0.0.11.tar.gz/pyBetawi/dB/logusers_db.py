# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import zydB


def get_logger():
    return zydB.get_key("LOGUSERS") or []


def is_logger(id_):
    return id_ in get_logger()


def log_user(id_):
    pmperm = get_logger()
    pmperm.append(id_)
    return zydB.set_key("LOGUSERS", pmperm)


def nolog_user(id_):
    pmperm = get_logger()
    pmperm.remove(id_)
    return zydB.set_key("LOGUSERS", pmperm)
