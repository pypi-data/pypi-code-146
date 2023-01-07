import os

from igittigitt import IgnoreParser
from rich.console import Console

from norma2.config.config_class import Config


def from_gitignore(console: Console, conf_path: str = ".") -> Config:
    full_path = os.path.join(conf_path, ".gitignore")
    full_path = os.path.abspath(full_path)
    conf = Config(console)
    if not os.path.isfile(full_path):
        return conf
    parser = IgnoreParser()
    parser.parse_rule_file(full_path)
    matches = parser.match
    conf.gitignore_matches = matches
    return conf
