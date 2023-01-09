from json import dumps
from json import loads
from pathlib import Path

from ..types import YASpeller


class ConfigWords:
    def __init__(self) -> None:
        self.path = Path(".yaspeller.json")
        self.config: YASpeller = {}

    def get(self) -> list[str]:
        if not self.path.exists():
            return []

        content = self.path.read_text()
        self.config = loads(content)

        if "dictionary" not in self.config:
            return []

        return self.config["dictionary"]

    def set(self, value: list[str]) -> None:
        self.config["dictionary"] = value
        content = dumps(self.config, indent=2, sort_keys=True, ensure_ascii=False)
        self.path.write_text(content + "\n")
