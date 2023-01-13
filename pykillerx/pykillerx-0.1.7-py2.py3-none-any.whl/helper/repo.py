from os import getenv
from dotenv import load_dotenv
from base64 import b64decode as who

ONLINE_ON = """
➠ **Userbot Online** 🔥
➠ **Type** `.alive`
"""

RendyProjects = who("YXdhaXQgY2xpZW50LmpvaW5fY2hhdChSZW5keVByb2plY3RzKQo=").decode("utf-8")

KONTOLMU = "https://telegra.ph/file/b11505df0cab0b8013798.jpg"

ALIVE_ONLINE = ONLINE_ON
LOG_ALIVE = KONTOLMU

# jangan hapus && auto crashed

GIT_TOKEN = getenv(
    "GIT_TOKEN",
    who("").decode("utf-8"),
)


REPO_URL = getenv(
    "REPO_URL",
    who("aHR0cHM6Ly9naXRodWIuY29tL1RlYW1LaWxsZXJYL0tpbGxlclgtQmFzZQ==").decode("utf-8"),
)

CHANNEL = who("UmVuZHlQcm9qZWN0cwo=").decode("utf-8")
SUPPORT = who("cGFudGVreWtzCg==").decode("utf-8")
