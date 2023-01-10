
from pathlib import Path


def is_source_code_file(path: Path):
    if path.suffix == ".rs":
        return True
    if path.name in ["Cargo.toml", "Cargo.lock", "elrond.json"]:
        return True
    return False
