
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


def setup_settings(settings, is_prod, **kwargs):

    if 'ordered_model' not in settings['INSTALLED_APPS']:
        settings['INSTALLED_APPS'] += ['ordered_model']

    settings['STYLESHEETS'] += ['slider/slideshow.css']

    settings['STATIC_APPS'] += [
        app for app in [
            'slick',
            'fancybox',
        ]
    ]


class SliderConfig(AppConfig):
    name = 'slider'
    verbose_name = _("Slider")


default_app_config = 'slider.SliderConfig'
