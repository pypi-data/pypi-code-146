import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Protocol

from . import __version__ as current_version
from .exceptions import GLParserException

logger = logging.getLogger(__name__)


class ConfigManager(Protocol):
    @classmethod
    def get_current(cls):
        ...


def backup_file(filename: Path, backup_folder: Path, add_version: bool = True) -> Path:
    if not backup_folder.is_dir():
        error_message = f'Backup folder has to be a folder.' \
                        f' Supplied: {backup_folder}. Type: {type(backup_folder)}'
        logger.error(error_message)
        raise GLParserException(error_message)

    datetime_format = '%Y%m%d_%H%M%S'
    try:
        if add_version:
            version_val = f'v{current_version}_'
        else:
            version_val = ''
        timestamp = datetime.now().strftime(datetime_format)
        backup_filename = backup_folder / f'{timestamp}_{version_val}{filename.name}'
        shutil.copy(filename, backup_filename)
        return backup_filename
    except Exception as e:
        error_message = f'Unexpected error backing up file {filename}. Type: {e.__class__.__name__}' \
                        f' error: {e}'
        logger.error(error_message)
        raise GLParserException(error_message)


def clean_filename(filename: str):
    new_name = filename.replace('.', '').replace(',', '').replace(' ', '_')
    return new_name


def build_output_excel_filename(excel_file: Path, configuration_manager: ConfigManager) -> str:
    configuration = configuration_manager.get_current()
    timestamp_format = configuration['application']['timestamp_format']
    timestamp = datetime.now().strftime(timestamp_format)
    clean_name = clean_filename(excel_file.stem)
    base_name = f'{timestamp}_{clean_name}.xlsx'
    return base_name
