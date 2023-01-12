from django.apps import AppConfig
from django.conf import settings

from . import app_settings as defaults

# Set some app default settings
for name in dir(defaults):
    if name.isupper() and not hasattr(settings, name):
        setattr(settings, name, getattr(defaults, name))


class NEMORatesConfig(AppConfig):
    name = "NEMO_billing.rates"
    verbose_name = "Rates"

    def ready(self):
        # Remove the rates customization coming from regular NEMO since we have our own
        from NEMO.views.customization import CustomizationBase

        del CustomizationBase._instances["rates"]


default_app_config = "NEMO_billing.rates.NEMORatesConfig"
