from pathlib import Path

from .exceptions import TemplateNotFound


class BaseLoader:
    def get_source(self, name):
        pass


class FileSystemLoader:
    def __init__(self, search_path):
        if isinstance(search_path, str):
            self.search_path = [Path(search_path).expanduser()]
        elif isinstance(search_path, Path):
            self.search_path = [search_path]
        else:
            self.search_path = [Path(_).expanduser() for _ in search_path]

    def get_source(self, name) -> [str, Path]:
        for path in self.search_path:
            if (source_path := path / name).is_file():
                with source_path.open('r', encoding='utf-8') as f:
                    return f.read(), source_path
        else:
            checked = ','.join(str(_) for _ in self.search_path)
            raise TemplateNotFound(f'{name} not found on path(s) {checked}')
