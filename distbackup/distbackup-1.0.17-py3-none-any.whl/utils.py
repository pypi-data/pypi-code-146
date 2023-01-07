import sys
import os
import json
import re
import uuid
import argparse
import fnmatch
import traceback
from ktpanda.textcolor import Colorizer

class CacheDict(dict):
    '''Works like `defaultdict`, except it passes the key to the factory function'''
    def __init__(self, factory):
        super().__init__()
        self.factory = factory

    def __missing__(self, key):
        r = self[key] = self.factory(key)
        return r

class Progress:
    _global_instance = None

    def __init__(self):
        self.current_percent:float = 0.0
        self.converted_progress:int = 0
        self.status:str = ''

    @classmethod
    def set_global(cls, progress):
        cls._global_instance = progress

    @classmethod
    def get_global(cls):
        return cls._global_instance or NullProgress()

    def set_status(self, status:str):
        self.status = status
        self.display()

    def _convert_percent(self, percent:float):
        return int(percent * 10)

    def progress(self, percent:float):
        if percent is None:
            self.reset()
            return

        new_progress = self._convert_percent(percent)
        if new_progress != self.converted_progress:
            self.current_percent = percent
            self.converted_progress = new_progress
            self.display()

    def reset(self):
        self.status = ''
        self.current_percent = 0.0
        self.converted_progress = self._convert_percent(0.0)
        self.clear()

    def display(self):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

class NullProgress(Progress):
    def display(self):
        pass

    def clear(self):
        pass

class ProgressBar(Progress):
    def display(self):
        barsz = 90 - len(self.status) - 12
        barfill = int(self.current_percent * barsz / 100)
        text = f'\r\033[?7l {self.status} {self.current_percent:5.1f}% |{"=" * barfill}{" " * (barsz - barfill)}|\r\033[?7h'
        sys.stdout.write(text)
        sys.stdout.flush()

    def clear(self):
        sys.stdout.write('\r\033[K')
        sys.stdout.flush()

def progress(pct=None):
    if Progress._global_instance:
        Progress._global_instance.progress(pct)

_unit = list("BKMGTPE")
_unit_color = [
    'fff',
    '05f',
    '3f3',
    'fc0',
    'c0f',
    '0f9',
    '0f0',
]

def _prettysize(n):
    neg = n < 0
    if neg:
        n = -n
    un = 0
    while n >= 1000.0:
        n /= 1000.0
        un += 1
    pfx = ('-' if neg else '')
    if un:
        return pfx, format(n, '.2f'), un
    return pfx, format(n, 'd'), 0

def prettysize(n):
    pfx, num, magnitude = _prettysize(n)
    return f'{pfx}{num}{_unit[magnitude]}'

def size_color(n):
    _, _, magnitude = _prettysize(n)
    return _unit_color[magnitude]

def prettysize_clr(n, padding=0):
    pfx, num, magnitude = _prettysize(n)
    return Colorizer().t(f'{pfx}{num}{_unit[magnitude]}'.rjust(padding), fg=_unit_color[magnitude])

RX_COMMA = re.compile(r'(\d\d\d)(?=\d)')
def addcomma(n):
    n, sep, d = str(n).partition('.')
    return RX_COMMA.sub(r'\1,', n[::-1])[::-1] + sep + d

mul = dict(k=1000, m=1000000, g=1000000000, t=1000000000000)
def parsesize(s):
    if s is None:
        return None

    s = s.lower().replace(',', '')
    m = mul.get(s[-1:])
    if m:
        return int(float(s[:-1]) * m)
    return int(s)

def read_file(p, default=None):
    try:
        r = p.read_text().strip()
        return r or default
    except FileNotFoundError:
        return default

def write_file(p, data=None):
    tmpf = p.with_name(p.name + '~')
    with tmpf.open('w') as fp:
        fp.write(data + '\n')
        fp.flush()
        os.fsync(fp.fileno())
    tmpf.replace(p)

def try_unlink(p):
    try:
        os.unlink(p)
        return True
    except OSError:
        return False

def check_dir(f):
    f.parent.mkdir(parents=True, exist_ok=True)

def compact_json(data):
    return json.dumps(data, separators=(',',':'))

def canonical_path(path, tslash=False):
    if path is None:
        return None

    # Collapse all multiple slashes into one
    path = re.sub(r'[\\/]+', '/', path)

    # Remove extra slashes from the beginning
    path = '/' + (path.lstrip('/') if tslash is None else path.strip('/'))
    if tslash and path != '/':
        path += '/'
    return path

##########################################################################################
# Functions exported to SQLite
##########################################################################################

SQL_FUNCS = {}
def sqlf(f):
    def ret(*args):
        try:
            return f(*args)
        except Exception:
            traceback.print_exc()
            raise
    SQL_FUNCS[f.__name__] = ret
    return f

@sqlf
def disk_in_nexus(nexus, nexus_index):
    if nexus_index < 0 or nexus_index >= len(nexus):
        return False
    return nexus[nexus_index] == '1'

@sqlf
def nexus_with_disk(nexus, nexus_index):
    if nexus_index >= len(nexus):
        return nexus + '0' * (nexus_index - len(nexus)) + '1'
    return nexus[:nexus_index] + '1' + nexus[nexus_index + 1:]

@sqlf
def nexus_without_disk(nexus, nexus_index):
    if nexus_index >= len(nexus):
        return nexus
    return (nexus[:nexus_index] + '0' + nexus[nexus_index + 1:]).rstrip('0')

@sqlf
def nexus_level(nexus):
    return nexus.count('1')

@sqlf
def new_uuid():
    return str(uuid.uuid4())

@sqlf
def canonical_uuid(val):
    return str(uuid.UUID(val))

def prefix_upper(prefix):
    return prefix[:-1] + chr(1 + ord(prefix[-1:]))

def prefix_sql(column, prefix):
    return f'({column} >= ? AND {column} < ?)', (prefix, prefix_upper(prefix))

def escape_like(text):
    return text.replace('\\', r'\\').replace('%', r'\%').replace('_', r'\_')

def hash_relpath(hash):
    return f'distbackup-objects/{hash[:3]}/{hash}'

def pattern_to_regex(pat):
    if not pat:
        return None, None

    pat = canonical_path(pat, None)

    prefix = None
    m = re.match(r'^([^\*\.\[\?]+)', pat)
    if m:
        prefix = m.group(1)

    rxpattern = fnmatch.translate(pat)

    # fnmatch.translate tacks on \Z to match the end of the string
    if rxpattern.endswith(r'\Z'):
        rxpattern = rxpattern[:-2]

    # Match either an exact file, or any file in a subdirectory
    if pat.endswith('/'):
        rxpattern += r'(.*)?\Z'
    else:
        rxpattern += r'(/.*)?\Z'

    return re.compile(rxpattern, re.S), prefix

def round_blocks(s):
    return 4096 + (s + 4095) & ~4095

def int_mtime(m):
    return int(m * 1000)

def restore_mtime(m):
    return m / 1000.0
