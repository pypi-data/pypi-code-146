import sys
import re
import time
import os
import json
import logging

from hashlib import sha256

try:
    import hashcopy
except ImportError:
    hashcopy = None

from .constants import META_SUFFIX
from .utils import round_blocks, progress
from .errors import FileChanged

log = logging.getLogger(__name__)

class SourceFile:
    ENABLE_HASHCOPY = True

    def __init__(self, path, stat=None):
        self.path = path
        self.size = 0
        self.blocksize = 0
        self.mode = 0
        self.mtime = 0
        self.inode = 0

        self.fp = None
        self.dest = None
        self.destfp = None
        self.hash = None
        self.priority = None
        self.maxcopies = None

        self.metadata = {}

        if stat is None:
            stat = path.lstat()
        self.setstat(stat)

    def read_meta(self):
        try:
            metapath = self.path.with_name(self.path.name + META_SUFFIX)
            with metapath.open() as fp:
                self.metadata = json.load(fp)

            hash = self.metadata.get('hash')
            if hash:
                if not (isinstance(hash, str) and re.match(r'^[0-9a-f]{64}$', hash, re.I)):
                    raise ValueError(f'Invalid hash: {hash}')
                self.hash = hash.lower()

            priority = self.metadata.get('priority')
            if priority is not None:
                if not (isinstance(priority, int) and priority >= 0):
                    raise ValueError(f'Invalid priority: {priority}')
                self.priority = priority

            maxcopies = self.metadata.get('maxcopies')
            if maxcopies is not None:
                if not (maxcopies == 'inf' or (isinstance(maxcopies, int) and maxcopies >= 1)):
                    raise ValueError(f'Invalid maxcopies: {maxcopies}')
                self.maxcopies = None if maxcopies == 'inf' else maxcopies
        except FileNotFoundError:
            pass
        except ValueError as e:
            print(f'WARNING: Metadata file {metapath} is corrupt: {e}', file=sys.stderr)


    def check_change(self):
        nst = self.path.lstat()
        if nst.st_mode != self.mode or nst.st_mtime != self.mtime or nst.st_size != self.size:
            self.setstat(nst)
            raise FileChanged()

    def _open(self):
        if self.fp is None:
            self.fp = self.path.open('rb')

    def reset(self):
        if self.fp is not None:
            self.fp.close()
            self.fp = None

    def setdest(self, dest):
        self._open()
        self.dest = dest
        self.destfp = dest.open('wb')

    def setstat(self, stat):
        self.size = stat.st_size
        self.blocksize = round_blocks(self.size)
        self.mode = stat.st_mode
        self.mtime = stat.st_mtime
        self.inode = stat.st_ino

    def copy(self, periodic=None, sync=False):
        self._open()
        ltime = time.time()
        pos = 0
        prog = False
        if hashcopy and SourceFile.ENABLE_HASHCOPY:
            hh = hashcopy.HashCopier(self.fp.fileno(), self.destfp.fileno() if self.destfp else -1)
        else:
            if SourceFile.ENABLE_HASHCOPY:
                log.warning('Hash accelerator is enabled but `hashcopy` module could not be imported')
                SourceFile.ENABLE_HASHCOPY = False
            hh = None
            sha = sha256()
        try:
            while True:
                if hh:
                    copylen = hh.update()
                else:
                    dat = self.fp.read(524288)
                    copylen = len(dat)
                    if self.destfp:
                        self.destfp.write(dat)

                if copylen == 0:
                    break

                pos += copylen
                ctime = time.time()
                if ctime >= ltime + 0.2:
                    if periodic:
                        periodic()
                    ltime = ctime
                    prog = True
                    pct = (pos * 100.0 / self.size)
                    progress(pct)

                # If we're using hash_helper, sync the destination after every
                # write. We're depending on readahead to fill the memory mapped buffer
                # while the sync is occurring.
                if hh:
                    if self.destfp and sync:
                        os.fsync(self.destfp.fileno())
                else:
                    sha.update(dat)

            self.reset()
            self.size = pos

            if self.destfp:
                if prog:
                    progress(100)
                if sync:
                    os.fsync(self.destfp.fileno())
                self.destfp.close()

            if hh:
                self.hash = hh.finalize().hex()
            else:
                self.hash = sha.hexdigest()

            return self.hash
        finally:
            if prog:
                progress(None)
