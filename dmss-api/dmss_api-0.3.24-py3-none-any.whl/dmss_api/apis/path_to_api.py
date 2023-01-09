import typing_extensions

from dmss_api.paths import PathValues
from dmss_api.apis.paths.api_acl_data_source_id_document_id import ApiAclDataSourceIdDocumentId
from dmss_api.apis.paths.api_blobs_data_source_id_blob_id import ApiBlobsDataSourceIdBlobId
from dmss_api.apis.paths.api_blueprint_type_ref import ApiBlueprintTypeRef
from dmss_api.apis.paths.api_resolve_path_absolute_id import ApiResolvePathAbsoluteId
from dmss_api.apis.paths.api_data_sources_data_source_id import ApiDataSourcesDataSourceId
from dmss_api.apis.paths.api_data_sources import ApiDataSources
from dmss_api.apis.paths.api_documents_id_reference import ApiDocumentsIdReference
from dmss_api.apis.paths.api_documents_by_path_absolute_path import ApiDocumentsByPathAbsolutePath
from dmss_api.apis.paths.api_documents_data_source_id_document_id import ApiDocumentsDataSourceIdDocumentId
from dmss_api.apis.paths.api_documents_data_source_id_dotted_id import ApiDocumentsDataSourceIdDottedId
from dmss_api.apis.paths.api_documents_path_reference_add_to_path import ApiDocumentsPathReferenceAddToPath
from dmss_api.apis.paths.api_documents_data_source_id_add_raw import ApiDocumentsDataSourceIdAddRaw
from dmss_api.apis.paths.api_documents_absolute_ref import ApiDocumentsAbsoluteRef
from dmss_api.apis.paths.api_documents_data_source_id_remove_by_path_directory import ApiDocumentsDataSourceIdRemoveByPathDirectory
from dmss_api.apis.paths.api_export_meta_absolute_document_ref import ApiExportMetaAbsoluteDocumentRef
from dmss_api.apis.paths.api_export_absolute_document_ref import ApiExportAbsoluteDocumentRef
from dmss_api.apis.paths.api_reference_data_source_id_document_dotted_id import ApiReferenceDataSourceIdDocumentDottedId
from dmss_api.apis.paths.api_search import ApiSearch
from dmss_api.apis.paths.api_whoami import ApiWhoami
from dmss_api.apis.paths.api_entity import ApiEntity
from dmss_api.apis.paths.api_application_application import ApiApplicationApplication
from dmss_api.apis.paths.api_token import ApiToken
from dmss_api.apis.paths.api_token_token_id import ApiTokenTokenId
from dmss_api.apis.paths.api_healthcheck import ApiHealthcheck

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_ACL_DATA_SOURCE_ID_DOCUMENT_ID: ApiAclDataSourceIdDocumentId,
        PathValues.API_BLOBS_DATA_SOURCE_ID_BLOB_ID: ApiBlobsDataSourceIdBlobId,
        PathValues.API_BLUEPRINT_TYPE_REF: ApiBlueprintTypeRef,
        PathValues.API_RESOLVEPATH_ABSOLUTE_ID: ApiResolvePathAbsoluteId,
        PathValues.API_DATASOURCES_DATA_SOURCE_ID: ApiDataSourcesDataSourceId,
        PathValues.API_DATASOURCES: ApiDataSources,
        PathValues.API_DOCUMENTS_ID_REFERENCE: ApiDocumentsIdReference,
        PathValues.API_DOCUMENTSBYPATH_ABSOLUTE_PATH: ApiDocumentsByPathAbsolutePath,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_DOCUMENT_ID: ApiDocumentsDataSourceIdDocumentId,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_DOTTED_ID: ApiDocumentsDataSourceIdDottedId,
        PathValues.API_DOCUMENTS_PATH_REFERENCE_ADDTOPATH: ApiDocumentsPathReferenceAddToPath,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_ADDRAW: ApiDocumentsDataSourceIdAddRaw,
        PathValues.API_DOCUMENTS_ABSOLUTE_REF: ApiDocumentsAbsoluteRef,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_REMOVEBYPATH_DIRECTORY: ApiDocumentsDataSourceIdRemoveByPathDirectory,
        PathValues.API_EXPORT_META_ABSOLUTE_DOCUMENT_REF: ApiExportMetaAbsoluteDocumentRef,
        PathValues.API_EXPORT_ABSOLUTE_DOCUMENT_REF: ApiExportAbsoluteDocumentRef,
        PathValues.API_REFERENCE_DATA_SOURCE_ID_DOCUMENT_DOTTED_ID: ApiReferenceDataSourceIdDocumentDottedId,
        PathValues.API_SEARCH: ApiSearch,
        PathValues.API_WHOAMI: ApiWhoami,
        PathValues.API_ENTITY: ApiEntity,
        PathValues.API_APPLICATION_APPLICATION: ApiApplicationApplication,
        PathValues.API_TOKEN: ApiToken,
        PathValues.API_TOKEN_TOKEN_ID: ApiTokenTokenId,
        PathValues.API_HEALTHCHECK: ApiHealthcheck,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_ACL_DATA_SOURCE_ID_DOCUMENT_ID: ApiAclDataSourceIdDocumentId,
        PathValues.API_BLOBS_DATA_SOURCE_ID_BLOB_ID: ApiBlobsDataSourceIdBlobId,
        PathValues.API_BLUEPRINT_TYPE_REF: ApiBlueprintTypeRef,
        PathValues.API_RESOLVEPATH_ABSOLUTE_ID: ApiResolvePathAbsoluteId,
        PathValues.API_DATASOURCES_DATA_SOURCE_ID: ApiDataSourcesDataSourceId,
        PathValues.API_DATASOURCES: ApiDataSources,
        PathValues.API_DOCUMENTS_ID_REFERENCE: ApiDocumentsIdReference,
        PathValues.API_DOCUMENTSBYPATH_ABSOLUTE_PATH: ApiDocumentsByPathAbsolutePath,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_DOCUMENT_ID: ApiDocumentsDataSourceIdDocumentId,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_DOTTED_ID: ApiDocumentsDataSourceIdDottedId,
        PathValues.API_DOCUMENTS_PATH_REFERENCE_ADDTOPATH: ApiDocumentsPathReferenceAddToPath,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_ADDRAW: ApiDocumentsDataSourceIdAddRaw,
        PathValues.API_DOCUMENTS_ABSOLUTE_REF: ApiDocumentsAbsoluteRef,
        PathValues.API_DOCUMENTS_DATA_SOURCE_ID_REMOVEBYPATH_DIRECTORY: ApiDocumentsDataSourceIdRemoveByPathDirectory,
        PathValues.API_EXPORT_META_ABSOLUTE_DOCUMENT_REF: ApiExportMetaAbsoluteDocumentRef,
        PathValues.API_EXPORT_ABSOLUTE_DOCUMENT_REF: ApiExportAbsoluteDocumentRef,
        PathValues.API_REFERENCE_DATA_SOURCE_ID_DOCUMENT_DOTTED_ID: ApiReferenceDataSourceIdDocumentDottedId,
        PathValues.API_SEARCH: ApiSearch,
        PathValues.API_WHOAMI: ApiWhoami,
        PathValues.API_ENTITY: ApiEntity,
        PathValues.API_APPLICATION_APPLICATION: ApiApplicationApplication,
        PathValues.API_TOKEN: ApiToken,
        PathValues.API_TOKEN_TOKEN_ID: ApiTokenTokenId,
        PathValues.API_HEALTHCHECK: ApiHealthcheck,
    }
)
