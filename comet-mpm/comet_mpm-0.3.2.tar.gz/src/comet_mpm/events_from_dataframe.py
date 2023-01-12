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
from typing import List, Optional

import comet_mpm.event


def generate(  # type: ignore[no-untyped-def]
    dataframe,
    prediction_id_column: str,
    feature_columns: Optional[List[str]] = None,
    output_value_column: Optional[str] = None,
    output_probability_column: Optional[str] = None,
):
    return (
        _event(
            row,
            prediction_id_column,
            feature_columns,
            output_value_column,
            output_probability_column,
        )
        for row in dataframe.to_dict(orient="records")
    )


def _event(  # type: ignore[no-untyped-def]
    row,
    prediction_id_column,
    feature_columns,
    output_value_column,
    output_probability_column,
) -> comet_mpm.event.Event:
    prediction_id = str(row[prediction_id_column])
    event = comet_mpm.event.Event(prediction_id=prediction_id)
    if feature_columns is not None:
        event.input_features = {key: row[key] for key in feature_columns}
    if output_value_column is not None:
        event.output_value = row[output_value_column]
    if output_probability_column is not None:
        event.output_probability = row[output_probability_column]

    return event
