
import base64
import json
from pathlib import Path
from typing import Any, Dict, List

from build_contract_rust.cargo_toml import get_contract_name_and_version
from build_contract_rust.filesystem import get_files_recursively
from build_contract_rust.source_code import is_source_code_file


class PackagedSourceCodeEntry:
    def __init__(self, path: Path, content: bytes) -> None:
        self.path = path
        self.content = content

    @classmethod
    def from_dict(cls, dict: Dict[str, Any]) -> 'PackagedSourceCodeEntry':
        path = Path(dict.get("path", ""))
        content = base64.b64decode(dict.get("content", ""))
        return PackagedSourceCodeEntry(path, content)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "path": str(self.path),
            "content": base64.b64encode(self.content).decode()
        }

        return data


class PackagedSourceCode:
    def __init__(self, name: str, version: str, entries: List[PackagedSourceCodeEntry]) -> None:
        self.name = name
        self.version = version
        self.entries = entries

    @classmethod
    def from_file(cls, path: Path) -> 'PackagedSourceCode':
        with open(path, "r") as f:
            data: Dict[str, Any] = json.load(f)

        return PackagedSourceCode.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PackagedSourceCode':
        name = data.get("name", "untitled")
        version = data.get("version", "0.0.0")
        entries_raw: List[Dict[str, Any]] = data.get("entries", [])
        entries = [PackagedSourceCodeEntry.from_dict(entry) for entry in entries_raw]
        return PackagedSourceCode(name, version, entries)

    @classmethod
    def from_folder(cls, folder: Path) -> 'PackagedSourceCode':
        entries = cls._create_entries_from_folder(folder)
        name, version = get_contract_name_and_version(folder)
        return PackagedSourceCode(name, version, entries)

    @classmethod
    def _create_entries_from_folder(cls, folder: Path) -> List[PackagedSourceCodeEntry]:
        files = get_files_recursively(folder, is_source_code_file)
        entries: List[PackagedSourceCodeEntry] = []

        for full_path in files:
            with open(full_path, "rb") as f:
                content = f.read()

            relative_path = full_path.relative_to(folder)
            entries.append(PackagedSourceCodeEntry(relative_path, content))

        return entries

    def unwrap_to_folder(self, folder: Path):
        for entry in self.entries:
            full_path = folder / entry.path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "wb") as f:
                f.write(entry.content)

    def save_to_file(self, path: Path):
        data = self.to_dict()

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        entries = [entry.to_dict() for entry in self.entries]

        return {
            "name": self.name,
            "version": self.version,
            "entries": entries
        }
