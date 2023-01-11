import numpy as np
import pandas as pd

from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    FloatTable  # pylint: disable=no-name-in-module
from truera.public.feature_influence_constants import QOI_TO_SCORE_TYPE
from truera.public.feature_influence_constants import SCORE_TYPE_TO_QOI
from truera.utils.truera_status import TruEraInternalError

PREDICTION_CACHE_COLUMN = "score"


def GetScoreTypeFromQuantityOfInterest(quantity_of_interest):
    if quantity_of_interest not in QOI_TO_SCORE_TYPE:
        raise TruEraInternalError(
            f"Quantity of Interest {quantity_of_interest} is not mapped to a score type."
        )
    return QOI_TO_SCORE_TYPE[quantity_of_interest]


def GetQuantityOfInterestFromScoreType(score_type):
    if score_type not in SCORE_TYPE_TO_QOI:
        raise TruEraInternalError(
            f"Score type {score_type} is not mapped to a Quantity of Interest."
        )
    return SCORE_TYPE_TO_QOI[score_type]


def convert_dataframe_to_float_table(df: pd.DataFrame, ft: FloatTable) -> None:
    ft.row_labels.extend(np.array(df.index).astype(str))
    for col in list(df.columns):
        ft.column_value_map[col].values.extend(df[col].to_numpy().ravel())
