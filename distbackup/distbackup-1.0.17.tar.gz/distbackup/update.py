import json
import fnmatch
import os
import re
import time
import logging

from typing import Optional
from collections import deque
from stat import S_ISREG, S_ISLNK, S_ISDIR

from ktpanda.sqlite_helper import in_transaction

from .constants import META_SUFFIX
from .errors import FileChanged
from .utils import int_mtime, compact_json, Progress
from .database import BackupDB
from .sourcefile import SourceFile

log = logging.getLogger(__name__)

class Matcher:
    RX_PATTERN = re.compile(r'^(!*)\s*([:\?/]?)(.*)')
    def __init__(self):
        self.patterns = []
        self.results = {}
        self.regex = None

    def add_pattern(self, pattern, result):
        key = f'p{len(self.patterns)}'
        self.patterns.append(f'{pattern}(?P<{key}>)')
        self.results[key] = result
        self.regex = None

    def parse_pattern(self, pattern):
        m = self.RX_PATTERN.match(pattern)
        prio, type, pat = m.groups()
        prio = len(prio)

        if type == ':':
            pat = r'\A' + re.escape(pat) + r'\Z'
        elif type == '?':
            pat = r'\A' + fnmatch.translate(pat)
        elif type  == '/':
            # Compile it now to validate it, even though we're just extracting the pattern
            # to combine later
            pat = re.compile(pat).pattern
        else:
            if re.search(r'[\*\?\[]', pat):
                pat = r'\A' + fnmatch.translate(pat)
            else:
                pat = r'\A' + re.escape(pat) + r'\Z'
        self.add_pattern(pat, prio)

    def match(self, fn):
        if self.regex is None:
            self.regex = re.compile('|'.join(self.patterns), re.S)
        m = self.regex.search(fn)
        if not m:
            return None
        return self.results[m.lastgroup]

    @classmethod
    def parse(cls, seq):
        self = cls()
        for pat in seq:
            self.parse_pattern(pat)
        return self

    @staticmethod
    def match_any(matchers, fn):
        for matcher in matchers:
            res = matcher.match(fn)
            if res is not None:
                return res
        return None

class Updater:
    def __init__(self, db:BackupDB, ignore_lock=False):
        self.db:BackupDB = db
        self.need_hash:list = []
        self.row_by_path:Optional[dict[str, tuple]] = None
        self.row_by_ino:Optional[dict[tuple, tuple]] = None
        self.ignore_lock:bool = ignore_lock
        self.symlink_unseen:set = set()

    def add_link(self, src, dest):
        if not self.db.readonly:
            self.db.execute_nonquery('INSERT OR REPLACE INTO symbolic_link(virtual_path, target) VALUES(?, ?)', (src, dest))
        self.symlink_unseen.pop(src, None)

    def update_file(self, virtual_path, srcf):
        oldhash = None
        fpath = srcf.path
        oldrow = self.row_by_path.pop(virtual_path, None)
        if not S_ISREG(srcf.mode):
            if oldrow:
                self.row_by_path[virtual_path] = oldrow

            if S_ISLNK(srcf.mode):
                dest = None
                try:
                    dest = os.readlink(fpath)
                except OSError:
                    pass
                if dest:
                    self.add_link(virtual_path, dest)

            return

        if srcf.priority == 0:
            return

        need_update_objects = False
        need_update_file_tree = False

        mtime = int_mtime(srcf.mtime)
        metatext = compact_json(srcf.metadata) if srcf.metadata else ''
        ometa = ''
        oprio = None

        ## Did the path already exist in the database?
        if oldrow:
            ## Is any of the data different?
            if oldrow[0] != mtime or oldrow[2] != srcf.size or oldrow[1] is None:
                need_update_file_tree = True

                ## Is the time different enough to need to rehash?
                if abs(oldrow[0] - mtime) >= 1000:
                    oldrow = None
        else:
            need_update_file_tree = True
            ## Check for a rename or hardlink.
            oldrow = self.row_by_ino.get((srcf.inode, srcf.size, mtime))

        if oldrow:
            omtime, oldhash, csize, opath, oino, ometa, oprio, omaxcopies = oldrow
            if opath != virtual_path:
                log.info(f'detect rename/hardlink {opath} -> {virtual_path}')

        if not oldhash:
            need_update_objects = True
            need_update_file_tree = True

            if srcf.hash is not None:
                log.info(f'hash {virtual_path} (precomputed)')
            elif srcf.size:
                log.info(f'need hash for {virtual_path} {srcf.path}')
                srcf.hash = ''
                self.need_hash.append((virtual_path, srcf))
        else:
            srcf.hash = oldhash

        if metatext != ometa or srcf.priority != oprio or srcf.maxcopies != omaxcopies:
            need_update_file_tree = True

        if srcf.size:
            if need_update_objects and srcf.hash and not self.db.readonly:
                self.db.execute_nonquery('INSERT OR IGNORE INTO object(hash) VALUES(?)', (srcf.hash,))
                self.db.execute_nonquery('UPDATE object SET size = ?, last_path = ?, last_modtime = ? WHERE hash = ?',
                             (srcf.size, virtual_path, mtime, srcf.hash))
        else:
            srcf.hash = None

        if need_update_file_tree and not self.db.readonly:
            self.db.execute_nonquery('INSERT OR REPLACE INTO file_tree(virtual_path, last_modified, hash, ino, size, priority, maxcopies, metadata) VALUES(?, ?, ?, ?, ?, ?, ?, ?)',
                         (virtual_path, int_mtime(srcf.mtime), srcf.hash, srcf.inode, srcf.size, srcf.priority or 1, srcf.maxcopies, metatext))

    def lock_path(self, vpath):
        log.info(f'{vpath} is locked')

        links = self.symlink_unseen
        locked_links = [k for k in links if k.startswith(vpath)]
        for k in locked_links:
            del links[k]

        bypath = self.row_by_path
        locked_files = [k for k in bypath if k.startswith(vpath)]
        for k in locked_files:
            del bypath[k]

    def walk_source(self):
        dq = deque()
        for virtual_path, real_path in self.db.iter_paths():
            dq.append((virtual_path, real_path, (), 1, None))

        while dq:
            vpath, apath, matchers, dir_priority, dir_maxcopies = dq.popleft()
            config = self.db.query_scalar('SELECT config FROM path_config WHERE virtual_path = ?', (vpath,))

            config = {} if config is None else json.loads(config)

            if not self.ignore_lock and config.get('lock'):
                self.lock_path(vpath)
                continue

            if config.get('hide'):
                continue

            config_prio = config.get('priority')
            if config_prio is not None:
                dir_priority = config_prio

            maxcopies = config.get('maxcopies')
            if maxcopies is not None:
                dir_maxcopies = maxcopies

            if dir_priority == 0:
                continue

            if (apath / ('.distbackup.skip')).exists():
                continue

            if config.get('noinherit', False):
                matchers = ()

            follow_links = config.get('follow_symlinks', False)

            rules = config.get('rules')
            if rules:
                matchers = (Matcher.parse(rules),) + matchers

            try:
                files = sorted(apath.iterdir())
            except EnvironmentError as e:
                log.warning(f'Cannot list {apath} ({e}), locking')
                self.lock_path(vpath)
                continue

            log.info(f'entering {vpath}')

            files.sort()
            for f in files:
                priority = Matcher.match_any(matchers, f.name)
                if priority == 0:
                    continue

                if priority is None:
                    priority = dir_priority

                virtual_path = f'{vpath.rstrip("/")}/{f.name}'
                if f.suffix == META_SUFFIX:
                    continue

                if self.db.get_mapped_path(virtual_path):
                    continue

                try:
                    srcf = SourceFile(f, f.stat() if follow_links else f.lstat())
                except os.error as e:
                    log.info(f'WARNING: cannot read {f} ({e})')
                    continue

                srcf.read_meta()
                if srcf.priority is None:
                    srcf.priority = priority

                if srcf.maxcopies is None:
                    srcf.maxcopies = dir_maxcopies

                while True:
                    self.update_file(virtual_path, srcf)
                    if S_ISDIR(srcf.mode):
                        dq.append((virtual_path + '/', f, matchers, priority, dir_maxcopies))
                    break

    def hash_files(self):
        self.db.check_run_deferred(True)

        try:
            for index, (virtual_path, srcf) in enumerate(self.need_hash):
                if self.db.readonly:
                    log.info(f'would hash {index + 1}/{len(self.need_hash)}: {virtual_path}')
                    continue

                while True:
                    log.info(f'hash {index + 1}/{len(self.need_hash)}: {virtual_path}')
                    try:
                        srcf.copy(self.db.check_run_deferred)
                        srcf.check_change()
                        break
                    except FileChanged:
                        log.info("file changed while reading!")
                        srcf.reset()
                        continue
                    except OSError as e:
                        log.info(f'WARNING: cannot read {virtual_path} ({e})')
                        break

                if srcf.hash:
                    self.db.defer(self.update_hash, virtual_path, srcf.hash, srcf.size, srcf.mtime)

                self.db.check_run_deferred()
        finally:
            self.db.check_run_deferred(True)

    def update_hash(self, virtual_path, hash, size, mtime):
        self.db.execute_nonquery('INSERT OR IGNORE INTO object(hash) VALUES(?)', (hash,))
        self.db.execute_nonquery('UPDATE object SET size = ?, last_path = ?, last_modtime = ? WHERE hash = ?',
                                 (size, virtual_path, int_mtime(mtime), hash))
        self.db.execute_nonquery('UPDATE file_tree SET hash = ? WHERE virtual_path = ?', (hash, virtual_path))

    def update_source(self, ignore_lock=False):
        self.need_hash = []
        self._update_source(ignore_lock)
        self.hash_files()

    @in_transaction(mode='IMMEDIATE', attr='db')
    def _update_source(self, ignore_lock=False):
        bypath = self.row_by_path = {}
        byino = self.row_by_ino = {}
        self.ignore_lock = ignore_lock

        cnt = self.db.query_scalar('SELECT count(virtual_path) FROM file_tree')
        i = 0
        t = time.time()
        progress = Progress.get_global()
        progress.set_status('loading db...')

        with self.db.execute('SELECT last_modified, hash, size, virtual_path, ino, metadata, priority, maxcopies FROM file_tree') as curs:
            for row in curs:
                bypath[row[3]] = row
                byino[(row[4], row[2], row[0])] = row

                i += 1
                progress.progress((i + 1) * 100 / cnt)

        with self.db.execute('SELECT virtual_path, target FROM symbolic_link') as curs:
            self.symlink_unseen = dict(curs)

        progress.reset()

        e = time.time()
        log.info(f'loaded in {e - t}s')

        self.walk_source()

        for path in sorted(self.row_by_path.keys()):
            log.info(f'deleted: {path}')

        if not self.db.readonly:
            self.db.executemany('DELETE FROM file_tree WHERE virtual_path = ?', ((k,) for k in self.row_by_path))
            self.db.executemany('DELETE FROM symbolic_link WHERE virtual_path = ?', ((k,) for k in self.symlink_unseen))
        self.db.cleanrefs()
