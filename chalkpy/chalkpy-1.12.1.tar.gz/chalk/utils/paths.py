import os
import sys
from pathlib import Path
from typing import Optional


def get_classpath(x: object) -> Path:
    filepath = sys.modules[x.__module__].__file__
    assert filepath is not None
    return Path(os.path.abspath(filepath))


def get_directory_root() -> Optional[Path]:
    current = Path(os.path.dirname(os.path.abspath("dummy.txt")))
    while True:
        if any((current / f).exists() for f in ("chalk.yaml", "chalk.yml")):
            return current
        if Path(os.path.dirname(current)) == current:
            # This is '/'
            return None
        current = current.parent
