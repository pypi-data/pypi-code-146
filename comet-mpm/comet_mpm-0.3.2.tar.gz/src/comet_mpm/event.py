# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

import copy
import dataclasses
from typing import Any, Dict, Optional


@dataclasses.dataclass
class Event:
    """
    This class represents a single event. Events are identified by the
    mandatory prediction_id parameter. Many events can have the same
    prediction_id. The MPM backend merges events with the same prediction_id
    automatically.
    Args:
        prediction_id: The unique prediction ID, could be provided by the
            framework, you or a random unique value could be provided like
            str(uuid4())
        input_features: If provided must be a flat Dictionary where the
            keys are the feature name and the value are native Python
            scalars, int, floats, booleans or strings. For example:
            `{“age”: 42, “income”: 42894.89}`
        output_value: The prediction as a native Python scalar, int,
            float, boolean or string.
        output_probability: If provided, must be a float between 0 and 1
            indicating the confidence of the model in the prediction
    """

    prediction_id: str
    input_features: Optional[Dict[str, Any]] = None
    output_value: Any = None
    output_probability: Any = None

    def to_dictionary(self) -> Dict[str, Any]:
        return copy.deepcopy(self.__dict__)
