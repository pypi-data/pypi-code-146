from configparser import ConfigParser
from ..os.file import check_file_exist


# 读取配置
def read_ini(file_path: str) -> dict:
    values = {}
    if check_file_exist(file_path) is True:
        config = ConfigParser()
        config.read(file_path)

        for section in config.sections():
            for option in config.options(section):
                if section not in values.keys():
                    values[section] = {}
                values[section][option] = config.get(section, option)
    return values


# 读取配置
def read_init_key(file_path: str, section: str, name: str):
    if check_file_exist(file_path) is True:
        config = ConfigParser()
        config.read(file_path)
        if config.has_section(section) is True:
            if config.has_option(section, name) is True:
                return config.get(section, name)
    return None


def write_init(file_path: str, values: dict, is_update: bool = False):
    config = ConfigParser()
    if is_update:
        config.read(file_path)
    for section, params in values.items():
        if config.has_section(section) is False:
            config.add_section(section)
        for name, value in params.items():
            config.set(section, name, value)
    config.write(open(file_path, 'w'))