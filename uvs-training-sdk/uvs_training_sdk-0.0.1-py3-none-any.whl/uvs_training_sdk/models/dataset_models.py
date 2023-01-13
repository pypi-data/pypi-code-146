from typing import List


class AnnotationKind:
    MULTICLASS_CLASSIFICATION = 'multiClassClassification'
    MULTILABEL_CLASSIFICATION = 'multiLabelClassification'
    OBJECT_DETECTION = 'objectDetection'
    VALID_KINDS = [MULTICLASS_CLASSIFICATION, MULTILABEL_CLASSIFICATION, OBJECT_DETECTION]


class Dataset:
    def __init__(self, name: str, annotation_kind: str, annotation_file_uris: List[str], storage_base_uri: str) -> None:
        assert name
        assert annotation_kind in AnnotationKind.VALID_KINDS, f'unknown kind {annotation_kind}'
        assert annotation_file_uris
        assert storage_base_uri

        self.name = name
        self.annotation_kind = annotation_kind
        self.annotation_file_uris = annotation_file_uris
        self.storage_base_uri = storage_base_uri
        self._params = {
            "AnnotationKind": annotation_kind,
            "AnnotationFileUris": annotation_file_uris,
            "StorageBaseUri": storage_base_uri
        }

    @property
    def params(self):
        return self._params


class DatasetResponse(Dataset):
    def __init__(self, name: str, annotation_kind: str, annotation_file_uris: List[str], storage_base_uri: str, created_date_time, last_modified_date_time) -> None:
        super().__init__(name, annotation_kind, annotation_file_uris, storage_base_uri)
        self.created_date_time = created_date_time
        self.last_modified_date_time = last_modified_date_time

    @staticmethod
    def from_response(json):
        return DatasetResponse(json['name'], json['annotationKind'], json['annotationFileUris'], json['storageBaseUri'], json['createdDateTime'], json['lastModifiedDateTime'])
