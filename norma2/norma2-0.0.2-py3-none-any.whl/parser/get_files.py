import os
from typing import List

from norma2.config.config_class import GITIGNORE_MATCHES_TYPE


def _can_add_file(
    file: str,
    full_file: str,
    exts: List[str],
    folder_out: List[str],
    gitignore_matches: GITIGNORE_MATCHES_TYPE,
):
    for ext in exts:
        if file.endswith(ext):
            return False
    splited = full_file.split(os.path.sep)
    for dirr in splited:
        for fold in folder_out:
            if dirr == fold:
                return False
    if gitignore_matches is None:
        return True
    return not gitignore_matches(full_file)


def get_all_files(
    folder_or_file_path: str,
    folder_exclude: List[str],
    file_ext_exclude: List[str],
    gitignore_matches: GITIGNORE_MATCHES_TYPE,
) -> List[str]:
    if os.path.isfile(folder_or_file_path):
        return [folder_or_file_path]
    if os.path.isdir(folder_or_file_path):
        res = []
        for root, _, files in os.walk(folder_or_file_path):
            for file in files:
                full_file = os.path.join(root, file)
                if not _can_add_file(
                    file, full_file, file_ext_exclude, folder_exclude, gitignore_matches
                ):
                    continue
                res.append(full_file)
        return res
    raise os.error(f"Invalid path: {folder_or_file_path}")
