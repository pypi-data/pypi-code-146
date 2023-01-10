import io
import magic
import os
import shutil

from aiofiles import open as async_open
from typing import Callable, Union

from .decorators import try_and_get_bool, try_and_get_data


# File

@try_and_get_data
async def async_read_file(path: str, **kwargs):
    """Async read file."""

    async with async_open(path, 'rb', **kwargs) as f:
        return await f.read()


@try_and_get_data
async def async_save_file(
    path: str,
    file: Union[bytes, io.BytesIO, io.FileIO, str],
    replace: bool = True,
    **kwargs
):
    """Async save file."""

    mode = 'w' if isinstance(file, str) else 'wb'

    if os.path.exists(path) and not replace:
        raise FileExistsError()
    if getattr(file, 'read', None):
        file = file.read()
    async with async_open(path, mode, **kwargs) as f:
        return await f.write(file)


def clear_dir(path: str):
    """Clear dir (Remove and create)."""

    rmdir(path)
    mkdirs(path)


@try_and_get_bool
def del_file(path: str):
    """Del file."""

    os.remove(path)


def get_file_mime(file: Union[bytes, io.BytesIO, io.FileIO]):
    """Get file mime."""

    is_file = getattr(file, 'read', None) != None
    data = file.read(2048) if is_file else file[:2048]
    file_mime = magic.from_buffer(data, mime=True)

    if is_file:
        file.seek(0)

    return file_mime.split('/')


@try_and_get_bool
def mkdir(path: str):
    """Create dir."""

    os.mkdir(path)


@try_and_get_bool
def mkdirs(path: str):
    """Create dir (use makedirs)."""

    os.makedirs(path, exist_ok=True)


@try_and_get_data
def read_file(path: str):
    """Read file."""

    with open(path, 'rb') as f:
        return f.read()


@try_and_get_bool
def rmdir(path: str):
    """Remove dir."""

    shutil.rmtree(path)


@try_and_get_data
def save_file(
    path: str,
    file: Union[bytes, io.BytesIO, io.FileIO, str],
    replace: bool = True
):
    """Save file."""

    mode = 'w' if isinstance(file, str) else 'wb'

    if os.path.exists(path) and not replace:
        raise FileExistsError()
    if getattr(file, 'read', None):
        file = file.read()
    with open(path, mode) as f:
        return f.write(file)


def save_file_as_bytesio(
    save_fnc: Callable,
    get_bytes: bool = False,
    **kwargs
):
    """Save file to io.BytesIO."""

    with io.BytesIO() as output:
        save_fnc(output, **kwargs)
        file_bytes = output.getvalue()

    if get_bytes:
        return file_bytes

    return io.BytesIO(file_bytes)


@try_and_get_bool
def move_file(path: str, target_path: str):
    """Move file or dir."""

    shutil.move(path, target_path)


@try_and_get_bool
def rename(path: str, name: str):
    """Rename file or dir."""

    os.rename(path, name)
