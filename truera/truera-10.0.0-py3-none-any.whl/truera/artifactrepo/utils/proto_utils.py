from truera.protobuf.public import metadata_message_types_pb2 as md_pb
from truera.protobuf.public.data import data_split_pb2


def map_split_type_to_str(split_type: data_split_pb2.DataSplitType, context):
    return data_split_pb2.DataSplitType.Name(split_type
                                            ).lower().replace('_split', '')


def transform_split_to_public(entity, context):
    if not entity:
        return None

    return md_pb.DataSplitMetadata(
        id=entity.id,
        name=entity.name,
        description=entity.description,
        project_id=entity.project_id,
        data_collection_id=entity.dataset_id,
        split_type=map_split_type_to_str(entity.split_type, context),
        preprocessed_locator=entity.preprocessed_locator,
        processed_locator=entity.processed_locator,
        label_locator=entity.label_locator,
        extra_data_locator=entity.extra_data_locator,
        tags=entity.tags,
        provenance=entity.provenance,
        created_at=entity.created_at,
        time_range=entity.time_range,
        unique_id_column_name=entity.unique_id_column_name,
        timestamp_column_name=entity.timestamp_column_name,
        split_mode=entity.split_mode,
        status=entity.status
    )
