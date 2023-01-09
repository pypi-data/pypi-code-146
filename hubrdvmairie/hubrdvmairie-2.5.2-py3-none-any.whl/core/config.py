import logging
from functools import lru_cache
from typing import Set

from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    api_prefix: str = "/api"
    project_name: str = "HUB RDV"

    logging_level: int = logging.DEBUG if debug else logging.INFO
    loggers: Set[str] = {"uvicorn.asgi", "uvicorn.access"}

    editors_list = []
    meeting_point_list = []
    ws_use_rates = {}

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
