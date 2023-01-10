import os
from pathlib import Path

PROJECT_NAME = 'gravity_auto_exit'
BASE_DIR = Path(__file__).resolve().parent.parent
INTERNAL_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
logs_dir = os.path.join(INTERNAL_DIR, 'logs')
pics_dir = os.path.join(INTERNAL_DIR, 'pics')
sys_log_name = os.path.join(logs_dir, 'journal.log')
