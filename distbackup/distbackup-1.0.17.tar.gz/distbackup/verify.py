import logging

from .database import BackupDB
from .sourcefile import SourceFile
from .utils import hash_relpath

log = logging.getLogger(__name__)

class Verifier:
    def __init__(self, db:BackupDB):
        self.db:BackupDB = db

    def verify(self, error_fp=None, minhash='', move_bad=False, del_bad=False):
        self.db.require_disk()
        self.db.current_disk.migrate_data()
        vlog = logging.getLogger(f'verify-{self.db.current_disk.name}')
        bad_object_path = self.db.current_disk.data_path / 'bad-objects'
        bad_objects = []
        try:
            for hash, fpath, stat in self.db.current_disk.walk_data():
                if hash <= minhash:
                    continue
                row = self.db.query_one('SELECT last_modified, size, virtual_path, ino FROM file_tree WHERE hash = ? LIMIT 1', (hash,))
                if not row:
                    vlog.warning(f'{hash} deleted or not in database')
                    continue

                lastmod, size, path, ino = row
                try:
                    srcf = SourceFile(fpath, fpath.lstat())
                except OSError as e:
                    vlog.warning(f'cannot read {fpath} ({e})')
                    continue

                err_desc = None
                if srcf.size != size:
                    vlog.error(f'{path}: size mismatch ({srcf.size} != {size})')
                    err_desc = f'size={srcf.size}'
                else:
                    vlog.info(f'check {path} ({hash})')
                    srcf.copy()
                    if srcf.hash != hash:
                        vlog.error(f'{path}: hash ({srcf.hash} != {hash})')
                        err_desc = f'hash={srcf.hash}'

                if err_desc:
                    bad_objects.append((path, hash))
                    if error_fp:
                        error_fp.write(f'{self.db.current_disk.name}\t{hash_relpath(hash)}\t{size}\t{path}\t{err_desc}\n')
                        error_fp.flush()

                    if move_bad or del_bad:
                        self.db.set_object_on_disk(hash, self.db.current_disk.nexus_index, False)

                    if move_bad:
                        bad_object_path.mkdir(parents=True, exist_ok=True)
                        fpath.replace(bad_object_path / hash)
                    elif del_bad:
                        fpath.unlink()
        except KeyboardInterrupt:
            pass

        if bad_objects:
            vlog.info('')
            vlog.info('Bad files:')
            for path, hash in bad_objects:
                vlog.info(f'  {hash} {path}')
        else:
            vlog.info('No bad files.')
