class HashError(Exception):
    pass

class StoreError(HashError):
    pass

class StoreNotFound(StoreError):
    pass
class StateStoreError(StoreError):
    pass

class ConfigStoreError(StoreError):
    pass

class ResourceStoreError(StoreError):
    pass

class ResourceError(HashError):
    pass

class UnsupportedResourceError(ResourceError):
    pass

class ResourceConfigError(ResourceError):
    pass

class ResourceInvalidYaml(ResourceError):
    pass

class ResourceSpecError(ResourceError):
    pass

class ResourceBuildError(ResourceError):
    pass

class ResourceTestError(ResourceError):
    pass

class ResourcePublishError(ResourceError):
    pass

class ResourceDeployError(ResourceError):
    pass

class ResourceNotFoundError(ResourceError):
    pass

class LocationError(HashError):
    pass

class UnsupportedLocationError(LocationError):
    pass

class ConfigLocationError(LocationError):
    pass

class ArtifactError(HashError):
    pass

class ArtifactStageError(ArtifactError):
    pass

class ArtifactKindError(ArtifactError):
    pass

class ArtifactNotFoundError(ArtifactError):
    pass

class TemplateError(HashError):
    pass

class TemplatePathNotFoundError(TemplateError):
    pass

class TemplateRenderError(TemplateError):
    pass

class ScriptError(HashError):
    pass

class ScriptNotFoundError(ScriptError):
    pass

class TargetError(HashError):
    pass

class TargetNotFound(TargetError):
    pass

class TargetConfigError(TargetError):
    pass

class TargetActionError(TargetError):
    pass

class TargetResourceError(TargetError):
    pass

class StateError(HashError):
    pass

class StateArtifactError(StateError):
    pass

class DictError(HashError):
    pass

class ActionError(HashError):
    pass

class GraphError(HashError):
    pass

class NodeError(HashError):
    pass

class EdgeError(HashError):
    pass

class ExecutorError(HashError):
    pass

class ExecutorErrorNotFound(ExecutorError):
    pass
