from pathlib import Path

from inspector_commons.database import Database


class DatabaseConnector(Database):
    def is_same_path(self, path):
        return Path(path).samefile(Path(self.path))
