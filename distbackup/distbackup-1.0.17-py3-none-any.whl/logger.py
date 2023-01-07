import re
import time
import logging
from pathlib import Path

# This will remove all the fancy colors that distbackup works so hard to add to its console output :'(
RX_UNSTYLE = re.compile(r'\033\[[;0-9]*[a-zA-Z]')

class FormatDelegator(logging.Formatter):
    '''A formatter which can delegate to other formatters based on log level'''
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._level_delegates = {}

    def set_level_formatter(self, level:int, formatter:logging.Formatter):
        self._level_delegates[level] = formatter

    def set_level_format(self, level:int, fmt:str, *a, **kw):
        self.set_level_formatter(level, logging.Formatter(fmt, *a, **kw))

    def format(self, record):
        formatter = self._level_delegates.get(record.levelno, None)
        if formatter:
            return formatter.format(record)
        else:
            return super().format(record)

class FilePatternLogger(logging.Handler):
    def __init__(self, filename_pattern=''):
        super().__init__()
        self.current_file = None
        self.current_log_path = None
        self.closed = False

        # Convert from pathlib.Path to string if necessary
        filename_pattern = str(filename_pattern)
        self.filename_pattern = filename_pattern
        self.bydate = bool(filename_pattern and '@@' in filename_pattern)

        # If we're not splitting based on date, just open the output now.
        if filename_pattern and not self.bydate:
            self._open(filename_pattern)

    def close(self):
        if self.current_file is not None:
            self.current_file.close()
            self.current_file = None
        self.closed = True

    def _open(self, path):
        # Don't reopen after close
        if not self.closed:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            self.current_file = Path(path).open('a', encoding='utf8')

    def emit(self, record):
        if self.closed:
            return

        text = RX_UNSTYLE.sub('', self.format(record))
        localtime = time.localtime(record.created)
        if self.bydate:
            cdate = time.strftime("%Y-%m-%d", localtime)
            current_log_path = self.filename_pattern.replace('@@', cdate)
            if current_log_path != self.current_log_path:
                if self.current_file:
                    self.current_file.close()
                self.current_log_path = current_log_path
                self._open(current_log_path)

        if self.current_file:
            self.current_file.write(text + '\n')
            self.current_file.flush()
