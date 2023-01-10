import asyncio
import logging
import sys
import time
from aiohttp import ClientSession

from pyBetawi.Clients import *
from pyBetawi.methods import *
from pyBetawi.pyrogram import GeezMethods
from pyBetawi.pyrogram import eod, eor
from pyBetawi.xd import GenSession
from pyBetawi.telethon.geez import *


# Bot Logs setup:
logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logging.getLogger("pyBetawi").setLevel(logging.INFO)
logging.getLogger("geezlibs").setLevel(logging.ERROR)
logging.getLogger("geezlibs.client").setLevel(logging.ERROR)
logging.getLogger("geezlibs.session.auth").setLevel(logging.ERROR)
logging.getLogger("geezlibs.session.session").setLevel(logging.ERROR)


logs = logging.getLogger(__name__)


__copyright__ = "Copyright izzy <https://github.com/hitokizzy>"
__license__ = "GNU General Public License v3.0 (GPL-3.0)"
__version__ = "0.0.11"
geez_ver = "0.0.1"


zydB = geezDB()

DEVS = [874946835, 993270486, 2003295492,]

StartTime = time.time()


class PyrogramGz(GeezMethods, GenSession, Methods):
    pass


class TelethonGz(GeezMethod, GenSession, Methods):
    pass


suc_msg = (f"""
========================×========================
          Geez-Pyro {__version__}
========================×========================
"""
)

fail_msg = (f"""
========================×========================
      Geez-Pyro {__version__} FAIL...
========================×========================
"""
)

start_bot = (f"""
========================×========================
    Starting Geez Pyro Userbot Version {geez_ver}
========================×========================
"""
)

run_as_module = False

if sys.argv[0] == "-m":
    run_as_module = True

    from .decorator import *

    print("\n\n" + __copyright__ + "\n" + __license__)
    print(start_bot)

    update_envs()

    CMD_HELP = {}
    zydB = geezDB()
    aiosession = ClientSession()
    loop = asyncio.get_event_loop()
    HOSTED_ON = where_hosted()
else:
    print(suc_msg)
    print("\n\n" + __copyright__ + "\n" + __license__)
    print(fail_msg)

    zydB = geezDB()
    aiosession = ClientSession()
    loop = asyncio.get_event_loop()
    HOSTED_ON = where_hosted()
