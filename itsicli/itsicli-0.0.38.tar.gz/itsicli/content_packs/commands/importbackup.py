# ${copyright}

import os

from pathlib import Path

from itsicli.setup_logging import logger, set_content_pack_id
from itsicli.content_packs.backup.workspace_import import BackupImporter
from itsicli.content_packs.commands.base import WorkspaceCommand
from itsicli.content_packs.files import ContentPackConfig


class ImportBackupCommand(WorkspaceCommand):

    HELP = 'import the content in a backup file'

    NAME = 'importbackup'

    class Args(object):
        BACKUP_FILE_PATH = 'backup_file_path'
        SKIP_KEY_MAPPING = 'skip_key_mapping'

    @classmethod
    def add_to_parser(cls, parser):
        subparser = parser.add_parser(cls.NAME, help=cls.HELP)
        subparser.add_argument('{}'.format(cls.Args.BACKUP_FILE_PATH), help='ITSI backup file path')
        subparser.add_argument('--{}'.format(cls.Args.SKIP_KEY_MAPPING), '-s',
                               action='store_true',
                               help='Skip key mapping')
        return subparser

    def run(self, args):
        backup_file = getattr(args, self.Args.BACKUP_FILE_PATH)

        #Setting the content pack id in the global dictionary so that it is added in the logger
        content_pack_config = ContentPackConfig(Path.cwd())
        set_content_pack_id(content_pack_config.get_cp_id())

        logger.info("Backup file path is set to '{}'".format(backup_file))

        skip_key_mapping = getattr(args, self.Args.SKIP_KEY_MAPPING)
        self.import_from_backup_file(self.config.id, backup_file, skip_key_mapping=skip_key_mapping)

        logger.info('Done.')

    def import_from_backup_file(self, content_pack_id, backup_file, skip_key_mapping=False):
        if not backup_file:
            return

        backup_path = Path(os.path.expanduser(backup_file)).resolve()

        importer = BackupImporter(content_pack_id, skip_key_mapping)
        importer.import_backup(backup_path)
