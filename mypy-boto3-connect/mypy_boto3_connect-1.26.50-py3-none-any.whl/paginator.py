"""
Type annotations for connect service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_connect.client import ConnectClient
    from mypy_boto3_connect.paginator import (
        GetMetricDataPaginator,
        ListAgentStatusesPaginator,
        ListApprovedOriginsPaginator,
        ListBotsPaginator,
        ListContactFlowModulesPaginator,
        ListContactFlowsPaginator,
        ListContactReferencesPaginator,
        ListDefaultVocabulariesPaginator,
        ListHoursOfOperationsPaginator,
        ListInstanceAttributesPaginator,
        ListInstanceStorageConfigsPaginator,
        ListInstancesPaginator,
        ListIntegrationAssociationsPaginator,
        ListLambdaFunctionsPaginator,
        ListLexBotsPaginator,
        ListPhoneNumbersPaginator,
        ListPhoneNumbersV2Paginator,
        ListPromptsPaginator,
        ListQueueQuickConnectsPaginator,
        ListQueuesPaginator,
        ListQuickConnectsPaginator,
        ListRoutingProfileQueuesPaginator,
        ListRoutingProfilesPaginator,
        ListRulesPaginator,
        ListSecurityKeysPaginator,
        ListSecurityProfilePermissionsPaginator,
        ListSecurityProfilesPaginator,
        ListTaskTemplatesPaginator,
        ListTrafficDistributionGroupsPaginator,
        ListUseCasesPaginator,
        ListUserHierarchyGroupsPaginator,
        ListUsersPaginator,
        SearchAvailablePhoneNumbersPaginator,
        SearchQueuesPaginator,
        SearchRoutingProfilesPaginator,
        SearchSecurityProfilesPaginator,
        SearchUsersPaginator,
        SearchVocabulariesPaginator,
    )

    session = Session()
    client: ConnectClient = session.client("connect")

    get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
    list_agent_statuses_paginator: ListAgentStatusesPaginator = client.get_paginator("list_agent_statuses")
    list_approved_origins_paginator: ListApprovedOriginsPaginator = client.get_paginator("list_approved_origins")
    list_bots_paginator: ListBotsPaginator = client.get_paginator("list_bots")
    list_contact_flow_modules_paginator: ListContactFlowModulesPaginator = client.get_paginator("list_contact_flow_modules")
    list_contact_flows_paginator: ListContactFlowsPaginator = client.get_paginator("list_contact_flows")
    list_contact_references_paginator: ListContactReferencesPaginator = client.get_paginator("list_contact_references")
    list_default_vocabularies_paginator: ListDefaultVocabulariesPaginator = client.get_paginator("list_default_vocabularies")
    list_hours_of_operations_paginator: ListHoursOfOperationsPaginator = client.get_paginator("list_hours_of_operations")
    list_instance_attributes_paginator: ListInstanceAttributesPaginator = client.get_paginator("list_instance_attributes")
    list_instance_storage_configs_paginator: ListInstanceStorageConfigsPaginator = client.get_paginator("list_instance_storage_configs")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    list_integration_associations_paginator: ListIntegrationAssociationsPaginator = client.get_paginator("list_integration_associations")
    list_lambda_functions_paginator: ListLambdaFunctionsPaginator = client.get_paginator("list_lambda_functions")
    list_lex_bots_paginator: ListLexBotsPaginator = client.get_paginator("list_lex_bots")
    list_phone_numbers_paginator: ListPhoneNumbersPaginator = client.get_paginator("list_phone_numbers")
    list_phone_numbers_v2_paginator: ListPhoneNumbersV2Paginator = client.get_paginator("list_phone_numbers_v2")
    list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
    list_queue_quick_connects_paginator: ListQueueQuickConnectsPaginator = client.get_paginator("list_queue_quick_connects")
    list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    list_quick_connects_paginator: ListQuickConnectsPaginator = client.get_paginator("list_quick_connects")
    list_routing_profile_queues_paginator: ListRoutingProfileQueuesPaginator = client.get_paginator("list_routing_profile_queues")
    list_routing_profiles_paginator: ListRoutingProfilesPaginator = client.get_paginator("list_routing_profiles")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_security_keys_paginator: ListSecurityKeysPaginator = client.get_paginator("list_security_keys")
    list_security_profile_permissions_paginator: ListSecurityProfilePermissionsPaginator = client.get_paginator("list_security_profile_permissions")
    list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
    list_task_templates_paginator: ListTaskTemplatesPaginator = client.get_paginator("list_task_templates")
    list_traffic_distribution_groups_paginator: ListTrafficDistributionGroupsPaginator = client.get_paginator("list_traffic_distribution_groups")
    list_use_cases_paginator: ListUseCasesPaginator = client.get_paginator("list_use_cases")
    list_user_hierarchy_groups_paginator: ListUserHierarchyGroupsPaginator = client.get_paginator("list_user_hierarchy_groups")
    list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
    search_available_phone_numbers_paginator: SearchAvailablePhoneNumbersPaginator = client.get_paginator("search_available_phone_numbers")
    search_queues_paginator: SearchQueuesPaginator = client.get_paginator("search_queues")
    search_routing_profiles_paginator: SearchRoutingProfilesPaginator = client.get_paginator("search_routing_profiles")
    search_security_profiles_paginator: SearchSecurityProfilesPaginator = client.get_paginator("search_security_profiles")
    search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    search_vocabularies_paginator: SearchVocabulariesPaginator = client.get_paginator("search_vocabularies")
    ```
"""
from datetime import datetime
from typing import Generic, Iterator, Sequence, TypeVar, Union

from botocore.paginate import PageIterator, Paginator

from .literals import (
    AgentStatusTypeType,
    ContactFlowModuleStateType,
    ContactFlowTypeType,
    EventSourceNameType,
    GroupingType,
    InstanceStorageResourceTypeType,
    IntegrationTypeType,
    LexVersionType,
    PhoneNumberCountryCodeType,
    PhoneNumberTypeType,
    QueueTypeType,
    QuickConnectTypeType,
    ReferenceTypeType,
    RulePublishStatusType,
    TaskTemplateStatusType,
    VocabularyLanguageCodeType,
    VocabularyStateType,
)
from .type_defs import (
    FiltersTypeDef,
    GetMetricDataResponseTypeDef,
    HistoricalMetricTypeDef,
    ListAgentStatusResponseTypeDef,
    ListApprovedOriginsResponseTypeDef,
    ListBotsResponseTypeDef,
    ListContactFlowModulesResponseTypeDef,
    ListContactFlowsResponseTypeDef,
    ListContactReferencesResponseTypeDef,
    ListDefaultVocabulariesResponseTypeDef,
    ListHoursOfOperationsResponseTypeDef,
    ListInstanceAttributesResponseTypeDef,
    ListInstancesResponseTypeDef,
    ListInstanceStorageConfigsResponseTypeDef,
    ListIntegrationAssociationsResponseTypeDef,
    ListLambdaFunctionsResponseTypeDef,
    ListLexBotsResponseTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListPhoneNumbersV2ResponseTypeDef,
    ListPromptsResponseTypeDef,
    ListQueueQuickConnectsResponseTypeDef,
    ListQueuesResponseTypeDef,
    ListQuickConnectsResponseTypeDef,
    ListRoutingProfileQueuesResponseTypeDef,
    ListRoutingProfilesResponseTypeDef,
    ListRulesResponseTypeDef,
    ListSecurityKeysResponseTypeDef,
    ListSecurityProfilePermissionsResponseTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListTaskTemplatesResponseTypeDef,
    ListTrafficDistributionGroupsResponseTypeDef,
    ListUseCasesResponseTypeDef,
    ListUserHierarchyGroupsResponseTypeDef,
    ListUsersResponseTypeDef,
    PaginatorConfigTypeDef,
    QueueSearchCriteriaTypeDef,
    QueueSearchFilterTypeDef,
    RoutingProfileSearchCriteriaTypeDef,
    RoutingProfileSearchFilterTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SearchQueuesResponseTypeDef,
    SearchRoutingProfilesResponseTypeDef,
    SearchSecurityProfilesResponseTypeDef,
    SearchUsersResponseTypeDef,
    SearchVocabulariesResponseTypeDef,
    SecurityProfileSearchCriteriaTypeDef,
    SecurityProfilesSearchFilterTypeDef,
    UserSearchCriteriaTypeDef,
    UserSearchFilterTypeDef,
)

__all__ = (
    "GetMetricDataPaginator",
    "ListAgentStatusesPaginator",
    "ListApprovedOriginsPaginator",
    "ListBotsPaginator",
    "ListContactFlowModulesPaginator",
    "ListContactFlowsPaginator",
    "ListContactReferencesPaginator",
    "ListDefaultVocabulariesPaginator",
    "ListHoursOfOperationsPaginator",
    "ListInstanceAttributesPaginator",
    "ListInstanceStorageConfigsPaginator",
    "ListInstancesPaginator",
    "ListIntegrationAssociationsPaginator",
    "ListLambdaFunctionsPaginator",
    "ListLexBotsPaginator",
    "ListPhoneNumbersPaginator",
    "ListPhoneNumbersV2Paginator",
    "ListPromptsPaginator",
    "ListQueueQuickConnectsPaginator",
    "ListQueuesPaginator",
    "ListQuickConnectsPaginator",
    "ListRoutingProfileQueuesPaginator",
    "ListRoutingProfilesPaginator",
    "ListRulesPaginator",
    "ListSecurityKeysPaginator",
    "ListSecurityProfilePermissionsPaginator",
    "ListSecurityProfilesPaginator",
    "ListTaskTemplatesPaginator",
    "ListTrafficDistributionGroupsPaginator",
    "ListUseCasesPaginator",
    "ListUserHierarchyGroupsPaginator",
    "ListUsersPaginator",
    "SearchAvailablePhoneNumbersPaginator",
    "SearchQueuesPaginator",
    "SearchRoutingProfilesPaginator",
    "SearchSecurityProfilesPaginator",
    "SearchUsersPaginator",
    "SearchVocabulariesPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetMetricDataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.GetMetricData)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#getmetricdatapaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        StartTime: Union[datetime, str],
        EndTime: Union[datetime, str],
        Filters: FiltersTypeDef,
        HistoricalMetrics: Sequence[HistoricalMetricTypeDef],
        Groupings: Sequence[GroupingType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetMetricDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.GetMetricData.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#getmetricdatapaginator)
        """


class ListAgentStatusesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListAgentStatuses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listagentstatusespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        AgentStatusTypes: Sequence[AgentStatusTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAgentStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListAgentStatuses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listagentstatusespaginator)
        """


class ListApprovedOriginsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListApprovedOrigins)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listapprovedoriginspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListApprovedOriginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListApprovedOrigins.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listapprovedoriginspaginator)
        """


class ListBotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListBots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listbotspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        LexVersion: LexVersionType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListBots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listbotspaginator)
        """


class ListContactFlowModulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListContactFlowModules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowmodulespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        ContactFlowModuleState: ContactFlowModuleStateType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListContactFlowModules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowmodulespaginator)
        """


class ListContactFlowsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListContactFlows)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        ContactFlowTypes: Sequence[ContactFlowTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListContactFlows.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactflowspaginator)
        """


class ListContactReferencesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListContactReferences)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactreferencespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        ContactId: str,
        ReferenceTypes: Sequence[ReferenceTypeType],
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListContactReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListContactReferences.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listcontactreferencespaginator)
        """


class ListDefaultVocabulariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListDefaultVocabularies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listdefaultvocabulariespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        LanguageCode: VocabularyLanguageCodeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListDefaultVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListDefaultVocabularies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listdefaultvocabulariespaginator)
        """


class ListHoursOfOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListHoursOfOperations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listhoursofoperationspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListHoursOfOperations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listhoursofoperationspaginator)
        """


class ListInstanceAttributesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListInstanceAttributes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstanceattributespaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstanceAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListInstanceAttributes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstanceattributespaginator)
        """


class ListInstanceStorageConfigsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListInstanceStorageConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancestorageconfigspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        ResourceType: InstanceStorageResourceTypeType,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstanceStorageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListInstanceStorageConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancestorageconfigspaginator)
        """


class ListInstancesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListInstances)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancespaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListInstances.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listinstancespaginator)
        """


class ListIntegrationAssociationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListIntegrationAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listintegrationassociationspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        IntegrationType: IntegrationTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListIntegrationAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listintegrationassociationspaginator)
        """


class ListLambdaFunctionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListLambdaFunctions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlambdafunctionspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLambdaFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListLambdaFunctions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlambdafunctionspaginator)
        """


class ListLexBotsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListLexBots)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlexbotspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListLexBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListLexBots.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listlexbotspaginator)
        """


class ListPhoneNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListPhoneNumbers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumberspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        PhoneNumberTypes: Sequence[PhoneNumberTypeType] = ...,
        PhoneNumberCountryCodes: Sequence[PhoneNumberCountryCodeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListPhoneNumbers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumberspaginator)
        """


class ListPhoneNumbersV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListPhoneNumbersV2)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumbersv2paginator)
    """

    def paginate(
        self,
        *,
        TargetArn: str = ...,
        PhoneNumberCountryCodes: Sequence[PhoneNumberCountryCodeType] = ...,
        PhoneNumberTypes: Sequence[PhoneNumberTypeType] = ...,
        PhoneNumberPrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPhoneNumbersV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListPhoneNumbersV2.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listphonenumbersv2paginator)
        """


class ListPromptsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListPrompts)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listpromptspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListPrompts.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listpromptspaginator)
        """


class ListQueueQuickConnectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListQueueQuickConnects)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuequickconnectspaginator)
    """

    def paginate(
        self, *, InstanceId: str, QueueId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListQueueQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListQueueQuickConnects.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuequickconnectspaginator)
        """


class ListQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListQueues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        QueueTypes: Sequence[QueueTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListQueues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listqueuespaginator)
        """


class ListQuickConnectsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListQuickConnects)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listquickconnectspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        QuickConnectTypes: Sequence[QuickConnectTypeType] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListQuickConnects.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listquickconnectspaginator)
        """


class ListRoutingProfileQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListRoutingProfileQueues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilequeuespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        RoutingProfileId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRoutingProfileQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListRoutingProfileQueues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilequeuespaginator)
        """


class ListRoutingProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListRoutingProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilespaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListRoutingProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listroutingprofilespaginator)
        """


class ListRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listrulespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        PublishStatus: RulePublishStatusType = ...,
        EventSourceName: EventSourceNameType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listrulespaginator)
        """


class ListSecurityKeysPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListSecurityKeys)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecuritykeyspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListSecurityKeys.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecuritykeyspaginator)
        """


class ListSecurityProfilePermissionsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListSecurityProfilePermissions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilepermissionspaginator)
    """

    def paginate(
        self,
        *,
        SecurityProfileId: str,
        InstanceId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityProfilePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListSecurityProfilePermissions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilepermissionspaginator)
        """


class ListSecurityProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListSecurityProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilespaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListSecurityProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listsecurityprofilespaginator)
        """


class ListTaskTemplatesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListTaskTemplates)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtasktemplatespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        Status: TaskTemplateStatusType = ...,
        Name: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTaskTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListTaskTemplates.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtasktemplatespaginator)
        """


class ListTrafficDistributionGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListTrafficDistributionGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtrafficdistributiongroupspaginator)
    """

    def paginate(
        self, *, InstanceId: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTrafficDistributionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListTrafficDistributionGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listtrafficdistributiongroupspaginator)
        """


class ListUseCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListUseCases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listusecasespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        IntegrationAssociationId: str,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUseCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListUseCases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listusecasespaginator)
        """


class ListUserHierarchyGroupsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListUserHierarchyGroups)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserhierarchygroupspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListUserHierarchyGroups.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserhierarchygroupspaginator)
        """


class ListUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserspaginator)
    """

    def paginate(
        self, *, InstanceId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.ListUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#listuserspaginator)
        """


class SearchAvailablePhoneNumbersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchAvailablePhoneNumbers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchavailablephonenumberspaginator)
    """

    def paginate(
        self,
        *,
        TargetArn: str,
        PhoneNumberCountryCode: PhoneNumberCountryCodeType,
        PhoneNumberType: PhoneNumberTypeType,
        PhoneNumberPrefix: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchAvailablePhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchAvailablePhoneNumbers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchavailablephonenumberspaginator)
        """


class SearchQueuesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchQueues)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchqueuespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        SearchFilter: QueueSearchFilterTypeDef = ...,
        SearchCriteria: "QueueSearchCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchQueues.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchqueuespaginator)
        """


class SearchRoutingProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchRoutingProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchroutingprofilespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        SearchFilter: RoutingProfileSearchFilterTypeDef = ...,
        SearchCriteria: "RoutingProfileSearchCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchRoutingProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchroutingprofilespaginator)
        """


class SearchSecurityProfilesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchSecurityProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchsecurityprofilespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        SearchCriteria: "SecurityProfileSearchCriteriaTypeDef" = ...,
        SearchFilter: SecurityProfilesSearchFilterTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchSecurityProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchsecurityprofilespaginator)
        """


class SearchUsersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchUsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchuserspaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str = ...,
        SearchFilter: UserSearchFilterTypeDef = ...,
        SearchCriteria: "UserSearchCriteriaTypeDef" = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchUsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchuserspaginator)
        """


class SearchVocabulariesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchVocabularies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchvocabulariespaginator)
    """

    def paginate(
        self,
        *,
        InstanceId: str,
        State: VocabularyStateType = ...,
        NameStartsWith: str = ...,
        LanguageCode: VocabularyLanguageCodeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[SearchVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect.html#Connect.Paginator.SearchVocabularies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_connect/paginators/#searchvocabulariespaginator)
        """
