import os
from datetime import datetime
from fu.utils.console import console
from fu.utils.path import (
    get_file_name,
    is_dir,
    is_file,
    path_files
)


def index_dir(path: str, output: str = None) -> None:
    """Creates a text file listing all files at given path in     \
        ascending order. Only direct children files are included \
        in index file.

    Args:
        path (str): Path to index
        output (str, optional): Name for generated index file. \
            Defaults to "idx-<date>-<time>-<microseconds>.txt".
    """
    console.print(
        f'Scanning contents of: { path } ...',
        style='info')

    fnames = []
    for filepath in path_files(path):
        fname = get_file_name(filepath)
        fnames.append(fname)
    fnames.sort()

    if len(fnames) == 0:
        console.print(
            'No files found in specified path',
            style='warning')
        return

    # Write found file names to index file
    if not output:
        now = datetime.now()
        output_fname = f'idx-{ now.strftime("%Y%m%d-%H%M%S-%f") }.txt'
        output = os.path.join(path, output_fname)

    if os.path.exists(output):
        console.print(
            f'A file with same name already exists: { output }',
            style='error'
        )
        return

    with open(output, 'a') as idx_file:
        idx_file.write(f'# Index for { path } { os.linesep }')
        idx_file.write(f'# { len(fnames) } file(s) indexed: { os.linesep }')
        idx_file.write(os.linesep)
        for fname in fnames:
            idx_file.write(f'{ fname }{ os.linesep }')

        console.print(f'Index saved at { output }', style='info')

def index_deleted_from(path: str, idx: str, output: str = None) -> None:
    """Creates a text file listing all files that are present in a given \
        index but doesn't exists in specified path anymore.

    Args:
        path (str): Where to look for files in index
        idx (str): Index of files to verify in specified path
        output (str, optional): Name for generated index file of not found \
            items. Defaults to "idx-removed-<date>-<time>-<microseconds>.txt".
    """
    if not is_file(idx):
        console.print(
            f'Invalid index file: { idx }',
            style='error')
        return

    if not is_dir(path):
        console.print(
            f'Invalid path: { path }',
            style='error')
        return

    # Find out removed files

    console.print(
        f'Scanning for removed files in: { path } ...',
        style='info')

    removed_fnames = []
    with open(idx, 'r') as idx_file:
        for idx_line in idx_file:
            idx_line = idx_line.strip("\n")

            # Ignore empty lines and comments
            if idx_line and not idx_line.startswith('#'):
                indexed_file = os.path.join(path, idx_line)

                # If file was removed from path
                if not os.path.exists(indexed_file):
                    removed_fnames.append(idx_line)
    removed_fnames.sort()

    if len(removed_fnames) == 0:
        console.print(
            'No indexed files has been removed',
            style='warning')
        return

    # Create index of removed files

    if not output:
        now = datetime.now()
        output_fname = f'idx-removed-{ now.strftime("%Y%m%d-%H%M%S-%f") }.txt'
        output = os.path.join(path, output_fname)

    if os.path.exists(output):
        console.print(
            f'A file with same name already exists: { output }',
            style='error'
        )
        return

    with open(output, 'a') as idx_rm_file:
        idx_rm_file.write(
            '# Index of removed files from: '
            f'{ path }{ os.linesep }'
        )
        idx_rm_file.write(f'# Based on index: { idx }{ os.linesep }')
        idx_rm_file.write(
            f'# { len(removed_fnames) } file(s) has been '
            f'removed:{ os.linesep }'
        )
        idx_rm_file.write(os.linesep)

        for fname in removed_fnames:
            idx_rm_file.write(f'{ fname }{ os.linesep }')

        console.print(
            f'Index of removed files saved at { output }',
            style='info')
