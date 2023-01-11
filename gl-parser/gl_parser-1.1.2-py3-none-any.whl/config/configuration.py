import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List

import toml

from .. import exceptions
from ..utils import backup_file


class ConfigurationManager:
    DEFAULT_CONFIG_FOLDER_NAME = '.gl_parser'
    DEFAULT_CONFIG_FILENAME = 'configuration.toml'
    APP_NAME = 'gl-parser'

    def __init__(self, config_folder: Optional[Path] = None,
                 config_filename: Optional[str] = None):
        if config_folder is None:
            self.config_folder = Path().home() / self.DEFAULT_CONFIG_FOLDER_NAME
        else:
            self.config_folder = config_folder
        if config_filename is None:
            self.config_file = self.config_folder / self.DEFAULT_CONFIG_FILENAME
        else:
            self.config_file = self.config_folder / config_filename

        self.config_backup_folder = self.config_folder / 'backups'
        self.logs_folder = self.config_folder / 'logs'

        self.username = os.getlogin()
        self.prep_config()

    def get_sample_config(self) -> Dict[str, Any]:
        home = Path().home()
        data = {
            'application': {
                'output_folder': {
                    'folder': str(home / 'output_general_ledgers'),
                    'prompt': 'Directorio de salida'
                },
                'parsed_folder': {
                    'folder': str(home / 'parsed_general_ledgers'),
                    #'prompt': 'Directorio de archivos procesados'
                },
                'input_folder': {
                    'folder': str(home / 'input_general_ledgers'),
                    # 'prompt': 'Directorio de entrada'
                },
                'timestamp_format': '%Y%m%d_%H%M%S'
            },
            'logs': {
                'folder': str(self.logs_folder),
                'filename': f'{self.APP_NAME}.log',
                'backup_count': 3
            },
            'parsers': {
                'sheet_name': 'General Ledger',
                'start_row': 6,
                'column_mappings': {
                    '1': {'name': 'account_id', 'title': 'Account ID', 'width': 12},
                    '2': {'name': 'account_description', 'title': 'Account Description', 'width': 24},
                    '3': {'name': 'date', 'title': 'Date', 'number_format': 'DD/MM/YYYY', 'width': 12},
                    '4': {'name': 'reference', 'title': 'Reference', 'width': 30},
                    '5': {'name': 'journal', 'title': 'Jrnl', 'width': 12},
                    '6': {'name': 'description', 'title': 'Trans Description', 'width': 36},
                    '7': {'name': 'debit_amount', 'title': 'Debit Amt', 'number_format': '#,##0.00', 'width': 12},
                    '8': {'name': 'credit_amount', 'title': 'Credit Amt', 'number_format': '#,##0.00', 'width': 12},
                    '9': {'name': 'balance', 'title': 'Balance', 'number_format': '#,##0.00', 'width': 12},
                }}
        }
        return data

    def prep_config(self):
        self.config_folder.mkdir(exist_ok=True)
        self.config_backup_folder.mkdir(exist_ok=True)
        self.logs_folder.mkdir(exist_ok=True)
        if not self.config_file.exists():
            tmp_config = self.get_sample_config()
            self.write_configuration(tmp_config)

    def write_configuration(self, config_data: Dict[str, Any], overwrite: bool = False, ) -> None:
        if self.config_file.exists() and not overwrite:
            raise Exception('Cannot overwrite config file.')
        with open(self.config_file, 'w') as f:
            toml.dump(config_data, f)

    def get_configuration(self) -> Dict[str, Any]:
        if not self.config_folder.exists():
            error_message = 'No configuration file found. Run  config.'
            raise exceptions.ConfigurationError(error_message)

        with open(self.config_file, 'r') as f:
            configuration = toml.load(f)
        return configuration

    def export_to_json(self, export_file: Path) -> None:
        config = self.get_configuration()
        with open(export_file, 'w') as f:
            json.dump(config, f)

    def backup(self) -> Path:
        backup_filename = backup_file(self.config_file, self.config_backup_folder)
        return backup_filename

    def delete(self) -> Path:
        backup_filename: Path = self.backup()
        self.config_file.unlink(missing_ok=True)
        return backup_filename

    def get_configuration_folders(self) -> Dict[str, Path]:
        config = self.get_configuration()
        folders = dict()
        for key, folder_option in config['application'].items():
            if not isinstance(folder_option, dict):
                continue
            if folder_option.get('folder') is None:
                continue
            folders[key] = Path(folder_option['folder'])
        return folders

    @classmethod
    def get_current(cls):
        config = cls()
        return config.get_configuration()


def get_report_info(configuration_manager: ConfigurationManager, output_folder):
    pass
