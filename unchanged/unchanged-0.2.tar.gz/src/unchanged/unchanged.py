from __future__ import annotations
from dataclasses import dataclass

import difflib
from pathlib import Path
import shutil
from typing import Any, Callable, TypeVar



Data = TypeVar("Data")


@dataclass(frozen=True)
class Verifier:
    files_match: Callable[[str, str], bool] = lambda f1, f2: Path(f1).read_text() == Path(f2).read_text()
    show_diffs: Callable[[str, str], None] = lambda f1, f2: '\n' + ''.join(difflib.unified_diff(Path(f1).read_text(), Path(f2).read_text(), fromfile=str(f1), tofile=str(f2)))
    write: Callable[[str, Data], None] = lambda f, data: Path(f).write_text(data)
    read: Callable[[str], Data] = lambda f: Path(f).read_text()
    approve_file: Callable[[str, str], None] = shutil.copy2
        
    def __call__(
        self,
        data: Any, 
        path: str, 
        approve_diff: bool = False,         
    ):
        """Mini Approval Testing tool."""

        # Create read/write paths
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        received_path = save_path.with_suffix('.received' + save_path.suffix)  # "received" (currently-being checked) filename
        approved_path = save_path.with_suffix('.approved' + save_path.suffix)  # "approved" (already-checked) filename
        
        # Put data into the received file
        self.write(received_path, data)

        # On first run: Just update the approved file with the current data.
        if not approved_path.exists():
            self.write(approved_path, data)
            return

        # On "approved changes" runs: just copy the received file to the approved file.
        if approve_diff:
            self.approve_file(received_path, approved_path)

        # On subsequent runs, do diff checking between the already-approved data and the new data.
        if not self.files_match(approved_path, received_path):
            raise AssertionError(self.show_diffs(received_path, approved_path))
        

            
verify = Verifier()  # default verifier




def void(*args, **kwargs) -> None:
    """swallows all inputs."""
    return None

