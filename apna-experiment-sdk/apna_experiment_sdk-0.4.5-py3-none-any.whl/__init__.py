# load enviornment variables first before initializing the package:
import logging
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
logging.debug('Enviornment variables loaded successfully!')

from .apna_experiment_tracker import ApnaExperimentTracker