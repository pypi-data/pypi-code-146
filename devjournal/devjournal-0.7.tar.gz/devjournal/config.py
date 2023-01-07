from dataclasses import dataclass

import tomli

from devjournal.constants import config_file


@dataclass
class Config:
    remote_repo_url: str
    remote_branch: str

    @property
    def path(self):
        return str(config_file())

    def write(self):
        config_file().write_text(
            f'''remote_repo_url = "{self.remote_repo_url}"
remote_branch = "{self.remote_branch}"'''
        )

    @property
    def text(self):
        return config_file().read_text()


def get_config():
    if not config_file().exists():
        return Config("", "")
    config_dict = tomli.loads(config_file().read_text())
    return Config(**config_dict)


def is_repo_defined():
    return bool(get_config().remote_repo_url)
