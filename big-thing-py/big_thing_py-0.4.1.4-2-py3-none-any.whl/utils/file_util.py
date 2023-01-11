from big_thing_py.utils.common_util import *
from big_thing_py.utils.exception_util import *
from big_thing_py.utils.log_util import *


def read_file(path: str) -> List[str]:
    try:
        with open(path, 'r') as f:
            return f.readlines()
    except FileNotFoundError as e:
        print_error(e)
        SOPLOG_DEBUG(f'File not found: {path}')
        raise e


def write_file(path: str, content: Union[str, List[str]]) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            if isinstance(content, str):
                f.write(content)
            elif isinstance(content, list):
                f.writelines(content)
        return path
    except FileNotFoundError as e:
        print_error(e)
        SOPLOG_DEBUG(f'Path not found: {path}')
        raise e
