# coding:utf-8
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class MyLogger(metaclass=SingletonMeta):

    def __init__(self,
                 level: str = 'INFO',
                 log_path: str = 'cf.log',
                 max_size: int = 100 * 1024 * 1024,
                 max_backup: int = 3,
                 *args,
                 **kwargs):
        LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'standard': {
                    'format':
                    '%(asctime)s [%(levelname)8s] [%(filename)s:%(lineno)s - %(funcName)10s() ] %(message)s'
                },
            },
            'handlers': {
                'default': {
                    'level': level,
                    'formatter': 'standard',
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',     # Default is stderr
                },
                'rotate': {
                    'level': level,
                    'formatter': 'standard',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': log_path,
                    'maxBytes': max_size,
                    'backupCount': max_backup,
                    'encoding': 'utf8',
                }
            },
            'loggers': {
                '': {     # root logger
                    'handlers': ['default', 'rotate'],
                    'level': level,
                    'propagate': False
                },
                'my.packg': {
                    'handlers': ['default', 'rotate'],
                    'level': 'INFO',
                    'propagate': False
                },
                '__main__': {     # if __name__ == '__main__'
                    'handlers': ['default', 'rotate'],
                    'level': 'DEBUG',
                    'propagate': False
                },
            }
        }

        import logging.config
        logging.config.dictConfig(LOGGING_CONFIG)

        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        return self.logger


def get_logger(level: str = 'INFO',
               log_path: str = '/tmp/cf.log',
               max_size: int = 100 * 1024 * 1024,
               max_backup: int = 3):
    return MyLogger(level, log_path, max_size, max_backup).get_logger()

info = get_logger().info
# def info(msg: str, *args, **kwargs):
#     """ Please use string-format to restrict unexpected behaviour. 
#     """
#     logger = get_logger()
#     if args or kwargs:
#         msg = {'msg': msg, 'args': args, 'kwargs': kwargs}
#     logger.info(msg)


def warning(msg: str):
    get_logger().warning(msg)


def error(msg: str):
    get_logger().error(msg)


def debug(msg: str):
    get_logger().debug(msg)


def critical(msg: str):
    get_logger().critical(msg)


def exception(msg: str):
    get_logger().exception(msg)
