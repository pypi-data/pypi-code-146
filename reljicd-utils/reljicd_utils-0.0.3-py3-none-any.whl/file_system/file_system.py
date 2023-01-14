from glob import glob
from typing import List


def files_in_dir(directory: str, extension: str = 'xml') -> List[str]:
    directory = _clean_directory_name(directory)
    return sorted(glob(f'{directory}/*.{extension}'))


def files_in_dir_recursive(directory: str, extension: str = 'xml') -> List[str]:
    directory = _clean_directory_name(directory)
    files = glob(f'{directory}/*.{extension}')

    subdirs = dirs_in_dir(directory)
    for subdir in subdirs:
        files += files_in_dir_recursive(subdir, extension)

    return sorted(files)


def dirs_in_dir(directory: str) -> List[str]:
    directory = _clean_directory_name(directory)
    return sorted(glob(f'{directory}/*/'))


def num_of_lines_in_file(file: str) -> int:
    return sum(1 for _ in open(file))


def _clean_directory_name(directory: str) -> str:
    return directory[:-1] if directory.endswith('/') else directory
