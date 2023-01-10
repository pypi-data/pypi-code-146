from ._wrappers import eod, eor
from .func import Function
from .misc import Misc
from .pastebin import PasteBin, paste, post, s_paste
from .sections import section
from .toolbot import ToolBot
from .tools import Tools


class GeezMethods(
    Function,
    Misc,
    ToolBot,
    Tools,
):
    pass
