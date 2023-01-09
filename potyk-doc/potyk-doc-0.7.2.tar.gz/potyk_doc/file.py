import inspect
from pathlib import Path
from typing import Union

from potyk_doc.models import FileName, FileData


def this_dir(caller_file: Union[str, Path] = None) -> Path:
    """
    Возвращает путь к директории модуля из которого запущена эта функция.

    Так, если запустить функцию в модуле tests/test_docx.py, то она вернет tests/.

    https://stackoverflow.com/a/8663885/5500609
    :return: Path на директорию модуля, в котором вызвана функция
    """
    caller_file = caller_file or _get_caller_file()
    return Path(caller_file).resolve().parent


def _get_caller_file(depth=2) -> str:
    """
    Возвращает путь к модулю, из которого был запущен этот метод
    """
    return inspect.stack()[depth][1]


def read_f(path, mode='rb'):
    with open(path, mode) as f:
        return f.read()


def read_f_in_this_dir(filename: FileName, mode='rb'):
    return read_f(this_dir(_get_caller_file()) / filename, mode)


def save_f_in_this_dir(filename: FileName, content: FileData):
    with open(this_dir(_get_caller_file()) / filename, mode='wb') as f:
        f.write(content)
