from __future__ import annotations

import json
from json import JSONDecodeError


class Configuration:
    def __init__(self, config_file_path: str):
        with open(config_file_path, "r") as config_file:
            try:
                self.config_object = json.load(config_file)
            except JSONDecodeError:
                raise SyntaxError("The json config file could not be read. Check that the file structure is valid.")
            except KeyError as error:
                raise KeyError(f"The key {error.args[0]} is required in the json config file.")

    def __getitem__(self, key) -> str | int:
        information: str | int = self.config_object.get(key)
        if not information:
            raise KeyError(key)
        return information
