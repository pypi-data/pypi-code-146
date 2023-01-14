'''
# `aws_fms_policy`

Refer to the Terraform Registory for docs: [`aws_fms_policy`](https://www.terraform.io/docs/providers/aws/r/fms_policy).
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


class FmsPolicy(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicy",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/fms_policy aws_fms_policy}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        exclude_resource_tags: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        security_service_policy_data: typing.Union["FmsPolicySecurityServicePolicyData", typing.Dict[builtins.str, typing.Any]],
        delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_unused_fm_managed_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_map: typing.Optional[typing.Union["FmsPolicyExcludeMap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_map: typing.Optional[typing.Union["FmsPolicyIncludeMap", typing.Dict[builtins.str, typing.Any]]] = None,
        remediation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/fms_policy aws_fms_policy} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param exclude_resource_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#exclude_resource_tags FmsPolicy#exclude_resource_tags}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#name FmsPolicy#name}.
        :param security_service_policy_data: security_service_policy_data block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#security_service_policy_data FmsPolicy#security_service_policy_data}
        :param delete_all_policy_resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#delete_all_policy_resources FmsPolicy#delete_all_policy_resources}.
        :param delete_unused_fm_managed_resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#delete_unused_fm_managed_resources FmsPolicy#delete_unused_fm_managed_resources}.
        :param exclude_map: exclude_map block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#exclude_map FmsPolicy#exclude_map}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#id FmsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_map: include_map block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#include_map FmsPolicy#include_map}
        :param remediation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#remediation_enabled FmsPolicy#remediation_enabled}.
        :param resource_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_tags FmsPolicy#resource_tags}.
        :param resource_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_type FmsPolicy#resource_type}.
        :param resource_type_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_type_list FmsPolicy#resource_type_list}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#tags FmsPolicy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#tags_all FmsPolicy#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee5af9a5cb7a63cafd4bdb0f8c1d3c1a1926ff0c89fef01bcd4ac26f2f406081)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FmsPolicyConfig(
            exclude_resource_tags=exclude_resource_tags,
            name=name,
            security_service_policy_data=security_service_policy_data,
            delete_all_policy_resources=delete_all_policy_resources,
            delete_unused_fm_managed_resources=delete_unused_fm_managed_resources,
            exclude_map=exclude_map,
            id=id,
            include_map=include_map,
            remediation_enabled=remediation_enabled,
            resource_tags=resource_tags,
            resource_type=resource_type,
            resource_type_list=resource_type_list,
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

    @jsii.member(jsii_name="putExcludeMap")
    def put_exclude_map(
        self,
        *,
        account: typing.Optional[typing.Sequence[builtins.str]] = None,
        orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#account FmsPolicy#account}.
        :param orgunit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#orgunit FmsPolicy#orgunit}.
        '''
        value = FmsPolicyExcludeMap(account=account, orgunit=orgunit)

        return typing.cast(None, jsii.invoke(self, "putExcludeMap", [value]))

    @jsii.member(jsii_name="putIncludeMap")
    def put_include_map(
        self,
        *,
        account: typing.Optional[typing.Sequence[builtins.str]] = None,
        orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#account FmsPolicy#account}.
        :param orgunit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#orgunit FmsPolicy#orgunit}.
        '''
        value = FmsPolicyIncludeMap(account=account, orgunit=orgunit)

        return typing.cast(None, jsii.invoke(self, "putIncludeMap", [value]))

    @jsii.member(jsii_name="putSecurityServicePolicyData")
    def put_security_service_policy_data(
        self,
        *,
        type: builtins.str,
        managed_service_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#type FmsPolicy#type}.
        :param managed_service_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#managed_service_data FmsPolicy#managed_service_data}.
        '''
        value = FmsPolicySecurityServicePolicyData(
            type=type, managed_service_data=managed_service_data
        )

        return typing.cast(None, jsii.invoke(self, "putSecurityServicePolicyData", [value]))

    @jsii.member(jsii_name="resetDeleteAllPolicyResources")
    def reset_delete_all_policy_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteAllPolicyResources", []))

    @jsii.member(jsii_name="resetDeleteUnusedFmManagedResources")
    def reset_delete_unused_fm_managed_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteUnusedFmManagedResources", []))

    @jsii.member(jsii_name="resetExcludeMap")
    def reset_exclude_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludeMap", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeMap")
    def reset_include_map(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeMap", []))

    @jsii.member(jsii_name="resetRemediationEnabled")
    def reset_remediation_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemediationEnabled", []))

    @jsii.member(jsii_name="resetResourceTags")
    def reset_resource_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTags", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetResourceTypeList")
    def reset_resource_type_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceTypeList", []))

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
    @jsii.member(jsii_name="excludeMap")
    def exclude_map(self) -> "FmsPolicyExcludeMapOutputReference":
        return typing.cast("FmsPolicyExcludeMapOutputReference", jsii.get(self, "excludeMap"))

    @builtins.property
    @jsii.member(jsii_name="includeMap")
    def include_map(self) -> "FmsPolicyIncludeMapOutputReference":
        return typing.cast("FmsPolicyIncludeMapOutputReference", jsii.get(self, "includeMap"))

    @builtins.property
    @jsii.member(jsii_name="policyUpdateToken")
    def policy_update_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyUpdateToken"))

    @builtins.property
    @jsii.member(jsii_name="securityServicePolicyData")
    def security_service_policy_data(
        self,
    ) -> "FmsPolicySecurityServicePolicyDataOutputReference":
        return typing.cast("FmsPolicySecurityServicePolicyDataOutputReference", jsii.get(self, "securityServicePolicyData"))

    @builtins.property
    @jsii.member(jsii_name="deleteAllPolicyResourcesInput")
    def delete_all_policy_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteAllPolicyResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteUnusedFmManagedResourcesInput")
    def delete_unused_fm_managed_resources_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteUnusedFmManagedResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeMapInput")
    def exclude_map_input(self) -> typing.Optional["FmsPolicyExcludeMap"]:
        return typing.cast(typing.Optional["FmsPolicyExcludeMap"], jsii.get(self, "excludeMapInput"))

    @builtins.property
    @jsii.member(jsii_name="excludeResourceTagsInput")
    def exclude_resource_tags_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "excludeResourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeMapInput")
    def include_map_input(self) -> typing.Optional["FmsPolicyIncludeMap"]:
        return typing.cast(typing.Optional["FmsPolicyIncludeMap"], jsii.get(self, "includeMapInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="remediationEnabledInput")
    def remediation_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "remediationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTagsInput")
    def resource_tags_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "resourceTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeListInput")
    def resource_type_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypeListInput"))

    @builtins.property
    @jsii.member(jsii_name="securityServicePolicyDataInput")
    def security_service_policy_data_input(
        self,
    ) -> typing.Optional["FmsPolicySecurityServicePolicyData"]:
        return typing.cast(typing.Optional["FmsPolicySecurityServicePolicyData"], jsii.get(self, "securityServicePolicyDataInput"))

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
    @jsii.member(jsii_name="deleteAllPolicyResources")
    def delete_all_policy_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteAllPolicyResources"))

    @delete_all_policy_resources.setter
    def delete_all_policy_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73eaa714b6382800029e901307d1c589a2c626b39d97e07f08a62bb4eb0ea715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAllPolicyResources", value)

    @builtins.property
    @jsii.member(jsii_name="deleteUnusedFmManagedResources")
    def delete_unused_fm_managed_resources(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteUnusedFmManagedResources"))

    @delete_unused_fm_managed_resources.setter
    def delete_unused_fm_managed_resources(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f17ddeec63b0e7b852176c1fab19c3c92e89b1ad06fecca3cd7bc521c9c8c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteUnusedFmManagedResources", value)

    @builtins.property
    @jsii.member(jsii_name="excludeResourceTags")
    def exclude_resource_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "excludeResourceTags"))

    @exclude_resource_tags.setter
    def exclude_resource_tags(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e6d2d02bc14aa319828fa4d88fc2169ce5a90c7c121200b22420698520ce595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeResourceTags", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a33442d2b3f10233d563ea54dbdc8b5cc850165fafd93e5349ac2a266c09291e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0994449e5c3af76e0d4866d6c9320955df193e2edeea1216567741d71875836)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="remediationEnabled")
    def remediation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remediationEnabled"))

    @remediation_enabled.setter
    def remediation_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1131f5f382db9c46a4aeb3148b3a666df750d7f511e424124a06ba8917811aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remediationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89de4e955c22dcefc525890f2fa87cd8ef57a93de2f5670e2c1693d54711f236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddecefa4c2d2b29de9af6d75d02788f8d7520d3e203d620a821f7b3ce2d3e43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTypeList")
    def resource_type_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypeList"))

    @resource_type_list.setter
    def resource_type_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244e26e6c8b89816d7d8a8c6342261287adb457488cb49e35271e5693a8898c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypeList", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__514ed2dbe07e54702d27781785cee685796a68f8c6a14e4d180a8897e15d85a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1c5a231a84f9241f6431b163a8fcf40915004eb088e17342ad2192cccbecdab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicyConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "exclude_resource_tags": "excludeResourceTags",
        "name": "name",
        "security_service_policy_data": "securityServicePolicyData",
        "delete_all_policy_resources": "deleteAllPolicyResources",
        "delete_unused_fm_managed_resources": "deleteUnusedFmManagedResources",
        "exclude_map": "excludeMap",
        "id": "id",
        "include_map": "includeMap",
        "remediation_enabled": "remediationEnabled",
        "resource_tags": "resourceTags",
        "resource_type": "resourceType",
        "resource_type_list": "resourceTypeList",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class FmsPolicyConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        exclude_resource_tags: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        security_service_policy_data: typing.Union["FmsPolicySecurityServicePolicyData", typing.Dict[builtins.str, typing.Any]],
        delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        delete_unused_fm_managed_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exclude_map: typing.Optional[typing.Union["FmsPolicyExcludeMap", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_map: typing.Optional[typing.Union["FmsPolicyIncludeMap", typing.Dict[builtins.str, typing.Any]]] = None,
        remediation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
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
        :param exclude_resource_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#exclude_resource_tags FmsPolicy#exclude_resource_tags}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#name FmsPolicy#name}.
        :param security_service_policy_data: security_service_policy_data block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#security_service_policy_data FmsPolicy#security_service_policy_data}
        :param delete_all_policy_resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#delete_all_policy_resources FmsPolicy#delete_all_policy_resources}.
        :param delete_unused_fm_managed_resources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#delete_unused_fm_managed_resources FmsPolicy#delete_unused_fm_managed_resources}.
        :param exclude_map: exclude_map block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#exclude_map FmsPolicy#exclude_map}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#id FmsPolicy#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_map: include_map block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#include_map FmsPolicy#include_map}
        :param remediation_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#remediation_enabled FmsPolicy#remediation_enabled}.
        :param resource_tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_tags FmsPolicy#resource_tags}.
        :param resource_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_type FmsPolicy#resource_type}.
        :param resource_type_list: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_type_list FmsPolicy#resource_type_list}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#tags FmsPolicy#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#tags_all FmsPolicy#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(security_service_policy_data, dict):
            security_service_policy_data = FmsPolicySecurityServicePolicyData(**security_service_policy_data)
        if isinstance(exclude_map, dict):
            exclude_map = FmsPolicyExcludeMap(**exclude_map)
        if isinstance(include_map, dict):
            include_map = FmsPolicyIncludeMap(**include_map)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89138902ae4301548599b6933fcd33a8c038c1944289f890e3ab239d36b086f3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument exclude_resource_tags", value=exclude_resource_tags, expected_type=type_hints["exclude_resource_tags"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument security_service_policy_data", value=security_service_policy_data, expected_type=type_hints["security_service_policy_data"])
            check_type(argname="argument delete_all_policy_resources", value=delete_all_policy_resources, expected_type=type_hints["delete_all_policy_resources"])
            check_type(argname="argument delete_unused_fm_managed_resources", value=delete_unused_fm_managed_resources, expected_type=type_hints["delete_unused_fm_managed_resources"])
            check_type(argname="argument exclude_map", value=exclude_map, expected_type=type_hints["exclude_map"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_map", value=include_map, expected_type=type_hints["include_map"])
            check_type(argname="argument remediation_enabled", value=remediation_enabled, expected_type=type_hints["remediation_enabled"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument resource_type_list", value=resource_type_list, expected_type=type_hints["resource_type_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exclude_resource_tags": exclude_resource_tags,
            "name": name,
            "security_service_policy_data": security_service_policy_data,
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
        if delete_all_policy_resources is not None:
            self._values["delete_all_policy_resources"] = delete_all_policy_resources
        if delete_unused_fm_managed_resources is not None:
            self._values["delete_unused_fm_managed_resources"] = delete_unused_fm_managed_resources
        if exclude_map is not None:
            self._values["exclude_map"] = exclude_map
        if id is not None:
            self._values["id"] = id
        if include_map is not None:
            self._values["include_map"] = include_map
        if remediation_enabled is not None:
            self._values["remediation_enabled"] = remediation_enabled
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if resource_type_list is not None:
            self._values["resource_type_list"] = resource_type_list
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
    def exclude_resource_tags(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#exclude_resource_tags FmsPolicy#exclude_resource_tags}.'''
        result = self._values.get("exclude_resource_tags")
        assert result is not None, "Required property 'exclude_resource_tags' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#name FmsPolicy#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_service_policy_data(self) -> "FmsPolicySecurityServicePolicyData":
        '''security_service_policy_data block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#security_service_policy_data FmsPolicy#security_service_policy_data}
        '''
        result = self._values.get("security_service_policy_data")
        assert result is not None, "Required property 'security_service_policy_data' is missing"
        return typing.cast("FmsPolicySecurityServicePolicyData", result)

    @builtins.property
    def delete_all_policy_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#delete_all_policy_resources FmsPolicy#delete_all_policy_resources}.'''
        result = self._values.get("delete_all_policy_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def delete_unused_fm_managed_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#delete_unused_fm_managed_resources FmsPolicy#delete_unused_fm_managed_resources}.'''
        result = self._values.get("delete_unused_fm_managed_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exclude_map(self) -> typing.Optional["FmsPolicyExcludeMap"]:
        '''exclude_map block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#exclude_map FmsPolicy#exclude_map}
        '''
        result = self._values.get("exclude_map")
        return typing.cast(typing.Optional["FmsPolicyExcludeMap"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#id FmsPolicy#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_map(self) -> typing.Optional["FmsPolicyIncludeMap"]:
        '''include_map block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#include_map FmsPolicy#include_map}
        '''
        result = self._values.get("include_map")
        return typing.cast(typing.Optional["FmsPolicyIncludeMap"], result)

    @builtins.property
    def remediation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#remediation_enabled FmsPolicy#remediation_enabled}.'''
        result = self._values.get("remediation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_tags FmsPolicy#resource_tags}.'''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_type FmsPolicy#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#resource_type_list FmsPolicy#resource_type_list}.'''
        result = self._values.get("resource_type_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#tags FmsPolicy#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#tags_all FmsPolicy#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FmsPolicyConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicyExcludeMap",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "orgunit": "orgunit"},
)
class FmsPolicyExcludeMap:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.Sequence[builtins.str]] = None,
        orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#account FmsPolicy#account}.
        :param orgunit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#orgunit FmsPolicy#orgunit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a026a84b5f04a6637d8ab7b052e6469c3e708dd3f2b27d55c815a8c6498a2e52)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument orgunit", value=orgunit, expected_type=type_hints["orgunit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if orgunit is not None:
            self._values["orgunit"] = orgunit

    @builtins.property
    def account(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#account FmsPolicy#account}.'''
        result = self._values.get("account")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def orgunit(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#orgunit FmsPolicy#orgunit}.'''
        result = self._values.get("orgunit")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FmsPolicyExcludeMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FmsPolicyExcludeMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicyExcludeMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba6883295442cff804c173a642d88c17664416d5255a73a0a31c73ecd9cdfa73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccount")
    def reset_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccount", []))

    @jsii.member(jsii_name="resetOrgunit")
    def reset_orgunit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgunit", []))

    @builtins.property
    @jsii.member(jsii_name="accountInput")
    def account_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountInput"))

    @builtins.property
    @jsii.member(jsii_name="orgunitInput")
    def orgunit_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "orgunitInput"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "account"))

    @account.setter
    def account(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60811fabea2b68cf7b3bedbb9c0b61d8944e954f1359d6914a1300ed3509e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "account", value)

    @builtins.property
    @jsii.member(jsii_name="orgunit")
    def orgunit(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "orgunit"))

    @orgunit.setter
    def orgunit(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b05bfcb6c41128c2c95ea30444f73126da51e7ac1f29d4f9253f5d006720db2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgunit", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FmsPolicyExcludeMap]:
        return typing.cast(typing.Optional[FmsPolicyExcludeMap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FmsPolicyExcludeMap]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60862734b2f4f33c74d762388f8f2ee2c3062d328f5a5e52f76dc7980c10a2b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicyIncludeMap",
    jsii_struct_bases=[],
    name_mapping={"account": "account", "orgunit": "orgunit"},
)
class FmsPolicyIncludeMap:
    def __init__(
        self,
        *,
        account: typing.Optional[typing.Sequence[builtins.str]] = None,
        orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param account: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#account FmsPolicy#account}.
        :param orgunit: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#orgunit FmsPolicy#orgunit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec4b5a14b0571fde6699fc29cc44c0323f339a901fc2ad2a8b522f2db5307ee6)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument orgunit", value=orgunit, expected_type=type_hints["orgunit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if orgunit is not None:
            self._values["orgunit"] = orgunit

    @builtins.property
    def account(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#account FmsPolicy#account}.'''
        result = self._values.get("account")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def orgunit(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#orgunit FmsPolicy#orgunit}.'''
        result = self._values.get("orgunit")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FmsPolicyIncludeMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FmsPolicyIncludeMapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicyIncludeMapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__920c82a6ea549593d5596fbc65cdc148bcda0e05f5680016d94ea554992a9cd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccount")
    def reset_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccount", []))

    @jsii.member(jsii_name="resetOrgunit")
    def reset_orgunit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOrgunit", []))

    @builtins.property
    @jsii.member(jsii_name="accountInput")
    def account_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "accountInput"))

    @builtins.property
    @jsii.member(jsii_name="orgunitInput")
    def orgunit_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "orgunitInput"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "account"))

    @account.setter
    def account(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1ffec6f0b4c17b829280c221a8dddb6d03acc4a6c88d26ece6a685a52fcc96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "account", value)

    @builtins.property
    @jsii.member(jsii_name="orgunit")
    def orgunit(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "orgunit"))

    @orgunit.setter
    def orgunit(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b19355d125696880f4d060b7e9f144294048e4b811df3b8bbf000acdd6cb4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "orgunit", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FmsPolicyIncludeMap]:
        return typing.cast(typing.Optional[FmsPolicyIncludeMap], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[FmsPolicyIncludeMap]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b389aca883c82a191fff292081f28fbec26d120059181728e0198e2e49c5024d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicySecurityServicePolicyData",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "managed_service_data": "managedServiceData"},
)
class FmsPolicySecurityServicePolicyData:
    def __init__(
        self,
        *,
        type: builtins.str,
        managed_service_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#type FmsPolicy#type}.
        :param managed_service_data: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#managed_service_data FmsPolicy#managed_service_data}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed3d7fb1064e4caa9c6d43ee5d1b13183e1a77985f964a97cff427b516f12de)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument managed_service_data", value=managed_service_data, expected_type=type_hints["managed_service_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if managed_service_data is not None:
            self._values["managed_service_data"] = managed_service_data

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#type FmsPolicy#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def managed_service_data(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/fms_policy#managed_service_data FmsPolicy#managed_service_data}.'''
        result = self._values.get("managed_service_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FmsPolicySecurityServicePolicyData(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FmsPolicySecurityServicePolicyDataOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.fmsPolicy.FmsPolicySecurityServicePolicyDataOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__475c833e36b2d6cfd33ed45f3c992e25f2cf916c5dc09797fad8f163030b9c79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetManagedServiceData")
    def reset_managed_service_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedServiceData", []))

    @builtins.property
    @jsii.member(jsii_name="managedServiceDataInput")
    def managed_service_data_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedServiceDataInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedServiceData")
    def managed_service_data(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedServiceData"))

    @managed_service_data.setter
    def managed_service_data(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b382b4892f181d0916f193726ca4caa9aba5321d295b5a6b91db72014075d5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedServiceData", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30824b9ea6110f295e65d0154c0b160621a6bb2dbdb1153024604443799c5479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FmsPolicySecurityServicePolicyData]:
        return typing.cast(typing.Optional[FmsPolicySecurityServicePolicyData], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FmsPolicySecurityServicePolicyData],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9f67db9205b7cfa25f144b1b81e020674c3509993295fbec8a57e75faee437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "FmsPolicy",
    "FmsPolicyConfig",
    "FmsPolicyExcludeMap",
    "FmsPolicyExcludeMapOutputReference",
    "FmsPolicyIncludeMap",
    "FmsPolicyIncludeMapOutputReference",
    "FmsPolicySecurityServicePolicyData",
    "FmsPolicySecurityServicePolicyDataOutputReference",
]

publication.publish()

def _typecheckingstub__ee5af9a5cb7a63cafd4bdb0f8c1d3c1a1926ff0c89fef01bcd4ac26f2f406081(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    exclude_resource_tags: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    security_service_policy_data: typing.Union[FmsPolicySecurityServicePolicyData, typing.Dict[builtins.str, typing.Any]],
    delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_unused_fm_managed_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_map: typing.Optional[typing.Union[FmsPolicyExcludeMap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_map: typing.Optional[typing.Union[FmsPolicyIncludeMap, typing.Dict[builtins.str, typing.Any]]] = None,
    remediation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__73eaa714b6382800029e901307d1c589a2c626b39d97e07f08a62bb4eb0ea715(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f17ddeec63b0e7b852176c1fab19c3c92e89b1ad06fecca3cd7bc521c9c8c02(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e6d2d02bc14aa319828fa4d88fc2169ce5a90c7c121200b22420698520ce595(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a33442d2b3f10233d563ea54dbdc8b5cc850165fafd93e5349ac2a266c09291e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0994449e5c3af76e0d4866d6c9320955df193e2edeea1216567741d71875836(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1131f5f382db9c46a4aeb3148b3a666df750d7f511e424124a06ba8917811aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89de4e955c22dcefc525890f2fa87cd8ef57a93de2f5670e2c1693d54711f236(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddecefa4c2d2b29de9af6d75d02788f8d7520d3e203d620a821f7b3ce2d3e43(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244e26e6c8b89816d7d8a8c6342261287adb457488cb49e35271e5693a8898c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514ed2dbe07e54702d27781785cee685796a68f8c6a14e4d180a8897e15d85a6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1c5a231a84f9241f6431b163a8fcf40915004eb088e17342ad2192cccbecdab(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89138902ae4301548599b6933fcd33a8c038c1944289f890e3ab239d36b086f3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    exclude_resource_tags: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    security_service_policy_data: typing.Union[FmsPolicySecurityServicePolicyData, typing.Dict[builtins.str, typing.Any]],
    delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    delete_unused_fm_managed_resources: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exclude_map: typing.Optional[typing.Union[FmsPolicyExcludeMap, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_map: typing.Optional[typing.Union[FmsPolicyIncludeMap, typing.Dict[builtins.str, typing.Any]]] = None,
    remediation_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a026a84b5f04a6637d8ab7b052e6469c3e708dd3f2b27d55c815a8c6498a2e52(
    *,
    account: typing.Optional[typing.Sequence[builtins.str]] = None,
    orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6883295442cff804c173a642d88c17664416d5255a73a0a31c73ecd9cdfa73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60811fabea2b68cf7b3bedbb9c0b61d8944e954f1359d6914a1300ed3509e62(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b05bfcb6c41128c2c95ea30444f73126da51e7ac1f29d4f9253f5d006720db2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60862734b2f4f33c74d762388f8f2ee2c3062d328f5a5e52f76dc7980c10a2b3(
    value: typing.Optional[FmsPolicyExcludeMap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4b5a14b0571fde6699fc29cc44c0323f339a901fc2ad2a8b522f2db5307ee6(
    *,
    account: typing.Optional[typing.Sequence[builtins.str]] = None,
    orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920c82a6ea549593d5596fbc65cdc148bcda0e05f5680016d94ea554992a9cd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1ffec6f0b4c17b829280c221a8dddb6d03acc4a6c88d26ece6a685a52fcc96d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b19355d125696880f4d060b7e9f144294048e4b811df3b8bbf000acdd6cb4e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b389aca883c82a191fff292081f28fbec26d120059181728e0198e2e49c5024d(
    value: typing.Optional[FmsPolicyIncludeMap],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed3d7fb1064e4caa9c6d43ee5d1b13183e1a77985f964a97cff427b516f12de(
    *,
    type: builtins.str,
    managed_service_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475c833e36b2d6cfd33ed45f3c992e25f2cf916c5dc09797fad8f163030b9c79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b382b4892f181d0916f193726ca4caa9aba5321d295b5a6b91db72014075d5ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30824b9ea6110f295e65d0154c0b160621a6bb2dbdb1153024604443799c5479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9f67db9205b7cfa25f144b1b81e020674c3509993295fbec8a57e75faee437(
    value: typing.Optional[FmsPolicySecurityServicePolicyData],
) -> None:
    """Type checking stubs"""
    pass
