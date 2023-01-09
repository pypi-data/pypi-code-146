import abc
import datetime
from typing import List

from tecton._internals.fco import Fco
from tecton_proto.args import feature_view_pb2
from tecton_proto.args import virtual_data_source_pb2


class BaseStreamConfig(abc.ABC):
    @abc.abstractmethod
    def _merge_stream_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        pass


class BaseBatchConfig(abc.ABC):
    @property
    @abc.abstractmethod
    def data_delay(self) -> datetime.timedelta:
        pass

    @abc.abstractmethod
    def _merge_batch_args(self, data_source_args: virtual_data_source_pb2.VirtualDataSourceArgs):
        pass


class OutputStream(abc.ABC):
    @abc.abstractmethod
    def _to_proto() -> feature_view_pb2.OutputStream:
        pass


class BaseEntity(Fco):
    @property
    def name(self) -> str:
        """
        Name of the entity.
        """
        raise NotImplementedError

    @property
    def join_keys(self) -> List[str]:
        """
        Join keys of the entity.
        """
        raise NotImplementedError


class BaseDataSource(Fco):
    @property
    def name(self) -> str:
        """
        The name of this DataSource.
        """
        raise NotImplementedError

    @property
    def data_delay(self) -> datetime.timedelta:
        raise NotImplementedError
