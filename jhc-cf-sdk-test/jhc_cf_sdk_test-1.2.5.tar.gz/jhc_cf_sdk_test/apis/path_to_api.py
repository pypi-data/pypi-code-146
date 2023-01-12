import typing_extensions

from jhc_cf_sdk_test.paths import PathValues
from jhc_cf_sdk_test.apis.paths.api_v1_access_rules import ApiV1AccessRules
from jhc_cf_sdk_test.apis.paths.api_v1_access_rules_rule_id import ApiV1AccessRulesRuleId
from jhc_cf_sdk_test.apis.paths.api_v1_access_rules_rule_id_approvers import ApiV1AccessRulesRuleIdApprovers
from jhc_cf_sdk_test.apis.paths.api_v1_requests import ApiV1Requests
from jhc_cf_sdk_test.apis.paths.api_v1_requests_upcoming import ApiV1RequestsUpcoming
from jhc_cf_sdk_test.apis.paths.api_v1_requests_past import ApiV1RequestsPast
from jhc_cf_sdk_test.apis.paths.api_v1_requests_request_id import ApiV1RequestsRequestId
from jhc_cf_sdk_test.apis.paths.api_v1_requests_request_id_events import ApiV1RequestsRequestIdEvents
from jhc_cf_sdk_test.apis.paths.api_v1_requests_request_id_review import ApiV1RequestsRequestIdReview
from jhc_cf_sdk_test.apis.paths.api_v1_requests_request_id_cancel import ApiV1RequestsRequestIdCancel
from jhc_cf_sdk_test.apis.paths.api_v1_requests_requestid_revoke import ApiV1RequestsRequestidRevoke
from jhc_cf_sdk_test.apis.paths.api_v1_requests_request_id_access_instructions import ApiV1RequestsRequestIdAccessInstructions
from jhc_cf_sdk_test.apis.paths.api_v1_requests_request_id_access_token import ApiV1RequestsRequestIdAccessToken
from jhc_cf_sdk_test.apis.paths.api_v1_users_user_id import ApiV1UsersUserId
from jhc_cf_sdk_test.apis.paths.api_v1_users_me import ApiV1UsersMe
from jhc_cf_sdk_test.apis.paths.api_v1_admin_access_rules import ApiV1AdminAccessRules
from jhc_cf_sdk_test.apis.paths.api_v1_admin_access_rules_rule_id import ApiV1AdminAccessRulesRuleId
from jhc_cf_sdk_test.apis.paths.api_v1_admin_access_rules_rule_id_archive import ApiV1AdminAccessRulesRuleIdArchive
from jhc_cf_sdk_test.apis.paths.api_v1_admin_access_rules_rule_id_versions import ApiV1AdminAccessRulesRuleIdVersions
from jhc_cf_sdk_test.apis.paths.api_v1_admin_access_rules_rule_id_versions_version import ApiV1AdminAccessRulesRuleIdVersionsVersion
from jhc_cf_sdk_test.apis.paths.api_v1_admin_deployment_version import ApiV1AdminDeploymentVersion
from jhc_cf_sdk_test.apis.paths.api_v1_admin_requests import ApiV1AdminRequests
from jhc_cf_sdk_test.apis.paths.api_v1_admin_requests_request_id import ApiV1AdminRequestsRequestId
from jhc_cf_sdk_test.apis.paths.api_v1_admin_users_user_id import ApiV1AdminUsersUserId
from jhc_cf_sdk_test.apis.paths.api_v1_admin_users import ApiV1AdminUsers
from jhc_cf_sdk_test.apis.paths.api_v1_admin_groups import ApiV1AdminGroups
from jhc_cf_sdk_test.apis.paths.api_v1_admin_groups_group_id import ApiV1AdminGroupsGroupId
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providers import ApiV1AdminProviders
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providers_provider_id import ApiV1AdminProvidersProviderId
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providers_provider_id_args import ApiV1AdminProvidersProviderIdArgs
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providers_provider_id_args_arg_id_options import ApiV1AdminProvidersProviderIdArgsArgIdOptions
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providersetups import ApiV1AdminProvidersetups
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providersetups_providersetup_id import ApiV1AdminProvidersetupsProvidersetupId
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providersetups_providersetup_id_instructions import ApiV1AdminProvidersetupsProvidersetupIdInstructions
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providersetups_providersetup_id_validate import ApiV1AdminProvidersetupsProvidersetupIdValidate
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providersetups_providersetup_id_complete import ApiV1AdminProvidersetupsProvidersetupIdComplete
from jhc_cf_sdk_test.apis.paths.api_v1_admin_providersetups_providersetup_id_steps_step_index_complete import ApiV1AdminProvidersetupsProvidersetupIdStepsStepIndexComplete
from jhc_cf_sdk_test.apis.paths.api_v1_admin_identity_sync import ApiV1AdminIdentitySync
from jhc_cf_sdk_test.apis.paths.api_v1_admin_identity import ApiV1AdminIdentity
from jhc_cf_sdk_test.apis.paths.api_v1_access_rules_lookup import ApiV1AccessRulesLookup
from jhc_cf_sdk_test.apis.paths.api_v1_favorites import ApiV1Favorites
from jhc_cf_sdk_test.apis.paths.api_v1_favorites_id import ApiV1FavoritesId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V1_ACCESSRULES: ApiV1AccessRules,
        PathValues.API_V1_ACCESSRULES_RULE_ID: ApiV1AccessRulesRuleId,
        PathValues.API_V1_ACCESSRULES_RULE_ID_APPROVERS: ApiV1AccessRulesRuleIdApprovers,
        PathValues.API_V1_REQUESTS: ApiV1Requests,
        PathValues.API_V1_REQUESTS_UPCOMING: ApiV1RequestsUpcoming,
        PathValues.API_V1_REQUESTS_PAST: ApiV1RequestsPast,
        PathValues.API_V1_REQUESTS_REQUEST_ID: ApiV1RequestsRequestId,
        PathValues.API_V1_REQUESTS_REQUEST_ID_EVENTS: ApiV1RequestsRequestIdEvents,
        PathValues.API_V1_REQUESTS_REQUEST_ID_REVIEW: ApiV1RequestsRequestIdReview,
        PathValues.API_V1_REQUESTS_REQUEST_ID_CANCEL: ApiV1RequestsRequestIdCancel,
        PathValues.API_V1_REQUESTS_REQUESTID_REVOKE: ApiV1RequestsRequestidRevoke,
        PathValues.API_V1_REQUESTS_REQUEST_ID_ACCESSINSTRUCTIONS: ApiV1RequestsRequestIdAccessInstructions,
        PathValues.API_V1_REQUESTS_REQUEST_ID_ACCESSTOKEN: ApiV1RequestsRequestIdAccessToken,
        PathValues.API_V1_USERS_USER_ID: ApiV1UsersUserId,
        PathValues.API_V1_USERS_ME: ApiV1UsersMe,
        PathValues.API_V1_ADMIN_ACCESSRULES: ApiV1AdminAccessRules,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID: ApiV1AdminAccessRulesRuleId,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID_ARCHIVE: ApiV1AdminAccessRulesRuleIdArchive,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID_VERSIONS: ApiV1AdminAccessRulesRuleIdVersions,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID_VERSIONS_VERSION: ApiV1AdminAccessRulesRuleIdVersionsVersion,
        PathValues.API_V1_ADMIN_DEPLOYMENT_VERSION: ApiV1AdminDeploymentVersion,
        PathValues.API_V1_ADMIN_REQUESTS: ApiV1AdminRequests,
        PathValues.API_V1_ADMIN_REQUESTS_REQUEST_ID: ApiV1AdminRequestsRequestId,
        PathValues.API_V1_ADMIN_USERS_USER_ID: ApiV1AdminUsersUserId,
        PathValues.API_V1_ADMIN_USERS: ApiV1AdminUsers,
        PathValues.API_V1_ADMIN_GROUPS: ApiV1AdminGroups,
        PathValues.API_V1_ADMIN_GROUPS_GROUP_ID: ApiV1AdminGroupsGroupId,
        PathValues.API_V1_ADMIN_PROVIDERS: ApiV1AdminProviders,
        PathValues.API_V1_ADMIN_PROVIDERS_PROVIDER_ID: ApiV1AdminProvidersProviderId,
        PathValues.API_V1_ADMIN_PROVIDERS_PROVIDER_ID_ARGS: ApiV1AdminProvidersProviderIdArgs,
        PathValues.API_V1_ADMIN_PROVIDERS_PROVIDER_ID_ARGS_ARG_ID_OPTIONS: ApiV1AdminProvidersProviderIdArgsArgIdOptions,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS: ApiV1AdminProvidersetups,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID: ApiV1AdminProvidersetupsProvidersetupId,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_INSTRUCTIONS: ApiV1AdminProvidersetupsProvidersetupIdInstructions,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_VALIDATE: ApiV1AdminProvidersetupsProvidersetupIdValidate,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_COMPLETE: ApiV1AdminProvidersetupsProvidersetupIdComplete,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_STEPS_STEP_INDEX_COMPLETE: ApiV1AdminProvidersetupsProvidersetupIdStepsStepIndexComplete,
        PathValues.API_V1_ADMIN_IDENTITY_SYNC: ApiV1AdminIdentitySync,
        PathValues.API_V1_ADMIN_IDENTITY: ApiV1AdminIdentity,
        PathValues.API_V1_ACCESSRULES_LOOKUP: ApiV1AccessRulesLookup,
        PathValues.API_V1_FAVORITES: ApiV1Favorites,
        PathValues.API_V1_FAVORITES_ID: ApiV1FavoritesId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V1_ACCESSRULES: ApiV1AccessRules,
        PathValues.API_V1_ACCESSRULES_RULE_ID: ApiV1AccessRulesRuleId,
        PathValues.API_V1_ACCESSRULES_RULE_ID_APPROVERS: ApiV1AccessRulesRuleIdApprovers,
        PathValues.API_V1_REQUESTS: ApiV1Requests,
        PathValues.API_V1_REQUESTS_UPCOMING: ApiV1RequestsUpcoming,
        PathValues.API_V1_REQUESTS_PAST: ApiV1RequestsPast,
        PathValues.API_V1_REQUESTS_REQUEST_ID: ApiV1RequestsRequestId,
        PathValues.API_V1_REQUESTS_REQUEST_ID_EVENTS: ApiV1RequestsRequestIdEvents,
        PathValues.API_V1_REQUESTS_REQUEST_ID_REVIEW: ApiV1RequestsRequestIdReview,
        PathValues.API_V1_REQUESTS_REQUEST_ID_CANCEL: ApiV1RequestsRequestIdCancel,
        PathValues.API_V1_REQUESTS_REQUESTID_REVOKE: ApiV1RequestsRequestidRevoke,
        PathValues.API_V1_REQUESTS_REQUEST_ID_ACCESSINSTRUCTIONS: ApiV1RequestsRequestIdAccessInstructions,
        PathValues.API_V1_REQUESTS_REQUEST_ID_ACCESSTOKEN: ApiV1RequestsRequestIdAccessToken,
        PathValues.API_V1_USERS_USER_ID: ApiV1UsersUserId,
        PathValues.API_V1_USERS_ME: ApiV1UsersMe,
        PathValues.API_V1_ADMIN_ACCESSRULES: ApiV1AdminAccessRules,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID: ApiV1AdminAccessRulesRuleId,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID_ARCHIVE: ApiV1AdminAccessRulesRuleIdArchive,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID_VERSIONS: ApiV1AdminAccessRulesRuleIdVersions,
        PathValues.API_V1_ADMIN_ACCESSRULES_RULE_ID_VERSIONS_VERSION: ApiV1AdminAccessRulesRuleIdVersionsVersion,
        PathValues.API_V1_ADMIN_DEPLOYMENT_VERSION: ApiV1AdminDeploymentVersion,
        PathValues.API_V1_ADMIN_REQUESTS: ApiV1AdminRequests,
        PathValues.API_V1_ADMIN_REQUESTS_REQUEST_ID: ApiV1AdminRequestsRequestId,
        PathValues.API_V1_ADMIN_USERS_USER_ID: ApiV1AdminUsersUserId,
        PathValues.API_V1_ADMIN_USERS: ApiV1AdminUsers,
        PathValues.API_V1_ADMIN_GROUPS: ApiV1AdminGroups,
        PathValues.API_V1_ADMIN_GROUPS_GROUP_ID: ApiV1AdminGroupsGroupId,
        PathValues.API_V1_ADMIN_PROVIDERS: ApiV1AdminProviders,
        PathValues.API_V1_ADMIN_PROVIDERS_PROVIDER_ID: ApiV1AdminProvidersProviderId,
        PathValues.API_V1_ADMIN_PROVIDERS_PROVIDER_ID_ARGS: ApiV1AdminProvidersProviderIdArgs,
        PathValues.API_V1_ADMIN_PROVIDERS_PROVIDER_ID_ARGS_ARG_ID_OPTIONS: ApiV1AdminProvidersProviderIdArgsArgIdOptions,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS: ApiV1AdminProvidersetups,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID: ApiV1AdminProvidersetupsProvidersetupId,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_INSTRUCTIONS: ApiV1AdminProvidersetupsProvidersetupIdInstructions,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_VALIDATE: ApiV1AdminProvidersetupsProvidersetupIdValidate,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_COMPLETE: ApiV1AdminProvidersetupsProvidersetupIdComplete,
        PathValues.API_V1_ADMIN_PROVIDERSETUPS_PROVIDERSETUP_ID_STEPS_STEP_INDEX_COMPLETE: ApiV1AdminProvidersetupsProvidersetupIdStepsStepIndexComplete,
        PathValues.API_V1_ADMIN_IDENTITY_SYNC: ApiV1AdminIdentitySync,
        PathValues.API_V1_ADMIN_IDENTITY: ApiV1AdminIdentity,
        PathValues.API_V1_ACCESSRULES_LOOKUP: ApiV1AccessRulesLookup,
        PathValues.API_V1_FAVORITES: ApiV1Favorites,
        PathValues.API_V1_FAVORITES_ID: ApiV1FavoritesId,
    }
)
