from abc import ABC, abstractmethod
from contextlib import contextmanager
from os import fchmod, get_exec_path, symlink
from pathlib import Path
from typing import Iterator, Optional, TextIO

from sym.shared.cli.helpers.contexts import push_env
from sym.shared.cli.helpers.os import find_command


class Sandbox(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.exec_path = get_exec_path()

    def link_binary(self, name):
        symlink(find_command(name, path=self.exec_path), str(self.path / "bin" / name))

    def create_binary(self, name, exist_ok=True):
        try:
            self.create_file(name, mode=0o755, contents="#!/bin/bash\n")
        except FileExistsError:
            if not exist_ok:
                raise

    def create_dir(self, name: str) -> Path:
        path = self.path / name
        path.mkdir(parents=True, exist_ok=True)
        return path

    def create_file(
        self, name: str, mode: int = 0o644, contents: Optional[str] = None
    ) -> None:
        with self.create_file_with_content(name, mode) as f:
            if contents:
                f.write(contents)

    @abstractmethod
    def reset_config(self):
        pass

    @abstractmethod
    def setup(self, *args, **kwargs):
        pass

    @contextmanager
    def create_file_with_content(self, name: str, mode: int = 0o644) -> Iterator[TextIO]:
        path = self.path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x") as f:
            fchmod(f.fileno(), mode)
            yield f

    @contextmanager
    def push_exec_path(self) -> Iterator[None]:
        with push_env("PATH", str(self.path / "bin")):
            yield

    @contextmanager
    def push_xdg_config_home(self) -> Iterator[None]:
        with push_env("XDG_CONFIG_HOME", str(self.path / ".config")):
            self.reset_config()
            yield

    @contextmanager
    def push_home(self) -> Iterator[None]:
        with push_env("HOME", str(self.create_dir("home"))):
            yield
