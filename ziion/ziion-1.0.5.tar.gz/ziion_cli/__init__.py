import os
from ziion_cli.constants import (
    SOLC_SELECT_DIR,
    SOLC_ARTIFACTS_DIR,
)

if not os.path.exists(SOLC_SELECT_DIR):
    os.mkdir(path=SOLC_SELECT_DIR)

if not os.path.exists(SOLC_ARTIFACTS_DIR):
    os.mkdir(path=SOLC_ARTIFACTS_DIR)
