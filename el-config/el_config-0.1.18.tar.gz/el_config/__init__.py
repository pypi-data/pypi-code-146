# -*- coding: utf-8 -*-

try:
    from el_config.config_base import ConfigBase
    from el_config.__version__ import __version__
except ImportError:
    from .config_base import ConfigBase
    from .__version__ import __version__
