'''
# `azurerm_windows_function_app_slot`

Refer to the Terraform Registory for docs: [`azurerm_windows_function_app_slot`](https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class WindowsFunctionAppSlot(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlot",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot azurerm_windows_function_app_slot}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_app_id: builtins.str,
        name: builtins.str,
        site_config: typing.Union["WindowsFunctionAppSlotSiteConfig", typing.Dict[builtins.str, typing.Any]],
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        backup: typing.Optional[typing.Union["WindowsFunctionAppSlotBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotConnectionString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        daily_memory_time_quota: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        functions_extension_version: typing.Optional[builtins.str] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["WindowsFunctionAppSlotIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
        storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
        storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WindowsFunctionAppSlotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot azurerm_windows_function_app_slot} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_app_id: The ID of the Windows Function App this Slot is a member of. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#function_app_id WindowsFunctionAppSlot#function_app_id}
        :param name: Specifies the name of the Windows Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        :param site_config: site_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#site_config WindowsFunctionAppSlot#site_config}
        :param app_settings: A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_settings WindowsFunctionAppSlot#app_settings}
        :param auth_settings: auth_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#auth_settings WindowsFunctionAppSlot#auth_settings}
        :param backup: backup block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#backup WindowsFunctionAppSlot#backup}
        :param builtin_logging_enabled: Should built in logging be enabled. Configures ``AzureWebJobsDashboard`` app setting based on the configured storage setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#builtin_logging_enabled WindowsFunctionAppSlot#builtin_logging_enabled}
        :param client_certificate_enabled: Should the Function App Slot use Client Certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_enabled WindowsFunctionAppSlot#client_certificate_enabled}
        :param client_certificate_exclusion_paths: Paths to exclude when using client certificates, separated by ; Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_exclusion_paths WindowsFunctionAppSlot#client_certificate_exclusion_paths}
        :param client_certificate_mode: The mode of the Function App Slot's client certificates requirement for incoming requests. Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_mode WindowsFunctionAppSlot#client_certificate_mode}
        :param connection_string: connection_string block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#connection_string WindowsFunctionAppSlot#connection_string}
        :param content_share_force_disabled: Force disable the content share settings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#content_share_force_disabled WindowsFunctionAppSlot#content_share_force_disabled}
        :param daily_memory_time_quota: The amount of memory in gigabyte-seconds that your application is allowed to consume per day. Setting this value only affects function apps in Consumption Plans. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#daily_memory_time_quota WindowsFunctionAppSlot#daily_memory_time_quota}
        :param enabled: Is the Windows Function App Slot enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        :param functions_extension_version: The runtime version associated with the Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#functions_extension_version WindowsFunctionAppSlot#functions_extension_version}
        :param https_only: Can the Function App Slot only be accessed via HTTPS? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#https_only WindowsFunctionAppSlot#https_only}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#id WindowsFunctionAppSlot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#identity WindowsFunctionAppSlot#identity}
        :param key_vault_reference_identity_id: The User Assigned Identity to use for Key Vault access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#key_vault_reference_identity_id WindowsFunctionAppSlot#key_vault_reference_identity_id}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account WindowsFunctionAppSlot#storage_account}
        :param storage_account_access_key: The access key which will be used to access the storage account for the Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_access_key WindowsFunctionAppSlot#storage_account_access_key}
        :param storage_account_name: The backend storage account name which will be used by this Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_name WindowsFunctionAppSlot#storage_account_name}
        :param storage_key_vault_secret_id: The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_key_vault_secret_id WindowsFunctionAppSlot#storage_key_vault_secret_id}
        :param storage_uses_managed_identity: Should the Function App Slot use its Managed Identity to access storage? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_uses_managed_identity WindowsFunctionAppSlot#storage_uses_managed_identity}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#tags WindowsFunctionAppSlot#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#timeouts WindowsFunctionAppSlot#timeouts}
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c39c7cfc5bdabe0a2a399b8ca12f11efcafceb20bb181001c1278d00dce79f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WindowsFunctionAppSlotConfig(
            function_app_id=function_app_id,
            name=name,
            site_config=site_config,
            app_settings=app_settings,
            auth_settings=auth_settings,
            backup=backup,
            builtin_logging_enabled=builtin_logging_enabled,
            client_certificate_enabled=client_certificate_enabled,
            client_certificate_exclusion_paths=client_certificate_exclusion_paths,
            client_certificate_mode=client_certificate_mode,
            connection_string=connection_string,
            content_share_force_disabled=content_share_force_disabled,
            daily_memory_time_quota=daily_memory_time_quota,
            enabled=enabled,
            functions_extension_version=functions_extension_version,
            https_only=https_only,
            id=id,
            identity=identity,
            key_vault_reference_identity_id=key_vault_reference_identity_id,
            storage_account=storage_account,
            storage_account_access_key=storage_account_access_key,
            storage_account_name=storage_account_name,
            storage_key_vault_secret_id=storage_key_vault_secret_id,
            storage_uses_managed_identity=storage_uses_managed_identity,
            tags=tags,
            timeouts=timeouts,
            virtual_network_subnet_id=virtual_network_subnet_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAuthSettings")
    def put_auth_settings(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_directory: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsFacebook", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsGoogle", typing.Dict[builtins.str, typing.Any]]] = None,
        issuer: typing.Optional[builtins.str] = None,
        microsoft: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsMicrosoft", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_client_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Should the Authentication / Authorization feature be enabled? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#active_directory WindowsFunctionAppSlot#active_directory}
        :param additional_login_parameters: Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#additional_login_parameters WindowsFunctionAppSlot#additional_login_parameters}
        :param allowed_external_redirect_urls: Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_external_redirect_urls WindowsFunctionAppSlot#allowed_external_redirect_urls}
        :param default_provider: The default authentication provider to use when multiple providers are configured. Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#default_provider WindowsFunctionAppSlot#default_provider}
        :param facebook: facebook block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#facebook WindowsFunctionAppSlot#facebook}
        :param github: github block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#github WindowsFunctionAppSlot#github}
        :param google: google block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#google WindowsFunctionAppSlot#google}
        :param issuer: The OpenID Connect Issuer URI that represents the entity which issues access tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#issuer WindowsFunctionAppSlot#issuer}
        :param microsoft: microsoft block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#microsoft WindowsFunctionAppSlot#microsoft}
        :param runtime_version: The RuntimeVersion of the Authentication / Authorization feature in use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#runtime_version WindowsFunctionAppSlot#runtime_version}
        :param token_refresh_extension_hours: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#token_refresh_extension_hours WindowsFunctionAppSlot#token_refresh_extension_hours}
        :param token_store_enabled: Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#token_store_enabled WindowsFunctionAppSlot#token_store_enabled}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#twitter WindowsFunctionAppSlot#twitter}
        :param unauthenticated_client_action: The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#unauthenticated_client_action WindowsFunctionAppSlot#unauthenticated_client_action}
        '''
        value = WindowsFunctionAppSlotAuthSettings(
            enabled=enabled,
            active_directory=active_directory,
            additional_login_parameters=additional_login_parameters,
            allowed_external_redirect_urls=allowed_external_redirect_urls,
            default_provider=default_provider,
            facebook=facebook,
            github=github,
            google=google,
            issuer=issuer,
            microsoft=microsoft,
            runtime_version=runtime_version,
            token_refresh_extension_hours=token_refresh_extension_hours,
            token_store_enabled=token_store_enabled,
            twitter=twitter,
            unauthenticated_client_action=unauthenticated_client_action,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthSettings", [value]))

    @jsii.member(jsii_name="putBackup")
    def put_backup(
        self,
        *,
        name: builtins.str,
        schedule: typing.Union["WindowsFunctionAppSlotBackupSchedule", typing.Dict[builtins.str, typing.Any]],
        storage_account_url: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name which should be used for this Backup. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#schedule WindowsFunctionAppSlot#schedule}
        :param storage_account_url: The SAS URL to the container. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_url WindowsFunctionAppSlot#storage_account_url}
        :param enabled: Should this backup job be enabled? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        '''
        value = WindowsFunctionAppSlotBackup(
            name=name,
            schedule=schedule,
            storage_account_url=storage_account_url,
            enabled=enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

    @jsii.member(jsii_name="putConnectionString")
    def put_connection_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotConnectionString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a9882e2b66377586d7aa196327709891fca2565cf9b4117d99d9ec58b7f177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectionString", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#identity_ids WindowsFunctionAppSlot#identity_ids}.
        '''
        value = WindowsFunctionAppSlotIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putSiteConfig")
    def put_site_config(
        self,
        *,
        always_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_definition_url: typing.Optional[builtins.str] = None,
        api_management_api_id: typing.Optional[builtins.str] = None,
        app_command_line: typing.Optional[builtins.str] = None,
        application_insights_connection_string: typing.Optional[builtins.str] = None,
        application_insights_key: typing.Optional[builtins.str] = None,
        application_stack: typing.Optional[typing.Union["WindowsFunctionAppSlotSiteConfigApplicationStack", typing.Dict[builtins.str, typing.Any]]] = None,
        app_scale_limit: typing.Optional[jsii.Number] = None,
        app_service_logs: typing.Optional[typing.Union["WindowsFunctionAppSlotSiteConfigAppServiceLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_swap_slot_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union["WindowsFunctionAppSlotSiteConfigCors", typing.Dict[builtins.str, typing.Any]]] = None,
        default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
        elastic_instance_minimum: typing.Optional[jsii.Number] = None,
        ftps_state: typing.Optional[builtins.str] = None,
        health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        load_balancing_mode: typing.Optional[builtins.str] = None,
        managed_pipeline_mode: typing.Optional[builtins.str] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        pre_warmed_instance_count: typing.Optional[jsii.Number] = None,
        remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_debugging_version: typing.Optional[builtins.str] = None,
        runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm_minimum_tls_version: typing.Optional[builtins.str] = None,
        scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param always_on: If this Windows Web App is Always On enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#always_on WindowsFunctionAppSlot#always_on}
        :param api_definition_url: The URL of the API definition that describes this Windows Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#api_definition_url WindowsFunctionAppSlot#api_definition_url}
        :param api_management_api_id: The ID of the API Management API for this Windows Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#api_management_api_id WindowsFunctionAppSlot#api_management_api_id}
        :param app_command_line: The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_command_line WindowsFunctionAppSlot#app_command_line}
        :param application_insights_connection_string: The Connection String for linking the Windows Function App to Application Insights. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_insights_connection_string WindowsFunctionAppSlot#application_insights_connection_string}
        :param application_insights_key: The Instrumentation Key for connecting the Windows Function App to Application Insights. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_insights_key WindowsFunctionAppSlot#application_insights_key}
        :param application_stack: application_stack block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_stack WindowsFunctionAppSlot#application_stack}
        :param app_scale_limit: The number of workers this function app can scale out to. Only applicable to apps on the Consumption and Premium plan. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_scale_limit WindowsFunctionAppSlot#app_scale_limit}
        :param app_service_logs: app_service_logs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_service_logs WindowsFunctionAppSlot#app_service_logs}
        :param auto_swap_slot_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#auto_swap_slot_name WindowsFunctionAppSlot#auto_swap_slot_name}.
        :param cors: cors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#cors WindowsFunctionAppSlot#cors}
        :param default_documents: Specifies a list of Default Documents for the Windows Web App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#default_documents WindowsFunctionAppSlot#default_documents}
        :param elastic_instance_minimum: The number of minimum instances for this Windows Function App. Only affects apps on Elastic Premium plans. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#elastic_instance_minimum WindowsFunctionAppSlot#elastic_instance_minimum}
        :param ftps_state: State of FTP / FTPS service for this function app. Possible values include: ``AllAllowed``, ``FtpsOnly`` and ``Disabled``. Defaults to ``Disabled``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ftps_state WindowsFunctionAppSlot#ftps_state}
        :param health_check_eviction_time_in_min: The amount of time in minutes that a node is unhealthy before being removed from the load balancer. Possible values are between ``2`` and ``10``. Defaults to ``10``. Only valid in conjunction with ``health_check_path`` Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#health_check_eviction_time_in_min WindowsFunctionAppSlot#health_check_eviction_time_in_min}
        :param health_check_path: The path to be checked for this function app health. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#health_check_path WindowsFunctionAppSlot#health_check_path}
        :param http2_enabled: Specifies if the http2 protocol should be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#http2_enabled WindowsFunctionAppSlot#http2_enabled}
        :param ip_restriction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_restriction WindowsFunctionAppSlot#ip_restriction}.
        :param load_balancing_mode: The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#load_balancing_mode WindowsFunctionAppSlot#load_balancing_mode}
        :param managed_pipeline_mode: The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#managed_pipeline_mode WindowsFunctionAppSlot#managed_pipeline_mode}
        :param minimum_tls_version: The configures the minimum version of TLS required for SSL requests. Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#minimum_tls_version WindowsFunctionAppSlot#minimum_tls_version}
        :param pre_warmed_instance_count: The number of pre-warmed instances for this function app. Only affects apps on an Elastic Premium plan. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#pre_warmed_instance_count WindowsFunctionAppSlot#pre_warmed_instance_count}
        :param remote_debugging_enabled: Should Remote Debugging be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#remote_debugging_enabled WindowsFunctionAppSlot#remote_debugging_enabled}
        :param remote_debugging_version: The Remote Debugging Version. Possible values include ``VS2017``, ``VS2019``, and ``VS2022``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#remote_debugging_version WindowsFunctionAppSlot#remote_debugging_version}
        :param runtime_scale_monitoring_enabled: Should Functions Runtime Scale Monitoring be enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#runtime_scale_monitoring_enabled WindowsFunctionAppSlot#runtime_scale_monitoring_enabled}
        :param scm_ip_restriction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_ip_restriction WindowsFunctionAppSlot#scm_ip_restriction}.
        :param scm_minimum_tls_version: Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_minimum_tls_version WindowsFunctionAppSlot#scm_minimum_tls_version}
        :param scm_use_main_ip_restriction: Should the Windows Function App ``ip_restriction`` configuration be used for the SCM also. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_use_main_ip_restriction WindowsFunctionAppSlot#scm_use_main_ip_restriction}
        :param use32_bit_worker: Should the Windows Web App use a 32-bit worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_32_bit_worker WindowsFunctionAppSlot#use_32_bit_worker}
        :param vnet_route_all_enabled: Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#vnet_route_all_enabled WindowsFunctionAppSlot#vnet_route_all_enabled}
        :param websockets_enabled: Should Web Sockets be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#websockets_enabled WindowsFunctionAppSlot#websockets_enabled}
        :param worker_count: The number of Workers for this Windows Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#worker_count WindowsFunctionAppSlot#worker_count}
        '''
        value = WindowsFunctionAppSlotSiteConfig(
            always_on=always_on,
            api_definition_url=api_definition_url,
            api_management_api_id=api_management_api_id,
            app_command_line=app_command_line,
            application_insights_connection_string=application_insights_connection_string,
            application_insights_key=application_insights_key,
            application_stack=application_stack,
            app_scale_limit=app_scale_limit,
            app_service_logs=app_service_logs,
            auto_swap_slot_name=auto_swap_slot_name,
            cors=cors,
            default_documents=default_documents,
            elastic_instance_minimum=elastic_instance_minimum,
            ftps_state=ftps_state,
            health_check_eviction_time_in_min=health_check_eviction_time_in_min,
            health_check_path=health_check_path,
            http2_enabled=http2_enabled,
            ip_restriction=ip_restriction,
            load_balancing_mode=load_balancing_mode,
            managed_pipeline_mode=managed_pipeline_mode,
            minimum_tls_version=minimum_tls_version,
            pre_warmed_instance_count=pre_warmed_instance_count,
            remote_debugging_enabled=remote_debugging_enabled,
            remote_debugging_version=remote_debugging_version,
            runtime_scale_monitoring_enabled=runtime_scale_monitoring_enabled,
            scm_ip_restriction=scm_ip_restriction,
            scm_minimum_tls_version=scm_minimum_tls_version,
            scm_use_main_ip_restriction=scm_use_main_ip_restriction,
            use32_bit_worker=use32_bit_worker,
            vnet_route_all_enabled=vnet_route_all_enabled,
            websockets_enabled=websockets_enabled,
            worker_count=worker_count,
        )

        return typing.cast(None, jsii.invoke(self, "putSiteConfig", [value]))

    @jsii.member(jsii_name="putStorageAccount")
    def put_storage_account(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotStorageAccount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c512eb33b5b007c360c2a69cbf614d9156b301dda9adfffa937965d42deaaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageAccount", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#create WindowsFunctionAppSlot#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#delete WindowsFunctionAppSlot#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#read WindowsFunctionAppSlot#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#update WindowsFunctionAppSlot#update}.
        '''
        value = WindowsFunctionAppSlotTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppSettings")
    def reset_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSettings", []))

    @jsii.member(jsii_name="resetAuthSettings")
    def reset_auth_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthSettings", []))

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetBuiltinLoggingEnabled")
    def reset_builtin_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuiltinLoggingEnabled", []))

    @jsii.member(jsii_name="resetClientCertificateEnabled")
    def reset_client_certificate_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateEnabled", []))

    @jsii.member(jsii_name="resetClientCertificateExclusionPaths")
    def reset_client_certificate_exclusion_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateExclusionPaths", []))

    @jsii.member(jsii_name="resetClientCertificateMode")
    def reset_client_certificate_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateMode", []))

    @jsii.member(jsii_name="resetConnectionString")
    def reset_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionString", []))

    @jsii.member(jsii_name="resetContentShareForceDisabled")
    def reset_content_share_force_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentShareForceDisabled", []))

    @jsii.member(jsii_name="resetDailyMemoryTimeQuota")
    def reset_daily_memory_time_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailyMemoryTimeQuota", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFunctionsExtensionVersion")
    def reset_functions_extension_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionsExtensionVersion", []))

    @jsii.member(jsii_name="resetHttpsOnly")
    def reset_https_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsOnly", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetKeyVaultReferenceIdentityId")
    def reset_key_vault_reference_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultReferenceIdentityId", []))

    @jsii.member(jsii_name="resetStorageAccount")
    def reset_storage_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccount", []))

    @jsii.member(jsii_name="resetStorageAccountAccessKey")
    def reset_storage_account_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountAccessKey", []))

    @jsii.member(jsii_name="resetStorageAccountName")
    def reset_storage_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountName", []))

    @jsii.member(jsii_name="resetStorageKeyVaultSecretId")
    def reset_storage_key_vault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageKeyVaultSecretId", []))

    @jsii.member(jsii_name="resetStorageUsesManagedIdentity")
    def reset_storage_uses_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageUsesManagedIdentity", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="authSettings")
    def auth_settings(self) -> "WindowsFunctionAppSlotAuthSettingsOutputReference":
        return typing.cast("WindowsFunctionAppSlotAuthSettingsOutputReference", jsii.get(self, "authSettings"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> "WindowsFunctionAppSlotBackupOutputReference":
        return typing.cast("WindowsFunctionAppSlotBackupOutputReference", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> "WindowsFunctionAppSlotConnectionStringList":
        return typing.cast("WindowsFunctionAppSlotConnectionStringList", jsii.get(self, "connectionString"))

    @builtins.property
    @jsii.member(jsii_name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomainVerificationId"))

    @builtins.property
    @jsii.member(jsii_name="defaultHostname")
    def default_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultHostname"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "WindowsFunctionAppSlotIdentityOutputReference":
        return typing.cast("WindowsFunctionAppSlotIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddressList")
    def outbound_ip_address_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIpAddressList"))

    @builtins.property
    @jsii.member(jsii_name="possibleOutboundIpAddresses")
    def possible_outbound_ip_addresses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "possibleOutboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="possibleOutboundIpAddressList")
    def possible_outbound_ip_address_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "possibleOutboundIpAddressList"))

    @builtins.property
    @jsii.member(jsii_name="siteConfig")
    def site_config(self) -> "WindowsFunctionAppSlotSiteConfigOutputReference":
        return typing.cast("WindowsFunctionAppSlotSiteConfigOutputReference", jsii.get(self, "siteConfig"))

    @builtins.property
    @jsii.member(jsii_name="siteCredential")
    def site_credential(self) -> "WindowsFunctionAppSlotSiteCredentialList":
        return typing.cast("WindowsFunctionAppSlotSiteCredentialList", jsii.get(self, "siteCredential"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "WindowsFunctionAppSlotStorageAccountList":
        return typing.cast("WindowsFunctionAppSlotStorageAccountList", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WindowsFunctionAppSlotTimeoutsOutputReference":
        return typing.cast("WindowsFunctionAppSlotTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appSettingsInput")
    def app_settings_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "appSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="authSettingsInput")
    def auth_settings_input(
        self,
    ) -> typing.Optional["WindowsFunctionAppSlotAuthSettings"]:
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettings"], jsii.get(self, "authSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional["WindowsFunctionAppSlotBackup"]:
        return typing.cast(typing.Optional["WindowsFunctionAppSlotBackup"], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="builtinLoggingEnabledInput")
    def builtin_logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "builtinLoggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabledInput")
    def client_certificate_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientCertificateEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateExclusionPathsInput")
    def client_certificate_exclusion_paths_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateExclusionPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateModeInput")
    def client_certificate_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateModeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionStringInput")
    def connection_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotConnectionString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotConnectionString"]]], jsii.get(self, "connectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="contentShareForceDisabledInput")
    def content_share_force_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "contentShareForceDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dailyMemoryTimeQuotaInput")
    def daily_memory_time_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dailyMemoryTimeQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAppIdInput")
    def function_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="functionsExtensionVersionInput")
    def functions_extension_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionsExtensionVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsOnlyInput")
    def https_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["WindowsFunctionAppSlotIdentity"]:
        return typing.cast(typing.Optional["WindowsFunctionAppSlotIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultReferenceIdentityIdInput")
    def key_vault_reference_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultReferenceIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="siteConfigInput")
    def site_config_input(self) -> typing.Optional["WindowsFunctionAppSlotSiteConfig"]:
        return typing.cast(typing.Optional["WindowsFunctionAppSlotSiteConfig"], jsii.get(self, "siteConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKeyInput")
    def storage_account_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotStorageAccount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotStorageAccount"]]], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountNameInput")
    def storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyVaultSecretIdInput")
    def storage_key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageKeyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUsesManagedIdentityInput")
    def storage_uses_managed_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageUsesManagedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["WindowsFunctionAppSlotTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["WindowsFunctionAppSlotTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appSettings")
    def app_settings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "appSettings"))

    @app_settings.setter
    def app_settings(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f854dbe2cecc8df66aada8e20d13fdef7f45123bff8bfe5e80a2c2c2dbce3187)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettings", value)

    @builtins.property
    @jsii.member(jsii_name="builtinLoggingEnabled")
    def builtin_logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "builtinLoggingEnabled"))

    @builtin_logging_enabled.setter
    def builtin_logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58e6f66a41e5bc7988168c38f3ef7dc78123376351fa7e9d0e4b26ffcaf36ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtinLoggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabled")
    def client_certificate_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientCertificateEnabled"))

    @client_certificate_enabled.setter
    def client_certificate_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fd566dcac8bb05624de680ce22184f53fcda577bdf4a35b44ad8a27d53c1e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateExclusionPaths")
    def client_certificate_exclusion_paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateExclusionPaths"))

    @client_certificate_exclusion_paths.setter
    def client_certificate_exclusion_paths(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c29db7d4ef3ef3a54d197dd633dc36b115835affb85f45ec972503a4f8df8ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateExclusionPaths", value)

    @builtins.property
    @jsii.member(jsii_name="clientCertificateMode")
    def client_certificate_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateMode"))

    @client_certificate_mode.setter
    def client_certificate_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a070b8c0d59c2d86399e45fe5382ce9214baabf87c7e6f9f4c640bc395a36da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateMode", value)

    @builtins.property
    @jsii.member(jsii_name="contentShareForceDisabled")
    def content_share_force_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "contentShareForceDisabled"))

    @content_share_force_disabled.setter
    def content_share_force_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab19ebb98e9b4b4ce4162f2ce9fbcf60a3e0fdbe0aa9bac6b38e07c9f60589d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentShareForceDisabled", value)

    @builtins.property
    @jsii.member(jsii_name="dailyMemoryTimeQuota")
    def daily_memory_time_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dailyMemoryTimeQuota"))

    @daily_memory_time_quota.setter
    def daily_memory_time_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0f8cc51248ecfd8f70718666ed8cf7eba31961d322ed6cf5f2d36c81337027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dailyMemoryTimeQuota", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677bf3ad271b60a8e970b8d3d62f2f3eb9c05dc75f8449cbdb852ee4770b1599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="functionAppId")
    def function_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionAppId"))

    @function_app_id.setter
    def function_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389e6483d524c51282157954b8e5365ef3031cdfa2ecf25750fc6e45a1090ab5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionAppId", value)

    @builtins.property
    @jsii.member(jsii_name="functionsExtensionVersion")
    def functions_extension_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionsExtensionVersion"))

    @functions_extension_version.setter
    def functions_extension_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89e634c8f07bcea3e1f64f65fbd4854a7c13e1132621515e6d66715f06b3958e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionsExtensionVersion", value)

    @builtins.property
    @jsii.member(jsii_name="httpsOnly")
    def https_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsOnly"))

    @https_only.setter
    def https_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd29b2b908d5eb7d3279b1372537333a24df08600de6c5ee8ce8ebefdf429fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsOnly", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef358c0055f92afe6fcd0680bb3b7d05e8bf145121e6814bd22c4b318a99181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="keyVaultReferenceIdentityId")
    def key_vault_reference_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultReferenceIdentityId"))

    @key_vault_reference_identity_id.setter
    def key_vault_reference_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108bdb79c2546c2a4f4facc86d28ad167f311acd9cd80654e107980d49af39ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultReferenceIdentityId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dda8f7e55ddf80db84c6446e4af7f187aa65db9d2a937fefdb6442d0b30af70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b7564c84940913bf0557dc56ffc2b8b20b0b695f1c063b2743f6380d71dfe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @storage_account_name.setter
    def storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96453ba9d746419dca32d5142c5e89e7b67ec14e9e52fc02183f31f69bf7479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountName", value)

    @builtins.property
    @jsii.member(jsii_name="storageKeyVaultSecretId")
    def storage_key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKeyVaultSecretId"))

    @storage_key_vault_secret_id.setter
    def storage_key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737652d9db0d93efb1da43fd78f11f761150c3b38de91b25a492e984671c6167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageKeyVaultSecretId", value)

    @builtins.property
    @jsii.member(jsii_name="storageUsesManagedIdentity")
    def storage_uses_managed_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storageUsesManagedIdentity"))

    @storage_uses_managed_identity.setter
    def storage_uses_managed_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe55ebff934998326b8416f416e8eef1cbf25354a0c5732be4382e0e31b2ce9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUsesManagedIdentity", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1146c17414cf4287553a531077615d321cfe1a2e16564034e0735c227e0cf630)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ca53f69280a26f28633a2fd381f898f590d304e2aeccbdbb7b14674f1ee748f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "active_directory": "activeDirectory",
        "additional_login_parameters": "additionalLoginParameters",
        "allowed_external_redirect_urls": "allowedExternalRedirectUrls",
        "default_provider": "defaultProvider",
        "facebook": "facebook",
        "github": "github",
        "google": "google",
        "issuer": "issuer",
        "microsoft": "microsoft",
        "runtime_version": "runtimeVersion",
        "token_refresh_extension_hours": "tokenRefreshExtensionHours",
        "token_store_enabled": "tokenStoreEnabled",
        "twitter": "twitter",
        "unauthenticated_client_action": "unauthenticatedClientAction",
    },
)
class WindowsFunctionAppSlotAuthSettings:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_directory: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsFacebook", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsGoogle", typing.Dict[builtins.str, typing.Any]]] = None,
        issuer: typing.Optional[builtins.str] = None,
        microsoft: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsMicrosoft", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter: typing.Optional[typing.Union["WindowsFunctionAppSlotAuthSettingsTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_client_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Should the Authentication / Authorization feature be enabled? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#active_directory WindowsFunctionAppSlot#active_directory}
        :param additional_login_parameters: Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#additional_login_parameters WindowsFunctionAppSlot#additional_login_parameters}
        :param allowed_external_redirect_urls: Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_external_redirect_urls WindowsFunctionAppSlot#allowed_external_redirect_urls}
        :param default_provider: The default authentication provider to use when multiple providers are configured. Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#default_provider WindowsFunctionAppSlot#default_provider}
        :param facebook: facebook block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#facebook WindowsFunctionAppSlot#facebook}
        :param github: github block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#github WindowsFunctionAppSlot#github}
        :param google: google block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#google WindowsFunctionAppSlot#google}
        :param issuer: The OpenID Connect Issuer URI that represents the entity which issues access tokens. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#issuer WindowsFunctionAppSlot#issuer}
        :param microsoft: microsoft block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#microsoft WindowsFunctionAppSlot#microsoft}
        :param runtime_version: The RuntimeVersion of the Authentication / Authorization feature in use. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#runtime_version WindowsFunctionAppSlot#runtime_version}
        :param token_refresh_extension_hours: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#token_refresh_extension_hours WindowsFunctionAppSlot#token_refresh_extension_hours}
        :param token_store_enabled: Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#token_store_enabled WindowsFunctionAppSlot#token_store_enabled}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#twitter WindowsFunctionAppSlot#twitter}
        :param unauthenticated_client_action: The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#unauthenticated_client_action WindowsFunctionAppSlot#unauthenticated_client_action}
        '''
        if isinstance(active_directory, dict):
            active_directory = WindowsFunctionAppSlotAuthSettingsActiveDirectory(**active_directory)
        if isinstance(facebook, dict):
            facebook = WindowsFunctionAppSlotAuthSettingsFacebook(**facebook)
        if isinstance(github, dict):
            github = WindowsFunctionAppSlotAuthSettingsGithub(**github)
        if isinstance(google, dict):
            google = WindowsFunctionAppSlotAuthSettingsGoogle(**google)
        if isinstance(microsoft, dict):
            microsoft = WindowsFunctionAppSlotAuthSettingsMicrosoft(**microsoft)
        if isinstance(twitter, dict):
            twitter = WindowsFunctionAppSlotAuthSettingsTwitter(**twitter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d196f4eace4fb0169d2aed9df231ee5764d30153e2954127a15ca35b596d451)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument active_directory", value=active_directory, expected_type=type_hints["active_directory"])
            check_type(argname="argument additional_login_parameters", value=additional_login_parameters, expected_type=type_hints["additional_login_parameters"])
            check_type(argname="argument allowed_external_redirect_urls", value=allowed_external_redirect_urls, expected_type=type_hints["allowed_external_redirect_urls"])
            check_type(argname="argument default_provider", value=default_provider, expected_type=type_hints["default_provider"])
            check_type(argname="argument facebook", value=facebook, expected_type=type_hints["facebook"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument google", value=google, expected_type=type_hints["google"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument microsoft", value=microsoft, expected_type=type_hints["microsoft"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument token_refresh_extension_hours", value=token_refresh_extension_hours, expected_type=type_hints["token_refresh_extension_hours"])
            check_type(argname="argument token_store_enabled", value=token_store_enabled, expected_type=type_hints["token_store_enabled"])
            check_type(argname="argument twitter", value=twitter, expected_type=type_hints["twitter"])
            check_type(argname="argument unauthenticated_client_action", value=unauthenticated_client_action, expected_type=type_hints["unauthenticated_client_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if active_directory is not None:
            self._values["active_directory"] = active_directory
        if additional_login_parameters is not None:
            self._values["additional_login_parameters"] = additional_login_parameters
        if allowed_external_redirect_urls is not None:
            self._values["allowed_external_redirect_urls"] = allowed_external_redirect_urls
        if default_provider is not None:
            self._values["default_provider"] = default_provider
        if facebook is not None:
            self._values["facebook"] = facebook
        if github is not None:
            self._values["github"] = github
        if google is not None:
            self._values["google"] = google
        if issuer is not None:
            self._values["issuer"] = issuer
        if microsoft is not None:
            self._values["microsoft"] = microsoft
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if token_refresh_extension_hours is not None:
            self._values["token_refresh_extension_hours"] = token_refresh_extension_hours
        if token_store_enabled is not None:
            self._values["token_store_enabled"] = token_store_enabled
        if twitter is not None:
            self._values["twitter"] = twitter
        if unauthenticated_client_action is not None:
            self._values["unauthenticated_client_action"] = unauthenticated_client_action

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Should the Authentication / Authorization feature be enabled?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def active_directory(
        self,
    ) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsActiveDirectory"]:
        '''active_directory block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#active_directory WindowsFunctionAppSlot#active_directory}
        '''
        result = self._values.get("active_directory")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsActiveDirectory"], result)

    @builtins.property
    def additional_login_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#additional_login_parameters WindowsFunctionAppSlot#additional_login_parameters}
        '''
        result = self._values.get("additional_login_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allowed_external_redirect_urls(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_external_redirect_urls WindowsFunctionAppSlot#allowed_external_redirect_urls}
        '''
        result = self._values.get("allowed_external_redirect_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_provider(self) -> typing.Optional[builtins.str]:
        '''The default authentication provider to use when multiple providers are configured.

        Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#default_provider WindowsFunctionAppSlot#default_provider}
        '''
        result = self._values.get("default_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def facebook(self) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsFacebook"]:
        '''facebook block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#facebook WindowsFunctionAppSlot#facebook}
        '''
        result = self._values.get("facebook")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsFacebook"], result)

    @builtins.property
    def github(self) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsGithub"]:
        '''github block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#github WindowsFunctionAppSlot#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsGithub"], result)

    @builtins.property
    def google(self) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsGoogle"]:
        '''google block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#google WindowsFunctionAppSlot#google}
        '''
        result = self._values.get("google")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsGoogle"], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''The OpenID Connect Issuer URI that represents the entity which issues access tokens.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#issuer WindowsFunctionAppSlot#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft(
        self,
    ) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsMicrosoft"]:
        '''microsoft block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#microsoft WindowsFunctionAppSlot#microsoft}
        '''
        result = self._values.get("microsoft")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsMicrosoft"], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The RuntimeVersion of the Authentication / Authorization feature in use.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#runtime_version WindowsFunctionAppSlot#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_refresh_extension_hours(self) -> typing.Optional[jsii.Number]:
        '''The number of hours after session token expiration that a session token can be used to call the token refresh API.

        Defaults to ``72`` hours.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#token_refresh_extension_hours WindowsFunctionAppSlot#token_refresh_extension_hours}
        '''
        result = self._values.get("token_refresh_extension_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token_store_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#token_store_enabled WindowsFunctionAppSlot#token_store_enabled}
        '''
        result = self._values.get("token_store_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def twitter(self) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsTwitter"]:
        '''twitter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#twitter WindowsFunctionAppSlot#twitter}
        '''
        result = self._values.get("twitter")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsTwitter"], result)

    @builtins.property
    def unauthenticated_client_action(self) -> typing.Optional[builtins.str]:
        '''The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#unauthenticated_client_action WindowsFunctionAppSlot#unauthenticated_client_action}
        '''
        result = self._values.get("unauthenticated_client_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "allowed_audiences": "allowedAudiences",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
    },
)
class WindowsFunctionAppSlotAuthSettingsActiveDirectory:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_audiences WindowsFunctionAppSlot#allowed_audiences}
        :param client_secret: The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c35a6582acee564757ab4ab195600c41ec98dfa27e90100d2788c131df1ec6)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the Client to use to authenticate with Azure Active Directory.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_audiences WindowsFunctionAppSlot#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettingsActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotAuthSettingsActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsActiveDirectoryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50f68c644dc88554864f85c8de4b04f2573c6e2014c82bb0356f9b2e1998e294)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acf79334f259c71f316b28146387e824fe33421aead50813ac2416019a5324f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2794684db621eed7c38d0f91bfda808b86bfc883eab221d95852bef6b20f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b929851d2617e8e2f39bcc9b3fe79afe19441bcb1aba0b05c3e4f313820c4476)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2d2660fec4907beca9d4c3158a818fef96fd083fc20b23347773be33feaf0cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettingsActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b39b2664238fa2eeca906fefc6acff6c59db5f6a2bc51fccab3493d42533a225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsFacebook",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_secret": "appSecret",
        "app_secret_setting_name": "appSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class WindowsFunctionAppSlotAuthSettingsFacebook:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        app_secret: typing.Optional[builtins.str] = None,
        app_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_id WindowsFunctionAppSlot#app_id}
        :param app_secret: The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_secret WindowsFunctionAppSlot#app_secret}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_secret_setting_name WindowsFunctionAppSlot#app_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1289900f438ffb9e66104647a3de8e3520c44766c1b4ffba9ecaca8f84140d9c)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_secret", value=app_secret, expected_type=type_hints["app_secret"])
            check_type(argname="argument app_secret_setting_name", value=app_secret_setting_name, expected_type=type_hints["app_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
        }
        if app_secret is not None:
            self._values["app_secret"] = app_secret
        if app_secret_setting_name is not None:
            self._values["app_secret_setting_name"] = app_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The App ID of the Facebook app used for login.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_id WindowsFunctionAppSlot#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_secret(self) -> typing.Optional[builtins.str]:
        '''The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_secret WindowsFunctionAppSlot#app_secret}
        '''
        result = self._values.get("app_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_secret_setting_name WindowsFunctionAppSlot#app_secret_setting_name}
        '''
        result = self._values.get("app_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettingsFacebook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotAuthSettingsFacebookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsFacebookOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81515c1b2694ebfbfab74b1bb7cc05320a59bc0ac6ad278d6dea107d85e7d2d0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppSecret")
    def reset_app_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSecret", []))

    @jsii.member(jsii_name="resetAppSecretSettingName")
    def reset_app_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appSecretInput")
    def app_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingNameInput")
    def app_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753e5e3d4f961b5855588841d9dd3bffa1087f0af9ccbdcc409ed50c2e34bf7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="appSecret")
    def app_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecret"))

    @app_secret.setter
    def app_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e3faebfa16731ed7930258d9fd39cc6014f68422ebbba87b333debcf0d37f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecret", value)

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingName")
    def app_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecretSettingName"))

    @app_secret_setting_name.setter
    def app_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15284ffa48ed6677fb25f9f76683f793d2e618b5e18240343e8d20e3547ee34a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecretSettingName", value)

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7913ddd7aabe10e1b51c5828828af1b6775961036a7caf99fd07ba51035278b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsFacebook]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsFacebook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettingsFacebook],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa670fc95d68b3aad0e729d7b97a79144af6e6c1fe1ae697a36f6d0d4988f3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsGithub",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class WindowsFunctionAppSlotAuthSettingsGithub:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param client_secret: The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21ca89ddab634ab02ea5bdb73b08a3859463cdad330adc46dee1ec6ec4d90809)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the GitHub app used for login.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettingsGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotAuthSettingsGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsGithubOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978725dc060f643c22bef640bf5961d106885b7bf8a50578230cc99200aa223c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8309542369ad0da7562100c766c52c701ba3cdacaf78487b5cfd6c7ed15018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272160f17090f860efac27f2f0997ad9d1b4ad08c7d3d2287b9d9dc97b249b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551f312005bdfb243d5d5b5bcb19e6f497e4007ce12b984833fdf5bd67034f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value)

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd4d765c91ecb3c8993777a14cdcbae61cbb2085e62293a61e84329785a54970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsGithub]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsGithub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettingsGithub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f06a479533af78e8e6e331ab3779ea60d36344cc349541eec5a9b13c041707)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsGoogle",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class WindowsFunctionAppSlotAuthSettingsGoogle:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param client_secret: The client secret associated with the Google web application. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363e749442e06f52ceb1e3cf6fdfe633dd2d012a558e4798896836ab0bfe3e2e)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OpenID Connect Client ID for the Google web application.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client secret associated with the Google web application.  Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettingsGoogle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotAuthSettingsGoogleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsGoogleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76715d1d8b28499c0478d4e86a7967da82e0a8b602f8d39b1e261ca9bcfa388f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4555adfb4223f5bbcadabfa35311c32b5a306d2c7ba5c3bb0b2972da5514d046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b516ade7d7e9bad6d5c104f3e539e6dabb4540cc3d1375f35816c9ca773f5226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44fc907e3abad123a456069700bd3db0da2c1d7882871a0c5c9c6df5f6b50627)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value)

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87e18fa08ce6647bb64a122be805465c74e5e8f54ed969ecbc4bff39c1598f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsGoogle]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsGoogle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettingsGoogle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81cccd1ec4541f4ad5990550f27454e4c4f5a6113cc82cbad115371ad92efb33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsMicrosoft",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class WindowsFunctionAppSlotAuthSettingsMicrosoft:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param client_secret: The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d57bae65544d28bc2d5573c0cdb642fbded0c2645db249e511b21da679e5c52)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OAuth 2.0 client ID that was created for the app used for authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettingsMicrosoft(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotAuthSettingsMicrosoftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsMicrosoftOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914b3ab78a6839b31456557b3d4e680e7782ae19a59b56f000a9e1f854d0b8a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be627bb2ecaab104b4b2ffb14f987b5b6dbb9b2aa63adb317b9317bb40c0a97d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55da5db050c65fbdfe2f5caeb25a6dcb284d9124b25ba08891565bcb1808510f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9155d3915a6c06aa3ee1125075f1d33dba7fc7ba9db92a5a9085709210aa84e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value)

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57b5b3a534638dbc2934bb29d88cd2e227921595ad9655e10977f6091d60ea7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsMicrosoft], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettingsMicrosoft],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702647eef51388977447a1917db6fee4149d978a33227313e4a2d9bce4c81426)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotAuthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ce541b6cf8b403c4bdca320a5774ddef224efa653419142f6f67d7eee746cf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectory")
    def put_active_directory(
        self,
        *,
        client_id: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_audiences WindowsFunctionAppSlot#allowed_audiences}
        :param client_secret: The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        '''
        value = WindowsFunctionAppSlotAuthSettingsActiveDirectory(
            client_id=client_id,
            allowed_audiences=allowed_audiences,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDirectory", [value]))

    @jsii.member(jsii_name="putFacebook")
    def put_facebook(
        self,
        *,
        app_id: builtins.str,
        app_secret: typing.Optional[builtins.str] = None,
        app_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_id WindowsFunctionAppSlot#app_id}
        :param app_secret: The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_secret WindowsFunctionAppSlot#app_secret}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_secret_setting_name WindowsFunctionAppSlot#app_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        value = WindowsFunctionAppSlotAuthSettingsFacebook(
            app_id=app_id,
            app_secret=app_secret,
            app_secret_setting_name=app_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putFacebook", [value]))

    @jsii.member(jsii_name="putGithub")
    def put_github(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param client_secret: The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        value = WindowsFunctionAppSlotAuthSettingsGithub(
            client_id=client_id,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putGithub", [value]))

    @jsii.member(jsii_name="putGoogle")
    def put_google(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param client_secret: The client secret associated with the Google web application. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        value = WindowsFunctionAppSlotAuthSettingsGoogle(
            client_id=client_id,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putGoogle", [value]))

    @jsii.member(jsii_name="putMicrosoft")
    def put_microsoft(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_id WindowsFunctionAppSlot#client_id}
        :param client_secret: The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret WindowsFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_secret_setting_name WindowsFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#oauth_scopes WindowsFunctionAppSlot#oauth_scopes}
        '''
        value = WindowsFunctionAppSlotAuthSettingsMicrosoft(
            client_id=client_id,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putMicrosoft", [value]))

    @jsii.member(jsii_name="putTwitter")
    def put_twitter(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret: typing.Optional[builtins.str] = None,
        consumer_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_key WindowsFunctionAppSlot#consumer_key}
        :param consumer_secret: The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_secret WindowsFunctionAppSlot#consumer_secret}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_secret_setting_name WindowsFunctionAppSlot#consumer_secret_setting_name}
        '''
        value = WindowsFunctionAppSlotAuthSettingsTwitter(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            consumer_secret_setting_name=consumer_secret_setting_name,
        )

        return typing.cast(None, jsii.invoke(self, "putTwitter", [value]))

    @jsii.member(jsii_name="resetActiveDirectory")
    def reset_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectory", []))

    @jsii.member(jsii_name="resetAdditionalLoginParameters")
    def reset_additional_login_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalLoginParameters", []))

    @jsii.member(jsii_name="resetAllowedExternalRedirectUrls")
    def reset_allowed_external_redirect_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExternalRedirectUrls", []))

    @jsii.member(jsii_name="resetDefaultProvider")
    def reset_default_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultProvider", []))

    @jsii.member(jsii_name="resetFacebook")
    def reset_facebook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFacebook", []))

    @jsii.member(jsii_name="resetGithub")
    def reset_github(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithub", []))

    @jsii.member(jsii_name="resetGoogle")
    def reset_google(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogle", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetMicrosoft")
    def reset_microsoft(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoft", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @jsii.member(jsii_name="resetTokenRefreshExtensionHours")
    def reset_token_refresh_extension_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenRefreshExtensionHours", []))

    @jsii.member(jsii_name="resetTokenStoreEnabled")
    def reset_token_store_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenStoreEnabled", []))

    @jsii.member(jsii_name="resetTwitter")
    def reset_twitter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwitter", []))

    @jsii.member(jsii_name="resetUnauthenticatedClientAction")
    def reset_unauthenticated_client_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnauthenticatedClientAction", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(
        self,
    ) -> WindowsFunctionAppSlotAuthSettingsActiveDirectoryOutputReference:
        return typing.cast(WindowsFunctionAppSlotAuthSettingsActiveDirectoryOutputReference, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="facebook")
    def facebook(self) -> WindowsFunctionAppSlotAuthSettingsFacebookOutputReference:
        return typing.cast(WindowsFunctionAppSlotAuthSettingsFacebookOutputReference, jsii.get(self, "facebook"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> WindowsFunctionAppSlotAuthSettingsGithubOutputReference:
        return typing.cast(WindowsFunctionAppSlotAuthSettingsGithubOutputReference, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="google")
    def google(self) -> WindowsFunctionAppSlotAuthSettingsGoogleOutputReference:
        return typing.cast(WindowsFunctionAppSlotAuthSettingsGoogleOutputReference, jsii.get(self, "google"))

    @builtins.property
    @jsii.member(jsii_name="microsoft")
    def microsoft(self) -> WindowsFunctionAppSlotAuthSettingsMicrosoftOutputReference:
        return typing.cast(WindowsFunctionAppSlotAuthSettingsMicrosoftOutputReference, jsii.get(self, "microsoft"))

    @builtins.property
    @jsii.member(jsii_name="twitter")
    def twitter(self) -> "WindowsFunctionAppSlotAuthSettingsTwitterOutputReference":
        return typing.cast("WindowsFunctionAppSlotAuthSettingsTwitterOutputReference", jsii.get(self, "twitter"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryInput")
    def active_directory_input(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsActiveDirectory], jsii.get(self, "activeDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalLoginParametersInput")
    def additional_login_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalLoginParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrlsInput")
    def allowed_external_redirect_urls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedExternalRedirectUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultProviderInput")
    def default_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="facebookInput")
    def facebook_input(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsFacebook]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsFacebook], jsii.get(self, "facebookInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(self) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsGithub]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsGithub], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="googleInput")
    def google_input(self) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsGoogle]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsGoogle], jsii.get(self, "googleInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftInput")
    def microsoft_input(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsMicrosoft], jsii.get(self, "microsoftInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionHoursInput")
    def token_refresh_extension_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tokenRefreshExtensionHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabledInput")
    def token_store_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tokenStoreEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="twitterInput")
    def twitter_input(
        self,
    ) -> typing.Optional["WindowsFunctionAppSlotAuthSettingsTwitter"]:
        return typing.cast(typing.Optional["WindowsFunctionAppSlotAuthSettingsTwitter"], jsii.get(self, "twitterInput"))

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedClientActionInput")
    def unauthenticated_client_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unauthenticatedClientActionInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalLoginParameters")
    def additional_login_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalLoginParameters"))

    @additional_login_parameters.setter
    def additional_login_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db1de5a520ec484a59c3ef47e8ff1c0ad1b7dc14a4635b69402bdc1e1af39306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalLoginParameters", value)

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrls")
    def allowed_external_redirect_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedExternalRedirectUrls"))

    @allowed_external_redirect_urls.setter
    def allowed_external_redirect_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b350d88fb88083c8697f92dff60eb331adcb83bb1e1fcb79f9a10072883672de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExternalRedirectUrls", value)

    @builtins.property
    @jsii.member(jsii_name="defaultProvider")
    def default_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProvider"))

    @default_provider.setter
    def default_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7e4c5fe35c6e26cfea0af0700cab13a9af2e5797b3b94368fd5d33fda0eb48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProvider", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc9ea0f797d88418f48e9e850f009a9cd9864e8e91d93376e21351289193584)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__159f1b06a5d3b88c619f019a23834aad5af99d928b7649962aca8eb39613b6ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value)

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1191ea77b8bd1a7717b2b50c39c4cf3d3f7b076844dedef67474fd1971354b76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value)

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionHours")
    def token_refresh_extension_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tokenRefreshExtensionHours"))

    @token_refresh_extension_hours.setter
    def token_refresh_extension_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__146cd834d38edecec0144b447cdd767979c712296bcaff21a11bdfd28d95d52d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenRefreshExtensionHours", value)

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabled")
    def token_store_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tokenStoreEnabled"))

    @token_store_enabled.setter
    def token_store_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fab2b993a87c411a96be333cc3a032f15fdebb65b5d7dab2f20b4cd4766a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStoreEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedClientAction")
    def unauthenticated_client_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unauthenticatedClientAction"))

    @unauthenticated_client_action.setter
    def unauthenticated_client_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b65a79f1cf8269443bac55c360aae81b720722a1ca3af57b3e7d808e7a3c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unauthenticatedClientAction", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotAuthSettings]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4189fcc10d053ac78659348e173871154f92d1e3749a7c20471de162911fb65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsTwitter",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_key": "consumerKey",
        "consumer_secret": "consumerSecret",
        "consumer_secret_setting_name": "consumerSecretSettingName",
    },
)
class WindowsFunctionAppSlotAuthSettingsTwitter:
    def __init__(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret: typing.Optional[builtins.str] = None,
        consumer_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_key WindowsFunctionAppSlot#consumer_key}
        :param consumer_secret: The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_secret WindowsFunctionAppSlot#consumer_secret}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_secret_setting_name WindowsFunctionAppSlot#consumer_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50fbeae3362683d6e08725689a29c4aa85142d5ec2cb8160e086a0362f79070)
            check_type(argname="argument consumer_key", value=consumer_key, expected_type=type_hints["consumer_key"])
            check_type(argname="argument consumer_secret", value=consumer_secret, expected_type=type_hints["consumer_secret"])
            check_type(argname="argument consumer_secret_setting_name", value=consumer_secret_setting_name, expected_type=type_hints["consumer_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_key": consumer_key,
        }
        if consumer_secret is not None:
            self._values["consumer_secret"] = consumer_secret
        if consumer_secret_setting_name is not None:
            self._values["consumer_secret_setting_name"] = consumer_secret_setting_name

    @builtins.property
    def consumer_key(self) -> builtins.str:
        '''The OAuth 1.0a consumer key of the Twitter application used for sign-in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_key WindowsFunctionAppSlot#consumer_key}
        '''
        result = self._values.get("consumer_key")
        assert result is not None, "Required property 'consumer_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_secret WindowsFunctionAppSlot#consumer_secret}
        '''
        result = self._values.get("consumer_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#consumer_secret_setting_name WindowsFunctionAppSlot#consumer_secret_setting_name}
        '''
        result = self._values.get("consumer_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotAuthSettingsTwitter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotAuthSettingsTwitterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotAuthSettingsTwitterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264402ff1e1f375f4e245c7ba8b7729433582081c19fa29cdd6904b0ca15c1fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConsumerSecret")
    def reset_consumer_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerSecret", []))

    @jsii.member(jsii_name="resetConsumerSecretSettingName")
    def reset_consumer_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerSecretSettingName", []))

    @builtins.property
    @jsii.member(jsii_name="consumerKeyInput")
    def consumer_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecretInput")
    def consumer_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingNameInput")
    def consumer_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerKey")
    def consumer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerKey"))

    @consumer_key.setter
    def consumer_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f2155f214bb3b5fa2a13bc40ac7c4d5d80c63ada149a0e7b2a0576dc1769ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerKey", value)

    @builtins.property
    @jsii.member(jsii_name="consumerSecret")
    def consumer_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecret"))

    @consumer_secret.setter
    def consumer_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468b9b4afb4a26d451b8dab70161a54ad37eb297ccc1f7eb3e325df175a94d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecret", value)

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingName")
    def consumer_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecretSettingName"))

    @consumer_secret_setting_name.setter
    def consumer_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e1f6c6b599d098506cee2c2b322ead4ce73a592cd237c6cbb9e8bb13534890d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecretSettingName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotAuthSettingsTwitter]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettingsTwitter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotAuthSettingsTwitter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1378096ffbe28e92927bf7fff55c1202b0e132f8674502228d3e1deda1ba0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotBackup",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "schedule": "schedule",
        "storage_account_url": "storageAccountUrl",
        "enabled": "enabled",
    },
)
class WindowsFunctionAppSlotBackup:
    def __init__(
        self,
        *,
        name: builtins.str,
        schedule: typing.Union["WindowsFunctionAppSlotBackupSchedule", typing.Dict[builtins.str, typing.Any]],
        storage_account_url: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name which should be used for this Backup. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#schedule WindowsFunctionAppSlot#schedule}
        :param storage_account_url: The SAS URL to the container. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_url WindowsFunctionAppSlot#storage_account_url}
        :param enabled: Should this backup job be enabled? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        '''
        if isinstance(schedule, dict):
            schedule = WindowsFunctionAppSlotBackupSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__613e64716bd39fc025d50ffed1483b8eff0d3a8ceb2159c82e825351159ec45a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument storage_account_url", value=storage_account_url, expected_type=type_hints["storage_account_url"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "schedule": schedule,
            "storage_account_url": storage_account_url,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def name(self) -> builtins.str:
        '''The name which should be used for this Backup.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> "WindowsFunctionAppSlotBackupSchedule":
        '''schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#schedule WindowsFunctionAppSlot#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("WindowsFunctionAppSlotBackupSchedule", result)

    @builtins.property
    def storage_account_url(self) -> builtins.str:
        '''The SAS URL to the container.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_url WindowsFunctionAppSlot#storage_account_url}
        '''
        result = self._values.get("storage_account_url")
        assert result is not None, "Required property 'storage_account_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should this backup job be enabled?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotBackupOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fc1bbd8a0cd9d42d7caa4c3872006fc90ba8d97aea01e4843b9e75730a86db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        frequency_interval: jsii.Number,
        frequency_unit: builtins.str,
        keep_at_least_one_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency_interval: How often the backup should be executed (e.g. for weekly backup, this should be set to ``7`` and ``frequency_unit`` should be set to ``Day``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#frequency_interval WindowsFunctionAppSlot#frequency_interval}
        :param frequency_unit: The unit of time for how often the backup should take place. Possible values include: ``Day`` and ``Hour``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#frequency_unit WindowsFunctionAppSlot#frequency_unit}
        :param keep_at_least_one_backup: Should the service keep at least one backup, regardless of age of backup. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#keep_at_least_one_backup WindowsFunctionAppSlot#keep_at_least_one_backup}
        :param retention_period_days: After how many days backups should be deleted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#retention_period_days WindowsFunctionAppSlot#retention_period_days}
        :param start_time: When the schedule should start working in RFC-3339 format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#start_time WindowsFunctionAppSlot#start_time}
        '''
        value = WindowsFunctionAppSlotBackupSchedule(
            frequency_interval=frequency_interval,
            frequency_unit=frequency_unit,
            keep_at_least_one_backup=keep_at_least_one_backup,
            retention_period_days=retention_period_days,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "WindowsFunctionAppSlotBackupScheduleOutputReference":
        return typing.cast("WindowsFunctionAppSlotBackupScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["WindowsFunctionAppSlotBackupSchedule"]:
        return typing.cast(typing.Optional["WindowsFunctionAppSlotBackupSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrlInput")
    def storage_account_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2bf4acf9e410db373be974a8ec2dfd15269536f54d34b42daac6a5a075e1049)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd3bda734e67818c282bd38ce1fb34350c59f2ec780e134fd46f20142342f15b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrl")
    def storage_account_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountUrl"))

    @storage_account_url.setter
    def storage_account_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e24e2c402232835f5eeca96adc73180387a1e95fdf21ba3bd0e40654059a5ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotBackup]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47ecb73cf0bdd7ed3b3f8905466bcbab1e1d542dff2f43a335b30e29e5ee84dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotBackupSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "frequency_unit": "frequencyUnit",
        "keep_at_least_one_backup": "keepAtLeastOneBackup",
        "retention_period_days": "retentionPeriodDays",
        "start_time": "startTime",
    },
)
class WindowsFunctionAppSlotBackupSchedule:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        frequency_unit: builtins.str,
        keep_at_least_one_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency_interval: How often the backup should be executed (e.g. for weekly backup, this should be set to ``7`` and ``frequency_unit`` should be set to ``Day``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#frequency_interval WindowsFunctionAppSlot#frequency_interval}
        :param frequency_unit: The unit of time for how often the backup should take place. Possible values include: ``Day`` and ``Hour``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#frequency_unit WindowsFunctionAppSlot#frequency_unit}
        :param keep_at_least_one_backup: Should the service keep at least one backup, regardless of age of backup. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#keep_at_least_one_backup WindowsFunctionAppSlot#keep_at_least_one_backup}
        :param retention_period_days: After how many days backups should be deleted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#retention_period_days WindowsFunctionAppSlot#retention_period_days}
        :param start_time: When the schedule should start working in RFC-3339 format. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#start_time WindowsFunctionAppSlot#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c309ca6725e641c7440b943e814df02ef87d04bce4f3d108221e359ad360e24c)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument frequency_unit", value=frequency_unit, expected_type=type_hints["frequency_unit"])
            check_type(argname="argument keep_at_least_one_backup", value=keep_at_least_one_backup, expected_type=type_hints["keep_at_least_one_backup"])
            check_type(argname="argument retention_period_days", value=retention_period_days, expected_type=type_hints["retention_period_days"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "frequency_unit": frequency_unit,
        }
        if keep_at_least_one_backup is not None:
            self._values["keep_at_least_one_backup"] = keep_at_least_one_backup
        if retention_period_days is not None:
            self._values["retention_period_days"] = retention_period_days
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''How often the backup should be executed (e.g. for weekly backup, this should be set to ``7`` and ``frequency_unit`` should be set to ``Day``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#frequency_interval WindowsFunctionAppSlot#frequency_interval}
        '''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frequency_unit(self) -> builtins.str:
        '''The unit of time for how often the backup should take place. Possible values include: ``Day`` and ``Hour``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#frequency_unit WindowsFunctionAppSlot#frequency_unit}
        '''
        result = self._values.get("frequency_unit")
        assert result is not None, "Required property 'frequency_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_at_least_one_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the service keep at least one backup, regardless of age of backup. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#keep_at_least_one_backup WindowsFunctionAppSlot#keep_at_least_one_backup}
        '''
        result = self._values.get("keep_at_least_one_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_period_days(self) -> typing.Optional[jsii.Number]:
        '''After how many days backups should be deleted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#retention_period_days WindowsFunctionAppSlot#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''When the schedule should start working in RFC-3339 format.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#start_time WindowsFunctionAppSlot#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotBackupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotBackupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotBackupScheduleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beafb38377d60d6136acd04d852aa35b077953dd5f6a9347b982501608f7d542)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepAtLeastOneBackup")
    def reset_keep_at_least_one_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAtLeastOneBackup", []))

    @jsii.member(jsii_name="resetRetentionPeriodDays")
    def reset_retention_period_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriodDays", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="lastExecutionTime")
    def last_execution_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastExecutionTime"))

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyUnitInput")
    def frequency_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAtLeastOneBackupInput")
    def keep_at_least_one_backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepAtLeastOneBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDaysInput")
    def retention_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad56e2f14ff74c90e0959dd64ce13da9b2c132d73c7c2d4a638c71c5b6940d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value)

    @builtins.property
    @jsii.member(jsii_name="frequencyUnit")
    def frequency_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyUnit"))

    @frequency_unit.setter
    def frequency_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45542d7deed8d87eaddf4b6c0cf0d79d3ec6afc4633b16ea2a16f67b4806b3de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyUnit", value)

    @builtins.property
    @jsii.member(jsii_name="keepAtLeastOneBackup")
    def keep_at_least_one_backup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepAtLeastOneBackup"))

    @keep_at_least_one_backup.setter
    def keep_at_least_one_backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ca699b5abec4bfa4f9e380fd1f3a2bbeb84cb028dcdbb4b0523edccbf4a8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAtLeastOneBackup", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7981f54cabe9961a1437b31673df4eca2585d5b8f7bcb557cfb2441a0225b2b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90cb57b0e818595209fd5f8b2b2bcf48b7e73dd95b01277021d28ba293ee975)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotBackupSchedule]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotBackupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotBackupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aff899b0bc0b846b36a10574aff357c1479ec05f0206357bf00f2f01c08099d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_app_id": "functionAppId",
        "name": "name",
        "site_config": "siteConfig",
        "app_settings": "appSettings",
        "auth_settings": "authSettings",
        "backup": "backup",
        "builtin_logging_enabled": "builtinLoggingEnabled",
        "client_certificate_enabled": "clientCertificateEnabled",
        "client_certificate_exclusion_paths": "clientCertificateExclusionPaths",
        "client_certificate_mode": "clientCertificateMode",
        "connection_string": "connectionString",
        "content_share_force_disabled": "contentShareForceDisabled",
        "daily_memory_time_quota": "dailyMemoryTimeQuota",
        "enabled": "enabled",
        "functions_extension_version": "functionsExtensionVersion",
        "https_only": "httpsOnly",
        "id": "id",
        "identity": "identity",
        "key_vault_reference_identity_id": "keyVaultReferenceIdentityId",
        "storage_account": "storageAccount",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_account_name": "storageAccountName",
        "storage_key_vault_secret_id": "storageKeyVaultSecretId",
        "storage_uses_managed_identity": "storageUsesManagedIdentity",
        "tags": "tags",
        "timeouts": "timeouts",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
    },
)
class WindowsFunctionAppSlotConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        function_app_id: builtins.str,
        name: builtins.str,
        site_config: typing.Union["WindowsFunctionAppSlotSiteConfig", typing.Dict[builtins.str, typing.Any]],
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        backup: typing.Optional[typing.Union[WindowsFunctionAppSlotBackup, typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotConnectionString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        daily_memory_time_quota: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        functions_extension_version: typing.Optional[builtins.str] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["WindowsFunctionAppSlotIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
        storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
        storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["WindowsFunctionAppSlotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_app_id: The ID of the Windows Function App this Slot is a member of. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#function_app_id WindowsFunctionAppSlot#function_app_id}
        :param name: Specifies the name of the Windows Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        :param site_config: site_config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#site_config WindowsFunctionAppSlot#site_config}
        :param app_settings: A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_settings WindowsFunctionAppSlot#app_settings}
        :param auth_settings: auth_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#auth_settings WindowsFunctionAppSlot#auth_settings}
        :param backup: backup block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#backup WindowsFunctionAppSlot#backup}
        :param builtin_logging_enabled: Should built in logging be enabled. Configures ``AzureWebJobsDashboard`` app setting based on the configured storage setting. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#builtin_logging_enabled WindowsFunctionAppSlot#builtin_logging_enabled}
        :param client_certificate_enabled: Should the Function App Slot use Client Certificates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_enabled WindowsFunctionAppSlot#client_certificate_enabled}
        :param client_certificate_exclusion_paths: Paths to exclude when using client certificates, separated by ; Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_exclusion_paths WindowsFunctionAppSlot#client_certificate_exclusion_paths}
        :param client_certificate_mode: The mode of the Function App Slot's client certificates requirement for incoming requests. Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_mode WindowsFunctionAppSlot#client_certificate_mode}
        :param connection_string: connection_string block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#connection_string WindowsFunctionAppSlot#connection_string}
        :param content_share_force_disabled: Force disable the content share settings. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#content_share_force_disabled WindowsFunctionAppSlot#content_share_force_disabled}
        :param daily_memory_time_quota: The amount of memory in gigabyte-seconds that your application is allowed to consume per day. Setting this value only affects function apps in Consumption Plans. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#daily_memory_time_quota WindowsFunctionAppSlot#daily_memory_time_quota}
        :param enabled: Is the Windows Function App Slot enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        :param functions_extension_version: The runtime version associated with the Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#functions_extension_version WindowsFunctionAppSlot#functions_extension_version}
        :param https_only: Can the Function App Slot only be accessed via HTTPS? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#https_only WindowsFunctionAppSlot#https_only}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#id WindowsFunctionAppSlot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#identity WindowsFunctionAppSlot#identity}
        :param key_vault_reference_identity_id: The User Assigned Identity to use for Key Vault access. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#key_vault_reference_identity_id WindowsFunctionAppSlot#key_vault_reference_identity_id}
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account WindowsFunctionAppSlot#storage_account}
        :param storage_account_access_key: The access key which will be used to access the storage account for the Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_access_key WindowsFunctionAppSlot#storage_account_access_key}
        :param storage_account_name: The backend storage account name which will be used by this Function App Slot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_name WindowsFunctionAppSlot#storage_account_name}
        :param storage_key_vault_secret_id: The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_key_vault_secret_id WindowsFunctionAppSlot#storage_key_vault_secret_id}
        :param storage_uses_managed_identity: Should the Function App Slot use its Managed Identity to access storage? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_uses_managed_identity WindowsFunctionAppSlot#storage_uses_managed_identity}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#tags WindowsFunctionAppSlot#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#timeouts WindowsFunctionAppSlot#timeouts}
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(site_config, dict):
            site_config = WindowsFunctionAppSlotSiteConfig(**site_config)
        if isinstance(auth_settings, dict):
            auth_settings = WindowsFunctionAppSlotAuthSettings(**auth_settings)
        if isinstance(backup, dict):
            backup = WindowsFunctionAppSlotBackup(**backup)
        if isinstance(identity, dict):
            identity = WindowsFunctionAppSlotIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = WindowsFunctionAppSlotTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87c5fa036e9ff6c5ef7178e14406dda061b080ad7da90cdbde0849b224fd9042)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_app_id", value=function_app_id, expected_type=type_hints["function_app_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument site_config", value=site_config, expected_type=type_hints["site_config"])
            check_type(argname="argument app_settings", value=app_settings, expected_type=type_hints["app_settings"])
            check_type(argname="argument auth_settings", value=auth_settings, expected_type=type_hints["auth_settings"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument builtin_logging_enabled", value=builtin_logging_enabled, expected_type=type_hints["builtin_logging_enabled"])
            check_type(argname="argument client_certificate_enabled", value=client_certificate_enabled, expected_type=type_hints["client_certificate_enabled"])
            check_type(argname="argument client_certificate_exclusion_paths", value=client_certificate_exclusion_paths, expected_type=type_hints["client_certificate_exclusion_paths"])
            check_type(argname="argument client_certificate_mode", value=client_certificate_mode, expected_type=type_hints["client_certificate_mode"])
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument content_share_force_disabled", value=content_share_force_disabled, expected_type=type_hints["content_share_force_disabled"])
            check_type(argname="argument daily_memory_time_quota", value=daily_memory_time_quota, expected_type=type_hints["daily_memory_time_quota"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument functions_extension_version", value=functions_extension_version, expected_type=type_hints["functions_extension_version"])
            check_type(argname="argument https_only", value=https_only, expected_type=type_hints["https_only"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument key_vault_reference_identity_id", value=key_vault_reference_identity_id, expected_type=type_hints["key_vault_reference_identity_id"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument storage_key_vault_secret_id", value=storage_key_vault_secret_id, expected_type=type_hints["storage_key_vault_secret_id"])
            check_type(argname="argument storage_uses_managed_identity", value=storage_uses_managed_identity, expected_type=type_hints["storage_uses_managed_identity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_app_id": function_app_id,
            "name": name,
            "site_config": site_config,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if app_settings is not None:
            self._values["app_settings"] = app_settings
        if auth_settings is not None:
            self._values["auth_settings"] = auth_settings
        if backup is not None:
            self._values["backup"] = backup
        if builtin_logging_enabled is not None:
            self._values["builtin_logging_enabled"] = builtin_logging_enabled
        if client_certificate_enabled is not None:
            self._values["client_certificate_enabled"] = client_certificate_enabled
        if client_certificate_exclusion_paths is not None:
            self._values["client_certificate_exclusion_paths"] = client_certificate_exclusion_paths
        if client_certificate_mode is not None:
            self._values["client_certificate_mode"] = client_certificate_mode
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if content_share_force_disabled is not None:
            self._values["content_share_force_disabled"] = content_share_force_disabled
        if daily_memory_time_quota is not None:
            self._values["daily_memory_time_quota"] = daily_memory_time_quota
        if enabled is not None:
            self._values["enabled"] = enabled
        if functions_extension_version is not None:
            self._values["functions_extension_version"] = functions_extension_version
        if https_only is not None:
            self._values["https_only"] = https_only
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if key_vault_reference_identity_id is not None:
            self._values["key_vault_reference_identity_id"] = key_vault_reference_identity_id
        if storage_account is not None:
            self._values["storage_account"] = storage_account
        if storage_account_access_key is not None:
            self._values["storage_account_access_key"] = storage_account_access_key
        if storage_account_name is not None:
            self._values["storage_account_name"] = storage_account_name
        if storage_key_vault_secret_id is not None:
            self._values["storage_key_vault_secret_id"] = storage_key_vault_secret_id
        if storage_uses_managed_identity is not None:
            self._values["storage_uses_managed_identity"] = storage_uses_managed_identity
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def function_app_id(self) -> builtins.str:
        '''The ID of the Windows Function App this Slot is a member of.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#function_app_id WindowsFunctionAppSlot#function_app_id}
        '''
        result = self._values.get("function_app_id")
        assert result is not None, "Required property 'function_app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the Windows Function App Slot.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_config(self) -> "WindowsFunctionAppSlotSiteConfig":
        '''site_config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#site_config WindowsFunctionAppSlot#site_config}
        '''
        result = self._values.get("site_config")
        assert result is not None, "Required property 'site_config' is missing"
        return typing.cast("WindowsFunctionAppSlotSiteConfig", result)

    @builtins.property
    def app_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_settings WindowsFunctionAppSlot#app_settings}
        '''
        result = self._values.get("app_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def auth_settings(self) -> typing.Optional[WindowsFunctionAppSlotAuthSettings]:
        '''auth_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#auth_settings WindowsFunctionAppSlot#auth_settings}
        '''
        result = self._values.get("auth_settings")
        return typing.cast(typing.Optional[WindowsFunctionAppSlotAuthSettings], result)

    @builtins.property
    def backup(self) -> typing.Optional[WindowsFunctionAppSlotBackup]:
        '''backup block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#backup WindowsFunctionAppSlot#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[WindowsFunctionAppSlotBackup], result)

    @builtins.property
    def builtin_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should built in logging be enabled. Configures ``AzureWebJobsDashboard`` app setting based on the configured storage setting.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#builtin_logging_enabled WindowsFunctionAppSlot#builtin_logging_enabled}
        '''
        result = self._values.get("builtin_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Function App Slot use Client Certificates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_enabled WindowsFunctionAppSlot#client_certificate_enabled}
        '''
        result = self._values.get("client_certificate_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate_exclusion_paths(self) -> typing.Optional[builtins.str]:
        '''Paths to exclude when using client certificates, separated by ;

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_exclusion_paths WindowsFunctionAppSlot#client_certificate_exclusion_paths}
        '''
        result = self._values.get("client_certificate_exclusion_paths")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the Function App Slot's client certificates requirement for incoming requests.

        Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#client_certificate_mode WindowsFunctionAppSlot#client_certificate_mode}
        '''
        result = self._values.get("client_certificate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotConnectionString"]]]:
        '''connection_string block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#connection_string WindowsFunctionAppSlot#connection_string}
        '''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotConnectionString"]]], result)

    @builtins.property
    def content_share_force_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force disable the content share settings.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#content_share_force_disabled WindowsFunctionAppSlot#content_share_force_disabled}
        '''
        result = self._values.get("content_share_force_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def daily_memory_time_quota(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory in gigabyte-seconds that your application is allowed to consume per day.

        Setting this value only affects function apps in Consumption Plans.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#daily_memory_time_quota WindowsFunctionAppSlot#daily_memory_time_quota}
        '''
        result = self._values.get("daily_memory_time_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the Windows Function App Slot enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#enabled WindowsFunctionAppSlot#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def functions_extension_version(self) -> typing.Optional[builtins.str]:
        '''The runtime version associated with the Function App Slot.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#functions_extension_version WindowsFunctionAppSlot#functions_extension_version}
        '''
        result = self._values.get("functions_extension_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Can the Function App Slot only be accessed via HTTPS?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#https_only WindowsFunctionAppSlot#https_only}
        '''
        result = self._values.get("https_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#id WindowsFunctionAppSlot#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["WindowsFunctionAppSlotIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#identity WindowsFunctionAppSlot#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotIdentity"], result)

    @builtins.property
    def key_vault_reference_identity_id(self) -> typing.Optional[builtins.str]:
        '''The User Assigned Identity to use for Key Vault access.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#key_vault_reference_identity_id WindowsFunctionAppSlot#key_vault_reference_identity_id}
        '''
        result = self._values.get("key_vault_reference_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotStorageAccount"]]]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account WindowsFunctionAppSlot#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotStorageAccount"]]], result)

    @builtins.property
    def storage_account_access_key(self) -> typing.Optional[builtins.str]:
        '''The access key which will be used to access the storage account for the Function App Slot.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_access_key WindowsFunctionAppSlot#storage_account_access_key}
        '''
        result = self._values.get("storage_account_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_name(self) -> typing.Optional[builtins.str]:
        '''The backend storage account name which will be used by this Function App Slot.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_account_name WindowsFunctionAppSlot#storage_account_name}
        '''
        result = self._values.get("storage_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_key_vault_secret_id(self) -> typing.Optional[builtins.str]:
        '''The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_key_vault_secret_id WindowsFunctionAppSlot#storage_key_vault_secret_id}
        '''
        result = self._values.get("storage_key_vault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_uses_managed_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Function App Slot use its Managed Identity to access storage?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#storage_uses_managed_identity WindowsFunctionAppSlot#storage_uses_managed_identity}
        '''
        result = self._values.get("storage_uses_managed_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#tags WindowsFunctionAppSlot#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WindowsFunctionAppSlotTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#timeouts WindowsFunctionAppSlot#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotTimeouts"], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.'''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotConnectionString",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class WindowsFunctionAppSlotConnectionString:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: The name which should be used for this Connection. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        :param type: Type of database. Possible values include: ``MySQL``, ``SQLServer``, ``SQLAzure``, ``Custom``, ``NotificationHub``, ``ServiceBus``, ``EventHub``, ``APIHub``, ``DocDb``, ``RedisCache``, and ``PostgreSQL``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}
        :param value: The connection string value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#value WindowsFunctionAppSlot#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b0b57adee72d12515e8851149d3cbb675e271b7986d608723b01650004a895)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name which should be used for this Connection.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of database. Possible values include: ``MySQL``, ``SQLServer``, ``SQLAzure``, ``Custom``, ``NotificationHub``, ``ServiceBus``, ``EventHub``, ``APIHub``, ``DocDb``, ``RedisCache``, and ``PostgreSQL``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The connection string value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#value WindowsFunctionAppSlot#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotConnectionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotConnectionStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotConnectionStringList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393a7f5d1d65b2a01d7c983a667e5749f929297b6fab9a77ce0ff46f6142aedd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotConnectionStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9d968cd830bd21b265afa717463dd165aeb4f473d57c04c7d42f0f08105a19)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotConnectionStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef354a9ec8149703741feacb1a0aac77d1760fc6a2f52e8cc7b85a7ae14d8d22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42138e7d704435529c3e9031ff167869a31063b3411503e10b43e8f590c4d654)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__962f38cc77597d8e85ef7df1bac76fabaeb80be746b40154de654cefe97600a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotConnectionString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotConnectionString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotConnectionString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b51634e37686afbd9199681504559188679feccdbcff619c7bfe2e379719d578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotConnectionStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotConnectionStringOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a93d77282427c4e959296009a8c20ddfcb9a556d20f1c554d31ebd4635088bb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0016ff2c09bf10e4d3777161855ce6c272a2eea76fd5237b33bad4d494905ba9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34df858a250769032142534a04999ac79dbe3436884bd558f2e8f971419db698)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438432602cdda20616a06d6616e932faff2b88648b05a6809e286ffec3fe05f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotConnectionString, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotConnectionString, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotConnectionString, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db8e44fa8162123117a9ddec829edf94853e9b971e92db4ddefedaaaf7bb501)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class WindowsFunctionAppSlotIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#identity_ids WindowsFunctionAppSlot#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21dc7437adf58ca06a7788f9a53c96974a9463497b11c17376750171d628b63a)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#identity_ids WindowsFunctionAppSlot#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40a5a7299e61802620de312d68a7cf99b4715acc5d4723021f938357d0feee5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1266c821ef7b0c6cdcd692f182eccd12e27e3fee909384fb8c1ceb5a3610a1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5922d54ddf858303e1735d48c5afc86ca0a4a506898f673e377159e85900a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotIdentity]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5e1941f56220ec7c6ce4cda16b07a87427e29b5f4e44a7bfd916b4bc0e937c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfig",
    jsii_struct_bases=[],
    name_mapping={
        "always_on": "alwaysOn",
        "api_definition_url": "apiDefinitionUrl",
        "api_management_api_id": "apiManagementApiId",
        "app_command_line": "appCommandLine",
        "application_insights_connection_string": "applicationInsightsConnectionString",
        "application_insights_key": "applicationInsightsKey",
        "application_stack": "applicationStack",
        "app_scale_limit": "appScaleLimit",
        "app_service_logs": "appServiceLogs",
        "auto_swap_slot_name": "autoSwapSlotName",
        "cors": "cors",
        "default_documents": "defaultDocuments",
        "elastic_instance_minimum": "elasticInstanceMinimum",
        "ftps_state": "ftpsState",
        "health_check_eviction_time_in_min": "healthCheckEvictionTimeInMin",
        "health_check_path": "healthCheckPath",
        "http2_enabled": "http2Enabled",
        "ip_restriction": "ipRestriction",
        "load_balancing_mode": "loadBalancingMode",
        "managed_pipeline_mode": "managedPipelineMode",
        "minimum_tls_version": "minimumTlsVersion",
        "pre_warmed_instance_count": "preWarmedInstanceCount",
        "remote_debugging_enabled": "remoteDebuggingEnabled",
        "remote_debugging_version": "remoteDebuggingVersion",
        "runtime_scale_monitoring_enabled": "runtimeScaleMonitoringEnabled",
        "scm_ip_restriction": "scmIpRestriction",
        "scm_minimum_tls_version": "scmMinimumTlsVersion",
        "scm_use_main_ip_restriction": "scmUseMainIpRestriction",
        "use32_bit_worker": "use32BitWorker",
        "vnet_route_all_enabled": "vnetRouteAllEnabled",
        "websockets_enabled": "websocketsEnabled",
        "worker_count": "workerCount",
    },
)
class WindowsFunctionAppSlotSiteConfig:
    def __init__(
        self,
        *,
        always_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_definition_url: typing.Optional[builtins.str] = None,
        api_management_api_id: typing.Optional[builtins.str] = None,
        app_command_line: typing.Optional[builtins.str] = None,
        application_insights_connection_string: typing.Optional[builtins.str] = None,
        application_insights_key: typing.Optional[builtins.str] = None,
        application_stack: typing.Optional[typing.Union["WindowsFunctionAppSlotSiteConfigApplicationStack", typing.Dict[builtins.str, typing.Any]]] = None,
        app_scale_limit: typing.Optional[jsii.Number] = None,
        app_service_logs: typing.Optional[typing.Union["WindowsFunctionAppSlotSiteConfigAppServiceLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_swap_slot_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Union["WindowsFunctionAppSlotSiteConfigCors", typing.Dict[builtins.str, typing.Any]]] = None,
        default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
        elastic_instance_minimum: typing.Optional[jsii.Number] = None,
        ftps_state: typing.Optional[builtins.str] = None,
        health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        load_balancing_mode: typing.Optional[builtins.str] = None,
        managed_pipeline_mode: typing.Optional[builtins.str] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        pre_warmed_instance_count: typing.Optional[jsii.Number] = None,
        remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_debugging_version: typing.Optional[builtins.str] = None,
        runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm_minimum_tls_version: typing.Optional[builtins.str] = None,
        scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param always_on: If this Windows Web App is Always On enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#always_on WindowsFunctionAppSlot#always_on}
        :param api_definition_url: The URL of the API definition that describes this Windows Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#api_definition_url WindowsFunctionAppSlot#api_definition_url}
        :param api_management_api_id: The ID of the API Management API for this Windows Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#api_management_api_id WindowsFunctionAppSlot#api_management_api_id}
        :param app_command_line: The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_command_line WindowsFunctionAppSlot#app_command_line}
        :param application_insights_connection_string: The Connection String for linking the Windows Function App to Application Insights. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_insights_connection_string WindowsFunctionAppSlot#application_insights_connection_string}
        :param application_insights_key: The Instrumentation Key for connecting the Windows Function App to Application Insights. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_insights_key WindowsFunctionAppSlot#application_insights_key}
        :param application_stack: application_stack block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_stack WindowsFunctionAppSlot#application_stack}
        :param app_scale_limit: The number of workers this function app can scale out to. Only applicable to apps on the Consumption and Premium plan. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_scale_limit WindowsFunctionAppSlot#app_scale_limit}
        :param app_service_logs: app_service_logs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_service_logs WindowsFunctionAppSlot#app_service_logs}
        :param auto_swap_slot_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#auto_swap_slot_name WindowsFunctionAppSlot#auto_swap_slot_name}.
        :param cors: cors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#cors WindowsFunctionAppSlot#cors}
        :param default_documents: Specifies a list of Default Documents for the Windows Web App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#default_documents WindowsFunctionAppSlot#default_documents}
        :param elastic_instance_minimum: The number of minimum instances for this Windows Function App. Only affects apps on Elastic Premium plans. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#elastic_instance_minimum WindowsFunctionAppSlot#elastic_instance_minimum}
        :param ftps_state: State of FTP / FTPS service for this function app. Possible values include: ``AllAllowed``, ``FtpsOnly`` and ``Disabled``. Defaults to ``Disabled``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ftps_state WindowsFunctionAppSlot#ftps_state}
        :param health_check_eviction_time_in_min: The amount of time in minutes that a node is unhealthy before being removed from the load balancer. Possible values are between ``2`` and ``10``. Defaults to ``10``. Only valid in conjunction with ``health_check_path`` Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#health_check_eviction_time_in_min WindowsFunctionAppSlot#health_check_eviction_time_in_min}
        :param health_check_path: The path to be checked for this function app health. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#health_check_path WindowsFunctionAppSlot#health_check_path}
        :param http2_enabled: Specifies if the http2 protocol should be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#http2_enabled WindowsFunctionAppSlot#http2_enabled}
        :param ip_restriction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_restriction WindowsFunctionAppSlot#ip_restriction}.
        :param load_balancing_mode: The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#load_balancing_mode WindowsFunctionAppSlot#load_balancing_mode}
        :param managed_pipeline_mode: The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#managed_pipeline_mode WindowsFunctionAppSlot#managed_pipeline_mode}
        :param minimum_tls_version: The configures the minimum version of TLS required for SSL requests. Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#minimum_tls_version WindowsFunctionAppSlot#minimum_tls_version}
        :param pre_warmed_instance_count: The number of pre-warmed instances for this function app. Only affects apps on an Elastic Premium plan. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#pre_warmed_instance_count WindowsFunctionAppSlot#pre_warmed_instance_count}
        :param remote_debugging_enabled: Should Remote Debugging be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#remote_debugging_enabled WindowsFunctionAppSlot#remote_debugging_enabled}
        :param remote_debugging_version: The Remote Debugging Version. Possible values include ``VS2017``, ``VS2019``, and ``VS2022``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#remote_debugging_version WindowsFunctionAppSlot#remote_debugging_version}
        :param runtime_scale_monitoring_enabled: Should Functions Runtime Scale Monitoring be enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#runtime_scale_monitoring_enabled WindowsFunctionAppSlot#runtime_scale_monitoring_enabled}
        :param scm_ip_restriction: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_ip_restriction WindowsFunctionAppSlot#scm_ip_restriction}.
        :param scm_minimum_tls_version: Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_minimum_tls_version WindowsFunctionAppSlot#scm_minimum_tls_version}
        :param scm_use_main_ip_restriction: Should the Windows Function App ``ip_restriction`` configuration be used for the SCM also. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_use_main_ip_restriction WindowsFunctionAppSlot#scm_use_main_ip_restriction}
        :param use32_bit_worker: Should the Windows Web App use a 32-bit worker. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_32_bit_worker WindowsFunctionAppSlot#use_32_bit_worker}
        :param vnet_route_all_enabled: Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#vnet_route_all_enabled WindowsFunctionAppSlot#vnet_route_all_enabled}
        :param websockets_enabled: Should Web Sockets be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#websockets_enabled WindowsFunctionAppSlot#websockets_enabled}
        :param worker_count: The number of Workers for this Windows Function App. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#worker_count WindowsFunctionAppSlot#worker_count}
        '''
        if isinstance(application_stack, dict):
            application_stack = WindowsFunctionAppSlotSiteConfigApplicationStack(**application_stack)
        if isinstance(app_service_logs, dict):
            app_service_logs = WindowsFunctionAppSlotSiteConfigAppServiceLogs(**app_service_logs)
        if isinstance(cors, dict):
            cors = WindowsFunctionAppSlotSiteConfigCors(**cors)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff650030a5bac5089174ff3c257ac53eecdf890c424958eaac22eca45ef1571)
            check_type(argname="argument always_on", value=always_on, expected_type=type_hints["always_on"])
            check_type(argname="argument api_definition_url", value=api_definition_url, expected_type=type_hints["api_definition_url"])
            check_type(argname="argument api_management_api_id", value=api_management_api_id, expected_type=type_hints["api_management_api_id"])
            check_type(argname="argument app_command_line", value=app_command_line, expected_type=type_hints["app_command_line"])
            check_type(argname="argument application_insights_connection_string", value=application_insights_connection_string, expected_type=type_hints["application_insights_connection_string"])
            check_type(argname="argument application_insights_key", value=application_insights_key, expected_type=type_hints["application_insights_key"])
            check_type(argname="argument application_stack", value=application_stack, expected_type=type_hints["application_stack"])
            check_type(argname="argument app_scale_limit", value=app_scale_limit, expected_type=type_hints["app_scale_limit"])
            check_type(argname="argument app_service_logs", value=app_service_logs, expected_type=type_hints["app_service_logs"])
            check_type(argname="argument auto_swap_slot_name", value=auto_swap_slot_name, expected_type=type_hints["auto_swap_slot_name"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument default_documents", value=default_documents, expected_type=type_hints["default_documents"])
            check_type(argname="argument elastic_instance_minimum", value=elastic_instance_minimum, expected_type=type_hints["elastic_instance_minimum"])
            check_type(argname="argument ftps_state", value=ftps_state, expected_type=type_hints["ftps_state"])
            check_type(argname="argument health_check_eviction_time_in_min", value=health_check_eviction_time_in_min, expected_type=type_hints["health_check_eviction_time_in_min"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument http2_enabled", value=http2_enabled, expected_type=type_hints["http2_enabled"])
            check_type(argname="argument ip_restriction", value=ip_restriction, expected_type=type_hints["ip_restriction"])
            check_type(argname="argument load_balancing_mode", value=load_balancing_mode, expected_type=type_hints["load_balancing_mode"])
            check_type(argname="argument managed_pipeline_mode", value=managed_pipeline_mode, expected_type=type_hints["managed_pipeline_mode"])
            check_type(argname="argument minimum_tls_version", value=minimum_tls_version, expected_type=type_hints["minimum_tls_version"])
            check_type(argname="argument pre_warmed_instance_count", value=pre_warmed_instance_count, expected_type=type_hints["pre_warmed_instance_count"])
            check_type(argname="argument remote_debugging_enabled", value=remote_debugging_enabled, expected_type=type_hints["remote_debugging_enabled"])
            check_type(argname="argument remote_debugging_version", value=remote_debugging_version, expected_type=type_hints["remote_debugging_version"])
            check_type(argname="argument runtime_scale_monitoring_enabled", value=runtime_scale_monitoring_enabled, expected_type=type_hints["runtime_scale_monitoring_enabled"])
            check_type(argname="argument scm_ip_restriction", value=scm_ip_restriction, expected_type=type_hints["scm_ip_restriction"])
            check_type(argname="argument scm_minimum_tls_version", value=scm_minimum_tls_version, expected_type=type_hints["scm_minimum_tls_version"])
            check_type(argname="argument scm_use_main_ip_restriction", value=scm_use_main_ip_restriction, expected_type=type_hints["scm_use_main_ip_restriction"])
            check_type(argname="argument use32_bit_worker", value=use32_bit_worker, expected_type=type_hints["use32_bit_worker"])
            check_type(argname="argument vnet_route_all_enabled", value=vnet_route_all_enabled, expected_type=type_hints["vnet_route_all_enabled"])
            check_type(argname="argument websockets_enabled", value=websockets_enabled, expected_type=type_hints["websockets_enabled"])
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if always_on is not None:
            self._values["always_on"] = always_on
        if api_definition_url is not None:
            self._values["api_definition_url"] = api_definition_url
        if api_management_api_id is not None:
            self._values["api_management_api_id"] = api_management_api_id
        if app_command_line is not None:
            self._values["app_command_line"] = app_command_line
        if application_insights_connection_string is not None:
            self._values["application_insights_connection_string"] = application_insights_connection_string
        if application_insights_key is not None:
            self._values["application_insights_key"] = application_insights_key
        if application_stack is not None:
            self._values["application_stack"] = application_stack
        if app_scale_limit is not None:
            self._values["app_scale_limit"] = app_scale_limit
        if app_service_logs is not None:
            self._values["app_service_logs"] = app_service_logs
        if auto_swap_slot_name is not None:
            self._values["auto_swap_slot_name"] = auto_swap_slot_name
        if cors is not None:
            self._values["cors"] = cors
        if default_documents is not None:
            self._values["default_documents"] = default_documents
        if elastic_instance_minimum is not None:
            self._values["elastic_instance_minimum"] = elastic_instance_minimum
        if ftps_state is not None:
            self._values["ftps_state"] = ftps_state
        if health_check_eviction_time_in_min is not None:
            self._values["health_check_eviction_time_in_min"] = health_check_eviction_time_in_min
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if http2_enabled is not None:
            self._values["http2_enabled"] = http2_enabled
        if ip_restriction is not None:
            self._values["ip_restriction"] = ip_restriction
        if load_balancing_mode is not None:
            self._values["load_balancing_mode"] = load_balancing_mode
        if managed_pipeline_mode is not None:
            self._values["managed_pipeline_mode"] = managed_pipeline_mode
        if minimum_tls_version is not None:
            self._values["minimum_tls_version"] = minimum_tls_version
        if pre_warmed_instance_count is not None:
            self._values["pre_warmed_instance_count"] = pre_warmed_instance_count
        if remote_debugging_enabled is not None:
            self._values["remote_debugging_enabled"] = remote_debugging_enabled
        if remote_debugging_version is not None:
            self._values["remote_debugging_version"] = remote_debugging_version
        if runtime_scale_monitoring_enabled is not None:
            self._values["runtime_scale_monitoring_enabled"] = runtime_scale_monitoring_enabled
        if scm_ip_restriction is not None:
            self._values["scm_ip_restriction"] = scm_ip_restriction
        if scm_minimum_tls_version is not None:
            self._values["scm_minimum_tls_version"] = scm_minimum_tls_version
        if scm_use_main_ip_restriction is not None:
            self._values["scm_use_main_ip_restriction"] = scm_use_main_ip_restriction
        if use32_bit_worker is not None:
            self._values["use32_bit_worker"] = use32_bit_worker
        if vnet_route_all_enabled is not None:
            self._values["vnet_route_all_enabled"] = vnet_route_all_enabled
        if websockets_enabled is not None:
            self._values["websockets_enabled"] = websockets_enabled
        if worker_count is not None:
            self._values["worker_count"] = worker_count

    @builtins.property
    def always_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this Windows Web App is Always On enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#always_on WindowsFunctionAppSlot#always_on}
        '''
        result = self._values.get("always_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def api_definition_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the API definition that describes this Windows Function App.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#api_definition_url WindowsFunctionAppSlot#api_definition_url}
        '''
        result = self._values.get("api_definition_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_management_api_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the API Management API for this Windows Function App.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#api_management_api_id WindowsFunctionAppSlot#api_management_api_id}
        '''
        result = self._values.get("api_management_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_command_line(self) -> typing.Optional[builtins.str]:
        '''The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_command_line WindowsFunctionAppSlot#app_command_line}
        '''
        result = self._values.get("app_command_line")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_insights_connection_string(self) -> typing.Optional[builtins.str]:
        '''The Connection String for linking the Windows Function App to Application Insights.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_insights_connection_string WindowsFunctionAppSlot#application_insights_connection_string}
        '''
        result = self._values.get("application_insights_connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_insights_key(self) -> typing.Optional[builtins.str]:
        '''The Instrumentation Key for connecting the Windows Function App to Application Insights.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_insights_key WindowsFunctionAppSlot#application_insights_key}
        '''
        result = self._values.get("application_insights_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_stack(
        self,
    ) -> typing.Optional["WindowsFunctionAppSlotSiteConfigApplicationStack"]:
        '''application_stack block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#application_stack WindowsFunctionAppSlot#application_stack}
        '''
        result = self._values.get("application_stack")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotSiteConfigApplicationStack"], result)

    @builtins.property
    def app_scale_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of workers this function app can scale out to.

        Only applicable to apps on the Consumption and Premium plan.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_scale_limit WindowsFunctionAppSlot#app_scale_limit}
        '''
        result = self._values.get("app_scale_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_service_logs(
        self,
    ) -> typing.Optional["WindowsFunctionAppSlotSiteConfigAppServiceLogs"]:
        '''app_service_logs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#app_service_logs WindowsFunctionAppSlot#app_service_logs}
        '''
        result = self._values.get("app_service_logs")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotSiteConfigAppServiceLogs"], result)

    @builtins.property
    def auto_swap_slot_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#auto_swap_slot_name WindowsFunctionAppSlot#auto_swap_slot_name}.'''
        result = self._values.get("auto_swap_slot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(self) -> typing.Optional["WindowsFunctionAppSlotSiteConfigCors"]:
        '''cors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#cors WindowsFunctionAppSlot#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional["WindowsFunctionAppSlotSiteConfigCors"], result)

    @builtins.property
    def default_documents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Default Documents for the Windows Web App.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#default_documents WindowsFunctionAppSlot#default_documents}
        '''
        result = self._values.get("default_documents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def elastic_instance_minimum(self) -> typing.Optional[jsii.Number]:
        '''The number of minimum instances for this Windows Function App. Only affects apps on Elastic Premium plans.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#elastic_instance_minimum WindowsFunctionAppSlot#elastic_instance_minimum}
        '''
        result = self._values.get("elastic_instance_minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ftps_state(self) -> typing.Optional[builtins.str]:
        '''State of FTP / FTPS service for this function app.

        Possible values include: ``AllAllowed``, ``FtpsOnly`` and ``Disabled``. Defaults to ``Disabled``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ftps_state WindowsFunctionAppSlot#ftps_state}
        '''
        result = self._values.get("ftps_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_eviction_time_in_min(self) -> typing.Optional[jsii.Number]:
        '''The amount of time in minutes that a node is unhealthy before being removed from the load balancer.

        Possible values are between ``2`` and ``10``. Defaults to ``10``. Only valid in conjunction with ``health_check_path``

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#health_check_eviction_time_in_min WindowsFunctionAppSlot#health_check_eviction_time_in_min}
        '''
        result = self._values.get("health_check_eviction_time_in_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''The path to be checked for this function app health.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#health_check_path WindowsFunctionAppSlot#health_check_path}
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the http2 protocol should be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#http2_enabled WindowsFunctionAppSlot#http2_enabled}
        '''
        result = self._values.get("http2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigIpRestriction"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_restriction WindowsFunctionAppSlot#ip_restriction}.'''
        result = self._values.get("ip_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigIpRestriction"]]], result)

    @builtins.property
    def load_balancing_mode(self) -> typing.Optional[builtins.str]:
        '''The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#load_balancing_mode WindowsFunctionAppSlot#load_balancing_mode}
        '''
        result = self._values.get("load_balancing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_pipeline_mode(self) -> typing.Optional[builtins.str]:
        '''The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#managed_pipeline_mode WindowsFunctionAppSlot#managed_pipeline_mode}
        '''
        result = self._values.get("managed_pipeline_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''The configures the minimum version of TLS required for SSL requests.

        Possible values include: ``1.0``, ``1.1``, and  ``1.2``. Defaults to ``1.2``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#minimum_tls_version WindowsFunctionAppSlot#minimum_tls_version}
        '''
        result = self._values.get("minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_warmed_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The number of pre-warmed instances for this function app. Only affects apps on an Elastic Premium plan.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#pre_warmed_instance_count WindowsFunctionAppSlot#pre_warmed_instance_count}
        '''
        result = self._values.get("pre_warmed_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def remote_debugging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Remote Debugging be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#remote_debugging_enabled WindowsFunctionAppSlot#remote_debugging_enabled}
        '''
        result = self._values.get("remote_debugging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remote_debugging_version(self) -> typing.Optional[builtins.str]:
        '''The Remote Debugging Version. Possible values include ``VS2017``, ``VS2019``, and ``VS2022``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#remote_debugging_version WindowsFunctionAppSlot#remote_debugging_version}
        '''
        result = self._values.get("remote_debugging_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_scale_monitoring_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Functions Runtime Scale Monitoring be enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#runtime_scale_monitoring_enabled WindowsFunctionAppSlot#runtime_scale_monitoring_enabled}
        '''
        result = self._values.get("runtime_scale_monitoring_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scm_ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigScmIpRestriction"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_ip_restriction WindowsFunctionAppSlot#scm_ip_restriction}.'''
        result = self._values.get("scm_ip_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigScmIpRestriction"]]], result)

    @builtins.property
    def scm_minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, and  ``1.2``. Defaults to ``1.2``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_minimum_tls_version WindowsFunctionAppSlot#scm_minimum_tls_version}
        '''
        result = self._values.get("scm_minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scm_use_main_ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Windows Function App ``ip_restriction`` configuration be used for the SCM also.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#scm_use_main_ip_restriction WindowsFunctionAppSlot#scm_use_main_ip_restriction}
        '''
        result = self._values.get("scm_use_main_ip_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use32_bit_worker(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Windows Web App use a 32-bit worker.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_32_bit_worker WindowsFunctionAppSlot#use_32_bit_worker}
        '''
        result = self._values.get("use32_bit_worker")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vnet_route_all_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#vnet_route_all_enabled WindowsFunctionAppSlot#vnet_route_all_enabled}
        '''
        result = self._values.get("vnet_route_all_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def websockets_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Web Sockets be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#websockets_enabled WindowsFunctionAppSlot#websockets_enabled}
        '''
        result = self._values.get("websockets_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def worker_count(self) -> typing.Optional[jsii.Number]:
        '''The number of Workers for this Windows Function App.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#worker_count WindowsFunctionAppSlot#worker_count}
        '''
        result = self._values.get("worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigAppServiceLogs",
    jsii_struct_bases=[],
    name_mapping={
        "disk_quota_mb": "diskQuotaMb",
        "retention_period_days": "retentionPeriodDays",
    },
)
class WindowsFunctionAppSlotSiteConfigAppServiceLogs:
    def __init__(
        self,
        *,
        disk_quota_mb: typing.Optional[jsii.Number] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_quota_mb: The amount of disk space to use for logs. Valid values are between ``25`` and ``100``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#disk_quota_mb WindowsFunctionAppSlot#disk_quota_mb}
        :param retention_period_days: The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#retention_period_days WindowsFunctionAppSlot#retention_period_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c18a1f0a4b03c5f48b4d4602d9260e1b72ed3b8ce9a4581b5195b189cc0160)
            check_type(argname="argument disk_quota_mb", value=disk_quota_mb, expected_type=type_hints["disk_quota_mb"])
            check_type(argname="argument retention_period_days", value=retention_period_days, expected_type=type_hints["retention_period_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_quota_mb is not None:
            self._values["disk_quota_mb"] = disk_quota_mb
        if retention_period_days is not None:
            self._values["retention_period_days"] = retention_period_days

    @builtins.property
    def disk_quota_mb(self) -> typing.Optional[jsii.Number]:
        '''The amount of disk space to use for logs. Valid values are between ``25`` and ``100``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#disk_quota_mb WindowsFunctionAppSlot#disk_quota_mb}
        '''
        result = self._values.get("disk_quota_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_period_days(self) -> typing.Optional[jsii.Number]:
        '''The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#retention_period_days WindowsFunctionAppSlot#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigAppServiceLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotSiteConfigAppServiceLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigAppServiceLogsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31818ec29479ff85bd3dc8fbd13b7004e8606e6ba3db82c798854c91bbc1e89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskQuotaMb")
    def reset_disk_quota_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskQuotaMb", []))

    @jsii.member(jsii_name="resetRetentionPeriodDays")
    def reset_retention_period_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriodDays", []))

    @builtins.property
    @jsii.member(jsii_name="diskQuotaMbInput")
    def disk_quota_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskQuotaMbInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDaysInput")
    def retention_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="diskQuotaMb")
    def disk_quota_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskQuotaMb"))

    @disk_quota_mb.setter
    def disk_quota_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de28fb46061d70f7284e18e05ab0f6ebaa4c688277a69211fd03c3321af47d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskQuotaMb", value)

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__983fd87c399e2bb3850511525198ae78eae5335dbaf4074447ac77dca2ddc7bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfigAppServiceLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotSiteConfigAppServiceLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fee79197bea3eb1b461fd19bbf3014b487cf716902d7a4ca41fac48ad9d6d0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigApplicationStack",
    jsii_struct_bases=[],
    name_mapping={
        "dotnet_version": "dotnetVersion",
        "java_version": "javaVersion",
        "node_version": "nodeVersion",
        "powershell_core_version": "powershellCoreVersion",
        "use_custom_runtime": "useCustomRuntime",
        "use_dotnet_isolated_runtime": "useDotnetIsolatedRuntime",
    },
)
class WindowsFunctionAppSlotSiteConfigApplicationStack:
    def __init__(
        self,
        *,
        dotnet_version: typing.Optional[builtins.str] = None,
        java_version: typing.Optional[builtins.str] = None,
        node_version: typing.Optional[builtins.str] = None,
        powershell_core_version: typing.Optional[builtins.str] = None,
        use_custom_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_dotnet_isolated_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dotnet_version: The version of .Net. Possible values are ``3.1`` ``6`` and ``7``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#dotnet_version WindowsFunctionAppSlot#dotnet_version}
        :param java_version: The version of Java to use. Possible values are ``8``, and ``11``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#java_version WindowsFunctionAppSlot#java_version}
        :param node_version: The version of Node to use. Possible values include ``12``, and ``14``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#node_version WindowsFunctionAppSlot#node_version}
        :param powershell_core_version: The PowerShell Core version to use. Possible values are ``7``, and ``7.2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#powershell_core_version WindowsFunctionAppSlot#powershell_core_version}
        :param use_custom_runtime: Does the Function App use a custom Application Stack? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_custom_runtime WindowsFunctionAppSlot#use_custom_runtime}
        :param use_dotnet_isolated_runtime: Should the DotNet process use an isolated runtime. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_dotnet_isolated_runtime WindowsFunctionAppSlot#use_dotnet_isolated_runtime}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa207df7a38aa1058516abed7c9d8f0c6d6cac4fe82895a91dc5f23477fc2def)
            check_type(argname="argument dotnet_version", value=dotnet_version, expected_type=type_hints["dotnet_version"])
            check_type(argname="argument java_version", value=java_version, expected_type=type_hints["java_version"])
            check_type(argname="argument node_version", value=node_version, expected_type=type_hints["node_version"])
            check_type(argname="argument powershell_core_version", value=powershell_core_version, expected_type=type_hints["powershell_core_version"])
            check_type(argname="argument use_custom_runtime", value=use_custom_runtime, expected_type=type_hints["use_custom_runtime"])
            check_type(argname="argument use_dotnet_isolated_runtime", value=use_dotnet_isolated_runtime, expected_type=type_hints["use_dotnet_isolated_runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dotnet_version is not None:
            self._values["dotnet_version"] = dotnet_version
        if java_version is not None:
            self._values["java_version"] = java_version
        if node_version is not None:
            self._values["node_version"] = node_version
        if powershell_core_version is not None:
            self._values["powershell_core_version"] = powershell_core_version
        if use_custom_runtime is not None:
            self._values["use_custom_runtime"] = use_custom_runtime
        if use_dotnet_isolated_runtime is not None:
            self._values["use_dotnet_isolated_runtime"] = use_dotnet_isolated_runtime

    @builtins.property
    def dotnet_version(self) -> typing.Optional[builtins.str]:
        '''The version of .Net. Possible values are ``3.1`` ``6`` and ``7``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#dotnet_version WindowsFunctionAppSlot#dotnet_version}
        '''
        result = self._values.get("dotnet_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_version(self) -> typing.Optional[builtins.str]:
        '''The version of Java to use. Possible values are ``8``, and ``11``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#java_version WindowsFunctionAppSlot#java_version}
        '''
        result = self._values.get("java_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_version(self) -> typing.Optional[builtins.str]:
        '''The version of Node to use. Possible values include ``12``, and ``14``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#node_version WindowsFunctionAppSlot#node_version}
        '''
        result = self._values.get("node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def powershell_core_version(self) -> typing.Optional[builtins.str]:
        '''The PowerShell Core version to use. Possible values are ``7``, and ``7.2``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#powershell_core_version WindowsFunctionAppSlot#powershell_core_version}
        '''
        result = self._values.get("powershell_core_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_custom_runtime(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Does the Function App use a custom Application Stack?

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_custom_runtime WindowsFunctionAppSlot#use_custom_runtime}
        '''
        result = self._values.get("use_custom_runtime")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_dotnet_isolated_runtime(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the DotNet process use an isolated runtime. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_dotnet_isolated_runtime WindowsFunctionAppSlot#use_dotnet_isolated_runtime}
        '''
        result = self._values.get("use_dotnet_isolated_runtime")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigApplicationStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotSiteConfigApplicationStackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigApplicationStackOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0c67dfac743447b06fcf93ce5aaf3b9f16fe763ac955a43ff5b3f24e47b0d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDotnetVersion")
    def reset_dotnet_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDotnetVersion", []))

    @jsii.member(jsii_name="resetJavaVersion")
    def reset_java_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJavaVersion", []))

    @jsii.member(jsii_name="resetNodeVersion")
    def reset_node_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeVersion", []))

    @jsii.member(jsii_name="resetPowershellCoreVersion")
    def reset_powershell_core_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowershellCoreVersion", []))

    @jsii.member(jsii_name="resetUseCustomRuntime")
    def reset_use_custom_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCustomRuntime", []))

    @jsii.member(jsii_name="resetUseDotnetIsolatedRuntime")
    def reset_use_dotnet_isolated_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDotnetIsolatedRuntime", []))

    @builtins.property
    @jsii.member(jsii_name="dotnetVersionInput")
    def dotnet_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dotnetVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="javaVersionInput")
    def java_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "javaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersionInput")
    def node_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="powershellCoreVersionInput")
    def powershell_core_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "powershellCoreVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="useCustomRuntimeInput")
    def use_custom_runtime_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCustomRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="useDotnetIsolatedRuntimeInput")
    def use_dotnet_isolated_runtime_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDotnetIsolatedRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dotnetVersion")
    def dotnet_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dotnetVersion"))

    @dotnet_version.setter
    def dotnet_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9687531031a91c66d844cdb42e6c40b63409143a708284a7721933b643991de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dotnetVersion", value)

    @builtins.property
    @jsii.member(jsii_name="javaVersion")
    def java_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "javaVersion"))

    @java_version.setter
    def java_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eea4cb0e4363a90ab6e9f0f27d25866d20c89e213ba661fcbc8c21244ed560a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javaVersion", value)

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def node_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeVersion"))

    @node_version.setter
    def node_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c02074d53e0a77ed0f393f03647f752d056cc496efc0bcce1d7842a95be9912b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeVersion", value)

    @builtins.property
    @jsii.member(jsii_name="powershellCoreVersion")
    def powershell_core_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "powershellCoreVersion"))

    @powershell_core_version.setter
    def powershell_core_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40104496ecd33dcd5d5987a6bde6454b881490dea5759eb9bcf040ea397aed53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powershellCoreVersion", value)

    @builtins.property
    @jsii.member(jsii_name="useCustomRuntime")
    def use_custom_runtime(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCustomRuntime"))

    @use_custom_runtime.setter
    def use_custom_runtime(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fbabc4ec5541362863116e6b7daabaa2a4fd131bd658a869d5a8327af034a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCustomRuntime", value)

    @builtins.property
    @jsii.member(jsii_name="useDotnetIsolatedRuntime")
    def use_dotnet_isolated_runtime(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useDotnetIsolatedRuntime"))

    @use_dotnet_isolated_runtime.setter
    def use_dotnet_isolated_runtime(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0049266c161a9424f5ad49769fcc318f42125a307bc54514abcaa9f9f5c9090e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDotnetIsolatedRuntime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotSiteConfigApplicationStack]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfigApplicationStack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotSiteConfigApplicationStack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba26ae2f4e4d0674ff8bc6e5261d1de0971329e49df9838f790f25db82a9ff2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigCors",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_origins": "allowedOrigins",
        "support_credentials": "supportCredentials",
    },
)
class WindowsFunctionAppSlotSiteConfigCors:
    def __init__(
        self,
        *,
        allowed_origins: typing.Sequence[builtins.str],
        support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_origins: Specifies a list of origins that should be allowed to make cross-origin calls. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_origins WindowsFunctionAppSlot#allowed_origins}
        :param support_credentials: Are credentials allowed in CORS requests? Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#support_credentials WindowsFunctionAppSlot#support_credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59dbca173248ffc01315f9bff5090c598520825e6d01cc8f8e3c9a713e053c22)
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument support_credentials", value=support_credentials, expected_type=type_hints["support_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allowed_origins": allowed_origins,
        }
        if support_credentials is not None:
            self._values["support_credentials"] = support_credentials

    @builtins.property
    def allowed_origins(self) -> typing.List[builtins.str]:
        '''Specifies a list of origins that should be allowed to make cross-origin calls.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_origins WindowsFunctionAppSlot#allowed_origins}
        '''
        result = self._values.get("allowed_origins")
        assert result is not None, "Required property 'allowed_origins' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def support_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Are credentials allowed in CORS requests? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#support_credentials WindowsFunctionAppSlot#support_credentials}
        '''
        result = self._values.get("support_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotSiteConfigCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigCorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0a717a5b43f394d19cc3b53d4cd1088f866b3a126d40341acdaae352c6f26bb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSupportCredentials")
    def reset_support_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportCredentialsInput")
    def support_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ea4e9fe8731ad108bbc6b639d55585117a10015f4b366b47b3d461e92740ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value)

    @builtins.property
    @jsii.member(jsii_name="supportCredentials")
    def support_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportCredentials"))

    @support_credentials.setter
    def support_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2133fa4008ad47bab96b420983c161e3e4aaf78c1ad40f57f3354d57db95bb4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportCredentials", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotSiteConfigCors]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfigCors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotSiteConfigCors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f53442c2c2cd6c0889555d46a9d92de6ca035eb78c9f86667665f40f23c54780)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigIpRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "headers": "headers",
        "ip_address": "ipAddress",
        "name": "name",
        "priority": "priority",
        "service_tag": "serviceTag",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
    },
)
class WindowsFunctionAppSlotSiteConfigIpRestriction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_tag: typing.Optional[builtins.str] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#action WindowsFunctionAppSlot#action}.
        :param headers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#headers WindowsFunctionAppSlot#headers}.
        :param ip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_address WindowsFunctionAppSlot#ip_address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}.
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#priority WindowsFunctionAppSlot#priority}.
        :param service_tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#service_tag WindowsFunctionAppSlot#service_tag}.
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e572e318e21d92a649a5620360ffae46f6126d2878f79380dbeaea99cdeefc)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument service_tag", value=service_tag, expected_type=type_hints["service_tag"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if headers is not None:
            self._values["headers"] = headers
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if service_tag is not None:
            self._values["service_tag"] = service_tag
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#action WindowsFunctionAppSlot#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#headers WindowsFunctionAppSlot#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders"]]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_address WindowsFunctionAppSlot#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#priority WindowsFunctionAppSlot#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#service_tag WindowsFunctionAppSlot#service_tag}.'''
        result = self._values.get("service_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.'''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "x_azure_fdid": "xAzureFdid",
        "x_fd_health_probe": "xFdHealthProbe",
        "x_forwarded_for": "xForwardedFor",
        "x_forwarded_host": "xForwardedHost",
    },
)
class WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders:
    def __init__(
        self,
        *,
        x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param x_azure_fdid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_azure_fdid WindowsFunctionAppSlot#x_azure_fdid}.
        :param x_fd_health_probe: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_fd_health_probe WindowsFunctionAppSlot#x_fd_health_probe}.
        :param x_forwarded_for: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_for WindowsFunctionAppSlot#x_forwarded_for}.
        :param x_forwarded_host: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_host WindowsFunctionAppSlot#x_forwarded_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ef9f24ff3ed77eff605420a9ecdd7d4950c5ee474bbaec77bee4f2fc3876f3)
            check_type(argname="argument x_azure_fdid", value=x_azure_fdid, expected_type=type_hints["x_azure_fdid"])
            check_type(argname="argument x_fd_health_probe", value=x_fd_health_probe, expected_type=type_hints["x_fd_health_probe"])
            check_type(argname="argument x_forwarded_for", value=x_forwarded_for, expected_type=type_hints["x_forwarded_for"])
            check_type(argname="argument x_forwarded_host", value=x_forwarded_host, expected_type=type_hints["x_forwarded_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x_azure_fdid is not None:
            self._values["x_azure_fdid"] = x_azure_fdid
        if x_fd_health_probe is not None:
            self._values["x_fd_health_probe"] = x_fd_health_probe
        if x_forwarded_for is not None:
            self._values["x_forwarded_for"] = x_forwarded_for
        if x_forwarded_host is not None:
            self._values["x_forwarded_host"] = x_forwarded_host

    @builtins.property
    def x_azure_fdid(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_azure_fdid WindowsFunctionAppSlot#x_azure_fdid}.'''
        result = self._values.get("x_azure_fdid")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_fd_health_probe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_fd_health_probe WindowsFunctionAppSlot#x_fd_health_probe}.'''
        result = self._values.get("x_fd_health_probe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_for WindowsFunctionAppSlot#x_forwarded_for}.'''
        result = self._values.get("x_forwarded_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_host WindowsFunctionAppSlot#x_forwarded_host}.'''
        result = self._values.get("x_forwarded_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c0e05aec039b7e796e2b08726817dcf59a8c2dbaf1a2a8c97def183ed6a6dc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d04eaad87b5c059978a3d66b5d1ac9103ad709e23636e1bad1412b73b5c77b36)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3bf01583f98ac96d5ffbc212ad1c69cf93606b572e75e8c15405462c3e381db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71da69d859f3b290295ab65d5aa7bc16639392eba7e3d85ca97376f5fb6cb15d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54646e3c153409812d25d0f180e69459d65dd1689dae631dc90846d71c5286a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767b99a7a96ef9ec847d5073fa4eedf86e6c393b131950d419ca075ebc432a0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d8d06ffe232d73d565e71e2eb5134b4f72db1051b735da6c15c26317c7b179)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetXAzureFdid")
    def reset_x_azure_fdid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXAzureFdid", []))

    @jsii.member(jsii_name="resetXFdHealthProbe")
    def reset_x_fd_health_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXFdHealthProbe", []))

    @jsii.member(jsii_name="resetXForwardedFor")
    def reset_x_forwarded_for(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedFor", []))

    @jsii.member(jsii_name="resetXForwardedHost")
    def reset_x_forwarded_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedHost", []))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdidInput")
    def x_azure_fdid_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xAzureFdidInput"))

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbeInput")
    def x_fd_health_probe_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xFdHealthProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedForInput")
    def x_forwarded_for_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedForInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedHostInput")
    def x_forwarded_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedHostInput"))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdid")
    def x_azure_fdid(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xAzureFdid"))

    @x_azure_fdid.setter
    def x_azure_fdid(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b2d69d138798336cb19825c035c208c9f9fc89dfc245010d1f11b0e6302b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xAzureFdid", value)

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @x_fd_health_probe.setter
    def x_fd_health_probe(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f8d3caae689429d638c658c5a0a9c9383b086f38df338c93cb2395b7610c129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xFdHealthProbe", value)

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @x_forwarded_for.setter
    def x_forwarded_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f2fd08623392e47bc03f341746c9c2bee0385f9bda9f712425a396723d55f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedFor", value)

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @x_forwarded_host.setter
    def x_forwarded_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3357fc68561d920a94beb8ede9b2ea4ccca4fa9a126384a7e379d66cef40feea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedHost", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d992ce419a03af3433645950ee0f2ac2b4fea154c4500722c925453a02d27f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigIpRestrictionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0523ec722a57ee86ec43dcb217ae3b3066a1922e11fcb8575cdd729dcc0f64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotSiteConfigIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63629fd6ce410a4412c7113770fa241015e428b3647c25b2ee73978e1c2f7c44)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotSiteConfigIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ee268a9d14269cf1128cfcc4df99f54232cce3f657ca665b60d0a87452f857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904c63fb397e4ac2261038941f8c4420ff06f9393daa16030d028bed8639fbcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368ff38ebe17da6f43cc8dbf4382b003a038fa8464541068ed8662d49793a222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__476c0a76dfc0facfba32cd0a5b884d0265b8a5407d2d6b92a2f29fc8f3084f71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigIpRestrictionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d114bd47cb961027f58da3a995813c46548a6e7711b1b7f27a20578cb9a60091)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__571e497370f11c4b6d1a005e38c558055483c143877317848c780527e9f92877)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetServiceTag")
    def reset_service_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceTag", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersList:
        return typing.cast(WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTagInput")
    def service_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26cdd65cfd217a5d7371285262dcaa75fe4521e7d2bbf8eafa5dcbbb1065992e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fd4b08f25f00d8779c0f87141f83b105e935f00cb94ff4ed7cc55371eb809e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e72c9c72abc30d420e29e375562fe71bcdd5d77a68152e598df67864cf43ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca17db56b5c7fc83b7f252ca217466215b64977b51ec5ff6a508085e570fd4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @service_tag.setter
    def service_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e9801ca72501558bea7ee916b63de4146c18b2c60b4055993d7e5ba38d4b40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceTag", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a09d145e48d173d56bb6c94ca8ef6b1f4e292db515f8dc6161797fda449abb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c5ff69f385ab9228cb5c4295299e8f78aa1f6929f66ed0322c9ace89c130b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06afcbdefa45bc9a469ef899ba45a3d27bf42d0a4791bffd1a0fbba905f7b0b3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApplicationStack")
    def put_application_stack(
        self,
        *,
        dotnet_version: typing.Optional[builtins.str] = None,
        java_version: typing.Optional[builtins.str] = None,
        node_version: typing.Optional[builtins.str] = None,
        powershell_core_version: typing.Optional[builtins.str] = None,
        use_custom_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_dotnet_isolated_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dotnet_version: The version of .Net. Possible values are ``3.1`` ``6`` and ``7``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#dotnet_version WindowsFunctionAppSlot#dotnet_version}
        :param java_version: The version of Java to use. Possible values are ``8``, and ``11``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#java_version WindowsFunctionAppSlot#java_version}
        :param node_version: The version of Node to use. Possible values include ``12``, and ``14``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#node_version WindowsFunctionAppSlot#node_version}
        :param powershell_core_version: The PowerShell Core version to use. Possible values are ``7``, and ``7.2``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#powershell_core_version WindowsFunctionAppSlot#powershell_core_version}
        :param use_custom_runtime: Does the Function App use a custom Application Stack? Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_custom_runtime WindowsFunctionAppSlot#use_custom_runtime}
        :param use_dotnet_isolated_runtime: Should the DotNet process use an isolated runtime. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#use_dotnet_isolated_runtime WindowsFunctionAppSlot#use_dotnet_isolated_runtime}
        '''
        value = WindowsFunctionAppSlotSiteConfigApplicationStack(
            dotnet_version=dotnet_version,
            java_version=java_version,
            node_version=node_version,
            powershell_core_version=powershell_core_version,
            use_custom_runtime=use_custom_runtime,
            use_dotnet_isolated_runtime=use_dotnet_isolated_runtime,
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationStack", [value]))

    @jsii.member(jsii_name="putAppServiceLogs")
    def put_app_service_logs(
        self,
        *,
        disk_quota_mb: typing.Optional[jsii.Number] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_quota_mb: The amount of disk space to use for logs. Valid values are between ``25`` and ``100``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#disk_quota_mb WindowsFunctionAppSlot#disk_quota_mb}
        :param retention_period_days: The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#retention_period_days WindowsFunctionAppSlot#retention_period_days}
        '''
        value = WindowsFunctionAppSlotSiteConfigAppServiceLogs(
            disk_quota_mb=disk_quota_mb, retention_period_days=retention_period_days
        )

        return typing.cast(None, jsii.invoke(self, "putAppServiceLogs", [value]))

    @jsii.member(jsii_name="putCors")
    def put_cors(
        self,
        *,
        allowed_origins: typing.Sequence[builtins.str],
        support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_origins: Specifies a list of origins that should be allowed to make cross-origin calls. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#allowed_origins WindowsFunctionAppSlot#allowed_origins}
        :param support_credentials: Are credentials allowed in CORS requests? Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#support_credentials WindowsFunctionAppSlot#support_credentials}
        '''
        value = WindowsFunctionAppSlotSiteConfigCors(
            allowed_origins=allowed_origins, support_credentials=support_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putIpRestriction")
    def put_ip_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1717ea3d8434b5f8e54a5ed4060009f38dc8197feb173a4deceea729d5a0a5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRestriction", [value]))

    @jsii.member(jsii_name="putScmIpRestriction")
    def put_scm_ip_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82a62d685a224e481f3cbaa4403863c2b31a0ef6167791ef56b40b77e67d993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScmIpRestriction", [value]))

    @jsii.member(jsii_name="resetAlwaysOn")
    def reset_always_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysOn", []))

    @jsii.member(jsii_name="resetApiDefinitionUrl")
    def reset_api_definition_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiDefinitionUrl", []))

    @jsii.member(jsii_name="resetApiManagementApiId")
    def reset_api_management_api_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiManagementApiId", []))

    @jsii.member(jsii_name="resetAppCommandLine")
    def reset_app_command_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppCommandLine", []))

    @jsii.member(jsii_name="resetApplicationInsightsConnectionString")
    def reset_application_insights_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationInsightsConnectionString", []))

    @jsii.member(jsii_name="resetApplicationInsightsKey")
    def reset_application_insights_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationInsightsKey", []))

    @jsii.member(jsii_name="resetApplicationStack")
    def reset_application_stack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationStack", []))

    @jsii.member(jsii_name="resetAppScaleLimit")
    def reset_app_scale_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppScaleLimit", []))

    @jsii.member(jsii_name="resetAppServiceLogs")
    def reset_app_service_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppServiceLogs", []))

    @jsii.member(jsii_name="resetAutoSwapSlotName")
    def reset_auto_swap_slot_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSwapSlotName", []))

    @jsii.member(jsii_name="resetCors")
    def reset_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCors", []))

    @jsii.member(jsii_name="resetDefaultDocuments")
    def reset_default_documents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDocuments", []))

    @jsii.member(jsii_name="resetElasticInstanceMinimum")
    def reset_elastic_instance_minimum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticInstanceMinimum", []))

    @jsii.member(jsii_name="resetFtpsState")
    def reset_ftps_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFtpsState", []))

    @jsii.member(jsii_name="resetHealthCheckEvictionTimeInMin")
    def reset_health_check_eviction_time_in_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckEvictionTimeInMin", []))

    @jsii.member(jsii_name="resetHealthCheckPath")
    def reset_health_check_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckPath", []))

    @jsii.member(jsii_name="resetHttp2Enabled")
    def reset_http2_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Enabled", []))

    @jsii.member(jsii_name="resetIpRestriction")
    def reset_ip_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRestriction", []))

    @jsii.member(jsii_name="resetLoadBalancingMode")
    def reset_load_balancing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingMode", []))

    @jsii.member(jsii_name="resetManagedPipelineMode")
    def reset_managed_pipeline_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPipelineMode", []))

    @jsii.member(jsii_name="resetMinimumTlsVersion")
    def reset_minimum_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumTlsVersion", []))

    @jsii.member(jsii_name="resetPreWarmedInstanceCount")
    def reset_pre_warmed_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreWarmedInstanceCount", []))

    @jsii.member(jsii_name="resetRemoteDebuggingEnabled")
    def reset_remote_debugging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteDebuggingEnabled", []))

    @jsii.member(jsii_name="resetRemoteDebuggingVersion")
    def reset_remote_debugging_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteDebuggingVersion", []))

    @jsii.member(jsii_name="resetRuntimeScaleMonitoringEnabled")
    def reset_runtime_scale_monitoring_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeScaleMonitoringEnabled", []))

    @jsii.member(jsii_name="resetScmIpRestriction")
    def reset_scm_ip_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmIpRestriction", []))

    @jsii.member(jsii_name="resetScmMinimumTlsVersion")
    def reset_scm_minimum_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmMinimumTlsVersion", []))

    @jsii.member(jsii_name="resetScmUseMainIpRestriction")
    def reset_scm_use_main_ip_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmUseMainIpRestriction", []))

    @jsii.member(jsii_name="resetUse32BitWorker")
    def reset_use32_bit_worker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUse32BitWorker", []))

    @jsii.member(jsii_name="resetVnetRouteAllEnabled")
    def reset_vnet_route_all_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetRouteAllEnabled", []))

    @jsii.member(jsii_name="resetWebsocketsEnabled")
    def reset_websockets_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsocketsEnabled", []))

    @jsii.member(jsii_name="resetWorkerCount")
    def reset_worker_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerCount", []))

    @builtins.property
    @jsii.member(jsii_name="applicationStack")
    def application_stack(
        self,
    ) -> WindowsFunctionAppSlotSiteConfigApplicationStackOutputReference:
        return typing.cast(WindowsFunctionAppSlotSiteConfigApplicationStackOutputReference, jsii.get(self, "applicationStack"))

    @builtins.property
    @jsii.member(jsii_name="appServiceLogs")
    def app_service_logs(
        self,
    ) -> WindowsFunctionAppSlotSiteConfigAppServiceLogsOutputReference:
        return typing.cast(WindowsFunctionAppSlotSiteConfigAppServiceLogsOutputReference, jsii.get(self, "appServiceLogs"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> WindowsFunctionAppSlotSiteConfigCorsOutputReference:
        return typing.cast(WindowsFunctionAppSlotSiteConfigCorsOutputReference, jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="detailedErrorLoggingEnabled")
    def detailed_error_logging_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "detailedErrorLoggingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="ipRestriction")
    def ip_restriction(self) -> WindowsFunctionAppSlotSiteConfigIpRestrictionList:
        return typing.cast(WindowsFunctionAppSlotSiteConfigIpRestrictionList, jsii.get(self, "ipRestriction"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestriction")
    def scm_ip_restriction(
        self,
    ) -> "WindowsFunctionAppSlotSiteConfigScmIpRestrictionList":
        return typing.cast("WindowsFunctionAppSlotSiteConfigScmIpRestrictionList", jsii.get(self, "scmIpRestriction"))

    @builtins.property
    @jsii.member(jsii_name="scmType")
    def scm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmType"))

    @builtins.property
    @jsii.member(jsii_name="windowsFxVersion")
    def windows_fx_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowsFxVersion"))

    @builtins.property
    @jsii.member(jsii_name="alwaysOnInput")
    def always_on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysOnInput"))

    @builtins.property
    @jsii.member(jsii_name="apiDefinitionUrlInput")
    def api_definition_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiDefinitionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementApiIdInput")
    def api_management_api_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementApiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appCommandLineInput")
    def app_command_line_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appCommandLineInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsConnectionStringInput")
    def application_insights_connection_string_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInsightsConnectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsKeyInput")
    def application_insights_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInsightsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationStackInput")
    def application_stack_input(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotSiteConfigApplicationStack]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfigApplicationStack], jsii.get(self, "applicationStackInput"))

    @builtins.property
    @jsii.member(jsii_name="appScaleLimitInput")
    def app_scale_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appScaleLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="appServiceLogsInput")
    def app_service_logs_input(
        self,
    ) -> typing.Optional[WindowsFunctionAppSlotSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfigAppServiceLogs], jsii.get(self, "appServiceLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSwapSlotNameInput")
    def auto_swap_slot_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoSwapSlotNameInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(self) -> typing.Optional[WindowsFunctionAppSlotSiteConfigCors]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfigCors], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDocumentsInput")
    def default_documents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultDocumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimumInput")
    def elastic_instance_minimum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticInstanceMinimumInput"))

    @builtins.property
    @jsii.member(jsii_name="ftpsStateInput")
    def ftps_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ftpsStateInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckEvictionTimeInMinInput")
    def health_check_eviction_time_in_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckEvictionTimeInMinInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckPathInput")
    def health_check_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckPathInput"))

    @builtins.property
    @jsii.member(jsii_name="http2EnabledInput")
    def http2_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "http2EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionInput")
    def ip_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestriction]]], jsii.get(self, "ipRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingModeInput")
    def load_balancing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPipelineModeInput")
    def managed_pipeline_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedPipelineModeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersionInput")
    def minimum_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="preWarmedInstanceCountInput")
    def pre_warmed_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "preWarmedInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingEnabledInput")
    def remote_debugging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "remoteDebuggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingVersionInput")
    def remote_debugging_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteDebuggingVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeScaleMonitoringEnabledInput")
    def runtime_scale_monitoring_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runtimeScaleMonitoringEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestrictionInput")
    def scm_ip_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigScmIpRestriction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigScmIpRestriction"]]], jsii.get(self, "scmIpRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="scmMinimumTlsVersionInput")
    def scm_minimum_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scmMinimumTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="scmUseMainIpRestrictionInput")
    def scm_use_main_ip_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scmUseMainIpRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="use32BitWorkerInput")
    def use32_bit_worker_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "use32BitWorkerInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetRouteAllEnabledInput")
    def vnet_route_all_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vnetRouteAllEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="websocketsEnabledInput")
    def websockets_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "websocketsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCountInput")
    def worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysOn")
    def always_on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysOn"))

    @always_on.setter
    def always_on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1988483a9f1b6337193df93a9f6956d6a357535a57e3116920f252bceba67be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysOn", value)

    @builtins.property
    @jsii.member(jsii_name="apiDefinitionUrl")
    def api_definition_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiDefinitionUrl"))

    @api_definition_url.setter
    def api_definition_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c2b552ddeec7d96cc7a99db49ab9cae54d5297e51a8a9ecc21cd9edbf12e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiDefinitionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="apiManagementApiId")
    def api_management_api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementApiId"))

    @api_management_api_id.setter
    def api_management_api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dbd545773013a88a0026294167ba5ba893bee3dd1bdfd6f157c44784ca51a0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementApiId", value)

    @builtins.property
    @jsii.member(jsii_name="appCommandLine")
    def app_command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appCommandLine"))

    @app_command_line.setter
    def app_command_line(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43f8ccec62f7decbd8c6ffd571035cbe62423407df234fe69ddd90d4f7301a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appCommandLine", value)

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsConnectionString")
    def application_insights_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsConnectionString"))

    @application_insights_connection_string.setter
    def application_insights_connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d22645e093642a55f177f53ec6daac3f8cd7e2693be2e1c3f0bc00b9a4cf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsConnectionString", value)

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsKey")
    def application_insights_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsKey"))

    @application_insights_key.setter
    def application_insights_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__709b32c1e4c5a9ac4c6215d71cb63f8b1aa2f916469b8bcb1c1849607ef499df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsKey", value)

    @builtins.property
    @jsii.member(jsii_name="appScaleLimit")
    def app_scale_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appScaleLimit"))

    @app_scale_limit.setter
    def app_scale_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be632dd815697f569f1345947c48e52b41f8192347758d2d7075516950f1328)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appScaleLimit", value)

    @builtins.property
    @jsii.member(jsii_name="autoSwapSlotName")
    def auto_swap_slot_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoSwapSlotName"))

    @auto_swap_slot_name.setter
    def auto_swap_slot_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c633a244100554c569faa8810c8289e960f39eb771e3e6d3abbba0b041f684)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSwapSlotName", value)

    @builtins.property
    @jsii.member(jsii_name="defaultDocuments")
    def default_documents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultDocuments"))

    @default_documents.setter
    def default_documents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de3ece4f86b8db36b4c3beb06c9195cee1e1b0b075fb48a0b574c1a461a07a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDocuments", value)

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimum")
    def elastic_instance_minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticInstanceMinimum"))

    @elastic_instance_minimum.setter
    def elastic_instance_minimum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d115df99d9e63a2d839924f02560c5c17743c6392c888b3b29a18eac78ee49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticInstanceMinimum", value)

    @builtins.property
    @jsii.member(jsii_name="ftpsState")
    def ftps_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ftpsState"))

    @ftps_state.setter
    def ftps_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c0b1f9d7948662fac74cb5ddd2d05775e273da37157e4a260878d0ea8d428c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ftpsState", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckEvictionTimeInMin")
    def health_check_eviction_time_in_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckEvictionTimeInMin"))

    @health_check_eviction_time_in_min.setter
    def health_check_eviction_time_in_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f712ca88c324de7a0b7818d30654ad10f6435066d24952ea459e77f8d921fdbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckEvictionTimeInMin", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779005e00a5a02deed06dc4985cd4140f81e143f9ef04d771a302961eb328a28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckPath", value)

    @builtins.property
    @jsii.member(jsii_name="http2Enabled")
    def http2_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "http2Enabled"))

    @http2_enabled.setter
    def http2_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0113399b0a00125fc0aaa0abffe7237e44ceaa8c1f3b147cf8a68f6a63a7e306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Enabled", value)

    @builtins.property
    @jsii.member(jsii_name="loadBalancingMode")
    def load_balancing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingMode"))

    @load_balancing_mode.setter
    def load_balancing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa2accf36624f0a6234319ac10604f4186d87cd91c98679791ee96380145f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingMode", value)

    @builtins.property
    @jsii.member(jsii_name="managedPipelineMode")
    def managed_pipeline_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedPipelineMode"))

    @managed_pipeline_mode.setter
    def managed_pipeline_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae56c5c5cbf11ff324f5a59782d3d523919bfa831433e864d79426c1ea460c10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPipelineMode", value)

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersion")
    def minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumTlsVersion"))

    @minimum_tls_version.setter
    def minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a238a144b4d2bfe750e8ba6c3ee72d2131a2a7389dc919b6e1292bfffde7f22c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumTlsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="preWarmedInstanceCount")
    def pre_warmed_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preWarmedInstanceCount"))

    @pre_warmed_instance_count.setter
    def pre_warmed_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f4b85cd5984a8c536843875126171a252800f9ec95b2f7bf3def048b2e062a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preWarmedInstanceCount", value)

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingEnabled")
    def remote_debugging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remoteDebuggingEnabled"))

    @remote_debugging_enabled.setter
    def remote_debugging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c4cd195503c64888329de8bbd16bb9abd5142e53c695cc9d62c9e99a34902b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteDebuggingEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingVersion")
    def remote_debugging_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteDebuggingVersion"))

    @remote_debugging_version.setter
    def remote_debugging_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3627598fdaca221fd97337498ed1c436fb8e301f864e434bc44e17aaf0be9257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteDebuggingVersion", value)

    @builtins.property
    @jsii.member(jsii_name="runtimeScaleMonitoringEnabled")
    def runtime_scale_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runtimeScaleMonitoringEnabled"))

    @runtime_scale_monitoring_enabled.setter
    def runtime_scale_monitoring_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec66db54c1c84e81a7597d8bfb66f099e59e6ededb5007e1e8ef71f69814dc17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeScaleMonitoringEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="scmMinimumTlsVersion")
    def scm_minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmMinimumTlsVersion"))

    @scm_minimum_tls_version.setter
    def scm_minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24c55219c34daf1e5b750357c0cdcd9317488255501b4de4989d98b8067a1df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scmMinimumTlsVersion", value)

    @builtins.property
    @jsii.member(jsii_name="scmUseMainIpRestriction")
    def scm_use_main_ip_restriction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scmUseMainIpRestriction"))

    @scm_use_main_ip_restriction.setter
    def scm_use_main_ip_restriction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74927308f83ac8b080cfe94924fbaa65f5681b2ad9f1adbf71bb8a9fc3958b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scmUseMainIpRestriction", value)

    @builtins.property
    @jsii.member(jsii_name="use32BitWorker")
    def use32_bit_worker(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "use32BitWorker"))

    @use32_bit_worker.setter
    def use32_bit_worker(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842168806da6c1e550797ee893342dc05b619025f4c018257248ecc2012e366b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "use32BitWorker", value)

    @builtins.property
    @jsii.member(jsii_name="vnetRouteAllEnabled")
    def vnet_route_all_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vnetRouteAllEnabled"))

    @vnet_route_all_enabled.setter
    def vnet_route_all_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982c9b03850a0d4c7fb906de391cbfaeec78212767dc9f0b0b77cccda21a6527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetRouteAllEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="websocketsEnabled")
    def websockets_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "websocketsEnabled"))

    @websockets_enabled.setter
    def websockets_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6dbc89982bcaa85381a8dad047fa2bb323cade85002a17ecd145264078c17d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websocketsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @worker_count.setter
    def worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c204da4bbee62e7ffdbf7dd8d12fc061c0397876871133cbcbadb26dc6bea2f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotSiteConfig]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotSiteConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd258d5fdfaa36c959dafaba0c53cddd90f35a4a5e25d7a7b7f0210cdd0ee115)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigScmIpRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "headers": "headers",
        "ip_address": "ipAddress",
        "name": "name",
        "priority": "priority",
        "service_tag": "serviceTag",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
    },
)
class WindowsFunctionAppSlotSiteConfigScmIpRestriction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_tag: typing.Optional[builtins.str] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#action WindowsFunctionAppSlot#action}.
        :param headers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#headers WindowsFunctionAppSlot#headers}.
        :param ip_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_address WindowsFunctionAppSlot#ip_address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}.
        :param priority: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#priority WindowsFunctionAppSlot#priority}.
        :param service_tag: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#service_tag WindowsFunctionAppSlot#service_tag}.
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de30f100ab4b578db7f7cf411fcc73b4e953be3cefa1508757b70b775c6a4a6e)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument service_tag", value=service_tag, expected_type=type_hints["service_tag"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if headers is not None:
            self._values["headers"] = headers
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if service_tag is not None:
            self._values["service_tag"] = service_tag
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#action WindowsFunctionAppSlot#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#headers WindowsFunctionAppSlot#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders"]]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#ip_address WindowsFunctionAppSlot#ip_address}.'''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#priority WindowsFunctionAppSlot#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_tag(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#service_tag WindowsFunctionAppSlot#service_tag}.'''
        result = self._values.get("service_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#virtual_network_subnet_id WindowsFunctionAppSlot#virtual_network_subnet_id}.'''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigScmIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "x_azure_fdid": "xAzureFdid",
        "x_fd_health_probe": "xFdHealthProbe",
        "x_forwarded_for": "xForwardedFor",
        "x_forwarded_host": "xForwardedHost",
    },
)
class WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders:
    def __init__(
        self,
        *,
        x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param x_azure_fdid: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_azure_fdid WindowsFunctionAppSlot#x_azure_fdid}.
        :param x_fd_health_probe: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_fd_health_probe WindowsFunctionAppSlot#x_fd_health_probe}.
        :param x_forwarded_for: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_for WindowsFunctionAppSlot#x_forwarded_for}.
        :param x_forwarded_host: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_host WindowsFunctionAppSlot#x_forwarded_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76386af5f8304950b5c3c1742fbe7148e6fd2573148f1e822d0ad76dc6cc7ae8)
            check_type(argname="argument x_azure_fdid", value=x_azure_fdid, expected_type=type_hints["x_azure_fdid"])
            check_type(argname="argument x_fd_health_probe", value=x_fd_health_probe, expected_type=type_hints["x_fd_health_probe"])
            check_type(argname="argument x_forwarded_for", value=x_forwarded_for, expected_type=type_hints["x_forwarded_for"])
            check_type(argname="argument x_forwarded_host", value=x_forwarded_host, expected_type=type_hints["x_forwarded_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x_azure_fdid is not None:
            self._values["x_azure_fdid"] = x_azure_fdid
        if x_fd_health_probe is not None:
            self._values["x_fd_health_probe"] = x_fd_health_probe
        if x_forwarded_for is not None:
            self._values["x_forwarded_for"] = x_forwarded_for
        if x_forwarded_host is not None:
            self._values["x_forwarded_host"] = x_forwarded_host

    @builtins.property
    def x_azure_fdid(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_azure_fdid WindowsFunctionAppSlot#x_azure_fdid}.'''
        result = self._values.get("x_azure_fdid")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_fd_health_probe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_fd_health_probe WindowsFunctionAppSlot#x_fd_health_probe}.'''
        result = self._values.get("x_fd_health_probe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_for WindowsFunctionAppSlot#x_forwarded_for}.'''
        result = self._values.get("x_forwarded_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#x_forwarded_host WindowsFunctionAppSlot#x_forwarded_host}.'''
        result = self._values.get("x_forwarded_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe25d28f8081b280efb9b0593b75714c2e66ee1158f513366f6ee93d69eecf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400f2f13cc92a61969f186c904f17b2e27a541f8946086e88b450d22952b617d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c199dc7fd43490398a7706a18e83de7db6af0421a294ad7f9c7b33010b245d92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5b4db8963e08361dc7866c2a1050fe516da6248127fac3a31764dff8c72759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad9e496e84382f6d782d85101a628e402c559b885221aacfe3246793687c5d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5366d6586e2e44bb492a26d5a69d951c2a9a543aabef56ea6724c40a61bb9a3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1a5c4fbfdc3a6903d48d868eed9a1423268b8cc78db30a38e7a966582d33ae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetXAzureFdid")
    def reset_x_azure_fdid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXAzureFdid", []))

    @jsii.member(jsii_name="resetXFdHealthProbe")
    def reset_x_fd_health_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXFdHealthProbe", []))

    @jsii.member(jsii_name="resetXForwardedFor")
    def reset_x_forwarded_for(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedFor", []))

    @jsii.member(jsii_name="resetXForwardedHost")
    def reset_x_forwarded_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedHost", []))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdidInput")
    def x_azure_fdid_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xAzureFdidInput"))

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbeInput")
    def x_fd_health_probe_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xFdHealthProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedForInput")
    def x_forwarded_for_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedForInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedHostInput")
    def x_forwarded_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedHostInput"))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdid")
    def x_azure_fdid(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xAzureFdid"))

    @x_azure_fdid.setter
    def x_azure_fdid(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8333b21408b1d25a9b33e95b138f48f35b2d5d617ef6f6e130b69a758ec5f731)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xAzureFdid", value)

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @x_fd_health_probe.setter
    def x_fd_health_probe(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0c951388588063fa756ed7975336f281c357a0f04ab71957b161947bce7c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xFdHealthProbe", value)

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @x_forwarded_for.setter
    def x_forwarded_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfcda6dcbbf32c6e7d02fcb837de1ac8b7b2eff20c9e3a7e5accece09913e2e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedFor", value)

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @x_forwarded_host.setter
    def x_forwarded_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4d173460989d6cfed27a86ecb7bd22509c9a355106fe5bc4653c33905fa645)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedHost", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72857414c08c778efa516a125ac83e6da8f9b7555c6705ce5d8a9c4f1fcf854d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigScmIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigScmIpRestrictionList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecbc14b16cdc1b94a4e14b1e880633da948221d74f2ab8bc08b64baea6b36da7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotSiteConfigScmIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94049aa70fa1cb18fea31220276705c5e9360ac794bd669794d0eec7dd88762b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotSiteConfigScmIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8d7fe01c9fad431db6aff5a98a96c8ebee46e1680351eea2006d7eac09cd69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09cce3a71f03866d351d6f0f370cf83e03b8b7e5602bef40837489815bd419a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba6a079bab403151e5475eb14be9fcfca3e3fa6d816ff65cd7e92fa3f47dd82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac9d9288101688644688793094424a5ec47c7bca42e99825852a9c84d2d51914)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotSiteConfigScmIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteConfigScmIpRestrictionOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2533ddb5d9803e3c79020e4faf181ef29dbcf1fe70589f8d6cc50b3275f825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedde117906bad2918fd85391f3a25935c48f3c26efc6a6447cd5701b0e48d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetServiceTag")
    def reset_service_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceTag", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersList:
        return typing.cast(WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTagInput")
    def service_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9de087fd2e681d4f1c13ffae601f51102f25f022745991ed550a63dcd099911f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a997a43671931a65f6b56fdfc1b1548b0224afca8f5b5faa7052168fc253e48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5871bb41534804bff858250bdf545b96a2c6e8a775e3dc7fe8b0f518b0dd6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8039cd704ba7d74150628d335d344ed1bea03bc62132b3f224ce7efa4ead0da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @service_tag.setter
    def service_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9cffb7984ea7bf517fd75a035b7a1eb7da5d5b068c1beadb773f52e0d1df53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceTag", value)

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b70602ee92d70972b795c943f3115a16427cc8464e39e487465b83f172b1f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestriction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestriction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestriction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0d7a7f5674e29ab476a427d4923268aea24701ad5164cbebd46478ed95abb1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteCredential",
    jsii_struct_bases=[],
    name_mapping={},
)
class WindowsFunctionAppSlotSiteCredential:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotSiteCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotSiteCredentialList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteCredentialList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb202e9017c09126c89f87af09d0e497938c14a34b2a88f5271aec1bc763f914)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotSiteCredentialOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6969540264288c782b803fe755d8ea76beda20e3f3e6778dbc8a6a2926ca78a9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotSiteCredentialOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__470aa6d5d056033f165004d850b603d624aef6848a6469e168f39f9977eb8182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae17ffddff2dbc41ba7a324309cfed6e5cd1c85affdf5483a35bceca003b3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd20dc46447f28ea98cb83dac7bbfcd2a436474b962c122c704f5148881f23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class WindowsFunctionAppSlotSiteCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotSiteCredentialOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d751b6a4434653b397d5c98a31eb912495f7dc4876aefbacc6d28f12fb0adfd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WindowsFunctionAppSlotSiteCredential]:
        return typing.cast(typing.Optional[WindowsFunctionAppSlotSiteCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WindowsFunctionAppSlotSiteCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd7be5fa25b7a5f6460f663920bc9145c0091ac0cd476488bf0b95c1a852dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotStorageAccount",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "account_name": "accountName",
        "name": "name",
        "share_name": "shareName",
        "type": "type",
        "mount_path": "mountPath",
    },
)
class WindowsFunctionAppSlotStorageAccount:
    def __init__(
        self,
        *,
        access_key: builtins.str,
        account_name: builtins.str,
        name: builtins.str,
        share_name: builtins.str,
        type: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#access_key WindowsFunctionAppSlot#access_key}.
        :param account_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#account_name WindowsFunctionAppSlot#account_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}.
        :param share_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#share_name WindowsFunctionAppSlot#share_name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}.
        :param mount_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#mount_path WindowsFunctionAppSlot#mount_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a029735483c080fd2b28318765557e14141fbe0f23478b53eb297e397094d5)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key": access_key,
            "account_name": account_name,
            "name": name,
            "share_name": share_name,
            "type": type,
        }
        if mount_path is not None:
            self._values["mount_path"] = mount_path

    @builtins.property
    def access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#access_key WindowsFunctionAppSlot#access_key}.'''
        result = self._values.get("access_key")
        assert result is not None, "Required property 'access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#account_name WindowsFunctionAppSlot#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#name WindowsFunctionAppSlot#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def share_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#share_name WindowsFunctionAppSlot#share_name}.'''
        result = self._values.get("share_name")
        assert result is not None, "Required property 'share_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#type WindowsFunctionAppSlot#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#mount_path WindowsFunctionAppSlot#mount_path}.'''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotStorageAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotStorageAccountList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1073a610b9f5ee2341501b3f4b0547e9b32101dc19eb4dd63c613b92e2ad516)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WindowsFunctionAppSlotStorageAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bfafb10abcd38076d4be7e4c4213d78c82f16e5442e5ce275eb368792e55626)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WindowsFunctionAppSlotStorageAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b40edb8a3489692869f5c1e0b6b77bb1fdfdd0a7f0623c0006413c01c5f48e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25bee84169acd4cfba3a16fb10097d536d4ba3336a2019ab345284367368ffb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f1c50223527708954dc123e597a8e92967cb9c684c43a5bdc02e96e3eca57f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotStorageAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotStorageAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotStorageAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606287685fd7899ac80d687958304be639617ad3e1d63f15f61a5259a94878a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class WindowsFunctionAppSlotStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotStorageAccountOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bdbd501ca8375ffe2630c0b974fdef410d4553a56635473d9085a7400ad0513)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountPath")
    def reset_mount_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountPath", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="shareNameInput")
    def share_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e0c491d4ad6bc1074f0693df78dd39af2a5b8b81330bf239d2fcebb01083bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value)

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7fa46f9c4b0c294dd085110b9f4b0fa5983afcd922a8a8e1e039167ef68fd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value)

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73ad9a4820403e424f0dbb5f5d0198a0eb4eb7048c545c789fa81f52665084a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb3e08948a0cfb630c74cf0466104ea4ae71eba3c0be7eb1ff239ed36d9f1a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7b17b36145f89792c1cf686f622b960794f8a63a615830827a55de504ab954)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a1695519412b353048910d7f9aa4e2d244e650dc243b15d53b14f420f25e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotStorageAccount, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotStorageAccount, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotStorageAccount, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5b5ac6512c731f41c4f81858ae8f01e28f5ae2c805df56506ebe556749884d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class WindowsFunctionAppSlotTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#create WindowsFunctionAppSlot#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#delete WindowsFunctionAppSlot#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#read WindowsFunctionAppSlot#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#update WindowsFunctionAppSlot#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0227ccb1d906e1bbf8abed87d31ad8731571d9c01e6e79e544d537930f81e66)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#create WindowsFunctionAppSlot#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#delete WindowsFunctionAppSlot#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#read WindowsFunctionAppSlot#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/windows_function_app_slot#update WindowsFunctionAppSlot#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WindowsFunctionAppSlotTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WindowsFunctionAppSlotTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.windowsFunctionAppSlot.WindowsFunctionAppSlotTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f43442944d9a8ea03be70eecaaa49eef858e0f1fb5beb46d122f750f3498a5c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff054763a63334715d3158293ec3b0f6c3b4a518622b1f96d03d4a18e3a4b438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__750e1f40a8483e2156aba285db6f0ad2c2715e225974d756177c1ee4606a11d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c616b404183cc0cafb1b68f1af22755c004290e85280c67510747628fbf0d2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d09ae63f1e845ebdaa5f37ce4b7dc6a86b2920f040f52e51f0a6af2d0a9430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[WindowsFunctionAppSlotTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[WindowsFunctionAppSlotTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[WindowsFunctionAppSlotTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd94d47c1e6d6110afb53e93c5145250286eb91990a647c0d4a3719bdaefee51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "WindowsFunctionAppSlot",
    "WindowsFunctionAppSlotAuthSettings",
    "WindowsFunctionAppSlotAuthSettingsActiveDirectory",
    "WindowsFunctionAppSlotAuthSettingsActiveDirectoryOutputReference",
    "WindowsFunctionAppSlotAuthSettingsFacebook",
    "WindowsFunctionAppSlotAuthSettingsFacebookOutputReference",
    "WindowsFunctionAppSlotAuthSettingsGithub",
    "WindowsFunctionAppSlotAuthSettingsGithubOutputReference",
    "WindowsFunctionAppSlotAuthSettingsGoogle",
    "WindowsFunctionAppSlotAuthSettingsGoogleOutputReference",
    "WindowsFunctionAppSlotAuthSettingsMicrosoft",
    "WindowsFunctionAppSlotAuthSettingsMicrosoftOutputReference",
    "WindowsFunctionAppSlotAuthSettingsOutputReference",
    "WindowsFunctionAppSlotAuthSettingsTwitter",
    "WindowsFunctionAppSlotAuthSettingsTwitterOutputReference",
    "WindowsFunctionAppSlotBackup",
    "WindowsFunctionAppSlotBackupOutputReference",
    "WindowsFunctionAppSlotBackupSchedule",
    "WindowsFunctionAppSlotBackupScheduleOutputReference",
    "WindowsFunctionAppSlotConfig",
    "WindowsFunctionAppSlotConnectionString",
    "WindowsFunctionAppSlotConnectionStringList",
    "WindowsFunctionAppSlotConnectionStringOutputReference",
    "WindowsFunctionAppSlotIdentity",
    "WindowsFunctionAppSlotIdentityOutputReference",
    "WindowsFunctionAppSlotSiteConfig",
    "WindowsFunctionAppSlotSiteConfigAppServiceLogs",
    "WindowsFunctionAppSlotSiteConfigAppServiceLogsOutputReference",
    "WindowsFunctionAppSlotSiteConfigApplicationStack",
    "WindowsFunctionAppSlotSiteConfigApplicationStackOutputReference",
    "WindowsFunctionAppSlotSiteConfigCors",
    "WindowsFunctionAppSlotSiteConfigCorsOutputReference",
    "WindowsFunctionAppSlotSiteConfigIpRestriction",
    "WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders",
    "WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersList",
    "WindowsFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference",
    "WindowsFunctionAppSlotSiteConfigIpRestrictionList",
    "WindowsFunctionAppSlotSiteConfigIpRestrictionOutputReference",
    "WindowsFunctionAppSlotSiteConfigOutputReference",
    "WindowsFunctionAppSlotSiteConfigScmIpRestriction",
    "WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders",
    "WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersList",
    "WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference",
    "WindowsFunctionAppSlotSiteConfigScmIpRestrictionList",
    "WindowsFunctionAppSlotSiteConfigScmIpRestrictionOutputReference",
    "WindowsFunctionAppSlotSiteCredential",
    "WindowsFunctionAppSlotSiteCredentialList",
    "WindowsFunctionAppSlotSiteCredentialOutputReference",
    "WindowsFunctionAppSlotStorageAccount",
    "WindowsFunctionAppSlotStorageAccountList",
    "WindowsFunctionAppSlotStorageAccountOutputReference",
    "WindowsFunctionAppSlotTimeouts",
    "WindowsFunctionAppSlotTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__2c39c7cfc5bdabe0a2a399b8ca12f11efcafceb20bb181001c1278d00dce79f6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_app_id: builtins.str,
    name: builtins.str,
    site_config: typing.Union[WindowsFunctionAppSlotSiteConfig, typing.Dict[builtins.str, typing.Any]],
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    backup: typing.Optional[typing.Union[WindowsFunctionAppSlotBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotConnectionString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    daily_memory_time_quota: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    functions_extension_version: typing.Optional[builtins.str] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[WindowsFunctionAppSlotIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_account_name: typing.Optional[builtins.str] = None,
    storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
    storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WindowsFunctionAppSlotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a9882e2b66377586d7aa196327709891fca2565cf9b4117d99d9ec58b7f177(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotConnectionString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c512eb33b5b007c360c2a69cbf614d9156b301dda9adfffa937965d42deaaf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotStorageAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f854dbe2cecc8df66aada8e20d13fdef7f45123bff8bfe5e80a2c2c2dbce3187(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58e6f66a41e5bc7988168c38f3ef7dc78123376351fa7e9d0e4b26ffcaf36ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fd566dcac8bb05624de680ce22184f53fcda577bdf4a35b44ad8a27d53c1e3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c29db7d4ef3ef3a54d197dd633dc36b115835affb85f45ec972503a4f8df8ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a070b8c0d59c2d86399e45fe5382ce9214baabf87c7e6f9f4c640bc395a36da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab19ebb98e9b4b4ce4162f2ce9fbcf60a3e0fdbe0aa9bac6b38e07c9f60589d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0f8cc51248ecfd8f70718666ed8cf7eba31961d322ed6cf5f2d36c81337027(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677bf3ad271b60a8e970b8d3d62f2f3eb9c05dc75f8449cbdb852ee4770b1599(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389e6483d524c51282157954b8e5365ef3031cdfa2ecf25750fc6e45a1090ab5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89e634c8f07bcea3e1f64f65fbd4854a7c13e1132621515e6d66715f06b3958e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd29b2b908d5eb7d3279b1372537333a24df08600de6c5ee8ce8ebefdf429fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef358c0055f92afe6fcd0680bb3b7d05e8bf145121e6814bd22c4b318a99181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108bdb79c2546c2a4f4facc86d28ad167f311acd9cd80654e107980d49af39ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dda8f7e55ddf80db84c6446e4af7f187aa65db9d2a937fefdb6442d0b30af70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b7564c84940913bf0557dc56ffc2b8b20b0b695f1c063b2743f6380d71dfe5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96453ba9d746419dca32d5142c5e89e7b67ec14e9e52fc02183f31f69bf7479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737652d9db0d93efb1da43fd78f11f761150c3b38de91b25a492e984671c6167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe55ebff934998326b8416f416e8eef1cbf25354a0c5732be4382e0e31b2ce9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1146c17414cf4287553a531077615d321cfe1a2e16564034e0735c227e0cf630(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca53f69280a26f28633a2fd381f898f590d304e2aeccbdbb7b14674f1ee748f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d196f4eace4fb0169d2aed9df231ee5764d30153e2954127a15ca35b596d451(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    active_directory: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettingsActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_provider: typing.Optional[builtins.str] = None,
    facebook: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettingsFacebook, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettingsGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    google: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettingsGoogle, typing.Dict[builtins.str, typing.Any]]] = None,
    issuer: typing.Optional[builtins.str] = None,
    microsoft: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettingsMicrosoft, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
    token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    twitter: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettingsTwitter, typing.Dict[builtins.str, typing.Any]]] = None,
    unauthenticated_client_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c35a6582acee564757ab4ab195600c41ec98dfa27e90100d2788c131df1ec6(
    *,
    client_id: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f68c644dc88554864f85c8de4b04f2573c6e2014c82bb0356f9b2e1998e294(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6acf79334f259c71f316b28146387e824fe33421aead50813ac2416019a5324f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2794684db621eed7c38d0f91bfda808b86bfc883eab221d95852bef6b20f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b929851d2617e8e2f39bcc9b3fe79afe19441bcb1aba0b05c3e4f313820c4476(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2d2660fec4907beca9d4c3158a818fef96fd083fc20b23347773be33feaf0cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39b2664238fa2eeca906fefc6acff6c59db5f6a2bc51fccab3493d42533a225(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettingsActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1289900f438ffb9e66104647a3de8e3520c44766c1b4ffba9ecaca8f84140d9c(
    *,
    app_id: builtins.str,
    app_secret: typing.Optional[builtins.str] = None,
    app_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81515c1b2694ebfbfab74b1bb7cc05320a59bc0ac6ad278d6dea107d85e7d2d0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753e5e3d4f961b5855588841d9dd3bffa1087f0af9ccbdcc409ed50c2e34bf7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e3faebfa16731ed7930258d9fd39cc6014f68422ebbba87b333debcf0d37f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15284ffa48ed6677fb25f9f76683f793d2e618b5e18240343e8d20e3547ee34a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7913ddd7aabe10e1b51c5828828af1b6775961036a7caf99fd07ba51035278b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa670fc95d68b3aad0e729d7b97a79144af6e6c1fe1ae697a36f6d0d4988f3a(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettingsFacebook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21ca89ddab634ab02ea5bdb73b08a3859463cdad330adc46dee1ec6ec4d90809(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978725dc060f643c22bef640bf5961d106885b7bf8a50578230cc99200aa223c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8309542369ad0da7562100c766c52c701ba3cdacaf78487b5cfd6c7ed15018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272160f17090f860efac27f2f0997ad9d1b4ad08c7d3d2287b9d9dc97b249b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551f312005bdfb243d5d5b5bcb19e6f497e4007ce12b984833fdf5bd67034f37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd4d765c91ecb3c8993777a14cdcbae61cbb2085e62293a61e84329785a54970(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f06a479533af78e8e6e331ab3779ea60d36344cc349541eec5a9b13c041707(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettingsGithub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363e749442e06f52ceb1e3cf6fdfe633dd2d012a558e4798896836ab0bfe3e2e(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76715d1d8b28499c0478d4e86a7967da82e0a8b602f8d39b1e261ca9bcfa388f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4555adfb4223f5bbcadabfa35311c32b5a306d2c7ba5c3bb0b2972da5514d046(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b516ade7d7e9bad6d5c104f3e539e6dabb4540cc3d1375f35816c9ca773f5226(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44fc907e3abad123a456069700bd3db0da2c1d7882871a0c5c9c6df5f6b50627(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87e18fa08ce6647bb64a122be805465c74e5e8f54ed969ecbc4bff39c1598f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81cccd1ec4541f4ad5990550f27454e4c4f5a6113cc82cbad115371ad92efb33(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettingsGoogle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d57bae65544d28bc2d5573c0cdb642fbded0c2645db249e511b21da679e5c52(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914b3ab78a6839b31456557b3d4e680e7782ae19a59b56f000a9e1f854d0b8a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be627bb2ecaab104b4b2ffb14f987b5b6dbb9b2aa63adb317b9317bb40c0a97d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55da5db050c65fbdfe2f5caeb25a6dcb284d9124b25ba08891565bcb1808510f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9155d3915a6c06aa3ee1125075f1d33dba7fc7ba9db92a5a9085709210aa84e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57b5b3a534638dbc2934bb29d88cd2e227921595ad9655e10977f6091d60ea7a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702647eef51388977447a1917db6fee4149d978a33227313e4a2d9bce4c81426(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettingsMicrosoft],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ce541b6cf8b403c4bdca320a5774ddef224efa653419142f6f67d7eee746cf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db1de5a520ec484a59c3ef47e8ff1c0ad1b7dc14a4635b69402bdc1e1af39306(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b350d88fb88083c8697f92dff60eb331adcb83bb1e1fcb79f9a10072883672de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7e4c5fe35c6e26cfea0af0700cab13a9af2e5797b3b94368fd5d33fda0eb48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc9ea0f797d88418f48e9e850f009a9cd9864e8e91d93376e21351289193584(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__159f1b06a5d3b88c619f019a23834aad5af99d928b7649962aca8eb39613b6ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1191ea77b8bd1a7717b2b50c39c4cf3d3f7b076844dedef67474fd1971354b76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146cd834d38edecec0144b447cdd767979c712296bcaff21a11bdfd28d95d52d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fab2b993a87c411a96be333cc3a032f15fdebb65b5d7dab2f20b4cd4766a25(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b65a79f1cf8269443bac55c360aae81b720722a1ca3af57b3e7d808e7a3c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4189fcc10d053ac78659348e173871154f92d1e3749a7c20471de162911fb65(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50fbeae3362683d6e08725689a29c4aa85142d5ec2cb8160e086a0362f79070(
    *,
    consumer_key: builtins.str,
    consumer_secret: typing.Optional[builtins.str] = None,
    consumer_secret_setting_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264402ff1e1f375f4e245c7ba8b7729433582081c19fa29cdd6904b0ca15c1fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f2155f214bb3b5fa2a13bc40ac7c4d5d80c63ada149a0e7b2a0576dc1769ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468b9b4afb4a26d451b8dab70161a54ad37eb297ccc1f7eb3e325df175a94d96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e1f6c6b599d098506cee2c2b322ead4ce73a592cd237c6cbb9e8bb13534890d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1378096ffbe28e92927bf7fff55c1202b0e132f8674502228d3e1deda1ba0c(
    value: typing.Optional[WindowsFunctionAppSlotAuthSettingsTwitter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__613e64716bd39fc025d50ffed1483b8eff0d3a8ceb2159c82e825351159ec45a(
    *,
    name: builtins.str,
    schedule: typing.Union[WindowsFunctionAppSlotBackupSchedule, typing.Dict[builtins.str, typing.Any]],
    storage_account_url: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fc1bbd8a0cd9d42d7caa4c3872006fc90ba8d97aea01e4843b9e75730a86db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2bf4acf9e410db373be974a8ec2dfd15269536f54d34b42daac6a5a075e1049(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd3bda734e67818c282bd38ce1fb34350c59f2ec780e134fd46f20142342f15b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e24e2c402232835f5eeca96adc73180387a1e95fdf21ba3bd0e40654059a5ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47ecb73cf0bdd7ed3b3f8905466bcbab1e1d542dff2f43a335b30e29e5ee84dc(
    value: typing.Optional[WindowsFunctionAppSlotBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c309ca6725e641c7440b943e814df02ef87d04bce4f3d108221e359ad360e24c(
    *,
    frequency_interval: jsii.Number,
    frequency_unit: builtins.str,
    keep_at_least_one_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_period_days: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beafb38377d60d6136acd04d852aa35b077953dd5f6a9347b982501608f7d542(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad56e2f14ff74c90e0959dd64ce13da9b2c132d73c7c2d4a638c71c5b6940d05(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45542d7deed8d87eaddf4b6c0cf0d79d3ec6afc4633b16ea2a16f67b4806b3de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ca699b5abec4bfa4f9e380fd1f3a2bbeb84cb028dcdbb4b0523edccbf4a8ba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7981f54cabe9961a1437b31673df4eca2585d5b8f7bcb557cfb2441a0225b2b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90cb57b0e818595209fd5f8b2b2bcf48b7e73dd95b01277021d28ba293ee975(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aff899b0bc0b846b36a10574aff357c1479ec05f0206357bf00f2f01c08099d(
    value: typing.Optional[WindowsFunctionAppSlotBackupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c5fa036e9ff6c5ef7178e14406dda061b080ad7da90cdbde0849b224fd9042(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_app_id: builtins.str,
    name: builtins.str,
    site_config: typing.Union[WindowsFunctionAppSlotSiteConfig, typing.Dict[builtins.str, typing.Any]],
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[WindowsFunctionAppSlotAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    backup: typing.Optional[typing.Union[WindowsFunctionAppSlotBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotConnectionString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    daily_memory_time_quota: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    functions_extension_version: typing.Optional[builtins.str] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[WindowsFunctionAppSlotIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_account_name: typing.Optional[builtins.str] = None,
    storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
    storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[WindowsFunctionAppSlotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b0b57adee72d12515e8851149d3cbb675e271b7986d608723b01650004a895(
    *,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393a7f5d1d65b2a01d7c983a667e5749f929297b6fab9a77ce0ff46f6142aedd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9d968cd830bd21b265afa717463dd165aeb4f473d57c04c7d42f0f08105a19(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef354a9ec8149703741feacb1a0aac77d1760fc6a2f52e8cc7b85a7ae14d8d22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42138e7d704435529c3e9031ff167869a31063b3411503e10b43e8f590c4d654(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962f38cc77597d8e85ef7df1bac76fabaeb80be746b40154de654cefe97600a4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b51634e37686afbd9199681504559188679feccdbcff619c7bfe2e379719d578(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotConnectionString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a93d77282427c4e959296009a8c20ddfcb9a556d20f1c554d31ebd4635088bb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0016ff2c09bf10e4d3777161855ce6c272a2eea76fd5237b33bad4d494905ba9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34df858a250769032142534a04999ac79dbe3436884bd558f2e8f971419db698(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438432602cdda20616a06d6616e932faff2b88648b05a6809e286ffec3fe05f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db8e44fa8162123117a9ddec829edf94853e9b971e92db4ddefedaaaf7bb501(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotConnectionString, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dc7437adf58ca06a7788f9a53c96974a9463497b11c17376750171d628b63a(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40a5a7299e61802620de312d68a7cf99b4715acc5d4723021f938357d0feee5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1266c821ef7b0c6cdcd692f182eccd12e27e3fee909384fb8c1ceb5a3610a1f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5922d54ddf858303e1735d48c5afc86ca0a4a506898f673e377159e85900a41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5e1941f56220ec7c6ce4cda16b07a87427e29b5f4e44a7bfd916b4bc0e937c(
    value: typing.Optional[WindowsFunctionAppSlotIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff650030a5bac5089174ff3c257ac53eecdf890c424958eaac22eca45ef1571(
    *,
    always_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    api_definition_url: typing.Optional[builtins.str] = None,
    api_management_api_id: typing.Optional[builtins.str] = None,
    app_command_line: typing.Optional[builtins.str] = None,
    application_insights_connection_string: typing.Optional[builtins.str] = None,
    application_insights_key: typing.Optional[builtins.str] = None,
    application_stack: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigApplicationStack, typing.Dict[builtins.str, typing.Any]]] = None,
    app_scale_limit: typing.Optional[jsii.Number] = None,
    app_service_logs: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigAppServiceLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_swap_slot_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigCors, typing.Dict[builtins.str, typing.Any]]] = None,
    default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
    elastic_instance_minimum: typing.Optional[jsii.Number] = None,
    ftps_state: typing.Optional[builtins.str] = None,
    health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    load_balancing_mode: typing.Optional[builtins.str] = None,
    managed_pipeline_mode: typing.Optional[builtins.str] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    pre_warmed_instance_count: typing.Optional[jsii.Number] = None,
    remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_debugging_version: typing.Optional[builtins.str] = None,
    runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scm_minimum_tls_version: typing.Optional[builtins.str] = None,
    scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    worker_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c18a1f0a4b03c5f48b4d4602d9260e1b72ed3b8ce9a4581b5195b189cc0160(
    *,
    disk_quota_mb: typing.Optional[jsii.Number] = None,
    retention_period_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31818ec29479ff85bd3dc8fbd13b7004e8606e6ba3db82c798854c91bbc1e89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de28fb46061d70f7284e18e05ab0f6ebaa4c688277a69211fd03c3321af47d73(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983fd87c399e2bb3850511525198ae78eae5335dbaf4074447ac77dca2ddc7bb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee79197bea3eb1b461fd19bbf3014b487cf716902d7a4ca41fac48ad9d6d0ef(
    value: typing.Optional[WindowsFunctionAppSlotSiteConfigAppServiceLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa207df7a38aa1058516abed7c9d8f0c6d6cac4fe82895a91dc5f23477fc2def(
    *,
    dotnet_version: typing.Optional[builtins.str] = None,
    java_version: typing.Optional[builtins.str] = None,
    node_version: typing.Optional[builtins.str] = None,
    powershell_core_version: typing.Optional[builtins.str] = None,
    use_custom_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_dotnet_isolated_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0c67dfac743447b06fcf93ce5aaf3b9f16fe763ac955a43ff5b3f24e47b0d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9687531031a91c66d844cdb42e6c40b63409143a708284a7721933b643991de1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eea4cb0e4363a90ab6e9f0f27d25866d20c89e213ba661fcbc8c21244ed560a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c02074d53e0a77ed0f393f03647f752d056cc496efc0bcce1d7842a95be9912b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40104496ecd33dcd5d5987a6bde6454b881490dea5759eb9bcf040ea397aed53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fbabc4ec5541362863116e6b7daabaa2a4fd131bd658a869d5a8327af034a5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0049266c161a9424f5ad49769fcc318f42125a307bc54514abcaa9f9f5c9090e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba26ae2f4e4d0674ff8bc6e5261d1de0971329e49df9838f790f25db82a9ff2e(
    value: typing.Optional[WindowsFunctionAppSlotSiteConfigApplicationStack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59dbca173248ffc01315f9bff5090c598520825e6d01cc8f8e3c9a713e053c22(
    *,
    allowed_origins: typing.Sequence[builtins.str],
    support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0a717a5b43f394d19cc3b53d4cd1088f866b3a126d40341acdaae352c6f26bb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ea4e9fe8731ad108bbc6b639d55585117a10015f4b366b47b3d461e92740ef(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2133fa4008ad47bab96b420983c161e3e4aaf78c1ad40f57f3354d57db95bb4d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f53442c2c2cd6c0889555d46a9d92de6ca035eb78c9f86667665f40f23c54780(
    value: typing.Optional[WindowsFunctionAppSlotSiteConfigCors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e572e318e21d92a649a5620360ffae46f6126d2878f79380dbeaea99cdeefc(
    *,
    action: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_tag: typing.Optional[builtins.str] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ef9f24ff3ed77eff605420a9ecdd7d4950c5ee474bbaec77bee4f2fc3876f3(
    *,
    x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c0e05aec039b7e796e2b08726817dcf59a8c2dbaf1a2a8c97def183ed6a6dc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d04eaad87b5c059978a3d66b5d1ac9103ad709e23636e1bad1412b73b5c77b36(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3bf01583f98ac96d5ffbc212ad1c69cf93606b572e75e8c15405462c3e381db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71da69d859f3b290295ab65d5aa7bc16639392eba7e3d85ca97376f5fb6cb15d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54646e3c153409812d25d0f180e69459d65dd1689dae631dc90846d71c5286a7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767b99a7a96ef9ec847d5073fa4eedf86e6c393b131950d419ca075ebc432a0c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d8d06ffe232d73d565e71e2eb5134b4f72db1051b735da6c15c26317c7b179(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b2d69d138798336cb19825c035c208c9f9fc89dfc245010d1f11b0e6302b40(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f8d3caae689429d638c658c5a0a9c9383b086f38df338c93cb2395b7610c129(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f2fd08623392e47bc03f341746c9c2bee0385f9bda9f712425a396723d55f8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3357fc68561d920a94beb8ede9b2ea4ccca4fa9a126384a7e379d66cef40feea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d992ce419a03af3433645950ee0f2ac2b4fea154c4500722c925453a02d27f(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0523ec722a57ee86ec43dcb217ae3b3066a1922e11fcb8575cdd729dcc0f64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63629fd6ce410a4412c7113770fa241015e428b3647c25b2ee73978e1c2f7c44(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ee268a9d14269cf1128cfcc4df99f54232cce3f657ca665b60d0a87452f857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904c63fb397e4ac2261038941f8c4420ff06f9393daa16030d028bed8639fbcb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368ff38ebe17da6f43cc8dbf4382b003a038fa8464541068ed8662d49793a222(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476c0a76dfc0facfba32cd0a5b884d0265b8a5407d2d6b92a2f29fc8f3084f71(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigIpRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d114bd47cb961027f58da3a995813c46548a6e7711b1b7f27a20578cb9a60091(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__571e497370f11c4b6d1a005e38c558055483c143877317848c780527e9f92877(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26cdd65cfd217a5d7371285262dcaa75fe4521e7d2bbf8eafa5dcbbb1065992e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fd4b08f25f00d8779c0f87141f83b105e935f00cb94ff4ed7cc55371eb809e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e72c9c72abc30d420e29e375562fe71bcdd5d77a68152e598df67864cf43ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca17db56b5c7fc83b7f252ca217466215b64977b51ec5ff6a508085e570fd4bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e9801ca72501558bea7ee916b63de4146c18b2c60b4055993d7e5ba38d4b40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a09d145e48d173d56bb6c94ca8ef6b1f4e292db515f8dc6161797fda449abb6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5ff69f385ab9228cb5c4295299e8f78aa1f6929f66ed0322c9ace89c130b95(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06afcbdefa45bc9a469ef899ba45a3d27bf42d0a4791bffd1a0fbba905f7b0b3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1717ea3d8434b5f8e54a5ed4060009f38dc8197feb173a4deceea729d5a0a5bd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82a62d685a224e481f3cbaa4403863c2b31a0ef6167791ef56b40b77e67d993(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1988483a9f1b6337193df93a9f6956d6a357535a57e3116920f252bceba67be5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c2b552ddeec7d96cc7a99db49ab9cae54d5297e51a8a9ecc21cd9edbf12e84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbd545773013a88a0026294167ba5ba893bee3dd1bdfd6f157c44784ca51a0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43f8ccec62f7decbd8c6ffd571035cbe62423407df234fe69ddd90d4f7301a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d22645e093642a55f177f53ec6daac3f8cd7e2693be2e1c3f0bc00b9a4cf30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__709b32c1e4c5a9ac4c6215d71cb63f8b1aa2f916469b8bcb1c1849607ef499df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be632dd815697f569f1345947c48e52b41f8192347758d2d7075516950f1328(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c633a244100554c569faa8810c8289e960f39eb771e3e6d3abbba0b041f684(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de3ece4f86b8db36b4c3beb06c9195cee1e1b0b075fb48a0b574c1a461a07a8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d115df99d9e63a2d839924f02560c5c17743c6392c888b3b29a18eac78ee49(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c0b1f9d7948662fac74cb5ddd2d05775e273da37157e4a260878d0ea8d428c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f712ca88c324de7a0b7818d30654ad10f6435066d24952ea459e77f8d921fdbc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779005e00a5a02deed06dc4985cd4140f81e143f9ef04d771a302961eb328a28(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0113399b0a00125fc0aaa0abffe7237e44ceaa8c1f3b147cf8a68f6a63a7e306(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa2accf36624f0a6234319ac10604f4186d87cd91c98679791ee96380145f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae56c5c5cbf11ff324f5a59782d3d523919bfa831433e864d79426c1ea460c10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a238a144b4d2bfe750e8ba6c3ee72d2131a2a7389dc919b6e1292bfffde7f22c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f4b85cd5984a8c536843875126171a252800f9ec95b2f7bf3def048b2e062a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c4cd195503c64888329de8bbd16bb9abd5142e53c695cc9d62c9e99a34902b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3627598fdaca221fd97337498ed1c436fb8e301f864e434bc44e17aaf0be9257(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec66db54c1c84e81a7597d8bfb66f099e59e6ededb5007e1e8ef71f69814dc17(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24c55219c34daf1e5b750357c0cdcd9317488255501b4de4989d98b8067a1df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74927308f83ac8b080cfe94924fbaa65f5681b2ad9f1adbf71bb8a9fc3958b02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842168806da6c1e550797ee893342dc05b619025f4c018257248ecc2012e366b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982c9b03850a0d4c7fb906de391cbfaeec78212767dc9f0b0b77cccda21a6527(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6dbc89982bcaa85381a8dad047fa2bb323cade85002a17ecd145264078c17d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c204da4bbee62e7ffdbf7dd8d12fc061c0397876871133cbcbadb26dc6bea2f9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd258d5fdfaa36c959dafaba0c53cddd90f35a4a5e25d7a7b7f0210cdd0ee115(
    value: typing.Optional[WindowsFunctionAppSlotSiteConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de30f100ab4b578db7f7cf411fcc73b4e953be3cefa1508757b70b775c6a4a6e(
    *,
    action: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_tag: typing.Optional[builtins.str] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76386af5f8304950b5c3c1742fbe7148e6fd2573148f1e822d0ad76dc6cc7ae8(
    *,
    x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe25d28f8081b280efb9b0593b75714c2e66ee1158f513366f6ee93d69eecf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400f2f13cc92a61969f186c904f17b2e27a541f8946086e88b450d22952b617d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c199dc7fd43490398a7706a18e83de7db6af0421a294ad7f9c7b33010b245d92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5b4db8963e08361dc7866c2a1050fe516da6248127fac3a31764dff8c72759(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad9e496e84382f6d782d85101a628e402c559b885221aacfe3246793687c5d3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5366d6586e2e44bb492a26d5a69d951c2a9a543aabef56ea6724c40a61bb9a3c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1a5c4fbfdc3a6903d48d868eed9a1423268b8cc78db30a38e7a966582d33ae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8333b21408b1d25a9b33e95b138f48f35b2d5d617ef6f6e130b69a758ec5f731(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0c951388588063fa756ed7975336f281c357a0f04ab71957b161947bce7c56(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfcda6dcbbf32c6e7d02fcb837de1ac8b7b2eff20c9e3a7e5accece09913e2e3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4d173460989d6cfed27a86ecb7bd22509c9a355106fe5bc4653c33905fa645(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72857414c08c778efa516a125ac83e6da8f9b7555c6705ce5d8a9c4f1fcf854d(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecbc14b16cdc1b94a4e14b1e880633da948221d74f2ab8bc08b64baea6b36da7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94049aa70fa1cb18fea31220276705c5e9360ac794bd669794d0eec7dd88762b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d7fe01c9fad431db6aff5a98a96c8ebee46e1680351eea2006d7eac09cd69e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09cce3a71f03866d351d6f0f370cf83e03b8b7e5602bef40837489815bd419a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba6a079bab403151e5475eb14be9fcfca3e3fa6d816ff65cd7e92fa3f47dd82(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9d9288101688644688793094424a5ec47c7bca42e99825852a9c84d2d51914(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotSiteConfigScmIpRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2533ddb5d9803e3c79020e4faf181ef29dbcf1fe70589f8d6cc50b3275f825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedde117906bad2918fd85391f3a25935c48f3c26efc6a6447cd5701b0e48d2f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9de087fd2e681d4f1c13ffae601f51102f25f022745991ed550a63dcd099911f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a997a43671931a65f6b56fdfc1b1548b0224afca8f5b5faa7052168fc253e48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee5871bb41534804bff858250bdf545b96a2c6e8a775e3dc7fe8b0f518b0dd6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8039cd704ba7d74150628d335d344ed1bea03bc62132b3f224ce7efa4ead0da8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9cffb7984ea7bf517fd75a035b7a1eb7da5d5b068c1beadb773f52e0d1df53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b70602ee92d70972b795c943f3115a16427cc8464e39e487465b83f172b1f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d7a7f5674e29ab476a427d4923268aea24701ad5164cbebd46478ed95abb1a(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotSiteConfigScmIpRestriction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb202e9017c09126c89f87af09d0e497938c14a34b2a88f5271aec1bc763f914(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6969540264288c782b803fe755d8ea76beda20e3f3e6778dbc8a6a2926ca78a9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__470aa6d5d056033f165004d850b603d624aef6848a6469e168f39f9977eb8182(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae17ffddff2dbc41ba7a324309cfed6e5cd1c85affdf5483a35bceca003b3ac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd20dc46447f28ea98cb83dac7bbfcd2a436474b962c122c704f5148881f23c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d751b6a4434653b397d5c98a31eb912495f7dc4876aefbacc6d28f12fb0adfd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd7be5fa25b7a5f6460f663920bc9145c0091ac0cd476488bf0b95c1a852dad(
    value: typing.Optional[WindowsFunctionAppSlotSiteCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a029735483c080fd2b28318765557e14141fbe0f23478b53eb297e397094d5(
    *,
    access_key: builtins.str,
    account_name: builtins.str,
    name: builtins.str,
    share_name: builtins.str,
    type: builtins.str,
    mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1073a610b9f5ee2341501b3f4b0547e9b32101dc19eb4dd63c613b92e2ad516(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bfafb10abcd38076d4be7e4c4213d78c82f16e5442e5ce275eb368792e55626(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b40edb8a3489692869f5c1e0b6b77bb1fdfdd0a7f0623c0006413c01c5f48e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25bee84169acd4cfba3a16fb10097d536d4ba3336a2019ab345284367368ffb3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1c50223527708954dc123e597a8e92967cb9c684c43a5bdc02e96e3eca57f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606287685fd7899ac80d687958304be639617ad3e1d63f15f61a5259a94878a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WindowsFunctionAppSlotStorageAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdbd501ca8375ffe2630c0b974fdef410d4553a56635473d9085a7400ad0513(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e0c491d4ad6bc1074f0693df78dd39af2a5b8b81330bf239d2fcebb01083bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7fa46f9c4b0c294dd085110b9f4b0fa5983afcd922a8a8e1e039167ef68fd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73ad9a4820403e424f0dbb5f5d0198a0eb4eb7048c545c789fa81f52665084a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb3e08948a0cfb630c74cf0466104ea4ae71eba3c0be7eb1ff239ed36d9f1a4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7b17b36145f89792c1cf686f622b960794f8a63a615830827a55de504ab954(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a1695519412b353048910d7f9aa4e2d244e650dc243b15d53b14f420f25e20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5b5ac6512c731f41c4f81858ae8f01e28f5ae2c805df56506ebe556749884d(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotStorageAccount, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0227ccb1d906e1bbf8abed87d31ad8731571d9c01e6e79e544d537930f81e66(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f43442944d9a8ea03be70eecaaa49eef858e0f1fb5beb46d122f750f3498a5c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff054763a63334715d3158293ec3b0f6c3b4a518622b1f96d03d4a18e3a4b438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__750e1f40a8483e2156aba285db6f0ad2c2715e225974d756177c1ee4606a11d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c616b404183cc0cafb1b68f1af22755c004290e85280c67510747628fbf0d2ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d09ae63f1e845ebdaa5f37ce4b7dc6a86b2920f040f52e51f0a6af2d0a9430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd94d47c1e6d6110afb53e93c5145250286eb91990a647c0d4a3719bdaefee51(
    value: typing.Optional[typing.Union[WindowsFunctionAppSlotTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
