from hashlib import sha3_256
from typing import Union, BinaryIO
from pathlib import Path


def ensure_path(
    path: Union[str, Path], must_exist: bool = False
) -> Path:
    """
    ensures that given path is of type Path
    and that HOME directory is resolved
    """
    path = (
        path
        if isinstance(path, Path) else
        Path(path)
    ).expanduser()

    if must_exist and not path.exists():
        # path does not exist
        raise ValueError(
            f"The directory '{path}' does not exist!"
        )

    return path


def hash_file(
    filename: Union[str, Path],
    hash_func: callable = sha3_256
) -> bytes:
    """
    obtain the hash of the file with given hash function

    :param filename: file object on which hash is computed
    :type filename: Path
    :param hash_func: hash function that is used, defaults to sha3_256
    :type hash_func: callable, optional
    :return: hash digest
    :rtype: bytes
    """
    assert isinstance(filename, (str, Path))
    assert callable(hash_func)

    # ensure that filename does exist
    filename = ensure_path(filename, must_exist=True)

    # initialize hash function
    h = hash_func()

    # read file chunkwise and update hash function
    with filename.open("rb") as f:
        while True:
            chunk = f.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.digest()


def hash_directory(
    directory: Union[str, Path],
    glob: str = "**/*",
    exclude_suffixes: list = [],
    exclude_filenames: list = [],
    hash_func: callable = sha3_256
) -> bytes:
    """
    obtain the XORed hash of all files in the given directory
    with given hash function

    :param directory: directory from which all files are hashed
    :type directory: Path
    :param glob: glob to obtain files from directory, defaults to **/*
    :type glob: str, optional
    :param exclude_suffixes: suffixes that are ignored
    :type exclude_suffixes: list
    :param exclude_filenames: filenames that are ignored
    :type exclude_filenames: list
    :param hash_func: hash function that is used, defaults to sha3_256
    :type hash_func: callable, optional
    :return: hash digest
    :rtype: bytes
    """
    assert isinstance(directory, (str, Path))
    assert isinstance(glob, str)
    assert callable(hash_func)

    # ensure that filename does exist
    directory = ensure_path(directory, must_exist=True)
    assert directory.is_dir()

    h = hash_func()
    digest = b"\0" * h.digest_size
    for fn in directory.glob(glob):
        if (
            fn.suffix in exclude_suffixes or
            fn.name in exclude_filenames or
            fn.is_dir()
        ):
            # skip excluded files and directories
            continue

        # XOR digest with file's digest
        digest = bytes([
            a ^ b
            for a, b in zip(digest, hash_file(fn, hash_func))
        ])

    return h.digest()
