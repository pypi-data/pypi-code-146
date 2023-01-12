import uuid

from copy import deepcopy
from typing import Optional, Dict, Any
from abc import ABC


class Tab(ABC):
    BLANK: Dict[str, Any]

    def __init__(self, deployable_id: Optional[str] = None) -> None:

        self._deployable_id = (
            str(uuid.uuid4()) if deployable_id is None else deployable_id
        )

    @property
    def deployable_id(self):
        return self._deployable_id

    @property
    def config(self) -> Dict[str, Any]:
        return self._config

    @config.setter
    def config(self, value: Dict[str, Any]):
        self._config = value

    def json(self):
        return self.config

    def reset(self):
        self.config = deepcopy(self.BLANK)
