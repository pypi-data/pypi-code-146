from io import BytesIO
from pathlib import Path
from typing import Optional, Union

Bytes = Union[bytes, BytesIO]
FilePath = Union[str, Path]


class File:
    def __init__(
        self, name: Optional[str] = None, content: Optional["Bytes"] = None
    ) -> None:
        self.name = name or "Unnamed"
        self.content = content.getvalue() if isinstance(content, BytesIO) else content

    @classmethod
    def from_bytes(cls, file_source: Bytes, name: Optional[str] = None) -> "File":
        return cls(name=name, content=file_source)

    @classmethod
    def from_path(
        cls, file_source: FilePath, name: Optional[str] = None
    ) -> "File":
        path = Path(file_source) if isinstance(file_source, str) else path

        with open(path, "rb") as f:
            return cls(name=name or path.name, content=f.read())

    def __repr__(self) -> str:
        return f"File(name={self.name!r})"
