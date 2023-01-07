import sys
import re
import json
import subprocess
import logging
import shutil

from typing import Optional
from dataclasses import dataclass
from collections import defaultdict
from pathlib import Path

import psutil

from .constants import DISK_CONF_NAME, OBJECT_DIR_NAME, LEGACY_OBJECT_DIR_NAME
from .utils import canonical_uuid, hash_relpath, read_file, write_file

log = logging.getLogger(__name__)

RX_HEX = re.compile(r'^[0-9a-fA-F]+$')

def find_mountpoint(path, partition_by_mountpoint):
    path = path.resolve()
    cpath = path
    cstat = path.stat()
    while True:
        partition = partition_by_mountpoint.get(str(cpath))
        if partition:
            break
        ppath = cpath.parent
        pstat = ppath.stat()
        if cpath == ppath or cstat.st_dev != pstat.st_dev:
            break
        cpath = ppath
        cstat = pstat

    return cpath, str(path.relative_to(cpath)), shutil.disk_usage(path).total, partition

@dataclass
class Partition:
    device: str
    mountpoint: Path
    size: int = 0
    label: Optional[str] = None
    fstype: Optional[str] = None
    fsuuid: Optional[str] = None

    @classmethod
    def list(cls):
        rtn = []
        if sys.platform == 'linux':
            try:
                p = subprocess.run(
                    'lsblk --json -p -b -o name,size,label,uuid,mountpoint,fstype,fsavail,fssize --list'.split(),
                    encoding='ascii', stdout=subprocess.PIPE, check=True
                )
                jsdata = json.loads(p.stdout)
                for dev in jsdata['blockdevices']:
                    mountpoint = dev.get('mountpoint')
                    part = cls(
                        device=dev.get('name'),
                        mountpoint=Path(mountpoint) if mountpoint else None,
                        size=dev.get('fssize') or dev.get('size'),
                        label=dev.get('label'),
                        fstype=dev.get('fstype'),
                        fsuuid=dev.get('uuid'),
                    )
                    if part.mountpoint or part.fsuuid:
                        rtn.append(part)

                return rtn

            except (OSError, ValueError, KeyError) as e:
                log.warning(f'Unable to use `lsblk`: {e}', file=sys.stderr)

        for disk in psutil.disk_partitions():
            if not disk.mountpoint:
                continue

            rtn.append(cls(device=disk.device, mountpoint=Path(disk.mountpoint), fstype=disk.fstype))
        return rtn

@dataclass
class BackupDisk:
    uuid: str
    name: str
    nexus_index: int = 0
    relative_path: Optional[str] = None
    size: int = 0
    fstype: Optional[str] = None
    fsuuid: Optional[str] = None
    used_space: int = 0
    mountpoint: Optional[Path] = None
    data_path: Optional[Path] = None
    device_name: Optional[str] = None

    def write_config(self):
        jsdata = json.dumps({
            "uuid": self.uuid,
            "name": self.name
        }, indent=4)
        write_file(self.data_path / DISK_CONF_NAME, jsdata)

    @classmethod
    def read_config(cls, path):
        try:
            with (path / DISK_CONF_NAME).open('r') as fp:
                jsdata = json.load(fp)

            uuid = canonical_uuid(jsdata['uuid'])
            name = jsdata.get('name')
            return cls(uuid, name, data_path=path)

        except FileNotFoundError:
            # Legacy configuration
            uuid = read_file(path / '.distbackup.uuid')
            if not uuid:
                return None
            name = read_file(path / '.distbackup.name')
            rdisk = cls(uuid, name, data_path=path)
            rdisk.write_config()
            return cls(uuid, name, data_path=path)

        except (ValueError, OSError, KeyError):
            return None

    def set_from_path(self, path: Path):
        partitions = Partition.list()
        partition_by_mountpoint = {part.mountpoint: part for part in partitions if part.mountpoint}
        mountpt, relpath, totalsize, partition = find_mountpoint(path, partition_by_mountpoint)

        if not self.size:
            # Reserve 5% of the disk, or 10G, whichever is smaller
            reserve = min(10_000_000_000, totalsize // 20)
            self.size = (totalsize - reserve) & ~0xFFF

        if partition is not None:
            self.fstype = partition.fstype
            self.fsuuid = partition.fsuuid

        self.mountpoint = mountpt
        self.data_path = path
        self.relative_path = relpath

    def hashpath(self, hash):
        return self.data_path / hash_relpath(hash)

    def migrate_data(self):
        if not self.data_path:
            return

        object_path = self.data_path / OBJECT_DIR_NAME
        if not object_path.exists():
            legacy_path = self.data_path / LEGACY_OBJECT_DIR_NAME
            if legacy_path.exists():
                legacy_path.rename(object_path)
            else:
                object_path.mkdir(parents=True, exist_ok=True)

    def walk_data(self):
        base = self.data_path / OBJECT_DIR_NAME

        for subdir in sorted(base.iterdir()):
            if not RX_HEX.match(subdir.name):
                continue

            for hashf in sorted(subdir.iterdir()):
                hash = hashf.name
                if not RX_HEX.match(hash):
                    continue

                try:
                    stat = hashf.lstat()
                except OSError:
                    continue

                yield hash, hashf, stat

    @classmethod
    def find_disk_data_paths(cls, disks):
        disk_by_fsuuid = defaultdict(list)
        disk_by_relpath = defaultdict(dict)
        for disk in disks:
            if disk.relative_path and disk.data_path is None:
                if disk.fsuuid:
                    disk_by_fsuuid[disk.fsuuid].append(disk)
                else:
                    disk_by_relpath[disk.relative_path][disk.uuid] = disk

        for part in Partition.list():
            if not part.mountpoint:
                if part.fsuuid:
                    for disk in disk_by_fsuuid.get(part.fsuuid, ()):
                        disk.device_name = part.device
                continue

            if part.fsuuid:
                for disk in disk_by_fsuuid.get(part.fsuuid, ()):
                    rdisk = BackupDisk.read_config(part.mountpoint / disk.relative_path)
                    if rdisk:
                        if rdisk.uuid != disk.uuid:
                            log.warning(f'Disk on partition {part.fsuuid} ({rdisk.data_path}) does not match expected UUID!', file=sys.stderr)
                            log.warning(f'  Expected: {disk.name} {disk.uuid}')
                            log.warning(f'  Got     : {rdisk.name} {rdisk.uuid}')
                            continue

                        disk.mountpoint = part.mountpoint
                        disk.data_path = rdisk.data_path
                        disk.device_name = part.device
                        log.debug(f'Found path for {disk.name} using partition UUID: {disk.data_path}')

                        if disk.name != rdisk.name:
                            disk.write_config()

            for path, disk_map in disk_by_relpath.items():
                # If we've already found all disks for this path, don't try to read it
                if not disk_map:
                    continue

                if not any(disk for disk in disk_map.values() if (disk.fstype is None or part.fstype == disk.fstype)):
                    continue

                rdisk = BackupDisk.read_config(part.mountpoint / path)
                if rdisk:
                    disk = disk_map.pop(rdisk.uuid, None)
                    if disk is None:
                        continue

                    disk.mountpoint = part.mountpoint
                    disk.data_path = rdisk.data_path
                    disk.device_name = part.device
                    log.debug(f'Found path for {disk.name} by scanning: {disk.data_path}')

                    if disk.name != rdisk.name:
                        disk.write_config()
