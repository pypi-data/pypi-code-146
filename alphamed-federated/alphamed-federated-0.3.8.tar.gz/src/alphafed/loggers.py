import logging

from concurrent_log_handler import ConcurrentRotatingFileHandler

__all__ = ['logger', 'task_logger']

if 'alphafed' in logging.Logger.manager.loggerDict.keys():
    logger = logging.getLogger('alphafed')
    logfile = '/logs/alphafed.log'
    handler = ConcurrentRotatingFileHandler(logfile, "a", 512*1024, 5)
    logger.addHandler(handler)

else:
    format = '%(asctime)s|%(levelname)s|%(module)s|%(funcName)s|%(lineno)d:\n%(message)s'
    logging.basicConfig(level=logging.DEBUG,
                        filename='alphafed.log',
                        filemode='w',
                        format=format)
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(format))
    logger.addHandler(console_handler)

if 'task' in logging.Logger.manager.loggerDict.keys():
    task_logger = logging.getLogger('task')
else:
    task_logger = logger
