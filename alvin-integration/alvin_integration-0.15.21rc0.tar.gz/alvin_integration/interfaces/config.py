from abc import ABC, abstractmethod
from typing import List

from alvin_integration.models import AlvinPatch


class AbstractProducerConfig(ABC):
    @property
    @abstractmethod
    def producer_name(self):
        pass

    @abstractmethod
    def get_patching_list(self) -> List[AlvinPatch]:
        pass

    @abstractmethod
    def get_target_packages(self):
        pass

    @abstractmethod
    def get_target_pipelines(self):
        pass

    @abstractmethod
    def get_lineage_config(self):
        pass
