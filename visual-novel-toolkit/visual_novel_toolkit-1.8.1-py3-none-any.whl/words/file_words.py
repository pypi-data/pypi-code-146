from json import dumps
from json import loads
from pathlib import Path


class FileWords:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.dictionary: list[str] = []

    def get(self) -> list[str]:
        if not self.path.exists():
            return []

        content = self.path.read_text()
        self.dictionary = loads(content)
        return self.dictionary

    def set(self, value: list[str]) -> None:
        self.dictionary = value
        content = dumps(value, indent=2, sort_keys=True, ensure_ascii=False)
        self.path.write_text(content + "\n")
