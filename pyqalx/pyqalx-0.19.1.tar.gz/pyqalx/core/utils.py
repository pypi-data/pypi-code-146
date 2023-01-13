from datetime import datetime

import colorama
import logging
from colorama import Fore, Back, Style

APPNAME = "qalx"
APPAUTHOR = "agiletek"


def _msg_user(
    msg,
    log,
    title="pyqalx",
    fore=Fore.WHITE,
    back=Back.BLACK,
    level=logging.DEBUG,
):
    """
    Sends a coloured message to the user and also writes the message
    to the logs
    :param msg: The msg that should be logged
    :param title: The title to print to the console
    :param fore: The foreground colour
    :param back: The background color
    :param log: The log to use to log the message.
    If `NoneType` then don't log
    :param level: The loglevel
    """
    colorama.init()
    bright = Style.BRIGHT
    normal = Style.NORMAL
    if level == logging.ERROR or fore == Fore.RED:
        # Ensure any errors - or those with a RED foreground are displayed
        # using a BRIGHT style
        fore = Fore.RED
        normal = Style.BRIGHT
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = f"[{now}] {title}"
    title = bright, fore, back, f"{title}:", normal
    message = fore, back, msg, Style.RESET_ALL
    print(*title, *message)

    if log is not None:
        log.log(level=level, msg=msg)
