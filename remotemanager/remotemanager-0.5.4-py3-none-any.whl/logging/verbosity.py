from enum import Enum

from remotemanager.storage.sendablemixin import SendableMixin


class Verbosity(SendableMixin):
    """
    Class to store verbosity information

    Initialise with Verbosity(level), where level is the integer level

    args:
        level (int, str):
            level above which to print
    """

    def __init__(self,
                 level):
        if level is None:
            level = 4

        # see if the level passed is already a Verbose instance
        if isinstance(level, self.__class__):
            level = level.value

        # first try to get level via from an int, falling back on string
        try:
            level = int(level)
        except ValueError:
            try:
                level = getattr(_levels, level.lower()).value
            except AttributeError:
                # raise _levels missing error with invalid level
                _levels(level)

        self._value = level
        self._name = _levels(level).name

    def __repr__(self):
        return self.name

    def __bool__(self):
        return self.value != 0

    @property
    def value(self):
        return self._value

    @property
    def level(self):
        return self._value

    @property
    def name(self):
        return self._name

    def print(self,
              message: str,
              atlevel: int = 2,
              end: str = '\n'):
        """
        Request that a message be printed. Compares against the set
        verbosity level before printing.

        Args:
            message (str):
                message to print
            atlevel (int):
                If this number is higher priority than (lower numeric value)
                (or equal to) the set limit, print
            end (str):
                print(..., end= ...) hook
        """
        # print(f'request {message[:24]} @ {atlevel}')
        if self and self.level <= atlevel:
            print(message, end=end)


class _levels(Enum):
    none = 0
    debug = 1
    runtime = 2
    info = 3
    important = 4
    warning = 5
    error = 6
    critical = 7

    @classmethod
    def _missing_(cls, value):
        msg = [f'{value} is not a valid Verbosity:']

        for v in _levels:
            msg.append(f'\t{v.value}: {v.name}')

        raise ValueError('\n'.join(msg))
