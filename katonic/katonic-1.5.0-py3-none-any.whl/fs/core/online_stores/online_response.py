#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd


class OnlineResponse:
    """
    Defines a online response in Kfs.
    """

    def __init__(
        self,
        online_response: List[Tuple[Optional[datetime], Optional[Dict[str, Any]], Optional[Dict[str, Any]]]],
        requested_features: List[str]
    ):
        """
        Construct a native online response from its Dictionary version.

        Args:
        online_response: GetOnlineResponse object to construct from.
        """
        self.online_response = online_response
        self.requested_features = requested_features

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts GetOnlineFeaturesResponse features into a dictionary form.
        List[Tuple[Optional[datetime], Optional[Dict[str, Any]]]]
        """
        result: Dict[str, List[Any]] = {k: list()
                                        for k in self.requested_features}

        for row in self.online_response:
            ts, data, entity_data = row
            for k, v in entity_data.items():
                entity_key = k
                entity_val = v
            for feature_name, feature_values in data.items():
                result[feature_name].append(feature_values)
            result[entity_key].append(entity_val)

        return result

    def to_df(self) -> pd.DataFrame:
        """
        Converts GetOnlineFeaturesResponse features into Panda dataframe form.
        """

        return pd.DataFrame(self.to_dict())
