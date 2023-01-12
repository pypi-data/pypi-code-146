from . import _version
from .plugin import (BotGoogleCalendarPlugin, EventDays,  # noqa: F401, F403
                     EventRecurrence)

__version__ = _version.get_versions()['version']
