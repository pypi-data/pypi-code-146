from pathlib import Path

from .. import MACROS


def PRINTSCREEN(filename):
    f = Path(filename)
    MACROS.CMD = [{"cmd":"PRINTSCREEN", "png":str(f.with_suffix(".png")), "suffix":str(f.suffix)}]
    return MACROS.localization("PrintScreenHint")
