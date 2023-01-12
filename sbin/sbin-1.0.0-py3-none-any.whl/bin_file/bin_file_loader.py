from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic.error_wrappers import ValidationError

from bin.bin_file.bin_file_resolver import BinFileResolver
from bin.bin_file.errors import BinFileNotFound, BinFileParsingError
from bin.models.bin_base_model import BinBaseModel


class BinConfigFile(BinBaseModel):
    bin_file: str


class BinFileLoader:
    DEFAULT_BIN_FILE_NAME = "bin.yml"
    CONFIG_FILE_PATHS = [".binconfig.yml", ".binconfig.yaml"]
    DEFAULT_BIN_FILE_PATHS = [DEFAULT_BIN_FILE_NAME, "bin.yaml"]

    @staticmethod
    def find_any_bin_file(current_dir: Path) -> Optional[Path]:
        return BinFileResolver.find_first_file(
            current_dir, BinFileLoader.DEFAULT_BIN_FILE_PATHS + BinFileLoader.CONFIG_FILE_PATHS
        )

    @staticmethod
    def load(current_dir: Path) -> Dict[str, Any]:
        bin_file = BinFileLoader._load_bin_file(current_dir)
        if bin_file is None:
            raise BinFileNotFound(f"bin file in dir '{current_dir.absolute()}' not found")

        return BinFileLoader._parse_as_dict(bin_file, "bin")

    @staticmethod
    def _load_bin_file(current_dir: Path) -> Optional[Path]:
        bin_file = BinFileLoader._load_bin_file_path_from_config(current_dir)
        if bin_file is None:
            return BinFileResolver.find_first_file(current_dir, BinFileLoader.DEFAULT_BIN_FILE_PATHS)

        bin_path = BinFileResolver.find_first_file(current_dir, [bin_file])
        if bin_path is None:
            raise BinFileNotFound(f"bin file '{current_dir / bin_file}' not found")

        return bin_path

    @staticmethod
    def _load_bin_file_path_from_config(current_dir: Path) -> Optional[str]:
        config_file = BinFileResolver.find_first_file(current_dir, BinFileLoader.CONFIG_FILE_PATHS)
        if config_file is None:
            return None

        parsed = BinFileLoader._parse_as_dict(config_file, "config")
        try:
            return BinConfigFile.parse_obj(parsed).bin_file
        except ValidationError:
            raise BinFileParsingError(f"invalid config file '{config_file}'")

    @staticmethod
    def _parse_as_dict(file_path: Path, file_type: str) -> Dict[str, Any]:
        try:
            content = yaml.safe_load(file_path.read_bytes())
            if not isinstance(content, dict):
                raise BinFileParsingError(f"invalid {file_type} file '{file_path}'")

            return content
        except Exception:
            raise BinFileParsingError(f"invalid {file_type} file '{file_path}'")
