import logging


class Logger(object):
    def __init__(self, name=None):
        scan_logger = logging.getLogger(name)
        scan_logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        ch.setFormatter(formatter)
        scan_logger.addHandler(ch)

        self.logger = scan_logger


def logger(name):
    return Logger(name).logger
