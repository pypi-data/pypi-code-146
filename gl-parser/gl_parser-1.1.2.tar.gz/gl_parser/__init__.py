"""Top-level package for GL Parser."""

__author__ = """Luis C. Berrocal"""
__email__ = 'luis.berrocal.1942@gmail.com'
__version__ = '1.1.2'

from gl_parser.config.configuration import ConfigurationManager

CONFIGURATION_MANAGER = ConfigurationManager()


def logger_configuration():
    import logging.config
    from gl_parser.settings import LOGGING
    logging.config.dictConfig(LOGGING)


logger_configuration()
