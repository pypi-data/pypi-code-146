import logging
from pyffmpeg import FFmpeg
from .. import MACROS


if not MACROS.DEBUG_MODE:
    logging.getLogger("pyffmpeg").setLevel("ERROR")

ff = FFmpeg()
