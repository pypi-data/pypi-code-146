from typing import Any

from pydantic import BaseModel

from chalk.streams.base import StreamSource


class FileSource(BaseModel, StreamSource, frozen=True):
    path: str
    key_separator: str = "|"

    def config_to_json(self) -> Any:
        return self.json()
