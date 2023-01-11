import atexit
import os
import sys
from loguru import logger
from ..logging_loki import LokiQueueHandler, emitter
from . import __version__
from multiprocessing import Queue
import uuid

class LogUtils():
    def _init_logging(
        url: str, 
        access_token: str,
        log_level: str):

        emitter.LokiEmitter.level_tag = "level"
        handler = LokiQueueHandler(
            Queue(1),
            url=url,
            tags={"client": "S2O.TechStack.Python"},
            version="1",
            token=access_token
        )

        logger.remove()
        logger.add(sys.stderr, level=log_level)
        logger.add(handler, level=log_level, serialize=True, backtrace=True, diagnose=True)
        logger.configure(extra={
            "PythonVersion": sys.version, 
            "Version": __version__,
            "SessionId": uuid.uuid4(),
            "MachineName": os.getenv("HOSTNAME"),
            "OsName": os.name
            })

        def _teardown_logging(handler):
            handler.listener.stop()

        atexit.register(_teardown_logging, handler)
