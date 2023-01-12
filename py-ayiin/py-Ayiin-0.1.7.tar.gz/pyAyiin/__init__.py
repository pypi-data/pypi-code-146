# py - Ayiin
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/pyAyiin >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/pyAyiin/blob/main/LICENSE/>.
#
# FROM py-Ayiin <https://github.com/AyiinXd/pyAyiin>
# t.me/AyiinChat & t.me/AyiinSupport


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import asyncio
import logging
import sys
import time
from aiohttp import ClientSession

from pyAyiin.Clients import *
from pyAyiin.methods import *
from pyAyiin.pyrogram import AyiinMethods
from pyAyiin.pyrogram import eod, eor
from pyAyiin.xd import GenSession
from pyAyiin.telethon.ayiin import *


# Bot Logs setup:
logging.basicConfig(
    format="[%(name)s] - [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logging.getLogger("pyAyiin").setLevel(logging.INFO)
logging.getLogger("fipper").setLevel(logging.ERROR)
logging.getLogger("fipper.client").setLevel(logging.ERROR)
logging.getLogger("fipper.session.auth").setLevel(logging.ERROR)
logging.getLogger("fipper.session.session").setLevel(logging.ERROR)


logs = logging.getLogger(__name__)


__copyright__ = "Copyright (C) 2022-present AyiinXd <https://github.com/AyiinXd>"
__license__ = "GNU General Public License v3.0 (GPL-3.0)"
__version__ = "0.1.7"
ayiin_ver = "0.0.5"


adB = AyiinDB()

DEVS = [
    607067484, # Ayiin
    997461844, # Ayang_Ayiin
    1905050903, # Ayiin
    2130526178, # Alfa
]

StartTime = time.time()


class PyrogramXd(AyiinMethods, GenSession, Methods):
    pass


class TelethonXd(AyiinMethod, GenSession, Methods):
    pass


suc_msg = (f"""
========================×========================
           Credit Py-Ayiin {__version__}
========================×========================
"""
)

fail_msg = (f"""
========================×========================
      Commit Yang Bener Bego Biar Gak Error
           Credit Py-Ayiin {__version__}
========================×========================
"""
)

start_bot = (f"""
========================×========================
         Starting AyiinUbot Version {ayiin_ver}
        Copyright (C) 2022-present AyiinXd
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
    adB = AyiinDB()
    aiosession = ClientSession()
    loop = asyncio.get_event_loop()
    HOSTED_ON = where_hosted()
    Yins = VcTools()
else:
    print(suc_msg)
    print("\n\n" + __copyright__ + "\n" + __license__)
    print(fail_msg)

    adB = AyiinDB()
    aiosession = ClientSession()
    loop = asyncio.get_event_loop()
    HOSTED_ON = where_hosted()