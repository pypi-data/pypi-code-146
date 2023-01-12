from pathlib import Path
from typing import List, Optional


class BinFileResolver:
    @staticmethod
    def find_first_file(parent: Path, files: List[str]) -> Optional[Path]:
        for f in files:
            file_path = parent / f
            if file_path.is_file():
                return file_path

        return None
