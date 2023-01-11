import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any

import click

from gl_parser import ConfigurationManager, CONFIGURATION_MANAGER
from gl_parser.enums import ExitCode
from gl_parser.exceptions import GLParserException

logger = logging.getLogger(__name__)


@click.command()
@click.argument('sub_command', required=False)
@click.option('--overwrite', is_flag=True, default=False, help="Overwrite the configuration file.")
def config(sub_command, overwrite):
    """Configure the application. Sub commands:

    SHOW: shows current configuration.
    DELETE: deletes current configuration."""
    if sub_command is None:
        click.echo('Configuration')
        do_configuration(overwrite)
    elif sub_command == 'show':
        do_show()
    elif sub_command == 'delete':
        backup_file = CONFIGURATION_MANAGER.backup()
        click.secho(f'Backed up current configuration {backup_file}', fg='green')
        confirmation = click.prompt(f'Are you sure you want to delete the configuration file. (Y/N)', default='N')
        if confirmation.upper() == 'Y':
            CONFIGURATION_MANAGER.config_file.unlink()
        # do_configuration(True)
    else:
        click.echo(f'sub command {sub_command}')


def do_configuration(overwrite: bool, configuration_manager: Optional[ConfigurationManager] = None):
    if configuration_manager is None:
        configuration_manager = CONFIGURATION_MANAGER
    if configuration_manager.config_file.exists() and not overwrite:
        click.secho('Configuration file already exists. Run with --overwrite flag.', fg='red')
        sys.exit(ExitCode.CANNOT_OVERWRITE)

    configuration = CONFIGURATION_MANAGER.get_current()

    prompt_for_folders(configuration, 'application')
    configuration_manager.write_configuration(configuration, overwrite=overwrite)
    # try:
    # output_folder_prompt = 'Type the default output folder'
    # output_folder_name = click.prompt(output_folder_prompt, default=configuration['application']['output_folder'])
    # output_folder = Path(output_folder_name)
    # if not output_folder.exists():
    #     message = f'The supplied folder does not exist {output_folder_name} please create it.'
    #     click.secho(message, fg='red')
    #     logger.warning(message)
    #     sys.exit(ExitCode.INVALID_CONFIGURATION)
    # if not output_folder.is_dir():
    #     message = f'The supplied folder is not a folder {output_folder_name}.'
    #     click.secho(message, fg='red')
    #     logger.warning(message)
    #     sys.exit(ExitCode.INVALID_CONFIGURATION)
    # configuration['application']['output_folder'] = str(output_folder.resolve())
    # backup_file = configuration_manager.backup()
    # logger.debug(f'Backed up configuration to {backup_file} before writing.')

    # configuration_manager.write_configuration(configuration, overwrite=overwrite)

    # except KeyError as e:
    #     error_message = f'Configuration error key not found. Error: {e}'
    #     logger.debug(error_message)
    #     raise GLParserException(error_message)


def prompt_for_folders(configuration: Dict[str, Any], key_with_folders: str) -> Dict[str, Any]:
    try:
        for key, folder_option in configuration[key_with_folders].items():
            if not isinstance(folder_option, dict):
                continue
            prompt = folder_option.get('prompt')
            if prompt is None:
                continue
            default_folder = configuration[key_with_folders][key]['folder']
            folder_name = click.prompt(prompt, default=default_folder)
            folder = Path(folder_name)
            if not folder.exists():
                message = f'The supplied folder does not exist {folder_name} please create it.'
                click.secho(message, fg='red')
                logger.warning(message)
                sys.exit(ExitCode.INVALID_CONFIGURATION)
            if not folder.is_dir():
                message = f'The supplied folder is not a folder {folder_name}.'
                click.secho(message, fg='red')
                logger.warning(message)
                sys.exit(ExitCode.INVALID_CONFIGURATION)

            configuration[key_with_folders][key]['folder'] = str(folder.resolve())
        return configuration
    except KeyError as e:
        error_message = f'Configuration error key not found. Error: {e}'
        logger.error(error_message)
        raise GLParserException(error_message)


def do_show(configuration_manager: Optional[ConfigurationManager] = None):
    if configuration_manager is None:
        configuration_manager = CONFIGURATION_MANAGER
    with open(configuration_manager.config_file, 'r') as f:
        text = f.read()
    click.echo(text)
