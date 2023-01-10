"""CLI getter for environment variables"""
from dataclasses import dataclass
from typing import Generator, List

from mcli.cli.m_get.display import MCLIDisplayItem, MCLIGetDisplay, OutputDisplay
from mcli.config import MCLIConfig, MCLIConfigError
from mcli.models import MCLIEnvVar
from mcli.utils.utils_logging import FAIL, err_console


@dataclass
class EnvDisplayItem(MCLIDisplayItem):
    key: str
    value: str


class MCLIEnvDisplay(MCLIGetDisplay):
    """`mcli get env` display class
    """

    def __init__(self, envs: List[MCLIEnvVar]):
        self.envs = envs

    def __iter__(self) -> Generator[EnvDisplayItem, None, None]:
        for env_var in self.envs:
            yield EnvDisplayItem(key=env_var.key, value=env_var.value)

    @property
    def index_label(self) -> str:
        return "key"


def get_environment_variables(output: OutputDisplay = OutputDisplay.TABLE, **kwargs) -> int:
    del kwargs

    try:
        conf: MCLIConfig = MCLIConfig.load_config()
    except MCLIConfigError:
        err_console.print(f'{FAIL} MCLI not yet initialized. Please run `mcli init` and then `mcli create env` '
                          'to create your first environment variable.')
        return 1

    display = MCLIEnvDisplay(conf.environment_variables)
    display.print(output)
    return 0
