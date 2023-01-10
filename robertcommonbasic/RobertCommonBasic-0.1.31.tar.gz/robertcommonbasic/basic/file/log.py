from typing import Union, Optional
from ..os.file import check_file_exist, get_file_folder
from ..os.path import create_dir_if_not_exist


def save_log(path: str, mode: str, values: Union[str, list], encoding: Optional[str] = None):
    create_dir_if_not_exist(get_file_folder(path))
    with open(path, newline='', mode=mode, encoding=encoding) as f:
        if isinstance(values, str):
            if not values.endswith('\n'):
                values = f'{values}\n'
            f.write(values)
        elif isinstance(values, list):
            for index, value in enumerate(values):
                if not value.endswith('\n'):
                    values[index] = f'{value}\n'
            f.writelines(values)


def read_log(path: str, mode: str = 'r'):
    if check_file_exist(path) is True:
        with open(path, mode=mode) as f:
            return f.read()


def read_logs(path: str):
    if check_file_exist(path) is True:
        with open(path, mode='r') as f:
            return f.readlines()
