import os
from pathlib import Path

from fu.common.errors import InvalidPathError


def get_file_name(path: str, include_extension=True) -> str:
    """
    Retrieves the filename of provided path

    :param path: Path to file
    """
    if is_dir(path):
        raise InvalidPathError()

    basename = os.path.basename(path)
    if include_extension:
        return basename
    else:
        return os.path.splitext(basename)[0]


def get_file_ext(path: str) -> str:
    """Get extension of provided file

    Args:
        path (str): File path

    Returns:
        str: File extension or empty string for files \
                without extension
    """
    if not os.path.isfile(path):
        raise InvalidPathError()

    return Path(path).suffix


def is_dir(path: str) -> bool:
    """
    Verifies that provided path exists as a directory
    in os filesystem

    :param path: Path to verify
    """
    return os.path.exists(path) and os.path.isdir(path)


def is_file(path: str) -> bool:
    """Test whether given path exists as a regular file

    Args:
        path (str): Path to verify

    Returns:
        bool: true if file exists
    """
    return os.path.exists(path) and os.path.isfile(path)


def path_files(path: str, extensions = []):
    """
    Creates a generator to iterate each file in provided
    directory path

    Yield values will be a string representing full path
    to every file

    :param path: Directory path
    :param extensions: If value is provided, only files
        with those extensions will be yield
    """
    if not is_dir(path):
        raise InvalidPathError()

    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if not extensions:
                yield os.path.join(path, file)

            else:
                file_ext = Path(file).suffix
                if file_ext.lower() in extensions:
                    yield os.path.join(path, file)

def count_path_files(path: str, extensions = []) -> int:
    """Counts all files in given directory

    Args:
        path (str): Directory path
        extensions (list, optional): If value is provided, only files with \
            those extensions will be counted. Defaults to [].

    Returns:
        int: Found files count
    """
    if not is_dir(path):
        raise InvalidPathError()

    count = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            if not extensions:
                count += 1

            else:
                file_ext = Path(file).suffix
                if file_ext.lower() in extensions:
                    count += 1

    return count