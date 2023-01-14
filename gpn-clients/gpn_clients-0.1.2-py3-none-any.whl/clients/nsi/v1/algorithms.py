from pydantic import HttpUrl, PositiveInt, validate_arguments

from gpn_clients.core.config import NSIConfig, nsi_config
from gpn_clients.models.base_nsi_api import AbstractAlgorithms
from gpn_clients.utils.urls import URLGenerator


class NSIAlgorithms(AbstractAlgorithms):
    path: str = "Algorithms"

    def __init__(self, config: NSIConfig = nsi_config) -> None:
        self._config = config
        self._url_generator = URLGenerator(
            host=config.HOST,
            port=config.PORT,
        )

    def get_all(self) -> HttpUrl:
        return self._url_generator.get_full_url(self.path)

    @validate_arguments
    def get_by_id(self, id_: PositiveInt) -> HttpUrl:
        return self._url_generator.get_full_url(self.path, str(id_))
