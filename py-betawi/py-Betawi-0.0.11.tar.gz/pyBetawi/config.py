import sys

from os import getenv

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


MSG_PERMIT = (
    """
╭┈──────────────────────
│“𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐓𝐡𝐞 𝐏𝐫𝐢𝐯𝐚𝐜𝐲 𝐌𝐞𝐬𝐬𝐚𝐠𝐞”
├┈────────────────────
│𝗗𝗜𝗟𝗔𝗥𝗔𝗡𝗚 𝗠𝗘𝗟𝗔𝗞𝗨𝗞𝗔𝗡 𝗦𝗣𝗔𝗠𝗠𝗜𝗡𝗚❗
│𝘒𝘢𝘳𝘦𝘯𝘢 𝘚𝘢𝘺𝘢 𝘈𝘬𝘢𝘯 𝘖𝘵𝘰𝘮𝘢𝘵𝘪𝘴 𝘔𝘦𝘮𝘣𝘭𝘰𝘬𝘪𝘳𝘈𝘯𝘥𝘢, 
|𝘛𝘶𝘯𝘨𝘨𝘶 𝘚𝘢𝘮𝘱𝘢𝘪 𝘗𝘦𝘮𝘪𝘭𝘪𝘬 𝘚𝘢𝘺𝘢
│𝘔𝘦𝘯𝘦𝘳𝘪𝘮𝘢 𝘗𝘦𝘴𝘢𝘯 𝘈𝘯𝘥𝘢, 𝘛𝘦𝘳𝘪𝘮𝘢𝘬𝘢𝘴𝘪𝘩
├┈──────────────────────
│ ○› `AUTOMATIC MESSAGES`
│ ○› `BY` Geez Pyro!
╰┈────────────────"
"""
)



class Var(object):
    # mandatory
    API_ID = int(getenv("API_ID"))
    API_HASH = str(getenv("API_HASH"))
    # Extras
    ALIVE_PIC = getenv("ALIVE_PIC", "https://telegra.ph/file/c78bb1efdeed38ee16eb2.png")
    ALIVE_TEXT = getenv("ALIVE_TEXT", "Geez Pyro Userbot")
    # Telethon Session
    STRING_1 = getenv("STRING_1", "")
    STRING_2 = getenv("STRING_2", "")
    STRING_3 = getenv("STRING_3", "")
    STRING_4 = getenv("STRING_4", "")
    STRING_5 = getenv("STRING_5", "")
    STRING_6 = getenv("STRING_6", "")
    STRING_7 = getenv("STRING_7", "")
    STRING_8 = getenv("STRING_8", "")
    STRING_9 = getenv("STRING_9", "")
    STRING_10 = getenv("STRING_10", "")
    
    # Pyrogram Session
    SESSION_1 = getenv("SESSION_1", "")
    SESSION_2 = getenv("SESSION_2", "")
    SESSION_3 = getenv("SESSION_3", "")
    SESSION_4 = getenv("SESSION_4", "")
    SESSION_5 = getenv("SESSION_5", "")
    SESSION_6 = getenv("SESSION_6", "")
    SESSION_7 = getenv("SESSION_7", "")
    SESSION_8 = getenv("SESSION_8", "")
    SESSION_9 = getenv("SESSION_9", "")
    SESSION_10 = getenv("SESSION_10", "")
    # For Handler
    HNDLR = getenv("HNDLR", [".", "!", "*", "^", "-", "?"])
    # Database
    REDIS_URI = (
        getenv("REDIS_URI", None) or getenv("REDIS_URL", None)
    )
    REDIS_PASSWORD = getenv("REDIS_PASSWORD", None)
    # extras
    BOT_TOKEN = getenv("BOT_TOKEN")
    LOG_CHAT = int(getenv("LOG_CHAT") or 0)
    HEROKU_APP_NAME = getenv("HEROKU_APP_NAME", None)
    HEROKU_API = getenv("HEROKU_API", None)
    TEMP_DOWNLOAD_DIRECTORY = getenv("TEMP_DOWNLOAD_DIRECTORY", "./downloads")
    NO_LOAD = [int(x) for x in getenv("NO_LOAD", "").split()]
    TZ = getenv("TZ", "Asia/Jakarta")
    PMPERMIT = bool(getenv("PMPERMIT", True))
    PERMIT_MSG = str(getenv("PERMIT_MSG", MSG_PERMIT))
    PERMIT_LIMIT = int(getenv("PERMIT_LIMIT", 6))
    # for railway
    REDISPASSWORD = getenv("REDISPASSWORD", None)
    REDISHOST = getenv("REDISHOST", None)
    REDISPORT = getenv("REDISPORT", None)
    REDISUSER = getenv("REDISUSER", None)
    # for sql
    DATABASE_URL = getenv("DATABASE_URL", None)
    # for MONGODB users
    MONGO_URI = getenv("MONGO_URI", None)
    # for Okteto Platform
    OKTETO = bool(getenv("OKTETO", False))
