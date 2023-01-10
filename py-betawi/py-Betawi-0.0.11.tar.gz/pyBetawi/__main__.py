import asyncio
import importlib

from geezlibs import idle

from pyBetawi import __version__

from . import *

from .config import Var
from .Clients.startup import StartPyrogram
from .exceptions import DependencyMissingError

izzy = Var()
gz = PyrogramGz()


try:
    from uvloop import install
except:
    install = None
    logs.info("'uvloop' not installed\ninstall 'uvloop' or add 'uvloop' in requirements.txt")


MSG_ON = """
<b>Geez Pyro Userbot telah aktif</b>
<b>Geezlibs Vᴇʀsɪᴏɴ</b> - [<code>{}</code>]
"""

async def start_main():
    await StartPyrogram()
    try:
        await tgbot.send_message(
            izzy.LOG_CHAT,
            MSG_ON.format(
                __version__,
                HOSTED_ON,
                geez_ver, 
                len(CMD_HELP),
            )
        )
    except BaseException as s:
        print(s)
    print(f"Geez Pyro Userbot Versi - {geez_ver}\n[ BERHASIL DIAKTIFKAN! ]")
    await idle()
    await aiosession.close()

if __name__ == "__main__":
    install()
    loop.run_until_complete(start_main())
    logs.info("Geez Pyro berhasil dimatikan")
