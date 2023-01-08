import shutil

from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from itsicli.content_packs.backup.convert_backup import BackupConverter
from itsicli.content_packs.workspace import root_path
from itsicli.content_packs.files import ContentPackManifest, ContentModel
from itsicli.setup_logging import logger

BACKUP_DIR = 'backup'
ITSI_DIR = 'itsi'


def unarchive(source_zip, dest_dir):
    if source_zip.is_dir():
        backup_dir = Path(dest_dir).joinpath(BACKUP_DIR)
        shutil.copytree(source_zip, backup_dir)
        return backup_dir

    zip_file = ZipFile(source_zip)
    zip_file.extractall(path=dest_dir)

    backup_dir = Path(dest_dir).joinpath(BACKUP_DIR)

    return backup_dir if backup_dir.is_dir() else None


class BackupImporter(object):
    def __init__(self, content_pack_id, skip_key_mapping=False):
        self.content_pack_id = content_pack_id
        self.skip_key_mapping= skip_key_mapping
        self.prefix = '{}-'.format(self.content_pack_id).lower()

    def import_backup(self, backup_path):
        with TemporaryDirectory() as extract_dir:
            backup_dir = unarchive(backup_path, extract_dir)
            if not backup_dir:
                msg = 'No {}/ directory found in the backup file'.format(BACKUP_DIR)
                logger.error(msg)
                raise Exception(msg)

            converter = BackupConverter(self.prefix, self.skip_key_mapping)
            models = converter.to_models(backup_dir)

        self.write_models(models)

    def write_models(self, content_models):
        home_path = root_path()

        manifest = ContentPackManifest(home_path)

        for content_type, models in content_models.items():
            for model in models:
                try:
                    content_model = ContentModel(home_path, model, self.skip_key_mapping,
                                                 self.prefix)

                    if content_model.path.exists():
                        logger.info('Updating {}'.format(content_model.path))
                    else:
                        logger.info('Creating {}'.format(content_model.path))

                    content_model.write()
                except Exception as exc:
                    message = 'Failed to create "{}" with id="{}"'.format(content_type, model.get_key())
                    print(message)
                    logger.error(message)
                    logger.exception(exc)
                else:
                    manifest.add_content_model(content_model)

        if manifest.path.exists():
            logger.info('Updating manifest file at {}'.format(manifest.path))
        else:
            logger.info('Creating manifest file at {}'.format(manifest.path))

        manifest.write()
