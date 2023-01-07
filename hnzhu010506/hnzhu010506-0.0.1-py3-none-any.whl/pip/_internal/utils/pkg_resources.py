from typing import Dict, Iterable, List

from pip._vendor.pkg_resources import yield_lines


class DictMetadata:
    """IMetadataProvider that reads metadata files from a dictionary."""

    def __init__(self, metadata: Dict[str, bytes]) -> None:
        self._metadata = metadata

    def has_metadata(self, name: str) -> bool:
        return name in self._metadata

    def get_metadata(self, name: str) -> str:
        try:
            return self._metadata[name].decode()
        except UnicodeDecodeError as e:
            # Mirrors handling done in pkg_resources.NullProvider.
            e.reason += f" in {name} file"
            raise

    def get_metadata_lines(self, name: str) -> Iterable[str]:
        return yield_lines(self.get_metadata(name))

    def metadata_isdir(self, name: str) -> bool:
        return False

    def metadata_listdir(self, name: str) -> List[str]:
        return []

    def run_script(self, script_name: str, namespace: str) -> None:
        pass
