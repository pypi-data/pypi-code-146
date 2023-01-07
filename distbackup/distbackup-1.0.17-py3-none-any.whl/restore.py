import os
import logging

from typing import Optional
from collections import deque
from pathlib import Path

from .utils import check_dir, restore_mtime
from .database import BackupDB
from .sourcefile import SourceFile
log = logging.getLogger(__name__)

class Restore:
    def __init__(self, db:BackupDB, restore_path:Optional[Path]=None, sync:bool=False):
        self.db:BackupDB = db
        self.sync:bool = sync
        self.restore_path:Optional[Path] = restore_path

    def _restore_one(self, f, hashpath, hash, path, lastmod):
        log.info(f'{hash} -> {path}')
        try:
            dpath = self.restore_path / path
            check_dir(dpath)
            f(hashpath, dpath)
        except OSError as e:
            log.error(f'Error restoring {path}: {e}')

        try:
            tm = restore_mtime(lastmod)
            os.utime(dpath, (tm, tm))
        except OSError as e:
            pass

    def _restore(self, f, pat=None, existing=()):
        self.db.require_disk_path()
        self.db.current_disk.migrate_data()
        not_present = []
        existing = [Path(v) for v in existing]
        if self.restore_path:
            existing.append(self.restore_path)

        for path, lastmod, hash, nexus in self.db.filter_files(pat, existing):
            path = path.lstrip('/')
            if hash is None:
                dpath = self.restore_path / path
                check_dir(dpath)
                dpath.write_bytes(b'')
                continue

            hashpath = self.db.current_disk.hashpath(hash)
            if hashpath.exists():
                self._restore_one(f, hashpath, hash, path, lastmod)
            elif nexus:
                not_present.append(path)


        for path, dest in self.db.filter_files(pat, existing, 'SELECT ft.virtual_path, ft.target FROM symbolic_link AS ft'):
            try:
                dpath = self.restore_path / path
                check_dir(dpath)
                dpath.symlink_to(dest)

            except OSError as e:
                log.error(f'Error restoring link {path}: {e}')

        if not_present:
            log.info('')
            log.info('The following files still need to be restored:')
            for file in not_present:
                log.info(f'  {file}')
            log.info(f'total not present: {len(not_present)}')

    def restore_link(self, pat=None, existing=()):
        self._restore(os.link, pat, existing)

    def restore_copy(self, pat=None, existing=()):
        def f(fpath, dpath):
            srcf = SourceFile(fpath)
            tmppath = dpath.with_name(f'{dpath.name}.dbtmp~')
            try:
                srcf.setdest(tmppath)
                srcf.copy()
                tmppath.replace(dpath)
            finally:
                if tmppath.exists():
                    tmppath.unlink()

        self._restore(f, pat, existing)

    def restore_set(self, pat=None, existing=()):
        matching_nexus = set()
        existing = [Path(v) for v in existing]
        disk_names = {i: disk.name for i, disk in self.db.disk_by_index.items()}

        sql = 'SELECT ft.virtual_path, ft.last_modified, ft.hash, f.nexus FROM file_tree AS ft INNER JOIN object AS f ON ft.hash = f.hash'
        filecount = 0
        for path, lastmod, hash, nexus in self.db.filter_files(pat, existing, sql):
            if nexus:
                filecount += 1
                matching_nexus.add(nexus)

        if not filecount:
            log.info(f'No files match "{pat}".')
            return

        max_disk = max(len(z) for z in matching_nexus)
        disk_seq = range(0, max_disk)

        def build_rtn(disks, cnt, sets):
            for j, next_set in disk_set:
                log.info(f'{j+1:5d} {len(next_set):5d} {next_set}')

        log.info(f'Finding minimum set for {filecount} files matching "{pat}" ...')

        all_file_nexus = set(sum((1<<i) for i, c in enumerate(nexus) if c == '1') for nexus in matching_nexus)
        for z in sorted(all_file_nexus):
            log.info(' '.join((disk_names.get(j, '?') if (z&(1<<j)) else '--').ljust(10) for j in disk_seq))

        found_list = None
        search_queue = deque()
        search_queue.append((0, all_file_nexus))
        while search_queue:
            chosen_disks, sets = search_queue.popleft()
            disk_set = [(disk_id, set()) for disk_id in disk_seq if not chosen_disks & (1<<disk_id)]
            for disk_id, next_set in disk_set:
                mask = 1 << disk_id
                if mask & chosen_disks:
                    continue
                for nexus_set in sets:
                    if not nexus_set & mask:
                        next_set.add(nexus_set & ~mask)

            disk_set.sort(key=lambda v: len(v[1]))
            del disk_set[4:]
            for disk_id, next_set in disk_set:
                new_chosen = chosen_disks | (1 << disk_id)
                if not next_set:
                    found_list = new_chosen
                    break
                search_queue.append((new_chosen, next_set))
            if found_list is not None:
                break

        log.info('')
        log.info('The smallest set of disks that contains the files is:')
        log.info('    ' + ' '.join([disk_names.get(n, '?') for n in disk_seq if found_list & (1 << n)]))
