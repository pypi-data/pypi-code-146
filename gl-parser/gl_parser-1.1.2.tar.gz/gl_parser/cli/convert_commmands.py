import logging
import shutil
import sys
from pathlib import Path

import click

from gl_parser import CONFIGURATION_MANAGER
from gl_parser.enums import ExitCode
from gl_parser.models import ParserConfig
from gl_parser.parsers import parse_general_ledger
from gl_parser.utils import build_output_excel_filename
from gl_parser.writers import write_parsed_transactions

logger = logging.getLogger(__name__)


@click.command(help='Convert general ledger Excel file')
@click.option('-f', '--filename', help="Excel file to convert.", type=click.Path(exists=False))
@click.option('-o', '--output-folder', required=False, help="Folder to save the new Excel file.")
def convert(filename, output_folder):
    excel_file = Path(filename)
    if not excel_file.exists():
        click.secho(f'File {excel_file} does not exist.', fg='red')
        sys.exit(ExitCode.INVALID_PATH)
    configuration = CONFIGURATION_MANAGER.get_current()
    if output_folder is None:
        output_directory = Path(configuration['application']['output_folder']['folder'])
    else:
        output_directory = Path(output_folder)
    if not output_directory.exists():
        click.secho(f'Output folder does not exist {output_directory}', fg='red')
        sys.exit(ExitCode.INVALID_PATH)
    try:
        parsing_config = ParserConfig()
        output_excel_filename = build_output_excel_filename(excel_file, CONFIGURATION_MANAGER)
        output_excel_file = output_directory / output_excel_filename
        shutil.copy(excel_file, output_excel_file)
        parsed_transactions = parse_general_ledger(excel_file, parsing_config)
        write_parsed_transactions(output_excel_file, parsed_transactions, parsing_config)
        click.secho(f'Successfully converted file to {output_excel_file}')
    except Exception as e:
        error_message = f'Unexpected error. Type: {e.__class__.__name__} error: {e}'
        logger.error(error_message)
        click.secho(error_message, fg='red')
        sys.exit(ExitCode.UNEXPECTED_ERROR)
