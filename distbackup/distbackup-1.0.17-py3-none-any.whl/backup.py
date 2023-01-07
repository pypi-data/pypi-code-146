import os
import time
import logging

from collections import deque, Counter

from ktpanda.textcolor import Colorizer

from .errors import ArgumentError, IncompleteUpdateError
from .utils import (CacheDict, addcomma, check_dir, int_mtime, nexus_with_disk, nexus_without_disk,
                    prettysize, prettysize_clr, restore_mtime, try_unlink, disk_in_nexus)
from .nexus import Nexus, NexusLevel, NexusLevelDict
from .objects import ObjectCopyEntry, ObjectGroup
from .database import BackupDB
from .sourcefile import SourceFile

log = logging.getLogger(__name__)

class Backup:
    def __init__(self, db:BackupDB, sync=False):
        self.db:BackupDB = db
        self.temp_index:int = 1
        self.sync:bool = sync

    def tempname(self):
        idx = self.temp_index
        self.temp_index = idx + 1
        path = self.db.current_disk.data_path / f'distbackup-tmp.{os.getpid()}.{idx}'
        return path

    def print_delete(self, del_obj):
        log.info(f"delete ({prettysize(del_obj.size)}) ({del_obj.nexusto.disks}) {del_obj.path}")

    def copy_object(self, copy_obj, copyremain=None):
        '''Copy an object to the current backup disk.'''
        srcf = None
        vpath = None
        with self.db.execute('SELECT virtual_path, last_modified FROM file_tree WHERE hash = ?', (copy_obj.hash,)) as curs:
            for path, lastmod in curs:
                fpath = self.db.get_file_path(path)
                if fpath is None:
                    log.warning(f"Could not find real file for virtual path {path}")
                    continue

                try:
                    st = fpath.stat()
                    srcf = SourceFile(fpath, st)

                    if int_mtime(st.st_mtime) != lastmod:
                        raise OSError()

                    vpath = path
                    break
                except OSError as e:
                    log.warning(f"source modified ({path}): {e}")

        if not vpath:
            return False

        txt = Colorizer().t(f'copy {vpath} (').t(prettysize_clr(copy_obj.size)).t(f') ({copy_obj.nexusfrom.disks})')

        if copyremain is not None:
            txt.t(' limit ').t(prettysize_clr(copyremain))

        log.info(txt.get())

        try:
            dstfn = self.tempname()
            srcf.setdest(dstfn)
            srcf.copy(self.db.check_run_deferred, self.sync)
            if srcf.hash != copy_obj.hash:
                log.info(f'WARNING: data for {vpath} does not match hash: expected {copy_obj.hash}, got {srcf.hash}')
                # Set the file's hash to the actual value. It will get picked up on the next update/copy.
                self.db.defer(self.db.set_file_hash, vpath, srcf.hash)
                return False
            destname = self.db.current_disk.hashpath(copy_obj.hash)
            check_dir(destname)
            dstfn.replace(destname)

            self.db.defer(self.db.set_object_on_disk, copy_obj.hash, self.db.current_disk.nexus_index, True)

            dstfn = None

        finally:
            if dstfn:
                try_unlink(dstfn)

        return True

    def delete_objects(self, to_delete, printf=None):
        for del_obj in to_delete:
            if printf:
                printf(del_obj)
            self.db.check_run_deferred()
            if try_unlink(self.db.current_disk.hashpath(del_obj.hash)):
                self.db.defer(self.db.set_object_on_disk, del_obj.hash, self.db.current_disk.nexus_index, False)
            else:
                log.info(f'warning: could not delete hash {hash}')
                continue

    def backup_files(self, simulate=False, noflush=False, limit_bytes=None, limit_copies=None):
        try:
            return self._backup_files(simulate, noflush, limit_bytes, limit_copies)
        finally:
            self.db.check_run_deferred(True)

            # Backup may have created new nexus objects from trigger.
            self.db.update_nexus_disk_text(only_new=True)

    def _backup_files(self, simulate=False, noflush=False, limit_bytes=None, limit_copies=None):
        self.db.require_disk()
        if not self.db.current_disk.data_path and not simulate:
            raise ArgumentError('updating target requires a backup destination or --simulate')

        missing_hash_count = self.db.query_scalar("SELECT count(*) FROM file_tree WHERE hash = ''")
        if missing_hash_count:
            raise IncompleteUpdateError(f'Source update incomplete: {missing_hash_count} files are missing hashes')

        if not simulate:
            self.db.cleanrefs()
            self.db.copy_database(self.db.current_disk.data_path)
            self.db.current_disk.migrate_data()

        # nexus_dict: Maps rows from the `nexus` table to `Nexus` objects
        nexus_dict: CacheDict[str, Nexus] = CacheDict(self.db.create_empty_nexus)
        nexus_dict.update(self.db.load_nexus())

        copyremain = limit_bytes
        self.db.update_free_space()

        total_copied = Counter()
        total_deleted = Counter()

        nexus_index = self.db.current_disk.nexus_index

        # objects_off_disk: Contains all objects not present on the disk. We will pick as
        # many objects from this container to copy to the disk. It starts out as a
        # CacheDict so we can group objects together by priority. Later, we convert it
        # into a list of groups sorted by priority.
        objects_off_disk = CacheDict(ObjectGroup)

        # objects_on_disk: Contains all objects on the disk that we can delete.
        objects_on_disk = CacheDict(ObjectGroup)

        available_space = self.db.current_disk.size - self.db.current_disk.used_space

        to_delete = []

        # Search through all objects that have references from file_tree.
        with self.db.execute('SELECT hash, size, blocksize, size_order, copies, refs, nexus, priority, maxcopies, last_path, last_modtime FROM object') as curs:
            for hash, size, blocksize, size_order, copies, refs, current_nexus, priority, maxcopies, last_path, last_modtime in curs:
                # If the current disk is in the object's nexus, that means the object is
                # currently on the disk, and we can delete it to make room for higher priority
                # objects,
                entry = ObjectCopyEntry(
                    hash=hash, size=size, blocksize=blocksize, size_order=size_order, refs=refs, groupkey=None,
                    nexusfrom=nexus_dict[current_nexus], maxcopies=maxcopies, path=last_path, modtime=last_modtime
                )

                if disk_in_nexus(current_nexus, nexus_index):
                    entry.groupkey = copies, -priority
                    entry.nexusto = nexus_dict[nexus_without_disk(current_nexus, nexus_index)]
                    # Immediately delete any objects with no more references or have too many copies
                    if (maxcopies is not None and copies > maxcopies) or refs == 0:
                        to_delete.append(entry)
                        continue

                    # Never delete files that have only one copy, regardless of priority.
                    if copies <= 1:
                        continue

                    objects_on_disk[entry.groupkey].add_entry(entry)
                else:
                    entry.groupkey = copies + 1, -priority
                    entry.nexusto = nexus_dict[nexus_with_disk(current_nexus, nexus_index)]

                    # Never copy files that already have the maximum number of copies, and
                    # don't copy objects that have no references.
                    if (maxcopies is not None and copies >= maxcopies) or refs == 0:
                        continue

                    # Don't copy files that already have the maximum number of copies for
                    # this session.
                    if limit_copies is not None and copies >= limit_copies:
                        continue

                    objects_off_disk[entry.groupkey].add_entry(entry)

        # levels: Maps `level` -> NexusLevel, which groups all Nexus objects by count of
        # disks in the set.
        levels: NexusLevelDict[int, NexusLevel] = NexusLevelDict(nexus_dict)
        nexus_dict.clear()

        # Delete all the dead and excess objects
        for del_obj in to_delete:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(restore_mtime(del_obj.modtime)))
            log.info(f"delete {del_obj.hash} ({timestamp}): {del_obj.path}")

            # Entries with refs == 0 are already excluded from size counts
            if del_obj.refs > 0:
                levels.move_object(del_obj.nexusfrom, del_obj.nexusto, del_obj.blocksize, del_obj.maxcopies)
                available_space += del_obj.blocksize
                total_deleted[del_obj.nexusfrom.level] += del_obj.blocksize

        if not simulate:
            self.delete_objects(to_delete)

        # Sort the groups so that the first element is the one with the lowest number of
        # copies and highest proiority.
        objects_off_disk = deque(sorted(objects_off_disk.values()))
        objects_on_disk = deque(sorted(objects_on_disk.values()))

        # All the objects that we could not copy, either because they were either
        # modified, moved, or deleted since the last update.
        unable_to_copy = []


        # Calculate the initial imbalance value for each level.
        for grp in levels.values():
            grp.update_imbalance()

        if self.db.verbose:
            log.info(f'Imbalance before ({len(levels)}):')
            for level, grp in sorted(levels.items()):
                log.info(f'  Level {level:2}: level={len(grp.members):3d} size={addcomma(grp.totalsize):>20} imbalance={addcomma(format(grp.imbalance, ".2f")):>24}')

        if self.db.verbose >= 2:
            for grp in objects_on_disk:
                log.info(f'reclaimable space for {grp.groupkey} = {addcomma(grp.totalsize)}')

        # Main backup loop
        while True:
            self.db.check_run_deferred()
            try:
                # Grab the highest priority group from objects_off_disk, removing any that are empty.
                while len((src_group := objects_off_disk[0]).objects) == 0:
                    objects_off_disk.popleft()
            except IndexError:
                # IndexError means there are no more groups and therefore no more objects to copy.
                break

            # Remove any groups from the delete set whose priority is greater than or
            # equal to the priority of the group we're copying from. An object can
            # only replace an object of a lower priority.
            try:
                while objects_on_disk[0].groupkey <= src_group.groupkey:
                    objects_on_disk.popleft()

                while len(objects_on_disk[-1].objects) == 0:
                    objects_on_disk.pop()
            except IndexError:
                pass

            # Calculate the maximum size of an object we can copy.
            if noflush:
                reclaimable_space = 0
            else:
                reclaimable_space = sum(grp.totalsize for grp in objects_on_disk)

            total_available = available_space + reclaimable_space

            # If we have a copy limit, cap `total_available`
            if copyremain is not None and total_available > copyremain:
                total_available = copyremain

            # Calculate the `imbalance_change` value for all the objects in this group if
            # it has not been calculated before.
            if not src_group.sorted:
                src_group.sort(levels)

            # Grab a random object to copy.
            try:
                copy_obj = src_group.pop_entry(total_available)
            except IndexError:
                # IndexError means no more items from this group could be copied. Move on
                # to the next group.
                continue

            assert not disk_in_nexus(copy_obj.nexusfrom.nexusid, nexus_index), f'copy_obj already on disk {copy_obj}'

            if self.db.verbose >= 2:
                log.info(f'trying to copy {copy_obj.path} ({addcomma(copy_obj.size)}), avail_space={addcomma(available_space)}')

            # We may still fail to copy, but for now, pretend we can. If we don't copy,
            # these changes will be rolled back. This is only for the current process, no
            # changes are made to the database unless files are actually copied or
            # deleted.
            if copyremain is not None:
                copyremain -= copy_obj.blocksize
            available_space -= copy_obj.blocksize
            levels.move_object(copy_obj.nexusfrom, copy_obj.nexusto, copy_obj.blocksize, copy_obj.maxcopies)

            to_delete = []

            # Initialize the group we're looking for to the end of objects_on_disk. We
            # want to avoid deleting empty sets because we may revert,
            del_group_index = len(objects_on_disk) - 1
            if available_space < 0:
                if self.db.verbose >= 2:
                    for grp in objects_on_disk:
                        log.info(f'reclaimable space for {grp.groupkey} = {addcomma(grp.totalsize)}')
                    log.info(f'total reclaimable space = {addcomma(reclaimable_space)}')

                if reclaimable_space < -available_space:
                    continue

            while available_space < 0 and not noflush:
                del_group = None

                while del_group_index >= 0 and len((del_group := objects_on_disk[del_group_index]).objects) == 0:
                    # Find the lowest priority group, skipping ones that are empty.
                    del_group_index -= 1

                if del_group is None or del_group_index < 0:
                    # No more files that can be deleted.
                    break

                # Calculate the `imbalance_change` value for all the objects in this group
                # if it has not been calculated before.
                if not del_group.sorted:
                    del_group.sort(levels)

                # Grab a random object to delete.
                del_obj = del_group.pop_entry()

                assert disk_in_nexus(del_obj.nexusfrom.nexusid, nexus_index), f'del_obj not on disk {del_obj}'

                to_delete.append(del_obj)
                levels.move_object(del_obj.nexusfrom, del_obj.nexusto, del_obj.blocksize, del_obj.maxcopies)
                available_space += del_obj.blocksize
                if self.db.verbose >= 2:
                    log.info(f'del {del_obj.path} ({addcomma(del_obj.size)}), avail_space={addcomma(available_space)}')

            copied = False
            # If we have enough space, then copy the object.
            if available_space >= 0:
                for del_obj in to_delete:
                    total_deleted[del_obj.nexusfrom.level] += del_obj.blocksize

                if simulate:
                    for obj in to_delete:
                        log.info(f'would delete {obj.path} {prettysize(obj.size)} ({obj.nexusfrom.disks})')
                    log.info(f'would copy {copy_obj.path} {prettysize(copy_obj.size)} ({copy_obj.nexusfrom.disks})')
                    copied = True
                else:
                    self.delete_objects(to_delete, self.print_delete)
                    if self.copy_object(copy_obj, copyremain):
                        copied = True
                    else:
                        unable_to_copy.append(copy_obj)
            else:
                if self.db.verbose >= 2:
                    log.info(f'Not enough space to copy {obj.path}')

            # If we didn't actually copy the file, roll back the changes that we made.
            if copied:
                total_copied[copy_obj.nexusto.level] += copy_obj.blocksize
                for grp in objects_on_disk:
                    grp.commit()
            else:
                if copyremain is not None:
                    copyremain += copy_obj.blocksize
                available_space += copy_obj.blocksize
                levels.move_object(copy_obj.nexusto, copy_obj.nexusfrom, copy_obj.blocksize, copy_obj.maxcopies)
                for grp in objects_on_disk:
                    if self.db.verbose >= 2:
                        if grp.saved_objects is not None:
                            log.info(f'roll back delete group {grp.groupkey} {len(grp.objects)} -> {len(grp.saved_objects)}')
                    grp.rollback()

        log.info(f'Copied {prettysize(sum(total_copied.values()))}:')
        for level, bytes in sorted(total_copied.items()):
            log.info(f'  Level {level - 1} -> {level}: {prettysize(bytes)}')

        log.info(f'Deleted {prettysize(sum(total_deleted.values()))}:')
        for level, bytes in sorted(total_deleted.items()):
            log.info(f'  Level {level} -> {level - 1}: {prettysize(bytes)}')

        if unable_to_copy:
            log.info('some files could not be copied (recommend --update)')

        if not simulate:
            self.db.cleanrefs()
            self.db.copy_database()
        return levels
