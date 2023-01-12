
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    settings['INSTALLED_APPS'] += [
        app for app in [
            'djmail'
        ] if app not in settings['INSTALLED_APPS']
    ]


class OrdersConfig(AppConfig):
    name = 'orders'
    verbose_name = _("Orders")


default_app_config = 'orders.OrdersConfig'
