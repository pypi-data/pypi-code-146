from django.conf import settings
from psu_base.classes.Log import Log

log = Log()

__version__ = "3.1.1"

__all__ = []

# Default settings
_DEFAULTS = {
    # Admin Menu Items
    "PSU_UPLOAD_ADMIN_LINKS": [
        # {
        #     'url': "upload:upload_index", 'label': "Manage Uploads", 'icon': "fa-whatever",
        #     'authorities': "admin"
        # },
    ]
}

# Assign default setting values
log.debug("Setting default settings for PSU_UPLOAD")
for key, value in list(_DEFAULTS.items()):
    try:
        getattr(settings, key)
    except AttributeError:
        setattr(settings, key, value)
    # Suppress errors from DJANGO_SETTINGS_MODULE not being set
    except ImportError as ee:
        log.debug(f"Error importing {key}: {ee}")
