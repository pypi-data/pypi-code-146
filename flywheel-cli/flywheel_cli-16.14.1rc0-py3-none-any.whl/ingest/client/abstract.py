"""Abstract ingest client (CRUD) interface"""

import typing
import uuid
from abc import ABC, abstractmethod

from ...models import FWAuth
from .. import schemas as T
from ..config import IngestConfig, StrategyConfig


class Client(ABC):
    """Abstract ingest client interface"""

    def __init__(self, url: str):
        self.url = url
        self._ingest_id: typing.Optional[uuid.UUID] = None

    @classmethod
    def from_url(
        cls, url: str, ingest_id: typing.Optional[uuid.UUID] = None
    ) -> "Client":
        """Return client instance, bind it to an ingest id if any provided"""
        client = cls(url)
        if ingest_id:
            client.bind(ingest_id)
        return client

    @property
    def ingest_id(self) -> uuid.UUID:
        """Raise when trying to use ingest bound method
        when the client is not bound to any ingest_id
        """
        if not self._ingest_id:
            raise TypeError("Accessing ingest_id on un-bound client")
        return self._ingest_id

    @property
    def is_bound(self) -> bool:
        """Return that this client is bound to an ingest or not"""
        return bool(self._ingest_id)

    def bind(self, ingest_id: uuid.UUID) -> None:
        """Bind the client to an ingest id"""
        self._ingest_id = ingest_id

    # Non-ingest-bound methods

    @abstractmethod
    def create_ingest(
        self,
        config: IngestConfig,
        strategy_config: StrategyConfig,
        fw_auth: typing.Optional[FWAuth] = None,
    ) -> T.IngestOutAPI:
        """Create a new ingest and bind the client to it"""

    @abstractmethod
    def delete_ingest(self, ingest_id: uuid.UUID) -> None:
        """Delete an ingest and all related tasks from the pipeline"""

    @abstractmethod
    def list_ingests(
        self, api_key: typing.Optional[str] = None
    ) -> typing.Iterable[T.IngestOutAPI]:
        """Get all ingests"""

    # Ingest-bound methods

    @property
    @abstractmethod
    def ingest(self) -> T.IngestOutAPI:
        """Get ingest operation the client is bound to"""

    @abstractmethod
    def load_subject_csv(self, subject_csv: typing.BinaryIO) -> None:
        """Load subject CSV file"""

    @abstractmethod
    def start(self) -> T.IngestOutAPI:
        """Start ingest scanning"""

    @abstractmethod
    def review(self, changes=None) -> T.IngestOutAPI:
        """Review (accept) ingest, add any changes and start importing"""

    @abstractmethod
    def abort(self) -> T.IngestOutAPI:
        """Abort ingest operation"""

    @property
    @abstractmethod
    def progress(self) -> T.Progress:
        """Get ingest scan task and item/file/byte counts by status"""

    @property
    @abstractmethod
    def summary(self) -> T.Summary:
        """Get ingest hierarchy node and file count by level and type"""

    @property
    @abstractmethod
    def report(self) -> T.Report:
        """Get ingest status, elapsed time per status and list of failed tasks"""

    @property
    @abstractmethod
    def tree(self) -> typing.Iterable[T.Container]:
        """Yield hierarchy nodes (containers)"""

    @property
    @abstractmethod
    def audit_logs(self) -> typing.Iterable[str]:
        """Yield audit log CSV lines"""

    @property
    @abstractmethod
    def deid_logs(self) -> typing.Iterable[str]:
        """Yield de-id log CSV lines"""

    @property
    @abstractmethod
    def subjects(self) -> typing.Iterable[str]:
        """Yield subject CSV lines"""
