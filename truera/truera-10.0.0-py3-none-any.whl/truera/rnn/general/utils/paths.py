import hashlib
from pathlib import Path
from urllib.parse import parse_qs


def find_in_parents(adir: Path, filename: str):
    """Try to find a parent directory (or current) that contains the given filename."""

    if (adir / filename).exists():
        return adir / filename

    else:
        for parent in adir.parents:
            if (parent / filename).exists():
                return parent / filename

    return None


def md5(p: Path):
    # https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python
    with open(p, "rb") as fh:
        h = hashlib.md5()  # nosec B324 - not using for security
        chunk = fh.read(8192)
        while chunk:
            h.update(chunk)
            chunk = fh.read(8192)
    return h.digest()


def parse_search_string(page_search_string: str):
    if (not page_search_string) or (not page_search_string.startswith('?')):
        return {}
    page_search_dict = parse_qs(page_search_string[1:])
    return {
        k: v[0] for k, v in page_search_dict.items()
    }  # only support one param per query for now
