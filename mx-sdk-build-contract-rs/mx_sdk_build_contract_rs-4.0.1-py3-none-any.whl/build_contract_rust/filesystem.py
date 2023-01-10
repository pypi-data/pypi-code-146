import logging
import os
from pathlib import Path
from typing import Callable, List, Union
from zipfile import ZIP_DEFLATED, ZipFile

from build_contract_rust.errors import ErrKnown


def archive_directory(archive_file: Path, directory: Path, should_include_file: Union[Callable[[Path], bool], None] = None):
    files = get_files_recursively(directory, should_include_file)

    with ZipFile(archive_file, "w", ZIP_DEFLATED) as archive:
        for full_path in files:
            archive.write(full_path, full_path.relative_to(directory))

    logging.info(f"Created archive: file = {archive_file}, with size = {archive_file.stat().st_size} bytes")


def get_files_recursively(directory: Path, should_include_file: Union[Callable[[Path], bool], None] = None):
    should_include_file = should_include_file or (lambda _: True)
    paths: List[Path] = []

    for root, _, files in os.walk(directory):
        root_path = Path(root)
        for file in files:
            file_path = Path(file)
            full_path = root_path / file_path

            if file_path.is_dir():
                continue
            if not should_include_file(file_path):
                continue

            paths.append(full_path)

    return paths


def find_file_in_folder(folder: Path, pattern: str) -> Path:
    files = list(folder.rglob(pattern))

    if len(files) == 0:
        raise ErrKnown(f"No file matches pattern [{pattern}] in folder {folder}")
    if len(files) > 1:
        logging.warning(f"More files match pattern [{pattern}] in folder {folder}. Will pick first:\n{files}")

    file = folder / files[0]
    return Path(file).resolve()
