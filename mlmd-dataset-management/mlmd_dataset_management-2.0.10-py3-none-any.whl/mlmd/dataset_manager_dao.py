from ml_metadata.proto import metadata_store_pb2
from dataset_management.connection_provider import get_mlmd_store
from mlmd.dataset_manager_scheme import ExecutionType, ArtifactType, ContextType

store = get_mlmd_store()

typelib = {
    ContextType.COMMIT_DATASET_VERSION: store.get_context_type(ContextType.COMMIT_DATASET_VERSION),
    ExecutionType.ADD_FILES_TO_DATASET: store.get_execution_type(ExecutionType.ADD_FILES_TO_DATASET),
    ExecutionType.REMOVE_FILES_FROM_DATASET: store.get_execution_type(ExecutionType.REMOVE_FILES_FROM_DATASET),
    ExecutionType.UPDATE_METADATA_DATASET: store.get_execution_type(ExecutionType.UPDATE_METADATA_DATASET),
    ExecutionType.UPDATE_ANNOTATION_DATASET: store.get_execution_type(ExecutionType.UPDATE_ANNOTATION_DATASET),
    ArtifactType.DATASET: store.get_artifact_type(ArtifactType.DATASET),
    ArtifactType.IMAGE: store.get_artifact_type(ArtifactType.IMAGE)
}

def get_type_name_from_id(type_id):
    for type_name, typeobj in typelib.items():
        if typeobj.id == type_id:
            return type_name
    return ""

def create_artifact(type, obj):
    artifact = metadata_store_pb2.Artifact()
    artifact.type_id = typelib.get(type).id
    for k, v in obj.items():
        if k == "name":
            artifact.name = v
        else:
            artifact.properties[k].string_value = v
    # if created_by is not None:
    #     artifact.properties["created_by"].string_value = created_by
    # if latest_version is not None:
    #     artifact.properties["latest_version"].string_value = latest_version
    # if uncommitted_version is not None:
    #     artifact.properties["uncommitted_version"].string_value = uncommitted_version
    [artifact_id] = store.put_artifacts([artifact])
    return artifact_id

def create_artifacts(type, obj_array):
    artifacts = []
    for obj in obj_array:
        artifact = metadata_store_pb2.Artifact()        
        artifact.type_id = typelib.get(type).id
        for k, v in obj.items():
            if k == "name":
                artifact.name = v
            else:
                artifact.properties[k].string_value = v
        artifacts.append(artifact)
    ids = store.put_artifacts(artifacts)
    return ids

def get_artifacts_by_type(type):    
    return store.get_artifacts_by_type(typelib.get(type).name)

def get_artifacts_by_context(context_id):
    return store.get_artifacts_by_context(context_id)

def get_artifact_by_type_and_name(type, name):
    return store.get_artifact_by_type_and_name(typelib.get(type).name, name)

def update_artifact(type, name, created_by=None, latest_version=None, uncommitted_version=None, trigger=None, tags=None):
    artifact = store.get_artifact_by_type_and_name(typelib.get(type).name, name)
    if created_by is not None:
        artifact.properties["created_by"].string_value = created_by
    if latest_version is not None:
        artifact.properties["latest_version"].string_value = latest_version
    if uncommitted_version is not None:
        artifact.properties["uncommitted_version"].string_value = uncommitted_version
    if trigger is not None:
        artifact.properties["trigger"].string_value = trigger
    if tags is not None:
        artifact.properties["tags"].string_value = tags
    [artifact_id] = store.put_artifacts([artifact])
    return artifact_id
    

def create_execution(type, obj):
    execution = metadata_store_pb2.Execution()
    execution.type_id = typelib.get(type).id
    for k,v in obj.items():
        execution.properties[k].string_value = str(v)
    try:
        [exe_id] = store.put_executions([execution])
    except Exception as e:
        print("Exception during putting execution {}".format(str(e)))
        print("Retrying putting execution")
        [exe_id] = store.put_executions([execution])
    return exe_id

def get_executions_by_context(context_id):
    return store.get_executions_by_context(context_id)

def get_execution_type_by_name(type):
    return store.get_execution_type(typelib.get(type).name)

def create_context(type, name, committed_by=None, prev_ref=None):
    ctx = metadata_store_pb2.Context()
    ctx.type_id = typelib.get(type).id
    ctx.name = name
    if committed_by is not None:
        ctx.properties["committed_by"].string_value = committed_by
    if prev_ref is not None:
        ctx.properties["prev_ref"].string_value = prev_ref
    [ctx_id] = store.put_contexts([ctx])
    return ctx_id

def update_context(context):
    return store.put_contexts([context])

def get_context(type, name):
    return store.get_context_by_type_and_name(typelib.get(type).name, name)

def get_contexts_by_artifact(type, artifact_id):
    contexts = store.get_contexts_by_artifact(artifact_id)
    return [context for context in contexts if context.type_id == typelib.get(type).id]

def get_contexts_by_execution(execution_id, context_types):
    context_type_filter = [typelib.get(context_type).id for context_type in context_types]
    contexts = store.get_contexts_by_execution(execution_id)
    return [ctx for ctx in contexts if ctx.type_id in context_type_filter]

def create_association_attribution(context_id, execution_id, artifact_id):
    association_arr = []
    attribution_arr = []
    if execution_id is not None:
        association = metadata_store_pb2.Association()
        association.execution_id = execution_id
        association.context_id = context_id
        association_arr.append(association)
    if artifact_id is not None:
        attribution = metadata_store_pb2.Attribution()
        attribution.artifact_id = artifact_id
        attribution.context_id = context_id
        attribution_arr.append(attribution)
    if len(association_arr) <= 0 and len(attribution_arr) <= 0:
        raise Exception("Invalid parameter for creating association and attribution")
    return store.put_attributions_and_associations(attribution_arr, association_arr)

def put_attr(attr_arr):
    return store.put_attributions_and_associations(attr_arr, [])

def create_association_attribution_multi_artifacts(context_id, execution_id, artifact_ids):
    association_arr = []
    attribution_arr = []
    if execution_id is not None:
        association = metadata_store_pb2.Association()
        association.execution_id = execution_id
        association.context_id = context_id
        association_arr.append(association)
    for artifact_id in artifact_ids:
        attribution = metadata_store_pb2.Attribution()
        attribution.artifact_id = artifact_id
        attribution.context_id = context_id
        attribution_arr.append(attribution)
    if len(association_arr) <= 0 and len(attribution_arr) <= 0:
        raise Exception("Invalid parameter for creating association and attribution")
    for chunk in chunks(attribution_arr, 10):
        store.put_attributions_and_associations(chunk, [])

    from multiprocessing import Pool, cpu_count
    p = Pool(cpu_count())
    r = p.map(put_attr, chunks(attribution_arr, 10))
    p.close()
    p.join()
        
    return store.put_attributions_and_associations([], association_arr)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
