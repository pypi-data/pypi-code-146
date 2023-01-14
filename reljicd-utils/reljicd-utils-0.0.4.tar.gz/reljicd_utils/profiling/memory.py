import tracemalloc

from reljicd_utils.config.env_vars import DEBUG
from reljicd_utils.profiling.display_top import display_top

if DEBUG:
    tracemalloc.start()

# Code to profile here

if DEBUG:
    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)
