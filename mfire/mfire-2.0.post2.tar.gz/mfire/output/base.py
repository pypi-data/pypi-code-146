""" class implementing an exportable Production model
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from pydantic import BaseModel

from mfire.settings import get_logger, Settings
from mfire.utils import JsonFile, MD5
from mfire.composite import AbstractComponentComposite

LOGGER = get_logger(name="output.base.mod", bind="output.base")


class BaseOutputProduction(BaseModel):
    """Base class to use for implementing an exportable Production model.
    This class may be used by heritage.
    """

    @property
    def hash(self) -> str:
        """Hash of the object

        Returns:
            str: hash
        """
        return MD5(obj=self.dict()).hash

    def dump(self, dump_dir: Path = None) -> Path:
        """Dump self to a JSON file.

        Args:
            dump_dir (Path, optional): Working directory where to dump.
                Defaults to None.

        Returns:
            Path: Dumped file's name.
        """
        if dump_dir is None:
            dump_dir = Settings().output_dirname
        else:
            dump_dir = Path(dump_dir)
        filename = dump_dir / f"prom_{self.ProductionId}_{self.hash}.json"
        filename.parent.mkdir(parents=True, exist_ok=True)
        JsonFile(filename).dump(self.dict(exclude_none=True))
        if filename.is_file():
            return filename
        LOGGER.error(f"Failed to dump {filename}.")
        return None

    def append(self, other_production: BaseOutputProduction) -> BaseOutputProduction:
        return BaseOutputProduction()

    @classmethod
    def concat(cls, productions: List[BaseOutputProduction]) -> BaseOutputProduction:
        if len(productions) == 0:
            return None
        production = productions.pop(0)
        for other_production in productions:
            production = production.append(other_production)
        return production


class BaseOutputAdapter(BaseModel):
    """Base class to use for implementing an adapter taking computed Components
    and their related texts as input and adapting them to an specific output model.

    """

    output_type: str
    component: AbstractComponentComposite
    texts: Dict[str, str]

    def compute(self) -> BaseOutputProduction:
        return BaseOutputProduction()
