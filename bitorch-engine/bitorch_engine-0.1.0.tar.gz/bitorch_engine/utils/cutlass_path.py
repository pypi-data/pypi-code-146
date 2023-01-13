import os
from pathlib import Path
from typing import Union, Tuple


def check_path(p: str) -> Tuple[bool, str]:
    p = Path(p)
    if (p / "cutlass.h").is_file():
        return True, str(p)
    if (p / "cutlass" / "cutlass.h").is_file():
        return True, str(p)
    if (p / "include" / "cutlass" / "cutlass.h").is_file():
        return True, str(p / "include")
    return False, ""


def find_cutlass(check_only: bool = True) -> Union[bool, str]:
    success, path = False, ""
    search_paths = ["/usr/local/include"] + os.environ.get("CPATH", "").split(":")
    for p in search_paths:
        if check_only:
            print("Searching Cutlass in:", p)
        success, path = check_path(p)
        if success:
            if check_only:
                print("Found Cutlass in:", p)
            break
    return success if check_only else path


def is_cutlass_available() -> bool:
    return find_cutlass()


def get_cutlass_include_path() -> str:
    return find_cutlass(check_only=False)
