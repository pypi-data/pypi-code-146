# -------------------
import sys


# -------------------
## Holds all info for logging to stdout.
# Normally used only when the logger is not avaialble or before it is configured
class LoggerStdout:
    # -------------------
    ## initialize
    #
    # @return None
    def init(self):
        pass

    # -------------------
    ## write a "start" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def start(self, msg):
        self._write_line('====', msg)

    # -------------------
    ## write a "line" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def line(self, msg):
        self._write_line(' ', msg)

    # -------------------
    ## write a "ok" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def ok(self, msg):
        self._write_line('OK', msg)

    # -------------------
    ## write a "warn" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def warn(self, msg):
        self._write_line('WARN', msg)

    # -------------------
    ## write a "err" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def err(self, msg):
        self._write_line('ERR', msg)

    # -------------------
    ## write a "dbg" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def dbg(self, msg):
        self._write_line('DBG', msg)

    # -------------------
    ## write a "raw" line with the given message
    #
    # @param msg   the message to write
    # @return None
    def raw(self, msg):
        self._write_line('', msg)

    # -------------------
    ## write the given line to stdout
    #
    # @param tag   the prefix tag
    # @param msg   the message to write
    # @return None
    def _write_line(self, tag, msg):
        print(f'{tag: <4} {msg}')
        sys.stdout.flush()
