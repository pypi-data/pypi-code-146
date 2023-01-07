import importlib.metadata
import logging
from pathlib import Path

__version__ = importlib.metadata.version(__package__ or __name__)

logging.basicConfig(format='%(asctime)d-%(levelname)s-%(message)s')

# folders location

FOLDER_PACKAGE = Path(__file__).parent
FOLDER_SOURCE = FOLDER_PACKAGE.parent
FOLDER_ROOT = FOLDER_SOURCE.parent
FOLDER_DATA = Path(FOLDER_ROOT, 'data')
