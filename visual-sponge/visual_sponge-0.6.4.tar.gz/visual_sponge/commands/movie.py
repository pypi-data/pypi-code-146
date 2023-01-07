from pathlib import Path

from .. import MACROS


def MOVIE(filename, fps=60, bitRate=8500000, start=0, stop=-1, stride=1, interval=100):
    f = Path(filename)
    MACROS.CMD = [{"cmd":"MOVIE",
                   "webm":str(f.with_suffix(".webm")),
                   "suffix":str(f.suffix),
                   "interval":interval,
                   "fps":fps,
                   "bitRate":bitRate,
                   "start":start,
                   "stop":stop,
                   "stride":stride}]
    return MACROS.localization("MovieHint")
