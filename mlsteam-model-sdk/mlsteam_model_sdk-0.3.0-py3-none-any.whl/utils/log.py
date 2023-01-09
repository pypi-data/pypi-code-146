import logging
import sys


DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def setup_logging():
    formatter = logging.Formatter(
        fmt='%(asctime)s %(name)s [%(levelname)s]: %(message)s',
        datefmt=DATE_FORMAT,
    )

    # mlsteam logger
    main_logger = logging.getLogger('mlsteam-model-sdk')
    main_logger.setLevel(logging.DEBUG)
    # Log to stderr
    stdoutHandler = logging.StreamHandler(sys.stderr)
    stdoutHandler.setFormatter(formatter)
    stdoutHandler.setLevel(logging.INFO)
    main_logger.addHandler(stdoutHandler)
    return main_logger


logger = setup_logging()

null_logger = logging.getLogger('null')
null_logger.addHandler(logging.NullHandler)
