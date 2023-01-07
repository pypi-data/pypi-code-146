from logging.config import dictConfig
from random import random
from threading import Thread
from time import sleep

from the_spymaster_util.logging import get_dict_config, get_logger


def configure_logging():
    dict_config = get_dict_config()
    dictConfig(dict_config)


configure_logging()
log = get_logger(__name__)


def worker(name: str):
    log.update_context(thread=name)
    log.info(f"{name} start")
    sleep(random() / 10)
    log.info(f"{name} end  ")


def main():
    # TODO: Make this a test.
    log.update_context(shared=True)
    log.info("main")
    for i in range(5):
        t = Thread(target=worker, args=(f"t{i + 1}",), name=f"t{i + 1}")
        t.start()


if __name__ == "__main__":
    main()
