import os
import sys
from pyrogram import Client

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "KillerXBase"])

async def join(client):
    try:
        await client.join_chat("RendyProjects")
        await client.join_chat("pantekyks")
    except BaseException:
        pass
