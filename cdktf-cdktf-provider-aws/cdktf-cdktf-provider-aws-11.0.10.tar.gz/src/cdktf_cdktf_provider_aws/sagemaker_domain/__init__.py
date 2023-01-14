'''
# `aws_sagemaker_domain`

Refer to the Terraform Registory for docs: [`aws_sagemaker_domain`](https://www.terraform.io/docs/providers/aws/r/sagemaker_domain).
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


class SagemakerDomain(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomain",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain aws_sagemaker_domain}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        auth_mode: builtins.str,
        default_user_settings: typing.Union["SagemakerDomainDefaultUserSettings", typing.Dict[builtins.str, typing.Any]],
        domain_name: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        app_network_access_type: typing.Optional[builtins.str] = None,
        app_security_group_management: typing.Optional[builtins.str] = None,
        default_space_settings: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_settings: typing.Optional[typing.Union["SagemakerDomainDomainSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["SagemakerDomainRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain aws_sagemaker_domain} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param auth_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#auth_mode SagemakerDomain#auth_mode}.
        :param default_user_settings: default_user_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_user_settings SagemakerDomain#default_user_settings}
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#domain_name SagemakerDomain#domain_name}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#subnet_ids SagemakerDomain#subnet_ids}.
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#vpc_id SagemakerDomain#vpc_id}.
        :param app_network_access_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_network_access_type SagemakerDomain#app_network_access_type}.
        :param app_security_group_management: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_security_group_management SagemakerDomain#app_security_group_management}.
        :param default_space_settings: default_space_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_space_settings SagemakerDomain#default_space_settings}
        :param domain_settings: domain_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#domain_settings SagemakerDomain#domain_settings}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#id SagemakerDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kms_key_id SagemakerDomain#kms_key_id}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#retention_policy SagemakerDomain#retention_policy}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tags SagemakerDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tags_all SagemakerDomain#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4c0a93de0d35c0e7b09853a9b719d3e76946cb5fe438d32f00e5258d57afd22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SagemakerDomainConfig(
            auth_mode=auth_mode,
            default_user_settings=default_user_settings,
            domain_name=domain_name,
            subnet_ids=subnet_ids,
            vpc_id=vpc_id,
            app_network_access_type=app_network_access_type,
            app_security_group_management=app_security_group_management,
            default_space_settings=default_space_settings,
            domain_settings=domain_settings,
            id=id,
            kms_key_id=kms_key_id,
            retention_policy=retention_policy,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putDefaultSpaceSettings")
    def put_default_space_settings(
        self,
        *,
        execution_role: builtins.str,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role SagemakerDomain#execution_role}.
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#jupyter_server_app_settings SagemakerDomain#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kernel_gateway_app_settings SagemakerDomain#kernel_gateway_app_settings}
        :param security_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_groups SagemakerDomain#security_groups}.
        '''
        value = SagemakerDomainDefaultSpaceSettings(
            execution_role=execution_role,
            jupyter_server_app_settings=jupyter_server_app_settings,
            kernel_gateway_app_settings=kernel_gateway_app_settings,
            security_groups=security_groups,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultSpaceSettings", [value]))

    @jsii.member(jsii_name="putDefaultUserSettings")
    def put_default_user_settings(
        self,
        *,
        execution_role: builtins.str,
        canvas_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsCanvasAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        r_session_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsRSessionAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        sharing_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsSharingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        tensor_board_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsTensorBoardAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role SagemakerDomain#execution_role}.
        :param canvas_app_settings: canvas_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#canvas_app_settings SagemakerDomain#canvas_app_settings}
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#jupyter_server_app_settings SagemakerDomain#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kernel_gateway_app_settings SagemakerDomain#kernel_gateway_app_settings}
        :param r_session_app_settings: r_session_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#r_session_app_settings SagemakerDomain#r_session_app_settings}
        :param security_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_groups SagemakerDomain#security_groups}.
        :param sharing_settings: sharing_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sharing_settings SagemakerDomain#sharing_settings}
        :param tensor_board_app_settings: tensor_board_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tensor_board_app_settings SagemakerDomain#tensor_board_app_settings}
        '''
        value = SagemakerDomainDefaultUserSettings(
            execution_role=execution_role,
            canvas_app_settings=canvas_app_settings,
            jupyter_server_app_settings=jupyter_server_app_settings,
            kernel_gateway_app_settings=kernel_gateway_app_settings,
            r_session_app_settings=r_session_app_settings,
            security_groups=security_groups,
            sharing_settings=sharing_settings,
            tensor_board_app_settings=tensor_board_app_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultUserSettings", [value]))

    @jsii.member(jsii_name="putDomainSettings")
    def put_domain_settings(
        self,
        *,
        execution_role_identity_config: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_role_identity_config: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role_identity_config SagemakerDomain#execution_role_identity_config}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_group_ids SagemakerDomain#security_group_ids}.
        '''
        value = SagemakerDomainDomainSettings(
            execution_role_identity_config=execution_role_identity_config,
            security_group_ids=security_group_ids,
        )

        return typing.cast(None, jsii.invoke(self, "putDomainSettings", [value]))

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        home_efs_file_system: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param home_efs_file_system: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#home_efs_file_system SagemakerDomain#home_efs_file_system}.
        '''
        value = SagemakerDomainRetentionPolicy(
            home_efs_file_system=home_efs_file_system
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="resetAppNetworkAccessType")
    def reset_app_network_access_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppNetworkAccessType", []))

    @jsii.member(jsii_name="resetAppSecurityGroupManagement")
    def reset_app_security_group_management(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSecurityGroupManagement", []))

    @jsii.member(jsii_name="resetDefaultSpaceSettings")
    def reset_default_space_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultSpaceSettings", []))

    @jsii.member(jsii_name="resetDomainSettings")
    def reset_domain_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomainSettings", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetRetentionPolicy")
    def reset_retention_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPolicy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="defaultSpaceSettings")
    def default_space_settings(
        self,
    ) -> "SagemakerDomainDefaultSpaceSettingsOutputReference":
        return typing.cast("SagemakerDomainDefaultSpaceSettingsOutputReference", jsii.get(self, "defaultSpaceSettings"))

    @builtins.property
    @jsii.member(jsii_name="defaultUserSettings")
    def default_user_settings(
        self,
    ) -> "SagemakerDomainDefaultUserSettingsOutputReference":
        return typing.cast("SagemakerDomainDefaultUserSettingsOutputReference", jsii.get(self, "defaultUserSettings"))

    @builtins.property
    @jsii.member(jsii_name="domainSettings")
    def domain_settings(self) -> "SagemakerDomainDomainSettingsOutputReference":
        return typing.cast("SagemakerDomainDomainSettingsOutputReference", jsii.get(self, "domainSettings"))

    @builtins.property
    @jsii.member(jsii_name="homeEfsFileSystemId")
    def home_efs_file_system_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homeEfsFileSystemId"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> "SagemakerDomainRetentionPolicyOutputReference":
        return typing.cast("SagemakerDomainRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdForDomainBoundary")
    def security_group_id_for_domain_boundary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "securityGroupIdForDomainBoundary"))

    @builtins.property
    @jsii.member(jsii_name="singleSignOnManagedApplicationInstanceId")
    def single_sign_on_managed_application_instance_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "singleSignOnManagedApplicationInstanceId"))

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @builtins.property
    @jsii.member(jsii_name="appNetworkAccessTypeInput")
    def app_network_access_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appNetworkAccessTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="appSecurityGroupManagementInput")
    def app_security_group_management_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSecurityGroupManagementInput"))

    @builtins.property
    @jsii.member(jsii_name="authModeInput")
    def auth_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authModeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultSpaceSettingsInput")
    def default_space_settings_input(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultSpaceSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDefaultSpaceSettings"], jsii.get(self, "defaultSpaceSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultUserSettingsInput")
    def default_user_settings_input(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettings"], jsii.get(self, "defaultUserSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="domainSettingsInput")
    def domain_settings_input(self) -> typing.Optional["SagemakerDomainDomainSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDomainSettings"], jsii.get(self, "domainSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["SagemakerDomainRetentionPolicy"]:
        return typing.cast(typing.Optional["SagemakerDomainRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdsInput")
    def subnet_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appNetworkAccessType")
    def app_network_access_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appNetworkAccessType"))

    @app_network_access_type.setter
    def app_network_access_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a789ed68ecb4037790f455759a9cbd9341c68006db9340da0b5d74cf669f5d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appNetworkAccessType", value)

    @builtins.property
    @jsii.member(jsii_name="appSecurityGroupManagement")
    def app_security_group_management(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecurityGroupManagement"))

    @app_security_group_management.setter
    def app_security_group_management(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd18bf0f20147152f18870038a0be061b0c302f1a1dbc3f5f9d4e047ad36427)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecurityGroupManagement", value)

    @builtins.property
    @jsii.member(jsii_name="authMode")
    def auth_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authMode"))

    @auth_mode.setter
    def auth_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f7b2bfd6dcb0215fe8f736f167d9e1f1920c2a8610faeef276ba2fcebfae416)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authMode", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591bc38cf28322f31eefbc8553b5bbf93015f8daa5f368491a380f727f4c9c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b962faa6c9afa45286174e0fb8dd041a619758e1cd5c02f7f9c884264321a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__660452657ee41967303b7e3b8771baeaf8b382468c79a2c856f053486db8200a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330e095be22d7d00793a78483dd25c32f3b94aba03d03470918341187383c42d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b556e1c7b545509f192c97858addc88086ac72e9761400bda96efcbc045662f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fda591cc3cbf7d718c2f408297e77b84cf04230459b9191dc4b839fbd2b820)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57c43629bcf879992cbe07042429c54bffeef4f5fe0a1b1a94d6854597348eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "auth_mode": "authMode",
        "default_user_settings": "defaultUserSettings",
        "domain_name": "domainName",
        "subnet_ids": "subnetIds",
        "vpc_id": "vpcId",
        "app_network_access_type": "appNetworkAccessType",
        "app_security_group_management": "appSecurityGroupManagement",
        "default_space_settings": "defaultSpaceSettings",
        "domain_settings": "domainSettings",
        "id": "id",
        "kms_key_id": "kmsKeyId",
        "retention_policy": "retentionPolicy",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class SagemakerDomainConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        auth_mode: builtins.str,
        default_user_settings: typing.Union["SagemakerDomainDefaultUserSettings", typing.Dict[builtins.str, typing.Any]],
        domain_name: builtins.str,
        subnet_ids: typing.Sequence[builtins.str],
        vpc_id: builtins.str,
        app_network_access_type: typing.Optional[builtins.str] = None,
        app_security_group_management: typing.Optional[builtins.str] = None,
        default_space_settings: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        domain_settings: typing.Optional[typing.Union["SagemakerDomainDomainSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        retention_policy: typing.Optional[typing.Union["SagemakerDomainRetentionPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param auth_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#auth_mode SagemakerDomain#auth_mode}.
        :param default_user_settings: default_user_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_user_settings SagemakerDomain#default_user_settings}
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#domain_name SagemakerDomain#domain_name}.
        :param subnet_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#subnet_ids SagemakerDomain#subnet_ids}.
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#vpc_id SagemakerDomain#vpc_id}.
        :param app_network_access_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_network_access_type SagemakerDomain#app_network_access_type}.
        :param app_security_group_management: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_security_group_management SagemakerDomain#app_security_group_management}.
        :param default_space_settings: default_space_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_space_settings SagemakerDomain#default_space_settings}
        :param domain_settings: domain_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#domain_settings SagemakerDomain#domain_settings}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#id SagemakerDomain#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kms_key_id SagemakerDomain#kms_key_id}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#retention_policy SagemakerDomain#retention_policy}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tags SagemakerDomain#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tags_all SagemakerDomain#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(default_user_settings, dict):
            default_user_settings = SagemakerDomainDefaultUserSettings(**default_user_settings)
        if isinstance(default_space_settings, dict):
            default_space_settings = SagemakerDomainDefaultSpaceSettings(**default_space_settings)
        if isinstance(domain_settings, dict):
            domain_settings = SagemakerDomainDomainSettings(**domain_settings)
        if isinstance(retention_policy, dict):
            retention_policy = SagemakerDomainRetentionPolicy(**retention_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b43f96c45f8a18112a22a83fa64c5d02568d4b1364e8dc31b5ca7bb65c3a3429)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument auth_mode", value=auth_mode, expected_type=type_hints["auth_mode"])
            check_type(argname="argument default_user_settings", value=default_user_settings, expected_type=type_hints["default_user_settings"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument app_network_access_type", value=app_network_access_type, expected_type=type_hints["app_network_access_type"])
            check_type(argname="argument app_security_group_management", value=app_security_group_management, expected_type=type_hints["app_security_group_management"])
            check_type(argname="argument default_space_settings", value=default_space_settings, expected_type=type_hints["default_space_settings"])
            check_type(argname="argument domain_settings", value=domain_settings, expected_type=type_hints["domain_settings"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "auth_mode": auth_mode,
            "default_user_settings": default_user_settings,
            "domain_name": domain_name,
            "subnet_ids": subnet_ids,
            "vpc_id": vpc_id,
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
        if app_network_access_type is not None:
            self._values["app_network_access_type"] = app_network_access_type
        if app_security_group_management is not None:
            self._values["app_security_group_management"] = app_security_group_management
        if default_space_settings is not None:
            self._values["default_space_settings"] = default_space_settings
        if domain_settings is not None:
            self._values["domain_settings"] = domain_settings
        if id is not None:
            self._values["id"] = id
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if retention_policy is not None:
            self._values["retention_policy"] = retention_policy
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
    def auth_mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#auth_mode SagemakerDomain#auth_mode}.'''
        result = self._values.get("auth_mode")
        assert result is not None, "Required property 'auth_mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_user_settings(self) -> "SagemakerDomainDefaultUserSettings":
        '''default_user_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_user_settings SagemakerDomain#default_user_settings}
        '''
        result = self._values.get("default_user_settings")
        assert result is not None, "Required property 'default_user_settings' is missing"
        return typing.cast("SagemakerDomainDefaultUserSettings", result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#domain_name SagemakerDomain#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#subnet_ids SagemakerDomain#subnet_ids}.'''
        result = self._values.get("subnet_ids")
        assert result is not None, "Required property 'subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#vpc_id SagemakerDomain#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_network_access_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_network_access_type SagemakerDomain#app_network_access_type}.'''
        result = self._values.get("app_network_access_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_security_group_management(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_security_group_management SagemakerDomain#app_security_group_management}.'''
        result = self._values.get("app_security_group_management")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_space_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultSpaceSettings"]:
        '''default_space_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_space_settings SagemakerDomain#default_space_settings}
        '''
        result = self._values.get("default_space_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultSpaceSettings"], result)

    @builtins.property
    def domain_settings(self) -> typing.Optional["SagemakerDomainDomainSettings"]:
        '''domain_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#domain_settings SagemakerDomain#domain_settings}
        '''
        result = self._values.get("domain_settings")
        return typing.cast(typing.Optional["SagemakerDomainDomainSettings"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#id SagemakerDomain#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kms_key_id SagemakerDomain#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_policy(self) -> typing.Optional["SagemakerDomainRetentionPolicy"]:
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#retention_policy SagemakerDomain#retention_policy}
        '''
        result = self._values.get("retention_policy")
        return typing.cast(typing.Optional["SagemakerDomainRetentionPolicy"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tags SagemakerDomain#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tags_all SagemakerDomain#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettings",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role": "executionRole",
        "jupyter_server_app_settings": "jupyterServerAppSettings",
        "kernel_gateway_app_settings": "kernelGatewayAppSettings",
        "security_groups": "securityGroups",
    },
)
class SagemakerDomainDefaultSpaceSettings:
    def __init__(
        self,
        *,
        execution_role: builtins.str,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role SagemakerDomain#execution_role}.
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#jupyter_server_app_settings SagemakerDomain#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kernel_gateway_app_settings SagemakerDomain#kernel_gateway_app_settings}
        :param security_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_groups SagemakerDomain#security_groups}.
        '''
        if isinstance(jupyter_server_app_settings, dict):
            jupyter_server_app_settings = SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings(**jupyter_server_app_settings)
        if isinstance(kernel_gateway_app_settings, dict):
            kernel_gateway_app_settings = SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings(**kernel_gateway_app_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270b7279a9cbea10aa26e9039ab79156a040f4997553838d2e7c1daeb3b9d1cf)
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument jupyter_server_app_settings", value=jupyter_server_app_settings, expected_type=type_hints["jupyter_server_app_settings"])
            check_type(argname="argument kernel_gateway_app_settings", value=kernel_gateway_app_settings, expected_type=type_hints["kernel_gateway_app_settings"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role": execution_role,
        }
        if jupyter_server_app_settings is not None:
            self._values["jupyter_server_app_settings"] = jupyter_server_app_settings
        if kernel_gateway_app_settings is not None:
            self._values["kernel_gateway_app_settings"] = kernel_gateway_app_settings
        if security_groups is not None:
            self._values["security_groups"] = security_groups

    @builtins.property
    def execution_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role SagemakerDomain#execution_role}.'''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jupyter_server_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings"]:
        '''jupyter_server_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#jupyter_server_app_settings SagemakerDomain#jupyter_server_app_settings}
        '''
        result = self._values.get("jupyter_server_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings"], result)

    @builtins.property
    def kernel_gateway_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings"]:
        '''kernel_gateway_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kernel_gateway_app_settings SagemakerDomain#kernel_gateway_app_settings}
        '''
        result = self._values.get("kernel_gateway_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings"], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_groups SagemakerDomain#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "code_repository": "codeRepository",
        "default_resource_spec": "defaultResourceSpec",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings:
    def __init__(
        self,
        *,
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#code_repository SagemakerDomain#code_repository}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3872dcdb3e01c906ef847747b58be3fb9c3ca79eef6a22df01e5e001976726fc)
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def code_repository(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository"]]]:
        '''code_repository block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#code_repository SagemakerDomain#code_repository}
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec"], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository",
    jsii_struct_bases=[],
    name_mapping={"repository_url": "repositoryUrl"},
)
class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository:
    def __init__(self, *, repository_url: builtins.str) -> None:
        '''
        :param repository_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#repository_url SagemakerDomain#repository_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f959bc2fedcf6898c2a91a2ee854ed6de47cd305a477ed7188e6c73d16865706)
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_url": repository_url,
        }

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#repository_url SagemakerDomain#repository_url}.'''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f359bc937d0841dc9083f39dc97135b658ce4a1a1d52326755e9dbc1647c7394)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc388bfc93c4bad0b45629abc410da2fc72e2a040bd70f09243dfffe272290f2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772c1f6b4a9f32dd8c6e2a1f5a702b95475a4196eab0cdd34864371fb31bf312)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc4c3249b0b37afc25fba5e2e77f13fb9968f6607566c48f97995edd81ccfe5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5688303d2931399ace6f453c36158605e9740e4e80ee445544fc4c735cb848)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__923ccd2f70b66b09d098843f7ded3ee75deccc9865f69b1f6e183c9efe1f0be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e449366bdda7b2d15e660de0295c7638ab7126fb287febed3a4d55c2df328a22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="repositoryUrlInput")
    def repository_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))

    @repository_url.setter
    def repository_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__946e2d39dc3779371d9f3e3c765b38da67879e8e2effd2fe418920c1e8bcd6ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0efa7a4e99ece534ef2c53bf911252a153c0b7f9d1946429c49395da8ee2cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3456985365b9b55660a17fb07083eec3fb4acd57c293b79cba3f0e010b889eb)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6845dbc45245ec5dc1210f0bf601799d646dd7ce973b90d6d0c03017e11abcf1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457c5d78c7b7213a17b3ed1d2a635b69f031d6773cef50c4ae7dcfb32349a586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dafee40090da458adf628290ad08fc1dd4924c59d7fad87a2b8b365a12dfe919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99cc59c0d3d9d5bf5c6447141f307af105580ba06e925e821b2e1b4601e93a65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e817670822f005f757f880aaf3fe66f1bbac3e06dc7ac6681c5cc454d85c38cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5a91e305e8c80459a155db9bc9d316678e45d8671e4a14c06f9fbffcd7254ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__448878be6a666d72e1a395d1696824401dc8dfccf9e430d1706bb21b06b8f67e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeRepository")
    def put_code_repository(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ff5ee10c90a44526d9b508b755b6de11e58d3c5648f96b241e3d8ffb489d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCodeRepository", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        value = SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCodeRepository")
    def reset_code_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeRepository", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryList:
        return typing.cast(SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryList, jsii.get(self, "codeRepository"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="codeRepositoryInput")
    def code_repository_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "codeRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b09653a47b5c3a7f0e0dd81606a33752db1a796fa8c7261d02bfa5130eba394)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99152b9381588c93fdc896e1a68e03a8c0b0b5700ee1266feabfb91a843e5b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "custom_image": "customImage",
        "default_resource_spec": "defaultResourceSpec",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings:
    def __init__(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa901fe75ae3242f4c2215186bf54d34004a4608317993bdfbb61c3b8395f7a4)
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def custom_image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage"]]]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec"], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "app_image_config_name": "appImageConfigName",
        "image_name": "imageName",
        "image_version_number": "imageVersionNumber",
    },
)
class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage:
    def __init__(
        self,
        *,
        app_image_config_name: builtins.str,
        image_name: builtins.str,
        image_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param app_image_config_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_image_config_name SagemakerDomain#app_image_config_name}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_name SagemakerDomain#image_name}.
        :param image_version_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_version_number SagemakerDomain#image_version_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f73d7586f80f54c528e4e2f6fb07fae7ffa3a28e1b2c274bd7d1c929c9d0a6)
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version_number", value=image_version_number, expected_type=type_hints["image_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
            "image_name": image_name,
        }
        if image_version_number is not None:
            self._values["image_version_number"] = image_version_number

    @builtins.property
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_image_config_name SagemakerDomain#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_name SagemakerDomain#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_version_number SagemakerDomain#image_version_number}.'''
        result = self._values.get("image_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed3c971f9cc655e8b9ef2f4ca5ed02f304c40711a756174ff1572cb947ace0ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27395f3c4f3fd290554296af6248c8063157c82ae64b9f21cf9db7bc93f0548d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc444000d22481e54c44fc695c832d93ab0b5fd13c25ee99b8a9837b35be435)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf1e2cea1d9cc347ff606c75d722c955a6c840b76f4738ec6c6219e300a6a9b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b862475f7bbfff074c63909eafd40b77b55c2a377a41e503eb92c02f8d567ee7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3f2982358c8c869c687f96fda51d6bb2092cb525de14307867e123054d74ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f699e4c80c8efc166f9c68b708047d44281a6c5e5880e3fb4b3bfc47642ddb4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageVersionNumber")
    def reset_image_version_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersionNumber", []))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumberInput")
    def image_version_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageVersionNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92863c155c5c0ff1ad2e695913a3754a3ce84dbce6e6a1a965dfc4049b087f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d582af55749b381b26b19fa20b8b0171661f0681682ae347cf422343a70531)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumber")
    def image_version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageVersionNumber"))

    @image_version_number.setter
    def image_version_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fa122e63ff116ad0e4c2ec994112c15b236c5f281168e51527cd5e2a7348118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6b1ad9aaf705493d1cf5a53cfb5dffa0c0a1b3bf32aaeee053ba267283219ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117c188b135c26e518901a6af08509bb6318fba74ac4ff2aafbbba8b976b9ae3)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58d9b16bf6747c14653a620e64893408726c2b202e7f81ef09ca0cd6e04e3116)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f836b257a17d439bf44cbe75cec2968618b6dad8c7cfe3e64ed131bd181c4ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f552678d0a1294405036b28a66c0511724aeb4a3d62d29bdaf70b92b78a18c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6939d576ae803045cbbfa0f702ec82d1bfb7924d17961842e23686f280b65286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6959e309e05f0c2312072cb2d1f39aa0974f33f15673d62258ef249fc1c7d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cbf15f32f3efbe7e3418f454b238b491b4b063ad7ab8059522dc2c9c0e8047b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ba6806af7b4f01b53443c893b21b63fd32619cadb005a56b0dc302d491467df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceb5c829d77fdd180ac95c7568b4ee295618c23dea4b9fa163ac90d760a68ea2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        value = SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(
        self,
    ) -> SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageList:
        return typing.cast(SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageList, jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb13731b3dda6a4d24e04c74f5e04f8c7be0e36693ca0e2ad9d9ee5d3f34909)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e49ae4ff3dc2b2c5215f214ec484171e9c2b79a43dc6045e8c867e68843d60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultSpaceSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultSpaceSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__667e3807e751393f76efec20d25f567f726fa47cb41ed8f21b7b903053efb0aa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putJupyterServerAppSettings")
    def put_jupyter_server_app_settings(
        self,
        *,
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#code_repository SagemakerDomain#code_repository}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        value = SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings(
            code_repository=code_repository,
            default_resource_spec=default_resource_spec,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putJupyterServerAppSettings", [value]))

    @jsii.member(jsii_name="putKernelGatewayAppSettings")
    def put_kernel_gateway_app_settings(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        value = SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings(
            custom_image=custom_image,
            default_resource_spec=default_resource_spec,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putKernelGatewayAppSettings", [value]))

    @jsii.member(jsii_name="resetJupyterServerAppSettings")
    def reset_jupyter_server_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJupyterServerAppSettings", []))

    @jsii.member(jsii_name="resetKernelGatewayAppSettings")
    def reset_kernel_gateway_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelGatewayAppSettings", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettings")
    def jupyter_server_app_settings(
        self,
    ) -> SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsOutputReference:
        return typing.cast(SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsOutputReference, jsii.get(self, "jupyterServerAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettings")
    def kernel_gateway_app_settings(
        self,
    ) -> SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsOutputReference:
        return typing.cast(SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsOutputReference, jsii.get(self, "kernelGatewayAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettingsInput")
    def jupyter_server_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings], jsii.get(self, "jupyterServerAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettingsInput")
    def kernel_gateway_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings], jsii.get(self, "kernelGatewayAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad8936ddf1ee50477399fa5461105e653694c3ebb2268226a8175f1304cea442)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfe6a18b9873260791c78374928c5c14b478bb904f6b4a4665d884330b5407c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerDomainDefaultSpaceSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultSpaceSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultSpaceSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe68495c3d220beda59e522aa606bf30647e5fc521595f65843f7ada282f3ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettings",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role": "executionRole",
        "canvas_app_settings": "canvasAppSettings",
        "jupyter_server_app_settings": "jupyterServerAppSettings",
        "kernel_gateway_app_settings": "kernelGatewayAppSettings",
        "r_session_app_settings": "rSessionAppSettings",
        "security_groups": "securityGroups",
        "sharing_settings": "sharingSettings",
        "tensor_board_app_settings": "tensorBoardAppSettings",
    },
)
class SagemakerDomainDefaultUserSettings:
    def __init__(
        self,
        *,
        execution_role: builtins.str,
        canvas_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsCanvasAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        jupyter_server_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsJupyterServerAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        kernel_gateway_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        r_session_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsRSessionAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        sharing_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsSharingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        tensor_board_app_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsTensorBoardAppSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execution_role: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role SagemakerDomain#execution_role}.
        :param canvas_app_settings: canvas_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#canvas_app_settings SagemakerDomain#canvas_app_settings}
        :param jupyter_server_app_settings: jupyter_server_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#jupyter_server_app_settings SagemakerDomain#jupyter_server_app_settings}
        :param kernel_gateway_app_settings: kernel_gateway_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kernel_gateway_app_settings SagemakerDomain#kernel_gateway_app_settings}
        :param r_session_app_settings: r_session_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#r_session_app_settings SagemakerDomain#r_session_app_settings}
        :param security_groups: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_groups SagemakerDomain#security_groups}.
        :param sharing_settings: sharing_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sharing_settings SagemakerDomain#sharing_settings}
        :param tensor_board_app_settings: tensor_board_app_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tensor_board_app_settings SagemakerDomain#tensor_board_app_settings}
        '''
        if isinstance(canvas_app_settings, dict):
            canvas_app_settings = SagemakerDomainDefaultUserSettingsCanvasAppSettings(**canvas_app_settings)
        if isinstance(jupyter_server_app_settings, dict):
            jupyter_server_app_settings = SagemakerDomainDefaultUserSettingsJupyterServerAppSettings(**jupyter_server_app_settings)
        if isinstance(kernel_gateway_app_settings, dict):
            kernel_gateway_app_settings = SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings(**kernel_gateway_app_settings)
        if isinstance(r_session_app_settings, dict):
            r_session_app_settings = SagemakerDomainDefaultUserSettingsRSessionAppSettings(**r_session_app_settings)
        if isinstance(sharing_settings, dict):
            sharing_settings = SagemakerDomainDefaultUserSettingsSharingSettings(**sharing_settings)
        if isinstance(tensor_board_app_settings, dict):
            tensor_board_app_settings = SagemakerDomainDefaultUserSettingsTensorBoardAppSettings(**tensor_board_app_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03d83a3719284499df4f62cb251e309d8366a16f13707636601d23784e265c8)
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument canvas_app_settings", value=canvas_app_settings, expected_type=type_hints["canvas_app_settings"])
            check_type(argname="argument jupyter_server_app_settings", value=jupyter_server_app_settings, expected_type=type_hints["jupyter_server_app_settings"])
            check_type(argname="argument kernel_gateway_app_settings", value=kernel_gateway_app_settings, expected_type=type_hints["kernel_gateway_app_settings"])
            check_type(argname="argument r_session_app_settings", value=r_session_app_settings, expected_type=type_hints["r_session_app_settings"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument sharing_settings", value=sharing_settings, expected_type=type_hints["sharing_settings"])
            check_type(argname="argument tensor_board_app_settings", value=tensor_board_app_settings, expected_type=type_hints["tensor_board_app_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role": execution_role,
        }
        if canvas_app_settings is not None:
            self._values["canvas_app_settings"] = canvas_app_settings
        if jupyter_server_app_settings is not None:
            self._values["jupyter_server_app_settings"] = jupyter_server_app_settings
        if kernel_gateway_app_settings is not None:
            self._values["kernel_gateway_app_settings"] = kernel_gateway_app_settings
        if r_session_app_settings is not None:
            self._values["r_session_app_settings"] = r_session_app_settings
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if sharing_settings is not None:
            self._values["sharing_settings"] = sharing_settings
        if tensor_board_app_settings is not None:
            self._values["tensor_board_app_settings"] = tensor_board_app_settings

    @builtins.property
    def execution_role(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role SagemakerDomain#execution_role}.'''
        result = self._values.get("execution_role")
        assert result is not None, "Required property 'execution_role' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def canvas_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsCanvasAppSettings"]:
        '''canvas_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#canvas_app_settings SagemakerDomain#canvas_app_settings}
        '''
        result = self._values.get("canvas_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsCanvasAppSettings"], result)

    @builtins.property
    def jupyter_server_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsJupyterServerAppSettings"]:
        '''jupyter_server_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#jupyter_server_app_settings SagemakerDomain#jupyter_server_app_settings}
        '''
        result = self._values.get("jupyter_server_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsJupyterServerAppSettings"], result)

    @builtins.property
    def kernel_gateway_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings"]:
        '''kernel_gateway_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#kernel_gateway_app_settings SagemakerDomain#kernel_gateway_app_settings}
        '''
        result = self._values.get("kernel_gateway_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings"], result)

    @builtins.property
    def r_session_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsRSessionAppSettings"]:
        '''r_session_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#r_session_app_settings SagemakerDomain#r_session_app_settings}
        '''
        result = self._values.get("r_session_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsRSessionAppSettings"], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_groups SagemakerDomain#security_groups}.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sharing_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsSharingSettings"]:
        '''sharing_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sharing_settings SagemakerDomain#sharing_settings}
        '''
        result = self._values.get("sharing_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsSharingSettings"], result)

    @builtins.property
    def tensor_board_app_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsTensorBoardAppSettings"]:
        '''tensor_board_app_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#tensor_board_app_settings SagemakerDomain#tensor_board_app_settings}
        '''
        result = self._values.get("tensor_board_app_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsTensorBoardAppSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsCanvasAppSettings",
    jsii_struct_bases=[],
    name_mapping={"time_series_forecasting_settings": "timeSeriesForecastingSettings"},
)
class SagemakerDomainDefaultUserSettingsCanvasAppSettings:
    def __init__(
        self,
        *,
        time_series_forecasting_settings: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_series_forecasting_settings: time_series_forecasting_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#time_series_forecasting_settings SagemakerDomain#time_series_forecasting_settings}
        '''
        if isinstance(time_series_forecasting_settings, dict):
            time_series_forecasting_settings = SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings(**time_series_forecasting_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944bdbdc4f6cd2e2618aa6c9206b9c9e91770b5175bf3c84dbac0fedb5afe965)
            check_type(argname="argument time_series_forecasting_settings", value=time_series_forecasting_settings, expected_type=type_hints["time_series_forecasting_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if time_series_forecasting_settings is not None:
            self._values["time_series_forecasting_settings"] = time_series_forecasting_settings

    @builtins.property
    def time_series_forecasting_settings(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"]:
        '''time_series_forecasting_settings block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#time_series_forecasting_settings SagemakerDomain#time_series_forecasting_settings}
        '''
        result = self._values.get("time_series_forecasting_settings")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsCanvasAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsCanvasAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsCanvasAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af5879b43d76e99a2256723ccbb9f5395f1e19ee7901778b11d6d2f3da3181b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTimeSeriesForecastingSettings")
    def put_time_series_forecasting_settings(
        self,
        *,
        amazon_forecast_role_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param amazon_forecast_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#amazon_forecast_role_arn SagemakerDomain#amazon_forecast_role_arn}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#status SagemakerDomain#status}.
        '''
        value = SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings(
            amazon_forecast_role_arn=amazon_forecast_role_arn, status=status
        )

        return typing.cast(None, jsii.invoke(self, "putTimeSeriesForecastingSettings", [value]))

    @jsii.member(jsii_name="resetTimeSeriesForecastingSettings")
    def reset_time_series_forecasting_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeSeriesForecastingSettings", []))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesForecastingSettings")
    def time_series_forecasting_settings(
        self,
    ) -> "SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference":
        return typing.cast("SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference", jsii.get(self, "timeSeriesForecastingSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesForecastingSettingsInput")
    def time_series_forecasting_settings_input(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings"], jsii.get(self, "timeSeriesForecastingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae6372baf99c8e396c70f49a5a7bb6f397613ba0ecec62b8c88267bf64f1124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "amazon_forecast_role_arn": "amazonForecastRoleArn",
        "status": "status",
    },
)
class SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings:
    def __init__(
        self,
        *,
        amazon_forecast_role_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param amazon_forecast_role_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#amazon_forecast_role_arn SagemakerDomain#amazon_forecast_role_arn}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#status SagemakerDomain#status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb6c86eee750eb3305a2843880a68afeb17e40f33aeb902f7f39cf845dc9665a)
            check_type(argname="argument amazon_forecast_role_arn", value=amazon_forecast_role_arn, expected_type=type_hints["amazon_forecast_role_arn"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if amazon_forecast_role_arn is not None:
            self._values["amazon_forecast_role_arn"] = amazon_forecast_role_arn
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def amazon_forecast_role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#amazon_forecast_role_arn SagemakerDomain#amazon_forecast_role_arn}.'''
        result = self._values.get("amazon_forecast_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#status SagemakerDomain#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10787220583c3c78b149c8dcf8eabab4365081ba7d0201e5aa9041e0e3da67d8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAmazonForecastRoleArn")
    def reset_amazon_forecast_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAmazonForecastRoleArn", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @builtins.property
    @jsii.member(jsii_name="amazonForecastRoleArnInput")
    def amazon_forecast_role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "amazonForecastRoleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="amazonForecastRoleArn")
    def amazon_forecast_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "amazonForecastRoleArn"))

    @amazon_forecast_role_arn.setter
    def amazon_forecast_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941ff61d7d08324d383e8e0dc6d10cb1eac1f3a420db2a8d592e1bb13bf409f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "amazonForecastRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5930838c7a99d9a1a7fdc171f2095357e0a1c9eadffb6a1ac61828e8fdd00651)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b0a1baf47476027935d9c7723814c1bcb32dc0d715cc93ae5043165a356833)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "code_repository": "codeRepository",
        "default_resource_spec": "defaultResourceSpec",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerDomainDefaultUserSettingsJupyterServerAppSettings:
    def __init__(
        self,
        *,
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#code_repository SagemakerDomain#code_repository}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a742cdbbe567a32d826407ec0b52b4d91299d09251932e37c1ada0b9352bc82)
            check_type(argname="argument code_repository", value=code_repository, expected_type=type_hints["code_repository"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_repository is not None:
            self._values["code_repository"] = code_repository
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def code_repository(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository"]]]:
        '''code_repository block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#code_repository SagemakerDomain#code_repository}
        '''
        result = self._values.get("code_repository")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec"], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsJupyterServerAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository",
    jsii_struct_bases=[],
    name_mapping={"repository_url": "repositoryUrl"},
)
class SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository:
    def __init__(self, *, repository_url: builtins.str) -> None:
        '''
        :param repository_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#repository_url SagemakerDomain#repository_url}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c902c75b8b4ba7b2333d71ad6b8e972286518683fbbc1b0617ff7afee1ea22)
            check_type(argname="argument repository_url", value=repository_url, expected_type=type_hints["repository_url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository_url": repository_url,
        }

    @builtins.property
    def repository_url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#repository_url SagemakerDomain#repository_url}.'''
        result = self._values.get("repository_url")
        assert result is not None, "Required property 'repository_url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eed3f8351bff2753c31d5c9fbfcef7c7177fc9a29e2185475df228f4027ea6c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cade65acbe0978ba775f6a246bea72d33efb55f76b1193aa6427c376c33fe7c2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966045a478a95050488ed41d9aa91e78bb20ede9a108c3ed0e1b2fdc25389e8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b52793615f2bf8f43804936628dfe985c18f8a87a55f371535a451586e93c716)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67a590d58a5037b2482e939af85908dd7d06d0f39fed0286afd46e6f73151601)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736fdce35a78b6768cbec74582bb021d32a791c0fe9ea8f8b677c75651794d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c846e351046a06aca12016e7e79cf24d1bee940e69bbd30bb67e27eb656b443)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="repositoryUrlInput")
    def repository_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repositoryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))

    @repository_url.setter
    def repository_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c44e2c2c948b6f7d13d49dc869ac4a2dcda9f1a94ef394cc4f28e1644efdbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repositoryUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d822fc2cea4385c1116bc07f2d9d97b026aadb8f9952b6c72f77f320ff1530c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b014fb3b00c194db2abf8d5b991e4bb73f10e549b8a85055a51f11fe8ba556)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c1f3ce3aa10a23744951fab0f82f53b9316ec3541dc4711026b73d87c63dc26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b40c4a22230b16995e8019d807d5f4864f24551f7c94fd34e2e26959309ddf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec88bd8141f60ed3b1b57d622c1f93658aa731d67ae33dc808e7d2beac216c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81081ca54cc689a799b407f445eded9b9ffcad2ece6befc08f5d31331b0adce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50566befde93daa7bfbb6eaf9dfd30bc80e0bb9733d6ddf22ab7ec68c127f62c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d76647c6b6f5bcb7f915c153e5fab90bd8951cb22dd7836a28ecdf79fb613230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__66cf52cc16d7ba09a624f0d92c8d5f110653685e8e649160f9d1934d11bf1d6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCodeRepository")
    def put_code_repository(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788c32affd538987cdf8ca73dac7dbe95dd0f16cbb4f732a6bf7f504a4ab97a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCodeRepository", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        value = SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCodeRepository")
    def reset_code_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCodeRepository", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="codeRepository")
    def code_repository(
        self,
    ) -> SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryList:
        return typing.cast(SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryList, jsii.get(self, "codeRepository"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="codeRepositoryInput")
    def code_repository_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository]]], jsii.get(self, "codeRepositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e04d856e19510ffa6688a969be07b5efeb21d6a47e8ab57617e6be4cd832392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0af993cfe172d6552820711e2cbf94e1514745bf42ae2f0fd6d0e85390bfe68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "custom_image": "customImage",
        "default_resource_spec": "defaultResourceSpec",
        "lifecycle_config_arns": "lifecycleConfigArns",
    },
)
class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings:
    def __init__(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd57ea261f000a4d4baa792c3844eb7b9050f14ca5d81270cd7f504f6d747515)
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
            check_type(argname="argument lifecycle_config_arns", value=lifecycle_config_arns, expected_type=type_hints["lifecycle_config_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec
        if lifecycle_config_arns is not None:
            self._values["lifecycle_config_arns"] = lifecycle_config_arns

    @builtins.property
    def custom_image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage"]]]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec"], result)

    @builtins.property
    def lifecycle_config_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.'''
        result = self._values.get("lifecycle_config_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "app_image_config_name": "appImageConfigName",
        "image_name": "imageName",
        "image_version_number": "imageVersionNumber",
    },
)
class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage:
    def __init__(
        self,
        *,
        app_image_config_name: builtins.str,
        image_name: builtins.str,
        image_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param app_image_config_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_image_config_name SagemakerDomain#app_image_config_name}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_name SagemakerDomain#image_name}.
        :param image_version_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_version_number SagemakerDomain#image_version_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6f450e5f3ca430859959a8de37da435b0d120a5908810e8ac4769643ebd353)
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version_number", value=image_version_number, expected_type=type_hints["image_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
            "image_name": image_name,
        }
        if image_version_number is not None:
            self._values["image_version_number"] = image_version_number

    @builtins.property
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_image_config_name SagemakerDomain#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_name SagemakerDomain#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_version_number SagemakerDomain#image_version_number}.'''
        result = self._values.get("image_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74e57474da8c2816a9ab271229b3fab532c2d84a74deafbacae15b4bf389088d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab61cd2ed59d256b8133f0b514034ecf8316bd3dbce7acbac786bce90b08697)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b76b7a16853d2f8904614323640fb83b1d256820f9e863bd08a9976943946f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28c47661d164f3b541397a27b8e102d2f28e05d15956a5ce608112613bbdfd14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d830d4046d89bf41ad775f1a3f731077c6ed2b418b55a82b93f10bba9489cdc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6614e7dc56c86c18bbe334b0e06179fc17b8a455fc88fa49a6bd00d28432d90a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86e8cf9f4407a174f21086132f1a97ae3f16587596c8171816f1db93d5ffdf79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageVersionNumber")
    def reset_image_version_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersionNumber", []))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumberInput")
    def image_version_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageVersionNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6425966b04172ad14f26e1feb402f44785c57711f299df44b93e9e6f5b05d66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eadbc1390906e31dd034f3311003d87ad4c2fa06bfb7a1bb125196a741b9e987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumber")
    def image_version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageVersionNumber"))

    @image_version_number.setter
    def image_version_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a6a7bd69c79bfff4f551f42edcb4405ff110f048e6a10b9aff766598737390e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85d88754ad105f8006c491641221a0522a79a000545c5db4b22a502ba80820d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e27edb3f764dff4f7286aa101a7a30d6d0ba92f2e63956ca18b89d30dec5e9)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25257682b96d81aa44e4493773f96b10bd7dfaed03fb551d1f4dc9e4356df7fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922cb30c2ef6e49ba0ca8cb83f925f2194c2c0ada2cf3ad317f62dddafe4cdd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6198a37abc3a99bffc67a3cd9f01076e770930130a5c303cd7e824d9dd0579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae8f1bdfffd9f9b718d7edf8ddb46dcc65251a60d390b3a7bc8e89c1fc35a306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3051c4bd1e6f383107df472d8ad03a56ed3a9e7873f849e9415558587e8cd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__108c4e635ab36e2966c8ba11f4d273787261ff35ed2d526b6617de92c58fc577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e587380a5c9acf4679727913313a5d865110054501303a8b68507a493b207f73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4170dee0b132aaf914cd4e7af57ad25d8ff9858c79269522b107e3d3b238ab6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        value = SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @jsii.member(jsii_name="resetLifecycleConfigArns")
    def reset_lifecycle_config_arns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArns", []))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(
        self,
    ) -> SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageList:
        return typing.cast(SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageList, jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage]]], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnsInput")
    def lifecycle_config_arns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "lifecycleConfigArnsInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArns")
    def lifecycle_config_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "lifecycleConfigArns"))

    @lifecycle_config_arns.setter
    def lifecycle_config_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d248292137757892ed6199e5f5dd4339a909232eb5b01b1ff0173a1895ca1f11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArns", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9307c745050c101ac0226aea8fe94e9e6f50fb1c06c167920907f6912e5bc3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cdeb5bc01fb7e56f1db72a71587b9d74794c7926ec85bbee5255cea15106bbb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCanvasAppSettings")
    def put_canvas_app_settings(
        self,
        *,
        time_series_forecasting_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param time_series_forecasting_settings: time_series_forecasting_settings block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#time_series_forecasting_settings SagemakerDomain#time_series_forecasting_settings}
        '''
        value = SagemakerDomainDefaultUserSettingsCanvasAppSettings(
            time_series_forecasting_settings=time_series_forecasting_settings
        )

        return typing.cast(None, jsii.invoke(self, "putCanvasAppSettings", [value]))

    @jsii.member(jsii_name="putJupyterServerAppSettings")
    def put_jupyter_server_app_settings(
        self,
        *,
        code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param code_repository: code_repository block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#code_repository SagemakerDomain#code_repository}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        value = SagemakerDomainDefaultUserSettingsJupyterServerAppSettings(
            code_repository=code_repository,
            default_resource_spec=default_resource_spec,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putJupyterServerAppSettings", [value]))

    @jsii.member(jsii_name="putKernelGatewayAppSettings")
    def put_kernel_gateway_app_settings(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
        lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        :param lifecycle_config_arns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arns SagemakerDomain#lifecycle_config_arns}.
        '''
        value = SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings(
            custom_image=custom_image,
            default_resource_spec=default_resource_spec,
            lifecycle_config_arns=lifecycle_config_arns,
        )

        return typing.cast(None, jsii.invoke(self, "putKernelGatewayAppSettings", [value]))

    @jsii.member(jsii_name="putRSessionAppSettings")
    def put_r_session_app_settings(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        value = SagemakerDomainDefaultUserSettingsRSessionAppSettings(
            custom_image=custom_image, default_resource_spec=default_resource_spec
        )

        return typing.cast(None, jsii.invoke(self, "putRSessionAppSettings", [value]))

    @jsii.member(jsii_name="putSharingSettings")
    def put_sharing_settings(
        self,
        *,
        notebook_output_option: typing.Optional[builtins.str] = None,
        s3_kms_key_id: typing.Optional[builtins.str] = None,
        s3_output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notebook_output_option: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#notebook_output_option SagemakerDomain#notebook_output_option}.
        :param s3_kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#s3_kms_key_id SagemakerDomain#s3_kms_key_id}.
        :param s3_output_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#s3_output_path SagemakerDomain#s3_output_path}.
        '''
        value = SagemakerDomainDefaultUserSettingsSharingSettings(
            notebook_output_option=notebook_output_option,
            s3_kms_key_id=s3_kms_key_id,
            s3_output_path=s3_output_path,
        )

        return typing.cast(None, jsii.invoke(self, "putSharingSettings", [value]))

    @jsii.member(jsii_name="putTensorBoardAppSettings")
    def put_tensor_board_app_settings(
        self,
        *,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        value = SagemakerDomainDefaultUserSettingsTensorBoardAppSettings(
            default_resource_spec=default_resource_spec
        )

        return typing.cast(None, jsii.invoke(self, "putTensorBoardAppSettings", [value]))

    @jsii.member(jsii_name="resetCanvasAppSettings")
    def reset_canvas_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanvasAppSettings", []))

    @jsii.member(jsii_name="resetJupyterServerAppSettings")
    def reset_jupyter_server_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJupyterServerAppSettings", []))

    @jsii.member(jsii_name="resetKernelGatewayAppSettings")
    def reset_kernel_gateway_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKernelGatewayAppSettings", []))

    @jsii.member(jsii_name="resetRSessionAppSettings")
    def reset_r_session_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRSessionAppSettings", []))

    @jsii.member(jsii_name="resetSecurityGroups")
    def reset_security_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroups", []))

    @jsii.member(jsii_name="resetSharingSettings")
    def reset_sharing_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharingSettings", []))

    @jsii.member(jsii_name="resetTensorBoardAppSettings")
    def reset_tensor_board_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTensorBoardAppSettings", []))

    @builtins.property
    @jsii.member(jsii_name="canvasAppSettings")
    def canvas_app_settings(
        self,
    ) -> SagemakerDomainDefaultUserSettingsCanvasAppSettingsOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsCanvasAppSettingsOutputReference, jsii.get(self, "canvasAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettings")
    def jupyter_server_app_settings(
        self,
    ) -> SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsOutputReference, jsii.get(self, "jupyterServerAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettings")
    def kernel_gateway_app_settings(
        self,
    ) -> SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsOutputReference, jsii.get(self, "kernelGatewayAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="rSessionAppSettings")
    def r_session_app_settings(
        self,
    ) -> "SagemakerDomainDefaultUserSettingsRSessionAppSettingsOutputReference":
        return typing.cast("SagemakerDomainDefaultUserSettingsRSessionAppSettingsOutputReference", jsii.get(self, "rSessionAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="sharingSettings")
    def sharing_settings(
        self,
    ) -> "SagemakerDomainDefaultUserSettingsSharingSettingsOutputReference":
        return typing.cast("SagemakerDomainDefaultUserSettingsSharingSettingsOutputReference", jsii.get(self, "sharingSettings"))

    @builtins.property
    @jsii.member(jsii_name="tensorBoardAppSettings")
    def tensor_board_app_settings(
        self,
    ) -> "SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsOutputReference":
        return typing.cast("SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsOutputReference", jsii.get(self, "tensorBoardAppSettings"))

    @builtins.property
    @jsii.member(jsii_name="canvasAppSettingsInput")
    def canvas_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettings], jsii.get(self, "canvasAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleInput")
    def execution_role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleInput"))

    @builtins.property
    @jsii.member(jsii_name="jupyterServerAppSettingsInput")
    def jupyter_server_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings], jsii.get(self, "jupyterServerAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="kernelGatewayAppSettingsInput")
    def kernel_gateway_app_settings_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings], jsii.get(self, "kernelGatewayAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="rSessionAppSettingsInput")
    def r_session_app_settings_input(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsRSessionAppSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsRSessionAppSettings"], jsii.get(self, "rSessionAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupsInput")
    def security_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="sharingSettingsInput")
    def sharing_settings_input(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsSharingSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsSharingSettings"], jsii.get(self, "sharingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="tensorBoardAppSettingsInput")
    def tensor_board_app_settings_input(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsTensorBoardAppSettings"]:
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsTensorBoardAppSettings"], jsii.get(self, "tensorBoardAppSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRole"))

    @execution_role.setter
    def execution_role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8465d7444351704ca534740b19c2a8c13034236b21f8a7c4ebc0f24beec7a111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRole", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroups"))

    @security_groups.setter
    def security_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0880e0a4aa8fad5644c3448dab53ee800b160b7881bafd387e242998730595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerDomainDefaultUserSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b3f40ae5d735cec98f3cca2a067ba5f6b2fdd5c45abf72bbd72868598a9ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettings",
    jsii_struct_bases=[],
    name_mapping={
        "custom_image": "customImage",
        "default_resource_spec": "defaultResourceSpec",
    },
)
class SagemakerDomainDefaultUserSettingsRSessionAppSettings:
    def __init__(
        self,
        *,
        custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param custom_image: custom_image block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86781476dec833bc7f5313b29b22e789caf48b521446b7e7d1b1b28634ae3bf9)
            check_type(argname="argument custom_image", value=custom_image, expected_type=type_hints["custom_image"])
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_image is not None:
            self._values["custom_image"] = custom_image
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec

    @builtins.property
    def custom_image(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage"]]]:
        '''custom_image block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#custom_image SagemakerDomain#custom_image}
        '''
        result = self._values.get("custom_image")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage"]]], result)

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsRSessionAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage",
    jsii_struct_bases=[],
    name_mapping={
        "app_image_config_name": "appImageConfigName",
        "image_name": "imageName",
        "image_version_number": "imageVersionNumber",
    },
)
class SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage:
    def __init__(
        self,
        *,
        app_image_config_name: builtins.str,
        image_name: builtins.str,
        image_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param app_image_config_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_image_config_name SagemakerDomain#app_image_config_name}.
        :param image_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_name SagemakerDomain#image_name}.
        :param image_version_number: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_version_number SagemakerDomain#image_version_number}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb206d52b9d39a3d5c8360ccb1f8dd6414f95e677febd3b2bb3f97bf3640173)
            check_type(argname="argument app_image_config_name", value=app_image_config_name, expected_type=type_hints["app_image_config_name"])
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_version_number", value=image_version_number, expected_type=type_hints["image_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_image_config_name": app_image_config_name,
            "image_name": image_name,
        }
        if image_version_number is not None:
            self._values["image_version_number"] = image_version_number

    @builtins.property
    def app_image_config_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#app_image_config_name SagemakerDomain#app_image_config_name}.'''
        result = self._values.get("app_image_config_name")
        assert result is not None, "Required property 'app_image_config_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_name SagemakerDomain#image_name}.'''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_version_number(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#image_version_number SagemakerDomain#image_version_number}.'''
        result = self._values.get("image_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f14805608c799191283dccb2d456e556d3efa8306da818a466b3daff4de228)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__682573eae243f5891f129bb9a23719d06aee8b334c624cc35af864d5a5eee0ff)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__939d5e0864b53e9e4f9d3596b9976087591384e243db1cee0df8269f3e9331c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31aaf944a1a8ff6dd7fca7d2e83ba83191a87850bd7a7d86dd9229d2a3c71783)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef62a43d30180370c930cd0d3d8ab7c29de21cde1031739f0d1bb97c221a26b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6557a68b36e64750cacb82a99178f40aa61340fc02df08124ce0ff6f81cc6cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__db261c6b6238541e4a8499c0c5333bc414980c86808c684c111e4a579150ffc7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetImageVersionNumber")
    def reset_image_version_number(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetImageVersionNumber", []))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigNameInput")
    def app_image_config_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appImageConfigNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumberInput")
    def image_version_number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "imageVersionNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="appImageConfigName")
    def app_image_config_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appImageConfigName"))

    @app_image_config_name.setter
    def app_image_config_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1065bf6fb69db0140f23f78b37c057e96f9c20f1dd976e106b3b1bcadccc8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appImageConfigName", value)

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b4578a918619380ddc03f862e0aa3d0f0f1a691bfa43e932513d00ed93a03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value)

    @builtins.property
    @jsii.member(jsii_name="imageVersionNumber")
    def image_version_number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "imageVersionNumber"))

    @image_version_number.setter
    def image_version_number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d80c779737e880e633cca5075ac67e76b00501eafee4aa2ec4ea5a5fcf6c3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageVersionNumber", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b303d2ae5258e390a07f039cffa559ef214456f7490e695d4737c6ec2cf5305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad37d8e183a97234d2d46d73891376072202857f186b75bd341b61a9c4cced5c)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50012167398576fa9034208afe2eabda25d17bce7c997ff66258b57d1a72dc38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2d9af20eac4dda672737c5c1ff874e86d403288d75226a3dff4ffee7527def)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1327b181d38b30db79b3c32745e9c19e228c5ce81257622cc842363e304ff36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39029cd911f5145d9cc70e5c7b68c58479f758ddcbe9487ea5072639caae4f2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86b2ed22f72ac68f3f5777c97ff15feae9f8283223edcf481b5ed76063bb035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d6ecf0360be4dc024aadbd1e47b2e54ea294e89a83c012e00aee8b5e44b6943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsRSessionAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsRSessionAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1c9e871312b9b41229f7b876957736cc20559593d21f59da0fcfa68e102e846)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putCustomImage")
    def put_custom_image(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fde7a2846cb4f7713d9a018f701980d5b2f0f769d5c42fefd268c3428249620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomImage", [value]))

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        value = SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetCustomImage")
    def reset_custom_image(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomImage", []))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @builtins.property
    @jsii.member(jsii_name="customImage")
    def custom_image(
        self,
    ) -> SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageList:
        return typing.cast(SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageList, jsii.get(self, "customImage"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="customImageInput")
    def custom_image_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage]]], jsii.get(self, "customImageInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3dc17b5fcb1d7f2ac57344499500afddc6a21ff4c119009d9e8143efbf6914e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsSharingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "notebook_output_option": "notebookOutputOption",
        "s3_kms_key_id": "s3KmsKeyId",
        "s3_output_path": "s3OutputPath",
    },
)
class SagemakerDomainDefaultUserSettingsSharingSettings:
    def __init__(
        self,
        *,
        notebook_output_option: typing.Optional[builtins.str] = None,
        s3_kms_key_id: typing.Optional[builtins.str] = None,
        s3_output_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param notebook_output_option: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#notebook_output_option SagemakerDomain#notebook_output_option}.
        :param s3_kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#s3_kms_key_id SagemakerDomain#s3_kms_key_id}.
        :param s3_output_path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#s3_output_path SagemakerDomain#s3_output_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7c40a3ad77da03f4acd5c6e595254050d086a913ba8320f8e2d740af1b6b76)
            check_type(argname="argument notebook_output_option", value=notebook_output_option, expected_type=type_hints["notebook_output_option"])
            check_type(argname="argument s3_kms_key_id", value=s3_kms_key_id, expected_type=type_hints["s3_kms_key_id"])
            check_type(argname="argument s3_output_path", value=s3_output_path, expected_type=type_hints["s3_output_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if notebook_output_option is not None:
            self._values["notebook_output_option"] = notebook_output_option
        if s3_kms_key_id is not None:
            self._values["s3_kms_key_id"] = s3_kms_key_id
        if s3_output_path is not None:
            self._values["s3_output_path"] = s3_output_path

    @builtins.property
    def notebook_output_option(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#notebook_output_option SagemakerDomain#notebook_output_option}.'''
        result = self._values.get("notebook_output_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#s3_kms_key_id SagemakerDomain#s3_kms_key_id}.'''
        result = self._values.get("s3_kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_output_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#s3_output_path SagemakerDomain#s3_output_path}.'''
        result = self._values.get("s3_output_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsSharingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsSharingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsSharingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6395f9bd89a48071e7ea065be50d3febc76b4eda4e8d5ecc04288009b38c7897)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetNotebookOutputOption")
    def reset_notebook_output_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotebookOutputOption", []))

    @jsii.member(jsii_name="resetS3KmsKeyId")
    def reset_s3_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3KmsKeyId", []))

    @jsii.member(jsii_name="resetS3OutputPath")
    def reset_s3_output_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3OutputPath", []))

    @builtins.property
    @jsii.member(jsii_name="notebookOutputOptionInput")
    def notebook_output_option_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notebookOutputOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KmsKeyIdInput")
    def s3_kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="s3OutputPathInput")
    def s3_output_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3OutputPathInput"))

    @builtins.property
    @jsii.member(jsii_name="notebookOutputOption")
    def notebook_output_option(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notebookOutputOption"))

    @notebook_output_option.setter
    def notebook_output_option(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1bea6f186c35e8bfce4cc95069dac683fd7aa8e1b22f8ffc4cf36c1d6a8c0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notebookOutputOption", value)

    @builtins.property
    @jsii.member(jsii_name="s3KmsKeyId")
    def s3_kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3KmsKeyId"))

    @s3_kms_key_id.setter
    def s3_kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2311415bccd37930d74a527967012fee008a5f3046cadc07ec907b4bba3e4172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="s3OutputPath")
    def s3_output_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3OutputPath"))

    @s3_output_path.setter
    def s3_output_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2da44edc662993e6baea05c97cb05afe7758973d7b5d02d8102877433c387183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3OutputPath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsSharingSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsSharingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsSharingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb8f0bc9e09a8e2a151c94788c94bca2842b3b06f3f1dcea96399431889c2d9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsTensorBoardAppSettings",
    jsii_struct_bases=[],
    name_mapping={"default_resource_spec": "defaultResourceSpec"},
)
class SagemakerDomainDefaultUserSettingsTensorBoardAppSettings:
    def __init__(
        self,
        *,
        default_resource_spec: typing.Optional[typing.Union["SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param default_resource_spec: default_resource_spec block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        if isinstance(default_resource_spec, dict):
            default_resource_spec = SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec(**default_resource_spec)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e473d2bc935ecb17237040690899e69f7c981fc283a0b4fb789c122cf602283)
            check_type(argname="argument default_resource_spec", value=default_resource_spec, expected_type=type_hints["default_resource_spec"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_resource_spec is not None:
            self._values["default_resource_spec"] = default_resource_spec

    @builtins.property
    def default_resource_spec(
        self,
    ) -> typing.Optional["SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec"]:
        '''default_resource_spec block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#default_resource_spec SagemakerDomain#default_resource_spec}
        '''
        result = self._values.get("default_resource_spec")
        return typing.cast(typing.Optional["SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsTensorBoardAppSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "lifecycle_config_arn": "lifecycleConfigArn",
        "sagemaker_image_arn": "sagemakerImageArn",
        "sagemaker_image_version_arn": "sagemakerImageVersionArn",
    },
)
class SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec:
    def __init__(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07ba0fade427ddb4588b646052faab6eaa3c37f8d26f581817c645abbaaca0e)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument lifecycle_config_arn", value=lifecycle_config_arn, expected_type=type_hints["lifecycle_config_arn"])
            check_type(argname="argument sagemaker_image_arn", value=sagemaker_image_arn, expected_type=type_hints["sagemaker_image_arn"])
            check_type(argname="argument sagemaker_image_version_arn", value=sagemaker_image_version_arn, expected_type=type_hints["sagemaker_image_version_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if lifecycle_config_arn is not None:
            self._values["lifecycle_config_arn"] = lifecycle_config_arn
        if sagemaker_image_arn is not None:
            self._values["sagemaker_image_arn"] = sagemaker_image_arn
        if sagemaker_image_version_arn is not None:
            self._values["sagemaker_image_version_arn"] = sagemaker_image_version_arn

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lifecycle_config_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.'''
        result = self._values.get("lifecycle_config_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.'''
        result = self._values.get("sagemaker_image_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sagemaker_image_version_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.'''
        result = self._values.get("sagemaker_image_version_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73569698a0f5a27d5ab405af5a93909233ce651d6f98f247a3fcffeb4f392456)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetLifecycleConfigArn")
    def reset_lifecycle_config_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLifecycleConfigArn", []))

    @jsii.member(jsii_name="resetSagemakerImageArn")
    def reset_sagemaker_image_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageArn", []))

    @jsii.member(jsii_name="resetSagemakerImageVersionArn")
    def reset_sagemaker_image_version_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSagemakerImageVersionArn", []))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArnInput")
    def lifecycle_config_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lifecycleConfigArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArnInput")
    def sagemaker_image_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageArnInput"))

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArnInput")
    def sagemaker_image_version_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sagemakerImageVersionArnInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc22ad176279e676ddd6f71f23bee51bebd131a0206530c8db8631eeafed7259)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycleConfigArn")
    def lifecycle_config_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lifecycleConfigArn"))

    @lifecycle_config_arn.setter
    def lifecycle_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f64ac190c18bc3a9f5b043b37a05cd657bffd7f13c3acad6fb1731da0cab0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lifecycleConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageArn")
    def sagemaker_image_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageArn"))

    @sagemaker_image_arn.setter
    def sagemaker_image_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__512c33399d42c771e115724aed2e4a7d9392192cd2c723dac2be495d32d7be4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageArn", value)

    @builtins.property
    @jsii.member(jsii_name="sagemakerImageVersionArn")
    def sagemaker_image_version_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sagemakerImageVersionArn"))

    @sagemaker_image_version_arn.setter
    def sagemaker_image_version_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37372960ef3a7c72dd74e10c8f72702671625cc72ce2902faceb2b72420aa1e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sagemakerImageVersionArn", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bae351b254d6af0343910e1aea2ad59f00463a796bcfab878842cfcb0e7ca0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3637966a383ad7068377d013477a0ab3aa3680cd9670bf7c3d5c0282e722625f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDefaultResourceSpec")
    def put_default_resource_spec(
        self,
        *,
        instance_type: typing.Optional[builtins.str] = None,
        lifecycle_config_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_arn: typing.Optional[builtins.str] = None,
        sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#instance_type SagemakerDomain#instance_type}.
        :param lifecycle_config_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#lifecycle_config_arn SagemakerDomain#lifecycle_config_arn}.
        :param sagemaker_image_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_arn SagemakerDomain#sagemaker_image_arn}.
        :param sagemaker_image_version_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#sagemaker_image_version_arn SagemakerDomain#sagemaker_image_version_arn}.
        '''
        value = SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec(
            instance_type=instance_type,
            lifecycle_config_arn=lifecycle_config_arn,
            sagemaker_image_arn=sagemaker_image_arn,
            sagemaker_image_version_arn=sagemaker_image_version_arn,
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultResourceSpec", [value]))

    @jsii.member(jsii_name="resetDefaultResourceSpec")
    def reset_default_resource_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResourceSpec", []))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpec")
    def default_resource_spec(
        self,
    ) -> SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference:
        return typing.cast(SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference, jsii.get(self, "defaultResourceSpec"))

    @builtins.property
    @jsii.member(jsii_name="defaultResourceSpecInput")
    def default_resource_spec_input(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec], jsii.get(self, "defaultResourceSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85978b80c40a0a9556a063c382fdcaf0d83febfc28f13b73bb5e3844de6d36ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDomainSettings",
    jsii_struct_bases=[],
    name_mapping={
        "execution_role_identity_config": "executionRoleIdentityConfig",
        "security_group_ids": "securityGroupIds",
    },
)
class SagemakerDomainDomainSettings:
    def __init__(
        self,
        *,
        execution_role_identity_config: typing.Optional[builtins.str] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param execution_role_identity_config: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role_identity_config SagemakerDomain#execution_role_identity_config}.
        :param security_group_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_group_ids SagemakerDomain#security_group_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c83a351af09bb58599dd39ed826ce730509febf98eb3581e9fa5078ebd0f94)
            check_type(argname="argument execution_role_identity_config", value=execution_role_identity_config, expected_type=type_hints["execution_role_identity_config"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execution_role_identity_config is not None:
            self._values["execution_role_identity_config"] = execution_role_identity_config
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids

    @builtins.property
    def execution_role_identity_config(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#execution_role_identity_config SagemakerDomain#execution_role_identity_config}.'''
        result = self._values.get("execution_role_identity_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#security_group_ids SagemakerDomain#security_group_ids}.'''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainDomainSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainDomainSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainDomainSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd721467973610c3765a6f487a860e627c83e975114253bc21ef785c99f007e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExecutionRoleIdentityConfig")
    def reset_execution_role_identity_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionRoleIdentityConfig", []))

    @jsii.member(jsii_name="resetSecurityGroupIds")
    def reset_security_group_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecurityGroupIds", []))

    @builtins.property
    @jsii.member(jsii_name="executionRoleIdentityConfigInput")
    def execution_role_identity_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleIdentityConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIdsInput")
    def security_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleIdentityConfig")
    def execution_role_identity_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionRoleIdentityConfig"))

    @execution_role_identity_config.setter
    def execution_role_identity_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09d9b288854d2ecdbd3f2130fc3c2090557263688b118d35556a6a1c27fb2fd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionRoleIdentityConfig", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e100a7d3817d8ef29add287036d05282655e7c85b0155661be677609c388ab6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerDomainDomainSettings]:
        return typing.cast(typing.Optional[SagemakerDomainDomainSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainDomainSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54c0fbd698557c2c11e03e90ba09ec441bd4e4a843eee51eae6eab5ce724550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"home_efs_file_system": "homeEfsFileSystem"},
)
class SagemakerDomainRetentionPolicy:
    def __init__(
        self,
        *,
        home_efs_file_system: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param home_efs_file_system: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#home_efs_file_system SagemakerDomain#home_efs_file_system}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cc831ec4b2ad3194d473404d7e76df9ef05a30e3802d034e2bc07254753750)
            check_type(argname="argument home_efs_file_system", value=home_efs_file_system, expected_type=type_hints["home_efs_file_system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if home_efs_file_system is not None:
            self._values["home_efs_file_system"] = home_efs_file_system

    @builtins.property
    def home_efs_file_system(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/sagemaker_domain#home_efs_file_system SagemakerDomain#home_efs_file_system}.'''
        result = self._values.get("home_efs_file_system")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SagemakerDomainRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SagemakerDomainRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.sagemakerDomain.SagemakerDomainRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc9a2dc2e0e95dc9e79a3ee2220ffa7da5e9c08bee9ddf3a35a260871e13dc5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHomeEfsFileSystem")
    def reset_home_efs_file_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHomeEfsFileSystem", []))

    @builtins.property
    @jsii.member(jsii_name="homeEfsFileSystemInput")
    def home_efs_file_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "homeEfsFileSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="homeEfsFileSystem")
    def home_efs_file_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "homeEfsFileSystem"))

    @home_efs_file_system.setter
    def home_efs_file_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1aab089434861562c491e7d94b48b97ac1c2c5b39d71f50997eb5db8eb2441e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "homeEfsFileSystem", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SagemakerDomainRetentionPolicy]:
        return typing.cast(typing.Optional[SagemakerDomainRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SagemakerDomainRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9330090e8b06a7b60a26ea6492d206e3379f62e24d1484096884735fa26712a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SagemakerDomain",
    "SagemakerDomainConfig",
    "SagemakerDomainDefaultSpaceSettings",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryList",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsOutputReference",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageList",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImageOutputReference",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsOutputReference",
    "SagemakerDomainDefaultSpaceSettingsOutputReference",
    "SagemakerDomainDefaultUserSettings",
    "SagemakerDomainDefaultUserSettingsCanvasAppSettings",
    "SagemakerDomainDefaultUserSettingsCanvasAppSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings",
    "SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettings",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryList",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepositoryOutputReference",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageList",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImageOutputReference",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettings",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageList",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImageOutputReference",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerDomainDefaultUserSettingsRSessionAppSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsSharingSettings",
    "SagemakerDomainDefaultUserSettingsSharingSettingsOutputReference",
    "SagemakerDomainDefaultUserSettingsTensorBoardAppSettings",
    "SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec",
    "SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpecOutputReference",
    "SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsOutputReference",
    "SagemakerDomainDomainSettings",
    "SagemakerDomainDomainSettingsOutputReference",
    "SagemakerDomainRetentionPolicy",
    "SagemakerDomainRetentionPolicyOutputReference",
]

publication.publish()

def _typecheckingstub__c4c0a93de0d35c0e7b09853a9b719d3e76946cb5fe438d32f00e5258d57afd22(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    auth_mode: builtins.str,
    default_user_settings: typing.Union[SagemakerDomainDefaultUserSettings, typing.Dict[builtins.str, typing.Any]],
    domain_name: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
    app_network_access_type: typing.Optional[builtins.str] = None,
    app_security_group_management: typing.Optional[builtins.str] = None,
    default_space_settings: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_settings: typing.Optional[typing.Union[SagemakerDomainDomainSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[SagemakerDomainRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__a789ed68ecb4037790f455759a9cbd9341c68006db9340da0b5d74cf669f5d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd18bf0f20147152f18870038a0be061b0c302f1a1dbc3f5f9d4e047ad36427(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7b2bfd6dcb0215fe8f736f167d9e1f1920c2a8610faeef276ba2fcebfae416(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591bc38cf28322f31eefbc8553b5bbf93015f8daa5f368491a380f727f4c9c0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b962faa6c9afa45286174e0fb8dd041a619758e1cd5c02f7f9c884264321a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__660452657ee41967303b7e3b8771baeaf8b382468c79a2c856f053486db8200a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330e095be22d7d00793a78483dd25c32f3b94aba03d03470918341187383c42d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b556e1c7b545509f192c97858addc88086ac72e9761400bda96efcbc045662f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fda591cc3cbf7d718c2f408297e77b84cf04230459b9191dc4b839fbd2b820(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57c43629bcf879992cbe07042429c54bffeef4f5fe0a1b1a94d6854597348eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43f96c45f8a18112a22a83fa64c5d02568d4b1364e8dc31b5ca7bb65c3a3429(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    auth_mode: builtins.str,
    default_user_settings: typing.Union[SagemakerDomainDefaultUserSettings, typing.Dict[builtins.str, typing.Any]],
    domain_name: builtins.str,
    subnet_ids: typing.Sequence[builtins.str],
    vpc_id: builtins.str,
    app_network_access_type: typing.Optional[builtins.str] = None,
    app_security_group_management: typing.Optional[builtins.str] = None,
    default_space_settings: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    domain_settings: typing.Optional[typing.Union[SagemakerDomainDomainSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    retention_policy: typing.Optional[typing.Union[SagemakerDomainRetentionPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270b7279a9cbea10aa26e9039ab79156a040f4997553838d2e7c1daeb3b9d1cf(
    *,
    execution_role: builtins.str,
    jupyter_server_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kernel_gateway_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3872dcdb3e01c906ef847747b58be3fb9c3ca79eef6a22df01e5e001976726fc(
    *,
    code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f959bc2fedcf6898c2a91a2ee854ed6de47cd305a477ed7188e6c73d16865706(
    *,
    repository_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f359bc937d0841dc9083f39dc97135b658ce4a1a1d52326755e9dbc1647c7394(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc388bfc93c4bad0b45629abc410da2fc72e2a040bd70f09243dfffe272290f2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772c1f6b4a9f32dd8c6e2a1f5a702b95475a4196eab0cdd34864371fb31bf312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4c3249b0b37afc25fba5e2e77f13fb9968f6607566c48f97995edd81ccfe5d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5688303d2931399ace6f453c36158605e9740e4e80ee445544fc4c735cb848(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923ccd2f70b66b09d098843f7ded3ee75deccc9865f69b1f6e183c9efe1f0be5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e449366bdda7b2d15e660de0295c7638ab7126fb287febed3a4d55c2df328a22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__946e2d39dc3779371d9f3e3c765b38da67879e8e2effd2fe418920c1e8bcd6ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0efa7a4e99ece534ef2c53bf911252a153c0b7f9d1946429c49395da8ee2cdd(
    value: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3456985365b9b55660a17fb07083eec3fb4acd57c293b79cba3f0e010b889eb(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6845dbc45245ec5dc1210f0bf601799d646dd7ce973b90d6d0c03017e11abcf1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457c5d78c7b7213a17b3ed1d2a635b69f031d6773cef50c4ae7dcfb32349a586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafee40090da458adf628290ad08fc1dd4924c59d7fad87a2b8b365a12dfe919(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99cc59c0d3d9d5bf5c6447141f307af105580ba06e925e821b2e1b4601e93a65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e817670822f005f757f880aaf3fe66f1bbac3e06dc7ac6681c5cc454d85c38cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a91e305e8c80459a155db9bc9d316678e45d8671e4a14c06f9fbffcd7254ef(
    value: typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448878be6a666d72e1a395d1696824401dc8dfccf9e430d1706bb21b06b8f67e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ff5ee10c90a44526d9b508b755b6de11e58d3c5648f96b241e3d8ffb489d48(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b09653a47b5c3a7f0e0dd81606a33752db1a796fa8c7261d02bfa5130eba394(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99152b9381588c93fdc896e1a68e03a8c0b0b5700ee1266feabfb91a843e5b97(
    value: typing.Optional[SagemakerDomainDefaultSpaceSettingsJupyterServerAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa901fe75ae3242f4c2215186bf54d34004a4608317993bdfbb61c3b8395f7a4(
    *,
    custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f73d7586f80f54c528e4e2f6fb07fae7ffa3a28e1b2c274bd7d1c929c9d0a6(
    *,
    app_image_config_name: builtins.str,
    image_name: builtins.str,
    image_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3c971f9cc655e8b9ef2f4ca5ed02f304c40711a756174ff1572cb947ace0ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27395f3c4f3fd290554296af6248c8063157c82ae64b9f21cf9db7bc93f0548d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc444000d22481e54c44fc695c832d93ab0b5fd13c25ee99b8a9837b35be435(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf1e2cea1d9cc347ff606c75d722c955a6c840b76f4738ec6c6219e300a6a9b6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b862475f7bbfff074c63909eafd40b77b55c2a377a41e503eb92c02f8d567ee7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3f2982358c8c869c687f96fda51d6bb2092cb525de14307867e123054d74ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f699e4c80c8efc166f9c68b708047d44281a6c5e5880e3fb4b3bfc47642ddb4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92863c155c5c0ff1ad2e695913a3754a3ce84dbce6e6a1a965dfc4049b087f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d582af55749b381b26b19fa20b8b0171661f0681682ae347cf422343a70531(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa122e63ff116ad0e4c2ec994112c15b236c5f281168e51527cd5e2a7348118(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6b1ad9aaf705493d1cf5a53cfb5dffa0c0a1b3bf32aaeee053ba267283219ae(
    value: typing.Optional[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117c188b135c26e518901a6af08509bb6318fba74ac4ff2aafbbba8b976b9ae3(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d9b16bf6747c14653a620e64893408726c2b202e7f81ef09ca0cd6e04e3116(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f836b257a17d439bf44cbe75cec2968618b6dad8c7cfe3e64ed131bd181c4ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f552678d0a1294405036b28a66c0511724aeb4a3d62d29bdaf70b92b78a18c63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6939d576ae803045cbbfa0f702ec82d1bfb7924d17961842e23686f280b65286(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6959e309e05f0c2312072cb2d1f39aa0974f33f15673d62258ef249fc1c7d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbf15f32f3efbe7e3418f454b238b491b4b063ad7ab8059522dc2c9c0e8047b(
    value: typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba6806af7b4f01b53443c893b21b63fd32619cadb005a56b0dc302d491467df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb5c829d77fdd180ac95c7568b4ee295618c23dea4b9fa163ac90d760a68ea2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb13731b3dda6a4d24e04c74f5e04f8c7be0e36693ca0e2ad9d9ee5d3f34909(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e49ae4ff3dc2b2c5215f214ec484171e9c2b79a43dc6045e8c867e68843d60(
    value: typing.Optional[SagemakerDomainDefaultSpaceSettingsKernelGatewayAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667e3807e751393f76efec20d25f567f726fa47cb41ed8f21b7b903053efb0aa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad8936ddf1ee50477399fa5461105e653694c3ebb2268226a8175f1304cea442(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfe6a18b9873260791c78374928c5c14b478bb904f6b4a4665d884330b5407c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe68495c3d220beda59e522aa606bf30647e5fc521595f65843f7ada282f3ac(
    value: typing.Optional[SagemakerDomainDefaultSpaceSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03d83a3719284499df4f62cb251e309d8366a16f13707636601d23784e265c8(
    *,
    execution_role: builtins.str,
    canvas_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsCanvasAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    jupyter_server_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    kernel_gateway_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    r_session_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    sharing_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsSharingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    tensor_board_app_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsTensorBoardAppSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944bdbdc4f6cd2e2618aa6c9206b9c9e91770b5175bf3c84dbac0fedb5afe965(
    *,
    time_series_forecasting_settings: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af5879b43d76e99a2256723ccbb9f5395f1e19ee7901778b11d6d2f3da3181b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae6372baf99c8e396c70f49a5a7bb6f397613ba0ecec62b8c88267bf64f1124(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6c86eee750eb3305a2843880a68afeb17e40f33aeb902f7f39cf845dc9665a(
    *,
    amazon_forecast_role_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10787220583c3c78b149c8dcf8eabab4365081ba7d0201e5aa9041e0e3da67d8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941ff61d7d08324d383e8e0dc6d10cb1eac1f3a420db2a8d592e1bb13bf409f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5930838c7a99d9a1a7fdc171f2095357e0a1c9eadffb6a1ac61828e8fdd00651(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b0a1baf47476027935d9c7723814c1bcb32dc0d715cc93ae5043165a356833(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsCanvasAppSettingsTimeSeriesForecastingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a742cdbbe567a32d826407ec0b52b4d91299d09251932e37c1ada0b9352bc82(
    *,
    code_repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c902c75b8b4ba7b2333d71ad6b8e972286518683fbbc1b0617ff7afee1ea22(
    *,
    repository_url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed3f8351bff2753c31d5c9fbfcef7c7177fc9a29e2185475df228f4027ea6c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cade65acbe0978ba775f6a246bea72d33efb55f76b1193aa6427c376c33fe7c2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966045a478a95050488ed41d9aa91e78bb20ede9a108c3ed0e1b2fdc25389e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52793615f2bf8f43804936628dfe985c18f8a87a55f371535a451586e93c716(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a590d58a5037b2482e939af85908dd7d06d0f39fed0286afd46e6f73151601(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736fdce35a78b6768cbec74582bb021d32a791c0fe9ea8f8b677c75651794d50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c846e351046a06aca12016e7e79cf24d1bee940e69bbd30bb67e27eb656b443(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c44e2c2c948b6f7d13d49dc869ac4a2dcda9f1a94ef394cc4f28e1644efdbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d822fc2cea4385c1116bc07f2d9d97b026aadb8f9952b6c72f77f320ff1530c0(
    value: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b014fb3b00c194db2abf8d5b991e4bb73f10e549b8a85055a51f11fe8ba556(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1f3ce3aa10a23744951fab0f82f53b9316ec3541dc4711026b73d87c63dc26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b40c4a22230b16995e8019d807d5f4864f24551f7c94fd34e2e26959309ddf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec88bd8141f60ed3b1b57d622c1f93658aa731d67ae33dc808e7d2beac216c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81081ca54cc689a799b407f445eded9b9ffcad2ece6befc08f5d31331b0adce7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50566befde93daa7bfbb6eaf9dfd30bc80e0bb9733d6ddf22ab7ec68c127f62c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76647c6b6f5bcb7f915c153e5fab90bd8951cb22dd7836a28ecdf79fb613230(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66cf52cc16d7ba09a624f0d92c8d5f110653685e8e649160f9d1934d11bf1d6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788c32affd538987cdf8ca73dac7dbe95dd0f16cbb4f732a6bf7f504a4ab97a1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsJupyterServerAppSettingsCodeRepository, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e04d856e19510ffa6688a969be07b5efeb21d6a47e8ab57617e6be4cd832392(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0af993cfe172d6552820711e2cbf94e1514745bf42ae2f0fd6d0e85390bfe68(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsJupyterServerAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd57ea261f000a4d4baa792c3844eb7b9050f14ca5d81270cd7f504f6d747515(
    *,
    custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
    lifecycle_config_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6f450e5f3ca430859959a8de37da435b0d120a5908810e8ac4769643ebd353(
    *,
    app_image_config_name: builtins.str,
    image_name: builtins.str,
    image_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e57474da8c2816a9ab271229b3fab532c2d84a74deafbacae15b4bf389088d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab61cd2ed59d256b8133f0b514034ecf8316bd3dbce7acbac786bce90b08697(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b76b7a16853d2f8904614323640fb83b1d256820f9e863bd08a9976943946f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c47661d164f3b541397a27b8e102d2f28e05d15956a5ce608112613bbdfd14(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d830d4046d89bf41ad775f1a3f731077c6ed2b418b55a82b93f10bba9489cdc9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6614e7dc56c86c18bbe334b0e06179fc17b8a455fc88fa49a6bd00d28432d90a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e8cf9f4407a174f21086132f1a97ae3f16587596c8171816f1db93d5ffdf79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6425966b04172ad14f26e1feb402f44785c57711f299df44b93e9e6f5b05d66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadbc1390906e31dd034f3311003d87ad4c2fa06bfb7a1bb125196a741b9e987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a6a7bd69c79bfff4f551f42edcb4405ff110f048e6a10b9aff766598737390e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85d88754ad105f8006c491641221a0522a79a000545c5db4b22a502ba80820d(
    value: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e27edb3f764dff4f7286aa101a7a30d6d0ba92f2e63956ca18b89d30dec5e9(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25257682b96d81aa44e4493773f96b10bd7dfaed03fb551d1f4dc9e4356df7fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922cb30c2ef6e49ba0ca8cb83f925f2194c2c0ada2cf3ad317f62dddafe4cdd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6198a37abc3a99bffc67a3cd9f01076e770930130a5c303cd7e824d9dd0579(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8f1bdfffd9f9b718d7edf8ddb46dcc65251a60d390b3a7bc8e89c1fc35a306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3051c4bd1e6f383107df472d8ad03a56ed3a9e7873f849e9415558587e8cd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__108c4e635ab36e2966c8ba11f4d273787261ff35ed2d526b6617de92c58fc577(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e587380a5c9acf4679727913313a5d865110054501303a8b68507a493b207f73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4170dee0b132aaf914cd4e7af57ad25d8ff9858c79269522b107e3d3b238ab6f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d248292137757892ed6199e5f5dd4339a909232eb5b01b1ff0173a1895ca1f11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9307c745050c101ac0226aea8fe94e9e6f50fb1c06c167920907f6912e5bc3d(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsKernelGatewayAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdeb5bc01fb7e56f1db72a71587b9d74794c7926ec85bbee5255cea15106bbb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8465d7444351704ca534740b19c2a8c13034236b21f8a7c4ebc0f24beec7a111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0880e0a4aa8fad5644c3448dab53ee800b160b7881bafd387e242998730595(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b3f40ae5d735cec98f3cca2a067ba5f6b2fdd5c45abf72bbd72868598a9ed5(
    value: typing.Optional[SagemakerDomainDefaultUserSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86781476dec833bc7f5313b29b22e789caf48b521446b7e7d1b1b28634ae3bf9(
    *,
    custom_image: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb206d52b9d39a3d5c8360ccb1f8dd6414f95e677febd3b2bb3f97bf3640173(
    *,
    app_image_config_name: builtins.str,
    image_name: builtins.str,
    image_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f14805608c799191283dccb2d456e556d3efa8306da818a466b3daff4de228(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__682573eae243f5891f129bb9a23719d06aee8b334c624cc35af864d5a5eee0ff(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__939d5e0864b53e9e4f9d3596b9976087591384e243db1cee0df8269f3e9331c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31aaf944a1a8ff6dd7fca7d2e83ba83191a87850bd7a7d86dd9229d2a3c71783(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef62a43d30180370c930cd0d3d8ab7c29de21cde1031739f0d1bb97c221a26b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6557a68b36e64750cacb82a99178f40aa61340fc02df08124ce0ff6f81cc6cb2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db261c6b6238541e4a8499c0c5333bc414980c86808c684c111e4a579150ffc7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1065bf6fb69db0140f23f78b37c057e96f9c20f1dd976e106b3b1bcadccc8ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b4578a918619380ddc03f862e0aa3d0f0f1a691bfa43e932513d00ed93a03c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d80c779737e880e633cca5075ac67e76b00501eafee4aa2ec4ea5a5fcf6c3ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b303d2ae5258e390a07f039cffa559ef214456f7490e695d4737c6ec2cf5305(
    value: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad37d8e183a97234d2d46d73891376072202857f186b75bd341b61a9c4cced5c(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50012167398576fa9034208afe2eabda25d17bce7c997ff66258b57d1a72dc38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2d9af20eac4dda672737c5c1ff874e86d403288d75226a3dff4ffee7527def(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1327b181d38b30db79b3c32745e9c19e228c5ce81257622cc842363e304ff36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39029cd911f5145d9cc70e5c7b68c58479f758ddcbe9487ea5072639caae4f2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86b2ed22f72ac68f3f5777c97ff15feae9f8283223edcf481b5ed76063bb035(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d6ecf0360be4dc024aadbd1e47b2e54ea294e89a83c012e00aee8b5e44b6943(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c9e871312b9b41229f7b876957736cc20559593d21f59da0fcfa68e102e846(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fde7a2846cb4f7713d9a018f701980d5b2f0f769d5c42fefd268c3428249620(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SagemakerDomainDefaultUserSettingsRSessionAppSettingsCustomImage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3dc17b5fcb1d7f2ac57344499500afddc6a21ff4c119009d9e8143efbf6914e(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsRSessionAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7c40a3ad77da03f4acd5c6e595254050d086a913ba8320f8e2d740af1b6b76(
    *,
    notebook_output_option: typing.Optional[builtins.str] = None,
    s3_kms_key_id: typing.Optional[builtins.str] = None,
    s3_output_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6395f9bd89a48071e7ea065be50d3febc76b4eda4e8d5ecc04288009b38c7897(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1bea6f186c35e8bfce4cc95069dac683fd7aa8e1b22f8ffc4cf36c1d6a8c0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2311415bccd37930d74a527967012fee008a5f3046cadc07ec907b4bba3e4172(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2da44edc662993e6baea05c97cb05afe7758973d7b5d02d8102877433c387183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb8f0bc9e09a8e2a151c94788c94bca2842b3b06f3f1dcea96399431889c2d9e(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsSharingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e473d2bc935ecb17237040690899e69f7c981fc283a0b4fb789c122cf602283(
    *,
    default_resource_spec: typing.Optional[typing.Union[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07ba0fade427ddb4588b646052faab6eaa3c37f8d26f581817c645abbaaca0e(
    *,
    instance_type: typing.Optional[builtins.str] = None,
    lifecycle_config_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_arn: typing.Optional[builtins.str] = None,
    sagemaker_image_version_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73569698a0f5a27d5ab405af5a93909233ce651d6f98f247a3fcffeb4f392456(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc22ad176279e676ddd6f71f23bee51bebd131a0206530c8db8631eeafed7259(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f64ac190c18bc3a9f5b043b37a05cd657bffd7f13c3acad6fb1731da0cab0c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512c33399d42c771e115724aed2e4a7d9392192cd2c723dac2be495d32d7be4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37372960ef3a7c72dd74e10c8f72702671625cc72ce2902faceb2b72420aa1e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bae351b254d6af0343910e1aea2ad59f00463a796bcfab878842cfcb0e7ca0(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettingsDefaultResourceSpec],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3637966a383ad7068377d013477a0ab3aa3680cd9670bf7c3d5c0282e722625f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85978b80c40a0a9556a063c382fdcaf0d83febfc28f13b73bb5e3844de6d36ff(
    value: typing.Optional[SagemakerDomainDefaultUserSettingsTensorBoardAppSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c83a351af09bb58599dd39ed826ce730509febf98eb3581e9fa5078ebd0f94(
    *,
    execution_role_identity_config: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd721467973610c3765a6f487a860e627c83e975114253bc21ef785c99f007e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d9b288854d2ecdbd3f2130fc3c2090557263688b118d35556a6a1c27fb2fd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e100a7d3817d8ef29add287036d05282655e7c85b0155661be677609c388ab6c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54c0fbd698557c2c11e03e90ba09ec441bd4e4a843eee51eae6eab5ce724550(
    value: typing.Optional[SagemakerDomainDomainSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cc831ec4b2ad3194d473404d7e76df9ef05a30e3802d034e2bc07254753750(
    *,
    home_efs_file_system: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9a2dc2e0e95dc9e79a3ee2220ffa7da5e9c08bee9ddf3a35a260871e13dc5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1aab089434861562c491e7d94b48b97ac1c2c5b39d71f50997eb5db8eb2441e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9330090e8b06a7b60a26ea6492d206e3379f62e24d1484096884735fa26712a(
    value: typing.Optional[SagemakerDomainRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass
