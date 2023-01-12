import asyncio
import importlib
import sys

from fipper import idle

from pyAyiin import __version__

from . import *

from .config import Var
from .Clients.startup import StartPyrogram
from .exceptions import DependencyMissingError

yins = Var()
xd = PyrogramXd()


try:
    from uvloop import install
except:
    install = None
    logs.info("'uvloop' not installed\ninstall 'uvloop' or add 'uvloop' in requirements.txt")


MSG_ON = """
<b>❏ ᴀʏɪɪɴ - ᴜʙᴏᴛ ʙᴇʀʜᴀsɪʟ ᴅɪᴀᴋᴛɪғᴋᴀɴ</b>
<b>╭╼┅━━━━━╍━━━━━┅╾</b>
<b>├▹ Pʏ-Aʏɪɪɴ Vᴇʀsɪᴏɴ</b> - •[<code>{}</code>]•
<b>├▹ Hᴏsᴛɪɴɢ</b> - <code>{}</code>
<b>├▹ Usᴇʀʙᴏᴛ Vᴇʀsɪᴏɴ</b> - <code>{}</code>
<b>├▹ Tᴏᴛᴀʟ Pʟᴜɢɪɴs</b> - <code>{}</code>
<b>╰╼┅━━━━━╍━━━━━┅╾</b>
"""

async def start_main():
    await StartPyrogram()
    try:
        await tgbot.send_message(
            yins.LOG_CHAT,
            MSG_ON.format(
                __version__,
                HOSTED_ON,
                ayiin_ver, 
                len(CMD_HELP),
            )
        )
    except BaseException as s:
        print(s)
    print(f"AyiinUbot Version - {ayiin_ver}\n[🔥 BERHASIL DIAKTIFKAN! 🔥]")
    await idle()
    await aiosession.close()

if __name__ == "__main__":
    install()
    loop.run_until_complete(start_main())
    logs.info("Stopping Ayiin Ubot! GoodBye")
