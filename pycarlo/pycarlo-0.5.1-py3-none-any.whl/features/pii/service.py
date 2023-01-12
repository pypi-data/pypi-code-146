from typing import Optional, Union, Dict

from pycarlo.core import Client
from pycarlo.features.pii import PiiFilteringFailModeType
from pycarlo.features.pii.pii_filterer import PiiActiveFiltersConfig, PiiActiveFilter
from pycarlo.features.pii.queries import GET_PII_PREFERENCES, GET_PII_FILTERS


class PiiService:

    def __init__(self, mc_client: Optional[Client] = None):
        self._mc_client = mc_client or Client()

    def get_pii_filters_config(self) -> Optional[Dict]:
        prefs = self._mc_client(query=GET_PII_PREFERENCES).get_pii_filtering_preferences
        if not prefs.enabled:
            return None

        fail_closed = prefs.fail_mode.upper() == PiiFilteringFailModeType.CLOSE
        pii_filters = self._mc_client(query=GET_PII_FILTERS).get_pii_filters
        if not pii_filters:
            return None

        return PiiActiveFiltersConfig(
            fail_closed=fail_closed,
            active=[
                PiiActiveFilter(
                    name=f.name,
                    pattern=f.pattern
                )
                for f in pii_filters if f.enabled
            ]
        ).to_dict()
