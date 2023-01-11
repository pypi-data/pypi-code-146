from typing import Optional, Sequence

from truera.client.client_utils import \
    get_explanation_algorithm_type_from_string
from truera.client.client_utils import get_qoi_from_string
from truera.protobuf.public.common import schema_pb2 as schema_pb
from truera.protobuf.public.data_service import \
    data_service_messages_pb2 as ds_messages_pb


def create_materialized_output_file(
    file_type: ds_messages_pb.MaterializedOutputFile.MaterializedFileType,
    *,
    column_names=[],
    skip_columns=[],
    upstream_input_rowset_id=""
):
    to_ret = ds_messages_pb.MaterializedOutputFile(
        type=file_type,
        columns=ds_messages_pb.ProjectionColumnCollection(),
        input_rowset_id=upstream_input_rowset_id
    )

    if column_names:
        for name in column_names:
            to_ret.columns.column_metadata.append(
                schema_pb.ColumnDetails(name=name)
            )
    else:
        for name in skip_columns:
            to_ret.columns.colummns_to_skip.append(name)

    return to_ret


def validate_column_input(column_input):
    if column_input is None:
        return None
    if not isinstance(column_input, (list, tuple, set, str)):
        raise TypeError(
            f"Invalid Column Input Type. Must provide sequence of column names or a single column name. Recieved input {column_input} of type {type(column_input)}"
        )
    return [column_input] if isinstance(column_input, str) else column_input


class ColumnInfo:

    def __init__(
        self,
        *,
        pre: Optional[Sequence[str]] = None,
        post: Optional[Sequence[str]] = None,
        label: Optional[Sequence[str]] = None,
        prediction: Optional[Sequence[str]] = None,
        feature_influences: Optional[Sequence[str]] = None,
        extra: Optional[Sequence[str]] = None,
        pre_skip: Optional[Sequence[str]] = None,
        post_skip: Optional[Sequence[str]] = None,
        extra_skip: Optional[Sequence[str]] = None,
        id_column: Optional[Sequence[str]] = None,
        timestamp_column: Optional[Sequence[str]] = None
    ):
        self.pre = validate_column_input(pre)
        self.pre_skip = validate_column_input(pre_skip)
        self.post = validate_column_input(post)
        self.post_skip = validate_column_input(post_skip)
        self.extra = validate_column_input(extra)
        self.extra_skip = validate_column_input(extra_skip)

        self.prediction = validate_column_input(prediction)
        self.feature_influences = validate_column_input(feature_influences)
        self.label = validate_column_input(label)
        self.id_column = validate_column_input(id_column)
        self.timestamp_column = validate_column_input(timestamp_column)

    #pylint: disable=no-member
    def get_projections(self):
        projections = []

        if self.pre is not None or self.pre_skip is not None:
            projections.append(
                create_materialized_output_file(
                    ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
                    MFT_PRETRANSFORM,
                    column_names=self.pre or [],
                    skip_columns=self.pre_skip or []
                )
            )
        if self.post is not None or self.post_skip is not None:
            projections.append(
                create_materialized_output_file(
                    ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
                    MFT_POSTTRANSFORM,
                    column_names=self.post or [],
                    skip_columns=self.post_skip or []
                )
            )
        if self.extra is not None or self.extra_skip is not None:
            projections.append(
                create_materialized_output_file(
                    ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
                    MFT_EXTRA,
                    column_names=self.extra or [],
                    skip_columns=self.extra_skip or []
                )
            )
        if self.label:
            projections.append(
                create_materialized_output_file(
                    ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
                    MFT_LABEL,
                    column_names=self.label
                )
            )
        if self.prediction:
            projections.append(
                create_materialized_output_file(
                    ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
                    MFT_PREDICTIONCACHE,
                    column_names=self.prediction
                )
            )

        if self.feature_influences:
            projections.append(
                create_materialized_output_file(
                    ds_messages_pb.MaterializedOutputFile.MaterializedFileType.
                    MFT_EXPLANATIONCACHE,
                    column_names=self.feature_influences
                )
            )

        return projections

    def get_system_column_details(self):
        if self.id_column and len(self.id_column) > 1:
            self.logger.warning(
                f"Warning: more then one id column are specified, only first will be used!"
            )
        if self.timestamp_column and len(self.timestamp_column) > 1:
            self.logger.warning(
                f"Warning: more then one timestamp columns are specified, only first will be used!"
            )
        if self.id_column or self.timestamp_column:
            system_column_details = ds_messages_pb.SystemColumnDetails()
            if self.id_column:
                system_column_details.id_columns.append(
                    schema_pb.ColumnDetails(name=self.id_column[0])
                )
            if self.timestamp_column:
                system_column_details.timestamp_column.CopyFrom(
                    schema_pb.ColumnDetails(name=self.timestamp_column[0])
                )
            return system_column_details
        else:
            return None

    def includes_cache(self):
        return self.prediction is not None or self.feature_influences is not None


class CreateCacheInfo:

    def __init__(
        self,
        model_id: str,
        *,
        score_type: str = None,
        background_split_id: Optional[str] = "",
        explanation_algorithm_type: str = ""
    ):
        self.model_id = model_id
        self.score_type = score_type
        self.background_split_id = background_split_id
        self.explanation_algorithm_type = explanation_algorithm_type

    def build_create_cache_info(self):
        create_cache_proto = ds_messages_pb.CreateCacheInfo(
            model_id=self.model_id
        )
        if self.score_type is not None:
            create_cache_proto.score_type = get_qoi_from_string(self.score_type)

        if self.background_split_id:
            create_cache_proto.background_split_id = self.background_split_id

        if self.explanation_algorithm_type:
            create_cache_proto.explanation_algorithm_type = \
                get_explanation_algorithm_type_from_string(self.explanation_algorithm_type)
        return create_cache_proto
