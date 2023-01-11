import logging

logger = logging.getLogger(name="rnn-demo")

debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical


def configure(demo_level=1, root_level=logging.WARNING):
    global logger
    logging.basicConfig(
        format=
        '%(levelname)s:%(name)s:%(filename)s:%(lineno)s(%(funcName)s): %(message)s',
        level=root_level
    )
    logger.setLevel(demo_level)

    logger.info("demo level={demo_level}".format(demo_level=demo_level))
    logger.info("root level={root_level}".format(root_level=root_level))
