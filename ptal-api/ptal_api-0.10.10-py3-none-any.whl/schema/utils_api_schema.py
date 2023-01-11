import sgqlc.types
# import sgqlc.types.datetime


utils_api_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class AccountSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('creator', 'id', 'lastUpdater', 'name', 'platformId', 'systemRegistrationDate', 'systemUpdateDate', 'url')


Boolean = sgqlc.types.Boolean

class ComponentView(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('keyValue', 'value')


class CompositeConceptTypeWidgetTypeSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('id', 'name', 'order')


class ConceptLinkDirection(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('from', 'to')


class ConceptLinkTypeSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('conceptType', 'id', 'name')


class ConceptPropertyTypeSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('name', 'registrationDate')


class ConceptSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('accessLevel', 'countConcepts', 'countConceptsAndDocuments', 'countDocumentFacts', 'countDocumentMentions', 'countEvents', 'countObjects', 'countPotentialDocuments', 'countProperties', 'countResearchMaps', 'countTasks', 'creator', 'id', 'lastUpdater', 'name', 'score', 'systemRegistrationDate', 'systemUpdateDate')


class ConceptTypeLinkMetadata(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('creator', 'endDate', 'lastUpdater', 'linkType', 'registrationDate', 'startDate', 'updateDate')


class ConceptTypeMetadata(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('concept', 'conceptType', 'creator', 'endDate', 'lastUpdater', 'markers', 'name', 'notes', 'startDate', 'systemRegistrationDate', 'systemUpdateDate')


class ConceptTypeSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('dictionary', 'id', 'name', 'regexp')


class ConceptUpdate(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('link', 'linkProperty', 'metadata', 'property')


class ConceptVariant(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('event', 'obj')


class DocumentGrouping(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('none', 'story')


class DocumentRecall(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('high', 'low', 'medium', 'none')


class DocumentSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('countChildDocs', 'countConcepts', 'countDisambiguatedEntities', 'countEntities', 'countEvents', 'countLinks', 'countNamedEntities', 'countObjects', 'countResearchMaps', 'countTasks', 'id', 'publicationDate', 'registrationDate', 'score', 'secretLevel', 'text', 'title', 'trustLevel', 'updateDate')


class DocumentSourceType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('external', 'internal')


class DocumentType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('image', 'text')


class DocumentUpdate(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('content', 'markup', 'metadata')


class FactStatus(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('approved', 'autoApproved', 'declined', 'hidden', 'new')


Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class IssuePriority(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('High', 'Low', 'Medium')


class IssueSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('creator', 'executor', 'id', 'lastUpdater', 'priority', 'registrationDate', 'status', 'topic', 'updateDate')


class IssueStatus(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('canceled', 'closed', 'dataRequested', 'development', 'improvementRequested', 'open', 'reviewRequested')


class LinkDirection(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('in', 'out', 'undirected')


class Locale(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('eng', 'other', 'ru')


class Long(sgqlc.types.Scalar):
    __schema__ = utils_api_schema


class MapEdgeType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('conceptCandidateFactMention', 'conceptFactLink', 'conceptImplicitLink', 'conceptLink', 'conceptLinkCandidateFact', 'conceptMention', 'conceptTypeLink', 'documentLink')


class MapNodeType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('concept', 'conceptCandidateFact', 'conceptType', 'document')


class NodeType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('header', 'image', 'json', 'key', 'list', 'other', 'row', 'table', 'text')


class PlatformType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('blog', 'database', 'fileStorage', 'forum', 'media', 'messenger', 'newsAggregator', 'procurement', 'review', 'socialNetwork')


class PropLinkOrConcept(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('concept', 'link')


class ResearchMapSorting(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('accessLevel', 'conceptAndDocumentLink', 'conceptLink', 'creator', 'documentLink', 'id', 'lastUpdater', 'name', 'systemRegistrationDate', 'systemUpdateDate')


class SortDirection(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('ascending', 'descending')


String = sgqlc.types.String

class TrustLevel(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('high', 'low', 'medium')


class UnixTime(sgqlc.types.Scalar):
    __schema__ = utils_api_schema


class Upload(sgqlc.types.Scalar):
    __schema__ = utils_api_schema


class ValueType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('Date', 'Double', 'Geo', 'Int', 'Link', 'String', 'StringLocale')


class WidgetTypeTableType(sgqlc.types.Enum):
    __schema__ = utils_api_schema
    __choices__ = ('horizontal', 'vertical')



########################################################################
# Input Objects
########################################################################
class AccountFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('search_string', 'platform_id', 'id', 'country', 'markers', 'creator', 'last_updater', 'registration_date', 'update_date')
    search_string = sgqlc.types.Field(String, graphql_name='searchString')
    platform_id = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='platformId')
    id = sgqlc.types.Field(ID, graphql_name='id')
    country = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='country')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='registrationDate')
    update_date = sgqlc.types.Field('TimestampInterval', graphql_name='updateDate')


class AccountGetOrCreateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'platform_id', 'name', 'url')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    platform_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='platformId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class AliasCreateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_id', 'value')
    concept_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptId')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class ConceptExtraSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('search_on_map', 'selected_content')
    search_on_map = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='searchOnMap')
    selected_content = sgqlc.types.Field('ResearchMapContentSelectInput', graphql_name='selectedContent')


class ConceptFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('property_filter_settings', 'link_filter_settings', 'concept_type_ids', 'concept_variant', 'name', 'exact_name', 'substring', 'access_level_id', 'creator', 'last_updater', 'creation_date', 'update_date', 'markers', 'has_linked_issues')
    property_filter_settings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('PropertyFilterSettings')), graphql_name='propertyFilterSettings')
    link_filter_settings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('LinkFilterSettings')), graphql_name='linkFilterSettings')
    concept_type_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='conceptTypeIds')
    concept_variant = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ConceptVariant)), graphql_name='conceptVariant')
    name = sgqlc.types.Field(String, graphql_name='name')
    exact_name = sgqlc.types.Field(String, graphql_name='exactName')
    substring = sgqlc.types.Field(String, graphql_name='substring')
    access_level_id = sgqlc.types.Field(ID, graphql_name='accessLevelId')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    creation_date = sgqlc.types.Field('TimestampInterval', graphql_name='creationDate')
    update_date = sgqlc.types.Field('TimestampInterval', graphql_name='updateDate')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')
    has_linked_issues = sgqlc.types.Field(Boolean, graphql_name='hasLinkedIssues')


class ConceptLinkFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('is_event', 'concept_link_type', 'document_id', 'creation_date', 'update_date')
    is_event = sgqlc.types.Field(Boolean, graphql_name='isEvent')
    concept_link_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='conceptLinkType')
    document_id = sgqlc.types.Field(ID, graphql_name='documentId')
    creation_date = sgqlc.types.Field('TimestampInterval', graphql_name='creationDate')
    update_date = sgqlc.types.Field('TimestampInterval', graphql_name='updateDate')


class ConceptLinkTypeFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('name', 'concept_from_type_id', 'concept_to_type_id', 'concept_type_and_event_filter', 'is_directed', 'is_hierarchical', 'creator', 'last_updater', 'registration_date', 'update_date', 'has_rel_ext_models')
    name = sgqlc.types.Field(String, graphql_name='name')
    concept_from_type_id = sgqlc.types.Field(ID, graphql_name='conceptFromTypeId')
    concept_to_type_id = sgqlc.types.Field(ID, graphql_name='conceptToTypeId')
    concept_type_and_event_filter = sgqlc.types.Field('conceptTypeAndEventFilter', graphql_name='conceptTypeAndEventFilter')
    is_directed = sgqlc.types.Field(Boolean, graphql_name='isDirected')
    is_hierarchical = sgqlc.types.Field(Boolean, graphql_name='isHierarchical')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='registrationDate')
    update_date = sgqlc.types.Field('TimestampInterval', graphql_name='updateDate')
    has_rel_ext_models = sgqlc.types.Field(Boolean, graphql_name='hasRelExtModels')


class ConceptMentionCountBatchInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('inputs', 'limit', 'extend_results')
    inputs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptMentionCountInput'))), graphql_name='inputs')
    limit = sgqlc.types.Field(Int, graphql_name='limit')
    extend_results = sgqlc.types.Field(Boolean, graphql_name='extendResults')


class ConceptMentionCountInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('term', 'concept_types')
    term = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='term')
    concept_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='conceptTypes')


class ConceptMutationInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('name', 'concept_type_id', 'notes', 'fact_info', 'markers', 'access_level_id', 'start_date', 'end_date')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    concept_type_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptTypeId')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    fact_info = sgqlc.types.Field('FactInput', graphql_name='factInfo')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')
    access_level_id = sgqlc.types.Field(ID, graphql_name='accessLevelId')
    start_date = sgqlc.types.Field('DateTimeValueInput', graphql_name='startDate')
    end_date = sgqlc.types.Field('DateTimeValueInput', graphql_name='endDate')


class ConceptPropertyFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('only_main', 'document_id')
    only_main = sgqlc.types.Field(Boolean, graphql_name='onlyMain')
    document_id = sgqlc.types.Field(ID, graphql_name='documentId')


class ConceptPropertyTypeFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('name', 'concept_type_id', 'concept_link_type_id', 'concept_value_type_id', 'value_type', 'concept_type_from_link_type_id')
    name = sgqlc.types.Field(String, graphql_name='name')
    concept_type_id = sgqlc.types.Field(ID, graphql_name='conceptTypeId')
    concept_link_type_id = sgqlc.types.Field(ID, graphql_name='conceptLinkTypeId')
    concept_value_type_id = sgqlc.types.Field(ID, graphql_name='conceptValueTypeId')
    value_type = sgqlc.types.Field(ValueType, graphql_name='valueType')
    concept_type_from_link_type_id = sgqlc.types.Field(ID, graphql_name='conceptTypeFromLinkTypeId')


class DateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('year', 'month', 'day')
    year = sgqlc.types.Field(Int, graphql_name='year')
    month = sgqlc.types.Field(Int, graphql_name='month')
    day = sgqlc.types.Field(Int, graphql_name='day')


class DateTimeIntervalInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field('DateTimeValueInput', graphql_name='start')
    end = sgqlc.types.Field('DateTimeValueInput', graphql_name='end')


class DateTimeIntervalPairInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field(sgqlc.types.non_null(DateTimeIntervalInput), graphql_name='start')
    end = sgqlc.types.Field(sgqlc.types.non_null(DateTimeIntervalInput), graphql_name='end')


class DateTimeValueInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('date', 'time')
    date = sgqlc.types.Field(sgqlc.types.non_null(DateInput), graphql_name='date')
    time = sgqlc.types.Field('TimeInput', graphql_name='time')


class DocumentFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('search_string', 'substring', 'named_entities', 'concepts', 'platforms', 'accounts', 'nerc_num', 'concepts_num', 'child_docs_num', 'publication_date', 'registration_date', 'last_update', 'creator', 'publication_author', 'last_updater', 'access_level_id', 'links', 'markers', 'document_type', 'source_type', 'trust_level', 'has_linked_issues', 'nested_ids', 'fact_types', 'story', 'show_read', 'job_ids', 'periodic_job_ids', 'task_ids', 'periodic_task_ids')
    search_string = sgqlc.types.Field(String, graphql_name='searchString')
    substring = sgqlc.types.Field(String, graphql_name='substring')
    named_entities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='namedEntities')
    concepts = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='concepts')
    platforms = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='platforms')
    accounts = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='accounts')
    nerc_num = sgqlc.types.Field('IntervalInt', graphql_name='nercNum')
    concepts_num = sgqlc.types.Field('IntervalInt', graphql_name='conceptsNum')
    child_docs_num = sgqlc.types.Field('IntervalInt', graphql_name='childDocsNum')
    publication_date = sgqlc.types.Field('TimestampInterval', graphql_name='publicationDate')
    registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='registrationDate')
    last_update = sgqlc.types.Field('TimestampInterval', graphql_name='lastUpdate')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    publication_author = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='publicationAuthor')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    access_level_id = sgqlc.types.Field(ID, graphql_name='accessLevelId')
    links = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='links')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')
    document_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DocumentType)), graphql_name='documentType')
    source_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DocumentSourceType)), graphql_name='sourceType')
    trust_level = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TrustLevel)), graphql_name='trustLevel')
    has_linked_issues = sgqlc.types.Field(Boolean, graphql_name='hasLinkedIssues')
    nested_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='nestedIds')
    fact_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='factTypes')
    story = sgqlc.types.Field(String, graphql_name='story')
    show_read = sgqlc.types.Field(Boolean, graphql_name='showRead')
    job_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='jobIds')
    periodic_job_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='periodicJobIds')
    task_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='taskIds')
    periodic_task_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='periodicTaskIds')


class DocumentLinkFilterSetting(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('document_type',)
    document_type = sgqlc.types.Field(DocumentType, graphql_name='documentType')


class DocumentsTextWithMarkerByDateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('marker', 'start_date', 'end_date')
    marker = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='marker')
    start_date = sgqlc.types.Field(UnixTime, graphql_name='startDate')
    end_date = sgqlc.types.Field(UnixTime, graphql_name='endDate')


class DocumentsWithConceptByDateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_type_id', 'start_date', 'end_date')
    concept_type_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptTypeId')
    start_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='startDate')
    end_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='endDate')


class ExtraSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('hide_child', 'search_on_map', 'ranking_script', 'selected_content')
    hide_child = sgqlc.types.Field(Boolean, graphql_name='hideChild')
    search_on_map = sgqlc.types.Field(Boolean, graphql_name='searchOnMap')
    ranking_script = sgqlc.types.Field(String, graphql_name='rankingScript')
    selected_content = sgqlc.types.Field('ResearchMapContentSelectInput', graphql_name='selectedContent')


class FactInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('document_id', 'annotations', 'fact_id')
    document_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='documentId')
    annotations = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('TextBoundingInput')), graphql_name='annotations')
    fact_id = sgqlc.types.Field(ID, graphql_name='factId')


class GeoPointFormInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('latitude', 'longitude')
    latitude = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='latitude')
    longitude = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='longitude')


class GeoPointWithNameFormInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('point', 'name', 'radius')
    point = sgqlc.types.Field(GeoPointFormInput, graphql_name='point')
    name = sgqlc.types.Field(String, graphql_name='name')
    radius = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='radius')


class IntervalDouble(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field(Float, graphql_name='start')
    end = sgqlc.types.Field(Float, graphql_name='end')


class IntervalInt(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field(Int, graphql_name='start')
    end = sgqlc.types.Field(Int, graphql_name='end')


class IssueFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('executor', 'creator', 'last_updater', 'status', 'priority', 'registration_date', 'update_date', 'issue_for_document', 'issue_for_concept', 'only_my', 'issue', 'concept', 'document', 'name', 'description', 'execution_time_limit', 'markers')
    executor = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='executor')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    status = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(IssueStatus)), graphql_name='status')
    priority = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(IssuePriority)), graphql_name='priority')
    registration_date = sgqlc.types.Field('TimestampInterval', graphql_name='registrationDate')
    update_date = sgqlc.types.Field('TimestampInterval', graphql_name='updateDate')
    issue_for_document = sgqlc.types.Field(Boolean, graphql_name='issueForDocument')
    issue_for_concept = sgqlc.types.Field(Boolean, graphql_name='issueForConcept')
    only_my = sgqlc.types.Field(Boolean, graphql_name='onlyMy')
    issue = sgqlc.types.Field(ID, graphql_name='issue')
    concept = sgqlc.types.Field(ID, graphql_name='concept')
    document = sgqlc.types.Field(ID, graphql_name='document')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    execution_time_limit = sgqlc.types.Field('TimestampInterval', graphql_name='executionTimeLimit')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')


class LinkFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('link_type_id', 'link_direction', 'other_concept_id')
    link_type_id = sgqlc.types.Field(ID, graphql_name='linkTypeId')
    link_direction = sgqlc.types.Field(LinkDirection, graphql_name='linkDirection')
    other_concept_id = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='otherConceptId')


class MapEdgeFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('edge_type',)
    edge_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(MapEdgeType)), graphql_name='edgeType')


class MapNodeFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('node_type',)
    node_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(MapNodeType)), graphql_name='nodeType')


class PlatformGetOrCreateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'platform_type', 'url')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    platform_type = sgqlc.types.Field(sgqlc.types.non_null(PlatformType), graphql_name='platformType')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class PropertyFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('property_type_id', 'component_id', 'property_type', 'string_filter', 'int_filter', 'double_filter', 'date_time_filter', 'date_time_interval_filter', 'geo_filter')
    property_type_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='propertyTypeId')
    component_id = sgqlc.types.Field(ID, graphql_name='componentId')
    property_type = sgqlc.types.Field(sgqlc.types.non_null(PropLinkOrConcept), graphql_name='propertyType')
    string_filter = sgqlc.types.Field('StringFilter', graphql_name='stringFilter')
    int_filter = sgqlc.types.Field(IntervalInt, graphql_name='intFilter')
    double_filter = sgqlc.types.Field(IntervalDouble, graphql_name='doubleFilter')
    date_time_filter = sgqlc.types.Field(DateTimeIntervalInput, graphql_name='dateTimeFilter')
    date_time_interval_filter = sgqlc.types.Field(DateTimeIntervalPairInput, graphql_name='dateTimeIntervalFilter')
    geo_filter = sgqlc.types.Field(GeoPointWithNameFormInput, graphql_name='geoFilter')


class ResearchMapContentSelectInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('nodes',)
    nodes = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='nodes')


class ResearchMapContentUpdateInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('nodes',)
    nodes = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='nodes')


class ResearchMapFilterSettings(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('name', 'description', 'access_level_id', 'creator', 'last_updater', 'markers', 'creation_date', 'update_date', 'concept_id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    access_level_id = sgqlc.types.Field(ID, graphql_name='accessLevelId')
    creator = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='creator')
    last_updater = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='lastUpdater')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')
    creation_date = sgqlc.types.Field('TimestampInterval', graphql_name='creationDate')
    update_date = sgqlc.types.Field('TimestampInterval', graphql_name='updateDate')
    concept_id = sgqlc.types.Field(ID, graphql_name='conceptId')


class StringFilter(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('str',)
    str = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='str')


class TextBoundingInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end', 'node_id')
    start = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='start')
    end = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='end')
    node_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='nodeId')


class TimeInput(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('hour', 'minute', 'second')
    hour = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='hour')
    minute = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minute')
    second = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='second')


class TimestampInterval(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field(UnixTime, graphql_name='start')
    end = sgqlc.types.Field(UnixTime, graphql_name='end')


class conceptTypeAndEventFilter(sgqlc.types.Input):
    __schema__ = utils_api_schema
    __field_names__ = ('full_type', 'is_event')
    full_type = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fullType')
    is_event = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isEvent')



########################################################################
# Output Objects and Interfaces
########################################################################
class AccessLevel(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'order')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    order = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='order')


class AccountFacet(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value', 'count')
    value = sgqlc.types.Field(sgqlc.types.non_null('Account'), graphql_name='value')
    count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='count')


class AccountPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_account', 'total', 'total_platforms')
    list_account = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Account'))), graphql_name='listAccount')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')
    total_platforms = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalPlatforms')


class AccountStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_doc', 'count_doc_today', 'count_doc_week', 'count_doc_month', 'recall_doc_today', 'recall_doc_week', 'recall_doc_month')
    count_doc = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDoc')
    count_doc_today = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocToday')
    count_doc_week = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocWeek')
    count_doc_month = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocMonth')
    recall_doc_today = sgqlc.types.Field(sgqlc.types.non_null(DocumentRecall), graphql_name='recallDocToday')
    recall_doc_week = sgqlc.types.Field(sgqlc.types.non_null(DocumentRecall), graphql_name='recallDocWeek')
    recall_doc_month = sgqlc.types.Field(sgqlc.types.non_null(DocumentRecall), graphql_name='recallDocMonth')


class Annotation(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end', 'value')
    start = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='start')
    end = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='end')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class CompositeConceptStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_concept_types',)
    count_concept_types = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countConceptTypes')


class CompositeConceptTypeWidgetTypeColumn(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'is_main_properties', 'list_values', 'sort_by_column', 'sort_direction', 'concept_link_types_path', 'property_type', 'metadata', 'link_property_type', 'link_metadata', 'sortable')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    is_main_properties = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isMainProperties')
    list_values = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='listValues')
    sort_by_column = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='sortByColumn')
    sort_direction = sgqlc.types.Field(SortDirection, graphql_name='sortDirection')
    concept_link_types_path = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptLinkTypePath'))), graphql_name='conceptLinkTypesPath')
    property_type = sgqlc.types.Field('ConceptPropertyType', graphql_name='propertyType')
    metadata = sgqlc.types.Field(ConceptTypeMetadata, graphql_name='metadata')
    link_property_type = sgqlc.types.Field('ConceptPropertyType', graphql_name='linkPropertyType')
    link_metadata = sgqlc.types.Field(ConceptTypeLinkMetadata, graphql_name='linkMetadata')
    sortable = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='sortable')


class CompositeConceptTypeWidgetTypePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_composite_concept_type_widget', 'total')
    list_composite_concept_type_widget = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('CompositeConceptTypeWidgetType'))), graphql_name='listCompositeConceptTypeWidget')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class CompositePropertyValueType(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'value_type', 'is_required', 'view')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    value_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptPropertyValueType'), graphql_name='valueType')
    is_required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRequired')
    view = sgqlc.types.Field(sgqlc.types.non_null(ComponentView), graphql_name='view')


class CompositeValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_value',)
    list_value = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('NamedValue'))), graphql_name='listValue')


class ConceptCandidateFactMention(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept', 'mention')
    concept = sgqlc.types.Field(sgqlc.types.non_null('ConceptCandidateFact'), graphql_name='concept')
    mention = sgqlc.types.Field(sgqlc.types.non_null('Mention'), graphql_name='mention')


class ConceptFactLink(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_id', 'concept_fact_id', 'status', 'is_implicit', 'concept', 'concept_fact')
    concept_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptId')
    concept_fact_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptFactId')
    status = sgqlc.types.Field(FactStatus, graphql_name='status')
    is_implicit = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isImplicit')
    concept = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='concept')
    concept_fact = sgqlc.types.Field(sgqlc.types.non_null('ConceptCandidateFact'), graphql_name='conceptFact')


class ConceptFactPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_concept_fact')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_concept_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptFact'))), graphql_name='listConceptFact')


class ConceptImplicitLink(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_from_id', 'concept_to_id', 'concept_from', 'concept_to', 'concept_link_type')
    concept_from_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptFromId')
    concept_to_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptToId')
    concept_from = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='conceptFrom')
    concept_to = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='conceptTo')
    concept_link_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptLinkType'), graphql_name='conceptLinkType')


class ConceptLinkFactPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_concept_link_fact')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_concept_link_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptLinkFact'))), graphql_name='listConceptLinkFact')


class ConceptLinkPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_concept_link')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_concept_link = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptLink'))), graphql_name='listConceptLink')


class ConceptLinkTypePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_concept_link_type', 'total')
    list_concept_link_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptLinkType'))), graphql_name='listConceptLinkType')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class ConceptLinkTypePath(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('link_type', 'fixed')
    link_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptLinkType'), graphql_name='linkType')
    fixed = sgqlc.types.Field(ConceptLinkDirection, graphql_name='fixed')


class ConceptLinkTypeStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_property_type',)
    count_property_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countPropertyType')


class ConceptMention(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept', 'mention')
    concept = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='concept')
    mention = sgqlc.types.Field(sgqlc.types.non_null('Mention'), graphql_name='mention')


class ConceptMentionCount(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept', 'count')
    concept = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='concept')
    count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='count')


class ConceptPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'show_total', 'list_concept')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    show_total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='showTotal')
    list_concept = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Concept'))), graphql_name='listConcept')


class ConceptPropertyPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_concept_property')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_concept_property = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptProperty'))), graphql_name='listConceptProperty')


class ConceptPropertyTypePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_concept_property_type', 'total')
    list_concept_property_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptPropertyType'))), graphql_name='listConceptPropertyType')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class ConceptPropertyValueStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_concept_type', 'count_link_type', 'count_dictionary', 'count_regexp')
    count_concept_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countConceptType')
    count_link_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countLinkType')
    count_dictionary = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDictionary')
    count_regexp = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countRegexp')


class ConceptStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_properties', 'count_objects', 'count_events', 'count_document_mentions', 'count_document_facts', 'count_potential_documents', 'count_research_maps', 'count_tasks', 'count_concepts', 'count_concepts_and_documents')
    count_properties = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countProperties')
    count_objects = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countObjects')
    count_events = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countEvents')
    count_document_mentions = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocumentMentions')
    count_document_facts = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocumentFacts')
    count_potential_documents = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countPotentialDocuments')
    count_research_maps = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countResearchMaps')
    count_tasks = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countTasks')
    count_concepts = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countConcepts')
    count_concepts_and_documents = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countConceptsAndDocuments')


class ConceptSubscriptions(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('subscriptions', 'list_user', 'count_users')
    subscriptions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptUpdate))), graphql_name='subscriptions')
    list_user = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('User'))), graphql_name='listUser')
    count_users = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countUsers')


class ConceptTypePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_concept_type', 'total')
    list_concept_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptType'))), graphql_name='listConceptType')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class ConceptTypeStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_property_type', 'count_link_type', 'count_dictionary', 'count_regexp')
    count_property_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countPropertyType')
    count_link_type = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countLinkType')
    count_dictionary = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDictionary')
    count_regexp = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countRegexp')


class ConceptTypeViewPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_concept_type_view', 'total')
    list_concept_type_view = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptTypeView'))), graphql_name='listConceptTypeView')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class ConceptView(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept', 'rows')
    concept = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='concept')
    rows = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptViewValue'))))), graphql_name='rows')


class ConceptViewPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_concept_view')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_concept_view = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptView))), graphql_name='listConceptView')


class Coordinates(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('latitude', 'longitude')
    latitude = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='latitude')
    longitude = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='longitude')


class Date(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('year', 'month', 'day')
    year = sgqlc.types.Field(Int, graphql_name='year')
    month = sgqlc.types.Field(Int, graphql_name='month')
    day = sgqlc.types.Field(Int, graphql_name='day')


class DateTimeInterval(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field('DateTimeValue', graphql_name='start')
    end = sgqlc.types.Field('DateTimeValue', graphql_name='end')


class DateTimeValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('date', 'time')
    date = sgqlc.types.Field(sgqlc.types.non_null(Date), graphql_name='date')
    time = sgqlc.types.Field('Time', graphql_name='time')


class DictValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class DocSpecificMetadata(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('category', 'last_printed_date', 'last_modified_by', 'created_date', 'comments', 'author', 'document_subject', 'keywords', 'modified_data', 'doc_name')
    category = sgqlc.types.Field(String, graphql_name='category')
    last_printed_date = sgqlc.types.Field(UnixTime, graphql_name='lastPrintedDate')
    last_modified_by = sgqlc.types.Field(String, graphql_name='lastModifiedBy')
    created_date = sgqlc.types.Field(UnixTime, graphql_name='createdDate')
    comments = sgqlc.types.Field(String, graphql_name='comments')
    author = sgqlc.types.Field(String, graphql_name='author')
    document_subject = sgqlc.types.Field(String, graphql_name='documentSubject')
    keywords = sgqlc.types.Field(String, graphql_name='keywords')
    modified_data = sgqlc.types.Field(UnixTime, graphql_name='modifiedData')
    doc_name = sgqlc.types.Field(String, graphql_name='docName')


class DocumentLink(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('parent_id', 'child_id')
    parent_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='parentId')
    child_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='childId')


class DocumentMetadata(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('file_name', 'size', 'file_type', 'modified_time', 'created_time', 'access_time', 'doc_specific_metadata', 'pdf_specific_metadata', 'image_specific_metadata', 'source', 'language', 'job_id', 'periodic_job_id', 'task_id', 'periodic_task_id', 'platform', 'account')
    file_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileName')
    size = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='size')
    file_type = sgqlc.types.Field(String, graphql_name='fileType')
    modified_time = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='modifiedTime')
    created_time = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='createdTime')
    access_time = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='accessTime')
    doc_specific_metadata = sgqlc.types.Field(DocSpecificMetadata, graphql_name='docSpecificMetadata')
    pdf_specific_metadata = sgqlc.types.Field('PdfSpecificMetadataGQL', graphql_name='pdfSpecificMetadata')
    image_specific_metadata = sgqlc.types.Field('ImageSpecificMetadataGQL', graphql_name='imageSpecificMetadata')
    source = sgqlc.types.Field(String, graphql_name='source')
    language = sgqlc.types.Field('Language', graphql_name='language')
    job_id = sgqlc.types.Field(String, graphql_name='jobId')
    periodic_job_id = sgqlc.types.Field(String, graphql_name='periodicJobId')
    task_id = sgqlc.types.Field(String, graphql_name='taskId')
    periodic_task_id = sgqlc.types.Field(String, graphql_name='periodicTaskId')
    platform = sgqlc.types.Field('Platform', graphql_name='platform')
    account = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Account'))), graphql_name='account')


class DocumentPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_document', 'total')
    list_document = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Document'))), graphql_name='listDocument')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class DocumentSubscriptions(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('subscriptions', 'list_user', 'count_users')
    subscriptions = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DocumentUpdate))), graphql_name='subscriptions')
    list_user = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('User'))), graphql_name='listUser')
    count_users = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countUsers')


class DoubleValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='value')


class Facet(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value', 'count')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')
    count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='count')


class FactInterface(sgqlc.types.Interface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'mention', 'system_registration_date', 'system_update_date', 'document')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    mention = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TextBounding'))), graphql_name='mention')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')
    document = sgqlc.types.Field(sgqlc.types.non_null('Document'), graphql_name='document')


class FlatDocumentStructure(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('text', 'annotations', 'metadata', 'document_id', 'node_id', 'hierarchy_level', 'translated_text', 'id', 'language')
    text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='text')
    annotations = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Annotation))), graphql_name='annotations')
    metadata = sgqlc.types.Field(sgqlc.types.non_null('ParagraphMetadata'), graphql_name='metadata')
    document_id = sgqlc.types.Field(ID, graphql_name='documentId')
    node_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='nodeId')
    hierarchy_level = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='hierarchyLevel')
    translated_text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='translatedText')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    language = sgqlc.types.Field('Language', graphql_name='language')


class GeoPointValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('point', 'name')
    point = sgqlc.types.Field(Coordinates, graphql_name='point')
    name = sgqlc.types.Field(String, graphql_name='name')


class Group(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'x_coordinate', 'y_coordinate', 'collapsed', 'layout')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    x_coordinate = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xCoordinate')
    y_coordinate = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yCoordinate')
    collapsed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='collapsed')
    layout = sgqlc.types.Field(String, graphql_name='layout')


class HLAnnotation(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='start')
    end = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='end')


class Highlighting(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('highlighting', 'annotations')
    highlighting = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='highlighting')
    annotations = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(HLAnnotation))), graphql_name='annotations')


class Image(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('url',)
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')


class ImageSpecificMetadataGQL(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('height', 'width', 'orientation')
    height = sgqlc.types.Field(Long, graphql_name='height')
    width = sgqlc.types.Field(Long, graphql_name='width')
    orientation = sgqlc.types.Field(Int, graphql_name='orientation')


class IntValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='value')


class IssueChangePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_issue_change')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_issue_change = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('IssueChange'))), graphql_name='listIssueChange')


class IssueInfo(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('topic', 'description', 'status', 'priority', 'execution_time_limit', 'markers', 'executor', 'list_concept', 'list_document', 'list_issue')
    topic = sgqlc.types.Field(String, graphql_name='topic')
    description = sgqlc.types.Field(String, graphql_name='description')
    status = sgqlc.types.Field(IssueStatus, graphql_name='status')
    priority = sgqlc.types.Field(IssuePriority, graphql_name='priority')
    execution_time_limit = sgqlc.types.Field(UnixTime, graphql_name='executionTimeLimit')
    markers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='markers')
    executor = sgqlc.types.Field('User', graphql_name='executor')
    list_concept = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Concept')), graphql_name='listConcept')
    list_document = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Document')), graphql_name='listDocument')
    list_issue = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Issue')), graphql_name='listIssue')


class IssuePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_issue', 'total')
    list_issue = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Issue'))), graphql_name='listIssue')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class IssueStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_concept', 'count_doc', 'count_issue')
    count_concept = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countConcept')
    count_doc = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDoc')
    count_issue = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countIssue')


class Language(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class LinkValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('link',)
    link = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='link')


class ListsTextsFromDocumentWithMarkerResponse(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('marker_text', 'not_marker_text')
    marker_text = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markerText')
    not_marker_text = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='notMarkerText')


class MapEdge(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('from_id', 'to_id', 'link_type', 'id', 'link')
    from_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='fromID')
    to_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='toID')
    link_type = sgqlc.types.Field(sgqlc.types.non_null(MapEdgeType), graphql_name='linkType')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    link = sgqlc.types.Field(sgqlc.types.non_null('EntityLink'), graphql_name='link')


class MapNode(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'group_id', 'x_coordinate', 'y_coordinate', 'node_type', 'entity')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    group_id = sgqlc.types.Field(ID, graphql_name='groupId')
    x_coordinate = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xCoordinate')
    y_coordinate = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yCoordinate')
    node_type = sgqlc.types.Field(sgqlc.types.non_null(MapNodeType), graphql_name='nodeType')
    entity = sgqlc.types.Field(sgqlc.types.non_null('Entity'), graphql_name='entity')


class Mention(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'document_id', 'text_bounding', 'verifier', 'system_registration_date', 'system_update_date', 'access_level')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    document_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='documentId')
    text_bounding = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TextBounding'))), graphql_name='textBounding')
    verifier = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='verifier')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')


class MergedConcept(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('concept', 'merge_author', 'merge_date')
    concept = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='concept')
    merge_author = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='mergeAuthor')
    merge_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='mergeDate')


class MergedConceptPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_merged_concept')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_merged_concept = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MergedConcept))), graphql_name='listMergedConcept')


class Metrics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_objects', 'count_events', 'count_entities', 'count_named_entities', 'count_disambiguated_entities', 'count_links', 'count_research_maps', 'count_child_docs', 'count_tasks', 'count_concepts')
    count_objects = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countObjects')
    count_events = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countEvents')
    count_entities = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countEntities')
    count_named_entities = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countNamedEntities')
    count_disambiguated_entities = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDisambiguatedEntities')
    count_links = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countLinks')
    count_research_maps = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countResearchMaps')
    count_child_docs = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countChildDocs')
    count_tasks = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countTasks')
    count_concepts = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countConcepts')


class Mutation(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('add_alias_to_concept', 'get_or_add_account', 'get_or_add_platform', 'get_or_add_concept')
    add_alias_to_concept = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='addAliasToConcept', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(AliasCreateInput), graphql_name='form', default=None)),
))
    )
    get_or_add_account = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='getOrAddAccount', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(AccountGetOrCreateInput), graphql_name='form', default=None)),
))
    )
    get_or_add_platform = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='getOrAddPlatform', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(PlatformGetOrCreateInput), graphql_name='form', default=None)),
))
    )
    get_or_add_concept = sgqlc.types.Field(sgqlc.types.non_null('Concept'), graphql_name='getOrAddConcept', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptFilterSettings), graphql_name='filterSettings', default=None)),
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(ConceptMutationInput), graphql_name='form', default=None)),
        ('file', sgqlc.types.Arg(Upload, graphql_name='file', default=None)),
        ('take_first_result', sgqlc.types.Arg(Boolean, graphql_name='takeFirstResult', default=False)),
))
    )


class NERCRegexp(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('regexp', 'context_regexp', 'auto_create')
    regexp = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='regexp')
    context_regexp = sgqlc.types.Field(String, graphql_name='contextRegexp')
    auto_create = sgqlc.types.Field(Boolean, graphql_name='autoCreate')


class NamedValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'property_value_type', 'value')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    property_value_type = sgqlc.types.Field(sgqlc.types.non_null(CompositePropertyValueType), graphql_name='propertyValueType')
    value = sgqlc.types.Field(sgqlc.types.non_null('Value'), graphql_name='value')


class ParagraphMetadata(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('page_id', 'line_id', 'original_text', 'hidden', 'text_translations', 'paragraph_type')
    page_id = sgqlc.types.Field(Int, graphql_name='pageId')
    line_id = sgqlc.types.Field(Int, graphql_name='lineId')
    original_text = sgqlc.types.Field(String, graphql_name='originalText')
    hidden = sgqlc.types.Field(Boolean, graphql_name='hidden')
    text_translations = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('Translation')), graphql_name='textTranslations')
    paragraph_type = sgqlc.types.Field(sgqlc.types.non_null(NodeType), graphql_name='paragraphType')


class Parameter(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class PdfSpecificMetadataGQL(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('author', 'creation_date')
    author = sgqlc.types.Field(String, graphql_name='author')
    creation_date = sgqlc.types.Field(UnixTime, graphql_name='creationDate')


class PlatformFacet(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value', 'count')
    value = sgqlc.types.Field(sgqlc.types.non_null('Platform'), graphql_name='value')
    count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='count')


class PlatformStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('count_account', 'count_doc', 'count_doc_today', 'count_doc_week', 'count_doc_month', 'recall_doc_today', 'recall_doc_week', 'recall_doc_month')
    count_account = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countAccount')
    count_doc = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDoc')
    count_doc_today = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocToday')
    count_doc_week = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocWeek')
    count_doc_month = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDocMonth')
    recall_doc_today = sgqlc.types.Field(sgqlc.types.non_null(DocumentRecall), graphql_name='recallDocToday')
    recall_doc_week = sgqlc.types.Field(sgqlc.types.non_null(DocumentRecall), graphql_name='recallDocWeek')
    recall_doc_month = sgqlc.types.Field(sgqlc.types.non_null(DocumentRecall), graphql_name='recallDocMonth')


class Query(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('mention_search', 'batch_mention_search', 'list_document_for_time_period', 'list_text_from_document_with_marker', 'pagination_concept_without_elastic', 'pagination_concept', 'pagination_concept_property_type')
    mention_search = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptMentionCount))), graphql_name='mentionSearch', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(ConceptMentionCountInput), graphql_name='form', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=5)),
        ('extend_results', sgqlc.types.Arg(Boolean, graphql_name='extendResults', default=False)),
))
    )
    batch_mention_search = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptMentionCount))))), graphql_name='batchMentionSearch', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(ConceptMentionCountBatchInput), graphql_name='form', default=None)),
))
    )
    list_document_for_time_period = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Document'))), graphql_name='listDocumentForTimePeriod', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(DocumentsWithConceptByDateInput), graphql_name='form', default=None)),
))
    )
    list_text_from_document_with_marker = sgqlc.types.Field(sgqlc.types.non_null(ListsTextsFromDocumentWithMarkerResponse), graphql_name='listTextFromDocumentWithMarker', args=sgqlc.types.ArgDict((
        ('form', sgqlc.types.Arg(sgqlc.types.non_null(DocumentsTextWithMarkerByDateInput), graphql_name='form', default=None)),
))
    )
    pagination_concept_without_elastic = sgqlc.types.Field(sgqlc.types.non_null(ConceptPagination), graphql_name='paginationConceptWithoutElastic', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptFilterSettings), graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(ConceptSorting, graphql_name='sortField', default='score')),
))
    )
    pagination_concept = sgqlc.types.Field(ConceptPagination, graphql_name='paginationConcept', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('query', sgqlc.types.Arg(String, graphql_name='query', default=None)),
        ('filter_settings', sgqlc.types.Arg(ConceptFilterSettings, graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(ConceptSorting, graphql_name='sortField', default='score')),
))
    )
    pagination_concept_property_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyTypePagination), graphql_name='paginationConceptPropertyType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyTypeFilterSettings), graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(ConceptPropertyTypeSorting, graphql_name='sortField', default='name')),
))
    )


class RecordInterface(sgqlc.types.Interface):
    __schema__ = utils_api_schema
    __field_names__ = ('system_registration_date', 'system_update_date', 'creator', 'last_updater')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')
    creator = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='creator')
    last_updater = sgqlc.types.Field('User', graphql_name='lastUpdater')


class RedmineIssue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'subject', 'tracker', 'status', 'priority', 'author', 'assignee', 'creation_date')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    subject = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='subject')
    tracker = sgqlc.types.Field(sgqlc.types.non_null('RedmineTracker'), graphql_name='tracker')
    status = sgqlc.types.Field(sgqlc.types.non_null('RedmineStatus'), graphql_name='status')
    priority = sgqlc.types.Field(sgqlc.types.non_null('RedminePriority'), graphql_name='priority')
    author = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='author')
    assignee = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='assignee')
    creation_date = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='creationDate')


class RedmineIssuePagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_redmine_issue', 'total')
    list_redmine_issue = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RedmineIssue))), graphql_name='listRedmineIssue')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')


class RedminePriority(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class RedmineStatus(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class RedmineTracker(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class RelExtModel(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('source_annotation_type', 'target_annotation_type', 'relation_type', 'invert_direction')
    source_annotation_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='sourceAnnotationType')
    target_annotation_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='targetAnnotationType')
    relation_type = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='relationType')
    invert_direction = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='invertDirection')


class ResearchMapPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('total', 'list_research_map')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')
    list_research_map = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ResearchMap'))), graphql_name='listResearchMap')


class ResearchMapStatistics(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('object_num', 'event_num', 'document_num', 'concept_num', 'concept_and_document_num')
    object_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='objectNum')
    event_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='eventNum')
    document_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='documentNum')
    concept_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='conceptNum')
    concept_and_document_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='conceptAndDocumentNum')


class State(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('is_success',)
    is_success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isSuccess')


class Story(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'title', 'system_registration_date', 'system_update_date', 'main', 'list_document', 'highlighting', 'count_doc', 'preview', 'access_level')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')
    main = sgqlc.types.Field(sgqlc.types.non_null('Document'), graphql_name='main')
    list_document = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Document'))), graphql_name='listDocument')
    highlighting = sgqlc.types.Field(Highlighting, graphql_name='highlighting')
    count_doc = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='countDoc')
    preview = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='preview')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')


class StoryPagination(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('list_story', 'total', 'show_total', 'list_named_entity_count_facet', 'list_concept_count_facet', 'list_account_count_facet', 'list_platform_count_facet', 'list_markers', 'sources', 'new_documents_today')
    list_story = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Story))), graphql_name='listStory')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')
    show_total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='showTotal')
    list_named_entity_count_facet = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Facet))), graphql_name='listNamedEntityCountFacet')
    list_concept_count_facet = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Facet))), graphql_name='listConceptCountFacet')
    list_account_count_facet = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AccountFacet))), graphql_name='listAccountCountFacet')
    list_platform_count_facet = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(PlatformFacet))), graphql_name='listPlatformCountFacet')
    list_markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Facet))), graphql_name='listMarkers')
    sources = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='sources')
    new_documents_today = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='newDocumentsToday')


class StringLocaleValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value', 'locale')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')
    locale = sgqlc.types.Field(sgqlc.types.non_null(Locale), graphql_name='locale')


class StringValue(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('value',)
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class Table(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('cells', 'metadata')
    cells = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))))), graphql_name='cells')
    metadata = sgqlc.types.Field(sgqlc.types.non_null('TableMetadata'), graphql_name='metadata')


class TableMetadata(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('page_id',)
    page_id = sgqlc.types.Field(Int, graphql_name='pageId')


class TextBounding(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('start', 'end', 'node_id')
    start = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='start')
    end = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='end')
    node_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='nodeId')


class Time(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('hour', 'minute', 'second')
    hour = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='hour')
    minute = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='minute')
    second = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='second')


class Translation(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('text', 'language')
    text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='text')
    language = sgqlc.types.Field(sgqlc.types.non_null(Language), graphql_name='language')


class User(sgqlc.types.Type):
    __schema__ = utils_api_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class Account(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'url', 'country', 'markers', 'params', 'platform', 'image', 'metric', 'period')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    country = sgqlc.types.Field(String, graphql_name='country')
    markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markers')
    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Parameter))), graphql_name='params')
    platform = sgqlc.types.Field(sgqlc.types.non_null('Platform'), graphql_name='platform')
    image = sgqlc.types.Field(Image, graphql_name='image')
    metric = sgqlc.types.Field(sgqlc.types.non_null(AccountStatistics), graphql_name='metric')
    period = sgqlc.types.Field(sgqlc.types.non_null(DateTimeInterval), graphql_name='period')


class CompositeConceptType(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'root_concept_type', 'is_default', 'layout', 'has_supporting_documents', 'has_header_information', 'metric', 'pagination_widget_type', 'list_widget_type', 'list_concept_link_types_composite_concept_type_consists_of', 'show_in_menu', 'internal_url')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    root_concept_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptType'), graphql_name='rootConceptType')
    is_default = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDefault')
    layout = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='layout')
    has_supporting_documents = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasSupportingDocuments')
    has_header_information = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasHeaderInformation')
    metric = sgqlc.types.Field(sgqlc.types.non_null(CompositeConceptStatistics), graphql_name='metric')
    pagination_widget_type = sgqlc.types.Field(sgqlc.types.non_null(CompositeConceptTypeWidgetTypePagination), graphql_name='paginationWidgetType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='ascending')),
        ('sorting', sgqlc.types.Arg(CompositeConceptTypeWidgetTypeSorting, graphql_name='sorting', default='order')),
))
    )
    list_widget_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('CompositeConceptTypeWidgetType'))), graphql_name='listWidgetType')
    list_concept_link_types_composite_concept_type_consists_of = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptLinkType'))), graphql_name='listConceptLinkTypesCompositeConceptTypeConsistsOf')
    show_in_menu = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='showInMenu')
    internal_url = sgqlc.types.Field(String, graphql_name='internalUrl')


class CompositeConceptTypeWidgetType(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'table_type', 'composite_concept_type', 'hierarchy', 'columns_info')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    table_type = sgqlc.types.Field(sgqlc.types.non_null(WidgetTypeTableType), graphql_name='tableType')
    composite_concept_type = sgqlc.types.Field(sgqlc.types.non_null(CompositeConceptType), graphql_name='compositeConceptType')
    hierarchy = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptLinkTypePath))))), graphql_name='hierarchy')
    columns_info = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CompositeConceptTypeWidgetTypeColumn))), graphql_name='columnsInfo')


class CompositePropertyValueTemplate(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'component_value_types')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    component_value_types = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CompositePropertyValueType))), graphql_name='componentValueTypes')


class Concept(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'is_actual', 'name', 'notes', 'markers', 'start_date', 'end_date', 'concept_type', 'pagination_concept_property', 'pagination_concept_link', 'pagination_concept_fact', 'pagination_concept_property_documents', 'pagination_concept_link_documents', 'list_concept_fact', 'image', 'metric', 'list_alias', 'pagination_alias', 'pagination_merged_concept', 'list_header_concept_property', 'pagination_redmine_issues', 'pagination_issue', 'access_level', 'list_subscription', 'pagination_research_map')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    is_actual = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActual')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markers')
    start_date = sgqlc.types.Field(DateTimeValue, graphql_name='startDate')
    end_date = sgqlc.types.Field(DateTimeValue, graphql_name='endDate')
    concept_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptType'), graphql_name='conceptType')
    pagination_concept_property = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyPagination), graphql_name='paginationConceptProperty', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyFilterSettings), graphql_name='filterSettings', default=None)),
))
    )
    pagination_concept_link = sgqlc.types.Field(sgqlc.types.non_null(ConceptLinkPagination), graphql_name='paginationConceptLink', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptLinkFilterSettings), graphql_name='filterSettings', default=None)),
))
    )
    pagination_concept_fact = sgqlc.types.Field(sgqlc.types.non_null(ConceptFactPagination), graphql_name='paginationConceptFact', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(DocumentLinkFilterSetting), graphql_name='filterSettings', default=None)),
))
    )
    pagination_concept_property_documents = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationConceptPropertyDocuments', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyFilterSettings), graphql_name='filterSettings', default=None)),
))
    )
    pagination_concept_link_documents = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationConceptLinkDocuments', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptLinkFilterSettings), graphql_name='filterSettings', default=None)),
))
    )
    list_concept_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptFact'))), graphql_name='listConceptFact')
    image = sgqlc.types.Field(Image, graphql_name='image')
    metric = sgqlc.types.Field(sgqlc.types.non_null(ConceptStatistics), graphql_name='metric')
    list_alias = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptProperty'))), graphql_name='listAlias')
    pagination_alias = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyPagination), graphql_name='paginationAlias', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    pagination_merged_concept = sgqlc.types.Field(sgqlc.types.non_null(MergedConceptPagination), graphql_name='paginationMergedConcept', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    list_header_concept_property = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptProperty'))), graphql_name='listHeaderConceptProperty')
    pagination_redmine_issues = sgqlc.types.Field(sgqlc.types.non_null(RedmineIssuePagination), graphql_name='paginationRedmineIssues', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='ascending')),
))
    )
    pagination_issue = sgqlc.types.Field(sgqlc.types.non_null(IssuePagination), graphql_name='paginationIssue', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(IssueFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(sgqlc.types.non_null(SortDirection), graphql_name='sortDirection', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.non_null(IssueSorting), graphql_name='sorting', default=None)),
))
    )
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    list_subscription = sgqlc.types.Field(sgqlc.types.non_null(ConceptSubscriptions), graphql_name='listSubscription')
    pagination_research_map = sgqlc.types.Field(sgqlc.types.non_null(ResearchMapPagination), graphql_name='paginationResearchMap', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ResearchMapFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(sgqlc.types.non_null(SortDirection), graphql_name='sortDirection', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.non_null(ResearchMapSorting), graphql_name='sorting', default=None)),
))
    )


class ConceptCandidateFact(sgqlc.types.Type, FactInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('name', 'concept_type', 'list_concept')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    concept_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptType'), graphql_name='conceptType')
    list_concept = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Concept))), graphql_name='listConcept')


class ConceptFact(sgqlc.types.Type, FactInterface, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('access_level', 'concept')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    concept = sgqlc.types.Field(sgqlc.types.non_null(Concept), graphql_name='concept')


class ConceptLink(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'concept_from_id', 'concept_to_id', 'notes', 'start_date', 'end_date', 'concept_from', 'concept_to', 'concept_link_type', 'pagination_concept_link_property', 'pagination_concept_link_property_documents', 'pagination_document', 'list_concept_link_fact', 'access_level')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    concept_from_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptFromId')
    concept_to_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='conceptToId')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    start_date = sgqlc.types.Field(DateTimeValue, graphql_name='startDate')
    end_date = sgqlc.types.Field(DateTimeValue, graphql_name='endDate')
    concept_from = sgqlc.types.Field(sgqlc.types.non_null(Concept), graphql_name='conceptFrom')
    concept_to = sgqlc.types.Field(sgqlc.types.non_null(Concept), graphql_name='conceptTo')
    concept_link_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptLinkType'), graphql_name='conceptLinkType')
    pagination_concept_link_property = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyPagination), graphql_name='paginationConceptLinkProperty', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyFilterSettings), graphql_name='filterSettings', default=None)),
))
    )
    pagination_concept_link_property_documents = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationConceptLinkPropertyDocuments', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyFilterSettings), graphql_name='filterSettings', default=None)),
))
    )
    pagination_document = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationDocument', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    list_concept_link_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptLinkFact'))), graphql_name='listConceptLinkFact')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')


class ConceptLinkCandidateFact(sgqlc.types.Type, FactInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_link_type', 'fact_from', 'fact_to')
    concept_link_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptLinkType'), graphql_name='conceptLinkType')
    fact_from = sgqlc.types.Field('ConceptLikeFact', graphql_name='factFrom')
    fact_to = sgqlc.types.Field('ConceptLikeFact', graphql_name='factTo')


class ConceptLinkFact(sgqlc.types.Type, FactInterface, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('access_level', 'concept_link')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    concept_link = sgqlc.types.Field(sgqlc.types.non_null(ConceptLink), graphql_name='conceptLink')


class ConceptLinkPropertyFact(sgqlc.types.Type, FactInterface, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('parent_concept_link', 'access_level', 'concept_link_property')
    parent_concept_link = sgqlc.types.Field(sgqlc.types.non_null(ConceptLink), graphql_name='parentConceptLink')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    concept_link_property = sgqlc.types.Field(sgqlc.types.non_null('ConceptProperty'), graphql_name='conceptLinkProperty')


class ConceptLinkType(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'is_directed', 'is_hierarchical', 'concept_from_type', 'concept_to_type', 'pretrained_rel_ext_models', 'notify_on_update', 'pagination_concept_link_property_type', 'list_concept_link_property_type', 'metric')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    is_directed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isDirected')
    is_hierarchical = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isHierarchical')
    concept_from_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptType'), graphql_name='conceptFromType')
    concept_to_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptType'), graphql_name='conceptToType')
    pretrained_rel_ext_models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RelExtModel))), graphql_name='pretrainedRelExtModels')
    notify_on_update = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='notifyOnUpdate')
    pagination_concept_link_property_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyTypePagination), graphql_name='paginationConceptLinkPropertyType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyTypeFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(sgqlc.types.non_null(SortDirection), graphql_name='sortDirection', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.non_null(ConceptTypeSorting), graphql_name='sorting', default=None)),
))
    )
    list_concept_link_property_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptPropertyType'))), graphql_name='listConceptLinkPropertyType')
    metric = sgqlc.types.Field(sgqlc.types.non_null(ConceptLinkTypeStatistics), graphql_name='metric')


class ConceptProperty(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'is_main', 'property_type', 'notes', 'start_date', 'end_date', 'pagination_document', 'access_level', 'value', 'list_concept_property_fact')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    is_main = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isMain')
    property_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptPropertyType'), graphql_name='propertyType')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    start_date = sgqlc.types.Field(DateTimeValue, graphql_name='startDate')
    end_date = sgqlc.types.Field(DateTimeValue, graphql_name='endDate')
    pagination_document = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationDocument', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    value = sgqlc.types.Field(sgqlc.types.non_null('AnyValue'), graphql_name='value')
    list_concept_property_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptPropertyLikeFact'))), graphql_name='listConceptPropertyFact')


class ConceptPropertyCandidateFact(sgqlc.types.Type, FactInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_property_type', 'fact_to', 'fact_from')
    concept_property_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptPropertyType'), graphql_name='conceptPropertyType')
    fact_to = sgqlc.types.Field(sgqlc.types.non_null('ConceptPropertyValueCandidateFact'), graphql_name='factTo')
    fact_from = sgqlc.types.Field('ConceptLikeFact', graphql_name='factFrom')


class ConceptPropertyFact(sgqlc.types.Type, FactInterface, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('parent_concept', 'access_level', 'concept_property')
    parent_concept = sgqlc.types.Field(sgqlc.types.non_null(Concept), graphql_name='parentConcept')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    concept_property = sgqlc.types.Field(sgqlc.types.non_null(ConceptProperty), graphql_name='conceptProperty')


class ConceptPropertyType(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'pretrained_rel_ext_models', 'notify_on_update', 'computable_formula', 'parent_concept_type', 'parent_concept_link_type', 'value_type')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    pretrained_rel_ext_models = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RelExtModel))), graphql_name='pretrainedRelExtModels')
    notify_on_update = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='notifyOnUpdate')
    computable_formula = sgqlc.types.Field(String, graphql_name='computableFormula')
    parent_concept_type = sgqlc.types.Field('ConceptType', graphql_name='parentConceptType')
    parent_concept_link_type = sgqlc.types.Field(ConceptLinkType, graphql_name='parentConceptLinkType')
    value_type = sgqlc.types.Field(sgqlc.types.non_null('AnyValueType'), graphql_name='valueType')


class ConceptPropertyValueCandidateFact(sgqlc.types.Type, FactInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('concept_property_value_type',)
    concept_property_value_type = sgqlc.types.Field(sgqlc.types.non_null('ConceptPropertyValueType'), graphql_name='conceptPropertyValueType')


class ConceptPropertyValueType(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'value_type', 'list_white_dictionary', 'pretrained_nercmodels', 'list_white_regexp', 'value_restriction', 'list_black_dictionary', 'metric', 'list_concept_type', 'pagination_concept_type', 'list_concept_link_type', 'pagination_concept_link_type', 'list_black_regexp', 'list_type_search_element', 'list_type_black_search_element')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    value_type = sgqlc.types.Field(sgqlc.types.non_null(ValueType), graphql_name='valueType')
    list_white_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listWhiteDictionary')
    pretrained_nercmodels = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='pretrainedNERCModels')
    list_white_regexp = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(NERCRegexp))), graphql_name='listWhiteRegexp')
    value_restriction = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='valueRestriction')
    list_black_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listBlackDictionary')
    metric = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyValueStatistics), graphql_name='metric')
    list_concept_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('ConceptType'))), graphql_name='listConceptType')
    pagination_concept_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptTypePagination), graphql_name='paginationConceptType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    list_concept_link_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptLinkType))), graphql_name='listConceptLinkType')
    pagination_concept_link_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptLinkTypePagination), graphql_name='paginationConceptLinkType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    list_black_regexp = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(NERCRegexp))), graphql_name='listBlackRegexp')
    list_type_search_element = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TypeSearchElement'))), graphql_name='listTypeSearchElement')
    list_type_black_search_element = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TypeSearchElement'))), graphql_name='listTypeBlackSearchElement')


class ConceptType(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'x_coordinate', 'y_coordinate', 'list_white_dictionary', 'pretrained_nercmodels', 'list_white_regexp', 'is_event', 'list_black_dictionary', 'pagination_concept_property_type', 'metric', 'pagination_concept_link_type', 'pagination_concept_type_view', 'list_composite_concept_type', 'list_concept_property_type', 'list_concept_link_type', 'list_concept_header_property_type', 'image', 'full_dictionary', 'non_configurable_dictionary', 'show_in_menu', 'list_black_regexp', 'list_names_dictionary', 'list_type_search_element', 'list_type_black_search_element')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    x_coordinate = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xCoordinate')
    y_coordinate = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yCoordinate')
    list_white_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listWhiteDictionary')
    pretrained_nercmodels = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='pretrainedNERCModels')
    list_white_regexp = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(NERCRegexp))), graphql_name='listWhiteRegexp')
    is_event = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isEvent')
    list_black_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listBlackDictionary')
    pagination_concept_property_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptPropertyTypePagination), graphql_name='paginationConceptPropertyType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptPropertyTypeFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='descending')),
        ('sorting', sgqlc.types.Arg(ConceptPropertyTypeSorting, graphql_name='sorting', default='name')),
))
    )
    metric = sgqlc.types.Field(sgqlc.types.non_null(ConceptTypeStatistics), graphql_name='metric')
    pagination_concept_link_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptLinkTypePagination), graphql_name='paginationConceptLinkType', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptLinkTypeFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='descending')),
        ('sorting', sgqlc.types.Arg(ConceptLinkTypeSorting, graphql_name='sorting', default='id')),
))
    )
    pagination_concept_type_view = sgqlc.types.Field(sgqlc.types.non_null(ConceptTypeViewPagination), graphql_name='paginationConceptTypeView', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
))
    )
    list_composite_concept_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CompositeConceptType))), graphql_name='listCompositeConceptType')
    list_concept_property_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptPropertyType))), graphql_name='listConceptPropertyType')
    list_concept_link_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptLinkType))), graphql_name='listConceptLinkType')
    list_concept_header_property_type = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptPropertyType))), graphql_name='listConceptHeaderPropertyType')
    image = sgqlc.types.Field(Image, graphql_name='image')
    full_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='fullDictionary')
    non_configurable_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='nonConfigurableDictionary')
    show_in_menu = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='showInMenu')
    list_black_regexp = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(NERCRegexp))), graphql_name='listBlackRegexp')
    list_names_dictionary = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='listNamesDictionary')
    list_type_search_element = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TypeSearchElement'))), graphql_name='listTypeSearchElement')
    list_type_black_search_element = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('TypeSearchElement'))), graphql_name='listTypeBlackSearchElement')


class ConceptTypeView(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'show_in_menu', 'concept_type', 'columns', 'pagination_concept')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    show_in_menu = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='showInMenu')
    concept_type = sgqlc.types.Field(sgqlc.types.non_null(ConceptType), graphql_name='conceptType')
    columns = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CompositeConceptTypeWidgetTypeColumn))), graphql_name='columns')
    pagination_concept = sgqlc.types.Field(sgqlc.types.non_null(ConceptViewPagination), graphql_name='paginationConcept', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_column', sgqlc.types.Arg(ID, graphql_name='sortColumn', default=None)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='descending')),
        ('query', sgqlc.types.Arg(String, graphql_name='query', default=None)),
        ('filter_settings', sgqlc.types.Arg(ConceptFilterSettings, graphql_name='filterSettings', default=None)),
))
    )


class Document(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'title', 'external_url', 'publication_date', 'publication_author', 'notes', 'document_type', 'highlightings', 'markers', 'tables', 'metadata', 'uuid', 'trust_level', 'score', 'has_text', 'parent', 'list_child', 'pagination_child', 'internal_url', 'avatar', 'metric', 'pagination_concept_fact', 'list_concept_fact', 'pagination_concept_link_fact', 'list_concept_link_document_fact', 'preview', 'pagination_redmine_issues', 'pagination_issue', 'access_level', 'text', 'story', 'list_subscription', 'pagination_similar_documents', 'is_read', 'list_fact')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(String, graphql_name='title')
    external_url = sgqlc.types.Field(String, graphql_name='externalUrl')
    publication_date = sgqlc.types.Field(UnixTime, graphql_name='publicationDate')
    publication_author = sgqlc.types.Field(String, graphql_name='publicationAuthor')
    notes = sgqlc.types.Field(String, graphql_name='notes')
    document_type = sgqlc.types.Field(sgqlc.types.non_null(DocumentType), graphql_name='documentType')
    highlightings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Highlighting))), graphql_name='highlightings')
    markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markers')
    tables = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Table))), graphql_name='tables')
    metadata = sgqlc.types.Field(DocumentMetadata, graphql_name='metadata')
    uuid = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='uuid')
    trust_level = sgqlc.types.Field(TrustLevel, graphql_name='trustLevel')
    score = sgqlc.types.Field(Float, graphql_name='score')
    has_text = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='hasText')
    parent = sgqlc.types.Field('Document', graphql_name='parent')
    list_child = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Document'))), graphql_name='listChild')
    pagination_child = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationChild', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(DocumentLinkFilterSetting), graphql_name='filterSettings', default=None)),
))
    )
    internal_url = sgqlc.types.Field(String, graphql_name='internalUrl')
    avatar = sgqlc.types.Field(Image, graphql_name='avatar')
    metric = sgqlc.types.Field(sgqlc.types.non_null(Metrics), graphql_name='metric')
    pagination_concept_fact = sgqlc.types.Field(sgqlc.types.non_null(ConceptFactPagination), graphql_name='paginationConceptFact', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    list_concept_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptFact))), graphql_name='listConceptFact')
    pagination_concept_link_fact = sgqlc.types.Field(sgqlc.types.non_null(ConceptLinkFactPagination), graphql_name='paginationConceptLinkFact', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    list_concept_link_document_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ConceptLinkFact))), graphql_name='listConceptLinkDocumentFact')
    preview = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='preview')
    pagination_redmine_issues = sgqlc.types.Field(sgqlc.types.non_null(RedmineIssuePagination), graphql_name='paginationRedmineIssues', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='ascending')),
))
    )
    pagination_issue = sgqlc.types.Field(sgqlc.types.non_null(IssuePagination), graphql_name='paginationIssue', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(IssueFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(sgqlc.types.non_null(SortDirection), graphql_name='sortDirection', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.non_null(IssueSorting), graphql_name='sorting', default=None)),
))
    )
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    text = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(FlatDocumentStructure))), graphql_name='text', args=sgqlc.types.ArgDict((
        ('show_hidden', sgqlc.types.Arg(Boolean, graphql_name='showHidden', default=False)),
))
    )
    story = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='story')
    list_subscription = sgqlc.types.Field(sgqlc.types.non_null(DocumentSubscriptions), graphql_name='listSubscription')
    pagination_similar_documents = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationSimilarDocuments', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    is_read = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRead')
    list_fact = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Fact'))), graphql_name='listFact')


class Issue(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'topic', 'description', 'status', 'priority', 'execution_time_limit', 'markers', 'executor', 'pagination_document', 'pagination_concept', 'pagination_issue', 'metric', 'pagination_issue_change')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    topic = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='topic')
    description = sgqlc.types.Field(String, graphql_name='description')
    status = sgqlc.types.Field(sgqlc.types.non_null(IssueStatus), graphql_name='status')
    priority = sgqlc.types.Field(sgqlc.types.non_null(IssuePriority), graphql_name='priority')
    execution_time_limit = sgqlc.types.Field(UnixTime, graphql_name='executionTimeLimit')
    markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markers')
    executor = sgqlc.types.Field(sgqlc.types.non_null(User), graphql_name='executor')
    pagination_document = sgqlc.types.Field(sgqlc.types.non_null(DocumentPagination), graphql_name='paginationDocument', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    pagination_concept = sgqlc.types.Field(sgqlc.types.non_null(ConceptPagination), graphql_name='paginationConcept', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )
    pagination_issue = sgqlc.types.Field(sgqlc.types.non_null(IssuePagination), graphql_name='paginationIssue', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(IssueFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(sgqlc.types.non_null(SortDirection), graphql_name='sortDirection', default=None)),
        ('sorting', sgqlc.types.Arg(sgqlc.types.non_null(IssueSorting), graphql_name='sorting', default=None)),
))
    )
    metric = sgqlc.types.Field(sgqlc.types.non_null(IssueStatistics), graphql_name='metric')
    pagination_issue_change = sgqlc.types.Field(sgqlc.types.non_null(IssueChangePagination), graphql_name='paginationIssueChange', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
))
    )


class IssueChange(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'from_', 'to', 'comment')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    from_ = sgqlc.types.Field(sgqlc.types.non_null(IssueInfo), graphql_name='from')
    to = sgqlc.types.Field(sgqlc.types.non_null(IssueInfo), graphql_name='to')
    comment = sgqlc.types.Field(String, graphql_name='comment')


class Platform(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'platform_type', 'url', 'country', 'language', 'markers', 'params', 'image', 'metric', 'period', 'accounts')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    platform_type = sgqlc.types.Field(sgqlc.types.non_null(PlatformType), graphql_name='platformType')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    country = sgqlc.types.Field(String, graphql_name='country')
    language = sgqlc.types.Field(String, graphql_name='language')
    markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markers')
    params = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Parameter))), graphql_name='params')
    image = sgqlc.types.Field(Image, graphql_name='image')
    metric = sgqlc.types.Field(sgqlc.types.non_null(PlatformStatistics), graphql_name='metric')
    period = sgqlc.types.Field(sgqlc.types.non_null(DateTimeInterval), graphql_name='period')
    accounts = sgqlc.types.Field(sgqlc.types.non_null(AccountPagination), graphql_name='accounts', args=sgqlc.types.ArgDict((
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(AccountFilterSettings), graphql_name='filterSettings', default=None)),
        ('sort_direction', sgqlc.types.Arg(SortDirection, graphql_name='sortDirection', default='descending')),
        ('sorting', sgqlc.types.Arg(AccountSorting, graphql_name='sorting', default='id')),
))
    )


class ResearchMap(sgqlc.types.Type, RecordInterface):
    __schema__ = utils_api_schema
    __field_names__ = ('id', 'name', 'description', 'is_temporary', 'markers', 'list_node', 'list_edge', 'research_map_statistics', 'list_group', 'is_active', 'access_level', 'pagination_concept', 'pagination_story', 'pagination_research_map')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    is_temporary = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isTemporary')
    markers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='markers')
    list_node = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MapNode))), graphql_name='listNode', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(MapNodeFilterSettings, graphql_name='filterSettings', default=None)),
        ('default_view', sgqlc.types.Arg(Boolean, graphql_name='defaultView', default=True)),
))
    )
    list_edge = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(MapEdge))), graphql_name='listEdge', args=sgqlc.types.ArgDict((
        ('filter_settings', sgqlc.types.Arg(MapEdgeFilterSettings, graphql_name='filterSettings', default=None)),
        ('default_view', sgqlc.types.Arg(Boolean, graphql_name='defaultView', default=True)),
))
    )
    research_map_statistics = sgqlc.types.Field(sgqlc.types.non_null(ResearchMapStatistics), graphql_name='researchMapStatistics')
    list_group = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Group))), graphql_name='listGroup')
    is_active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isActive')
    access_level = sgqlc.types.Field(sgqlc.types.non_null(AccessLevel), graphql_name='accessLevel')
    pagination_concept = sgqlc.types.Field(sgqlc.types.non_null(ConceptPagination), graphql_name='paginationConcept', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('query', sgqlc.types.Arg(String, graphql_name='query', default=None)),
        ('filter_settings', sgqlc.types.Arg(ConceptFilterSettings, graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(ConceptSorting, graphql_name='sortField', default=None)),
        ('extra_settings', sgqlc.types.Arg(sgqlc.types.non_null(ConceptExtraSettings), graphql_name='extraSettings', default=None)),
))
    )
    pagination_story = sgqlc.types.Field(sgqlc.types.non_null(StoryPagination), graphql_name='paginationStory', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('grouping', sgqlc.types.Arg(DocumentGrouping, graphql_name='grouping', default='none')),
        ('query', sgqlc.types.Arg(String, graphql_name='query', default=None)),
        ('filter_settings', sgqlc.types.Arg(DocumentFilterSettings, graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(DocumentSorting, graphql_name='sortField', default=None)),
        ('extra_settings', sgqlc.types.Arg(sgqlc.types.non_null(ExtraSettings), graphql_name='extraSettings', default=None)),
))
    )
    pagination_research_map = sgqlc.types.Field(sgqlc.types.non_null(ResearchMapPagination), graphql_name='paginationResearchMap', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(ResearchMapFilterSettings), graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(ResearchMapSorting, graphql_name='sortField', default='conceptAndDocumentLink')),
        ('research_map_content_select_input', sgqlc.types.Arg(ResearchMapContentUpdateInput, graphql_name='ResearchMapContentSelectInput', default=None)),
))
    )



########################################################################
# Unions
########################################################################
class AnyValue(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (DateTimeValue, GeoPointValue, IntValue, DoubleValue, StringLocaleValue, StringValue, LinkValue, CompositeValue)


class AnyValueType(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (ConceptPropertyValueType, CompositePropertyValueTemplate)


class ConceptLikeFact(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (ConceptCandidateFact, ConceptFact)


class ConceptPropertyLikeFact(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (ConceptPropertyFact, ConceptLinkPropertyFact)


class ConceptViewValue(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (DateTimeValue, GeoPointValue, IntValue, DoubleValue, StringLocaleValue, StringValue, LinkValue, CompositeValue, Concept, ConceptType, ConceptLinkType, User)


class Entity(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (Concept, Document, ConceptCandidateFact, ConceptType)


class EntityLink(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (ConceptLink, ConceptFactLink, ConceptImplicitLink, ConceptCandidateFactMention, ConceptMention, DocumentLink, ConceptLinkCandidateFact, ConceptLinkType)


class Fact(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (ConceptCandidateFact, ConceptFact, ConceptLinkCandidateFact, ConceptLinkFact, ConceptPropertyCandidateFact, ConceptPropertyFact, ConceptPropertyValueCandidateFact, ConceptLinkPropertyFact)


class TypeSearchElement(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (DictValue, NERCRegexp)


class Value(sgqlc.types.Union):
    __schema__ = utils_api_schema
    __types__ = (DateTimeValue, GeoPointValue, IntValue, DoubleValue, StringLocaleValue, StringValue, LinkValue)



########################################################################
# Schema Entry Points
########################################################################
utils_api_schema.query_type = Query
utils_api_schema.mutation_type = Mutation
utils_api_schema.subscription_type = None

