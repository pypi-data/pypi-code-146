import os


class SettingsContainer:

    def __init__(self):
        self.settings = {}

    def __getitem__(self, key):
        return self.settings[key]

    def __setitem__(self, key, value):
        self.settings[key] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f'setting {name} does not exist')

    def get(self, key, default=None):
        return self.settings.get(key, default)


def env(key):
    return os.environ[key]


def load_settings():
    settings = __import__('settings')
    res = SettingsContainer()
    for key in dir(settings):
        if not key.startswith('_'):
            value = getattr(settings, key)
            res[key] = value
    return res


settings = load_settings()
