from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    i18n_loading_dir: str = 'messages'
    i18n_default_package: str = 'msg'
    i18n_default_locale: str = 'default'
    i18n_fallback_locale: str | None = None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings():
    return Settings()
