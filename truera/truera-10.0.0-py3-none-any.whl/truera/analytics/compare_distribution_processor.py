from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Iterable, Mapping, Optional, Sequence

from truera.analytics.distance import Distance
from truera.analytics.distance import DistanceComputers
from truera.protobuf.public.aiq.distance_pb2 import \
    DistanceType  # pylint: disable=no-name-in-module


@dataclass
class CompareDistributionOutput:
    score: float
    score_breakdown: Optional[Mapping[str, float]] = None


class CompareDistributionProcessor(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def compare_distributions(
        self,
        distribution1: Iterable[float],
        distribution2: Iterable[float],
        breakdown1: Optional[Mapping[str, Iterable[float]]] = None,
        breakdown2: Optional[Mapping[str, Iterable[float]]] = None,
        metrics: Optional[Sequence[Distance]] = None
    ) -> Mapping[DistanceType, CompareDistributionOutput]:
        output_dict = {}
        if metrics is None:
            metrics = self._get_score_infos()
        for metric in metrics:
            score_key = metric.type_proto
            score_lambda = metric.distance_of_samples_iterable
            score = score_lambda(distribution1, distribution2)
            breakdown_score_map = None
            if breakdown1 is not None and breakdown2 is not None:
                breakdown_score_map = {}
                total_sum = 0
                for breakdown_key in breakdown1:
                    ind_score = score_lambda(
                        breakdown1[breakdown_key], breakdown2[breakdown_key]
                    )
                    breakdown_score_map[breakdown_key] = ind_score
                    total_sum += abs(ind_score)
                if total_sum != 0:
                    for breakdown_key in breakdown_score_map:
                        breakdown_score_map[
                            breakdown_key
                        ] = breakdown_score_map[breakdown_key] / total_sum
            output_dict[score_key] = CompareDistributionOutput(
                score, breakdown_score_map
            )
        return output_dict

    def _get_score_infos(self) -> Iterable[Distance]:
        return [
            DistanceComputers.Numerical.Wasserstein(),
            DistanceComputers.Numerical.DifferenceOfMean(),
            DistanceComputers.Numerical.PopulationStabilityIndex()
        ]
