import numpy as np
from scipy.special import expit as scipy_expit
from scipy.special import logit as scipy_logit

from truera.protobuf.public.qoi_pb2 import \
    QuantityOfInterest  # pylint: disable=no-name-in-module
from truera.utils.truera_status import TruEraInternalError

CONVERTABLE_SCORE_TYPES = (
    QuantityOfInterest.PROBITS_SCORE, QuantityOfInterest.LOGITS_SCORE
)


def convert_prediction_scores(
    source_score_type: QuantityOfInterest,
    target_score_type: QuantityOfInterest, prediction_values: np.ndarray
) -> np.ndarray:
    if not (
        source_score_type in CONVERTABLE_SCORE_TYPES and
        target_score_type in CONVERTABLE_SCORE_TYPES
    ):
        raise TruEraInternalError(
            f"Cannot convert between {QuantityOfInterest.Name(source_score_type)} and {QuantityOfInterest.Name(target_score_type)} score types!"
        )

    if source_score_type == target_score_type:
        return prediction_values

    if target_score_type == QuantityOfInterest.LOGITS_SCORE:
        return scipy_logit(prediction_values)
    else:
        return scipy_expit(prediction_values)
