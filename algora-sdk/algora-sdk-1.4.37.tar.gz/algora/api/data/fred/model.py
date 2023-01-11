from datetime import date
from typing import Optional

from pydantic import Field, validator

from algora.common.base import Base
from algora.common.config import EnvironmentConfig

config = EnvironmentConfig()


class FredQuery(Base):
    series_id: str
    api_key: str = Field(default=config.auth_config.fred_api_key, init=False)
    file_type: str = Field(default='json')
    observation_start: Optional[date] = None
    observation_end: Optional[date] = None

    @validator("observation_start")
    def observation_start_to_string(cls, d):
        # necessary for serialization
        return d.isoformat()

    @validator("observation_end")
    def observation_end_to_string(cls, d):
        # necessary for serialization
        return d.isoformat()
