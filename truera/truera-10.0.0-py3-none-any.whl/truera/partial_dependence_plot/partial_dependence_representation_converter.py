from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

import numpy as np

from truera.protobuf.public.aiq.intelligence_service_pb2 import \
    PartialDependencePlotResponse  # pylint: disable=no-name-in-module
from truera.protobuf.public.modelrunner.cache_entries_pb2 import \
    PartialDependenceCache  # pylint: disable=no-name-in-module
from truera.utils.data_utils import get_list_from_value_list


def convert_PartialDependenceCache_to_tuple(
    proto: PartialDependenceCache,
    get_feature_special_values_func: Optional[Callable[[str],
                                                       Optional[Sequence[Any]]]
                                             ] = None
) -> Tuple[Sequence[str], Mapping[str, Sequence], Mapping[str, Sequence]]:
    response_proto = convert_PartialDependenceCache_to_PartialDependencePlotResponse(
        proto, get_feature_special_values_func
    )
    return convert_PartialDependencePlotResponse_to_tuple(response_proto)


def convert_PartialDependenceCache_to_PartialDependencePlotResponse(
    proto: PartialDependenceCache,
    get_feature_special_values_func: Optional[Callable[[str],
                                                       Optional[Sequence[Any]]]
                                             ] = None
) -> PartialDependencePlotResponse:
    ret = PartialDependencePlotResponse()
    ret.prefeatures.extend(proto.prefeatures)
    for prefeature in proto.prefeatures:
        special_values = None
        if get_feature_special_values_func is not None:
            special_values = get_feature_special_values_func(prefeature)
        if special_values:
            xs = proto.xs[prefeature]
            ys = np.array(proto.ys[prefeature].values)
            if len(xs.floats.values) > 0:
                xs_type = "floats"
            elif len(xs.integers.values) > 0:
                xs_type = "integers"
            else:
                xs_type = "strings"
            special_values = np.array(special_values)
            xs = np.array(getattr(xs, xs_type).values)
            is_special_value = np.isin(xs, special_values)
            ret_xs = list(xs[~is_special_value])
            ret_ys = list(ys[~is_special_value])
            ret_special_values_xs = list(xs[is_special_value])
            ret_special_values_ys = list(ys[is_special_value])
            is_seen_special_value = np.isin(special_values, xs)
            num_unseen_special_values = len(is_seen_special_value
                                           ) - np.sum(is_seen_special_value)
            if num_unseen_special_values > 0:
                ret_special_values_xs.extend(
                    list(special_values[~is_seen_special_value])
                )
                ret_special_values_ys.extend(
                    num_unseen_special_values * [np.nan]
                )
            getattr(ret.xs[prefeature], xs_type).values.extend(ret_xs)
            ret.ys[prefeature].values.extend(ret_ys)
            getattr(ret.special_values_xs[prefeature],
                    xs_type).values.extend(ret_special_values_xs)
            ret.special_values_ys[prefeature].values.extend(
                ret_special_values_ys
            )
        else:
            ret.xs[prefeature].CopyFrom(proto.xs[prefeature])
            ret.ys[prefeature].CopyFrom(proto.ys[prefeature])
    return ret


def convert_PartialDependencePlotResponse_to_tuple(
    proto: PartialDependencePlotResponse
) -> Tuple[Sequence[str], Mapping[str, Sequence], Mapping[str, Sequence]]:
    prefeatures = list(proto.prefeatures)
    xs = {}
    ys = {}
    for prefeature in prefeatures:
        xs[prefeature] = get_list_from_value_list(proto.xs[prefeature])
        ys[prefeature] = list(proto.ys[prefeature].values)
        if prefeature in proto.special_values_xs:
            xs[prefeature] += get_list_from_value_list(
                proto.special_values_xs[prefeature]
            )
            ys[prefeature] += list(proto.special_values_ys[prefeature].values)
    return prefeatures, xs, ys
