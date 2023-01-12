import logging
import sys
from os.path import dirname

base_dir = dirname(__file__)

# create logger
logger = logging.getLogger('winval')
logger.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')

# create console handler and set level to debug
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

# add package paths to PYTHONPATH
path = f'{dirname(dirname(__file__))}'
if path not in sys.path:
    sys.path.append(path)
