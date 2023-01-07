from django.apps import AppConfig


class Plugin2Meta:
    verbose_name = "Plugin 2"
    version = "blah_foo"


class Plugin2Config(AppConfig):

    name = "tests.plugins.plugin2"
    PluginMeta = Plugin2Meta
