import logging
import sys
from pythonjsonlogger import jsonlogger


class _AnsiColorizer(object):
    """
    A colorizer is an object that loosely wraps around a stream, allowing
    callers to write text to the stream in a particular color.

    Colorizer classes must implement C{supported()} and C{write(text, color)}.
    """

    _colors = dict(
        black=30, red=31, green=32, yellow=33, blue=34, magenta=35, cyan=36, white=37
    )

    def __init__(self, stream):
        self.stream = stream

    @classmethod
    def supported(cls, stream=sys.stdout):
        """
        A class method that returns True if the current platform supports
        coloring terminal output using this method. Returns False otherwise.
        """
        if not stream.isatty():
            return False  # auto color only on TTYs
        try:
            import curses
        except ImportError:
            return False
        else:
            try:
                return curses.tigetnum("colors") > 2
            except curses.error:
                curses.setupterm()
                return curses.tigetnum("colors") > 2

    def write(self, text, color):
        """
        Write the given text to the stream in the given color.

        @param text: Text to be written to the stream.
        @param color: A string label for a color. e.g. 'red', 'white'.
        """
        color = self._colors[color]
        self.stream.write("\x1b[%s;1m%s\x1b[0m" % (color, text))


class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=sys.stderr):
        super(ColorHandler, self).__init__(_AnsiColorizer(stream))

    def emit(self, record):
        msg_colors = {
            logging.DEBUG: "green",
            logging.INFO: "blue",
            logging.WARNING: "yellow",
            logging.ERROR: "red",
        }

        color = msg_colors.get(record.levelno, "blue")
        self.stream.write(self.format(record) + "\n", color)


logger = None


def get_logger():
    global logger
    if logger is None:
        logger = logging.getLogger("osim")
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(module)s %(funcName)s %(lineno)d %(name)-2s %(levelname)-8s %(message)s"
        )
        formatter.default_msec_format = "%s.%03d"

        log_handler = ColorHandler()
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(formatter)

        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False
    return logger
