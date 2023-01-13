from typing import Literal

from pydantic import HttpUrl, PositiveInt, constr, validate_arguments

from gpn_clients.core.config import NSIConfig, nsi_config
from gpn_clients.models.base_nsi_api import AbstractModelsML
from gpn_clients.utils.urls import URLGenerator


class NSIModelsML(AbstractModelsML):
    path: str = "Models"

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

    @validate_arguments
    def get_binary_view(self, id_: PositiveInt) -> HttpUrl:
        binary_view_path: str = "binary"
        return self._url_generator.get_full_url(self.path, str(id_), binary_view_path)

    @validate_arguments
    def get_info_for_name(self, model_name: constr(min_length=1)) -> HttpUrl:
        model_path: str = "info/name"
        get_params = {"name": model_name}
        return self._url_generator.get_full_url_with_get_params(
            model_path,
            get_params=get_params,
        )

    @validate_arguments
    def get_ml_data_for_tag(
            self,
            tag_name: constr(min_length=1),
            input_function: Literal["predict", "train", "calc", "calc"],
    ) -> HttpUrl:
        ml_data_path: str = "data/name"
        get_params = {"name": tag_name}
        return self._url_generator.get_full_url_with_get_params(
            ml_data_path, input_function,
            get_params=get_params,
        )
