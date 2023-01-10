from dataset_management.connection_provider import get_mlmd_store
from ml_metadata.proto import metadata_store_pb2
from ml_metadata.metadata_store import MetadataStore

class ArtifactType():
    DATASET = "Dataset"
    IMAGE = "Image"
class ExecutionType():
    ADD_FILES_TO_DATASET = "AddFilesToDataset"
    REMOVE_FILES_FROM_DATASET = "RemoveFilesFromDataset"
    UPDATE_METADATA_DATASET = "UpdateMetadataToDataset"
    UPDATE_ANNOTATION_DATASET = "UpdateAnnotationToDataset"

class ContextType():
    COMMIT_DATASET_VERSION = "CommitDatasetVersion"

def init_dataset_scheme(store):
    # create artifact type Dataset
    data_type = metadata_store_pb2.ArtifactType()
    data_type.name = ArtifactType.DATASET
    data_type.properties["created_by"] = metadata_store_pb2.STRING
    data_type.properties["latest_version"] = metadata_store_pb2.STRING
    data_type.properties["uncommitted_version"] = metadata_store_pb2.STRING
    data_type.properties["trigger"] = metadata_store_pb2.STRING
    data_type.properties["tags"] = metadata_store_pb2.STRING
    store.put_artifact_type(data_type, can_omit_fields=True)

    # create artifact type Image
    data_type = metadata_store_pb2.ArtifactType()
    data_type.name = ArtifactType.IMAGE
    data_type.properties["annotation"] = metadata_store_pb2.STRING
    data_type.properties["author"] = metadata_store_pb2.STRING
    store.put_artifact_type(data_type, can_omit_fields=True)

    # execution type
    trainer_type = metadata_store_pb2.ExecutionType()
    trainer_type.name = ExecutionType.ADD_FILES_TO_DATASET
    trainer_type.properties["executed_by"] = metadata_store_pb2.STRING
    trainer_type.properties["file_location"] = metadata_store_pb2.STRING
    trainer_type.properties["tenant"] = metadata_store_pb2.STRING
    trainer_type.properties["annotation"] = metadata_store_pb2.STRING
    store.put_execution_type(trainer_type)

    trainer_type = metadata_store_pb2.ExecutionType()
    trainer_type.name = ExecutionType.REMOVE_FILES_FROM_DATASET
    trainer_type.properties["executed_by"] = metadata_store_pb2.STRING
    store.put_execution_type(trainer_type)

    # Context type
    context_type = metadata_store_pb2.ContextType()
    context_type.name = ContextType.COMMIT_DATASET_VERSION
    context_type.properties["prev_ref"] = metadata_store_pb2.STRING
    context_type.properties["committed_by"] = metadata_store_pb2.STRING
    context_type.properties["commit_message"] = metadata_store_pb2.STRING
    store.put_context_type(context_type)

def get_all_artifact_types(store: MetadataStore):
    return store.get_artifact_types()

def create_execution_type(execution_type):
    trainer_type = metadata_store_pb2.ExecutionType()
    trainer_type.name = execution_type
    trainer_type.properties["executed_by"] = metadata_store_pb2.STRING
    store.put_execution_type(trainer_type)

if __name__ == "__main__":
    store = get_mlmd_store()
    # init_dataset_scheme(store)
    create_execution_type(ExecutionType.UPDATE_METADATA_DATASET)


# print(store.get_artifact_type("Dataset"))

# print(store.get_execution_type(ExecutionType.ADD_FILES_TO_DATASET))
# store.get_executions()