# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinChat & t.me/AyiinSupport

from ._wrappers import eod, eor
from .func import Function
from .misc import Misc
from .pastebin import PasteBin, paste, post, s_paste
from .sections import section
from .toolbot import ToolBot
from .tools import Tools


class AyiinMethods(
    Function,
    Misc,
    ToolBot,
    Tools,
):
    pass
