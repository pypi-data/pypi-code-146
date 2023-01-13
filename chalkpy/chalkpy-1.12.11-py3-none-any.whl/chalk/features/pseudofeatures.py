from datetime import datetime

from chalk.features.feature_field import Feature

__all__ = [
    "CHALK_TS_FEATURE",
    "ID_FEATURE",
    "OBSERVED_AT_FEATURE",
    "REPLACED_OBSERVED_AT_FEATURE",
    "PSEUDOFEATURES",
    "PSEUDONAMESPACE",
]

PSEUDONAMESPACE = "__chalk__"

CHALK_TS_FEATURE = Feature(
    name="CHALK_TS",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
)
ID_FEATURE = Feature(name="__id__", namespace=PSEUDONAMESPACE, typ=str, max_staleness=None, etl_offline_to_online=False)
OBSERVED_AT_FEATURE = Feature(
    name="__observed_at__", namespace=PSEUDONAMESPACE, typ=datetime, max_staleness=None, etl_offline_to_online=False
)
REPLACED_OBSERVED_AT_FEATURE = Feature(
    name="__replaced_observed_at__",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
)

PSEUDOFEATURES = [CHALK_TS_FEATURE, ID_FEATURE, OBSERVED_AT_FEATURE, REPLACED_OBSERVED_AT_FEATURE]
