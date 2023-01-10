# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

from .. import zydB


def get_channels():  # Returns List
    return zydB.get_key("BROADCAST") or []


def is_channel_added(id_):
    return id_ in get_channels()


def add_channel(id_):
    channels = get_channels()
    if id_ not in channels:
        channels.append(id_)
        zydB.set_key("BROADCAST", channels)
    return True


def rem_channel(id_):
    channels = get_channels()
    if id_ in channels:
        channels.remove(id_)
        zydB.set_key("BROADCAST", channels)
        return True
    return False
