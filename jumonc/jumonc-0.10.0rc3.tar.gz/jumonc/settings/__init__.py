"""settings package of jumonc, central place for settings."""
import os
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from jumonc.settings.helpers import parse_boolean

LOG_LEVEL: str = os.environ.get("JUMONC_LOG_LEVEL", "INFO")
LOG_STDOUT: bool = parse_boolean(os.environ.get("JUMONC_LOG_STDOUT", "false"))
LOG_PREFIX: str = os.environ.get("JUMONC_LOG_PREFIX", "")
LOG_FORMAT: str = os.environ.get(
    "JUMONC_LOG_FORMAT",
    "[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s",
)
LOGGING_MPI_RANKS = [0]

REST_API_PORT: int = -1
FLASK_DEBUG = False
FLASK_HOST:str = "0.0.0.0" # nosec B104


PENDING_TASKS_SOFT_LIMIT: int = -1
SHORT_JOB_MAX_TIME:float = 0


ONLY_CHOOSEN_REST_API_VERSION: bool = False
REST_API_VERSION: int = -1


MAX_THREADS_PER_TASK: int = 1
MAX_WORKER_THREADS: int = 1 


DEFAULT_TO_HUMAN_READABLE_NUMBERS = True


ENABLE_AUTH = True

USER_DEFINED_TOKEN = None

PLUGIN_PATHS: List[str] = []

DB_PATH = "jumonc.db"

CACHE_DEFAULT_ENTRIES_PER_PAGE = 10

DATETIME_FORMAT = "%d.%m.%Y, %H:%M:%S"

SSL_ENABLED = False
SSL_MODE:Optional[Union[str,Tuple[str,str]]] = None

MPI_IDs_per_plugin:int = 1000


SCHEDULED_TASKS_ENABLED = True
SCHEDULE_TASKS:List[str] = []


MPI_reduce_idle_CPU_load = True
MPI_sleep_timer=0.001
