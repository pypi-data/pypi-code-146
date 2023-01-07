import re
import traceback
import time
import sqlite3
import uuid
import json
import logging

from typing import Optional
from pathlib import Path

# Third party imports
from ktpanda.sqlite_helper import SQLiteDB, in_transaction

from .constants import DBNAME, DEFAULT_CONFIG
from .disk import BackupDisk
from .nexus import Nexus
from .utils import (SQL_FUNCS, addcomma, canonical_path, canonical_uuid, compact_json,
                    disk_in_nexus, new_uuid, nexus_level, nexus_with_disk, nexus_without_disk,
                    pattern_to_regex, prefix_sql, Progress)
from .errors import ArgumentError, DiskNotFoundError
from .schema import PRE_DATA, SCHEMA_VERSION, TABLES_INDICES, TRIGGERS

log = logging.getLogger(__name__)

class BackupDB(SQLiteDB):
    common_schema = TABLES_INDICES + TRIGGERS + PRE_DATA
    schema_version = SCHEMA_VERSION

    def __init__(self, dbpath:Path, readonly:bool=False, verbose:bool=False):
        if dbpath.is_dir():
            dbpath = dbpath / DBNAME

        super().__init__(dbpath, readonly=readonly)

        self.verbose = verbose

        self.disk_by_index:dict[int, BackupDisk] = {}
        self.disk_by_uuid:dict[str, BackupDisk] = {}
        self.disk_by_name:dict[str, BackupDisk] = {}
        self._disk_name_index:list[tuple[str, int]] = []

        self.current_disk:Optional[BackupDisk] = None
        self.defer_queue:list[tuple] = []
        self.last_run_deferred:float = 0

        self.path_map:dict[str, Path] = {}
        self.path_cache:dict[str, Path] = {}
        #self.diropt_cache = {}

        self.nocopydb:bool = False

    ##########################################################################################
    # Upgrades
    ##########################################################################################

    def _upgrade_to_13(self, oldvers):
        self.backend.execute('ALTER TABLE disks ADD COLUMN relative_path TEXT')

    def _upgrade_to_16(self, oldvers):
        self.backend.execute("ALTER TABLE file_names ADD COLUMN metadata TEXT NOT NULL DEFAULT ''")

    def _upgrade_to_18(self, oldvers):
        for column in ('file_names.path', 'path_map.virtual_path', 'path_config.virtual_path', 'links.path', 'files.last_path'):
            table, column = column.split('.')
            sql = f"UPDATE {table} SET {column} = '/' || {column} WHERE {column} NOT LIKE '/%'"
            self.backend.execute(sql)

    def _upgrade_to_20(self, oldvers):
        if self.backend.execute("SELECT name FROM sqlite_master WHERE name = 'source_path'"):
            self.backend.execute('ALTER TABLE source_path RENAME TO path_map')

        if self.backend.execute("SELECT name FROM sqlite_master WHERE name = 'source_config'"):
            self.backend.execute('ALTER TABLE source_config RENAME TO path_config')

    def _drop_triggers(self):
        triggers = [row[0] for row in self.backend.execute("SELECT name FROM sqlite_master WHERE type = 'trigger'")]
        for trigger in triggers:
            self.backend.execute(f'DROP TRIGGER {trigger}')

    def _upgrade_to_21(self, oldvers):
        '''*BIG UPDATE* - drop all triggers, create the new tables, copy
        the data over, then let it create the new triggers'''

        self._drop_triggers()

        self.exec_schema(TABLES_INDICES)

        self.backend.create_function('newid', 0, new_uuid)
        self.backend.execute('INSERT INTO object(hash, size, nexus, refs, last_path, last_modtime) SELECT hash, size, nexus, refs, last_path, last_lastmod FROM files')
        self.backend.execute('INSERT INTO file_tree(virtual_path, last_modified, hash, ino, size, metadata) SELECT path, lastmod, hash, ino, size, metadata FROM file_names')
        self.backend.execute('INSERT INTO symbolic_link(virtual_path, target) SELECT path, dest FROM links')
        self.backend.execute('INSERT INTO disk(uuid, name, nexus_index, relative_path, size) SELECT IFNULL(uuid, newid()), name, id - 1, relative_path, size FROM disks')
        self.backend.execute('INSERT INTO nexus(nexus, refs, totalsize) SELECT nexus, refs, totalsize FROM dist_nexus')
        self.backend.execute('DROP TABLE files')
        self.backend.execute('DROP TABLE file_names')
        self.backend.execute('DROP TABLE links')
        self.backend.execute('DROP TABLE disks')
        self.backend.execute('DROP TABLE dist_nexus')
        self.backend.execute('DROP TABLE IF EXISTS vars')
        self.backend.execute('DROP TABLE IF EXISTS source_lock')

    def _upgrade_to_22(self, oldvers):
        self._drop_triggers()
        self.backend.execute("ALTER TABLE file_tree ADD COLUMN maxcopies INTEGER")
        self.backend.execute("ALTER TABLE object ADD COLUMN maxcopies INTEGER")

    def _upgrade_to_23(self, oldvers):
        self._drop_triggers()
        self.backend.execute("ALTER TABLE nexus RENAME COLUMN count TO level")

    def _upgrade_to_24(self, oldvers):
        self.backend.execute("ALTER TABLE nexus ADD COLUMN disks TEXT NOT NULL DEFAULT ''")
        self.update_nexus_disk_text()

    def _upgrade_to_25(self, oldvers):
        self._drop_triggers()
        self.backend.execute('ALTER TABLE object RENAME TO old_object')
        self.backend.execute('ALTER TABLE file_tree RENAME TO old_file_tree')
        self.exec_schema(TABLES_INDICES)
        self.backend.execute('INSERT INTO object(hash, size, nexus, refs, priority, last_path, last_modtime) SELECT hash, size, nexus, refs, priority, last_path, last_modtime FROM old_object')
        self.backend.execute('INSERT INTO file_tree(virtual_path, last_modified, hash, ino, size, priority, metadata) SELECT virtual_path, last_modified, hash, ino, size, priority, metadata FROM old_file_tree')
        self.backend.execute('DROP TABLE old_object')
        self.backend.execute('DROP TABLE old_file_tree')

    def _upgrade_to_26(self, oldvers):
        self._drop_triggers()

    def _upgrade_to_27(self, oldvers):
        self._drop_triggers()
        # Add STRICT option to all tables
        self.alter_schema(
            ("type = 'table'", (), r'(\)\s*)(WITHOUT ROWID\s*)$', r'\1STRICT, \2'),
            ("type = 'table'", (), r'(\))(\s*)$', r'\1 STRICT\2'),
            debug=False
        )

    def _upgrade_to_28(self, oldvers):
        self._drop_triggers()

    def _upgrade_to_29(self, oldvers):
        self._drop_triggers()
        self.backend.execute("ALTER TABLE object ADD COLUMN saturated INTEGER GENERATED ALWAYS AS (CASE WHEN copies >= maxcopies THEN 1 ELSE 0 END)")
        self.backend.execute("ALTER TABLE object ADD COLUMN relevant_size INTEGER GENERATED ALWAYS AS (CASE WHEN refs > 0 THEN blocksize ELSE 0 END)")
        self.backend.execute("ALTER TABLE object ADD COLUMN saturated_size INTEGER GENERATED ALWAYS AS (CASE WHEN copies >= maxcopies AND refs > 0 THEN blocksize ELSE 0 END)")
        self.backend.execute("ALTER TABLE nexus ADD COLUMN saturated_size INTEGER NOT NULL DEFAULT 0")

    def _upgrade_to_30(self, oldvers):
        self._drop_triggers()
        self.backend.execute("UPDATE nexus SET saturated_size = COALESCE((SELECT SUM(saturated_size) FROM object o WHERE o.nexus = nexus.nexus), 0)")
        self.backend.execute("UPDATE nexus SET totalsize = COALESCE((SELECT SUM(relevant_size) FROM object o WHERE o.nexus = nexus.nexus), 0)")

    def _upgrade_to_31(self, oldvers):
        self._drop_triggers()
        self.backend.execute("UPDATE object SET last_path = '' WHERE last_path ISNULL")
        self.backend.execute("UPDATE object SET last_modtime = 0 WHERE last_modtime ISNULL")
        self.alter_schema(
            ("type = 'table' AND name = 'object'", (), lambda text: (
                re.sub(r'(last_path TEXT)(\s*,)', r"\1 NOT NULL DEFAULT ''\2",
                       re.sub(r'(last_modtime INTEGER)(\s*,)', r"\1 NOT NULL DEFAULT 0\2", text))
            )),
            debug=True
        )

    ##########################################################################################
    # Database
    ##########################################################################################

    def connect(self, *a, **kw):
        super().connect(*a, **kw)
        for n, f in SQL_FUNCS.items():
            self.backend.create_function(n, -1, f)

        self.disk_by_index = {}
        self.disk_by_name = {}
        self.disk_by_uuid = {}
        with self.execute('SELECT uuid, name, nexus_index, relative_path, size, fstype, fsuuid FROM disk WHERE name NOTNULL') as curs:
            for uuid, name, nexus_index, relative_path, size, fstype, fsuuid in curs:
                disk = BackupDisk(uuid, name, nexus_index, relative_path, size, fstype, fsuuid)
                self.disk_by_uuid[uuid] = disk
                self.disk_by_index[nexus_index] = disk
                self.disk_by_name[name] = disk

        self._disk_name_index = sorted((disk.name, index) for index, disk in self.disk_by_index.items())

        self.path_map = {
            virtual_path: Path(real_path)
            for virtual_path, real_path in
            self.query_list('SELECT virtual_path, real_path FROM path_map')
        }
        self.path_cache = self.path_map.copy()

    @in_transaction
    def copy_database(self, dest_dir=None):
        if dest_dir is None:
            dest_dir = self.current_disk.data_path

        self.execute_nonquery('PRAGMA wal_checkpoint(FULL)')
        if self.nocopydb:
            return

        if not self.current_disk or not self.current_disk.data_path:
            return

        progress = Progress.get_global()
        progress.set_status('copying database')
        tmppath = dest_dir / (DBNAME + '.new')
        backup_db = sqlite3.connect(tmppath)
        def log_progress(status, remaining, total):
            progress.progress((total - remaining) * 100 / total)

        self.backend.backup(backup_db, pages=256, progress=log_progress)
        backup_db.commit()
        backup_db.execute('PRAGMA wal_checkpoint(FULL)')
        backup_db.close()
        progress.reset()

        dstf = tmppath.with_name(DBNAME)
        tmppath.replace(dstf)

    def defer(self, f, *a, **kw):
        '''Queue a database-modifying function to run in the near future in a transaction.'''
        self.defer_queue.append((f, a, kw))

    @in_transaction
    def _run_deferred(self):
        for f, a, kw in self.defer_queue:
            f(*a, **kw)
        del self.defer_queue[:]

    def check_run_deferred(self, force=False):
        ctime = time.time()
        if force or ctime >= self.last_run_deferred + 0.2:
            self.last_run_deferred = ctime
            if self.defer_queue:
                self._run_deferred()

    def load_nexus(self):
        rtn = {}
        with self.execute('SELECT nexus, level, refs, totalsize, saturated_size, disks FROM nexus') as curs:
            for nexus, level, refs, totalsize, saturated_size, disks in curs:
                rtn[nexus] = Nexus(nexus, level, refs, totalsize, saturated_size, disks)
        return rtn

    def create_empty_nexus(self, nexusid:str):
        return Nexus(nexusid, nexus_level(nexusid), 0, 0, 0, ','.join(self.nexus_disks(nexusid)))

    def get_used_space(self, nexus_index):
        return self.query_scalar('SELECT COALESCE(sum(totalsize), 0) FROM nexus WHERE disk_in_nexus(nexus, ?)', (nexus_index,))

    def update_free_space(self):
        self.current_disk.used_space = self.get_used_space(self.current_disk.nexus_index)

    ##########################################################################################
    # Disk selection
    ##########################################################################################

    def set_backup_disk(self, arg):
        if '/' in arg:
            path = Path(arg)
            if not path.is_dir():
                raise DiskNotFoundError(f'path {path} does not exist or is not a directory')

            rdisk = BackupDisk.read_config(path)
            if not rdisk:
                raise DiskNotFoundError(f'path {path} does not contain a valid distbackup config')

            try:
                disk = self.disk_by_uuid[rdisk.uuid]
            except KeyError:
                raise ArgumentError(f'path {path} is from a different backup set') from None

            disk.data_path = path
            if disk.name != rdisk.name:
                disk.write_config()

            return self._set_current_disk(disk)

        try:
            return self.set_backup_disk_from_uuid(arg)
        except (ValueError, DiskNotFoundError):
            pass

        return self.set_backup_disk_from_name(arg)

    def set_backup_disk_from_name(self, name, search_data=True):
        try:
            disk = self.disk_by_name[name]
        except KeyError:
            raise DiskNotFoundError(f'disk {name} not found') from None

        self._set_current_disk(disk, search_data)

    def set_backup_disk_from_uuid(self, diskuuid, search_data=True):
        try:
            disk = self.disk_by_uuid[str(uuid.UUID(diskuuid))]
        except KeyError:
            raise DiskNotFoundError(f'disk {diskuuid} not found') from None

        self._set_current_disk(disk, search_data)

    def _set_current_disk(self, disk, search_data=True):
        self.current_disk = disk
        if not disk.data_path and search_data:
            BackupDisk.find_disk_data_paths([disk])

        log.debug(f'using data path {disk.data_path}')
        self.update_free_space()


    def require_disk(self):
        if not self.current_disk:
            raise ArgumentError('no disk selected')

    def require_disk_path(self):
        self.require_disk()
        if not self.current_disk.data_path:
            raise ArgumentError(f'{self.current_disk.name} is not mounted, or not configured correctly')

    def find_disk_data_paths(self):
        BackupDisk.find_disk_data_paths(self.disk_by_uuid.values())

    ##########################################################################################
    # Disk management
    ##########################################################################################

    @in_transaction('IMMEDIATE')
    def add_disk(self, name, path, size=None):
        uuid = new_uuid()
        new_disk = BackupDisk(uuid, name, None, size)
        new_disk.set_from_path(path)

        try:
            nexus_index = self.query_scalar('SELECT COALESCE((SELECT MIN(nexus_index) FROM disk WHERE name ISNULL), (SELECT MAX(nexus_index) + 1 FROM disk), 0)')
            new_disk.nexus_index = nexus_index
            self.execute_nonquery('DELETE FROM disk WHERE nexus_index = ?', (nexus_index,))
            self.execute_nonquery(
                'INSERT INTO disk(uuid, name, nexus_index, size, relative_path, fstype, fsuuid) VALUES(?, ?, ?, ?, ?, ?, ?)',
                (uuid, name, nexus_index, new_disk.size, new_disk.relative_path, new_disk.fstype, new_disk.fsuuid))

        except sqlite3.IntegrityError as e:
            raise ArgumentError(f'disk {name} already exists ({e})') from None

        self.current_disk = new_disk

        self.disk_by_index[nexus_index] = new_disk
        self.disk_by_name[name] = new_disk
        self.disk_by_uuid[uuid] = new_disk
        self._disk_name_index = sorted((disk.name, index) for index, disk in self.disk_by_index.items())

        self.update_nexus_disk_text()
        self.update_free_space()
        new_disk.write_config()
        new_disk.migrate_data()

        return new_disk

    @in_transaction
    def rename_disk(self, newname):
        self.require_disk()
        self.execute_nonquery('UPDATE disk SET name = ? WHERE uuid = ?', (newname, self.current_disk.uuid))
        self.disk_by_name.pop(self.current_disk.name, None)
        self.current_disk.name = newname
        self.disk_by_name[newname] = self.current_disk

        self.update_nexus_disk_text()

        if self.current_disk.data_path:
            self.current_disk.write_config()

    @in_transaction
    def set_disk_params(self, size=None, relpath=None, path=None, fstype=None, fsuuid=None):
        disk = self.current_disk
        if path is not None:
            disk.set_from_path(path)
            self.execute_nonquery(
                'UPDATE disk SET relative_path= ?, fstype = ?, fsuuid = ? WHERE uuid = ?',
                (disk.relative_path, disk.fstype, disk.fsuuid, disk.uuid)
            )

        if size is not None:
            self.execute_nonquery('UPDATE disk SET size = ? WHERE uuid = ?', (size, disk.uuid))
            disk.size = size

        if relpath is not None:
            disk.relative_path = relpath or None
            self.execute_nonquery('UPDATE disk SET relative_path = ? WHERE uuid = ?', (disk.relative_path, disk.uuid))

        if fstype is not None:
            disk.fstype = fstype or None
            self.execute_nonquery('UPDATE disk SET fstype = ? WHERE uuid = ?', (disk.fstype, disk.uuid))

        if fsuuid is not None:
            disk.fsuuid = fsuuid or None
            self.execute_nonquery('UPDATE disk SET fsuuid = ? WHERE uuid = ?', (disk.fsuuid, disk.uuid))

        self.update_nexus_disk_text()

        if disk.data_path:
            disk.write_config()

    def drop_disk_objects(self):
        index = self.current_disk.nexus_index
        with self.execute('SELECT nexus, level, totalsize FROM nexus') as curs:
            for nexus, copies, totalsize in curs:
                if disk_in_nexus(nexus, index):
                    new_nexus = nexus_without_disk(nexus, index)
                    self.execute_nonquery('UPDATE object SET nexus = ? WHERE nexus = ?', (new_nexus, nexus))

    @in_transaction
    def drop_disk(self):
        self.require_disk()
        self.drop_disk_objects()
        self.update_nexus_disk_text(only_new=True)
        self.cleanrefs()

    @in_transaction
    def delete_disk(self):
        self.require_disk()

        used_space = self.query_scalar('SELECT sum(totalsize) FROM nexus WHERE disk_in_nexus(nexus, ?)', (self.current_disk.nexus_index,))
        if used_space:
            print(f'{self.current_disk.name} has backup files (use `disk drop`)')
            return

        self.execute_nonquery('UPDATE disk SET name = NULL WHERE uuid = ?', (self.current_disk.uuid,))
        self.cleanrefs()

    @in_transaction
    def _refresh_disk(self):
        self.require_disk()
        self.current_disk.migrate_data()
        self.drop_disk_objects()
        for hash, fpath, stat in self.current_disk.walk_data():
            log.info(f'found {hash}')
            self.execute_nonquery('INSERT OR IGNORE INTO object(hash, size) VALUES(?, ?)', (hash, stat.st_size))
            self.set_object_on_disk(hash, self.current_disk.nexus_index, True)

        self.update_nexus_disk_text(only_new=True)
        self.cleanrefs()

    def refresh_disk(self):
        self._refresh_disk()
        self.update_free_space()
        self.copy_database()

    ##########################################################################################
    # Configuration
    ##########################################################################################

    @in_transaction
    def map_source(self, vpath:str, ppath:str):
        self.execute_nonquery('INSERT OR REPLACE INTO path_map(virtual_path, real_path) VALUES(?, ?)', (vpath, ppath))

    @in_transaction
    def unmap_source(self, vpath:str):
        rowcount, lastrowid = self.execute_nonquery('DELETE FROM path_map WHERE virtual_path = ?', (vpath,))
        return rowcount > 0

    @in_transaction
    def set_path_config(self, paths:list[str], updates:dict, clear:bool=False, append_keys=()):
        rtn = []
        for vpath in paths:
            vpath = canonical_path(vpath, True)
            prev_config_text = self.query_scalar('SELECT config FROM path_config WHERE virtual_path = ?', (vpath,))
            prev_config = json.loads(prev_config_text) if prev_config_text else {}

            if prev_config_text is None:
                config = updates.copy()
                if config:
                    self.execute_nonquery('INSERT INTO path_config(virtual_path, config) VALUES(?, ?)', (vpath, compact_json(config)))
            else:
                config = {} if clear else prev_config.copy()
                for key, val in updates.items():
                    if val is None or val == DEFAULT_CONFIG.get(key):
                        config.pop(key, None)
                    else:
                        if key in append_keys:
                            newval = list(config.get(key) or ())
                            for cval in val:
                                if cval not in newval:
                                    newval.append(cval)
                            val = newval
                        config[key] = val
                if config:
                    self.execute_nonquery('UPDATE path_config SET config = ? WHERE virtual_path = ?', (compact_json(config), vpath))
                else:
                    self.execute_nonquery("DELETE FROM path_config WHERE virtual_path = ?", (vpath,))

            rtn.append((vpath, prev_config, config))
        return rtn

    def export_config(self, path_prefix=None):
        path_config = {}
        disks = {}
        data = {
            'path_map': {
                k: str(v) for k, v in self.path_map.items()
            }
        }

        sql = 'SELECT virtual_path, config FROM path_config'
        args = ()
        if path_prefix:
            # Make sure the specified path is in the resulting export
            path_config[path_prefix] = {}
            text, args = prefix_sql('virtual_path', path_prefix)
            sql += " WHERE " + text

            data['path_prefix'] = path_prefix

        data['path_config'] = path_config
        for path, config in self.execute(sql, args):
            path_config[path] = json.loads(config)

        data['disks'] = disks
        with self.execute('SELECT uuid, name, relative_path, size, fstype, fsuuid FROM disk WHERE name NOTNULL') as curs:
            for uuid, name, relative_path, size, fstype, fsuuid in curs:
                disks[uuid] = {
                    'name': name,
                    'size_bytes': addcomma(size),
                    'relative_path': relative_path,
                    'fstype': fstype,
                    'fsuuid': fsuuid
                }

        return data

    @in_transaction
    def import_config(self, data):
        if 'path_map' in data:
            self.execute_nonquery('DELETE FROM path_map')
            for virtual_path, real_path in data['path_map'].items():
                if not isinstance(real_path, str):
                    raise ValueError(f'Expected string for path map: {virtual_path!r}, got {type(real_path).__name__!r}')

                virtual_path = canonical_path(virtual_path, True)
                self.execute_nonquery('INSERT INTO path_map(virtual_path, real_path) VALUES(?, ?)', (virtual_path, real_path))

        if 'path_config' in data:
            path_prefix = data.get('path_prefix')
            if path_prefix:
                text, args = prefix_sql('virtual_path', path_prefix)

                self.execute_nonquery("DELETE FROM path_config WHERE " + text, args)
            else:
                self.execute_nonquery('DELETE FROM path_config')

            for virtual_path, config in data['path_config'].items():
                virtual_path = canonical_path(virtual_path, True)
                if not isinstance(config, dict):
                    raise ValueError(f'Expected dict for path config: {virtual_path!r}, got {type(config).__name__}')

                for key, val in DEFAULT_CONFIG.items():
                    if key in config and type(val) != type(config[key]):
                        raise ValueError(f'Path {virtual_path}: Expected {type(val).__name__} for {key}, got {type(config[key]).__name__}')

                self.execute_nonquery('INSERT INTO path_config(virtual_path, config) VALUES(?, ?)', (virtual_path, compact_json(config)))

        if 'disks' in data:
            for uuid, config in data['disks'].items():
                realuuid = self.query_scalar('SELECT uuid FROM disk WHERE uuid = ?', (canonical_uuid(uuid),))
                if realuuid is None:
                    raise ValueError(f'Disk with UUID {realuuid} not in database (disks cannot be added with import)')

                if 'size_bytes' in config:
                    size = int(str(config['size_bytes']).replace(',', ''))
                    self.execute_nonquery('UPDATE disk SET size = ? WHERE uuid = ?', (size, realuuid))

                if 'relative_path' in config:
                    val = config['relative_path']
                    self.execute_nonquery('UPDATE disk SET relative_path = ? WHERE uuid = ?', (val, realuuid))

                if 'fstype' in config:
                    val = config['fstype']
                    self.execute_nonquery('UPDATE disk SET fstype = ? WHERE uuid = ?', (val, realuuid))

                if 'fsuuid' in config:
                    val = config['fsuuid']
                    self.execute_nonquery('UPDATE disk SET fsuuid = ? WHERE uuid = ?', (val, realuuid))

                if 'name' in config:
                    val = config['name']
                    self.execute_nonquery('UPDATE disk SET name = ? WHERE uuid = ?', (val, realuuid))

    ##########################################################################################
    # Utils
    ##########################################################################################

    def nexus_disks(self, nexus):
        '''Given a nexus ID, yields a sequence of the names of the disks in the nexus.'''
        for name, index in self._disk_name_index:
            if disk_in_nexus(nexus, index):
                yield name

    @in_transaction('IMMEDIATE')
    def cleanrefs(self):
        if not self.readonly:
            self.execute_nonquery('DELETE FROM nexus WHERE refs = 0 AND nexus != \'\'')
            self.execute_nonquery('DELETE FROM object WHERE refs = 0 AND copies = 0')

    @in_transaction
    def update_nexus_disk_text(self, only_new:bool=False):
        updates = []
        disk_names = {}
        with self.execute('SELECT name, nexus_index FROM disk WHERE name NOTNULL') as curs:
            for name, index in curs:
                disk_names[index] = name

        with self.execute('SELECT nexus, disks FROM nexus' + (" WHERE disks = ''" if only_new else '')) as curs:
            for nexus, text in curs:
                new_text = ','.join(sorted(name for i, c in enumerate(nexus) if (c == '1' and (name := disk_names.get(i)))))
                if new_text != text:
                    updates.append((new_text, nexus))
        if updates:
            with self.executemany('UPDATE nexus SET disks = ? WHERE nexus = ?', updates) as curs:
                pass

    def filter_files(self, pat=None, existing=(), sql='SELECT ft.virtual_path, ft.last_modified, ft.hash, ob.nexus FROM file_tree ft LEFT JOIN object ob ON ft.hash = ob.hash'):
        rx, prefix = pattern_to_regex(pat)

        args = ()
        if prefix:
            text, args = prefix_sql('ft.virtual_path', prefix)
            sql += r" WHERE " + text

        with self.execute(sql, args) as curs:
            for row in curs:
                path = row[0]
                if rx and not rx.match(path):
                    continue

                if any((base / path).exists() for base in existing):
                    continue

                yield row

    @in_transaction
    def set_object_on_disk(self, hash, diskid, present):
        prev_nexus = self.query_scalar('SELECT nexus FROM object WHERE hash = ?', (hash,))
        nexus = nexus_with_disk(prev_nexus, diskid) if present else nexus_without_disk(prev_nexus, diskid)
        if nexus != prev_nexus:
            self.execute_nonquery('UPDATE object SET nexus = ? WHERE hash = ?', (nexus, hash))
        return nexus

    @in_transaction
    def set_file_hash(self, vpath, hash):
        self.execute_nonquery('UPDATE file_tree SET hash = ? WHERE virtual_path = ?', (hash, vpath))

    ##########################################################################################
    # Path map
    ##########################################################################################

    def iter_paths(self):
        return self.path_map.items()

    def get_mapped_path(self, vpath:str):
        return self.path_map.get(vpath)

    def get_dir_path(self, dir):
        path = self.path_cache.get(dir + '/')
        if path is None:
            if not dir:
                return None
            parent, _, dirname = dir.rpartition('/')
            parent_path = self.get_dir_path(parent)
            if parent_path is None:
                return None
            path = self.path_cache[dir] = parent_path / dirname
        return path

    def get_file_path(self, fn):
        dir, _, filename = fn.rpartition('/')
        dir_path = self.get_dir_path(dir)
        if dir_path is None:
            return None
        return dir_path / filename
