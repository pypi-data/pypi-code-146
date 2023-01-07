'''Constants'''

MAX_SHORT_TOKENS = 20
N_LOGPROBS = 5
LOGPROB_THRESHOLD = -7
PARALLEL_REQUEST_LIMIT = 1 # ideally would like to set this to 20, but would require changes to run_ai
PER_MINUTE_REQUEST_LIMIT = 20
DELAY_IN_SECONDS = 60.0 / PER_MINUTE_REQUEST_LIMIT
KEYWORDS = ['true', 'null', '*', 'select', 'from', 'where', 'with', 'group by', 'inner', 'outer', 'left', 'join']