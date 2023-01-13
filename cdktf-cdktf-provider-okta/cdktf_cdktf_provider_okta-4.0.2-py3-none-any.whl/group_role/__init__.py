'''
# `okta_group_role`

Refer to the Terraform Registory for docs: [`okta_group_role`](https://www.terraform.io/docs/providers/okta/r/group_role).
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


class GroupRole(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.groupRole.GroupRole",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/group_role okta_group_role}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        group_id: builtins.str,
        role_type: builtins.str,
        disable_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        target_app_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_group_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/group_role okta_group_role} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param group_id: ID of group to attach admin roles to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#group_id GroupRole#group_id}
        :param role_type: Type of Role to assign. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#role_type GroupRole#role_type}
        :param disable_notifications: When this setting is enabled, the admins won't receive any of the default Okta administrator emails. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#disable_notifications GroupRole#disable_notifications}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#id GroupRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param target_app_list: List of apps ids for the targets of the admin role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#target_app_list GroupRole#target_app_list}
        :param target_group_list: List of groups ids for the targets of the admin role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#target_group_list GroupRole#target_group_list}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc60f6b1388de1d2e974c744f040a246dac77c5299ba7c3b88948e0ecc26dac4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GroupRoleConfig(
            group_id=group_id,
            role_type=role_type,
            disable_notifications=disable_notifications,
            id=id,
            target_app_list=target_app_list,
            target_group_list=target_group_list,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetDisableNotifications")
    def reset_disable_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableNotifications", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTargetAppList")
    def reset_target_app_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetAppList", []))

    @jsii.member(jsii_name="resetTargetGroupList")
    def reset_target_group_list(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetGroupList", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="disableNotificationsInput")
    def disable_notifications_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="roleTypeInput")
    def role_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetAppListInput")
    def target_app_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetAppListInput"))

    @builtins.property
    @jsii.member(jsii_name="targetGroupListInput")
    def target_group_list_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "targetGroupListInput"))

    @builtins.property
    @jsii.member(jsii_name="disableNotifications")
    def disable_notifications(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableNotifications"))

    @disable_notifications.setter
    def disable_notifications(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5cea53c6409648748939df3c53a1bf5878a9d288a0963f5b168fc09fcf468fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableNotifications", value)

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05359a1a6fa4a675ef404e8ee52d603924b5ad015a678cb19716ea5e36edf11c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a3fe02a47a795d775ba93d49f24bb93a05856d8745d0db48a62d3567fe7a371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="roleType")
    def role_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleType"))

    @role_type.setter
    def role_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e544516d5e82071b3bbaf62082b7bcb88e5c7f5656643f6f17f1845ba8fdc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleType", value)

    @builtins.property
    @jsii.member(jsii_name="targetAppList")
    def target_app_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetAppList"))

    @target_app_list.setter
    def target_app_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92e0efc5d4066bd4049df51cabf51efd1ead8f08745e83a6978feac4b6bebed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetAppList", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroupList")
    def target_group_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "targetGroupList"))

    @target_group_list.setter
    def target_group_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a274c482356d17e6254495178d34de4b45f931d008ee0a6ac8f02d8ef2f7588e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetGroupList", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.groupRole.GroupRoleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "group_id": "groupId",
        "role_type": "roleType",
        "disable_notifications": "disableNotifications",
        "id": "id",
        "target_app_list": "targetAppList",
        "target_group_list": "targetGroupList",
    },
)
class GroupRoleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        group_id: builtins.str,
        role_type: builtins.str,
        disable_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        target_app_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        target_group_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param group_id: ID of group to attach admin roles to. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#group_id GroupRole#group_id}
        :param role_type: Type of Role to assign. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#role_type GroupRole#role_type}
        :param disable_notifications: When this setting is enabled, the admins won't receive any of the default Okta administrator emails. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#disable_notifications GroupRole#disable_notifications}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#id GroupRole#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param target_app_list: List of apps ids for the targets of the admin role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#target_app_list GroupRole#target_app_list}
        :param target_group_list: List of groups ids for the targets of the admin role. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#target_group_list GroupRole#target_group_list}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c336b0548b10f349b61e86a92df6f755f175e4d90b93efcaf5431f2eab0ad81e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument role_type", value=role_type, expected_type=type_hints["role_type"])
            check_type(argname="argument disable_notifications", value=disable_notifications, expected_type=type_hints["disable_notifications"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument target_app_list", value=target_app_list, expected_type=type_hints["target_app_list"])
            check_type(argname="argument target_group_list", value=target_group_list, expected_type=type_hints["target_group_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_id": group_id,
            "role_type": role_type,
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
        if disable_notifications is not None:
            self._values["disable_notifications"] = disable_notifications
        if id is not None:
            self._values["id"] = id
        if target_app_list is not None:
            self._values["target_app_list"] = target_app_list
        if target_group_list is not None:
            self._values["target_group_list"] = target_group_list

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
    def group_id(self) -> builtins.str:
        '''ID of group to attach admin roles to.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#group_id GroupRole#group_id}
        '''
        result = self._values.get("group_id")
        assert result is not None, "Required property 'group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_type(self) -> builtins.str:
        '''Type of Role to assign.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#role_type GroupRole#role_type}
        '''
        result = self._values.get("role_type")
        assert result is not None, "Required property 'role_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disable_notifications(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When this setting is enabled, the admins won't receive any of the default Okta administrator emails.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#disable_notifications GroupRole#disable_notifications}
        '''
        result = self._values.get("disable_notifications")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#id GroupRole#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_app_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of apps ids for the targets of the admin role.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#target_app_list GroupRole#target_app_list}
        '''
        result = self._values.get("target_app_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def target_group_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of groups ids for the targets of the admin role.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/group_role#target_group_list GroupRole#target_group_list}
        '''
        result = self._values.get("target_group_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupRoleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GroupRole",
    "GroupRoleConfig",
]

publication.publish()

def _typecheckingstub__dc60f6b1388de1d2e974c744f040a246dac77c5299ba7c3b88948e0ecc26dac4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    group_id: builtins.str,
    role_type: builtins.str,
    disable_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    target_app_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_group_list: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__b5cea53c6409648748939df3c53a1bf5878a9d288a0963f5b168fc09fcf468fe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05359a1a6fa4a675ef404e8ee52d603924b5ad015a678cb19716ea5e36edf11c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3fe02a47a795d775ba93d49f24bb93a05856d8745d0db48a62d3567fe7a371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e544516d5e82071b3bbaf62082b7bcb88e5c7f5656643f6f17f1845ba8fdc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92e0efc5d4066bd4049df51cabf51efd1ead8f08745e83a6978feac4b6bebed(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a274c482356d17e6254495178d34de4b45f931d008ee0a6ac8f02d8ef2f7588e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c336b0548b10f349b61e86a92df6f755f175e4d90b93efcaf5431f2eab0ad81e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    group_id: builtins.str,
    role_type: builtins.str,
    disable_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    target_app_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_group_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
