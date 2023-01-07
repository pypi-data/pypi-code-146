import sys
import os
import re
import logging
import time
import json
import subprocess
import traceback
import tempfile
from pathlib import Path

from ktpanda.textcolor import Colorizer

from .constants import DEFAULT_CONFIG
from .database import BackupDB
from .utils import (canonical_path, escape_like, prefix_upper,
                    addcomma, prettysize, round_blocks, parsesize, restore_mtime)
from .nexus import NexusLevelDict

from ktpanda.cli import Parser, arg

log = logging.getLogger(__name__)

arg_parser = Parser(description='', default_func=lambda db, parser, args: parser.print_help())
command = arg_parser.command

##########################################################################################
# Completers
##########################################################################################

def complete_virtual_path(prefix, parsed_args, **kwargs):
    db = open_db(parsed_args, expand=True)
    prefix = canonical_path(prefix, None)
    pflen = len(prefix)
    rtn_paths = {}
    rx_stripslash = re.compile(r'/.*')
    for row in db.execute("SELECT virtual_path FROM file_tree WHERE virtual_path >= ? AND virtual_path < ?", (prefix, prefix_upper(prefix))):
        path = row[0]
        path = path[:pflen] + rx_stripslash.sub('/', path[pflen:])
        rtn_paths[path] = True

    return list(rtn_paths)

def complete_disk(prefix, parsed_args, **kwargs):
    db = open_db(parsed_args, expand=True)
    if '/' in prefix:
        return []

    rtn = []
    like_prefix = escape_like(prefix) + '%'
    for row in db.execute("SELECT name FROM disk WHERE name NOTNULL AND name LIKE ? ESCAPE '\\'", (like_prefix,)):
        rtn.append(row[0])

    return rtn

##########################################################################################
# Utilities
##########################################################################################

def open_db(args, expand=False):
    if args.db and expand:
        args.db = args.db.expanduser()
    db = BackupDB(args.db, args.noaction, args.verbose)
    db.nocopydb = args.nocopy
    db.explain = args.explain
    db.connect()
    return db

##########################################################################################
# Common arguments
##########################################################################################

arg_disk = arg('disk', metavar='NAME', completer=complete_disk, help='Name, UUID, or path to disk data files')
arg_update = arg('-u', '--update', action='store_true', help='Perform an update before copying')
arg_nocopy = arg('--nocopy', action='store_true', help='Do not copy database')
arg_nohelper = arg('--nohelper', action='store_true', help='Do not use hash_helper module')
arg_sync = arg('--sync', action='store_true', help='Sync files to disk after copy')
arg_ignore_lock = arg('--ignore-lock', action='store_true', help='Scan locked directories')

@command('info', help='Report usage')
@arg('--no-saturated', action='store_true', help='Exclude the size of saturated objects from individual disk counts')
def cmd_report(db:BackupDB, parser, args):
    from .report import Reporter
    Reporter(db).print_report(exclude_saturated=args.no_saturated)

@command('ls', help='List files in database')
@arg('filter', metavar='PATTERN', nargs='?', completer=complete_virtual_path, help='Limit view to files that match the given pattern')
@arg('-d', '--disk', metavar='NAME', completer=complete_disk, help='Limit view to files on the given disk')
def cmd_list(db:BackupDB, parser, args):
    from .report import Reporter
    if args.disk:
        db.set_backup_disk(args.disk)
    Reporter(db).list_files(args.filter)

@command('tree', help='Show tree of files')
@arg('-m', '--mincopies', metavar='N', type=int, help='Only show files that have at least N copies')
@arg('-x', '--maxcopies', metavar='N', type=int, help='Only show files that have at most N copies')
@arg('-c', '--copies', metavar='N', type=int, help='Only show files that have exactly N copies')
def cmd_tree(db:BackupDB, parser, args):
    from .report import Reporter
    if args.copies is not None:
        args.mincopies = args.maxcopies = args.copies
    root = Reporter(db).get_tree(mincopies=args.mincopies, maxcopies=args.maxcopies)
    def dumpnode(level, node):
        print('%02d %5d %18s %s %2s %s %s' % (level, node.total_files, addcomma(node.total_size), ' '.join('%4d/%-8s' % (fcnt, prettysize(size)) for fcnt, size in zip(node.copy_files, node.copy_size)), '' if node.copies is None else node.copies, '   ' * level, node.name))
        for cnode in sorted(list(node.children.values()), key=lambda c:-c.total_size):
            dumpnode(level + 1, cnode)
    dumpnode(0, root)

@command('ncdu', help='Show size of backup set using `ncdu`')
@arg('-o', '--output', type=Path, metavar='FILE', help='Write output to file (readable by `ncdu -f`)')
@arg('-m', '--mincopies', metavar='N', type=int, help='Only show files that have at least N copies')
@arg('-x', '--maxcopies', metavar='N', type=int, help='Only show files that have at most N copies')
@arg('-c', '--copies', metavar='N', type=int, help='Only show files that have exactly N copies')
def cmd_ncdu(db:BackupDB, parser, args):
    from .report import Reporter
    if args.copies is not None:
        args.mincopies = args.maxcopies = args.copies
    data = Reporter(db).make_ncdu(mincopies=args.mincopies, maxcopies=args.maxcopies)
    if args.output:
        with args.output.open('w') as fp:
            json.dump(data, fp, indent=True)
    else:
        subprocess.run(['ncdu', '-f', '-'], encoding='utf8', input=json.dumps(data))


##########################################################################################
# Update
##########################################################################################

@command('update', help='Update the database view of the source files')
@arg_ignore_lock
@arg_nohelper
def cmd_update(db:BackupDB, parser, args):
    from .update import Updater
    from .report import Reporter
    Updater(db).update_source(args.ignore_lock)
    log.info('source updated.')
    Reporter(db).print_report()

##########################################################################################
# Backup
##########################################################################################

@command('backup', help='Back up files to a disk')
@arg_disk
@arg('--slack', action='store', help='Extra temporary space on target')
@arg('--limit', action='store', help='Stop after copying a specific amount of data')
@arg('--maxcopies', action='store', metavar='N', type=int, help="Don't make new copies of objects that already have at least N copies")
@arg('--noflush', action='store_true', help='Do not delete redundant copies to make room for new files')
@arg('--simulate', action='store_true', help='Do not actually modify target')
@arg_sync
@arg_update
@arg_ignore_lock
@arg_nohelper
def cmd_backup(db:BackupDB, parser, args):
    from .backup import Backup
    from .report import Reporter
    db.set_backup_disk(args.disk)
    if args.update:
        from .update import Updater
        Updater(db).update_source(args.ignore_lock)
        log.info('source updated.')

    limit = None
    if args.limit is not None:
        limit = parsesize(args.limit)

    pre_levels = NexusLevelDict(db.load_nexus())
    levels = Backup(db).backup_files(
        simulate=args.simulate,
        noflush=args.noflush,
        limit_bytes=limit,
        limit_copies=args.maxcopies
    )
    log.info('Pre-backup state:')
    reporter = Reporter(db)
    reporter.print_report(pre_levels, indent='    ')
    log.info('')
    log.info('Post-backup state:')
    reporter.print_report(levels, indent='    ')
    if args.simulate:
        log.info(f'simulated update to {db.current_disk.name} complete.')
    else:
        log.info(f'destination {db.current_disk.name} updated.')


##########################################################################################
# Restore
##########################################################################################

@command('restore', help='Restore files from backup')
@arg('src', nargs='?', metavar='DISK', completer=complete_disk, help='Disk or path to restore from')
@arg('dest', nargs='?', type=Path, metavar='PATH', help='Destination path to copy restored files')
@arg('-l', '--link', action='store_true', help='Make a hard link of the files instead of copying')
@arg('-f', '--filter', metavar='PATTERN', completer=complete_virtual_path, help='Restore only files that match PATTERN')
@arg('-e', '--existing', action='append', default=[], help='Ignore files that are present relative to this folder (can be specified multiple times)')
@arg('--minset', action='store_true', help="Deterimine the minimum set of disks necessary to restore the files")
def cmd_restore(db:BackupDB, parser, args):
    from .restore import Restore
    restore = Restore(db, args.dest)
    if args.minset:
        restore.restore_set(args.filter, args.existing)
        return

    if args.src is None or args.dest is None:
        parser.print_help()
        return

    db.set_backup_disk(args.src)

    if args.link:
        restore.restore_link(args.filter, args.existing)
    else:
        restore.restore_copy(args.filter, args.existing)

##########################################################################################
# Verify
##########################################################################################

@command('verify', help="Verify the integrity of the files on a backup disk. Objects that "
         "fail verification are moved to a directory called 'bad-objects' for analysis.")
@arg_disk
@arg('-e', '--errors', metavar=Path, default=None, help='Write tab-separated errors to a file descriptor (e.g. @3) or a file')
@arg('-s', '--start', default='', help="First few characters of last hash, for resuming an interrupted verification")
@arg('-c', '--check', dest='move', default=True, action='store_false', help="Only report bad objects, don't move them")
@arg('-d', '--delete', action='store_true', help="Delete bad objects instead of moving them")
def cmd_verify(db:BackupDB, parser, args):
    from .verify import Verifier
    db.set_backup_disk(args.disk)
    vf = Verifier(db)
    if args.errors:
        if args.errors.startswith('@'):
            with os.fdopen(int(args.errors[1:]), 'w', encoding='utf8') as fp:
                vf.verify(error_fp=fp, minhash=args.start, move_bad=args.move, del_bad=args.delete)
        else:
            with open(args.errors, 'w', encoding='utf8') as fp:
                vf.verify(error_fp=fp, minhash=args.start, move_bad=args.move, del_bad=args.delete)
    else:
        vf.verify(minhash=args.start, move_bad=args.move, del_bad=args.delete)

##########################################################################################
# Source
##########################################################################################

@command('source', help='Manage backup sources')
def list_sources(db:BackupDB, parser, args):
    if not db.path_map:
        print('No sources defined')
        return

    vheader = 'Virtual path'
    pheader = 'Physical path'
    vpath_len = max(len(vheader), max(len(vpath) for vpath in db.path_map))
    ppath_len = max(len(pheader), max(len(str(ppath)) for ppath in db.path_map.values()))
    print(f'{vheader.ljust(vpath_len)} {pheader}')
    print(f'{"-" * vpath_len} {"-" * ppath_len}')
    for vpath, ppath in db.path_map.items():
        print(f'{vpath.ljust(vpath_len)} {ppath}')


@command('source', 'map', help='Map a virtual path to a physical path')
@arg('vpath', metavar='VPATH', completer=complete_virtual_path, help='Virtual path in backup set')
@arg('ppath', metavar='PATH', type=Path, help='Physical path where files are located')
def source_map(db:BackupDB, parser, args):
    vpath = canonical_path(args.vpath, True)
    ppath = args.ppath
    if not ppath.is_absolute():
        ppath = ppath.resolve()

    db.map_source(vpath, str(ppath))
    print(f'Set {vpath} -> {ppath}')

@command('source', 'unmap', aliases=['del'], help='Delete a virtual path mapping')
@arg('vpath', metavar='VPATH', completer=complete_virtual_path, help='Virtual path in backup set')
def del_source(db:BackupDB, parser, args):
    vpath = canonical_path(args.vpath, True)
    if db.unmap_source(vpath):
        print(f'Deleted path {vpath}')
    else:
        print(f'Virtual path {vpath} not found')

@command('source', 'lock', help='Lock source paths (prevent scanning, assume unchanged)')
@arg('vpath', nargs='*', metavar='VPATH', completer=complete_virtual_path, help='Virtual path in backup set')
def lock_source(db:BackupDB, parser, args, lock=True):
    if not args.vpath:
        for vpath, config in db.execute('SELECT virtual_path, config FROM path_config'):
            if config and json.loads(config).get('lock'):
                print(vpath)

    for vpath, prev_config, new_config in db.set_path_config(args.vpath, {'lock': lock}):
        vpath = canonical_path(vpath, True)
        was_locked = bool(prev_config.get('lock'))
        if was_locked:
            print(f'{vpath} already locked' if lock else f'Unlocked: {vpath}')
        else:
            print(f'Locked: {vpath}' if lock else f'{vpath} not locked')

@command('source', 'unlock', help='Unlock source paths')
@arg('vpath', nargs='+', metavar='VPATH', completer=complete_virtual_path, help='Virtual path in backup set')
def unlock_source(db:BackupDB, parser, args):
    return lock_source(db, parser, args, False)

@command('source', 'set', help='Configure source paths')
@arg('vpath', nargs='+', metavar='VPATH', completer=complete_virtual_path, help='Virtual path in backup set')
@arg('-j', '--json', metavar='JSON', help='Specify updates in JSON format. Other options will override fields from this.')
@arg('-l', '--lock', action='store_true', help='Lock the specified paths')
@arg('-u', '--unlock', action='store_true', help='Unlock the specified paths')
@arg('-i', '--ignore', metavar='PATTERNS', action='append', default=None,
     help='Filename or patterns to ignore. Prefix with `!` to negate the ignore '
     '(include even if excluded by a later rule). The first pattern that matches '
     'determines the action, so include rules should be specified before ignore rules')
@arg('-a', '--append', action='store_true', help='Append new rules instead of replacing existing rules')
@arg('-p', '--priority', type=int, help='Set the default priority for the given paths (use 0 to clear)')
@arg('-m', '--maxcopies', type=int, help='Set the default priority for the given paths (use 0 to clear)')
@arg('--hide', action='store_true', help='Mark the specified paths as hidden')
@arg('--unhide', action='store_true', help='Unhide the specified paths')
@arg('--follow', action='store_true', help='Follow symbolic links in the directory')
@arg('--nofollow', action='store_true', help='Do not follow symbolic links in the directory')
def set_source(db:BackupDB, parser, args):
    updates = json.loads(args.json) if args.json else {}
    if args.lock:
        updates['lock'] = True
    if args.unlock:
        updates['lock'] = False
    if args.hide:
        updates['hide'] = True
    if args.unhide:
        updates['hide'] = None
    if args.follow:
        updates['follow_symlinks'] = True
    if args.nofollow:
        updates['follow_symlinks'] = None

    if args.priority is not None:
        updates['priority'] = args.priority or None

    if args.maxcopies is not None:
        updates['maxcopies'] = args.maxcopies or None

    lst = args.ignore
    if lst is not None:
        update_list = []
        for val in lst:
            update_list.append(val.strip())
        updates['rules'] = update_list

    if not updates:
        for vpath in args.vpath:
            vpath = canonical_path(vpath, True)
            config_text = db.query_scalar('SELECT config FROM path_config WHERE virtual_path = ?', (vpath,))
            config = dict(DEFAULT_CONFIG)
            if config_text:
                config.update(json.loads(config_text))
            print(f'{vpath}: {json.dumps(config)}')
        return

    print(f'Applying the following configuration changes: {json.dumps(updates)}')
    for vpath, prev_config, new_config in db.set_path_config(args.vpath, updates, False, ('rules',) if args.append else ()):
        all_keys = prev_config.keys() | new_config.keys()
        changes = {}
        for key in sorted(all_keys):
            default = DEFAULT_CONFIG.get(key)
            prev_val = prev_config.get(key, default)
            new_val = new_config.get(key, default)
            if prev_val != new_val:
                changes[key] = prev_val, new_val
        if changes:
            print(f'{vpath}:')
            for key, (prev_val, new_val) in changes.items():
                print(f'   {key}: {prev_val} -> {new_val}')
            print()
        else:
            print(f'{vpath}: no changes')

@command('source', 'reset', help='Clear configuration for source paths')
@arg('vpath', nargs='+', metavar='VPATH', completer=complete_virtual_path, help='Virtual path in backup set')
def reset_source(db:BackupDB, parser, args):
    paths = [canonical_path(path, True) for path in args.vpath]
    db.set_path_config(paths, {}, True)

##########################################################################################
# Disk
##########################################################################################

@command('disk', help='Manage backup disks')
def cmd_disk(db:BackupDB, parser, args):
    parser.print_help()

@command('disk', 'list', help='List all disks')
def cmd_disk_list(db:BackupDB, parser, args):
    db.find_disk_data_paths()
    clridx = 1
    print(f'{"disk":<20} {"device":<20} data path')
    maxpath = max(len(str(disk.data_path or '')) for disk in db.disk_by_name.values())
    for name, disk in sorted(db.disk_by_name.items()):
        txt = Colorizer(fg='ccc' if (clridx & 1) else 'fff', bg='222' if (clridx & 1) else '333')
        txt.t(name, rpad=20).t(' ')
        txt.t(disk.device_name or "-", rpad=20).t(' ')
        txt.t(str(disk.data_path or "-"), rpad=maxpath)
        print(txt.get())
        clridx += 1

@command('disk', 'add', help='Add a backup disk')
@arg('name', metavar='NAME', help='Name of new disk')
@arg('path', metavar='PATH', type=Path, help='Path to data files')
@arg('-s', '--size', help='Set size of selected disk')
@arg('-p', '--path', metavar='PATH', help='Path to data files')
def cmd_disk_add(db:BackupDB, parser, args):
    args.path.mkdir(parents=True, exist_ok=True)
    path = args.path.resolve()
    disk = db.add_disk(args.name, path, parsesize(args.size))
    db.copy_database()
    print(f'Added disk {disk.name}:')
    print(f'  UUID: {disk.uuid}')
    print(f'  Nexus index: {disk.nexus_index}')
    print(f'  Size: {addcomma(disk.size)}')
    if disk.device_name:
        print(f'  Device (current): {disk.device_name}')
    if disk.mountpoint:
        print(f'  Mount point (current): {disk.mountpoint}')
    if disk.relative_path:
        print(f'  Relative path from mountpoint: {disk.relative_path}')

@command('disk', 'set', help='Set parameters for a backup disk')
@arg_disk
@arg('-s', '--size', help='Set size of selected disk')
@arg('-p', '--path', metavar='PATH', type=Path, help='Path to data files')
@arg('-r', '--relpath', help='Set path of data files relative to mount')
def cmd_disk_set(db:BackupDB, parser, args):
    db.set_backup_disk(args.disk)
    db.set_disk_params(size=parsesize(args.size), relpath=args.relpath, path=args.path)

@command('disk', 'rename', aliases=['mv'], help='Set parameters for a backup disk')
@arg_disk
@arg('newname', metavar='NAME', help='New name for disk')
def cmd_disk_rename(db:BackupDB, parser, args):
    db.set_backup_disk(args.disk)
    db.rename_disk(args.newname)

@command('disk', 'drop', help='Drop all files from a disk. Use when a disk has failed.')
@arg_disk
def disk_drop(db:BackupDB, parser, args):
    db.set_backup_disk(args.disk)
    db.drop_disk()

@command('disk', 'del', help='Delete a disk. The disk must not have any files (use `disk drop` first)')
@arg_disk
def disk_del(db:BackupDB, parser, args):
    db.set_backup_disk(args.disk)
    db.delete_disk()

@command('disk', 'refresh', help='Refresh database view of files on the selected disk.')
@arg_disk
def disk_refresh(db:BackupDB, parser, args):
    db.set_backup_disk(args.disk)
    db.refresh_disk()
    log.info('database refreshed.')

##########################################################################################
# Config
##########################################################################################

@command('config', help='Manage configuration')
def cmd_config(db:BackupDB, parser, args):
    parser.print_help()

@command('config', 'export', help='Export configuration to JSON file')
@arg('path', type=Path, help='File to export to, or "-" for standard output')
@arg('-p', '--path-prefix', completer=complete_virtual_path, help='Export path_config only for the given directory and subdirectories')
def export_config(db:BackupDB, parser, args):
    data = db.export_config(canonical_path(args.path_prefix, True))
    if str(args.path) == '-':
        print(json.dumps(data, indent=4))
    else:
        with args.path.open('w') as fp:
            json.dump(data, fp, indent=4)

@command('config', 'import', help='Import configuration from JSON file')
@arg('path', type=Path, help='File to import from, or "-" for standard output')
def import_config(db:BackupDB, parser, args):
    if str(args.path) == '-':
        data = json.load(sys.stdin)
    else:
        with args.path.open() as fp:
            data = json.load(fp)
    db.import_config(data)

@command('config', 'edit', help='Edit configuration with an external editor')
@arg('-e', '--editor', help='Editor command (defaults to $EDITOR environment variable)')
def edit_config(db:BackupDB, parser, args, keys=(), path_prefix=None):
    editor = os.getenv('EDITOR') or 'editor'
    if args.editor:
        editor = args.editor

    with tempfile.NamedTemporaryFile(prefix='distbackup-edit-', suffix='.json') as tmpf:
        path = Path(tmpf.name)
        data = db.export_config(path_prefix)
        if keys:
            data = {k: v for k, v in data.items() if k in keys}

        with path.open('w', encoding='utf8') as fp:
            json.dump(data, fp, indent=4)

        while True:
            print(f'Running editor: {editor}')
            try:
                subprocess.run([editor, tmpf.name], check=True)
                with path.open(encoding='utf8') as fp:
                    new_data = json.load(fp)
                db.import_config(new_data)
                break
            except Exception:
                traceback.print_exc(file=sys.stdout)
                print()
                print('Errors occurred while editing configuration.')
                while True:
                    choice = input('(c)ancel, (e)dit again, (r)evert edits? ').lower()
                    if choice == 'c':
                        return
                    elif choice == 'e':
                        break
                    elif choice == 'r':
                        with path.open('w', encoding='utf8') as fp:
                            json.dump(data, fp, indent=4)
                        break

@command('config', 'edit', 'map', help='Edit mapping configuration with an external editor')
@arg('-e', '--editor', help='Editor command (defaults to $EDITOR environment variable)')
def edit_config_map(db:BackupDB, parser, args):
    edit_config(db, parser, args, ('path_map',))

@command('config', 'edit', 'path', help='Edit path configuration with an external editor')
@arg('vpath', nargs='?', metavar='VPATH', completer=complete_virtual_path, help='Virtual paths to edit')
@arg('-e', '--editor', help='Editor command (defaults to $EDITOR environment variable)')
def edit_config_path(db:BackupDB, parser, args):
    edit_config(db, parser, args, ('path_config', 'path_prefix'), canonical_path(args.vpath, True))

@command('config', 'edit', 'disks', help='Edit disk configuration with an external editor')
@arg('-e', '--editor', help='Editor command (defaults to $EDITOR environment variable)')
def edit_config_disk(db:BackupDB, parser, args):
    edit_config(db, parser, args, ('disks',))

##########################################################################################
# Debug
##########################################################################################

@command('debug', help='Debugging commands')
def cmd_debug(db:BackupDB, parser, args):
    parser.print_help()

@command('debug', 'hash', help='Hash a file')
@arg('path', type=Path, help='File to hash')
def cmd_debug_hash(db:BackupDB, parser, args):
    from .sourcefile import SourceFile
    srcf = SourceFile(args.path)
    print(f'hashing {args.path}')
    srcf.copy()
    print(f'hash = {srcf.hash}')

@command('debug', 'info', help='Show debug info about a path')
@arg('vpath', completer=complete_virtual_path, help='Virtual path to file')
def cmd_debug_info(db:BackupDB, parser, args):
    sql = '''
      SELECT
        ft.hash, ft.size, ft.last_modified, ft.ino, ft.metadata,
        ob.blocksize, ob.nexus, ob.refs, ob.copies
      FROM file_tree ft
      LEFT JOIN object ob ON ob.hash = ft.hash
      WHERE ft.virtual_path = ?
    '''

    args.vpath = canonical_path(args.vpath)
    row = db.query_one(sql, (args.vpath,))
    if not row:
        print(f'{args.vpath}: not found.')
        return

    hash, size, lastmod, ino, meta, blocksize, nexus, refs, copies = row
    mtimetxt = time.strftime('%Y-%m-%d %H:%M:%S%z', time.localtime(restore_mtime(lastmod)))

    print(f'{args.vpath}:')
    print(f'  Hash: {hash}')
    print(f'  Size: {addcomma(size)} ({addcomma(round_blocks(size))})')
    print(f'  Modified: {lastmod} ({mtimetxt})')
    print(f'  Inode: {ino}')
    if refs is not None:
        print(f'  Refs: {refs}')
    if nexus is not None:
        print(f'Nexus: {copies}, {nexus!r} ({" ".join(db.nexus_disks(nexus))})')
    if refs > 1:
        print('Identical files:')
        for nvpath, lastmod in db.execute('SELECT path, last_modified FROM object WHERE hash = ? AND path <> ?', (hash, args.vpath)):
            mtimetxt = time.strftime('%Y-%m-%d %H:%M:%S%z', time.localtime(restore_mtime(lastmod)))
            print(f'   ({mtimetxt}) {nvpath}')
