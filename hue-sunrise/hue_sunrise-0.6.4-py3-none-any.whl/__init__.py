from __future__ import annotations

import json
import logging
import logging.config
import os
from dataclasses import asdict, dataclass
from pathlib import Path

import appdirs

CONFIG_DIR = Path(appdirs.user_config_dir("hue-sunrise"))
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
BASE_CONFIG_FILE = CONFIG_DIR / "base-config.json"

LOG_DIR = Path(appdirs.user_log_dir())
LOG_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = LOG_DIR / "hue-sunrise.log"


@dataclass
class BaseConfig:
    config_file: Path
    log_file: Path

    def dump(self) -> None:
        with open(BASE_CONFIG_FILE, "w") as fp:
            d = asdict(self)
            d = {
                k: v if not isinstance(v, Path) else str(v)
                for k, v in d.items()
            }
            json.dump(d, fp, indent=2)

    @classmethod
    def default(cls) -> BaseConfig:
        return BaseConfig(
            config_file=CONFIG_DIR / "config.json",
            log_file=LOG_FILE,
        )

    @classmethod
    def from_file(cls) -> BaseConfig:
        if not BASE_CONFIG_FILE.exists():
            cls.default().dump()

        with open(BASE_CONFIG_FILE, "r") as fp:
            raw: dict[str, str] = json.load(fp)

        return BaseConfig(
            config_file=Path(
                os.environ.get("HS_CONFIG_PATH", raw["config_file"]),
            ),
            log_file=Path(os.environ.get("HS_LOG_PATH", raw["log_file"])),
        )


@dataclass
class Config:
    bridge_ip_address: str | None
    bridge_username: str | None
    lights: list[str]
    total_scene_length_min: int
    afterglow_length_min: int
    config_file: Path
    log_file: Path

    def dump(self) -> None:
        with open(self.config_file, "w") as fp:
            d = asdict(self)
            d = {
                k: v if not isinstance(v, Path) else str(v)
                for k, v in d.items()
            }
            json.dump(d, fp, indent=2)

    def reset(self) -> None:
        self.config_file.unlink()

    @classmethod
    def default(cls, config_file: Path, log_file: Path) -> Config:
        return Config(
            bridge_ip_address=None,
            bridge_username=None,
            lights=[],
            total_scene_length_min=15,
            afterglow_length_min=15,
            config_file=config_file,
            log_file=log_file,
        )

    @classmethod
    def from_file(cls) -> Config:
        base_config = BaseConfig.from_file()
        config_file = base_config.config_file
        log_file = base_config.log_file

        if config_file.exists():
            with open(config_file, "r") as fp:
                raw: dict[str, str | list[str] | None] = json.load(fp)

            bridge_ip_address = raw["bridge_ip_address"]
            bridge_username = raw["bridge_username"]
            lights = raw["lights"]
            total_scene_length_min = raw["total_scene_length_min"]
            afterglow_length_min = raw["afterglow_length_min"]

            if bridge_ip_address is not None:
                assert isinstance(bridge_ip_address, str)
            if bridge_username is not None:
                assert isinstance(bridge_username, str)
            assert isinstance(lights, list)
            assert isinstance(total_scene_length_min, int)
            assert isinstance(afterglow_length_min, int)

            config = Config(
                bridge_ip_address=bridge_ip_address,
                bridge_username=bridge_username,
                lights=lights,
                total_scene_length_min=total_scene_length_min,
                afterglow_length_min=afterglow_length_min,
                config_file=config_file,
                log_file=log_file,
            )
        else:
            config = cls.default(config_file=config_file, log_file=log_file)
            config.dump()

        return config

    def set_ip(self, ip: str) -> None:
        self.bridge_ip_address = ip
        self.dump()

    def set_username(self, username: str) -> None:
        self.bridge_username = username
        self.dump()

    def set_lights(self, lights: list[str]) -> None:
        self.lights = lights
        self.dump()

    def set_total_scene_length_min(self, total_scene_length_min: int) -> None:
        self.total_scene_length_min = total_scene_length_min
        self.dump()

    def set_afterglow_length_min(self, afterglow_length_min: int) -> None:
        self.afterglow_length_min = afterglow_length_min
        self.dump()


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "file": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": str(BaseConfig.from_file().log_file),
                "when": "W0",  # Monday
                "backupCount": 1,
            },
            "stream": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "": {
                "handlers": ["file", "stream"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
)
logger = logging.getLogger(__name__)
