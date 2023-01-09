from configparser import ConfigParser

from clutchGen.constants import CONFIG_PATH
from clutchGen.enums import ConfigSectionEnum

_configparser = ConfigParser(strict=True)
_configparser.read(CONFIG_PATH)


def _save_config():
    with open(CONFIG_PATH, "w") as config_file:
        _configparser.write(config_file)


def get_all_template_name():
    return list(_configparser[ConfigSectionEnum.TEMPLATE_FILES].keys())


def get_template_file(template_name: str):
    return _configparser[ConfigSectionEnum.TEMPLATE_FILES].get(template_name)


def get_default_file_name(template_name: str):
    return _configparser[ConfigSectionEnum.TEMPLATE_DEFAULT_NAMES].get(template_name)


def set_template_file(template_name, file):
    _configparser.set(ConfigSectionEnum.TEMPLATE_FILES, template_name, file)
    _save_config()


def set_default_filename(template_name, filename):
    _configparser.set(ConfigSectionEnum.TEMPLATE_DEFAULT_NAMES, template_name, filename)
    _save_config()


def delete_template_file(template_name):
    _configparser.remove_option(ConfigSectionEnum.TEMPLATE_FILES, template_name)
    _save_config()


def delete_default_filename(template_name):
    _configparser.remove_option(ConfigSectionEnum.TEMPLATE_DEFAULT_NAMES, template_name)
    _save_config()
