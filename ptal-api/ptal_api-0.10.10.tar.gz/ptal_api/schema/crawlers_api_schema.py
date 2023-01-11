import sgqlc.types


crawlers_api_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

class CollectionStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Canceled', 'Error', 'InProgress', 'Success', 'WithMistakes')


class CrawlerSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('avgPerformanceTime', 'id', 'lastCollectionDate', 'projectTitle', 'title')


class CrawlersType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('EggFileCrawlers', 'SitemapCrawlers')


class CredentialSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('dataType', 'domain', 'id', 'status', 'value')


class CredentialStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Invalid', 'Valid')


class CredentialType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Account', 'Token')


Float = sgqlc.types.Float

ID = sgqlc.types.ID

class InformationSourceLoaderActualStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Daily', 'EveryTwoDays', 'Never', 'Weekly')


class InformationSourceLoaderSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('id', 'status')


class InformationSourceSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('error', 'id', 'job', 'siteName', 'status', 'url')


Int = sgqlc.types.Int

class JSON(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class JobFinishedSort(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('args', 'collectionStatus', 'crawlerName', 'createdAt', 'createdBy', 'endTime', 'id', 'periodicJobId', 'projectName', 'settings', 'startTime')


class JobPendingSort(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('args', 'crawlerName', 'createdBy', 'id', 'jobPriority', 'periodicJobId', 'projectName', 'queueTime', 'settings')


class JobPriorityType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('High', 'Highest', 'Low', 'Normal')


class JobRunningSort(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('args', 'crawlerName', 'createdAt', 'createdBy', 'id', 'jobPriority', 'periodicJobId', 'projectName', 'settings', 'startTime')


class JobStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Finished', 'Pending', 'Running')


class LogLevel(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Critical', 'Debug', 'Error', 'Info', 'Trace', 'Warning')


class LogSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('level', 'timestamp')


class Long(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class MetricSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('timestamp',)


class PeriodicJobSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('changedAt', 'changedBy', 'crawlerId', 'crawlerName', 'createdAt', 'createdBy', 'id', 'name', 'nextScheduleTime', 'priority', 'projectId', 'projectName', 'status')


class PeriodicJobStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Disabled', 'Enabled')


class ProjectSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('changedAt', 'changedBy', 'createdAt', 'createdBy', 'description', 'id', 'name', 'title')


class RequestSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('timestamp',)


class SettingsType(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('array', 'boolean', 'float', 'int', 'object', 'string')


class SortDirection(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('ascending', 'descending')


String = sgqlc.types.String

class TypeOfCrawl(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Actual', 'Retrospective')


class UnixTime(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class Upload(sgqlc.types.Scalar):
    __schema__ = crawlers_api_schema


class VersionSorting(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('createdAt', 'id', 'versionName')


class VersionStatus(sgqlc.types.Enum):
    __schema__ = crawlers_api_schema
    __choices__ = ('Active', 'Outdated', 'Removed')



########################################################################
# Input Objects
########################################################################
class CrawlerFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'projects', 'crawlers_types', 'last_collection_date', 'created_by', 'changed_by', 'created_at', 'changed_at', 'have_active_versions')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    crawlers_types = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CrawlersType)), graphql_name='crawlersTypes')
    last_collection_date = sgqlc.types.Field('TimestampInterval', graphql_name='lastCollectionDate')
    created_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='createdBy')
    changed_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='changedBy')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    changed_at = sgqlc.types.Field('TimestampInterval', graphql_name='changedAt')
    have_active_versions = sgqlc.types.Field(Boolean, graphql_name='haveActiveVersions')


class CrawlerUpdateInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('project_id', 'title', 'description', 'settings', 'args', 'state', 'state_version')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='args')
    state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='state')
    state_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='stateVersion')


class CredentialFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'projects', 'status', 'data_type', 'created_by', 'changed_by', 'created_at', 'changed_at')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    status = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CredentialStatus)), graphql_name='status')
    data_type = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CredentialType)), graphql_name='dataType')
    created_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='createdBy')
    changed_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='changedBy')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    changed_at = sgqlc.types.Field('TimestampInterval', graphql_name='changedAt')


class CredentialInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('projects', 'status', 'domain', 'description', 'data_type', 'login', 'password', 'token', 'state', 'cookies')
    projects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='projects')
    status = sgqlc.types.Field(CredentialStatus, graphql_name='status')
    domain = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='domain')
    description = sgqlc.types.Field(String, graphql_name='description')
    data_type = sgqlc.types.Field(sgqlc.types.non_null(CredentialType), graphql_name='dataType')
    login = sgqlc.types.Field(String, graphql_name='login')
    password = sgqlc.types.Field(String, graphql_name='password')
    token = sgqlc.types.Field(String, graphql_name='token')
    state = sgqlc.types.Field(JSON, graphql_name='state')
    cookies = sgqlc.types.Field(JSON, graphql_name='cookies')


class FileSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('file_id', 'is_first_row_title', 'is_site_name_not_exist')
    file_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileId')
    is_first_row_title = sgqlc.types.Field(Boolean, graphql_name='isFirstRowTitle')
    is_site_name_not_exist = sgqlc.types.Field(Boolean, graphql_name='isSiteNameNotExist')


class InformationSourceFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'status')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    status = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CollectionStatus)), graphql_name='status')


class InformationSourceLoaderFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'type_of_crawl', 'status', 'created_by', 'changed_by', 'created_at', 'changed_at')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    type_of_crawl = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(TypeOfCrawl)), graphql_name='typeOfCrawl')
    status = sgqlc.types.Field(CollectionStatus, graphql_name='status')
    created_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='createdBy')
    changed_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='changedBy')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    changed_at = sgqlc.types.Field('TimestampInterval', graphql_name='changedAt')


class InformationSourceLoaderInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('file_settings', 'urls', 'is_retrospective', 'retrospective_interval', 'actual_status')
    file_settings = sgqlc.types.Field(FileSettings, graphql_name='fileSettings')
    urls = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('KeyOptionValueInput')), graphql_name='urls')
    is_retrospective = sgqlc.types.Field(Boolean, graphql_name='isRetrospective')
    retrospective_interval = sgqlc.types.Field('TimestampInterval', graphql_name='retrospectiveInterval')
    actual_status = sgqlc.types.Field(InformationSourceLoaderActualStatus, graphql_name='actualStatus')


class JobInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler_id', 'version_id', 'priority', 'is_noise', 'settings', 'args')
    crawler_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='crawlerId')
    version_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='versionId')
    priority = sgqlc.types.Field(sgqlc.types.non_null(JobPriorityType), graphql_name='priority')
    is_noise = sgqlc.types.Field(Boolean, graphql_name='isNoise')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('KeyValueInputType'))), graphql_name='args')


class JobSorting(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_pending_sorting', 'job_running_sorting', 'job_finished_sorting')
    job_pending_sorting = sgqlc.types.Field('JobsPendingSort', graphql_name='jobPendingSorting')
    job_running_sorting = sgqlc.types.Field('JobsRunningSort', graphql_name='jobRunningSorting')
    job_finished_sorting = sgqlc.types.Field('JobsFinishedSort', graphql_name='jobFinishedSorting')


class JobsFilter(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'projects', 'crawlers', 'created_by', 'changed_by', 'created_at', 'changed_at', 'periodic_jobs', 'collection_statuses', 'job_ids', 'start_time', 'end_time')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    crawlers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='crawlers')
    created_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='createdBy')
    changed_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='changedBy')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    changed_at = sgqlc.types.Field('TimestampInterval', graphql_name='changedAt')
    periodic_jobs = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='periodicJobs')
    collection_statuses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(CollectionStatus)), graphql_name='collectionStatuses')
    job_ids = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Long)), graphql_name='jobIds')
    start_time = sgqlc.types.Field('TimestampInterval', graphql_name='startTime')
    end_time = sgqlc.types.Field('TimestampInterval', graphql_name='endTime')


class JobsFinishedSort(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('sort', 'direction')
    sort = sgqlc.types.Field(JobFinishedSort, graphql_name='sort')
    direction = sgqlc.types.Field(SortDirection, graphql_name='direction')


class JobsPendingSort(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('sort', 'direction')
    sort = sgqlc.types.Field(JobPendingSort, graphql_name='sort')
    direction = sgqlc.types.Field(SortDirection, graphql_name='direction')


class JobsRunningSort(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('sort', 'direction')
    sort = sgqlc.types.Field(JobRunningSort, graphql_name='sort')
    direction = sgqlc.types.Field(SortDirection, graphql_name='direction')


class KeyOptionValueInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(String, graphql_name='value')


class KeyValueInputType(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class LogFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_text', 'levels', 'interval')
    input_text = sgqlc.types.Field(String, graphql_name='inputText')
    levels = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(LogLevel)), graphql_name='levels')
    interval = sgqlc.types.Field('TimestampInterval', graphql_name='interval')


class MetricFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_text', 'interval')
    input_text = sgqlc.types.Field(String, graphql_name='inputText')
    interval = sgqlc.types.Field('TimestampInterval', graphql_name='interval')


class PeriodicJobFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'projects', 'crawlers', 'priorities', 'running_statuses', 'created_by', 'changed_by', 'created_at', 'changed_at', 'next_schedule_time')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    projects = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='projects')
    crawlers = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(ID)), graphql_name='crawlers')
    priorities = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(JobPriorityType)), graphql_name='priorities')
    running_statuses = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(PeriodicJobStatus)), graphql_name='runningStatuses')
    created_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='createdBy')
    changed_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='changedBy')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    changed_at = sgqlc.types.Field('TimestampInterval', graphql_name='changedAt')
    next_schedule_time = sgqlc.types.Field('TimestampInterval', graphql_name='nextScheduleTime')


class PeriodicJobInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('title', 'description', 'crawler_id', 'version_id', 'status', 'priority', 'cron_expression', 'cron_utcoffset_minutes', 'settings', 'args', 'update_on_reload')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    crawler_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='crawlerId')
    version_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='versionId')
    status = sgqlc.types.Field(PeriodicJobStatus, graphql_name='status')
    priority = sgqlc.types.Field(JobPriorityType, graphql_name='priority')
    cron_expression = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cronExpression')
    cron_utcoffset_minutes = sgqlc.types.Field(Int, graphql_name='cronUTCOffsetMinutes')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args')
    update_on_reload = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateOnReload')


class ProjectFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'name', 'created_by', 'changed_by', 'created_at', 'changed_at')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    name = sgqlc.types.Field(String, graphql_name='name')
    created_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='createdBy')
    changed_by = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='changedBy')
    created_at = sgqlc.types.Field('TimestampInterval', graphql_name='createdAt')
    changed_at = sgqlc.types.Field('TimestampInterval', graphql_name='changedAt')


class ProjectInput(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('title', 'name', 'description', 'eggfile', 'pipfile', 'lockfile', 'settings', 'args')
    title = sgqlc.types.Field(String, graphql_name='title')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    eggfile = sgqlc.types.Field(String, graphql_name='eggfile')
    pipfile = sgqlc.types.Field(String, graphql_name='pipfile')
    lockfile = sgqlc.types.Field(String, graphql_name='lockfile')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args')


class RequestFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_text', 'interval')
    input_text = sgqlc.types.Field(String, graphql_name='inputText')
    interval = sgqlc.types.Field('TimestampInterval', graphql_name='interval')


class TimestampInterval(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('start', 'end')
    start = sgqlc.types.Field(UnixTime, graphql_name='start')
    end = sgqlc.types.Field(UnixTime, graphql_name='end')


class VersionFilterSettings(sgqlc.types.Input):
    __schema__ = crawlers_api_schema
    __field_names__ = ('input_value', 'with_removed_versions')
    input_value = sgqlc.types.Field(String, graphql_name='inputValue')
    with_removed_versions = sgqlc.types.Field(Boolean, graphql_name='withRemovedVersions')



########################################################################
# Output Objects and Interfaces
########################################################################
class ArgsAndSettingsDescription(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('args', 'settings')
    args = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('SettingDescription')), graphql_name='args')
    settings = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('SettingDescription')), graphql_name='settings')


class CrawlerData(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'title', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class CrawlerHistogram(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('crawler_name', 'items_scraped_count', 'jobs_count', 'jobs_with_errors_logs')
    crawler_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='crawlerName')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    jobs_with_errors_logs = sgqlc.types.Field(Int, graphql_name='jobsWithErrorsLogs')


class CrawlerPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_crawler')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_crawler = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Crawler'))), graphql_name='listCrawler')


class CrawlerStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('items_scraped_count', 'next_schedule_time', 'total_time', 'items_scraped_count_last', 'avg_performance_time', 'last_collection_date')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    next_schedule_time = sgqlc.types.Field(Long, graphql_name='nextScheduleTime')
    total_time = sgqlc.types.Field(Long, graphql_name='totalTime')
    items_scraped_count_last = sgqlc.types.Field(Long, graphql_name='itemsScrapedCountLast')
    avg_performance_time = sgqlc.types.Field(Long, graphql_name='avgPerformanceTime')
    last_collection_date = sgqlc.types.Field(Long, graphql_name='lastCollectionDate')


class CredentialPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_credential')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')
    list_credential = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Credential'))), graphql_name='listCredential')


class DateHistogramBucket(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('date', 'timestamp', 'doc_count')
    date = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='date')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='timestamp')
    doc_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='docCount')


class DeployedProject(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('project_id', 'crawlers', 'status', 'update_stats')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    crawlers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Crawler'))), graphql_name='crawlers')
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')
    update_stats = sgqlc.types.Field(sgqlc.types.non_null('UpdateProjectStats'), graphql_name='updateStats')


class FileData(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'file_name')
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='id')
    file_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileName')


class InformationSource(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'url', 'site_name', 'status', 'periodic_job', 'job', 'crawler', 'error_message')
    id = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='id')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    site_name = sgqlc.types.Field(String, graphql_name='siteName')
    status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='status')
    periodic_job = sgqlc.types.Field('PeriodicJob', graphql_name='periodicJob')
    job = sgqlc.types.Field('Job', graphql_name='job')
    crawler = sgqlc.types.Field('Crawler', graphql_name='crawler')
    error_message = sgqlc.types.Field(String, graphql_name='errorMessage')


class InformationSourceData(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'url', 'site_name', 'status', 'crawler', 'version_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    site_name = sgqlc.types.Field(String, graphql_name='siteName')
    status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='status')
    crawler = sgqlc.types.Field(CrawlerData, graphql_name='crawler')
    version_id = sgqlc.types.Field(ID, graphql_name='versionId')


class InformationSourceLoaderStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total_source_count', 'finished_source_count')
    total_source_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='totalSourceCount')
    finished_source_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='finishedSourceCount')


class JobList(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_job')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Job'))), graphql_name='listJob')


class JobMetrics(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id',)
    job_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='jobId')


class JobPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_job')
    total = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='total')
    list_job = sgqlc.types.Field(sgqlc.types.non_null('Jobs'), graphql_name='listJob')


class JobStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('jobs_count', 'total_time', 'items_scraped_count', 'requests_count', 'errors_count', 'duplicated_request_count', 'jobs_with_errors_logs_count', 'jobs_with_critical_logs_count')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    total_time = sgqlc.types.Field(Long, graphql_name='totalTime')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    requests_count = sgqlc.types.Field(Long, graphql_name='requestsCount')
    errors_count = sgqlc.types.Field(Int, graphql_name='errorsCount')
    duplicated_request_count = sgqlc.types.Field(Int, graphql_name='duplicatedRequestCount')
    jobs_with_errors_logs_count = sgqlc.types.Field(Int, graphql_name='jobsWithErrorsLogsCount')
    jobs_with_critical_logs_count = sgqlc.types.Field(Int, graphql_name='jobsWithCriticalLogsCount')


class Jobs(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('pending', 'running', 'finished')
    pending = sgqlc.types.Field(sgqlc.types.non_null(JobList), graphql_name='pending')
    running = sgqlc.types.Field(sgqlc.types.non_null(JobList), graphql_name='running')
    finished = sgqlc.types.Field(sgqlc.types.non_null(JobList), graphql_name='finished')


class KeyValue(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('key', 'value')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    value = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='value')


class Log(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id', 'timestamp', 'level', 'message', 'logger_name', 'stack_trace')
    job_id = sgqlc.types.Field(String, graphql_name='jobId')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='timestamp')
    level = sgqlc.types.Field(sgqlc.types.non_null(LogLevel), graphql_name='level')
    message = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='message')
    logger_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='loggerName')
    stack_trace = sgqlc.types.Field(String, graphql_name='stackTrace')


class Metric(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id', 'timestamp', 'metric')
    job_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='jobId')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='timestamp')
    metric = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='metric')


class Mutation(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('update_crawler', 'update_crawler_settings_arguments_and_state', 'delete_crawler_versions', 'delete_crawlers', 'update_site_map_crawler_body', 'add_credential', 'update_credential', 'delete_credential', 'single_upload', 'add_job', 'delete_job', 'cancel_job', 'add_periodic_job', 'run_periodic_jobs', 'update_enable_jobs_scheduling', 'update_disable_jobs_scheduling', 'delete_periodic_job', 'update_periodic_job', 'update_periodic_job_settings_and_arguments', 'delete_project', 'delete_project_versions', 'add_project', 'update_project', 'update_set_active_project', 'update_remove_active_project', 'update_project_settings_and_arguments', 'add_information_source_loader', 'delete_information_source_loader')
    update_crawler = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='updateCrawler', args=sgqlc.types.ArgDict((
        ('crawler_update_input', sgqlc.types.Arg(sgqlc.types.non_null(CrawlerUpdateInput), graphql_name='crawlerUpdateInput', default=None)),
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('project_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='projectId', default=None)),
))
    )
    update_crawler_settings_arguments_and_state = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='updateCrawlerSettingsArgumentsAndState', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('settings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings', default=None)),
        ('args', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args', default=None)),
        ('state', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='state', default=None)),
        ('state_version', sgqlc.types.Arg(sgqlc.types.non_null(Long), graphql_name='stateVersion', default=None)),
))
    )
    delete_crawler_versions = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCrawlerVersions', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('version_ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='versionIds', default=None)),
))
    )
    delete_crawlers = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCrawlers', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_site_map_crawler_body = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='updateSiteMapCrawlerBody', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('project_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='projectId', default=None)),
        ('json', sgqlc.types.Arg(sgqlc.types.non_null(JSON), graphql_name='json', default=None)),
))
    )
    add_credential = sgqlc.types.Field(sgqlc.types.non_null('Credential'), graphql_name='addCredential', args=sgqlc.types.ArgDict((
        ('credential_input', sgqlc.types.Arg(sgqlc.types.non_null(CredentialInput), graphql_name='credentialInput', default=None)),
))
    )
    update_credential = sgqlc.types.Field(sgqlc.types.non_null('Credential'), graphql_name='updateCredential', args=sgqlc.types.ArgDict((
        ('credential_input', sgqlc.types.Arg(sgqlc.types.non_null(CredentialInput), graphql_name='credentialInput', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='version', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    delete_credential = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteCredential', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    single_upload = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='singleUpload', args=sgqlc.types.ArgDict((
        ('file', sgqlc.types.Arg(Upload, graphql_name='file', default=None)),
))
    )
    add_job = sgqlc.types.Field(sgqlc.types.non_null('Job'), graphql_name='addJob', args=sgqlc.types.ArgDict((
        ('job_input', sgqlc.types.Arg(sgqlc.types.non_null(JobInput), graphql_name='jobInput', default=None)),
))
    )
    delete_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    cancel_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='cancelJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    add_periodic_job = sgqlc.types.Field(sgqlc.types.non_null('PeriodicJob'), graphql_name='addPeriodicJob', args=sgqlc.types.ArgDict((
        ('periodic_job_input', sgqlc.types.Arg(sgqlc.types.non_null(PeriodicJobInput), graphql_name='periodicJobInput', default=None)),
))
    )
    run_periodic_jobs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Job'))), graphql_name='runPeriodicJobs', args=sgqlc.types.ArgDict((
        ('periodic_job_ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='periodicJobIds', default=None)),
))
    )
    update_enable_jobs_scheduling = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PeriodicJob'))), graphql_name='updateEnableJobsScheduling', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_disable_jobs_scheduling = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PeriodicJob'))), graphql_name='updateDisableJobsScheduling', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_periodic_job = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deletePeriodicJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    update_periodic_job = sgqlc.types.Field(sgqlc.types.non_null('PeriodicJob'), graphql_name='updatePeriodicJob', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('periodic_job_input', sgqlc.types.Arg(sgqlc.types.non_null(PeriodicJobInput), graphql_name='periodicJobInput', default=None)),
))
    )
    update_periodic_job_settings_and_arguments = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='updatePeriodicJobSettingsAndArguments', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('settings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings', default=None)),
        ('args', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args', default=None)),
))
    )
    delete_project = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteProject', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    delete_project_versions = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteProjectVersions', args=sgqlc.types.ArgDict((
        ('project_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='projectId', default=None)),
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    add_project = sgqlc.types.Field(sgqlc.types.non_null(DeployedProject), graphql_name='addProject', args=sgqlc.types.ArgDict((
        ('project_input', sgqlc.types.Arg(sgqlc.types.non_null(ProjectInput), graphql_name='projectInput', default=None)),
))
    )
    update_project = sgqlc.types.Field(sgqlc.types.non_null(DeployedProject), graphql_name='updateProject', args=sgqlc.types.ArgDict((
        ('project_input', sgqlc.types.Arg(sgqlc.types.non_null(ProjectInput), graphql_name='projectInput', default=None)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    update_set_active_project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='updateSetActiveProject', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    update_remove_active_project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='updateRemoveActiveProject', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    update_project_settings_and_arguments = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='updateProjectSettingsAndArguments', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('settings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='settings', default=None)),
        ('args', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValueInputType))), graphql_name='args', default=None)),
))
    )
    add_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('InformationSourceLoader'), graphql_name='addInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('information_source_loader_input', sgqlc.types.Arg(sgqlc.types.non_null(InformationSourceLoaderInput), graphql_name='informationSourceLoaderInput', default=None)),
))
    )
    delete_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('State'), graphql_name='deleteInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )


class PaginationInformationSource(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_information_source')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_information_source = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InformationSource))), graphql_name='listInformationSource')


class PaginationInformationSourceLoader(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('list_information_source_loader', 'total')
    list_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('InformationSourceLoader'))), graphql_name='listInformationSourceLoader')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')


class PaginationLog(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'log_list')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    log_list = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Log))), graphql_name='logList')


class PaginationMetric(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'metric_list')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    metric_list = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Metric))), graphql_name='metricList')


class PaginationRequest(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'request_list')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    request_list = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Request'))), graphql_name='requestList')


class PeriodicJobData(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')


class PeriodicJobMetrics(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('periodic_job_id',)
    periodic_job_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='periodicJobId')


class PeriodicJobPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_periodic_job')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_periodic_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('PeriodicJob'))), graphql_name='listPeriodicJob')


class ProjectData(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'title')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')


class ProjectHistogram(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('project_name', 'items_scraped_count', 'jobs_count', 'jobs_with_errors_logs')
    project_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='projectName')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    jobs_with_errors_logs = sgqlc.types.Field(Int, graphql_name='jobsWithErrorsLogs')


class ProjectPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_project')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_project = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Project'))), graphql_name='listProject')


class ProjectStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('items_scraped_count', 'errors_count', 'jobs_count', 'jobs_with_errors_logs_count', 'job_ids_with_error_logs', 'jobs_with_critical_logs_count')
    items_scraped_count = sgqlc.types.Field(Long, graphql_name='itemsScrapedCount')
    errors_count = sgqlc.types.Field(Int, graphql_name='errorsCount')
    jobs_count = sgqlc.types.Field(Int, graphql_name='jobsCount')
    jobs_with_errors_logs_count = sgqlc.types.Field(Int, graphql_name='jobsWithErrorsLogsCount')
    job_ids_with_error_logs = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Long))), graphql_name='jobIdsWithErrorLogs')
    jobs_with_critical_logs_count = sgqlc.types.Field(Int, graphql_name='jobsWithCriticalLogsCount')


class Query(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('analytics', 'crawler', 'list_crawler', 'pagination_crawler', 'crawler_args_and_settings_description', 'credential', 'pagination_credential', 'job', 'list_job', 'pagination_job_logs', 'pagination_job_requests', 'pagination_job_metrics', 'pagination_job', 'periodic_job', 'pagination_periodic_job', 'pagination_periodic_job_logs', 'pagination_periodic_job_requests', 'pagination_periodic_job_metrics', 'check_periodic_job_by_input', 'project', 'pagination_project', 'project_args_and_settings_description', 'project_default_args_and_settings_description', 'information_source_loader', 'pagination_information_source_loader', 'information_source', 'pagination_information_source', 'version', 'list_version', 'pagination_versions_crawler', 'pagination_egg_file_versions_project', 'web_scraper_version_is_compatible')
    analytics = sgqlc.types.Field(sgqlc.types.non_null('Stats'), graphql_name='analytics')
    crawler = sgqlc.types.Field(sgqlc.types.non_null('Crawler'), graphql_name='crawler', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_crawler = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Crawler')), graphql_name='listCrawler', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    pagination_crawler = sgqlc.types.Field(sgqlc.types.non_null(CrawlerPagination), graphql_name='paginationCrawler', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(CrawlerFilterSettings, graphql_name='filterSettings', default={})),
        ('sort_field', sgqlc.types.Arg(CrawlerSorting, graphql_name='sortField', default='id')),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    crawler_args_and_settings_description = sgqlc.types.Field(sgqlc.types.non_null(ArgsAndSettingsDescription), graphql_name='crawlerArgsAndSettingsDescription', args=sgqlc.types.ArgDict((
        ('crawler_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='crawlerId', default=None)),
        ('version_id', sgqlc.types.Arg(ID, graphql_name='versionId', default=None)),
))
    )
    credential = sgqlc.types.Field(sgqlc.types.non_null('Credential'), graphql_name='credential', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    pagination_credential = sgqlc.types.Field(sgqlc.types.non_null(CredentialPagination), graphql_name='paginationCredential', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(CredentialSorting, graphql_name='sortField', default='id')),
        ('filter_settings', sgqlc.types.Arg(sgqlc.types.non_null(CredentialFilterSettings), graphql_name='filterSettings', default=None)),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    job = sgqlc.types.Field(sgqlc.types.non_null('Job'), graphql_name='job', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_job = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Job')), graphql_name='listJob', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    pagination_job_logs = sgqlc.types.Field(sgqlc.types.non_null(PaginationLog), graphql_name='paginationJobLogs', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('filter_settings', sgqlc.types.Arg(LogFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(LogSorting, graphql_name='sortField', default=None)),
))
    )
    pagination_job_requests = sgqlc.types.Field(sgqlc.types.non_null(PaginationRequest), graphql_name='paginationJobRequests', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('filter_settings', sgqlc.types.Arg(RequestFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(RequestSorting, graphql_name='sortField', default=None)),
))
    )
    pagination_job_metrics = sgqlc.types.Field(sgqlc.types.non_null(PaginationMetric), graphql_name='paginationJobMetrics', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('filter_settings', sgqlc.types.Arg(MetricFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(MetricSorting, graphql_name='sortField', default=None)),
))
    )
    pagination_job = sgqlc.types.Field(sgqlc.types.non_null(JobPagination), graphql_name='paginationJob', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort', sgqlc.types.Arg(JobSorting, graphql_name='sort', default={'jobPendingSorting': {'sort': 'id', 'direction': 'descending'}, 'jobRunningSorting': {'sort': 'id', 'direction': 'descending'}, 'jobFinishedSorting': {'sort': 'id', 'direction': 'descending'}})),
        ('jobs_filter', sgqlc.types.Arg(JobsFilter, graphql_name='jobsFilter', default={})),
))
    )
    periodic_job = sgqlc.types.Field(sgqlc.types.non_null('PeriodicJob'), graphql_name='periodicJob', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    pagination_periodic_job = sgqlc.types.Field(sgqlc.types.non_null(PeriodicJobPagination), graphql_name='paginationPeriodicJob', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(PeriodicJobFilterSettings, graphql_name='filterSettings', default={})),
        ('sort_field', sgqlc.types.Arg(PeriodicJobSorting, graphql_name='sortField', default='id')),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    pagination_periodic_job_logs = sgqlc.types.Field(sgqlc.types.non_null(PaginationLog), graphql_name='paginationPeriodicJobLogs', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('filter_settings', sgqlc.types.Arg(LogFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(LogSorting, graphql_name='sortField', default=None)),
))
    )
    pagination_periodic_job_requests = sgqlc.types.Field(sgqlc.types.non_null(PaginationRequest), graphql_name='paginationPeriodicJobRequests', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('filter_settings', sgqlc.types.Arg(RequestFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(RequestSorting, graphql_name='sortField', default=None)),
))
    )
    pagination_periodic_job_metrics = sgqlc.types.Field(sgqlc.types.non_null(PaginationMetric), graphql_name='paginationPeriodicJobMetrics', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('filter_settings', sgqlc.types.Arg(MetricFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
        ('sort_field', sgqlc.types.Arg(MetricSorting, graphql_name='sortField', default=None)),
))
    )
    check_periodic_job_by_input = sgqlc.types.Field('PeriodicJob', graphql_name='checkPeriodicJobByInput', args=sgqlc.types.ArgDict((
        ('periodic_job_input', sgqlc.types.Arg(sgqlc.types.non_null(PeriodicJobInput), graphql_name='periodicJobInput', default=None)),
))
    )
    project = sgqlc.types.Field(sgqlc.types.non_null('Project'), graphql_name='project', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    pagination_project = sgqlc.types.Field(sgqlc.types.non_null(ProjectPagination), graphql_name='paginationProject', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('sort_field', sgqlc.types.Arg(ProjectSorting, graphql_name='sortField', default='id')),
        ('filter_settings', sgqlc.types.Arg(ProjectFilterSettings, graphql_name='filterSettings', default={})),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    project_args_and_settings_description = sgqlc.types.Field(sgqlc.types.non_null(ArgsAndSettingsDescription), graphql_name='projectArgsAndSettingsDescription', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('version_id', sgqlc.types.Arg(ID, graphql_name='versionId', default=None)),
))
    )
    project_default_args_and_settings_description = sgqlc.types.Field(sgqlc.types.non_null(ArgsAndSettingsDescription), graphql_name='projectDefaultArgsAndSettingsDescription')
    information_source_loader = sgqlc.types.Field(sgqlc.types.non_null('InformationSourceLoader'), graphql_name='informationSourceLoader', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    pagination_information_source_loader = sgqlc.types.Field(sgqlc.types.non_null(PaginationInformationSourceLoader), graphql_name='paginationInformationSourceLoader', args=sgqlc.types.ArgDict((
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(InformationSourceLoaderFilterSettings, graphql_name='filterSettings', default={})),
        ('sort_field', sgqlc.types.Arg(InformationSourceLoaderSorting, graphql_name='sortField', default='id')),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    information_source = sgqlc.types.Field(sgqlc.types.non_null(InformationSource), graphql_name='informationSource', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    pagination_information_source = sgqlc.types.Field(sgqlc.types.non_null(PaginationInformationSource), graphql_name='paginationInformationSource', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(InformationSourceFilterSettings, graphql_name='filterSettings', default={})),
        ('sort_field', sgqlc.types.Arg(InformationSourceSorting, graphql_name='sortField', default='id')),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    version = sgqlc.types.Field(sgqlc.types.non_null('Version'), graphql_name='version', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Version')), graphql_name='listVersion', args=sgqlc.types.ArgDict((
        ('ids', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ID))), graphql_name='ids', default=None)),
))
    )
    pagination_versions_crawler = sgqlc.types.Field(sgqlc.types.non_null('VersionPagination'), graphql_name='paginationVersionsCrawler', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('filter_settings', sgqlc.types.Arg(VersionFilterSettings, graphql_name='filterSettings', default={'withRemovedVersions': False})),
        ('sort_field', sgqlc.types.Arg(VersionSorting, graphql_name='sortField', default='id')),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    pagination_egg_file_versions_project = sgqlc.types.Field(sgqlc.types.non_null('VersionPagination'), graphql_name='paginationEggFileVersionsProject', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=20)),
        ('offset', sgqlc.types.Arg(Int, graphql_name='offset', default=0)),
        ('with_removed', sgqlc.types.Arg(sgqlc.types.non_null(Boolean), graphql_name='withRemoved', default=False)),
        ('sort_field', sgqlc.types.Arg(VersionSorting, graphql_name='sortField', default='id')),
        ('direction', sgqlc.types.Arg(SortDirection, graphql_name='direction', default='descending')),
))
    )
    web_scraper_version_is_compatible = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='webScraperVersionIsCompatible', args=sgqlc.types.ArgDict((
        ('web_scraper_version', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='webScraperVersion', default=None)),
))
    )


class RecordInterface(sgqlc.types.Interface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('system_registration_date', 'system_update_date', 'creator', 'last_updater')
    system_registration_date = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='systemRegistrationDate')
    system_update_date = sgqlc.types.Field(UnixTime, graphql_name='systemUpdateDate')
    creator = sgqlc.types.Field(sgqlc.types.non_null('User'), graphql_name='creator')
    last_updater = sgqlc.types.Field('User', graphql_name='lastUpdater')


class Request(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('job_id', 'timestamp', 'last_seen', 'url', 'request_url', 'fingerprint', 'method', 'http_status', 'response_size', 'duration')
    job_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='jobId')
    timestamp = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='timestamp')
    last_seen = sgqlc.types.Field(sgqlc.types.non_null(UnixTime), graphql_name='lastSeen')
    url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='url')
    request_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='requestUrl')
    fingerprint = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fingerprint')
    method = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='method')
    http_status = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='httpStatus')
    response_size = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='responseSize')
    duration = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='duration')


class SettingDescription(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('name', 'type', 'short_description', 'long_description', 'required', 'default')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    type = sgqlc.types.Field(sgqlc.types.non_null(SettingsType), graphql_name='type')
    short_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='shortDescription')
    long_description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='longDescription')
    required = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='required')
    default = sgqlc.types.Field(String, graphql_name='default')


class State(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('is_success',)
    is_success = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isSuccess')


class Stats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('type_of_stats', 'user_id', 'jobs_metrics', 'items_histogram', 'projects_histogram', 'previous_items_histogram')
    type_of_stats = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='typeOfStats')
    user_id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userId')
    jobs_metrics = sgqlc.types.Field(sgqlc.types.non_null(JobStats), graphql_name='jobsMetrics', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    items_histogram = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='itemsHistogram', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    projects_histogram = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ProjectHistogram))), graphql_name='projectsHistogram', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    previous_items_histogram = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='previousItemsHistogram', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )


class UpdateProjectStats(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('added_crawlers_count', 'deleted_crawlers_count', 'updated_crawlers_count', 'is_metadata_updated', 'updated_periodic_ids', 'stopped_periodic_ids')
    added_crawlers_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='addedCrawlersCount')
    deleted_crawlers_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='deletedCrawlersCount')
    updated_crawlers_count = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='updatedCrawlersCount')
    is_metadata_updated = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isMetadataUpdated')
    updated_periodic_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Long))), graphql_name='updatedPeriodicIds')
    stopped_periodic_ids = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(Long))), graphql_name='stoppedPeriodicIds')


class User(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')


class VersionData(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'version_name', 'status')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    version_name = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='versionName')
    status = sgqlc.types.Field(sgqlc.types.non_null(VersionStatus), graphql_name='status')


class VersionPagination(sgqlc.types.Type):
    __schema__ = crawlers_api_schema
    __field_names__ = ('total', 'list_version')
    total = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='total')
    list_version = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Version'))), graphql_name='listVersion')


class Crawler(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'name', 'title', 'description', 'project', 'periodic_jobs_num', 'onetime_jobs_num', 'last_collection_date', 'state_version', 'avg_performance_time', 'pinned', 'settings', 'args', 'state', 'analytics', 'histogram_items', 'histogram_requests', 'job_stats', 'current_version', 'start_urls', 'sitemap')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    project = sgqlc.types.Field(sgqlc.types.non_null(ProjectData), graphql_name='project')
    periodic_jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='periodicJobsNum')
    onetime_jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='onetimeJobsNum')
    last_collection_date = sgqlc.types.Field(Long, graphql_name='lastCollectionDate')
    state_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='stateVersion')
    avg_performance_time = sgqlc.types.Field(Float, graphql_name='avgPerformanceTime')
    pinned = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='pinned')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    state = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='state')
    analytics = sgqlc.types.Field(sgqlc.types.non_null(CrawlerStats), graphql_name='analytics', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_requests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramRequests', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    job_stats = sgqlc.types.Field(sgqlc.types.non_null(JobStats), graphql_name='jobStats', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    current_version = sgqlc.types.Field('Version', graphql_name='currentVersion')
    start_urls = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='startUrls')
    sitemap = sgqlc.types.Field(JSON, graphql_name='sitemap')


class Credential(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'data_type', 'description', 'login', 'password', 'token', 'domain', 'projects', 'status', 'state', 'cookies', 'version')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    data_type = sgqlc.types.Field(sgqlc.types.non_null(CredentialType), graphql_name='dataType')
    description = sgqlc.types.Field(String, graphql_name='description')
    login = sgqlc.types.Field(String, graphql_name='login')
    password = sgqlc.types.Field(String, graphql_name='password')
    token = sgqlc.types.Field(String, graphql_name='token')
    domain = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='domain')
    projects = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(ProjectData))), graphql_name='projects')
    status = sgqlc.types.Field(sgqlc.types.non_null(CredentialStatus), graphql_name='status')
    state = sgqlc.types.Field(JSON, graphql_name='state')
    cookies = sgqlc.types.Field(JSON, graphql_name='cookies')
    version = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='version')


class InformationSourceLoader(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'file', 'sources', 'title', 'is_retrospective', 'retrospective_start', 'retrospective_end', 'actual_status', 'status', 'metrics')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    file = sgqlc.types.Field(FileData, graphql_name='file')
    sources = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InformationSourceData))), graphql_name='sources')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    is_retrospective = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isRetrospective')
    retrospective_start = sgqlc.types.Field(UnixTime, graphql_name='retrospectiveStart')
    retrospective_end = sgqlc.types.Field(UnixTime, graphql_name='retrospectiveEnd')
    actual_status = sgqlc.types.Field(sgqlc.types.non_null(InformationSourceLoaderActualStatus), graphql_name='actualStatus')
    status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='status')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(InformationSourceLoaderStats), graphql_name='metrics')


class Job(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'status', 'priority', 'start_time', 'end_time', 'collection_status', 'is_noise', 'crawler', 'project', 'version', 'periodic', 'settings', 'args', 'metrics', 'job_stats', 'histogram_requests', 'histogram_items', 'schema')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    status = sgqlc.types.Field(sgqlc.types.non_null(JobStatus), graphql_name='status')
    priority = sgqlc.types.Field(sgqlc.types.non_null(JobPriorityType), graphql_name='priority')
    start_time = sgqlc.types.Field(Long, graphql_name='startTime')
    end_time = sgqlc.types.Field(Long, graphql_name='endTime')
    collection_status = sgqlc.types.Field(sgqlc.types.non_null(CollectionStatus), graphql_name='collectionStatus')
    is_noise = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isNoise')
    crawler = sgqlc.types.Field(sgqlc.types.non_null(CrawlerData), graphql_name='crawler')
    project = sgqlc.types.Field(sgqlc.types.non_null(ProjectData), graphql_name='project')
    version = sgqlc.types.Field(sgqlc.types.non_null(VersionData), graphql_name='version')
    periodic = sgqlc.types.Field(PeriodicJobData, graphql_name='periodic')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(JobMetrics), graphql_name='metrics')
    job_stats = sgqlc.types.Field(JobStats, graphql_name='jobStats')
    histogram_requests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramRequests')
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems')
    schema = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='schema')


class PeriodicJob(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'name', 'description', 'project', 'crawler', 'version', 'priority', 'status', 'cron', 'cron_utcoffset_minutes', 'next_schedule_time', 'update_on_reload', 'settings', 'args', 'metrics', 'histogram_requests', 'histogram_items', 'job_stats')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    description = sgqlc.types.Field(String, graphql_name='description')
    project = sgqlc.types.Field(sgqlc.types.non_null(ProjectData), graphql_name='project')
    crawler = sgqlc.types.Field(sgqlc.types.non_null(CrawlerData), graphql_name='crawler')
    version = sgqlc.types.Field(sgqlc.types.non_null(VersionData), graphql_name='version')
    priority = sgqlc.types.Field(sgqlc.types.non_null(JobPriorityType), graphql_name='priority')
    status = sgqlc.types.Field(sgqlc.types.non_null(PeriodicJobStatus), graphql_name='status')
    cron = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='cron')
    cron_utcoffset_minutes = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='cronUTCOffsetMinutes')
    next_schedule_time = sgqlc.types.Field(Long, graphql_name='nextScheduleTime')
    update_on_reload = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='updateOnReload')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    metrics = sgqlc.types.Field(sgqlc.types.non_null(PeriodicJobMetrics), graphql_name='metrics')
    histogram_requests = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramRequests', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    job_stats = sgqlc.types.Field(sgqlc.types.non_null(JobStats), graphql_name='jobStats', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )


class Project(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'name', 'title', 'description', 'crawlers_num', 'periodic_jobs_num', 'jobs_num', 'active', 'settings', 'args', 'project_stats', 'histogram_items', 'histogram_crawlers', 'current_version', 'egg_file')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    crawlers_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='crawlersNum')
    periodic_jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='periodicJobsNum')
    jobs_num = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='jobsNum')
    active = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='active')
    settings = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='settings')
    args = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(KeyValue))), graphql_name='args')
    project_stats = sgqlc.types.Field(sgqlc.types.non_null(ProjectStats), graphql_name='projectStats', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_items = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(DateHistogramBucket))), graphql_name='histogramItems', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    histogram_crawlers = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CrawlerHistogram))), graphql_name='histogramCrawlers', args=sgqlc.types.ArgDict((
        ('interval', sgqlc.types.Arg(TimestampInterval, graphql_name='interval', default=None)),
))
    )
    current_version = sgqlc.types.Field('Version', graphql_name='currentVersion')
    egg_file = sgqlc.types.Field(String, graphql_name='eggFile')


class Version(sgqlc.types.Type, RecordInterface):
    __schema__ = crawlers_api_schema
    __field_names__ = ('id', 'version_name', 'project_id', 'status')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    version_name = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='versionName')
    project_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='projectId')
    status = sgqlc.types.Field(sgqlc.types.non_null(VersionStatus), graphql_name='status')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
crawlers_api_schema.query_type = Query
crawlers_api_schema.mutation_type = Mutation
crawlers_api_schema.subscription_type = None

