from pathlib import Path


def mkdir(path: Path):
    Path(path).mkdir(parents=True, exist_ok=True)
