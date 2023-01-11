'''Constants'''

MAX_SHORT_TOKENS = 20
N_LOGPROBS = 5
LOGPROB_THRESHOLD = -7
PARALLEL_REQUEST_LIMIT = 1 # ideally would like to set this to 20, but would require changes to run_ai
KEYWORDS = ['true', 'null', '*', 'select', 'from', 'where', 'with', 'group by', 'inner', 'outer', 'left', 'join']