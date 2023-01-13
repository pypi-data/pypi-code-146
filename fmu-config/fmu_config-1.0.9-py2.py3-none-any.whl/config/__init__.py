"""Top-level package for fmu_config"""

try:
    from ._theversion import version

    __version__ = version
except ImportError:
    __version__ = "0.0.0"


from .configparserfmu import ConfigParserFMU  # noqa
