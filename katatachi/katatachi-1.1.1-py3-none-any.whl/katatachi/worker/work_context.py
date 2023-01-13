import logging

from katatachi.content import ContentStore
from katatachi.interface.worker import MetadataStore
from katatachi.interface.worker import WorkContext
from .metadata_store import MetadataStoreFactory
from .worker_run_store import WorkerRunStore


class WorkContextImpl(WorkContext):
    def __init__(
        self,
        worker_id: str,
        run_id: str,
        content_store: ContentStore,
        worker_run_store: WorkerRunStore,
        metadata_store_factory: MetadataStoreFactory,
    ):
        class WorkerRunStoreHandler(logging.Handler):
            def emit(self, record):
                message = self.format(record)
                worker_run_store.log(worker_id, run_id, message)

        # still need the prefix to globally configure logging for all katatachi workers
        self._logger = logging.getLogger(f"katatachi.worker.{worker_id}.{run_id}")
        self._logger.addHandler(WorkerRunStoreHandler())
        self._content_store = content_store
        self._metadata_store = metadata_store_factory.build(worker_id)

    def logger(self) -> logging.Logger:
        return self._logger

    def content_store(self) -> ContentStore:
        return self._content_store

    def metadata_store(self) -> MetadataStore:
        return self._metadata_store


class WorkContextFactory(object):
    def __init__(
        self,
        content_store: ContentStore,
        worker_run_store: WorkerRunStore,
        metadata_store_factory: MetadataStoreFactory,
    ):
        self.content_store = content_store
        self.metadata_store_factory = metadata_store_factory
        self.worker_run_store = worker_run_store

    def build(self, worker_id: str, run_id: str) -> WorkContext:
        return WorkContextImpl(
            worker_id=worker_id,
            run_id=run_id,
            content_store=self.content_store,
            worker_run_store=self.worker_run_store,
            metadata_store_factory=self.metadata_store_factory,
        )
