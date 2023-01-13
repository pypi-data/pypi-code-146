from datetime import datetime
from typing import Optional

from pydantic import HttpUrl, PositiveInt, constr, validate_arguments

from gpn_clients.core.config import NSIConfig, nsi_config
from gpn_clients.models.base_nsi_api import AbstractTimeSeries
from gpn_clients.utils.urls import URLGenerator


class NSITimeSeries(AbstractTimeSeries):
    path: str = "TimeSeries"

    def __init__(self, config: NSIConfig = nsi_config) -> None:
        self._config = config
        self._url_generator = URLGenerator(
            host=config.HOST,
            port=config.PORT,
        )

    @validate_arguments
    def get_for_timerange(
            self,
            tag_name: constr(min_length=1),
            start: datetime,
            finish: Optional[datetime] = None,
    ) -> HttpUrl:
        timerange_path: str = "raw/tag/range"
        finish = finish or datetime.utcnow()
        get_params = {
            "tag": tag_name,
            "from": start.isoformat(),
            "to": finish.isoformat(),
        }
        return self._url_generator.get_full_url_with_get_params(
            timerange_path,
            get_params=get_params,
        )

    @validate_arguments
    def get_for_tail(self, tag_name: constr(min_length=1), tail_size: PositiveInt) -> HttpUrl:
        tail_path: str = "raw/tag/points"
        get_params = {
            "tag": tag_name,
        }
        return self._url_generator.get_full_url_with_get_params(
            tail_path, str(tail_size),
            get_params=get_params,
        )
