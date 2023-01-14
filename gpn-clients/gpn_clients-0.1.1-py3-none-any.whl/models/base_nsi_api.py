from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from pydantic import HttpUrl, PositiveInt


class AbstractAlgorithms(ABC):
    @abstractmethod
    def get_all(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_by_id(self, *args, **kwargs) -> HttpUrl:
        pass


class AbstractConfigs(ABC):
    @abstractmethod
    def get_all(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_by_id(self, *args, **kwargs) -> HttpUrl:
        pass


class AbstractModelsML(ABC):
    @abstractmethod
    def get_all(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_by_id(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_binary_view(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_info_for_name(self, model_name: str, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_ml_data_for_tag(self, tag_name: str, *args, **kwargs) -> HttpUrl:
        pass


class AbstractTimeSeries(ABC):
    @abstractmethod
    def get_for_timerange(
        self,
        tag_name: str,
        start: datetime,
        finish: Optional[datetime],
    ) -> HttpUrl:
        pass

    @abstractmethod
    def get_for_tail(self, tag_name: str, tail_size: PositiveInt) -> HttpUrl:
        pass


class AbstractIOConfig(ABC):
    @abstractmethod
    def get_all(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_by_id(self, *args, **kwargs) -> HttpUrl:
        pass

    @abstractmethod
    def get_by_id_config(self, *args, **kwargs) -> HttpUrl:
        pass
