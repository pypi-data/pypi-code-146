'''
# `data_azurerm_linux_function_app`

Refer to the Terraform Registory for docs: [`data_azurerm_linux_function_app`](https://www.terraform.io/docs/providers/azurerm/d/linux_function_app).
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


class DataAzurermLinuxFunctionApp(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionApp",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app azurerm_linux_function_app}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzurermLinuxFunctionAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app azurerm_linux_function_app} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#name DataAzurermLinuxFunctionApp#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#resource_group_name DataAzurermLinuxFunctionApp#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#id DataAzurermLinuxFunctionApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#timeouts DataAzurermLinuxFunctionApp#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faf10b5ea115baaec813908cd3b74d485f5aa67802df090497663dbf62e44bc8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAzurermLinuxFunctionAppConfig(
            name=name,
            resource_group_name=resource_group_name,
            id=id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#read DataAzurermLinuxFunctionApp#read}.
        '''
        value = DataAzurermLinuxFunctionAppTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="appSettings")
    def app_settings(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "appSettings"))

    @builtins.property
    @jsii.member(jsii_name="authSettings")
    def auth_settings(self) -> "DataAzurermLinuxFunctionAppAuthSettingsList":
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsList", jsii.get(self, "authSettings"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> "DataAzurermLinuxFunctionAppBackupList":
        return typing.cast("DataAzurermLinuxFunctionAppBackupList", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="builtinLoggingEnabled")
    def builtin_logging_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "builtinLoggingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabled")
    def client_certificate_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "clientCertificateEnabled"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateExclusionPaths")
    def client_certificate_exclusion_paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateExclusionPaths"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateMode")
    def client_certificate_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateMode"))

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> "DataAzurermLinuxFunctionAppConnectionStringList":
        return typing.cast("DataAzurermLinuxFunctionAppConnectionStringList", jsii.get(self, "connectionString"))

    @builtins.property
    @jsii.member(jsii_name="contentShareForceDisabled")
    def content_share_force_disabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "contentShareForceDisabled"))

    @builtins.property
    @jsii.member(jsii_name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomainVerificationId"))

    @builtins.property
    @jsii.member(jsii_name="dailyMemoryTimeQuota")
    def daily_memory_time_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dailyMemoryTimeQuota"))

    @builtins.property
    @jsii.member(jsii_name="defaultHostname")
    def default_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultHostname"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="functionsExtensionVersion")
    def functions_extension_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionsExtensionVersion"))

    @builtins.property
    @jsii.member(jsii_name="httpsOnly")
    def https_only(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "httpsOnly"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "DataAzurermLinuxFunctionAppIdentityList":
        return typing.cast("DataAzurermLinuxFunctionAppIdentityList", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

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
    @jsii.member(jsii_name="servicePlanId")
    def service_plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePlanId"))

    @builtins.property
    @jsii.member(jsii_name="siteConfig")
    def site_config(self) -> "DataAzurermLinuxFunctionAppSiteConfigList":
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigList", jsii.get(self, "siteConfig"))

    @builtins.property
    @jsii.member(jsii_name="siteCredential")
    def site_credential(self) -> "DataAzurermLinuxFunctionAppSiteCredentialList":
        return typing.cast("DataAzurermLinuxFunctionAppSiteCredentialList", jsii.get(self, "siteCredential"))

    @builtins.property
    @jsii.member(jsii_name="stickySettings")
    def sticky_settings(self) -> "DataAzurermLinuxFunctionAppStickySettingsList":
        return typing.cast("DataAzurermLinuxFunctionAppStickySettingsList", jsii.get(self, "stickySettings"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyVaultSecretId")
    def storage_key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKeyVaultSecretId"))

    @builtins.property
    @jsii.member(jsii_name="storageUsesManagedIdentity")
    def storage_uses_managed_identity(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "storageUsesManagedIdentity"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataAzurermLinuxFunctionAppTimeoutsOutputReference":
        return typing.cast("DataAzurermLinuxFunctionAppTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataAzurermLinuxFunctionAppTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataAzurermLinuxFunctionAppTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d356341de135c93cff2b86082274c3f1a16abc7ecc112f4e77d2a454e9df00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667546a2d7c71390f3780baaa1236c09466cd0279b509018a86c0add40907331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6659b8435e1ed72569e1a89f282a053f713e6cd79128702e1074d836763449c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf22ba6aed51fd4375d994246b09d5dcd29d7e1b5a41c2d1dd4d261f1cc0c719)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66f66d6f738c4bd805b0cb1f70706c97f01872450505ea71053f2a9f8ecd7ee)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab6a6b4b68e7356095929844755b7315482b8e4f6d7d39c48ff7a48e1d39a6f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55b244abad3aabf2a673f3118d9cebcbfdbc4989c6512809c2fb44081d8f48a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e45235b42005a99422602de5dd8499aeda2a73c84695c7cd7e42d08c13f47e5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__385b5c104d48331d29dbe3f6485ef35b26102fe70d45661b50f7b2c57fefce3c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6e928afa0d262f88a97b350435b9039afaa65e48971ed5048346839a080debe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsFacebook",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettingsFacebook:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettingsFacebook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppAuthSettingsFacebookList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsFacebookList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__017623997755dd1dbd390e2f4b53af247518017163a6a90e2eeb0ff429872145)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsFacebookOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641fee60c01d75145d735127a2ecc167e0121bbba43258a40fd681a6598ac223)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsFacebookOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94034d084e6a548c005aa216b8e9454b085a67543870a918c7ef88301afe89fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__471efc7b51475d3ffcf1c9d21ae44565e4fd44bd9276b560ccc2636af34cd2bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c5a9ed3c17c742baadfd044a06498385b5839d92aeb160cc70ce49a88419bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppAuthSettingsFacebookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsFacebookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97cb8d1b237d21ac3c46fd646c70ab948e158dbe61f4fc98d5c29930d9c6c997)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @builtins.property
    @jsii.member(jsii_name="appSecret")
    def app_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecret"))

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingName")
    def app_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsFacebook]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsFacebook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsFacebook],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f44aee60daa35df532f2d715c030530844e686e9fe9cc676d307528dab5308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsGithub",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettingsGithub:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettingsGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppAuthSettingsGithubList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsGithubList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6abb93c05341dfa5466d0e70fc028cd961b6130d17f2e3fd734d8c0b5a044013)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsGithubOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02129fdb09d35f609593b742dd38ad8625bbd1d659d0ef6ba918de2fdbfbffea)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsGithubOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04837a4ff1a32fafaaa6a97552e8a3d685cd435cc3a150f360beabc19cc850c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__063219655875e4f7b62e6b052d4a7abab209620644d81f14fa8ed53a70532540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba360166ca8cf4ce4622b1b9bb0d0b6e7e060fbd8a943050d5d2ff64b12969bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppAuthSettingsGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86a445646c6bf64caa5df5c35ae1ce969dc64bd44056e6533563b2d74d9f56b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGithub]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGithub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGithub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d90c31c84524f1504f87a5e66aafef464920f35d95519da54730f8ffaf3bc03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsGoogle",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettingsGoogle:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettingsGoogle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppAuthSettingsGoogleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsGoogleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__775c1e090be8c646ccc28526514e19d35719b1a0fa2324aa94c933d064e40dc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsGoogleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efdc52033f6257526010a9c453bcbbd7779fb3ea43c29eff6c6b85e5f6000e29)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsGoogleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eed7b9dc365b3786c608707d3af1c61f4bdea75773ef7501ef0d3adaa3bed75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc8770a5fe7a598c627af7982003887638c62835062a3388d11378e2c75c5acf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__83fba49ff01bd8450f59fc5343b3f74e1969a5b0247f6e00b937877a78fe774f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppAuthSettingsGoogleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsGoogleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e629832e81a1d1fa6b0a534cebd8dca7cff86a34a79e78d01e9f921be36db7b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGoogle]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGoogle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGoogle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5300a5e96371e664d2a8e0376a8831a8d6780e47e653717b3acfc34989363401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAzurermLinuxFunctionAppAuthSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__101f2a411532ff5d2164267cabcb196c3448a7a582eca75c035215b60308d1e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c83406e8ae4c6a85cec87d31881bd8acd1b05a267f476e992afdd37b89e8df28)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03a0196773217ca09163676cc67edbf6b9168dd4ebd31ced32c49030583770b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5947fdd19a6e2949a1811525936be679419934abedaad13269ca0c4a12b86a77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b6b4f4dd72bc9cedb8bb48038771ba9e3a820aa5749b3e80f2ed1e519e5b6de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsMicrosoft",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettingsMicrosoft:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettingsMicrosoft(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppAuthSettingsMicrosoftList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsMicrosoftList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__901502a1ff9f19363662f2c952a3b56d1a4b29cd991f7e4bcf401367fa91f9fb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsMicrosoftOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fce6b771da64f6fb9e3102d78f52ff15aaa5170c51fd47f08d1a27349ac56a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsMicrosoftOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b8d663649a4a9b7ee98544bdad2bb1834675a2ccfb0803b130191a4a1ac387)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46788429a944647350dd2b0166d5b6fa0b834ed58dad26047d9cf496a4dc0e07)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dadceb7e28c3160faeb71e5c4aec1c40c10213ba2262496d4688ee595c363965)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppAuthSettingsMicrosoftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsMicrosoftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c07526759289687868234fcabcb055cca28268a3861d782635b7cbf2b71796a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsMicrosoft], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsMicrosoft],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b125dbc834e949323abb9d04c157e20875057083f086777f94b8d63766fd7587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAzurermLinuxFunctionAppAuthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d831f291ee5c270cc7c95c9227de0191c2f8e044963eba411a20e435ff82cc06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(
        self,
    ) -> DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryList:
        return typing.cast(DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryList, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="additionalLoginParameters")
    def additional_login_parameters(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "additionalLoginParameters"))

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrls")
    def allowed_external_redirect_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedExternalRedirectUrls"))

    @builtins.property
    @jsii.member(jsii_name="defaultProvider")
    def default_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProvider"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="facebook")
    def facebook(self) -> DataAzurermLinuxFunctionAppAuthSettingsFacebookList:
        return typing.cast(DataAzurermLinuxFunctionAppAuthSettingsFacebookList, jsii.get(self, "facebook"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> DataAzurermLinuxFunctionAppAuthSettingsGithubList:
        return typing.cast(DataAzurermLinuxFunctionAppAuthSettingsGithubList, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="google")
    def google(self) -> DataAzurermLinuxFunctionAppAuthSettingsGoogleList:
        return typing.cast(DataAzurermLinuxFunctionAppAuthSettingsGoogleList, jsii.get(self, "google"))

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @builtins.property
    @jsii.member(jsii_name="microsoft")
    def microsoft(self) -> DataAzurermLinuxFunctionAppAuthSettingsMicrosoftList:
        return typing.cast(DataAzurermLinuxFunctionAppAuthSettingsMicrosoftList, jsii.get(self, "microsoft"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionHours")
    def token_refresh_extension_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tokenRefreshExtensionHours"))

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabled")
    def token_store_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "tokenStoreEnabled"))

    @builtins.property
    @jsii.member(jsii_name="twitter")
    def twitter(self) -> "DataAzurermLinuxFunctionAppAuthSettingsTwitterList":
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsTwitterList", jsii.get(self, "twitter"))

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedClientAction")
    def unauthenticated_client_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unauthenticatedClientAction"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettings]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6916fd2d1ff8e0add714778779c84f6ecf49f4993e6d24bda76e661122f0f2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsTwitter",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppAuthSettingsTwitter:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppAuthSettingsTwitter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppAuthSettingsTwitterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsTwitterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b251ba2c9466e68ed27add33be0bf44e26310f3b422daae56359c72f81e70ebf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppAuthSettingsTwitterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197a111eed70656667bc96a7b7fd119fc9a2ac23de7cc59273cdf03a45534b72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppAuthSettingsTwitterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00f2094b26231e8d674444e383e4199d59e423ba080bb364f0d6622bf67e325f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fac215c746b1b193fad749fac05df4ae1779783218aa6b253d15091f431c5323)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69d039a994065217a5eac65587ef169671e7578ac72a60e9f2afe77308f76f20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppAuthSettingsTwitterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppAuthSettingsTwitterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea0f0efebf04fd1671388cf7f15ca8662c4adc4ec3863d2ed716087e6fca5f1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="consumerKey")
    def consumer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerKey"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecret")
    def consumer_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecret"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingName")
    def consumer_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsTwitter]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsTwitter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsTwitter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__331ff9d722810d3ad4975cf84d1182c27abc18831f2931f25a461ef5f8eabb78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppBackup",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppBackup:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppBackupList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppBackupList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__47e3e5dfac1b353375e1d30f930356bbb8040bb6da2cda595f40f29c601e83af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppBackupOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7280f26a9c36633beeafc582c9d91f9e36251eb55eef8f1109980ee6ce464062)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppBackupOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7722b3f86e07bf5bc4683feaed56b5238902f63f064101ebefa93c502b2d76e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54981703b11f602d6211e68067907fb2cb97e63c2416aa94d36a93dedced6a3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e1ed0f8b8b03df4050f430f7928ed152445e2c6c215e3c1d3b464f6baf3ec11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppBackupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f28474d2a08757b037de9f6538e9fbcd3931c3d373f64b7d79bbe2096292cb17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "DataAzurermLinuxFunctionAppBackupScheduleList":
        return typing.cast("DataAzurermLinuxFunctionAppBackupScheduleList", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrl")
    def storage_account_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountUrl"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAzurermLinuxFunctionAppBackup]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f7f3b0647dbdff2c5f1c3992ab7dbd5f29f02327e6f951cf28b560264dca9f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppBackupSchedule",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppBackupSchedule:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppBackupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppBackupScheduleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppBackupScheduleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__beff5a8bf63f70243fa4a3d0e4be16c34f31f8f0d97f247d6129ca14b09d2b25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppBackupScheduleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__087e33d16bcbf4813454e8e5968ba63a7d037d453d570fb319d6da22b6f657bd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppBackupScheduleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1261d02c7ef06f9b4eb7e019ce0aa7bcac51354d399c1ca870961a99cf46fa1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4811c6ebff98c5fd30b1edbd4be1d33148dcf7e0ee9b6e3a8553718deee82220)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97a3c802a854d5d29b309d53b7e7c47996808f9124373c9f1e7ad93255f36712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppBackupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppBackupScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca02544039b2682ee1f515b75fcbc45ec766d9a67f76dedeff67e51fcdeca775)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @builtins.property
    @jsii.member(jsii_name="frequencyUnit")
    def frequency_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyUnit"))

    @builtins.property
    @jsii.member(jsii_name="keepAtLeastOneBackup")
    def keep_at_least_one_backup(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "keepAtLeastOneBackup"))

    @builtins.property
    @jsii.member(jsii_name="lastExecutionTime")
    def last_execution_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastExecutionTime"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppBackupSchedule]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppBackupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppBackupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361d41b7fec025105ba7b68d3306ebebc6183abe4ea747675780089c301df67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class DataAzurermLinuxFunctionAppConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        resource_group_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DataAzurermLinuxFunctionAppTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#name DataAzurermLinuxFunctionApp#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#resource_group_name DataAzurermLinuxFunctionApp#resource_group_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#id DataAzurermLinuxFunctionApp#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#timeouts DataAzurermLinuxFunctionApp#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataAzurermLinuxFunctionAppTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf2f72aea53d19eb7ab0850f44cecf3c9900159eac2e674a021c21adb7e80a1a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
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
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#name DataAzurermLinuxFunctionApp#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#resource_group_name DataAzurermLinuxFunctionApp#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#id DataAzurermLinuxFunctionApp#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataAzurermLinuxFunctionAppTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#timeouts DataAzurermLinuxFunctionApp#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataAzurermLinuxFunctionAppTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppConnectionString",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppConnectionString:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppConnectionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppConnectionStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppConnectionStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b660b762a9429da91e070981b1e49eeb8756ca2e93f3f082bfca37980b6c85ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppConnectionStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5686c5096aa8109c75aec2b358a933fd3fb36125f9d36d2007d62064753c9fa1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppConnectionStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4ca35632fa423c60bd490c71449b36ba234428ff8db88b8c2cdf8d5e0bb436)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d4125b94d595adbe56540e9a4e36714757f9fc8a2dcbba9b00ef15cdc35b7de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff9fd1b515385f40a4a5e18290571479589b84ff1284de980b6d1335323d2cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppConnectionStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppConnectionStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06489a8321c6726fe6e3429e44572eefcecf9efbfc4a0ba26e0199694414cbe3)
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
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppConnectionString]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppConnectionString], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppConnectionString],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fb04169c77cfda247cf75019cc9e7344545c19f242db9b8f1692291370d84d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppIdentity",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppIdentity:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppIdentityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppIdentityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c205499fe5ddd9760b9812aecc66411f98a51ad1b58fd4df2ba0b13b50bb218)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppIdentityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3054989c1b93ccdbbce768239097dac84e42237b524d98f318b4cb0b0215466)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppIdentityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c717d2e6a289690e1a0aced25354da6f2fcc59b1411e3e6a9eee093271b82f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0066c17d97447313fa0a60556cdb29c1df140eccc896f85a415e5f9611742b5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95f452567b880f6d487d3605bfd81776ffa2ff18d8e96b188effec3a765df7f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9118292093ebfb650b6ebe20ab7372aed44bd4100b0aee41e4bea677672cd9c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAzurermLinuxFunctionAppIdentity]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a200d0717c3acb45885318ac3190d2f3e57d7960c3c49ac45509bb52152e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2003c3375718ebe5cb931ef9a3a386e09cb6d9ea414daaf8c5a18b88955f7ae8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a08c0beec4b124e56c387e4919e7a055fc714d8c056999a4272c67f39c6999c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a0a015984107e1ec981edddfd053e58e2a11627954aca5b6a79faab9fd01f8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__475b15da23b08d497d5724df97960d8e28469422b55a29a8168da4eda43f6b6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6e87bc041a8520da9f14371398381f6c632da632ced98373aa2764d97161ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b98329dde9116763f57f74236a9d4ac72ed69a7c76fd15da12f61412e518e90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="diskQuotaMb")
    def disk_quota_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskQuotaMb"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37be8e6f0d913c9ce71e240bd81ec8306e4c84d01563979683eb3ba7bdd17d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigApplicationStack",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigApplicationStack:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigApplicationStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8ce978c16e9ac9f41dca654feab57c7ec83fabc90afee4b37e1cc12eccf7550)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abca840d50d4873a18f33b003bec7cf08e67ead0a664f4566da1a8856d67586)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d2ff55bd3094931026ea9f1938e9761d693f24b3bed0fb08db9a5a953f0846)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8437c5b3bb6dc3e8ce59c3617ce65dd76467406f6b63be7d9a5d82f83e51a3b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d89610a137db1261c0e78682ad265327afb0866df6489d40af54373f068c8ad3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d442a46aae4ddb0c51989ac512a82c0a83c020fa4c6709f941b08a263da0549)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @builtins.property
    @jsii.member(jsii_name="registryPassword")
    def registry_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryPassword"))

    @builtins.property
    @jsii.member(jsii_name="registryUrl")
    def registry_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUrl"))

    @builtins.property
    @jsii.member(jsii_name="registryUsername")
    def registry_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUsername"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd276aebd06e636f8dc765382365b201b201ab823cd08b2676e8b70c7a4678f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAzurermLinuxFunctionAppSiteConfigApplicationStackList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigApplicationStackList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3b7b861489b7f70289a1fd18892173ef83b900817dc883e3ff0aea8f9521f9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigApplicationStackOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64e784192794acec73b5cfaf0e5600787a4ab6ed6b93b6b3eff0f9c34cd69ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigApplicationStackOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d2cb230d8446cce509c7b91a0a2f77727030f4a7c4857e604dc7309f9876f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87b0625c7ee45213b8c32a70fab76a51233d50f56da59b260a60b0e4a4a51b7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cd35b1ce4daf606546e0e979a48459de965b0460a2337df7915ca2c7f6ed0f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigApplicationStackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigApplicationStackOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ee03b0eab2f44613fffb95ac371a0697f862b2cd74fb8f59129b064aa6d64c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="docker")
    def docker(self) -> DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerList, jsii.get(self, "docker"))

    @builtins.property
    @jsii.member(jsii_name="dotnetVersion")
    def dotnet_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dotnetVersion"))

    @builtins.property
    @jsii.member(jsii_name="javaVersion")
    def java_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "javaVersion"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def node_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="powershellCoreVersion")
    def powershell_core_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "powershellCoreVersion"))

    @builtins.property
    @jsii.member(jsii_name="pythonVersion")
    def python_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonVersion"))

    @builtins.property
    @jsii.member(jsii_name="useCustomRuntime")
    def use_custom_runtime(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "useCustomRuntime"))

    @builtins.property
    @jsii.member(jsii_name="useDotnetIsolatedRuntime")
    def use_dotnet_isolated_runtime(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "useDotnetIsolatedRuntime"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStack]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e488537ea917d09af2372d45e446a18777d6a8f36987e4454df2359567839cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigCors",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigCors:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppSiteConfigCorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigCorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b77f1637eec7aa1864d16245bcec8da591b9958c8f02ffd478b2af0528464fad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigCorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e34944a68b96fe2612a46eebf7c26ceed05288542f458a7b2209da1a273611fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigCorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71740fbdb9e98d33e3d1efedd37643c4ad63d4bdbad8f1057d8c7ad8770f635)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1763b975d99737d943e968f541a7e1fd6b8a7d4c44e00d55164a4d4df1142918)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d855129ca2d91acb9dddfdb7139a8b2290a6d915a9ff1f42cf7593e7476c099e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigCorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f26bc50e30caf87085c1c98d986d403dd908b6d0b1fa6dcb198e6f26b7cc1221)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @builtins.property
    @jsii.member(jsii_name="supportCredentials")
    def support_credentials(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "supportCredentials"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigCors]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigCors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigCors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27451eb74ea1644d486ed1632852fede0b4d4dc1fd27a40e54a0f2d45bed93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigIpRestriction",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigIpRestriction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53bd7c72915eae77802fe1f67093945c9028ade848d107c05c145cb8124686b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f563217efcad5f6e67fcd41feb1f6419b4021c96d28c5ab6711a7a37731901a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__883e365ba1435ba7ffdde79bb5bd53d6a4f66608f08efb7a3a1661fae8b1b255)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0ec74f406779c17dafd9ead6450960eac23861be833872fbecb1a0f68b02e01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b8c7d2b5f254eb88735e430d1b57ac0eacfd958fe912e7807d75e59f61d06e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edba2b4a1c43f6092e8a27478ec3f67ca644ff0a1f021586f7eb93c20afcd798)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="xAzureFdid")
    def x_azure_fdid(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xAzureFdid"))

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345cb339cecf26aa06b66730686bcb493fadb3a717f29c647ca6ef347b8f4961)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAzurermLinuxFunctionAppSiteConfigIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigIpRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c46d4effe25dd7f5d0ab2b31d4856fb4d5924e286afbcbe805b341bfacc4612f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77542958046d0f125e11f618bb9d4e678e93725fca00a9fbf690913b959090f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b33a39f352339e44dd1e479f82aef79a12ffdfd403bc434078a9d34e51fdfa7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87e5aefe58e706f99472c6a241c2dd35f77334e1f18e45af4f7224baa22ed3aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__176e37a7c496b0e5df54255b91cb81a7da6901d4381a22d54533950a97fc7689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigIpRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7c4a3ef98e8c04195e65a529ad7b961d1a9db8caef9cfb572aa20a2c49a8367)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestriction]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestriction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestriction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb704233abef4d0a09521fb9a6ca8cba64ebded668bdfdb49c09145ab9bdaa5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAzurermLinuxFunctionAppSiteConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ccc7d4d74cf5e04fc2f4d3314ea3ea53074b5ff4b7755d7806cfd594a709ca4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e87fc2ef65eea88dbe457b900f26c7e9e3733fdffa1c15dbb67503cacf7f1e2e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a9050abeb10fe3a4448ec93a605e51996a47728efa6c637b93c155af3a1ac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__edaf4c96679e36163d6a7b9fdc89998cd127cdf3c95d272c1a3d69914b6de165)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28bf25a12b4c83aa13490e73050a06a3e3b2aaa451c30b8a96c10e9c63e232c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19bd7ff59554201e42c4dd0e84379a2fe0bab867b70449d64868390c14c73e57)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="alwaysOn")
    def always_on(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "alwaysOn"))

    @builtins.property
    @jsii.member(jsii_name="apiDefinitionUrl")
    def api_definition_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiDefinitionUrl"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementApiId")
    def api_management_api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementApiId"))

    @builtins.property
    @jsii.member(jsii_name="appCommandLine")
    def app_command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appCommandLine"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsConnectionString")
    def application_insights_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsKey")
    def application_insights_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsKey"))

    @builtins.property
    @jsii.member(jsii_name="applicationStack")
    def application_stack(
        self,
    ) -> DataAzurermLinuxFunctionAppSiteConfigApplicationStackList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigApplicationStackList, jsii.get(self, "applicationStack"))

    @builtins.property
    @jsii.member(jsii_name="appScaleLimit")
    def app_scale_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appScaleLimit"))

    @builtins.property
    @jsii.member(jsii_name="appServiceLogs")
    def app_service_logs(
        self,
    ) -> DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsList, jsii.get(self, "appServiceLogs"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryManagedIdentityClientId")
    def container_registry_managed_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryManagedIdentityClientId"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryUseManagedIdentity")
    def container_registry_use_managed_identity(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "containerRegistryUseManagedIdentity"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> DataAzurermLinuxFunctionAppSiteConfigCorsList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigCorsList, jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="defaultDocuments")
    def default_documents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultDocuments"))

    @builtins.property
    @jsii.member(jsii_name="detailedErrorLoggingEnabled")
    def detailed_error_logging_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "detailedErrorLoggingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimum")
    def elastic_instance_minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticInstanceMinimum"))

    @builtins.property
    @jsii.member(jsii_name="ftpsState")
    def ftps_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ftpsState"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckEvictionTimeInMin")
    def health_check_eviction_time_in_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckEvictionTimeInMin"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckPath"))

    @builtins.property
    @jsii.member(jsii_name="http2Enabled")
    def http2_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "http2Enabled"))

    @builtins.property
    @jsii.member(jsii_name="ipRestriction")
    def ip_restriction(self) -> DataAzurermLinuxFunctionAppSiteConfigIpRestrictionList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigIpRestrictionList, jsii.get(self, "ipRestriction"))

    @builtins.property
    @jsii.member(jsii_name="linuxFxVersion")
    def linux_fx_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linuxFxVersion"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingMode")
    def load_balancing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingMode"))

    @builtins.property
    @jsii.member(jsii_name="managedPipelineMode")
    def managed_pipeline_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedPipelineMode"))

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersion")
    def minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumTlsVersion"))

    @builtins.property
    @jsii.member(jsii_name="preWarmedInstanceCount")
    def pre_warmed_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preWarmedInstanceCount"))

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingEnabled")
    def remote_debugging_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "remoteDebuggingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingVersion")
    def remote_debugging_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteDebuggingVersion"))

    @builtins.property
    @jsii.member(jsii_name="runtimeScaleMonitoringEnabled")
    def runtime_scale_monitoring_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "runtimeScaleMonitoringEnabled"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestriction")
    def scm_ip_restriction(
        self,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionList":
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionList", jsii.get(self, "scmIpRestriction"))

    @builtins.property
    @jsii.member(jsii_name="scmMinimumTlsVersion")
    def scm_minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmMinimumTlsVersion"))

    @builtins.property
    @jsii.member(jsii_name="scmType")
    def scm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmType"))

    @builtins.property
    @jsii.member(jsii_name="scmUseMainIpRestriction")
    def scm_use_main_ip_restriction(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "scmUseMainIpRestriction"))

    @builtins.property
    @jsii.member(jsii_name="use32BitWorker")
    def use32_bit_worker(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "use32BitWorker"))

    @builtins.property
    @jsii.member(jsii_name="vnetRouteAllEnabled")
    def vnet_route_all_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "vnetRouteAllEnabled"))

    @builtins.property
    @jsii.member(jsii_name="websocketsEnabled")
    def websockets_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "websocketsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfig]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcf6ae8fb21aa193a1b5ccfee0efab466ab74b4deedea8eeaadfb05e4fcf25ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8de5d901ebb9b67e7ad49db512652fc66449b858c8f6a95e80227f0f7b605ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf06ec02a3bb67a1ba2d9fd9ef6374e8e7ae8ca9243bc147763cd71ffe7a25bb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84dd563202c7bb26a29708c94fa208a97f6a1f1762d3fdb8fae048eeaed81c73)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0839eaaa1a19bae2a28540ff2368fe6fea63c8ff02961920b53e706faad2e8c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f070637ea27aa8b38b25ebaf2b58a67bedd7c719d856e837c6b07ca6f7f6c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19bf58d98115dd0830d710049c6c19bd57ffe55a2e9521b963e349e07dc942f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="xAzureFdid")
    def x_azure_fdid(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xAzureFdid"))

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c806fe274a613878feacf26cf2f6f920edb8374b5b35f989e8c2fd782820525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e908f98e0eb7d31b7f5dbddbac801183c6dbf92f8b3e635661421828a898536)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1fced52063f363db0f33cc937d81859960e651c3a3cfc3eafb8e02ece48f90b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d2f6031ebac97a1a6b68566d6e8acf1bbc7621ac0165156a9d73decb5e7e36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80db56982250ee2be25ea72fa1feddfec5f428deeda22a88dd88334caf5a1189)
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
            type_hints = typing.get_type_hints(_typecheckingstub__caeb5b2fa28606d5db2caf57d8ee155fdf1cc3269513a13c5276bcbaaef0460f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ea6a7bc7eb9ab9f2a567ce6a3e41074d27e5f25eaf426393b26668e6f00798b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(
        self,
    ) -> DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersList:
        return typing.cast(DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23a1040f58507c8175f040842bf7985e919daa2da48634b4d6d24b642c104d10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteCredential",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppSiteCredential:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppSiteCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppSiteCredentialList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteCredentialList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02a9d567d17b6932c4c1c5f5efee5cbdc02a112327f8297b6cd192a1f0264d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppSiteCredentialOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e652301a6cd386e2b9b5073d4e21f54afd2f786fe8de905beda593fbbb3d4e7c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppSiteCredentialOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292d99f9f3fdb019363d9a793b9d9ffba65b1389fbfc5831836cd578258214f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06b3fdc1a0e17ec4c312a5341dbdcd96f0c5e67d09ed46f9e376c711a2017c41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__291049ee84eef11a825d72422832fe73e1046680f10ae18d92b4e674df86c281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppSiteCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppSiteCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__34c6238c363d1709a451922ab74a6daf6476920014fb28f600c56416ab54b0eb)
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
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppSiteCredential]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppSiteCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppSiteCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbae116d4beb63073f7f42990a62f23cf2a2a13813cdf1466b0b846186b11b92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppStickySettings",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAzurermLinuxFunctionAppStickySettings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppStickySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppStickySettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppStickySettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d151ff98785aa58c53f1c8b7a8650c35b7f75373803dccc13c67632fccf7da97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAzurermLinuxFunctionAppStickySettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03cfbb15394993c88096d84f18ee484eed1765a0e54136b3fa0287919588c39a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAzurermLinuxFunctionAppStickySettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be568f39ce9cede340dc18cad1a360b12c2a26463f2e62773900ad678610786e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfe1b9d6c69985e9881a90642e13982292fdb36cef3d3fe8b43dea2cbf4ac4d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20bc418286a7cbe55b2afe03700fead41c034d4d393ed56623157429a4acf0a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAzurermLinuxFunctionAppStickySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppStickySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ff1b6752917922d2fd9d68198deea80c3546bf6398860ea485623963c8d9e72)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="appSettingNames")
    def app_setting_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "appSettingNames"))

    @builtins.property
    @jsii.member(jsii_name="connectionStringNames")
    def connection_string_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connectionStringNames"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAzurermLinuxFunctionAppStickySettings]:
        return typing.cast(typing.Optional[DataAzurermLinuxFunctionAppStickySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAzurermLinuxFunctionAppStickySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b77eece2a7da0117ab148b2c0d4ce38a4e00e7eb81a226318acae388a36cfe10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class DataAzurermLinuxFunctionAppTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#read DataAzurermLinuxFunctionApp#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a1dc70f10be2d1ee1a506a65a2dfdc2e1213bf936344b0bb9b1a2a765a07e0b)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/d/linux_function_app#read DataAzurermLinuxFunctionApp#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAzurermLinuxFunctionAppTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAzurermLinuxFunctionAppTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dataAzurermLinuxFunctionApp.DataAzurermLinuxFunctionAppTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29a58a0567af37f3de8caecd716e5bd8f3b9e8962e16a97241c07930983f4d97)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902617243ff7526c8f2dcc9aa15d00aac7d724fede844ef4c4c2f7527568182f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAzurermLinuxFunctionAppTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAzurermLinuxFunctionAppTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAzurermLinuxFunctionAppTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545562f1f4af6b90573ad8b85c08d6f4922da319cea44873185cf0b9f1ba9d83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataAzurermLinuxFunctionApp",
    "DataAzurermLinuxFunctionAppAuthSettings",
    "DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory",
    "DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryList",
    "DataAzurermLinuxFunctionAppAuthSettingsActiveDirectoryOutputReference",
    "DataAzurermLinuxFunctionAppAuthSettingsFacebook",
    "DataAzurermLinuxFunctionAppAuthSettingsFacebookList",
    "DataAzurermLinuxFunctionAppAuthSettingsFacebookOutputReference",
    "DataAzurermLinuxFunctionAppAuthSettingsGithub",
    "DataAzurermLinuxFunctionAppAuthSettingsGithubList",
    "DataAzurermLinuxFunctionAppAuthSettingsGithubOutputReference",
    "DataAzurermLinuxFunctionAppAuthSettingsGoogle",
    "DataAzurermLinuxFunctionAppAuthSettingsGoogleList",
    "DataAzurermLinuxFunctionAppAuthSettingsGoogleOutputReference",
    "DataAzurermLinuxFunctionAppAuthSettingsList",
    "DataAzurermLinuxFunctionAppAuthSettingsMicrosoft",
    "DataAzurermLinuxFunctionAppAuthSettingsMicrosoftList",
    "DataAzurermLinuxFunctionAppAuthSettingsMicrosoftOutputReference",
    "DataAzurermLinuxFunctionAppAuthSettingsOutputReference",
    "DataAzurermLinuxFunctionAppAuthSettingsTwitter",
    "DataAzurermLinuxFunctionAppAuthSettingsTwitterList",
    "DataAzurermLinuxFunctionAppAuthSettingsTwitterOutputReference",
    "DataAzurermLinuxFunctionAppBackup",
    "DataAzurermLinuxFunctionAppBackupList",
    "DataAzurermLinuxFunctionAppBackupOutputReference",
    "DataAzurermLinuxFunctionAppBackupSchedule",
    "DataAzurermLinuxFunctionAppBackupScheduleList",
    "DataAzurermLinuxFunctionAppBackupScheduleOutputReference",
    "DataAzurermLinuxFunctionAppConfig",
    "DataAzurermLinuxFunctionAppConnectionString",
    "DataAzurermLinuxFunctionAppConnectionStringList",
    "DataAzurermLinuxFunctionAppConnectionStringOutputReference",
    "DataAzurermLinuxFunctionAppIdentity",
    "DataAzurermLinuxFunctionAppIdentityList",
    "DataAzurermLinuxFunctionAppIdentityOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfig",
    "DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs",
    "DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsList",
    "DataAzurermLinuxFunctionAppSiteConfigAppServiceLogsOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigApplicationStack",
    "DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker",
    "DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerList",
    "DataAzurermLinuxFunctionAppSiteConfigApplicationStackDockerOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigApplicationStackList",
    "DataAzurermLinuxFunctionAppSiteConfigApplicationStackOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigCors",
    "DataAzurermLinuxFunctionAppSiteConfigCorsList",
    "DataAzurermLinuxFunctionAppSiteConfigCorsOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigIpRestriction",
    "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders",
    "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersList",
    "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeadersOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionList",
    "DataAzurermLinuxFunctionAppSiteConfigIpRestrictionOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigList",
    "DataAzurermLinuxFunctionAppSiteConfigOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction",
    "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders",
    "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersList",
    "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeadersOutputReference",
    "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionList",
    "DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionOutputReference",
    "DataAzurermLinuxFunctionAppSiteCredential",
    "DataAzurermLinuxFunctionAppSiteCredentialList",
    "DataAzurermLinuxFunctionAppSiteCredentialOutputReference",
    "DataAzurermLinuxFunctionAppStickySettings",
    "DataAzurermLinuxFunctionAppStickySettingsList",
    "DataAzurermLinuxFunctionAppStickySettingsOutputReference",
    "DataAzurermLinuxFunctionAppTimeouts",
    "DataAzurermLinuxFunctionAppTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__faf10b5ea115baaec813908cd3b74d485f5aa67802df090497663dbf62e44bc8(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzurermLinuxFunctionAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b4d356341de135c93cff2b86082274c3f1a16abc7ecc112f4e77d2a454e9df00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667546a2d7c71390f3780baaa1236c09466cd0279b509018a86c0add40907331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6659b8435e1ed72569e1a89f282a053f713e6cd79128702e1074d836763449c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf22ba6aed51fd4375d994246b09d5dcd29d7e1b5a41c2d1dd4d261f1cc0c719(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66f66d6f738c4bd805b0cb1f70706c97f01872450505ea71053f2a9f8ecd7ee(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab6a6b4b68e7356095929844755b7315482b8e4f6d7d39c48ff7a48e1d39a6f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b244abad3aabf2a673f3118d9cebcbfdbc4989c6512809c2fb44081d8f48a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e45235b42005a99422602de5dd8499aeda2a73c84695c7cd7e42d08c13f47e5c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385b5c104d48331d29dbe3f6485ef35b26102fe70d45661b50f7b2c57fefce3c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6e928afa0d262f88a97b350435b9039afaa65e48971ed5048346839a080debe(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__017623997755dd1dbd390e2f4b53af247518017163a6a90e2eeb0ff429872145(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641fee60c01d75145d735127a2ecc167e0121bbba43258a40fd681a6598ac223(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94034d084e6a548c005aa216b8e9454b085a67543870a918c7ef88301afe89fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471efc7b51475d3ffcf1c9d21ae44565e4fd44bd9276b560ccc2636af34cd2bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5a9ed3c17c742baadfd044a06498385b5839d92aeb160cc70ce49a88419bc1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cb8d1b237d21ac3c46fd646c70ab948e158dbe61f4fc98d5c29930d9c6c997(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f44aee60daa35df532f2d715c030530844e686e9fe9cc676d307528dab5308(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsFacebook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abb93c05341dfa5466d0e70fc028cd961b6130d17f2e3fd734d8c0b5a044013(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02129fdb09d35f609593b742dd38ad8625bbd1d659d0ef6ba918de2fdbfbffea(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04837a4ff1a32fafaaa6a97552e8a3d685cd435cc3a150f360beabc19cc850c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063219655875e4f7b62e6b052d4a7abab209620644d81f14fa8ed53a70532540(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba360166ca8cf4ce4622b1b9bb0d0b6e7e060fbd8a943050d5d2ff64b12969bf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a445646c6bf64caa5df5c35ae1ce969dc64bd44056e6533563b2d74d9f56b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d90c31c84524f1504f87a5e66aafef464920f35d95519da54730f8ffaf3bc03(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGithub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775c1e090be8c646ccc28526514e19d35719b1a0fa2324aa94c933d064e40dc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdc52033f6257526010a9c453bcbbd7779fb3ea43c29eff6c6b85e5f6000e29(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eed7b9dc365b3786c608707d3af1c61f4bdea75773ef7501ef0d3adaa3bed75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8770a5fe7a598c627af7982003887638c62835062a3388d11378e2c75c5acf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83fba49ff01bd8450f59fc5343b3f74e1969a5b0247f6e00b937877a78fe774f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e629832e81a1d1fa6b0a534cebd8dca7cff86a34a79e78d01e9f921be36db7b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5300a5e96371e664d2a8e0376a8831a8d6780e47e653717b3acfc34989363401(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsGoogle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101f2a411532ff5d2164267cabcb196c3448a7a582eca75c035215b60308d1e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83406e8ae4c6a85cec87d31881bd8acd1b05a267f476e992afdd37b89e8df28(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03a0196773217ca09163676cc67edbf6b9168dd4ebd31ced32c49030583770b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5947fdd19a6e2949a1811525936be679419934abedaad13269ca0c4a12b86a77(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6b4f4dd72bc9cedb8bb48038771ba9e3a820aa5749b3e80f2ed1e519e5b6de(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901502a1ff9f19363662f2c952a3b56d1a4b29cd991f7e4bcf401367fa91f9fb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fce6b771da64f6fb9e3102d78f52ff15aaa5170c51fd47f08d1a27349ac56a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b8d663649a4a9b7ee98544bdad2bb1834675a2ccfb0803b130191a4a1ac387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46788429a944647350dd2b0166d5b6fa0b834ed58dad26047d9cf496a4dc0e07(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadceb7e28c3160faeb71e5c4aec1c40c10213ba2262496d4688ee595c363965(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c07526759289687868234fcabcb055cca28268a3861d782635b7cbf2b71796a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b125dbc834e949323abb9d04c157e20875057083f086777f94b8d63766fd7587(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsMicrosoft],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d831f291ee5c270cc7c95c9227de0191c2f8e044963eba411a20e435ff82cc06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6916fd2d1ff8e0add714778779c84f6ecf49f4993e6d24bda76e661122f0f2bb(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b251ba2c9466e68ed27add33be0bf44e26310f3b422daae56359c72f81e70ebf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197a111eed70656667bc96a7b7fd119fc9a2ac23de7cc59273cdf03a45534b72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00f2094b26231e8d674444e383e4199d59e423ba080bb364f0d6622bf67e325f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fac215c746b1b193fad749fac05df4ae1779783218aa6b253d15091f431c5323(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69d039a994065217a5eac65587ef169671e7578ac72a60e9f2afe77308f76f20(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0f0efebf04fd1671388cf7f15ca8662c4adc4ec3863d2ed716087e6fca5f1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__331ff9d722810d3ad4975cf84d1182c27abc18831f2931f25a461ef5f8eabb78(
    value: typing.Optional[DataAzurermLinuxFunctionAppAuthSettingsTwitter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e3e5dfac1b353375e1d30f930356bbb8040bb6da2cda595f40f29c601e83af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7280f26a9c36633beeafc582c9d91f9e36251eb55eef8f1109980ee6ce464062(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7722b3f86e07bf5bc4683feaed56b5238902f63f064101ebefa93c502b2d76e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54981703b11f602d6211e68067907fb2cb97e63c2416aa94d36a93dedced6a3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1ed0f8b8b03df4050f430f7928ed152445e2c6c215e3c1d3b464f6baf3ec11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28474d2a08757b037de9f6538e9fbcd3931c3d373f64b7d79bbe2096292cb17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f7f3b0647dbdff2c5f1c3992ab7dbd5f29f02327e6f951cf28b560264dca9f3(
    value: typing.Optional[DataAzurermLinuxFunctionAppBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beff5a8bf63f70243fa4a3d0e4be16c34f31f8f0d97f247d6129ca14b09d2b25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__087e33d16bcbf4813454e8e5968ba63a7d037d453d570fb319d6da22b6f657bd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1261d02c7ef06f9b4eb7e019ce0aa7bcac51354d399c1ca870961a99cf46fa1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4811c6ebff98c5fd30b1edbd4be1d33148dcf7e0ee9b6e3a8553718deee82220(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97a3c802a854d5d29b309d53b7e7c47996808f9124373c9f1e7ad93255f36712(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca02544039b2682ee1f515b75fcbc45ec766d9a67f76dedeff67e51fcdeca775(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361d41b7fec025105ba7b68d3306ebebc6183abe4ea747675780089c301df67a(
    value: typing.Optional[DataAzurermLinuxFunctionAppBackupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf2f72aea53d19eb7ab0850f44cecf3c9900159eac2e674a021c21adb7e80a1a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource_group_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DataAzurermLinuxFunctionAppTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b660b762a9429da91e070981b1e49eeb8756ca2e93f3f082bfca37980b6c85ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5686c5096aa8109c75aec2b358a933fd3fb36125f9d36d2007d62064753c9fa1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4ca35632fa423c60bd490c71449b36ba234428ff8db88b8c2cdf8d5e0bb436(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4125b94d595adbe56540e9a4e36714757f9fc8a2dcbba9b00ef15cdc35b7de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff9fd1b515385f40a4a5e18290571479589b84ff1284de980b6d1335323d2cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06489a8321c6726fe6e3429e44572eefcecf9efbfc4a0ba26e0199694414cbe3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb04169c77cfda247cf75019cc9e7344545c19f242db9b8f1692291370d84d7(
    value: typing.Optional[DataAzurermLinuxFunctionAppConnectionString],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c205499fe5ddd9760b9812aecc66411f98a51ad1b58fd4df2ba0b13b50bb218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3054989c1b93ccdbbce768239097dac84e42237b524d98f318b4cb0b0215466(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c717d2e6a289690e1a0aced25354da6f2fcc59b1411e3e6a9eee093271b82f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0066c17d97447313fa0a60556cdb29c1df140eccc896f85a415e5f9611742b5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f452567b880f6d487d3605bfd81776ffa2ff18d8e96b188effec3a765df7f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9118292093ebfb650b6ebe20ab7372aed44bd4100b0aee41e4bea677672cd9c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a200d0717c3acb45885318ac3190d2f3e57d7960c3c49ac45509bb52152e0d(
    value: typing.Optional[DataAzurermLinuxFunctionAppIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2003c3375718ebe5cb931ef9a3a386e09cb6d9ea414daaf8c5a18b88955f7ae8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a08c0beec4b124e56c387e4919e7a055fc714d8c056999a4272c67f39c6999c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0a015984107e1ec981edddfd053e58e2a11627954aca5b6a79faab9fd01f8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475b15da23b08d497d5724df97960d8e28469422b55a29a8168da4eda43f6b6b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e87bc041a8520da9f14371398381f6c632da632ced98373aa2764d97161ee6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b98329dde9116763f57f74236a9d4ac72ed69a7c76fd15da12f61412e518e90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37be8e6f0d913c9ce71e240bd81ec8306e4c84d01563979683eb3ba7bdd17d0(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigAppServiceLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ce978c16e9ac9f41dca654feab57c7ec83fabc90afee4b37e1cc12eccf7550(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abca840d50d4873a18f33b003bec7cf08e67ead0a664f4566da1a8856d67586(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d2ff55bd3094931026ea9f1938e9761d693f24b3bed0fb08db9a5a953f0846(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8437c5b3bb6dc3e8ce59c3617ce65dd76467406f6b63be7d9a5d82f83e51a3b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d89610a137db1261c0e78682ad265327afb0866df6489d40af54373f068c8ad3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d442a46aae4ddb0c51989ac512a82c0a83c020fa4c6709f941b08a263da0549(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd276aebd06e636f8dc765382365b201b201ab823cd08b2676e8b70c7a4678f(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStackDocker],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b7b861489b7f70289a1fd18892173ef83b900817dc883e3ff0aea8f9521f9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64e784192794acec73b5cfaf0e5600787a4ab6ed6b93b6b3eff0f9c34cd69ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d2cb230d8446cce509c7b91a0a2f77727030f4a7c4857e604dc7309f9876f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b0625c7ee45213b8c32a70fab76a51233d50f56da59b260a60b0e4a4a51b7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd35b1ce4daf606546e0e979a48459de965b0460a2337df7915ca2c7f6ed0f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee03b0eab2f44613fffb95ac371a0697f862b2cd74fb8f59129b064aa6d64c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e488537ea917d09af2372d45e446a18777d6a8f36987e4454df2359567839cd8(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigApplicationStack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77f1637eec7aa1864d16245bcec8da591b9958c8f02ffd478b2af0528464fad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34944a68b96fe2612a46eebf7c26ceed05288542f458a7b2209da1a273611fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71740fbdb9e98d33e3d1efedd37643c4ad63d4bdbad8f1057d8c7ad8770f635(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1763b975d99737d943e968f541a7e1fd6b8a7d4c44e00d55164a4d4df1142918(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d855129ca2d91acb9dddfdb7139a8b2290a6d915a9ff1f42cf7593e7476c099e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26bc50e30caf87085c1c98d986d403dd908b6d0b1fa6dcb198e6f26b7cc1221(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27451eb74ea1644d486ed1632852fede0b4d4dc1fd27a40e54a0f2d45bed93c(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigCors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bd7c72915eae77802fe1f67093945c9028ade848d107c05c145cb8124686b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f563217efcad5f6e67fcd41feb1f6419b4021c96d28c5ab6711a7a37731901a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883e365ba1435ba7ffdde79bb5bd53d6a4f66608f08efb7a3a1661fae8b1b255(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ec74f406779c17dafd9ead6450960eac23861be833872fbecb1a0f68b02e01(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8c7d2b5f254eb88735e430d1b57ac0eacfd958fe912e7807d75e59f61d06e9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edba2b4a1c43f6092e8a27478ec3f67ca644ff0a1f021586f7eb93c20afcd798(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345cb339cecf26aa06b66730686bcb493fadb3a717f29c647ca6ef347b8f4961(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestrictionHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46d4effe25dd7f5d0ab2b31d4856fb4d5924e286afbcbe805b341bfacc4612f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77542958046d0f125e11f618bb9d4e678e93725fca00a9fbf690913b959090f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33a39f352339e44dd1e479f82aef79a12ffdfd403bc434078a9d34e51fdfa7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e5aefe58e706f99472c6a241c2dd35f77334e1f18e45af4f7224baa22ed3aa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__176e37a7c496b0e5df54255b91cb81a7da6901d4381a22d54533950a97fc7689(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c4a3ef98e8c04195e65a529ad7b961d1a9db8caef9cfb572aa20a2c49a8367(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb704233abef4d0a09521fb9a6ca8cba64ebded668bdfdb49c09145ab9bdaa5c(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigIpRestriction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ccc7d4d74cf5e04fc2f4d3314ea3ea53074b5ff4b7755d7806cfd594a709ca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e87fc2ef65eea88dbe457b900f26c7e9e3733fdffa1c15dbb67503cacf7f1e2e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a9050abeb10fe3a4448ec93a605e51996a47728efa6c637b93c155af3a1ac8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edaf4c96679e36163d6a7b9fdc89998cd127cdf3c95d272c1a3d69914b6de165(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28bf25a12b4c83aa13490e73050a06a3e3b2aaa451c30b8a96c10e9c63e232c0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bd7ff59554201e42c4dd0e84379a2fe0bab867b70449d64868390c14c73e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf6ae8fb21aa193a1b5ccfee0efab466ab74b4deedea8eeaadfb05e4fcf25ff(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8de5d901ebb9b67e7ad49db512652fc66449b858c8f6a95e80227f0f7b605ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf06ec02a3bb67a1ba2d9fd9ef6374e8e7ae8ca9243bc147763cd71ffe7a25bb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84dd563202c7bb26a29708c94fa208a97f6a1f1762d3fdb8fae048eeaed81c73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0839eaaa1a19bae2a28540ff2368fe6fea63c8ff02961920b53e706faad2e8c9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f070637ea27aa8b38b25ebaf2b58a67bedd7c719d856e837c6b07ca6f7f6c52(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19bf58d98115dd0830d710049c6c19bd57ffe55a2e9521b963e349e07dc942f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c806fe274a613878feacf26cf2f6f920edb8374b5b35f989e8c2fd782820525(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestrictionHeaders],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e908f98e0eb7d31b7f5dbddbac801183c6dbf92f8b3e635661421828a898536(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1fced52063f363db0f33cc937d81859960e651c3a3cfc3eafb8e02ece48f90b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d2f6031ebac97a1a6b68566d6e8acf1bbc7621ac0165156a9d73decb5e7e36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80db56982250ee2be25ea72fa1feddfec5f428deeda22a88dd88334caf5a1189(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caeb5b2fa28606d5db2caf57d8ee155fdf1cc3269513a13c5276bcbaaef0460f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ea6a7bc7eb9ab9f2a567ce6a3e41074d27e5f25eaf426393b26668e6f00798b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23a1040f58507c8175f040842bf7985e919daa2da48634b4d6d24b642c104d10(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteConfigScmIpRestriction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a9d567d17b6932c4c1c5f5efee5cbdc02a112327f8297b6cd192a1f0264d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e652301a6cd386e2b9b5073d4e21f54afd2f786fe8de905beda593fbbb3d4e7c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292d99f9f3fdb019363d9a793b9d9ffba65b1389fbfc5831836cd578258214f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b3fdc1a0e17ec4c312a5341dbdcd96f0c5e67d09ed46f9e376c711a2017c41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291049ee84eef11a825d72422832fe73e1046680f10ae18d92b4e674df86c281(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34c6238c363d1709a451922ab74a6daf6476920014fb28f600c56416ab54b0eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbae116d4beb63073f7f42990a62f23cf2a2a13813cdf1466b0b846186b11b92(
    value: typing.Optional[DataAzurermLinuxFunctionAppSiteCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d151ff98785aa58c53f1c8b7a8650c35b7f75373803dccc13c67632fccf7da97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03cfbb15394993c88096d84f18ee484eed1765a0e54136b3fa0287919588c39a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be568f39ce9cede340dc18cad1a360b12c2a26463f2e62773900ad678610786e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe1b9d6c69985e9881a90642e13982292fdb36cef3d3fe8b43dea2cbf4ac4d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bc418286a7cbe55b2afe03700fead41c034d4d393ed56623157429a4acf0a0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff1b6752917922d2fd9d68198deea80c3546bf6398860ea485623963c8d9e72(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77eece2a7da0117ab148b2c0d4ce38a4e00e7eb81a226318acae388a36cfe10(
    value: typing.Optional[DataAzurermLinuxFunctionAppStickySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1dc70f10be2d1ee1a506a65a2dfdc2e1213bf936344b0bb9b1a2a765a07e0b(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a58a0567af37f3de8caecd716e5bd8f3b9e8962e16a97241c07930983f4d97(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902617243ff7526c8f2dcc9aa15d00aac7d724fede844ef4c4c2f7527568182f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545562f1f4af6b90573ad8b85c08d6f4922da319cea44873185cf0b9f1ba9d83(
    value: typing.Optional[typing.Union[DataAzurermLinuxFunctionAppTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
