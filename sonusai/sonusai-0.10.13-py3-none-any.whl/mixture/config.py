from pathlib import Path
from typing import Dict
from typing import List
from typing import Union

from sonusai.mixture.types import ImpulseResponseFiles
from sonusai.mixture.types import Location
from sonusai.mixture.types import NoiseFiles
from sonusai.mixture.types import TargetFiles


def raw_load_config(name: Location) -> Dict:
    """Load YAML config file

    :param name: File name
    :return: Dictionary of config data
    """
    import yaml

    with open(file=name, mode='r') as f:
        config = yaml.safe_load(f)

    return config


def get_default_config() -> Dict:
    """Load default SonusAI config

    :return: Dictionary of default config data
    """
    from sonusai import SonusAIError
    from sonusai.mixture import DEFAULT_CONFIG

    try:
        return raw_load_config(DEFAULT_CONFIG)
    except Exception as e:
        raise SonusAIError(f'Error loading default config: {e}')


def load_config(name: Location) -> Dict:
    """Load SonusAI default config and update with given location (performing SonusAI variable substitution)

    :param name: Directory containing mixture database
    :return: Dictionary of config data
    """
    from os.path import join

    return update_config_from_file(name=join(name, 'config.yml'), config=get_default_config())


def update_config_from_file(name: Location, config: Dict) -> Dict:
    """Update the given config with the config in the given YAML file

    :param name: File name
    :param config: Config dictionary to update
    :return: Updated config dictionary
    """
    from copy import deepcopy

    from sonusai import SonusAIError
    from sonusai.mixture import REQUIRED_CONFIGS
    from sonusai.mixture import VALID_CONFIGS

    new_config = deepcopy(config)

    try:
        given_config = raw_load_config(name)
    except Exception as e:
        raise SonusAIError(f'Error loading config from {name}: {e}')

    # Check for unrecognized keys
    for key in given_config:
        if key not in VALID_CONFIGS:
            nice_list = '\n'.join([f'  {item}' for item in VALID_CONFIGS])
            raise SonusAIError(f'Invalid config parameter in {name}: {key}.\nValid config parameters are:\n{nice_list}')

    # Use default config as base and overwrite with given config keys as found
    for key in new_config:
        if key in given_config:
            if key not in ['truth_settings']:
                new_config[key] = given_config[key]

    # Handle 'truth_settings' special case
    if 'truth_settings' in given_config:
        new_config['truth_settings'] = deepcopy(given_config['truth_settings'])

    if not isinstance(new_config['truth_settings'], list):
        new_config['truth_settings'] = [new_config['truth_settings']]

    default = deepcopy(config['truth_settings'])
    if not isinstance(default, list):
        default = [default]

    new_config['truth_settings'] = update_truth_settings(new_config['truth_settings'], default)

    # Check for required keys
    for key in REQUIRED_CONFIGS:
        if key not in new_config:
            raise SonusAIError(f'Missing required config in {name}: {key}')

    return new_config


def update_truth_settings(given: Union[List[Dict], Dict], default: List[Dict] = None) -> List[Dict]:
    """Update missing fields in given 'truth_settings' with default values

    :param given: The dictionary of given truth settings
    :param default: The dictionary of default truth settings
    :return: Updated dictionary of truth settings
    """
    from copy import deepcopy

    from sonusai import SonusAIError
    from sonusai.mixture import VALID_TRUTH_SETTINGS

    truth_settings = deepcopy(given)
    if not isinstance(truth_settings, list):
        truth_settings = [truth_settings]

    if default is not None and len(truth_settings) != len(default):
        raise SonusAIError(f'Length of given does not match default')

    for n in range(len(truth_settings)):
        for key in truth_settings[n]:
            if key not in VALID_TRUTH_SETTINGS:
                nice_list = '\n'.join([f'  {item}' for item in VALID_TRUTH_SETTINGS])
                raise SonusAIError(f'Invalid truth_settings: {key}.\nValid truth_settings are:\n{nice_list}')

        for key in VALID_TRUTH_SETTINGS:
            if key not in truth_settings[n]:
                if default is not None and key in default[n]:
                    truth_settings[n][key] = default[n][key]
                else:
                    raise SonusAIError(f'Missing required truth_settings: {key}')

    for truth_setting in truth_settings:
        if not isinstance(truth_setting['index'], list):
            truth_setting['index'] = [truth_setting['index']]

    return truth_settings


def get_hierarchical_config_files(root: str, leaf: str) -> List[Path]:
    """Get a hierarchical list of config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :return: List of config files found in the hierarchy
    """
    from sonusai import SonusAIError
    import os

    config_file = 'config.yml'

    root_path = Path(os.path.abspath(root))
    if not root_path.is_dir():
        raise SonusAIError(f'Given root, {root_path}, is not a directory.')

    leaf_path = Path(os.path.abspath(leaf))
    if not leaf_path.is_dir():
        raise SonusAIError(f'Given leaf, {leaf_path}, is not a directory.')

    common = os.path.commonpath((root_path, leaf_path))
    if os.path.normpath(common) != os.path.normpath(root_path):
        raise SonusAIError(f'Given leaf, {leaf_path}, is not in the hierarchy of the given root, {root_path}')

    top_config_file = Path(os.path.join(root_path, config_file))
    if not top_config_file.is_file():
        raise SonusAIError(f'Could not find {top_config_file}')

    current = leaf_path
    config_files = []
    while current != root_path:
        local_config_file = Path(os.path.join(current, config_file))
        if local_config_file.is_file():
            config_files.append(local_config_file)
        current = current.parent

    config_files.append(top_config_file)
    return list(reversed(config_files))


def update_config_from_hierarchy(root: str, leaf: str, config: dict) -> dict:
    """Update the given config using the hierarchical config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :param config: Config to update
    :return: Updated config
    """
    from copy import deepcopy

    new_config = deepcopy(config)
    config_files = get_hierarchical_config_files(root=root, leaf=leaf)
    for config_file in config_files:
        new_config = update_config_from_file(name=config_file, config=new_config)

    return new_config


def get_max_class(num_classes: int, truth_mutex: bool) -> int:
    """Get the maximum class index

    :param num_classes: Number of classes
    :param truth_mutex: Truth is mutex mode
    :return: Highest class index
    """
    max_class = num_classes
    if truth_mutex:
        max_class -= 1
    return max_class


def get_target_files(config: dict) -> TargetFiles:
    """Get the list of target files from a config

    :param config: Config dictionary
    :return: List of target files
    """
    from sonusai import SonusAIError
    from sonusai.utils import dataclass_from_dict

    truth_settings = config.get('truth_settings', list())
    target_level_type = config.get('target_level_type', None)
    target_files = []
    for target_file in config['targets']:
        append_target_files(target_files, target_file, truth_settings, target_level_type)

    max_class = get_max_class(config['num_classes'], config['truth_mode'] == 'mutex')

    for target_file in target_files:
        target_file['truth_settings'] = update_truth_settings(target_file['truth_settings'], config['truth_settings'])

        for truth_setting in target_file['truth_settings']:
            if any(idx > max_class for idx in truth_setting['index']):
                raise SonusAIError('invalid truth index')

    return dataclass_from_dict(TargetFiles, target_files)


def append_target_files(target_files: List[dict],
                        target_file: Union[dict, str],
                        truth_settings: List[dict],
                        target_level_type: str,
                        tokens: dict = None) -> None:
    """Process target files list and append as needed

    :param target_files: Working list of target files
    :param target_file: Target file entry to append to the list
    :param truth_settings: Truth settings for the target
    :param target_level_type: Target level type for the target
    :param tokens: Tokens used for variable expansion
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import sox

    from sonusai import SonusAIError

    if tokens is None:
        tokens = {}

    if isinstance(target_file, dict):
        if 'name' in target_file:
            in_name = target_file['name']
        else:
            raise SonusAIError('Target list contained record without name')

        if 'truth_settings' in target_file:
            truth_settings = target_file['truth_settings']
        if 'target_level_type' in target_file:
            target_level_type = target_file['target_level_type']
    else:
        in_name = target_file

    in_name, new_tokens = tokenized_expandvars(in_name)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                append_target_files(target_files, child, truth_settings, target_level_type, tokens)
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expandvars(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                append_target_files(target_files, child, truth_settings, target_level_type, tokens)
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'targets' in yml_config:
                            for record in yml_config['targets']:
                                append_target_files(target_files, record, truth_settings, target_level_type, tokens)
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    sox.file_info.validate_input_file(name)
                    duration = sox.file_info.duration(name)
                    for key, value in tokens.items():
                        name = name.replace(value, f'${key}')
                    entry = {
                        'name': name,
                        'duration': duration,
                    }
                    if len(truth_settings) > 0:
                        entry['truth_settings'] = truth_settings
                        for truth_setting in entry['truth_settings']:
                            if 'function' in truth_setting and truth_setting['function'] == 'file':
                                truth_setting['config']['file'] = splitext(name)[0] + '.h5'
                    if target_level_type is not None:
                        entry['target_level_type'] = target_level_type
                    target_files.append(entry)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')


def get_noise_files(config: dict) -> NoiseFiles:
    """Get the list of noise files from a config

    :param config: Config dictionary
    :return: List of noise file
    """
    from sonusai.utils import dataclass_from_dict

    noise_files = []
    for noise_file in config['noises']:
        append_noise_files(noise_files, noise_file)

    return dataclass_from_dict(NoiseFiles, noise_files)


def append_noise_files(noise_files: List[dict],
                       noise_file: Union[dict, str],
                       tokens: dict = None) -> None:
    """Process noise files list and append as needed

    :param noise_files: Working list of noise files
    :param noise_file: Noise file entry to append to the list
    :param tokens: Tokens used for variable expansion
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import sox

    from sonusai import SonusAIError

    if tokens is None:
        tokens = {}

    if isinstance(noise_file, dict):
        if 'name' in noise_file:
            in_name = noise_file['name']
        else:
            raise SonusAIError('Noise list contained record without name')
    else:
        in_name = noise_file

    in_name, new_tokens = tokenized_expandvars(in_name)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                append_noise_files(noise_files, child, tokens)
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expandvars(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                append_noise_files(noise_files, child, tokens)
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'noises' in yml_config:
                            for record in yml_config['noises']:
                                append_noise_files(noise_files, record, tokens)
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    sox.file_info.validate_input_file(name)
                    duration = sox.file_info.duration(name)
                    for key, value in tokens.items():
                        name = name.replace(value, f'${key}')
                    entry = {
                        'name': name,
                        'duration': duration,
                    }
                    noise_files.append(entry)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')


def get_ir_files(config: dict) -> ImpulseResponseFiles:
    """Get the list of impulse response files from a config

    :param config: Config dictionary
    :return: List of impulse response files
    """
    ir_files = []
    for ir_file in config['impulse_responses']:
        append_ir_files(ir_files, ir_file)

    return ir_files


def append_ir_files(ir_files: List[Location],
                    ir_file: Location,
                    tokens: dict = None) -> None:
    """Process impulse response files list and append as needed

    :param ir_files: Working list of impulse response files
    :param ir_file: Impulse response file entry to append to the list
    :param tokens: Tokens used for variable expansion
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    import sox

    from sonusai import SonusAIError

    if tokens is None:
        tokens = {}

    in_name, new_tokens = tokenized_expandvars(ir_file)
    tokens.update(new_tokens)
    names = glob(in_name)
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                append_ir_files(ir_files, child, tokens)
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expandvars(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                append_ir_files(ir_files, child, tokens)
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'impulse_responses' in yml_config:
                            for record in yml_config['impulse_responses']:
                                append_ir_files(ir_files, record, tokens)
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    sox.file_info.validate_input_file(name)
                    for key, value in tokens.items():
                        name = name.replace(value, f'${key}')
                    ir_files.append(name)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')


def tokenized_expandvars(path: str) -> (str, dict):
    """Expand shell variables of the forms $var, ${var} and %var%.
    Unknown variables are left unchanged.

    Expand paths containing shell variable substitutions. The following rules apply:
        - no expansion within single quotes
        - '$$' is translated into '$'
        - '%%' is translated into '%' if '%%' are not seen in %var1%%var2%
        - ${varname} is accepted.
        - $varname is accepted.
        - %varname% is accepted.
        - varnames can be made out of letters, digits and the characters '_-'
        (though is not verified in the ${varname} and %varname% cases)

    :param path: String to expand
    :return: Tuple of (expanded string, dictionary of tokens)
    """
    import os
    import string

    from sonusai.mixture import DEFAULT_NOISE

    os.environ['default_noise'] = DEFAULT_NOISE

    path = os.fspath(path)
    token_map = {}
    if isinstance(path, bytes):
        if b'$' not in path and b'%' not in path:
            return path, token_map
        varchars = bytes(string.ascii_letters + string.digits + '_-', 'ascii')
        quote = b'\''
        percent = b'%'
        brace = b'{'
        rbrace = b'}'
        dollar = b'$'
        environ = getattr(os, 'environb', None)
    else:
        if '$' not in path and '%' not in path:
            return path, token_map
        varchars = string.ascii_letters + string.digits + '_-'
        quote = '\''
        percent = '%'
        brace = '{'
        rbrace = '}'
        dollar = '$'
        environ = os.environ
    res = path[:0]
    index = 0
    pathlen = len(path)
    while index < pathlen:
        c = path[index:index + 1]
        if c == quote:  # no expansion within single quotes
            path = path[index + 1:]
            pathlen = len(path)
            try:
                index = path.index(c)
                res += c + path[:index + 1]
            except ValueError:
                res += c + path
                index = pathlen - 1
        elif c == percent:  # variable or '%'
            if path[index + 1:index + 2] == percent:
                res += c
                index += 1
            else:
                path = path[index + 1:]
                pathlen = len(path)
                try:
                    index = path.index(percent)
                except ValueError:
                    res += percent + path
                    index = pathlen - 1
                else:
                    var = path[:index]
                    try:
                        if environ is None:
                            value = os.fsencode(os.environ[os.fsdecode(var)])
                        else:
                            value = environ[var]
                        token_map[var] = value
                    except KeyError:
                        value = percent + var + percent
                    res += value
        elif c == dollar:  # variable or '$$'
            if path[index + 1:index + 2] == dollar:
                res += c
                index += 1
            elif path[index + 1:index + 2] == brace:
                path = path[index + 2:]
                pathlen = len(path)
                try:
                    index = path.index(rbrace)
                except ValueError:
                    res += dollar + brace + path
                    index = pathlen - 1
                else:
                    var = path[:index]
                    try:
                        if environ is None:
                            value = os.fsencode(os.environ[os.fsdecode(var)])
                        else:
                            value = environ[var]
                        token_map[var] = value
                    except KeyError:
                        value = dollar + brace + var + rbrace
                    res += value
            else:
                var = path[:0]
                index += 1
                c = path[index:index + 1]
                while c and c in varchars:
                    var += c
                    index += 1
                    c = path[index:index + 1]
                try:
                    if environ is None:
                        value = os.fsencode(os.environ[os.fsdecode(var)])
                    else:
                        value = environ[var]
                    token_map[var] = value
                except KeyError:
                    value = dollar + var
                res += value
                if c:
                    index -= 1
        else:
            res += c
        index += 1
    return res, token_map


def get_class_weights_threshold(config: Dict) -> List[float]:
    """Get the class_weights_threshold from a config

    :param config: Config dictionary
    :return: class_weights_threshold
    """
    from sonusai import SonusAIError

    class_weights_threshold = config['class_weights_threshold']
    num_classes = config['num_classes']

    if not isinstance(class_weights_threshold, list):
        class_weights_threshold = [class_weights_threshold]

    if len(class_weights_threshold) == 1:
        class_weights_threshold = [class_weights_threshold[0]] * num_classes

    if len(class_weights_threshold) != num_classes:
        raise SonusAIError(f'invalid class_weights_threshold length: {len(class_weights_threshold)}')

    return class_weights_threshold


def generate_mixture_filename(mixid: int, padding: int) -> str:
    """Generate a zero-padded mixture file name

    :param mixid: Mixture ID
    :param padding: Amount of padding
    :return: Zero-padded mixture file name
    """
    return f'{mixid:0{padding}}.h5'
