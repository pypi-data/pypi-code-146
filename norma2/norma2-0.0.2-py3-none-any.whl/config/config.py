from typing import List, Optional

from rich.console import Console

from norma2.config.config_class import Config
from norma2.config.from_cmdline import from_cmdline
from norma2.config.from_gitignore import from_gitignore
from norma2.config.from_json import from_json


def get_config(console: Console, argv: Optional[List[str]] = None) -> Config:
    conf = Config(console)
    conf_cmdline = from_cmdline(console, argv)
    conf = conf + conf_cmdline
    conf_json = from_json(console)
    conf = conf + conf_json
    conf_gitignore = from_gitignore(console)
    conf = conf + conf_gitignore
    return conf
