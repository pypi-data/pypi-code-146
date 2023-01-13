import logging
import os

import appdirs

from ...core.utils import APPNAME, APPAUTHOR

TOKEN = None
"""API token"""

LOGGING_LEVEL = logging._levelToName[logging.ERROR]
"""Level that we should log at by default. """

LOG_FILE_PATH = os.path.join(
    appdirs.user_log_dir(APPNAME, APPAUTHOR), ".qalx.log"
)
r"""The path where log files will be stored.

* Windows: C:\\Users\\<User>\\AppData\\Local\\agiletek\\qalx\\Logs\\.qalx.log
* Linux: /home/<user>/.cache/qalx/log/.qalx.log
* Max ~/Library/Logs/qalx/.qalx.log

"""

MSG_BLACKOUTSECONDS = 30
"""
After this time in seconds the message will be returned to the queue if
it has not been deleted.

.. note::
    Workers automatically issue a heartbeat to the queue while the job is being
    processed to keep extending the blackout during processing
"""

MAX_RETRY_500 = 2
"""How many times should pyqalx retry the request when receiving a 5XX error
back from the API?"""

FACTORY_PACK_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
r"""
The directory where factory bot code will be packed and deployed from.
Defaults to the following:

* Windows: C:\\Users\\<User>\\AppData\\Local\\agiletek\\qalx
* Linux: ~/.local/share/qalx
* Mac: ~/Library/Application Support/qalx
"""

DOWNLOAD_DIR = appdirs.user_data_dir(APPNAME, APPAUTHOR)
r"""
The directory where files from qalx will be downloaded by default.
Defaults to the following:

* Windows: C:\\Users\\<User>\\AppData\\Local\\agiletek\\qalx
* Linux: ~/.local/share/qalx
* Mac: ~/Library/Application Support/qalx
"""

REGION = "eu-west-2"
r"""
The region that will be used when connecting to databases or other remote
services.  Originally set via `qalx configure`.  Change this to another valid
region to use services in that region.
This is only a valid option for User configs - not for Bot configs
"""

del APPNAME, APPAUTHOR  # These are not config keys
