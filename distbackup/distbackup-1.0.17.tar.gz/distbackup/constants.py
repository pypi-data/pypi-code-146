DBNAME = 'distbackup.sqlite'
META_SUFFIX = '.meta-inf'
DISK_CONF_NAME = 'distbackup-disk.json'
OBJECT_DIR_NAME = 'distbackup-objects'
LEGACY_OBJECT_DIR_NAME = '.distbackup.data'

DEFAULT_CONFIG = {
    'lock': False,
    'hide': False,
    'follow_symlinks': False,
    'include': [],
    'exclude': [],
}
