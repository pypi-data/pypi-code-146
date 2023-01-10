from remotemanager.serialisation.serialyaml import serialyaml
from remotemanager.serialisation.serialjson import serialjson

__all__ = ['serialyaml', 'serialjson']

try:
    from remotemanager.serialisation.serialdill import serialdill  # noqa: F401
    __all__.append('serialdill')
except ImportError:
    pass

try:
    from remotemanager.serialisation.serialjsonpickle import serialjsonpickle  # noqa: F401, E501
    __all__.append('serialjsonpickle')
except ImportError:
    pass
