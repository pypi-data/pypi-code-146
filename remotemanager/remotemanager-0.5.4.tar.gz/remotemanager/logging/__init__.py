import logging


class LoggingMixin:
    @property
    def _logger(self):
        def create_logger():
            self._logobj = \
                LoggerInsert(f'{__name__}.{self.__class__.__name__}',
                             self)

        if not hasattr(self, '_logobj'):
            create_logger()

        if not isinstance(self._logobj, LoggerInsert):
            create_logger()
        return self._logobj


class LoggerInsert:
    """
    This class inserts itself between the logging Logger and the
    _logobj used
    """

    def __init__(self,
                 logger: str,
                 parent):
        self._logger = logging.getLogger(logger)

        self._add_logging_level('runtime', 15)
        self._add_logging_level('important', 25)

        self._parent = parent

    def _add_logging_level(self, name, level):

        def loglevel(self, message, *args, **kwargs):
            if self.isEnabledFor(level):
                self._log(level, message, args, **kwargs)

        def logroot(message, *args, **kwargs):
            logging.log(level, message, *args, **kwargs)

        logging.addLevelName(level, name)
        setattr(logging, name, level)
        setattr(logging.getLoggerClass(), name, loglevel)
        setattr(logging, name, logroot)

    @property
    def verbose(self):
        try:
            return self._parent._verbose
        except AttributeError:
            return None

    def _print(self, msg, lvl, end):
        # print(f'\t{msg[:10]} @ {lvl}')
        try:
            self.verbose.print(msg, lvl, end)
        except AttributeError:
            # usually raised if the stored _verbose is None
            pass

    def debug(self,
              msg: str,
              silent: bool = False,
              prepend: str = '',
              append: str = '',
              end: str = '\n',
              *args,
              **kwargs):
        self._logger.debug(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 1, end=end)

    def runtime(self,
                msg: str,
                silent: bool = False,
                prepend: str = '',
                append: str = '',
                end: str = '\n',
                *args,
                **kwargs):
        self._logger.runtime(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 2, end=end)

    def info(self,
             msg: str,
             silent: bool = False,
             prepend: str = '',
             append: str = '',
             end: str = '\n',
             *args,
             **kwargs):
        self._logger.info(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 3, end=end)

    def important(self,
                  msg: str,
                  silent: bool = False,
                  prepend: str = '',
                  append: str = '',
                  end: str = '\n',
                  *args,
                  **kwargs):
        self._logger.important(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 4, end=end)

    def warning(self,
                msg: str,
                silent: bool = False,
                prepend: str = '',
                append: str = '',
                end: str = '\n',
                *args,
                **kwargs):
        self._logger.warning(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 5, end=end)

    def error(self,
              msg: str,
              silent: bool = False,
              prepend: str = '',
              append: str = '',
              end: str = '\n',
              *args,
              **kwargs):
        self._logger.error(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 6, end=end)

    def critical(self,
                 msg: str,
                 silent: bool = False,
                 prepend: str = '',
                 append: str = '',
                 end: str = '\n',
                 *args,
                 **kwargs):
        self._logger.critical(msg, *args, **kwargs)
        if not silent:
            self._print(prepend + str(msg) + append, 7, end=end)
