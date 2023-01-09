import base64
import inspect
import os
import pprint
import subprocess
import sys
import time
import uuid
from shutil import copy2
from typing import List, Tuple, Union

from pydub.utils import mediainfo

from codefast.base.format_print import FormatPrint, pretty_print
from codefast.ds import fplist
from codefast.logger import info


def file2string(filename: str) -> str:
    """ Read file and return base64 encoded string, use string2file 
    to write back to file.
    """
    with open(filename, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def string2file(filename: str, content: str) -> None:
    """ Write content to file 
    Args:
        filename (str): filename
        content (str): base64 encoded content
    """
    assert len(
        filename) < 100, "Filename too long, you might misused this function."
    with open(filename, 'wb') as f:
        f.write(base64.b64decode(content))


class ProgressBar(object):
    '''Display progress bar on uploading/downloading files
    '''

    def __init__(self) -> None:
        self._processed = 0
        self._start_time = time.time()
        self._pre_time = self._start_time
        self._speed = ''
        self._eta = ''
        self._speed_str = ''

    def run(self, count: int, total: int):
        fp = FormatPrint
        ratio = int(count * 10 / total)
        current_time = time.time()
        time_diff = current_time - self._pre_time
        if time_diff >= 1:
            process_diff = count - self._processed
            self._processed = count
            self._pre_time = current_time
            self._speed = process_diff / time_diff
            self._eta = int((total - count) / self._speed)
            self._speed_str = fp.sizeof_fmt(self._speed)
        size_a = fp.sizeof_fmt(count)
        size_b = fp.sizeof_fmt(total)
        done, undone = '-', '~'
        str_s = "[{}{}{}] {}/{} ({}/s, {}s) {}".format(
            fp.green(done) * (ratio - 1),
            fp.magenta(undone) if ratio < 10 else '', undone * (10 - ratio), size_a,
            size_b, self._speed_str, self._eta, ' ' * 3)
        sys.stdout.write(str_s)
        sys.stdout.flush()
        sys.stdout.write('\b' * (len(str_s)))


class FileIO(object):

    def __call__(self, filename: str = '', delimiter: str = '\n') -> list:
        if filename:
            return FileIO.read(filename, delimiter)

    @classmethod
    def tmpfile(cls, prefix: str, suffix: str) -> str:
        '''return file name'''
        suffix = suffix.lstrip('.')
        opf = '/tmp/{}_{}.{}'.format(prefix, str(uuid.uuid4()), suffix)
        info(f'creating file {opf}')
        return opf

    @classmethod
    def readable_size(cls, size: int) -> str:
        '''Convert file size into human readable string'''
        units = ['KB', 'MB', 'GB', 'TB', 'PB'][::-1]
        res, copy_size = [], size
        size //= 1024
        while size > 0:
            res.append("{}{}".format(size % 1024, units.pop()))
            size //= 1024
        return str(copy_size) + ' ({})'.format(' '.join(reversed(res)))

    @classmethod
    def readable_duration(cls, duration: float) -> str:
        '''Convert duration into human readable string'''
        units = ['second', 'minute', 'hour', 'day', 'week'][::-1]
        res, duration = [], duration
        while duration > 0:
            n, unit = int(duration % 60), units.pop()
            unit = unit if n == 1 else unit + 's'
            res.append("{} {}".format(n, unit))
            duration //= 60
        return ' '.join(reversed(res))

    @classmethod
    def info(cls, file_path: str) -> dict:
        mi = mediainfo(file_path.strip())
        if 'size' in mi:
            mi['size'] = FormatPrint.sizeof_fmt(int(mi['size']))

        if 'duration' in mi:
            mi['duration'] = float(mi['duration'])
        return mi

    @staticmethod
    def read(file_name: str) -> fplist:
        texts = open(file_name, 'r').read().__str__()
        return fplist(texts.strip().split('\n'))

    @staticmethod
    def reads(file_name: str) -> str:
        '''Different with read method, this method will return string only'''
        return open(file_name, 'r').read().__str__()

    @staticmethod
    def rd(file_name: str, delimiter: str = '\n'):
        return FileIO.read(file_name, delimiter)

    @staticmethod
    def iter(filename: str) -> None:
        with open(filename, 'r') as f:
            for line in f:
                yield line.strip()

    @staticmethod
    def dumps(file_path: str, content: str) -> None:
        with open(file_path, 'w') as f:
            f.write(content)

    @staticmethod
    def write(cons: Union[str, List, set],
              file_name: str,
              mode='w',
              overwrite: bool = True) -> None:
        if not overwrite and FileIO.exists(file_name):
            print(f'{file_name} exists')
            return

        with open(file_name, mode) as f:
            if isinstance(cons, str):
                cons = [cons]
            text = '\n'.join(map(str, list(cons)))
            f.write(text)

    @staticmethod
    def wt(cons, file_name, mode='w', overwrite: bool = True):
        FileIO.write(cons, file_name, mode, overwrite)

    @staticmethod
    def say(*contents):
        for e in contents:
            if isinstance(e, dict) or isinstance(e, list):
                pretty_print(e)
            else:
                pprint.pprint(e)

    @classmethod
    def walk(cls, path, depth: int = 1, suffix=None):
        if depth <= 0:
            return []

        for f in os.listdir(path):
            abs_path = os.path.join(path, f)
            if os.path.isfile(abs_path):
                if not suffix or (suffix and abs_path.endswith(suffix)):
                    yield abs_path

            else:
                for sf in cls.walk(abs_path, depth - 1, suffix):
                    yield sf

    @staticmethod
    def exists(file_name: str) -> bool:
        return os.path.exists(file_name)

    @staticmethod
    def mkdir(dir: str) -> bool:
        os.mkdir(dir)

    @staticmethod
    def dirname() -> str:
        previous_frame = inspect.currentframe().f_back
        # (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
        filename, *_ = inspect.getframeinfo(previous_frame)
        return os.path.dirname(os.path.realpath(filename))

    @staticmethod
    def pwd() -> str:
        return subprocess.check_output(['pwd']).decode('utf-8').strip()

    @staticmethod
    def basename(file_path: str) -> str:
        return os.path.basename(file_path)

    @staticmethod
    def extension(file_path: str) -> str:
        return file_path.split('.').pop()

    @staticmethod
    def stem(file_path: str) -> str:
        ''' Get file name stem only. E.g., /tmp/gone-with-wind.json -> gone-with-wind '''
        return os.path.splitext(os.path.basename(file_path))[0]

    @staticmethod
    def path(file_path: str) -> str:
        return os.path.dirname(file_path)

    @staticmethod
    def rm(file_path: str) -> None:
        try:
            os.remove(file_path)
        except:
            pass

    @staticmethod
    def rename(old_name: str, new_name: str) -> None:
        os.rename(old_name, new_name)

    @staticmethod
    def copy(old_name: str, new_name: str) -> None:
        copy2(old_name, new_name)

    @staticmethod
    def home() -> str:
        from pathlib import Path
        return str(Path.home())

    @staticmethod
    def md5(file_path: str) -> str:
        import hashlib
        with open(file_path, "rb") as f:
            md5 = hashlib.md5()
            while True:
                chunk = f.read(8192)
                if chunk:
                    md5.update(chunk)
                else:
                    break
            return md5.hexdigest()
