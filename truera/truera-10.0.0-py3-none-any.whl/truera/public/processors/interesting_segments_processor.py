from __future__ import annotations

import hashlib
from logging import Logger
from numbers import Number
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple, Union

from google.protobuf.struct_pb2 import \
    Value  # pylint: disable=no-name-in-module
import numpy as np
import pandas as pd

# pylint: disable=no-name-in-module
from truera.protobuf.public.data.filter_pb2 import FilterExpression
from truera.protobuf.public.data.filter_pb2 import FilterExpressionOperator
from truera.protobuf.public.data.filter_pb2 import FilterLeaf
from truera.protobuf.public.data.segment_pb2 import InterestingSegment
from truera.protobuf.public.data.segment_pb2 import Segment
from truera.utils.accuracy_utils import auc_pointwise
from truera.utils.accuracy_utils import classification_accuracy_pointwise
from truera.utils.accuracy_utils import log_loss_score_pointwise
from truera.utils.accuracy_utils import mean_absolute_error_pointwise
from truera.utils.accuracy_utils import mean_squared_error_pointwise
from truera.utils.accuracy_utils import mean_squared_log_error_pointwise
from truera.utils.truera_status import TruEraInvalidArgumentError

EPSILON = 1e-15  # factor to avoid NaNs in HIGH_LOG_LOSS calc

POINTWISE_METRIC_MAP = {
    InterestingSegment.Type.HIGH_MEAN_ABSOLUTE_ERROR:
        mean_absolute_error_pointwise,
    InterestingSegment.Type.HIGH_MEAN_SQUARED_ERROR:
        mean_squared_error_pointwise,
    InterestingSegment.Type.HIGH_MEAN_SQUARED_LOG_ERROR:
        mean_squared_log_error_pointwise,
    InterestingSegment.Type.HIGH_LOG_LOSS:
        log_loss_score_pointwise,
    InterestingSegment.Type.LOW_POINTWISE_AUC:
        auc_pointwise,
    InterestingSegment.Type.LOW_CLASSIFICATION_ACCURACY:
        classification_accuracy_pointwise
}


class InterestingSegmentsProcessor:
    """
    RPC calls covered here:

       GetInterestingSegments(InterestingSegmentsRequest) -> InterestingSegmentsResponse
    """
    _DEFAULT_NUM_SAMPLES = 100

    @staticmethod
    def validate_num_features(num_features: int) -> None:
        if num_features <= 0:
            raise TruEraInvalidArgumentError(f"`num_features` must be > 0!")

    @staticmethod
    def validate_and_get_num_samples(num_samples: int, logger: Logger) -> int:
        if num_samples <= 0:
            logger.info(
                f"`num_samples` is <= 0, setting to default value of {InterestingSegmentsProcessor._DEFAULT_NUM_SAMPLES}"
            )
            return InterestingSegmentsProcessor._DEFAULT_NUM_SAMPLES
        return num_samples

    @staticmethod
    def validate_and_get_pointwise_metrics(
        interesting_segment_type: InterestingSegment.Type,
        all_ys: Sequence[pd.Series],
        all_ys_pred: Sequence[pd.Series],
    ) -> Sequence[pd.Series]:
        if len(all_ys) != len(all_ys_pred) or len(all_ys) == 0:
            raise ValueError(
                "`all_ys` and `all_ys_pred` must be the same length >= 1!"
            )
        ret = []
        for idx in range(len(all_ys)):
            if interesting_segment_type in POINTWISE_METRIC_MAP.keys():
                pointwise_metric_fn = POINTWISE_METRIC_MAP[
                    interesting_segment_type]
                error = pointwise_metric_fn(all_ys[idx], all_ys_pred[idx])
                ret.append(error)
            else:
                raise TruEraInvalidArgumentError(
                    f"Unsupported `interesting_segment_type`: {interesting_segment_type}!"
                )
        ret = [curr - np.mean(curr) for curr in ret]
        return [
            pd.Series(ret[idx], index=all_ys[idx].index)
            for idx in range(len(all_ys))
        ]

    @staticmethod
    def pointwise_metrics_aggregator(
        minimum_size: int = 50,
        size_exponent: float = 0.25
    ) -> Callable[[Sequence[float], Sequence[int]], float]:
        """Returns a pointwise aggregator used in `find_interesting_segments` that computes a size-weighted value mean.

        Args:
            minimum_size: Minimum size of a segment.
            size_exponent: Exponential factor on size of segment. Should be in [0, 1]. A zero value implies the segment size has no effect.

        Returns:
            Callable[[Sequence[float], Sequence[int]], float]:
                Function which takes the sums of the subset of points in question and the sizes of the subset and computes a size-weighted value mean.
        """

        def ret(sums: Sequence[float], szs: Sequence[int]) -> float:
            if any([curr < minimum_size for curr in szs]):
                return -np.inf
            if len(sums) == 1:
                return (sums[0] / szs[0]) * szs[0]**size_exponent
            if len(sums) == 2:
                return ((sums[0] / szs[0]) -
                        (sums[1] / szs[1])) * min(szs)**size_exponent
            raise ValueError(
                "Currently not supporting aggregators for more than two sets!"
            )

        return ret

    @staticmethod
    def find_interesting_segments(
        logger: Logger,
        xs: Sequence[pd.DataFrame],
        pointwise_metrics: Sequence[pd.Series],
        pointwise_metrics_aggregator: Callable[[Sequence[float], Sequence[int]],
                                               float],
        num_features: int,
        num_samples: int,
        random_state: Optional[int] = None
    ) -> pd.DataFrame:
        """Randomly searches for interesting segments in the provided data given by `xs`, `ys`, `ys_pred` that maximize the `f` function subject to being describable by `num_features`.

        Args:
            logger: logger to output to.
            xs: pretransformed xs data.
            pointwise_metrics: metric value for each point we wish to maximize the pointwise_metrics_aggregator of. The ith entry must correspond to the ith entry of `xs`.
            pointwise_metrics_aggregator: function aggregating a subset of the pointwise_metrics to a single float to maximize.
            num_features: number of features to use to describe the segments.
            num_samples: number of random segments to investigate. Defaults to 100.
            random_state: random state for computation. Defaults to None which is unseeded.

        Returns:
            All found segments ranked from most interesting to least along with their corresponding hashed masks.
        """
        np.random.seed(random_state)
        all_features = list(xs[0].columns)
        unique_vals = InterestingSegmentsProcessor._compute_unique_vals(xs[0])
        f_scores = []
        segments = []
        hashed_masks = []
        seen = set()
        for sample_idx in range(num_samples):
            features = np.random.choice(
                all_features,
                size=min(num_features, len(all_features)),
                replace=False
            )
            if tuple(features) in seen:
                continue
            seen.add(tuple(features))
            candidate_masks, candidate_filter, candidate_f_score, valid = InterestingSegmentsProcessor._find_interesting_segment_using_features(
                xs, unique_vals, pointwise_metrics,
                pointwise_metrics_aggregator, features
            )
            if valid:
                logger.info(f"sample = {sample_idx}: {candidate_f_score}")
                f_scores.append(candidate_f_score)
                segments.append(Segment(filter_expression=candidate_filter))
                hashed_masks.append(
                    hashlib.sha256(
                        np.hstack(
                            [curr.to_numpy() for curr in candidate_masks]
                        )
                    ).hexdigest()
                )
            else:
                logger.info("Could not find viable segment!")
        ret = pd.DataFrame.from_dict(
            {
                "f_scores": f_scores,
                "segments": segments,
                "hashed_masks": hashed_masks,
            }
        )
        ret.drop_duplicates(subset=["hashed_masks"], inplace=True)
        ret.sort_values(by="f_scores", ascending=False, inplace=True)
        ret.index = range(ret.shape[0])
        if len(ret) > 0:
            logger.info(f"best f_score = {ret['f_scores'].iloc[0]}")
            logger.debug(f"best filter = {ret['segments'].iloc[0]}")
        return ret

    @staticmethod
    def _find_interesting_segment_using_features(
        xs: Sequence[pd.DataFrame], unique_vals: Mapping[str, Sequence[Any]],
        pointwise_metrics: Sequence[pd.Series],
        pointwise_metrics_aggregator: Callable[[Sequence[float], Sequence[int]],
                                               float], features: Sequence[str]
    ) -> Tuple[Optional[Sequence[pd.Series]], Optional[FilterExpression],
               Optional[float], bool]:
        """Greedily find the best possible segment for the provided data constrained by using exactly the features in `features`.

        Args:
            xs: pretransformed xs data.
            unique_vals: unique values of `xs` to use for segment construction.
            pointwise_metrics: metric value for each point we wish to maximize the pointwise_metrics_aggregator of. The ith entry must correspond to the ith entry of `xs`.
            pointwise_metrics_aggregator: function aggregating a subset of the pointwise_metrics to a single float to maximize.
            features: features to use to construct the segment.

        Returns:
            Tuple[Optional[Sequence[pd.Series]], Optional[FilterExpression], Optional[float], bool]:
                1. Masks determining which xs/ys/ys_pred to use.
                2. `FilterExpression` defining segment.
                3. Score of the segment.
                4. Whether the segment is a valid segment or not.
        """
        xs_orig_indexes = [curr.index.copy() for curr in xs]
        base_expressions = []
        ret_f_score = -np.inf
        for feature in features:
            dtype = xs[0].dtypes[feature]
            best_f_score = -np.inf
            best_masks = None
            if dtype in ["object", "str"]:
                # Categorical feature.
                best_val = ""
                best_negate = None
                total_sums = []
                total_sizes = []
                for curr in pointwise_metrics:
                    total_sums.append(np.sum(curr))
                    total_sizes.append(len(curr))
                for val in unique_vals[feature]:
                    nonnegated_candidate_masks = []
                    nonnegated_candidate_sums = []
                    nonnegated_candidate_sizes = []
                    for idx in range(len(xs)):
                        nonnegated_candidate_mask = xs[idx][feature] == val
                        nonnegated_pointwise_metrics = pointwise_metrics[idx][
                            nonnegated_candidate_mask]
                        nonnegated_candidate_masks.append(
                            nonnegated_candidate_mask
                        )
                        nonnegated_candidate_sums.append(
                            np.sum(nonnegated_pointwise_metrics)
                        )
                        nonnegated_candidate_sizes.append(
                            len(nonnegated_pointwise_metrics)
                        )
                    for negate in [False, True]:
                        candidate_sums = nonnegated_candidate_sums
                        candidate_sizes = nonnegated_candidate_sizes
                        if negate:
                            candidate_sums = [
                                total_sums[idx] - nonnegated_candidate_sums[idx]
                                for idx in range(len(xs))
                            ]
                            candidate_sizes = [
                                total_sizes[idx] -
                                nonnegated_candidate_sizes[idx]
                                for idx in range(len(xs))
                            ]
                        candidate_f_score = pointwise_metrics_aggregator(
                            candidate_sums, candidate_sizes
                        )
                        if best_f_score < candidate_f_score:
                            best_f_score = candidate_f_score
                            best_val = val
                            best_negate = negate
                            best_masks = nonnegated_candidate_masks
                            if negate:
                                best_masks = [
                                    ~curr for curr in nonnegated_candidate_masks
                                ]
                # Create base expression.
                base_expression = InterestingSegmentsProcessor._create_categorical_base_expression(
                    feature, best_val, best_negate
                )
                base_expressions.append(base_expression)
            else:
                # Numerical feature.
                xs_sorted = []
                for idx in range(len(xs)):
                    curr = pd.DataFrame(
                        data={
                            "feature": xs[idx][feature],
                            "pointwise_metrics": pointwise_metrics[idx]
                        },
                        index=xs[idx].index
                    )
                    curr.sort_values(by="feature", inplace=True)
                    curr["pointwise_metrics"] = np.cumsum(
                        curr["pointwise_metrics"]
                    )
                    xs_sorted.append(curr)
                curr_unique_vals = unique_vals[feature]
                best_lo = -1
                best_hi = -1
                for lo_idx, lo in enumerate(curr_unique_vals):
                    for hi_idx in range(lo_idx, len(curr_unique_vals)):
                        hi = curr_unique_vals[hi_idx]
                        candidate_sums = []
                        candidate_sizes = []
                        for curr in xs_sorted:
                            range_lo_idx = np.searchsorted(
                                curr["feature"], lo, side="left"
                            )
                            range_hi_idx = np.searchsorted(
                                curr["feature"], hi, side="right"
                            )
                            hi_cumsum = curr["pointwise_metrics"].iloc[
                                range_hi_idx - 1] if range_hi_idx > 0 else 0
                            lo_cumsum = curr["pointwise_metrics"].iloc[
                                range_lo_idx - 1] if range_lo_idx > 0 else 0
                            candidate_sizes.append(range_hi_idx - range_lo_idx)
                            candidate_sums.append(hi_cumsum - lo_cumsum)
                        candidate_f_score = pointwise_metrics_aggregator(
                            candidate_sums, candidate_sizes
                        )
                        if best_f_score < candidate_f_score:
                            best_f_score = candidate_f_score
                            best_lo = lo
                            best_hi = hi
                if best_f_score > -np.inf:
                    best_masks = [
                        (best_lo <= curr[feature]) & (curr[feature] <= best_hi)
                        for curr in xs
                    ]
                # Create base expression.
                base_expression = InterestingSegmentsProcessor._create_numerical_base_expression(
                    feature, best_lo, best_hi
                )
                base_expressions.append(base_expression)
            if best_masks is None:
                return None, None, None, False
            ret_f_score = best_f_score
            xs = [xs[idx][best_masks[idx]] for idx in range(len(xs))]
            pointwise_metrics = [
                pointwise_metrics[idx][best_masks[idx]]
                for idx in range(len(xs))
            ]
        if len(base_expressions) == 0:
            return None, None, None, False
        ret_masks = []
        for idx in range(len(xs)):
            curr = pd.Series(
                np.zeros(len(xs_orig_indexes[idx]), dtype=bool),
                index=xs_orig_indexes[idx]
            )
            curr[xs[idx].index] = True
            ret_masks.append(curr)
        if len(base_expressions) == 1:
            return ret_masks, base_expressions[0], ret_f_score, True
        ret = base_expressions[0]
        for i in range(1, len(base_expressions)):
            left = ret
            ret = FilterExpression()
            ret.operator = FilterExpressionOperator.FEO_AND
            right = base_expressions[i]
            ret.sub_expressions.extend([left, right])
        return ret_masks, ret, ret_f_score, True

    @staticmethod
    def _create_numerical_base_expression(
        feature: str, lo: Number, hi: Number
    ) -> FilterExpression:
        expression_lo = FilterExpression(
            filter_leaf=FilterLeaf(
                value_type=FilterLeaf.FilterLeafValueType.COLUMN_VALUE,
                column_name=feature,
                filter_type=FilterLeaf.FilterLeafComparisonType.
                GREATER_THAN_EQUAL_TO,
                values=[
                    Value(number_value=lo),
                ]
            )
        )
        expression_hi = FilterExpression(
            filter_leaf=FilterLeaf(
                value_type=FilterLeaf.FilterLeafValueType.COLUMN_VALUE,
                column_name=feature,
                filter_type=FilterLeaf.FilterLeafComparisonType.
                LESS_THAN_EQUAL_TO,
                values=[
                    Value(number_value=hi),
                ]
            )
        )
        return FilterExpression(
            operator=FilterExpressionOperator.FEO_AND,
            sub_expressions=[expression_lo, expression_hi],
        )

    @staticmethod
    def _create_categorical_base_expression(
        feature: str, best_val: str, negate: bool
    ) -> FilterExpression:
        filter_type = FilterLeaf.FilterLeafComparisonType.EQUALS
        if negate:
            filter_type = FilterLeaf.FilterLeafComparisonType.NOT_EQUALS
        return FilterExpression(
            filter_leaf=FilterLeaf(
                value_type=FilterLeaf.FilterLeafValueType.COLUMN_VALUE,
                column_name=feature,
                filter_type=filter_type,
                values=[Value(string_value=best_val)]
            )
        )

    @staticmethod
    def _compute_unique_vals(xs: pd.DataFrame,
                             lim: int = 100) -> Mapping[str, np.ndarray]:
        ret = {}
        for feature in xs.columns:
            unique_vals = xs[feature]
            if unique_vals.dtype in [str, object]:
                unique_vals.fillna("", inplace=True)
            unique_vals = unique_vals.unique()
            ret[feature] = np.sort(xs[feature].unique())
            sz = len(ret[feature])
            if sz > lim:
                idxs = np.floor(np.linspace(0, sz - 1, lim)).astype(np.int64)
                ret[feature] = ret[feature][idxs]
        return ret
