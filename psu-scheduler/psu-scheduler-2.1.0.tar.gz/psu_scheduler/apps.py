from django.apps import AppConfig
from django.conf import settings
from psu_base.classes.Log import Log

log = Log()

# Default settings
_DEFAULTS = {
    'SCHEDULER_PUBLIC_URLS': ['.*/scheduler/run', '.*/scheduler/aws/run', '.*/scheduled/.*'],
    'SCHEDULER_MAX_RECORD_AGE': 30,
    # Admin Menu Items
    'PSU_SCHEDULER_ADMIN_LINKS': [
        {
            'url': "scheduler:jobs", 'label': "Scheduled Jobs", 'icon': "fa-clock-o",
            'authorities': "~PowerUser"
        },
        {
            'url': "scheduler:endpoints", 'label': "Schedule-able Endpoints", 'icon': "fa-link",
            'authorities': "~PowerUser"
        },
    ]
}


class PsuschedulerConfig(AppConfig):
    name = 'psu_scheduler'

    def ready(self):
        # Assign default setting values
        log.debug("Setting default settings for PSU_scheduler")
        for key, value in _DEFAULTS.items():
            try:
                getattr(settings, key)
            except AttributeError:
                setattr(settings, key, value)
            # Suppress errors from DJANGO_SETTINGS_MODULE not being set
            except ImportError as ee:
                log.debug(f"Error importing {key}: {ee}")
