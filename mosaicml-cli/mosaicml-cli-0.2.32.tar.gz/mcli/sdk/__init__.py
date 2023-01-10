"""Primary import target for the Python API"""

# pylint: disable=useless-import-alias
from mcli.cli.m_init.m_init import initialize as initialize
from mcli.cli.m_set_unset.api_key import set_api_key as set_api_key
from mcli.config import FeatureFlag, MCLIConfig

if MCLIConfig.load_config(safe=True).feature_enabled(FeatureFlag.USE_MCLOUD):
    from mcli.api.cluster import *
    from mcli.api.runs import *
    from mcli.api.secrets import *
else:
    from mcli.api.kube.runs import *
