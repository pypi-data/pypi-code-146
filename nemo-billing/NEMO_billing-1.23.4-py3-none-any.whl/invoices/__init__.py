from django.apps import AppConfig

from . import app_settings as defaults
from django.conf import settings

# Set some app default settings
for name in dir(defaults):
    if name.isupper() and not hasattr(settings, name):
        setattr(settings, name, getattr(defaults, name))


class NEMOInvoicesConfig(AppConfig):
    name = "NEMO_billing.invoices"
    verbose_name = "Invoices"


default_app_config = "NEMO_billing.invoices.NEMOInvoicesConfig"
