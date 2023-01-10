"""Utility functions for converting between SDK args and proto objects."""

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional, cast

from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from rime_sdk.swagger.swagger_client.models import (
    CliconfigDataParams,
    CliconfigEmbeddingInfo,
    CliconfigRankingInfo,
    CliconfigSinglePredictionInfo,
    CliconfigTabularSingleDataInfoParams,
    CliconfigUnstructuredEmbeddingInfo,
    CliconfigUnstructuredSingleDataInfoParams,
    RimeBinSize,
    RimeCustomLoaderArgs,
    RimeDataLocation,
    RimeDataLocationType,
    RimeDataType,
    RimeDeltaLakeArgs,
    RimeModelTask,
    RimeThresholdDirection,
    RimeThresholdInfo,
)


def swagger_is_empty(swagger_val: Any) -> bool:
    """Check if a swagger object is empty."""
    return not bool(swagger_val)


def get_bin_size_swagger(bin_size_str: str) -> RimeBinSize:
    """Get bin size proto from string."""
    years = 0
    months = 0
    seconds = 0
    if bin_size_str == "year":
        years += 1
    elif bin_size_str == "month":
        months += 1
    elif bin_size_str == "week":
        seconds += 7 * 24 * 60 * 60
    elif bin_size_str == "day":
        seconds += 24 * 60 * 60
    elif bin_size_str == "hour":
        seconds += 60 * 60
    else:
        raise ValueError(
            f"Got unknown bin size ({bin_size_str}), "
            f"should be one of: `year`, `month`, `week`, `day`, `hour`"
        )
    return RimeBinSize(years=years, months=months, seconds=seconds)


TYPE_KEY = "enum_type"
PROTO_FIELD_KEY = "proto_field"
PROTO_TYPE_KEY = "proto_type"
LOCATION_TYPE_MAP: Dict[str, Dict] = {
    "data_collector": {TYPE_KEY: RimeDataLocationType.DATA_COLLECTOR},
    "delta_lake": {
        TYPE_KEY: RimeDataLocationType.DELTA_LAKE,
        PROTO_FIELD_KEY: "delta_lake_args",
        PROTO_TYPE_KEY: RimeDeltaLakeArgs,
    },
    "custom_loader": {
        TYPE_KEY: RimeDataLocationType.CUSTOM_LOADER,
        PROTO_FIELD_KEY: "custom_loader_args",
        PROTO_TYPE_KEY: RimeCustomLoaderArgs,
    },
}

DATA_TYPE_TO_PARAMS_MAP: Dict[str, Dict] = {
    RimeDataType.TABULAR: {
        PROTO_FIELD_KEY: "tabular_params",
        PROTO_TYPE_KEY: CliconfigTabularSingleDataInfoParams,
    },
    RimeDataType.NLP: {
        PROTO_FIELD_KEY: "unstructured_params",
        PROTO_TYPE_KEY: CliconfigUnstructuredSingleDataInfoParams,
    },
}

BASE_TYPES = ["str", "float", "int", "bool"]


def _parse_dict_to_ctsdip(obj_dict: dict) -> CliconfigTabularSingleDataInfoParams:
    new_obj = CliconfigTabularSingleDataInfoParams()
    for key, value in obj_dict.items():
        if key == "ranking_info":
            setattr(new_obj, key, parse_dict_to_swagger(value, CliconfigRankingInfo()))
        elif key == "embeddings":
            new_list = []
            for elm in value:
                new_list.append(parse_dict_to_swagger(elm, CliconfigEmbeddingInfo()))
            setattr(new_obj, key, new_list)
        else:
            setattr(new_obj, key, value)
    return new_obj


def _parse_dict_to_cusdip(obj_dict: dict) -> CliconfigUnstructuredSingleDataInfoParams:
    new_obj = CliconfigUnstructuredSingleDataInfoParams()
    for key, value in obj_dict.items():
        if key == "prediction_info":
            setattr(
                new_obj,
                key,
                parse_dict_to_swagger(value, CliconfigSinglePredictionInfo()),
            )
        else:
            new_list = []
            for elm in value:
                new_list.append(
                    parse_dict_to_swagger(elm, CliconfigUnstructuredEmbeddingInfo())
                )
            setattr(new_obj, key, new_list)
    return new_obj


def parse_dict_to_swagger(obj_dict: Optional[Dict], new_obj: Any) -> Any:
    """Parse non-nested dicts into a new object."""
    if obj_dict:
        for key, value in obj_dict.items():
            setattr(new_obj, key, value)
    return new_obj


def location_args_to_data_location_swagger(
    location_type: str,
    location_info: Optional[Dict],
    data_params: Optional[Dict] = None,
    data_type: Optional[str] = None,
) -> RimeDataLocation:
    """Create Data Location object for Firewall Requests."""
    location_keys = set(LOCATION_TYPE_MAP.keys())
    if location_type not in location_keys:
        raise ValueError(
            f"Location type {location_type} must be one of {location_keys}"
        )
    location_enum = LOCATION_TYPE_MAP[location_type][TYPE_KEY]
    data_location = RimeDataLocation(location_type=location_enum)

    proto_field = LOCATION_TYPE_MAP[location_type].get(PROTO_FIELD_KEY, None)
    proto_type = LOCATION_TYPE_MAP[location_type].get(PROTO_TYPE_KEY, None)
    if proto_type is not None and location_info is None:
        raise ValueError(
            "Must specify args for location info if setting location type "
            f"to {location_type}. See documentation for details"
        )

    if proto_field is not None and proto_type is not None:
        location_args_obj = parse_dict_to_swagger(location_info, proto_type())
        setattr(data_location, proto_field, location_args_obj)
    if data_params is None:
        return data_location

    data_location.data_params = get_data_params_swagger(data_params, data_type)
    return data_location


def get_data_params_swagger(
    data_params: Dict, data_type: Optional[str]
) -> CliconfigDataParams:
    """Get data params swagger object from dictionary."""
    if data_type is None:
        raise ValueError("Must specify data type when specifying data params")
    if data_type not in DATA_TYPE_TO_PARAMS_MAP:
        raise ValueError(
            f"Specifying data params for {data_type} is not current supported"
        )
    data_params_sw = CliconfigDataParams()
    proto_field = DATA_TYPE_TO_PARAMS_MAP[data_type].get(PROTO_FIELD_KEY)
    data_proto_field = cast(str, proto_field)
    data_proto_type: Any = DATA_TYPE_TO_PARAMS_MAP[data_type].get(PROTO_TYPE_KEY)
    if data_proto_type == CliconfigTabularSingleDataInfoParams:
        setattr(
            data_params_sw, data_proto_field, _parse_dict_to_ctsdip(data_params),
        )
    elif data_proto_type == CliconfigUnstructuredSingleDataInfoParams:
        setattr(
            data_params_sw, data_proto_field, _parse_dict_to_cusdip(data_params),
        )
    else:
        raise ValueError("bad data_type")
    return data_params_sw


THRESHOLD_INFO_TO_ENUM_MAP = {
    "above": RimeThresholdDirection.ABOVE,
    "below": RimeThresholdDirection.BELOW,
    None: RimeThresholdDirection.UNSPECIFIED,
}


def get_threshold_direction_swagger(direction: Optional[str]) -> str:
    """Get the threshold direction protobuf."""
    _direction = THRESHOLD_INFO_TO_ENUM_MAP.get(direction)
    if _direction is None:
        # TODO: Handle "both" cases
        raise ValueError(
            f"Invalid threshold direction {direction}. Expected 'above' or 'below'."
        )
    return _direction


def get_threshold_info_swagger(metric_threshold_info: dict) -> RimeThresholdInfo:
    """Return the threshold info map."""
    info_copy = deepcopy(metric_threshold_info)
    info_copy["direction"] = get_threshold_direction_swagger(
        metric_threshold_info.get("direction")
    )
    return parse_dict_to_swagger(info_copy, RimeThresholdInfo())


def threshold_infos_to_map(
    threshold_infos: List[RimeThresholdInfo],
) -> Dict[str, RimeThresholdInfo]:
    """Return map of metric name to RimeThresholdInfo."""
    threshold_info_map = {}
    for threshold_info in threshold_infos:
        info_without_metric = RimeThresholdInfo(
            direction=threshold_info.direction,
            low=threshold_info.low,
            medium=threshold_info.medium,
            high=threshold_info.high,
            disabled=threshold_info.disabled,
        )
        threshold_info_map[threshold_info.metric_name] = info_without_metric
    return threshold_info_map


DEFAULT_THRESHOLD_INFO_KEY_ORDER = list(RimeThresholdInfo.swagger_types.keys())
# Put metric_name at the beginning
DEFAULT_THRESHOLD_INFO_KEY_ORDER.remove("metric_name")
DEFAULT_THRESHOLD_INFO_KEY_ORDER = ["metric_name"] + DEFAULT_THRESHOLD_INFO_KEY_ORDER


def get_data_type_enum_swagger(data_type: str) -> str:
    """Get data type enum value from string."""
    if data_type == "tabular":
        return RimeDataType.TABULAR
    elif data_type == "nlp":
        return RimeDataType.NLP
    elif data_type == "images":
        return RimeDataType.IMAGES
    else:
        raise ValueError(
            f"Got unknown data type ({data_type}), "
            f"should be one of: `tabular`, `nlp`, `images`"
        )


def get_model_task_enum_swagger(model_task: str) -> str:
    """Get the model task enum from string."""
    if model_task == "Binary Classification":
        return RimeModelTask.BINARY_CLASSIFICATION
    elif model_task == "Multi-class Classification":
        return RimeModelTask.MULTICLASS_CLASSIFICATION
    elif model_task == "Regression":
        return RimeModelTask.REGRESSION
    elif model_task == "Ranking":
        return RimeModelTask.RANKING
    elif model_task == "Named Entity Recognition":
        return RimeModelTask.NAMED_ENTITY_RECOGNITION
    elif model_task == "Natural Language Inference":
        return RimeModelTask.NATURAL_LANGUAGE_INFERENCE
    elif model_task == "Text Classification":
        return RimeModelTask.TEXT_CLASSIFICATION
    elif model_task == "Object Detection":
        return RimeModelTask.OBJECT_DETECTION
    elif model_task == "Image Classification":
        return RimeModelTask.IMAGE_CLASSIFICATION
    else:
        raise ValueError(f"Got unknown model task ({model_task}).")


def valid_model_task_for_data_type(model_task: str, data_type: str) -> bool:
    """Check if the model task is compatible with the data type."""
    if data_type == RimeDataType.TABULAR:
        return model_task in [
            RimeModelTask.BINARY_CLASSIFICATION,
            RimeModelTask.MULTICLASS_CLASSIFICATION,
            RimeModelTask.RANKING,
            RimeModelTask.REGRESSION,
        ]
    elif data_type == RimeDataType.NLP:
        return model_task in [
            RimeModelTask.NAMED_ENTITY_RECOGNITION,
            RimeModelTask.NATURAL_LANGUAGE_INFERENCE,
            RimeModelTask.TEXT_CLASSIFICATION,
        ]
    elif data_type == RimeDataType.IMAGES:
        return model_task in [
            RimeModelTask.OBJECT_DETECTION,
            RimeModelTask.IMAGE_CLASSIFICATION,
        ]
    else:
        raise ValueError(f"Invalid data type {data_type}.")


def serialize_datetime_to_proto_timestamp(date: datetime) -> Dict:
    """Convert datetime to swagger compatible grpc timestamp."""
    timestamp = Timestamp()
    timestamp.FromDatetime(date)
    # Swagger serialize datetime to iso8601 format, convert to
    # protobuf compatible serialization
    return MessageToDict(timestamp)


def get_swagger_data_type_enum(data_type: str) -> str:
    """Get RimeDataType enum value from string."""
    if data_type == "tabular":
        return RimeDataType.TABULAR
    elif data_type == "nlp":
        return RimeDataType.NLP
    elif data_type == "images":
        return RimeDataType.IMAGES
    else:
        raise ValueError(
            f"Got unknown data type ({data_type}), "
            f"should be one of: `tabular`, `nlp`, `images`"
        )
