from . import _version
from .plugin import BotTelegramPlugin  # noqa: F401, F403

__version__ = _version.get_versions()['version']
