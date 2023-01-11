from typing import NamedTuple


class BiasResult(NamedTuple):
    segment1_name: str
    segment2_name: str
    aggregate_metric: float
    segment1_metric: float
    segment2_metric: float
    favored_segment: str
    metric_name: str
    result_type: int  # intelligence_service_pb2.BiasResult.BiasResultType
    error_message: str = ''

    def __str__(self) -> str:
        bias_str = "BiasResult:"
        for k, v in self._asdict().items():  # pylint: disable=no-member
            bias_str += f"\n\t{k}: {v}"
        return bias_str

    def __repr__(self) -> str:
        return str(self)


#TODO(divya) - support bias metrics for local explainer
