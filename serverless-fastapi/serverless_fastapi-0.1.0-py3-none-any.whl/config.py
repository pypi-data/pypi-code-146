from pydantic import BaseSettings, Field, BaseConfig


class Settings(BaseSettings):
    """Settings class"""

    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    class Config(BaseConfig):
        env_file = ".env"


env = Settings()
