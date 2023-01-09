import typing_extensions

from dmss_api.apis.tags import TagValues
from dmss_api.apis.tags.default_api import DefaultApi
from dmss_api.apis.tags.access_control_api import AccessControlApi
from dmss_api.apis.tags.blob_api import BlobApi
from dmss_api.apis.tags.blueprint_api import BlueprintApi
from dmss_api.apis.tags.datasource_api import DatasourceApi
from dmss_api.apis.tags.lookup_table_api import LookupTableApi
from dmss_api.apis.tags.document_api import DocumentApi
from dmss_api.apis.tags.export_api import ExportApi
from dmss_api.apis.tags.health_check_api import HealthCheckApi
from dmss_api.apis.tags.entity_api import EntityApi
from dmss_api.apis.tags.reference_api import ReferenceApi
from dmss_api.apis.tags.search_api import SearchApi
from dmss_api.apis.tags.personal_access_token_api import PersonalAccessTokenApi
from dmss_api.apis.tags.whoami_api import WhoamiApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.DEFAULT: DefaultApi,
        TagValues.ACCESS_CONTROL: AccessControlApi,
        TagValues.BLOB: BlobApi,
        TagValues.BLUEPRINT: BlueprintApi,
        TagValues.DATASOURCE: DatasourceApi,
        TagValues.LOOKUPTABLE: LookupTableApi,
        TagValues.DOCUMENT: DocumentApi,
        TagValues.EXPORT: ExportApi,
        TagValues.HEALTH_CHECK: HealthCheckApi,
        TagValues.ENTITY: EntityApi,
        TagValues.REFERENCE: ReferenceApi,
        TagValues.SEARCH: SearchApi,
        TagValues.PERSONAL_ACCESS_TOKEN: PersonalAccessTokenApi,
        TagValues.WHOAMI: WhoamiApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.DEFAULT: DefaultApi,
        TagValues.ACCESS_CONTROL: AccessControlApi,
        TagValues.BLOB: BlobApi,
        TagValues.BLUEPRINT: BlueprintApi,
        TagValues.DATASOURCE: DatasourceApi,
        TagValues.LOOKUPTABLE: LookupTableApi,
        TagValues.DOCUMENT: DocumentApi,
        TagValues.EXPORT: ExportApi,
        TagValues.HEALTH_CHECK: HealthCheckApi,
        TagValues.ENTITY: EntityApi,
        TagValues.REFERENCE: ReferenceApi,
        TagValues.SEARCH: SearchApi,
        TagValues.PERSONAL_ACCESS_TOKEN: PersonalAccessTokenApi,
        TagValues.WHOAMI: WhoamiApi,
    }
)
