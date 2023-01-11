from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_service import SyncService
from truera.rnn.general.utils.strings import Printable


class ArtifactsContainer(Printable, object):
    """
    Convenience class to keep track both of a artifact locator and a sync client to retrieve the
    artifact.
    """

    def __init__(self, cache_client: SyncService, locator: Locator):
        self.cache_client = cache_client
        self.locator = locator
        self.cache_path = cache_client.get_cache_path(self.locator)

    def get_path(self) -> str:
        return self.cache_path
