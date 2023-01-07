from . import _cmd as __cmd
from . import _api as __api
from .utils import clean_port

# ---- error日志 ----
from loguru import logger
logger.add(open("error.log", "a+", encoding="utf8"), level="ERROR")
