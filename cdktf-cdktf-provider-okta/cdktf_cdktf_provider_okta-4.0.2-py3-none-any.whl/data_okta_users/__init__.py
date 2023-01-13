'''
# `data_okta_users`

Refer to the Terraform Registory for docs: [`data_okta_users`](https://www.terraform.io/docs/providers/okta/d/users).
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


class DataOktaUsers(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsers",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/d/users okta_users}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        compound_search_operator: typing.Optional[builtins.str] = None,
        delay_read_seconds: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        include_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_roles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        search: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOktaUsersSearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/d/users okta_users} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param compound_search_operator: Search operator used when joining mulitple search clauses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#compound_search_operator DataOktaUsers#compound_search_operator}
        :param delay_read_seconds: Force delay of the users read by N seconds. Useful when eventual consistency of users information needs to be allowed for. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#delay_read_seconds DataOktaUsers#delay_read_seconds}
        :param group_id: Find users based on group membership using the id of the group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#group_id DataOktaUsers#group_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#id DataOktaUsers#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_groups: Fetch group memberships for each user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#include_groups DataOktaUsers#include_groups}
        :param include_roles: Fetch user roles for each user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#include_roles DataOktaUsers#include_roles}
        :param search: search block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#search DataOktaUsers#search}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac67ea17d42c5d55c71a095418f941a8606800b21aeed4d53cc2685ecc94004a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataOktaUsersConfig(
            compound_search_operator=compound_search_operator,
            delay_read_seconds=delay_read_seconds,
            group_id=group_id,
            id=id,
            include_groups=include_groups,
            include_roles=include_roles,
            search=search,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSearch")
    def put_search(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOktaUsersSearch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9678c1f8523687745878330117ac313cb0ba5343e2fbe706db05c06d42652f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSearch", [value]))

    @jsii.member(jsii_name="resetCompoundSearchOperator")
    def reset_compound_search_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCompoundSearchOperator", []))

    @jsii.member(jsii_name="resetDelayReadSeconds")
    def reset_delay_read_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelayReadSeconds", []))

    @jsii.member(jsii_name="resetGroupId")
    def reset_group_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGroupId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeGroups")
    def reset_include_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeGroups", []))

    @jsii.member(jsii_name="resetIncludeRoles")
    def reset_include_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeRoles", []))

    @jsii.member(jsii_name="resetSearch")
    def reset_search(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearch", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="search")
    def search(self) -> "DataOktaUsersSearchList":
        return typing.cast("DataOktaUsersSearchList", jsii.get(self, "search"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> "DataOktaUsersUsersList":
        return typing.cast("DataOktaUsersUsersList", jsii.get(self, "users"))

    @builtins.property
    @jsii.member(jsii_name="compoundSearchOperatorInput")
    def compound_search_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "compoundSearchOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="delayReadSecondsInput")
    def delay_read_seconds_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "delayReadSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="groupIdInput")
    def group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeGroupsInput")
    def include_groups_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="includeRolesInput")
    def include_roles_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="searchInput")
    def search_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOktaUsersSearch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOktaUsersSearch"]]], jsii.get(self, "searchInput"))

    @builtins.property
    @jsii.member(jsii_name="compoundSearchOperator")
    def compound_search_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "compoundSearchOperator"))

    @compound_search_operator.setter
    def compound_search_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72226b01504a354134fb0775ed8b2489fcc5fe223e0e7582fe755e44d6e4e560)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "compoundSearchOperator", value)

    @builtins.property
    @jsii.member(jsii_name="delayReadSeconds")
    def delay_read_seconds(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delayReadSeconds"))

    @delay_read_seconds.setter
    def delay_read_seconds(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9434bfc7c74724bb8ffe226a4ae609c981feb058cc4e1a76feadc19fbe8f6b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delayReadSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="groupId")
    def group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupId"))

    @group_id.setter
    def group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4252b3654aef0fdcfb7f4836cb5c1baa97e6d31e41ca0fb2750e86bcaf98c6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf8d53b050aea05917d40823ce9099143d758e0df416bf28f1152275732a337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="includeGroups")
    def include_groups(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeGroups"))

    @include_groups.setter
    def include_groups(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d2fc21944f17eb248002d1ebc8081c5ac6cb8a73a7f8babb6a6d713a64d619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeGroups", value)

    @builtins.property
    @jsii.member(jsii_name="includeRoles")
    def include_roles(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeRoles"))

    @include_roles.setter
    def include_roles(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e83d15b8628693418934f7a201246a8a6606569cd4114229720678d6066b106)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeRoles", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "compound_search_operator": "compoundSearchOperator",
        "delay_read_seconds": "delayReadSeconds",
        "group_id": "groupId",
        "id": "id",
        "include_groups": "includeGroups",
        "include_roles": "includeRoles",
        "search": "search",
    },
)
class DataOktaUsersConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        compound_search_operator: typing.Optional[builtins.str] = None,
        delay_read_seconds: typing.Optional[builtins.str] = None,
        group_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        include_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        include_roles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        search: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataOktaUsersSearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param compound_search_operator: Search operator used when joining mulitple search clauses. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#compound_search_operator DataOktaUsers#compound_search_operator}
        :param delay_read_seconds: Force delay of the users read by N seconds. Useful when eventual consistency of users information needs to be allowed for. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#delay_read_seconds DataOktaUsers#delay_read_seconds}
        :param group_id: Find users based on group membership using the id of the group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#group_id DataOktaUsers#group_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#id DataOktaUsers#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_groups: Fetch group memberships for each user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#include_groups DataOktaUsers#include_groups}
        :param include_roles: Fetch user roles for each user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#include_roles DataOktaUsers#include_roles}
        :param search: search block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#search DataOktaUsers#search}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05afd3c7e5d36925e50580f23a0db7fd345e23e8678824f78d12bda86e6c65df)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument compound_search_operator", value=compound_search_operator, expected_type=type_hints["compound_search_operator"])
            check_type(argname="argument delay_read_seconds", value=delay_read_seconds, expected_type=type_hints["delay_read_seconds"])
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_groups", value=include_groups, expected_type=type_hints["include_groups"])
            check_type(argname="argument include_roles", value=include_roles, expected_type=type_hints["include_roles"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if compound_search_operator is not None:
            self._values["compound_search_operator"] = compound_search_operator
        if delay_read_seconds is not None:
            self._values["delay_read_seconds"] = delay_read_seconds
        if group_id is not None:
            self._values["group_id"] = group_id
        if id is not None:
            self._values["id"] = id
        if include_groups is not None:
            self._values["include_groups"] = include_groups
        if include_roles is not None:
            self._values["include_roles"] = include_roles
        if search is not None:
            self._values["search"] = search

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
    def compound_search_operator(self) -> typing.Optional[builtins.str]:
        '''Search operator used when joining mulitple search clauses.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#compound_search_operator DataOktaUsers#compound_search_operator}
        '''
        result = self._values.get("compound_search_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay_read_seconds(self) -> typing.Optional[builtins.str]:
        '''Force delay of the users read by N seconds.

        Useful when eventual consistency of users information needs to be allowed for.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#delay_read_seconds DataOktaUsers#delay_read_seconds}
        '''
        result = self._values.get("delay_read_seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''Find users based on group membership using the id of the group.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#group_id DataOktaUsers#group_id}
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#id DataOktaUsers#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_groups(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Fetch group memberships for each user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#include_groups DataOktaUsers#include_groups}
        '''
        result = self._values.get("include_groups")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def include_roles(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Fetch user roles for each user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#include_roles DataOktaUsers#include_roles}
        '''
        result = self._values.get("include_roles")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def search(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOktaUsersSearch"]]]:
        '''search block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#search DataOktaUsers#search}
        '''
        result = self._values.get("search")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataOktaUsersSearch"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaUsersConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersSearch",
    jsii_struct_bases=[],
    name_mapping={
        "comparison": "comparison",
        "expression": "expression",
        "name": "name",
        "value": "value",
    },
)
class DataOktaUsersSearch:
    def __init__(
        self,
        *,
        comparison: typing.Optional[builtins.str] = None,
        expression: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comparison: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#comparison DataOktaUsers#comparison}.
        :param expression: A raw search expression string. This requires the search feature be on. Please see Okta documentation on their filter API for users. https://developer.okta.com/docs/api/resources/users#list-users-with-search Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#expression DataOktaUsers#expression}
        :param name: Property name to search for. This requires the search feature be on. Please see Okta documentation on their filter API for users. https://developer.okta.com/docs/api/resources/users#list-users-with-search Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#name DataOktaUsers#name}
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#value DataOktaUsers#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__393a63781a2b1784828dbadce495b45e7e1bcbc11ebcbadb57a2a28edb608c16)
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comparison is not None:
            self._values["comparison"] = comparison
        if expression is not None:
            self._values["expression"] = expression
        if name is not None:
            self._values["name"] = name
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def comparison(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#comparison DataOktaUsers#comparison}.'''
        result = self._values.get("comparison")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expression(self) -> typing.Optional[builtins.str]:
        '''A raw search expression string.

        This requires the search feature be on. Please see Okta documentation on their filter API for users. https://developer.okta.com/docs/api/resources/users#list-users-with-search

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#expression DataOktaUsers#expression}
        '''
        result = self._values.get("expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Property name to search for.

        This requires the search feature be on. Please see Okta documentation on their filter API for users. https://developer.okta.com/docs/api/resources/users#list-users-with-search

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#name DataOktaUsers#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/d/users#value DataOktaUsers#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaUsersSearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaUsersSearchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersSearchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fe949b5e8ddb2983f34b7ab4ef1d8583a96bf29ad089976692afa0adab171a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataOktaUsersSearchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ef2a0994fc40a2a29c507889c22a631bafa86ee994809b7e7893dabdfb3e54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOktaUsersSearchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d25915391af881d70c4bdff898488d4068819fe4596346818141f533ab7113)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b6ce8c53922f9beb20135532a63012daa4590862f4ffa3e2fb26cd30a582c26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f012d19df1acf8db7ef4a9c0ea302220f27cfc73f79c423a98309f1899d5bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOktaUsersSearch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOktaUsersSearch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOktaUsersSearch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d56928910c9409b71e436bb8cc692ba032d6343c7fbc447fba10a42c5d890d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataOktaUsersSearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersSearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5790a264506e91217799d0f596df5517cf924f2e038cab13d783f77ca9643e6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetComparison")
    def reset_comparison(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparison", []))

    @jsii.member(jsii_name="resetExpression")
    def reset_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpression", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6a18d78f23716dc3b43ddfdea6e53fc41d5fb6d7df99c9267e8d8a6b3a3dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value)

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75296f249822656b0ff113ae9185db5d412c97cc807eaa32aeec7123fbb26f4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091aec1dbe6316386ac553d31438fe061742a97aa65d0e386fb1b9e1d8a630ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5515f76e5333722afb5445ec930fc8fc72d77549b94d4af3a0cc2dcf665d0f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataOktaUsersSearch, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataOktaUsersSearch, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataOktaUsersSearch, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa6b04f5d42107862d5220c9d419bfd90d42e53bd4d34e601d393bc7ccf2d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersUsers",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataOktaUsersUsers:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataOktaUsersUsers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataOktaUsersUsersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersUsersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b93cbff457544914c37c6d5908783809b70f1f4d68e36fdfb0b836d568454d60)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DataOktaUsersUsersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0521c75a187e353291ef3230a0861809659fbf476a35cb2fa886875015ade2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataOktaUsersUsersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dba4f483387786adecea29581c86195a3ab61fe447504e5361c7e6179e6bb99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c145906e8824397de593092dcc15522dfe06eddfa22f3383c9214cdff3728bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a454e3f73610d6fe4df7a4b4f1bd4c9a73d3ed1f38c617ad239a904dda2d2eb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataOktaUsersUsersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.dataOktaUsers.DataOktaUsersUsersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb79e4090b91ad5c9004562434d8eee3cbfa2d34e990e655a2534f583a2be7ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="adminRoles")
    def admin_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "adminRoles"))

    @builtins.property
    @jsii.member(jsii_name="city")
    def city(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "city"))

    @builtins.property
    @jsii.member(jsii_name="costCenter")
    def cost_center(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "costCenter"))

    @builtins.property
    @jsii.member(jsii_name="countryCode")
    def country_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "countryCode"))

    @builtins.property
    @jsii.member(jsii_name="customProfileAttributes")
    def custom_profile_attributes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customProfileAttributes"))

    @builtins.property
    @jsii.member(jsii_name="department")
    def department(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "department"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @builtins.property
    @jsii.member(jsii_name="division")
    def division(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "division"))

    @builtins.property
    @jsii.member(jsii_name="email")
    def email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "email"))

    @builtins.property
    @jsii.member(jsii_name="employeeNumber")
    def employee_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "employeeNumber"))

    @builtins.property
    @jsii.member(jsii_name="firstName")
    def first_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firstName"))

    @builtins.property
    @jsii.member(jsii_name="groupMemberships")
    def group_memberships(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "groupMemberships"))

    @builtins.property
    @jsii.member(jsii_name="honorificPrefix")
    def honorific_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "honorificPrefix"))

    @builtins.property
    @jsii.member(jsii_name="honorificSuffix")
    def honorific_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "honorificSuffix"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="lastName")
    def last_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastName"))

    @builtins.property
    @jsii.member(jsii_name="locale")
    def locale(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "locale"))

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "login"))

    @builtins.property
    @jsii.member(jsii_name="manager")
    def manager(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "manager"))

    @builtins.property
    @jsii.member(jsii_name="managerId")
    def manager_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managerId"))

    @builtins.property
    @jsii.member(jsii_name="middleName")
    def middle_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "middleName"))

    @builtins.property
    @jsii.member(jsii_name="mobilePhone")
    def mobile_phone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobilePhone"))

    @builtins.property
    @jsii.member(jsii_name="nickName")
    def nick_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nickName"))

    @builtins.property
    @jsii.member(jsii_name="organization")
    def organization(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "organization"))

    @builtins.property
    @jsii.member(jsii_name="postalAddress")
    def postal_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "postalAddress"))

    @builtins.property
    @jsii.member(jsii_name="preferredLanguage")
    def preferred_language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preferredLanguage"))

    @builtins.property
    @jsii.member(jsii_name="primaryPhone")
    def primary_phone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryPhone"))

    @builtins.property
    @jsii.member(jsii_name="profileUrl")
    def profile_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "profileUrl"))

    @builtins.property
    @jsii.member(jsii_name="secondEmail")
    def second_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secondEmail"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="streetAddress")
    def street_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "streetAddress"))

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @builtins.property
    @jsii.member(jsii_name="userType")
    def user_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userType"))

    @builtins.property
    @jsii.member(jsii_name="zipCode")
    def zip_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zipCode"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataOktaUsersUsers]:
        return typing.cast(typing.Optional[DataOktaUsersUsers], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DataOktaUsersUsers]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25a14d2a557d6a0cf71d17164d3efa6220f4b3f25500ccaedaf609e30aaf128a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataOktaUsers",
    "DataOktaUsersConfig",
    "DataOktaUsersSearch",
    "DataOktaUsersSearchList",
    "DataOktaUsersSearchOutputReference",
    "DataOktaUsersUsers",
    "DataOktaUsersUsersList",
    "DataOktaUsersUsersOutputReference",
]

publication.publish()

def _typecheckingstub__ac67ea17d42c5d55c71a095418f941a8606800b21aeed4d53cc2685ecc94004a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    compound_search_operator: typing.Optional[builtins.str] = None,
    delay_read_seconds: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    include_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_roles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    search: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOktaUsersSearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__a9678c1f8523687745878330117ac313cb0ba5343e2fbe706db05c06d42652f8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOktaUsersSearch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72226b01504a354134fb0775ed8b2489fcc5fe223e0e7582fe755e44d6e4e560(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9434bfc7c74724bb8ffe226a4ae609c981feb058cc4e1a76feadc19fbe8f6b9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4252b3654aef0fdcfb7f4836cb5c1baa97e6d31e41ca0fb2750e86bcaf98c6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf8d53b050aea05917d40823ce9099143d758e0df416bf28f1152275732a337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d2fc21944f17eb248002d1ebc8081c5ac6cb8a73a7f8babb6a6d713a64d619(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e83d15b8628693418934f7a201246a8a6606569cd4114229720678d6066b106(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05afd3c7e5d36925e50580f23a0db7fd345e23e8678824f78d12bda86e6c65df(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    compound_search_operator: typing.Optional[builtins.str] = None,
    delay_read_seconds: typing.Optional[builtins.str] = None,
    group_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    include_groups: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    include_roles: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    search: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataOktaUsersSearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393a63781a2b1784828dbadce495b45e7e1bcbc11ebcbadb57a2a28edb608c16(
    *,
    comparison: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe949b5e8ddb2983f34b7ab4ef1d8583a96bf29ad089976692afa0adab171a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ef2a0994fc40a2a29c507889c22a631bafa86ee994809b7e7893dabdfb3e54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d25915391af881d70c4bdff898488d4068819fe4596346818141f533ab7113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6ce8c53922f9beb20135532a63012daa4590862f4ffa3e2fb26cd30a582c26(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f012d19df1acf8db7ef4a9c0ea302220f27cfc73f79c423a98309f1899d5bfe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d56928910c9409b71e436bb8cc692ba032d6343c7fbc447fba10a42c5d890d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataOktaUsersSearch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5790a264506e91217799d0f596df5517cf924f2e038cab13d783f77ca9643e6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6a18d78f23716dc3b43ddfdea6e53fc41d5fb6d7df99c9267e8d8a6b3a3dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75296f249822656b0ff113ae9185db5d412c97cc807eaa32aeec7123fbb26f4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091aec1dbe6316386ac553d31438fe061742a97aa65d0e386fb1b9e1d8a630ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5515f76e5333722afb5445ec930fc8fc72d77549b94d4af3a0cc2dcf665d0f3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa6b04f5d42107862d5220c9d419bfd90d42e53bd4d34e601d393bc7ccf2d7b(
    value: typing.Optional[typing.Union[DataOktaUsersSearch, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93cbff457544914c37c6d5908783809b70f1f4d68e36fdfb0b836d568454d60(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0521c75a187e353291ef3230a0861809659fbf476a35cb2fa886875015ade2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dba4f483387786adecea29581c86195a3ab61fe447504e5361c7e6179e6bb99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c145906e8824397de593092dcc15522dfe06eddfa22f3383c9214cdff3728bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a454e3f73610d6fe4df7a4b4f1bd4c9a73d3ed1f38c617ad239a904dda2d2eb2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb79e4090b91ad5c9004562434d8eee3cbfa2d34e990e655a2534f583a2be7ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25a14d2a557d6a0cf71d17164d3efa6220f4b3f25500ccaedaf609e30aaf128a(
    value: typing.Optional[DataOktaUsersUsers],
) -> None:
    """Type checking stubs"""
    pass
