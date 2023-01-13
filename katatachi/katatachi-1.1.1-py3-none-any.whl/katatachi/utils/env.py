import os
import logging

logger = logging.getLogger(__name__)


def getenv_or_raise(env):
    if env not in os.environ:
        raise RuntimeError(f"{env} does not exist")
    return os.environ[env]


def getenv_or_meh(env, default):
    if env not in os.environ:
        logger.info(f"{env} does not exist, using default value {default}")
        return default
    return os.environ[env]
