from logging.config import dictConfig

from the_spymaster_util.logging import get_dict_config


def configure_logging():
    config = get_dict_config(std_formatter="debug")
    dictConfig(config)


configure_logging()
