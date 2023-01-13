import os

import appdirs

from pyqalx.core.utils import APPNAME, APPAUTHOR

WORKER_LOG_FILE_DIR = os.path.join(appdirs.user_log_dir(APPNAME, APPAUTHOR))
r"""Directory to save worker log files

* Windows: C:\\Users\\<User>\\AppData\\Local\\agiletek\\qalx\\Logs
* Linux: /home/<user>/.cache/qalx/log
* Max ~/Library/Logs/qalx

"""

SAVE_INTERMITTENT = False
"""Save the entity after every processing step?"""

SKIP_FINAL_SAVE = False
"""Skip saving the entity back to qalx after post-processing."""

KILL_AFTER = None
"""The number of attempts to get a message from an empty queue before exiting.
When set to None the worker will keep asking forever."""

Q_WAITTIMESECONDS = 20
"""The minimum time in seconds to wait before asking for a message from an
empty queue"""

Q_MSGBATCHSIZE = 1
"""The number of messages to get in each request"""

Q_WAITTIMEMAXSPREADING = 12
"""The maximum spreading factor for a wait.
The maximum wait time will be ``Q_WAITTIMEMAXSPREADING*Q_WAITTIMESECONDS``."""

MSG_WAITTIMESECONDS = 20
"""The time in seconds the bot will wait for a message to appear in the queue"""

del APPNAME, APPAUTHOR  # These are not config keys
