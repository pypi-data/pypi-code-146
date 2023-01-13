from typing import Dict, Iterator, List, Tuple

import os
import re


MAX_FNAME: int = 256

PUNCTUATION_RE_CLASS: str = r"""[!"#$%&'()*+,:;<=>?@\[\\\]^`{|}]"""  # not including ~ . / - _
WHITESPACE_RE_CLASS: str = r"""[ \t\n\r\x0b\x0c]"""
WHITESPACE_EXCEPT_FOR_SPACE_RE_CLASS: str = r"""[\t\n\r\x0b\x0c]"""

DELIMITER_RE: str = "[" + PUNCTUATION_RE_CLASS[1:-1] + WHITESPACE_RE_CLASS[1:-1] + "]"
NON_DELIMITER_RE: str = "[^" + PUNCTUATION_RE_CLASS[1:-1] + WHITESPACE_EXCEPT_FOR_SPACE_RE_CLASS[1:-1] + "]"

PAT_DELIMITER_RE: re.Pattern = re.compile(DELIMITER_RE)
PAT_WHITESPACE_RE: re.Pattern = re.compile(WHITESPACE_RE_CLASS)
PAT_PATHLIKE: re.Pattern = re.compile(r"%s{1,%d}" % (NON_DELIMITER_RE, MAX_FNAME))


def pathlike_iter(L: str) -> Iterator[Tuple[int, str]]:
    """
    Iterate over substrings that satisfy the following conditions:
    * the previous char is start of line or one of DELIMITERS
    * when the first char is '/', the previous char is not '~'
    * the next char is either end of line or one of DELIMITERS
    * all of the sub-substrings split by '/' does not exceed MAX_FNAME
    * does not include '//', does not start with ' ', does not end with ' '.
    * a maximal (any string extending it does not satisfy all the above conditions)
    """

    for i in range(len(L)):
        if i == 0 or PAT_DELIMITER_RE.match(L[i - 1]):
            m = PAT_PATHLIKE.match(L, i)
            if m:
                p = m.group(0)
                if (
                    p
                    and not PAT_WHITESPACE_RE.match(p)
                    and (not p.startswith("/") or i == 0 or L[i - 1] != "~")
                    and not p.startswith(" ")
                    and p.find("//") < 0
                ):
                    yield i, p


def existing_file_iter(L: str) -> Iterator[Tuple[int, str, str]]:
    dir_to_files: Dict[str, List[str]] = dict()
    dir_to_dirs: Dict[str, List[str]] = dict()

    def find_files_and_dirs(d):
        dir_files = dir_to_files.get(d, None)
        dir_dirs = dir_to_dirs.get(d, None)
        if dir_files is None:
            assert dir_dirs is None
            dir_files = []
            dir_dirs = []
            fs = os.listdir(d if d != '' else os.curdir)
            for f in fs:
                p = os.path.join(d, f)
                if os.path.isfile(p):
                    dir_files.append(f)
                elif os.path.isdir(p):
                    dir_dirs.append(f)
            dir_to_files[d] = dir_files
            dir_to_dirs[d] = dir_dirs
        assert dir_dirs is not None
        return dir_files, dir_dirs

    for pos, pathstr in pathlike_iter(L):
        p0 = pathstr
        existing_file_or_dir_found = False
        while not existing_file_or_dir_found:
            d0, f0 = os.path.split(p0)
            if d0 == '' or os.path.exists(d0) and os.path.isdir(d0):
                dir_files, dir_dirs = find_files_and_dirs(d0)

                for df in dir_files:
                    if f0 == df:
                        yield pos, "file", os.path.join(d0, df)
                        existing_file_or_dir_found = True
                    elif f0.startswith(df):
                        assert len(df) < len(f0)
                        if PAT_DELIMITER_RE.match(f0[len(df)]):
                            yield pos, "file", os.path.join(d0, df)
                            existing_file_or_dir_found = True
                for dd in dir_dirs:
                    if f0 == dd:
                        yield pos, "directory", os.path.join(d0, dd)
                        existing_file_or_dir_found = True
                    elif f0.startswith(dd):
                        assert len(dd) < len(f0)
                        if PAT_DELIMITER_RE.match(f0[len(dd)]):
                            yield pos, "directory", os.path.join(d0, dd)
                            existing_file_or_dir_found = True
            if d0 in ['', '/']:
                break  # while not existing_file_or_dir_found
            p0 = d0
