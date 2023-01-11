import re

from click.testing import CliRunner

import gl_parser.cli.config_commands
from gl_parser import CONFIGURATION_MANAGER
from gl_parser.enums import ExitCode

OUTPUT_PROMPT_REGEX = re.compile(r"Directorio\sde\ssalida\s\[.+\]:\s(?P<folder>[\w\-/]+)")
INPUT_PROMPT_REGEX = re.compile(r"Directorio\sde\sentrada\s\[.+\]:\s(?P<folder>[\w\-/]+)")
PROCESSED_PROMPT_REGEX = re.compile(r"Directorio\sde\sarchivos\sprocesados\s\[.+\]:\s(?P<folder>[\w\-/]+)")


def test_config_invalid_folder():
    runner = CliRunner()
    invalid_folder = '/home/does/not/exist'
    result = runner.invoke(gl_parser.cli.config_commands.config, ['--overwrite'],
                           input=f'{invalid_folder}\n')
    result_lines = result.output.split('\n')
    assert result.exit_code == ExitCode.INVALID_CONFIGURATION
    assert len(result_lines) == 4
    assert result_lines[0] == 'Configuration'
    assert OUTPUT_PROMPT_REGEX.match(result_lines[1]) is not None
    assert result_lines[2] == 'The supplied folder does not exist /home/does/not/exist please create it.'


def test_config_valid(output_folder):
    current_folders = CONFIGURATION_MANAGER.get_configuration_folders()
    input_folder = output_folder / 'input'
    out_folder = output_folder / 'output'
    processed_folder = output_folder / 'processed'

    assert input_folder != current_folders['input_folder']
    assert out_folder != current_folders['output_folder']
    assert processed_folder != current_folders['parsed_folder']

    new_folders = [out_folder, processed_folder, input_folder]
    prompt_response = '\n'.join([str(x) for x in new_folders])
    for folder in new_folders:
        folder.mkdir(exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(gl_parser.cli.config_commands.config, ['--overwrite'],
                           input=prompt_response)
    result_lines = result.output.split('\n')
    assert result.exit_code == 0
    assert result_lines[0] == 'Configuration'
    assert len(result_lines) == 5

    o_match = OUTPUT_PROMPT_REGEX.match(result_lines[1])
    assert o_match is not None
    assert o_match.group('folder') == str(out_folder)

    p_match = PROCESSED_PROMPT_REGEX.match(result_lines[2])
    assert p_match is not None
    assert p_match.group('folder') == str(processed_folder)

    i_match = INPUT_PROMPT_REGEX.match(result_lines[3])
    assert i_match is not None
    assert i_match.group('folder') == str(input_folder)

    config = CONFIGURATION_MANAGER.get_configuration()
    assert config['application']['output_folder']['folder'] == str(out_folder)
    assert config['application']['input_folder']['folder'] == str(input_folder)
    assert config['application']['parsed_folder']['folder'] == str(processed_folder)

    for folder_name, c_folder in current_folders.items():
        config['application'][folder_name]['folder'] = str(c_folder)
    CONFIGURATION_MANAGER.write_configuration(config_data=config, overwrite=True)
