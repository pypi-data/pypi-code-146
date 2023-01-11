'''
# `newrelic_one_dashboard`

Refer to the Terraform Registory for docs: [`newrelic_one_dashboard`](https://www.terraform.io/docs/providers/newrelic/r/one_dashboard).
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


class OneDashboard(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboard",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard newrelic_one_dashboard}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        page: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPage", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard newrelic_one_dashboard} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The dashboard's name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        :param page: page block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#page OneDashboard#page}
        :param account_id: The New Relic account ID where you want to create the dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        :param description: The dashboard's description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#description OneDashboard#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#id OneDashboard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: Determines who can see or edit the dashboard. Valid values are private, public_read_only, public_read_write. Defaults to public_read_only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#permissions OneDashboard#permissions}
        :param variable: variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#variable OneDashboard#variable}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feca567106b8718efc93d950aad2c0578a8de5ce54cbfc6f44ca17c804c2626f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OneDashboardConfig(
            name=name,
            page=page,
            account_id=account_id,
            description=description,
            id=id,
            permissions=permissions,
            variable=variable,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPage")
    def put_page(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPage", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c4803501bb8b54897eae197c2cb79eae7f3709d0d16634d00d600dc23b0f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPage", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9de57c9e41664179a6133c15816d5cc1f1ca4ee5f82ea1597c3225a775e42ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPermissions")
    def reset_permissions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissions", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @builtins.property
    @jsii.member(jsii_name="page")
    def page(self) -> "OneDashboardPageList":
        return typing.cast("OneDashboardPageList", jsii.get(self, "page"))

    @builtins.property
    @jsii.member(jsii_name="permalink")
    def permalink(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permalink"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "OneDashboardVariableList":
        return typing.cast("OneDashboardVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pageInput")
    def page_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPage"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPage"]]], jsii.get(self, "pageInput"))

    @builtins.property
    @jsii.member(jsii_name="permissionsInput")
    def permissions_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e89aeae913cc56708e3bbbe9107e552e4e5a954bdfd7067b870e5dbcb02b5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ec2164b43e91f5ad208b6db064916847ef31a81a329fb92d562206cc3cddfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f751be9c0fc528c2067b3d388841a0c0497c913308ec8296501ff22d1254445e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e256d2cd840af74023616f1df3551e739f981c27ffae0dffe75e35e283538fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="permissions")
    def permissions(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "permissions"))

    @permissions.setter
    def permissions(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2c9555d9ec06b00b525f23399b17b061b23636caf36387a29a9908f2f48904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissions", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardConfig",
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
        "page": "page",
        "account_id": "accountId",
        "description": "description",
        "id": "id",
        "permissions": "permissions",
        "variable": "variable",
    },
)
class OneDashboardConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        page: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPage", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The dashboard's name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        :param page: page block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#page OneDashboard#page}
        :param account_id: The New Relic account ID where you want to create the dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        :param description: The dashboard's description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#description OneDashboard#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#id OneDashboard#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param permissions: Determines who can see or edit the dashboard. Valid values are private, public_read_only, public_read_write. Defaults to public_read_only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#permissions OneDashboard#permissions}
        :param variable: variable block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#variable OneDashboard#variable}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf246025deeda1e6a2d2f0ee4748ee6ac41552f5535bd2c9fec6b73660b58ff)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument page", value=page, expected_type=type_hints["page"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "page": page,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if permissions is not None:
            self._values["permissions"] = permissions
        if variable is not None:
            self._values["variable"] = variable

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
        '''The dashboard's name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def page(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPage"]]:
        '''page block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#page OneDashboard#page}
        '''
        result = self._values.get("page")
        assert result is not None, "Required property 'page' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPage"]], result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The New Relic account ID where you want to create the dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The dashboard's description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#description OneDashboard#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#id OneDashboard#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[builtins.str]:
        '''Determines who can see or edit the dashboard. Valid values are private, public_read_only, public_read_write. Defaults to public_read_only.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#permissions OneDashboard#permissions}
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#variable OneDashboard#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPage",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "widget_area": "widgetArea",
        "widget_bar": "widgetBar",
        "widget_billboard": "widgetBillboard",
        "widget_bullet": "widgetBullet",
        "widget_funnel": "widgetFunnel",
        "widget_heatmap": "widgetHeatmap",
        "widget_histogram": "widgetHistogram",
        "widget_json": "widgetJson",
        "widget_line": "widgetLine",
        "widget_log_table": "widgetLogTable",
        "widget_markdown": "widgetMarkdown",
        "widget_pie": "widgetPie",
        "widget_stacked_bar": "widgetStackedBar",
        "widget_table": "widgetTable",
    },
)
class OneDashboardPage:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        widget_area: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetArea", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_bar: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBar", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_billboard: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBillboard", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_bullet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBullet", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_funnel: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetFunnel", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_heatmap: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetHeatmap", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_histogram: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetHistogram", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetJson", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_line: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetLine", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_log_table: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetLogTable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_markdown: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetMarkdown", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_pie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetPie", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_stacked_bar: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetStackedBar", typing.Dict[builtins.str, typing.Any]]]]] = None,
        widget_table: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetTable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param name: The dashboard page's name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        :param description: The dashboard page's description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#description OneDashboard#description}
        :param widget_area: widget_area block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_area OneDashboard#widget_area}
        :param widget_bar: widget_bar block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_bar OneDashboard#widget_bar}
        :param widget_billboard: widget_billboard block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_billboard OneDashboard#widget_billboard}
        :param widget_bullet: widget_bullet block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_bullet OneDashboard#widget_bullet}
        :param widget_funnel: widget_funnel block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_funnel OneDashboard#widget_funnel}
        :param widget_heatmap: widget_heatmap block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_heatmap OneDashboard#widget_heatmap}
        :param widget_histogram: widget_histogram block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_histogram OneDashboard#widget_histogram}
        :param widget_json: widget_json block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_json OneDashboard#widget_json}
        :param widget_line: widget_line block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_line OneDashboard#widget_line}
        :param widget_log_table: widget_log_table block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_log_table OneDashboard#widget_log_table}
        :param widget_markdown: widget_markdown block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_markdown OneDashboard#widget_markdown}
        :param widget_pie: widget_pie block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_pie OneDashboard#widget_pie}
        :param widget_stacked_bar: widget_stacked_bar block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_stacked_bar OneDashboard#widget_stacked_bar}
        :param widget_table: widget_table block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_table OneDashboard#widget_table}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad90e159424eaeeb508b02cde06a6c3bdd8561b00435df1ce2dd2ebbbbb7fe6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument widget_area", value=widget_area, expected_type=type_hints["widget_area"])
            check_type(argname="argument widget_bar", value=widget_bar, expected_type=type_hints["widget_bar"])
            check_type(argname="argument widget_billboard", value=widget_billboard, expected_type=type_hints["widget_billboard"])
            check_type(argname="argument widget_bullet", value=widget_bullet, expected_type=type_hints["widget_bullet"])
            check_type(argname="argument widget_funnel", value=widget_funnel, expected_type=type_hints["widget_funnel"])
            check_type(argname="argument widget_heatmap", value=widget_heatmap, expected_type=type_hints["widget_heatmap"])
            check_type(argname="argument widget_histogram", value=widget_histogram, expected_type=type_hints["widget_histogram"])
            check_type(argname="argument widget_json", value=widget_json, expected_type=type_hints["widget_json"])
            check_type(argname="argument widget_line", value=widget_line, expected_type=type_hints["widget_line"])
            check_type(argname="argument widget_log_table", value=widget_log_table, expected_type=type_hints["widget_log_table"])
            check_type(argname="argument widget_markdown", value=widget_markdown, expected_type=type_hints["widget_markdown"])
            check_type(argname="argument widget_pie", value=widget_pie, expected_type=type_hints["widget_pie"])
            check_type(argname="argument widget_stacked_bar", value=widget_stacked_bar, expected_type=type_hints["widget_stacked_bar"])
            check_type(argname="argument widget_table", value=widget_table, expected_type=type_hints["widget_table"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if widget_area is not None:
            self._values["widget_area"] = widget_area
        if widget_bar is not None:
            self._values["widget_bar"] = widget_bar
        if widget_billboard is not None:
            self._values["widget_billboard"] = widget_billboard
        if widget_bullet is not None:
            self._values["widget_bullet"] = widget_bullet
        if widget_funnel is not None:
            self._values["widget_funnel"] = widget_funnel
        if widget_heatmap is not None:
            self._values["widget_heatmap"] = widget_heatmap
        if widget_histogram is not None:
            self._values["widget_histogram"] = widget_histogram
        if widget_json is not None:
            self._values["widget_json"] = widget_json
        if widget_line is not None:
            self._values["widget_line"] = widget_line
        if widget_log_table is not None:
            self._values["widget_log_table"] = widget_log_table
        if widget_markdown is not None:
            self._values["widget_markdown"] = widget_markdown
        if widget_pie is not None:
            self._values["widget_pie"] = widget_pie
        if widget_stacked_bar is not None:
            self._values["widget_stacked_bar"] = widget_stacked_bar
        if widget_table is not None:
            self._values["widget_table"] = widget_table

    @builtins.property
    def name(self) -> builtins.str:
        '''The dashboard page's name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The dashboard page's description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#description OneDashboard#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def widget_area(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetArea"]]]:
        '''widget_area block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_area OneDashboard#widget_area}
        '''
        result = self._values.get("widget_area")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetArea"]]], result)

    @builtins.property
    def widget_bar(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBar"]]]:
        '''widget_bar block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_bar OneDashboard#widget_bar}
        '''
        result = self._values.get("widget_bar")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBar"]]], result)

    @builtins.property
    def widget_billboard(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBillboard"]]]:
        '''widget_billboard block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_billboard OneDashboard#widget_billboard}
        '''
        result = self._values.get("widget_billboard")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBillboard"]]], result)

    @builtins.property
    def widget_bullet(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBullet"]]]:
        '''widget_bullet block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_bullet OneDashboard#widget_bullet}
        '''
        result = self._values.get("widget_bullet")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBullet"]]], result)

    @builtins.property
    def widget_funnel(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetFunnel"]]]:
        '''widget_funnel block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_funnel OneDashboard#widget_funnel}
        '''
        result = self._values.get("widget_funnel")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetFunnel"]]], result)

    @builtins.property
    def widget_heatmap(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHeatmap"]]]:
        '''widget_heatmap block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_heatmap OneDashboard#widget_heatmap}
        '''
        result = self._values.get("widget_heatmap")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHeatmap"]]], result)

    @builtins.property
    def widget_histogram(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHistogram"]]]:
        '''widget_histogram block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_histogram OneDashboard#widget_histogram}
        '''
        result = self._values.get("widget_histogram")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHistogram"]]], result)

    @builtins.property
    def widget_json(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetJson"]]]:
        '''widget_json block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_json OneDashboard#widget_json}
        '''
        result = self._values.get("widget_json")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetJson"]]], result)

    @builtins.property
    def widget_line(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLine"]]]:
        '''widget_line block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_line OneDashboard#widget_line}
        '''
        result = self._values.get("widget_line")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLine"]]], result)

    @builtins.property
    def widget_log_table(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLogTable"]]]:
        '''widget_log_table block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_log_table OneDashboard#widget_log_table}
        '''
        result = self._values.get("widget_log_table")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLogTable"]]], result)

    @builtins.property
    def widget_markdown(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetMarkdown"]]]:
        '''widget_markdown block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_markdown OneDashboard#widget_markdown}
        '''
        result = self._values.get("widget_markdown")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetMarkdown"]]], result)

    @builtins.property
    def widget_pie(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetPie"]]]:
        '''widget_pie block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_pie OneDashboard#widget_pie}
        '''
        result = self._values.get("widget_pie")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetPie"]]], result)

    @builtins.property
    def widget_stacked_bar(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetStackedBar"]]]:
        '''widget_stacked_bar block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_stacked_bar OneDashboard#widget_stacked_bar}
        '''
        result = self._values.get("widget_stacked_bar")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetStackedBar"]]], result)

    @builtins.property
    def widget_table(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetTable"]]]:
        '''widget_table block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#widget_table OneDashboard#widget_table}
        '''
        result = self._values.get("widget_table")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetTable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cff5a67842ce39ee793086a8751ca33e6db073a384983147ac8b5a82a2bf90d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19fafd33a889731bf38d89935767917448bd94db445264feccf9799526b6392c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5c4cccd632b3d63b2e46a24a280f42abecf0e2775433501028069f320b8a914)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b557b195645bb7553b9deb9d116599cc8b20fd5bc19022186504ee6c236d9618)
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
            type_hints = typing.get_type_hints(_typecheckingstub__030b8a998f62bcb54c79ced0a98aa03b55acef12de0acd1f89d97ca232147bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82ff19f4a9b0e1cc4c0efe0ae026a121e88538f2ef4eeb5c8a4c6d620ee034b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__812cda7b001a2fdcb6c1a9e9fa043d9092d77ff2c7b9a1583a90d7969348651c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putWidgetArea")
    def put_widget_area(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetArea", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc40807903017bb98d2bc10303e803173880f844245748c8ccc2f53de964066)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetArea", [value]))

    @jsii.member(jsii_name="putWidgetBar")
    def put_widget_bar(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBar", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70dccb11444f8b75235a86f241a576d426cb76ae4b4f99d8dbbd9b31f6d12f4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetBar", [value]))

    @jsii.member(jsii_name="putWidgetBillboard")
    def put_widget_billboard(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBillboard", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f56c048406405ead03777bf8e7c4211d75e6f41c76ee8d8694d2e96c3ca4277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetBillboard", [value]))

    @jsii.member(jsii_name="putWidgetBullet")
    def put_widget_bullet(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBullet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777087add7016c4857de95b7f8a53b06aaf674685e0b9f527e90971a4ce52472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetBullet", [value]))

    @jsii.member(jsii_name="putWidgetFunnel")
    def put_widget_funnel(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetFunnel", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a865e47824c262809ae0c6eb30214c28fc1a9d4c3dcd4691d3ac5ece4d3423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetFunnel", [value]))

    @jsii.member(jsii_name="putWidgetHeatmap")
    def put_widget_heatmap(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetHeatmap", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c57fd9012eb439ed8fe92047b0ee43fae8b291d7438f4322813dfceba9d9d5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetHeatmap", [value]))

    @jsii.member(jsii_name="putWidgetHistogram")
    def put_widget_histogram(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetHistogram", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b448a939ecb5fe12b3d9d0a3a51f49ab77b9f9ce03c391ce898f826bcdc2937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetHistogram", [value]))

    @jsii.member(jsii_name="putWidgetJson")
    def put_widget_json(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetJson", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e70f96de5d02450424dda738f11db90e35af6eb3cf1954f739695aba0117a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetJson", [value]))

    @jsii.member(jsii_name="putWidgetLine")
    def put_widget_line(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetLine", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefd6046dab76fe13e484e4ed3aeee6ae36ece945ef8bd2a7de2a25c6f8ea2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetLine", [value]))

    @jsii.member(jsii_name="putWidgetLogTable")
    def put_widget_log_table(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetLogTable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71ccafb0891025b1e4de88c4a7d4d036065d9b7e843d5ab8cad1cc39678827dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetLogTable", [value]))

    @jsii.member(jsii_name="putWidgetMarkdown")
    def put_widget_markdown(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetMarkdown", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85d2e66a6af0d94b94ad2734a4cf09366ea58a431906830f37e9e9851cca8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetMarkdown", [value]))

    @jsii.member(jsii_name="putWidgetPie")
    def put_widget_pie(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetPie", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__396a554edb1a0ebf81e3c63cd05b160d67ad05f82b56df5907f28aacdc200b6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetPie", [value]))

    @jsii.member(jsii_name="putWidgetStackedBar")
    def put_widget_stacked_bar(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetStackedBar", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a66da789f19569d92b64b12b233faf45fd0ec90996eb25237a582345d8157b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetStackedBar", [value]))

    @jsii.member(jsii_name="putWidgetTable")
    def put_widget_table(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetTable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6795d358808e2ddd9c69ec6409d7210f9d0967310cca777453726303510bd3b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWidgetTable", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetWidgetArea")
    def reset_widget_area(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetArea", []))

    @jsii.member(jsii_name="resetWidgetBar")
    def reset_widget_bar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetBar", []))

    @jsii.member(jsii_name="resetWidgetBillboard")
    def reset_widget_billboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetBillboard", []))

    @jsii.member(jsii_name="resetWidgetBullet")
    def reset_widget_bullet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetBullet", []))

    @jsii.member(jsii_name="resetWidgetFunnel")
    def reset_widget_funnel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetFunnel", []))

    @jsii.member(jsii_name="resetWidgetHeatmap")
    def reset_widget_heatmap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetHeatmap", []))

    @jsii.member(jsii_name="resetWidgetHistogram")
    def reset_widget_histogram(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetHistogram", []))

    @jsii.member(jsii_name="resetWidgetJson")
    def reset_widget_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetJson", []))

    @jsii.member(jsii_name="resetWidgetLine")
    def reset_widget_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetLine", []))

    @jsii.member(jsii_name="resetWidgetLogTable")
    def reset_widget_log_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetLogTable", []))

    @jsii.member(jsii_name="resetWidgetMarkdown")
    def reset_widget_markdown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetMarkdown", []))

    @jsii.member(jsii_name="resetWidgetPie")
    def reset_widget_pie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetPie", []))

    @jsii.member(jsii_name="resetWidgetStackedBar")
    def reset_widget_stacked_bar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetStackedBar", []))

    @jsii.member(jsii_name="resetWidgetTable")
    def reset_widget_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidgetTable", []))

    @builtins.property
    @jsii.member(jsii_name="guid")
    def guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "guid"))

    @builtins.property
    @jsii.member(jsii_name="widgetArea")
    def widget_area(self) -> "OneDashboardPageWidgetAreaList":
        return typing.cast("OneDashboardPageWidgetAreaList", jsii.get(self, "widgetArea"))

    @builtins.property
    @jsii.member(jsii_name="widgetBar")
    def widget_bar(self) -> "OneDashboardPageWidgetBarList":
        return typing.cast("OneDashboardPageWidgetBarList", jsii.get(self, "widgetBar"))

    @builtins.property
    @jsii.member(jsii_name="widgetBillboard")
    def widget_billboard(self) -> "OneDashboardPageWidgetBillboardList":
        return typing.cast("OneDashboardPageWidgetBillboardList", jsii.get(self, "widgetBillboard"))

    @builtins.property
    @jsii.member(jsii_name="widgetBullet")
    def widget_bullet(self) -> "OneDashboardPageWidgetBulletList":
        return typing.cast("OneDashboardPageWidgetBulletList", jsii.get(self, "widgetBullet"))

    @builtins.property
    @jsii.member(jsii_name="widgetFunnel")
    def widget_funnel(self) -> "OneDashboardPageWidgetFunnelList":
        return typing.cast("OneDashboardPageWidgetFunnelList", jsii.get(self, "widgetFunnel"))

    @builtins.property
    @jsii.member(jsii_name="widgetHeatmap")
    def widget_heatmap(self) -> "OneDashboardPageWidgetHeatmapList":
        return typing.cast("OneDashboardPageWidgetHeatmapList", jsii.get(self, "widgetHeatmap"))

    @builtins.property
    @jsii.member(jsii_name="widgetHistogram")
    def widget_histogram(self) -> "OneDashboardPageWidgetHistogramList":
        return typing.cast("OneDashboardPageWidgetHistogramList", jsii.get(self, "widgetHistogram"))

    @builtins.property
    @jsii.member(jsii_name="widgetJson")
    def widget_json(self) -> "OneDashboardPageWidgetJsonList":
        return typing.cast("OneDashboardPageWidgetJsonList", jsii.get(self, "widgetJson"))

    @builtins.property
    @jsii.member(jsii_name="widgetLine")
    def widget_line(self) -> "OneDashboardPageWidgetLineList":
        return typing.cast("OneDashboardPageWidgetLineList", jsii.get(self, "widgetLine"))

    @builtins.property
    @jsii.member(jsii_name="widgetLogTable")
    def widget_log_table(self) -> "OneDashboardPageWidgetLogTableList":
        return typing.cast("OneDashboardPageWidgetLogTableList", jsii.get(self, "widgetLogTable"))

    @builtins.property
    @jsii.member(jsii_name="widgetMarkdown")
    def widget_markdown(self) -> "OneDashboardPageWidgetMarkdownList":
        return typing.cast("OneDashboardPageWidgetMarkdownList", jsii.get(self, "widgetMarkdown"))

    @builtins.property
    @jsii.member(jsii_name="widgetPie")
    def widget_pie(self) -> "OneDashboardPageWidgetPieList":
        return typing.cast("OneDashboardPageWidgetPieList", jsii.get(self, "widgetPie"))

    @builtins.property
    @jsii.member(jsii_name="widgetStackedBar")
    def widget_stacked_bar(self) -> "OneDashboardPageWidgetStackedBarList":
        return typing.cast("OneDashboardPageWidgetStackedBarList", jsii.get(self, "widgetStackedBar"))

    @builtins.property
    @jsii.member(jsii_name="widgetTable")
    def widget_table(self) -> "OneDashboardPageWidgetTableList":
        return typing.cast("OneDashboardPageWidgetTableList", jsii.get(self, "widgetTable"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetAreaInput")
    def widget_area_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetArea"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetArea"]]], jsii.get(self, "widgetAreaInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetBarInput")
    def widget_bar_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBar"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBar"]]], jsii.get(self, "widgetBarInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetBillboardInput")
    def widget_billboard_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBillboard"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBillboard"]]], jsii.get(self, "widgetBillboardInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetBulletInput")
    def widget_bullet_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBullet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBullet"]]], jsii.get(self, "widgetBulletInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetFunnelInput")
    def widget_funnel_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetFunnel"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetFunnel"]]], jsii.get(self, "widgetFunnelInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetHeatmapInput")
    def widget_heatmap_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHeatmap"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHeatmap"]]], jsii.get(self, "widgetHeatmapInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetHistogramInput")
    def widget_histogram_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHistogram"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHistogram"]]], jsii.get(self, "widgetHistogramInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetJsonInput")
    def widget_json_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetJson"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetJson"]]], jsii.get(self, "widgetJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetLineInput")
    def widget_line_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLine"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLine"]]], jsii.get(self, "widgetLineInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetLogTableInput")
    def widget_log_table_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLogTable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLogTable"]]], jsii.get(self, "widgetLogTableInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetMarkdownInput")
    def widget_markdown_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetMarkdown"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetMarkdown"]]], jsii.get(self, "widgetMarkdownInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetPieInput")
    def widget_pie_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetPie"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetPie"]]], jsii.get(self, "widgetPieInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetStackedBarInput")
    def widget_stacked_bar_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetStackedBar"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetStackedBar"]]], jsii.get(self, "widgetStackedBarInput"))

    @builtins.property
    @jsii.member(jsii_name="widgetTableInput")
    def widget_table_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetTable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetTable"]]], jsii.get(self, "widgetTableInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8b1deec46dac39726858185173d5ccb5acdc12a0988922bae82e579f334d4b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d0d6310069491de3c098640fd45c8b59928e2a1c55b8ba4ea371fc8cbfe14b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPage, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPage, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPage, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38905a63f7ca2cf0fa26532e7489db78097b0ac33dd4a9c9c1e9d9e26788f7a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetArea",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetArea:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetAreaNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f54147f0484c97291ee89b7cc0b4a467986eff65c7bfade83cb0e27f7d5448)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetAreaNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetAreaNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetArea(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetAreaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetAreaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f57e7a42531872c8b50b58a8f3e4189fdd3bd7ad6b21ed8510103762887d67)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetAreaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e7e2557492f7e3c22f77282de0fa5fd7a12f3871ea35624a4342fb721aeb629)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetAreaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__219eea473fe7d0372257d6a8c5a06a26b15cf07893a39fab8931e50b5e5da411)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67da9de2ee0461ac9ddcf4923789cc45ca186593aa40d32c157372736a39464c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca2b2110e3751cfa4de2e7db8b5387a82c61e8a91154c25bd074342ba1a21e8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetArea]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetArea]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetArea]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5f82482d2338f77c052b3f96b9daf2a93e44fa5c13b82d53ed00d0f91145ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetAreaNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetAreaNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957a77ef06d2b06a5ed740f10df5fea7f9c08a538f37ef5435446df7ab99fd05)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetAreaNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetAreaNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetAreaNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3700326127ab76a4fe666e375c5b74b367f238b0602323ad988c09e5bc72a686)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetAreaNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4933d6a83022b05b4717e18e4297dcbf055c8b10671423fe4ae50885922de5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetAreaNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c649c70a8ff909456d0de8eccdfc70d69bd3fa230c58100925c5215405f5927c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__69ef6e7e29772966882d3cc62e8e856abcd16e4e7769ba232a39a026a6554f05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72df003ff9d45093cbdba688a207d093dd4774cedecbaa105eee9f35eaf2f4bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetAreaNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetAreaNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetAreaNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4a2ad5ed1541c1c0fa96d4df410c60218cefa1eabe123d4c6b7af674f77031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetAreaNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetAreaNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__198506a28cc10e1cb203a914fd29564d95f805e118bb241ceac9b6e80110de73)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e62be1affe33864dea41eed3b0c10dbdc3f65ca438c7c50bb012cbf5240f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b19eaeb18507cd5eeedce89ef86fdaea7a0cb83533da28562c02f11735f7e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9f6f1ac5d3ec75b2597b6a506f1866c22939fe9ea0f599e9eb2ebdac7c793dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetAreaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetAreaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e34f6d2f11ebffd5380995e337bd9918482bed3f521c0fadee03c5d200694cdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1beb89b4a4773fa3959de85504057e34fe8666bd03e7a623e7cc731ed6a3e2c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetAreaNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetAreaNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetAreaNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetAreaNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9ec47174de1df60d0e6656643a49fba7d15182277351b06eb5b5474227a63e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b925daa15a3c52ca42453cc7401e423c2ae2a37beb7861f8b523f6d4e4ba4489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc0c44dbbddbaed7648c0c968649dfcf51b1335ba3bd372805405455eeea437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a2526ff077a49d64dc0133bf9674ac9716540cdd52c84fe0666507f0cc44f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2785e9b50ef3975fd112f7847c6b01777127437d126e98bd5a927e93e1004c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2923b233cd6d7378eb5fd31112c2cb1acd6a5917505f9289d22c82e27b2be82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetArea, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetArea, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetArea, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e8fed6d42099125f481658f092a85657f5a5c1d133caaace195eb11e918897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBar",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "filter_current_dashboard": "filterCurrentDashboard",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "linked_entity_guids": "linkedEntityGuids",
        "width": "width",
    },
)
class OneDashboardPageWidgetBar:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBarNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param filter_current_dashboard: Use this item to filter the current dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param linked_entity_guids: Related entities. Currently only supports Dashboard entities, but may allow other cases in the future. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7fd8f09732c40f5c70b0c3f4f6ccdd6538746442266f32a806a4c3c807c797)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument filter_current_dashboard", value=filter_current_dashboard, expected_type=type_hints["filter_current_dashboard"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument linked_entity_guids", value=linked_entity_guids, expected_type=type_hints["linked_entity_guids"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if filter_current_dashboard is not None:
            self._values["filter_current_dashboard"] = filter_current_dashboard
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if linked_entity_guids is not None:
            self._values["linked_entity_guids"] = linked_entity_guids
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBarNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBarNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_current_dashboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use this item to filter the current dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        '''
        result = self._values.get("filter_current_dashboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def linked_entity_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Related entities. Currently only supports Dashboard entities, but may allow other cases in the future.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        '''
        result = self._values.get("linked_entity_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetBar(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetBarList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBarList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85b5486f560cbe28b41402719068f9150ba0307b2e9e92fcf31f2205686d7b9a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetBarOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0657dfa99d288047ff79f42ead5444750670c769866c9b74c2ba28d2f9c4a3c8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetBarOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d5c5fced03c6b0f78e95318b7d7ada3184262de6a9a5340cf9592ad8f056af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6cb4689f24b1b13343b9023eaa9c0173103f4c86450d4391ed915ff954e468cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abb120db001e855d2ff7b2f885953d2a80565de28b7a26891c5f4a2cf20ab8fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBar]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBar]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBar]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11be4a4fbc649867e11e91216f90f4c0cfd8cbf394bed19d69c667c49b1ecb49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBarNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetBarNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a9443b6c0754224b7df09b9601b83e2dffe0f14164ac765f119d65d6812dd2)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetBarNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetBarNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBarNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ac5c266eeef75b5b0cd5d5882576e74e14ce248ca9c192d7b2d6719954df06f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetBarNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1657e5f419f31a9561ac3df55e1af295ad1aca3d91462a72586e7ffb415adb5f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetBarNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5c9d1c5af069284cf3af71764ff14ca5a3839e369484920f04463743c9bce10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e73fdb95acf20e9f7df0bfe45bdff630cf3de9011520f85b9b249f654de9ef4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9d8515f55c159fd6cc3d70d3fc78395afcea937334e87367e7bc08746a455f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBarNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBarNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBarNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__140bf3eeed3bad2af69c6de7632b56b01ede4e0f1fc8486859351322e801b5f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetBarNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBarNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f472d68d8ed0e291396f1e4e20c37ec1e178682d900070a8a82d04ae75eef53)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__945868a74b0681e0cd2b3cc9316a6c28ee3a852c5936aa321791b11a723670aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b48ee21ae3d6865a2b4d284f94f6316f1ca8b24997b8c74a2bec609e44e4d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetBarNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetBarNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetBarNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__443d296956e2a1e1f7b0f64b99e6fab3490408bcdca0c17be288dd59601ae766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetBarOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBarOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f0d3347255e73a5ab0040ae4818356866c1d01e6851264b11d2ae1f209895e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBarNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e49a042f684f05e397f03acd7d3d2ad9edd4badd08b576eb6e0a9a855f432529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetFilterCurrentDashboard")
    def reset_filter_current_dashboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCurrentDashboard", []))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetLinkedEntityGuids")
    def reset_linked_entity_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedEntityGuids", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetBarNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetBarNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboardInput")
    def filter_current_dashboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterCurrentDashboardInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuidsInput")
    def linked_entity_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linkedEntityGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBarNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBarNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c0a295dcaf6f2934705b69e71d6baa4091743148aa2df5c3198e9e334ca27e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboard")
    def filter_current_dashboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterCurrentDashboard"))

    @filter_current_dashboard.setter
    def filter_current_dashboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a09b0fac3db716b2bba83ee56eefd7ba60d07ac25fc367eada924a2bdfe7d573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterCurrentDashboard", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21198abb6340923fa8e662cc2f258e227b8eb3fe7236a02c4bac6220d1d63ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd031a028f45f767d27837808315ae8250ec1c7a73bb4f2a0413baad3b55b93c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuids")
    def linked_entity_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "linkedEntityGuids"))

    @linked_entity_guids.setter
    def linked_entity_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a54078c351d49bf3f83eda5da11fd9fd1b949b8f33ac6af0bb4919298be6c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedEntityGuids", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e47d5555af8927b028672ab5e440854d2ac9732cb8be92ed10ffe7df75d027)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b3dbb25a65ff1b86cea9d0a720ea6a86ff5aba1a895bc2037775ac6b1f66bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257a41382f8f4cebf3117ea423737cd31517c06887a1adea9895a547ffe78fd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetBar, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetBar, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetBar, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72d03546533b8322f04e13122ff247c06e1fd29ad50251ea45fa8fb01ad4b88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBillboard",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "critical": "critical",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "warning": "warning",
        "width": "width",
    },
)
class OneDashboardPageWidgetBillboard:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBillboardNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        critical: typing.Optional[builtins.str] = None,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        warning: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param critical: The critical threshold value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#critical OneDashboard#critical}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param warning: The warning threshold value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#warning OneDashboard#warning}
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4519ff1c610e118dde2c95bf8426f5724dfa9398cd0519416b372703ee0f53a6)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if critical is not None:
            self._values["critical"] = critical
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if warning is not None:
            self._values["warning"] = warning
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBillboardNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBillboardNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def critical(self) -> typing.Optional[builtins.str]:
        '''The critical threshold value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#critical OneDashboard#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def warning(self) -> typing.Optional[builtins.str]:
        '''The warning threshold value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#warning OneDashboard#warning}
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetBillboard(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetBillboardList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBillboardList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__894fdab0f58338f0b572982508016551d77bf9dea527bdcc9252b74d49d6c05e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetBillboardOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46e0c9c70918be2a6b2f97413afa7d53548ba4ffd44f4c28957b419fc720183)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetBillboardOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3513ee2b75ba0a7cf72a8d2a3b666263335324ef3ab7ac439d658ecd79f6a5e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b50e130bfe66b9e2248172a008b949d1b01b3dae6d5cdfaa3091b0cd847c9392)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72c36205dd37c589015f42cc775e72fa5cf6a5b36526e888f03aacb342768dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboard]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboard]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboard]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72e79a0b43824b61866cfcdcdd1ef386ae5f13fb9fa13e7fbda439443a483467)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBillboardNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetBillboardNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aafa3074e861e1d5ebf2e8c4077b3dfa1f545d4b2db6d102bae2a908189a3598)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetBillboardNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetBillboardNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBillboardNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48377d1f09f6fa228f0b8a8c06e85d85be44eeacf8f152b24da4f02b4e58c2f3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetBillboardNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee644d2f4c7fb4dc3d5c77c8051148e822c03b5ef83ee9b02b93e3e1e31b8c87)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetBillboardNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3c47a15a87e0c14f9c702394fab3fc33effc9d1be71d23db9f18545329d317a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f03eefe536ec78a1237cd8ad54fa4af08823da15946d3218a76b4caba9d9f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__418d6735c96d7f2144d86c144c05e84a9b5ffd3739348b45afce2841a416a1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboardNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboardNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboardNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88631c13b2527746d3f58d88744cf32495cbfbf120427d3ca139acc8730ddd33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetBillboardNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBillboardNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f1a55f09aafc860275896e0376bf0dbcadd7982bae99a11e13444a5e58ce48a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76a466793b66e28573281916b44fc7d6344b2e8e84f025b8182c639f6772f6b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4da882a93de44627d05dcfbdfb9d0b3f37a8d1ab73c978d6626d5c22105e7cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0279a8a50903b255714cc3158eeecc6134583afd1b2eec59f9432963da0e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetBillboardOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBillboardOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b2a58c80eb16a1e50a5ab1bdaba280dfd71696708a83f71e15b5389bf845578)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a296a21633fa7f7b7a4d45fc88a73bb60b7641b013839bba730bb8a68150e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetCritical")
    def reset_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCritical", []))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetBillboardNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetBillboardNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboardNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboardNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a18dffa16f429263e7d27b2371285a08dd64bfab2e742f1f690cc46993bb7c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "critical"))

    @critical.setter
    def critical(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e139c1d753b5fbe05a725c540362ffcf60a4f4c9efe95e76fbc01cacdc3b7962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0b1875c5ee7f0a0831783325d83299bb4b1489cd4847fad5446a0a5e8bc341)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0de7ab04d21d6f62effbf6aa02e21c5a247caa8642170a1c186fdccccf43a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e4fd9a3bba4caf7de4314341d1309ca69deac272637cdde9d618c5762c228c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6fc0e22620ebe540aedfb24f046292d0c0e3d9f315e858e80a66c993d85a30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "warning"))

    @warning.setter
    def warning(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9327724f805ffeaacb104c68f13bd5e209426601540f8b764d6ae606736558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "warning", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc40fb460a2882fbecb1c489b1626d7801f4545dbaa39bf186c99a5ffa7124c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetBillboard, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetBillboard, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetBillboard, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd280d1ba2eb59f0afb44d739c9133da4dc36f41160c491cf27a8aaa06c96411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBullet",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "limit": "limit",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetBullet:
    def __init__(
        self,
        *,
        column: jsii.Number,
        limit: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetBulletNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param limit: The maximum value for the visualization. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#limit OneDashboard#limit}
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1eddc8ab7bda5dc1856a97b6e9a0daa659f395c405b38d7f1aaed4d210e590f)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument limit", value=limit, expected_type=type_hints["limit"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "limit": limit,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def limit(self) -> jsii.Number:
        '''The maximum value for the visualization.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#limit OneDashboard#limit}
        '''
        result = self._values.get("limit")
        assert result is not None, "Required property 'limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBulletNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetBulletNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetBullet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetBulletList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBulletList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3852ea534a10337bef8d8d4948320a74e40e6892d8eba9d3e90caf1733e347e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetBulletOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccf70bb55a2d3ddbf1611a392159d3a4f32c3e0bd3ca126acce1dd602ff6b011)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetBulletOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c01d19b1a4ada2a2366f02c577516aa90772f1481174f54dcdd73eed3f38eaee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d44eb5d97732f8a43e7e91ac2b25eafb65aa35e3cdc8b5f964908444523aa7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa71dee47c241fb33bd778fe2964ca01d2f63bf794ec2dd8515da2b5e9a10574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBullet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBullet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBullet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d1466b5ed53a0a827db75cef6c6cacb917349c128cec6893f7fb464bb1134f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBulletNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetBulletNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__830407ff9c790892d7f3d865d2e12e4b5e33ea3848217ae530bfcb329328e5e2)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetBulletNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetBulletNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBulletNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa632382ceb6ac5f9793b4e7f35a9cf5604ef143cee22563ad2f291349f31c6f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetBulletNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2234b67d237340a19724a04e952446ace59e80605aae39a64a31074f374cd05f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetBulletNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__539dcbd59fa549868ce6af9bca57a114e143e4689f65d7b84d82405966d13559)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf01d7766ccf39888ecf6c6ca8e82cd4abab920d2ec0ce2d576f5cb1f83d8bdf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a0d6fdec01fb5c0864a6d8e345e017cedd7856459d9c5546f8a487f1c362a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBulletNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBulletNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBulletNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8124207fe863c347857484fdf131470697bcf90167e8ff518d174eed9b4bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetBulletNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBulletNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7418bf484b6c56d82111e44b59e4537e944b10eef223caa83ba3c79b4e7c335b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e28b5a7c62256cac6bcea277a72794a992f5e547dc9038ac289e4aa8d94e6827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__566768ac9cf64270dc0012afdeeb81aed713e2867f448ede93a8e7d28b16e73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ef039acd99a1484a800d026842f309dc2dd7772a344304840c835905c1bccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetBulletOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetBulletOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cbc29faf7db3077ad18ed7adef206724bb40a3ec0c0e2635baf803de7c24b0c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91ddd8d69381a842f9e8b16f44cc9c751ad6a3e9cfed50a4047f1233b773177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetBulletNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetBulletNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="limitInput")
    def limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "limitInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBulletNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBulletNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__121461dfcf0f6009638d5315e2b760d253ce8e1db8dca3855ac882defed4adf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebde968b9e629fcdef60488d2d60b8ec38907c96327432783c2fd186c7b98e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38cb579f1593999e34a2ac80a6f718e6affaefdb53153397b581fb23b2da3dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="limit")
    def limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "limit"))

    @limit.setter
    def limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b7850fab8e4d9531df7225e0afff389f82087fc44c66a9afd7396ab056d045)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "limit", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a50099ed247ebe9901b5b4b4c7ce3fafe5b9bdb09b181131ce7669e48ad8cb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9734507856a058302b91d644b544a4153903268d88dcdfbf1b0b666cf060fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe19dd3afd9bb3c6ffab99310f4916094d6e197e0d340940bdbdeba3410d6dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetBullet, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetBullet, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetBullet, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ea5a899a8dee914d61f6586ef998506dee739f05e07b2a761a79515f8c1ae23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetFunnel",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetFunnel:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetFunnelNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ecd9a6b0fb08de51cb5866fa122f575713c64086df42aff6d60640694311943)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetFunnelNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetFunnelNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetFunnel(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetFunnelList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetFunnelList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21fceba0d6768354f26a811503217927cf9cd31b3bea45ac6d6e160498c9d54c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetFunnelOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0f2f6545b1f8feaac3b067774befa68e457cd9399d2642c385c250ca011ba0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetFunnelOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5361d9a7ced494aed67622964bcf1f686da82addf31c1a289df6a32043d96e41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dde6feea9845fdf87fafb64f8cfffbddffc924b2c6cef3e951b548b06f83d9a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88b6cdb94df3888c22adced4f1661a7add5472b58eaa84d640c8ceb428e7c9c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnel]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnel]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnel]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76637a88105678d2f0c3f437e6dc18564e20d126c46e46b21ebc6fc1eb3f2a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetFunnelNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetFunnelNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18599d442fc91055a62517eda1609f83a90bff913719ef9f7be06aff0640fa5)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetFunnelNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetFunnelNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetFunnelNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__304d58510782c486f012360f9c06311ab9b6f7d832a6a8ba982c00284fa902da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetFunnelNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a42fa844c0b2250ee106c9b4c9fed2b4d76a02ca0966047fd3dda9f68f158b59)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetFunnelNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e018ca08335cba86810a716eaa08292df209c1fa0abf06f4e4d2d6e8311fdc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63ee0c2ea00364fc8e40043b6d96de6918a8d77b54b57fa776aeb946348c9640)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c034c46b8e6f6ab36707ad3e3f44ae6007c429634d3164cc840454c033caeed2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnelNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnelNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnelNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6a0a82fae381d175bb094d91cc4289b4899030a57324be951223c2d56f5ea8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetFunnelNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetFunnelNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2083d024a1fea48a05e376d09dbf600ddd0facbf33a12a36d3957057c19a4200)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617570785272fc9cb485f7719e4d7052a00a05781dcfcb092a47f2441fade482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbca120b6c6f516b2cd2b5c239538dcfd595aef472707099cba7098ea5a48c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d79eb646d91b56c6df7c99c2a364ff4627da7bf21e1075e00317e7b92b39ee20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetFunnelOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetFunnelOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7212d0d1203e0b5cf6564bd475e8784e8b82316533aa1c6fb2a4fa1510ffeb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__137909aa4c853fe36b1cd736f01f94150c0ca1c7ce7872604e0f3d73cc821bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetFunnelNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetFunnelNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnelNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnelNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0aa2a7d357a9e1173b0f806439414ad5829fcf17f64d2a4cc971fdea7fa8f0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8342254ebd02fbe1767c7ec5272c45c0e0657e2a8774de30545ed853cd8c463b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24270658967482c61afb5297c564dcc4550cf22a24dc32d514cfa55c1c0459e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d8c46fd94511ab72c2e47bf9c68a68aee4cf05c061644dbe5e5de5a496d566)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed1d12433c0c6ce3e4e934fe86ba5d7181916c9033f9973110babfa31dee7db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b87e22b23df9145d3912e5597245e5d6de128baa82a033f32a03134ab16f4e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetFunnel, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetFunnel, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetFunnel, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22a4e82cf4c04d694410031fe7806629d618879919776ed89900ff190990c5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHeatmap",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "filter_current_dashboard": "filterCurrentDashboard",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "linked_entity_guids": "linkedEntityGuids",
        "width": "width",
    },
)
class OneDashboardPageWidgetHeatmap:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetHeatmapNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param filter_current_dashboard: Use this item to filter the current dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param linked_entity_guids: Related entities. Currently only supports Dashboard entities, but may allow other cases in the future. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a48668e851711da36e9562bf945f2418c3a6c87d91621b6b38cd7de2c3cb5f3)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument filter_current_dashboard", value=filter_current_dashboard, expected_type=type_hints["filter_current_dashboard"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument linked_entity_guids", value=linked_entity_guids, expected_type=type_hints["linked_entity_guids"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if filter_current_dashboard is not None:
            self._values["filter_current_dashboard"] = filter_current_dashboard
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if linked_entity_guids is not None:
            self._values["linked_entity_guids"] = linked_entity_guids
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHeatmapNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHeatmapNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_current_dashboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use this item to filter the current dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        '''
        result = self._values.get("filter_current_dashboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def linked_entity_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Related entities. Currently only supports Dashboard entities, but may allow other cases in the future.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        '''
        result = self._values.get("linked_entity_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetHeatmap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetHeatmapList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHeatmapList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51caa13b0ebb5bdb86ea44014acc44d3d15ba1ce9bd3d45c9176913accf7d07a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetHeatmapOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f49a9514adc18db6a887eadaae2bb3210799ea2d37dff953b5ebc00c02b906)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetHeatmapOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6b9c8c9f6a45cd39eb97b05b41c146b2e533ba170a55cb90f3f5e0111e0d0f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e42431a8819d7cb334d968d4d03d1f384bf4c4fb29173d6b9cc2e3f1d7960de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f919e8ac7d53e5765149e96db31be15c67c2c9e47ddc09c84c17506728a08e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmap]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmap]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmap]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d23626f4696aa43f80dd511ada0bc63dd55cf49f173b155e41ad5a964f24e96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHeatmapNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetHeatmapNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48f6ea791b34a1fab69ea90cc7a764d46c48a5859ac6aee2d122e71d1a6e0b49)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetHeatmapNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetHeatmapNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHeatmapNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e982f44ccdcefa53701b5f47c5822292ebf6544e48b8780914f24b5c81251695)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetHeatmapNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0872650b35cdbbcd0aef59b5ec366915af24e187dcdb5b3e0546c0220e346138)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetHeatmapNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b032d7134f4987cc5efe53eaf4ae3ca3080307480f04d63237359af3ef8ee5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f12c7348622730b8456a40e83aa67fbc3c0e3e9244f159f02853dd6e61f1ac1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b06789c59c116f26a5c79c03e4de1cb6268d1da8273e0183e9dc3a3a36ef5f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmapNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmapNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmapNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64491ce37caedf0753c638035eaaead850a5ef3535af87b337563b13cee38395)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetHeatmapNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHeatmapNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__44749baacbf0262c14a862db751c5f78e4c4ff426389a467a66b410680bb331e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a47a015b5eeb328ed06dc15ba5ed4bd5ff30d0e9300233f866e1b21cd8db04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ede34d867fb31c22914653b4f50ceaead4e29583161ac77e97a6f8531147df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5ec99b27d6ef8cd032b44e314d88089262af84fd7953cb3a6459576557a940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetHeatmapOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHeatmapOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6aee874e2c9d9750dcb6f1716b207575761476123496be60c7baae824b1818f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cb92828002a2e7bf6629157c109bb376b5818eaea46a097ec37a88d5a2c953e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetFilterCurrentDashboard")
    def reset_filter_current_dashboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCurrentDashboard", []))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetLinkedEntityGuids")
    def reset_linked_entity_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedEntityGuids", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetHeatmapNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetHeatmapNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboardInput")
    def filter_current_dashboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterCurrentDashboardInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuidsInput")
    def linked_entity_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linkedEntityGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmapNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmapNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9abd1b40d8a1f78d80eb6fdf923ba5203e87bcee56bd1a35179085f479abebf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboard")
    def filter_current_dashboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterCurrentDashboard"))

    @filter_current_dashboard.setter
    def filter_current_dashboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef559e2bb6d62fd16c601730fbd291e8f5c99d289f0892edca0d0f45f27c2e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterCurrentDashboard", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99adce21d444150c4fff8cf2b58731b7762fcd4eb944547f0881621bc76831d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3532fe23ad894dc35fd8bee4d3cfe470d7a56877b192a7c39d0e6002845620c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuids")
    def linked_entity_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "linkedEntityGuids"))

    @linked_entity_guids.setter
    def linked_entity_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cead5768d805a654e389dfe26c11ab254388cc9c981ea7f61e32262290a8b8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedEntityGuids", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32ac7657c875baa52fde7960de56b697b4b03df37f49da61b129b5d5b3e4f9b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6e22bb6432ccfb959a2da6bba3ca2a5659bcb1f2c67df180aeff59ec752627f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec792db211d5952157b01d8d02b1b7c458cbf5f43e1e0032ab41edf563bf6de4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetHeatmap, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetHeatmap, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetHeatmap, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f430c66f13f645b2dfa7fc39df2e05c8e8de8852ed511e6acce23761b52bef1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHistogram",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetHistogram:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetHistogramNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81b4aa18dfd455e9a25c069343ad099e643e61975ecc01a5a7679dc43460b07a)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHistogramNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetHistogramNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetHistogram(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetHistogramList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHistogramList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bdbc753eb485882022e483f950ed5ba3a004e02505bc09d3e24ddf7407a21e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetHistogramOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__134d64b2a4e3e32fb17f43e23f113f4e6490778b62e7bdc74c961712e73cbfbd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetHistogramOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551efabbf8b6c3e236c38bcf66f4df5d6892cf5433fadff5e5295c948bcf7885)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce31c80552a3e7a4946008044af99b99c58e449494f800349cd5fb51edf24e5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab1abeb843fe9809ef99f6f284fa54e4f2d0f1029dcc1ca070f624b41110ef65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogram]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogram]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogram]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35da2e69f7f8b923ace71d42847ca72cf2f6b4f49c50eb2a2261e60cbfb9e7c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHistogramNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetHistogramNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0960a9b185a5c7ab276087057011e25a6b3569b169865dc93219771e6db56e0a)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetHistogramNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetHistogramNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHistogramNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__477f5b48f4fbc6126151ce433af47e1d2b89e6c88fccc9b2e17a80cf9cdd0c24)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetHistogramNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abab7167b3b5672991d21c8d78b89291fce3d7735ef11e293c8193b244f56823)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetHistogramNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59e280929e547b88de7338a57e9a1dc466856aa357e103ccbf1d73e28d5a9a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4781ea0ba02c72c39a65eeccc6b8907b94845db2d58afa16d818a823b56e85d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0074345df9f11abc8d5c6eb57be30a4497518b450bfe87742be670a11803986b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogramNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogramNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogramNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7fc5e90430d1399f0cf7a3522d237b3f0502068bef3c3db2803fdd6ac1ffbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetHistogramNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHistogramNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__539b0a13f9d6f024250eb539a23601702c2200b4dade882c6a8a99d8f23cb91c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc0aaf10599f0bc10335914ebf8fa7b3e9c322e21fb4d8b1aaa212410c4ba438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c93e0d6b02564a053feebe4970e6c965ed2788019fed15f03716775cbe98031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6300feb44433e811c485b5f7eee5ddb0c090d4fdea770ceeea15df79479f1ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetHistogramOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetHistogramOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__edcd1ca27e962053e4bdfc4e45f2aa19c03849c71c50d7ec6c32d134884d8e17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856797a553b2ebb48d41568daf37e7311f3f2da4efd8f6b5d055f79b9481eee5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetHistogramNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetHistogramNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogramNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogramNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1ed59404e17bd667c659646b329bc0226921210927b6730def796b2649eff78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2937e081bdd8d5494995d827912515ffff9f16c81508d9d64beaed44721f7039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8cb99b41a4641f1d6bca29eebd410bc7f9bd7cfddc0f3c2cda72a17aa87c79c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f480d4324c25cd6634803148565a5cf47b5d5b07ed308d1e7cc33b6abbde04a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d83f1b001f7b9ba2cf3d4099c0c428df293d34f43ac3ed014ba779b168d8558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc11d3a37fa43ba0f0aef0156b49987969d239cdfb03e8da2c9ad29c0aed661a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetHistogram, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetHistogram, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetHistogram, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73d2d0888584fab272cc493928e6c0ef0e4cc6ed482adf0146f157b80e9c87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetJson",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetJson:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetJsonNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0c7da08740c8d81ea8e144152c334411c5fb54c9d1c704be0d8582e3db7f60)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetJsonNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetJsonNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetJson(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetJsonList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetJsonList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__282760c11198cf171a3fa1e162c3be860a192ed49a5871535666a7f9e97d211b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetJsonOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93b8f2a79f64a42fb0d9b4926a963cca9eee62fbc391f28b7d1ef2a231c52e45)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetJsonOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2203d0d6593bd758659857610be4edb5ffcf7e64089cfe7fd42cf12eef303be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0df47a0c164cd86551428b2a117ae279a716451ac02cd1598ef5f79b8b724a6a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ac1f4cec76829acf5043ad93e0a36cb87560b0d038f833ad3f9de620e2cf83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJson]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJson]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJson]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aea7327d7e76db90b1eb66aeea782daf5a6e4e03d5031076d1c439ef65400b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetJsonNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetJsonNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b644b5c3d27e0e7c4665fd93b743ac4856e0f6baf4cad80991b9a524dc07258)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetJsonNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetJsonNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetJsonNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__70707c438dabb738e093c72dfebba5e5c96f2d04e9450f360b5dace34a770dca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetJsonNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178f1370df3ae1c0b8e4195891306c92ba30664e62a3735c140afabca080420f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetJsonNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ac9c42920567ae5aab8e07ba921286fd99d492545969ffaca52c2b1d18235f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1409374d4ea3cd972ababe9e9ebca4eb06f6cea05dce4ef122323115a7d07d03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28c34cd4776caddaa86654a909cd633baa7614efe5fe0790afa9d0b8b480cf9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJsonNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJsonNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJsonNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3c8a408091e46575805940818632949c315ba1d6fdfd61b6f6fb05360c70b47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetJsonNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetJsonNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a236c367885381343585a09804589944a5fbbf0bddb8b3a71329dbb2c73551bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f5f1e863c9bae6199c15a523d48571828b6f85fa52aa98ea6c3d96743eb089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae172cc5f3c0eda58d199f29e77fba4534ab7b4724c055b14b1747d18b8a264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a401156f408835684fa95f04843a1373d41316a5841c73b90fcd07486887105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetJsonOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetJsonOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d76b2e18c406bd5291d3d9f9885f2077f67e0c04ad6caa6b271cfb0edc1a8f7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f49a3a167acd4007da90ddd15f6e8676ba5709eba0418eb45bf43cd896f550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetJsonNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetJsonNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJsonNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJsonNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e181007ab327b04f61c91ac379141b30e9c67d2b15d0e638b82bc2c71ff51a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6899733ce2ea2d870c11e3150c0f6a0b477de931492d1e92ab7b956e9949e6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39930dffa26f369afa3cd1691c85a1ef1543ca75f3748399f21268543f1ea8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de568b12bda7868542d6003266158171c218b3d630a1d44631ef770283eef3f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ffdffe59db666bc41d1a8520846de54a9249afa98f165087126d5ef0064925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e18ec56b5fa54bff76177bcbbcfae0d07878373cbc87d23d8ec80189fe88154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetJson, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetJson, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetJson, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65e103e464726157303b7864c547f91698271946ec34779080ebbd11def47af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLine",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetLine:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetLineNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18149664903820e719a1ae6d88101663f1385b175f6fe3fae3dec3bddd0115b3)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLineNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLineNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetLine(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetLineList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLineList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__459b2b8d8365a03ec643ed1618c7a8cebafd7e7ed11180156ddb45b2e6ddc463)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetLineOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df34111e345276c1f29227917c86afe0a0d03f1fc37c955f4a758569825dc068)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetLineOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001fdc0128fe3746c02994c4cba36985d02d10a86772fa9758ec4cdac15754f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a16433a8b8de224813eb0e752c65656ae1a443b5743f1cf255b6e99959e4550)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20a1365d17c95f03f452afaa47032c128255b1bf2cc86342d5e1948907f1ef38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLine]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLine]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLine]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7cc17e2c5816452eebf28e5d9b303944c9a6229b91171a23059c9c50b9e1b2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLineNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetLineNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e04d2773849871dc2fd8ae87adb5ff5bd10960506c1f80c01980b6f125a9aa)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetLineNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetLineNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLineNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65da24ed376189d012f38cdf2ff1caeb71d2402085fb6608ca4d0ab8243992fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetLineNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8f3b65ce9d112d1ef61c252ac8a63a03b201ae2999b554c6f9d1d06bc3c5ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetLineNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088d18ad27f0e50d27cbe55b23ee35ad65c5f38757d1d76f648940cc79e12757)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bf2c70ded1112dd7e1e6b5121450104b752985743b2421e099a549ea0154398)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07e25ac40a8344f5c6c471584d6ba53d810d2aba73978233ec88d27f5049833b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLineNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLineNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLineNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b53c5f2aa89dfef3fe92412a28ec9cefcd2b67d25560522f18c95863002b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetLineNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLineNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__629d2eb3fcc088d4ea88a049811b19a56ddb3c870fc54ca98c0e237097831f20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dacd1d1f0c3458b9d9504ed5684080a3500b056904feac7abcefdcc61bd3840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16579d62ab3b349bb4c1ad35325bc68dd6224d568c9c58fad94df2d734df27c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetLineNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetLineNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetLineNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27a87d4f99ee7913e63b2a560fe73be28b480b64eb5072dd7684569c2e3efc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetLineOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLineOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c49be1160e85958c7a2a0f6635f47964cfaeb078de9066ff02bd9f059165787)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLineNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaf278546e6e79a818a4e82a55a7f3597c58a21e1f50102fd1a8f913a8c2d365)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetLineNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetLineNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLineNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLineNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ab97ee40e807f6e93c068077ecf1a0eb04316591a6751cecc5b22c0898862c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e5e8713630e8d855bb9f4c21327deb439efab4e64a7b0a8e65fd3ec1900d39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aebe376b7b245072b3423e251c29d1e3eaa6c880da37ec42947f28b3d1abfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091d501e7bd3e4067e8260b28f701572d17ace2d4d6ada367821469c9f77a335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce6c35b1dc673bcbf1f36d593239bd9dbd11a73127c820c1bb21a388f10cf5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cd7e243d4dd0ad9374e6173fc592ae3b9d2049a891160fe1831f6313a2926a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetLine, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetLine, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetLine, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f111ca0289d6f0d2aa217b09e7f698c65d7b1e8045b55dd74ac4409b28c0338)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLogTable",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetLogTable:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetLogTableNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256f0694cbefd9641e4281d2d5f9565b29cd1b64dd7a51e3b5c1fba334c804bb)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLogTableNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetLogTableNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetLogTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetLogTableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLogTableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb08aae410359b8514f479a7d5180d126a5eba01c6d3d0627c84431f291bc51d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetLogTableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69584cd969523c647b8d5f3b24198a5b88dc85cff40dd0a9db285d4b0577fa3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetLogTableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ac392e9d1b7fd186ef96e14481536686fcab0f6c996b041c6d1b00cbddf8ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1823c49b1f341a237515e35ff39b461da1077ff84d04ccc34d2c33d9b297f947)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee806efccdc8fa45cfe887643a888c30cc71a0624741e9cc4f354fb70ea4d835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71dbf2a4c3f8246ea08bf1b1e30a3f88582a3db189a42d2e8897dfa324c0bb29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLogTableNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetLogTableNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0faeb7a4013b88c959a6bd72f125b3b0b4610529ba148f3aa09e3c66d1151d6c)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetLogTableNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetLogTableNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLogTableNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0818cdd4cdcbf5130bdcc236665adce429997fe1aa717241b4f54254bade8f71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetLogTableNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__207f02806589225a9a681e9b9f1a5ab4cbf984336974082feda26feecf4baded)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetLogTableNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce9fac8908b8071f10d6bd85667b76816f38dc88db04f6247200a22976c2b937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53c1b7fdc09c94d22e4c92aff0dad6d289cd596f16d1796a38a9a157542621da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3eca7fdc70000c45639886dcf28c6675acab2671d6fbacd2485d44e0648bbe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTableNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTableNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTableNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ba9ecad74ed48a93904e7f0dfbd162b497c9593e4e1d904cf1385462fae29a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetLogTableNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLogTableNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df2284c8cc0d29a655f31446748a8c654de4d908db461cb8f7e4d0a1efa997e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77703fbf7f6a2ed15b75bec2842dbe6207d06ccb57767882ef983221b852cd76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c1e59a4b47573c58beea681c7ca7d3c4398303538f881086d8b563edc7ed546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e74ddadf831e7fd049a10a25cde67950862fff34250ce10c02256f0c770de12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetLogTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetLogTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efff0c7a20e4209a519725b3ae5a1cb813a4e8b7aa4db605037cd2877fcfb07c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e19d40157f76867faf82951de958915e4209166cfa1b1f60572b095b70e66da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetLogTableNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetLogTableNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTableNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTableNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26562561c45104585436cde1af74bba464c09985f5937495a119ba5bfc67fdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715a25e5536e5eddc7a4b3f692b2f3b5242b95fbd508a5ebf5214e32535fe8e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f72efeac648d382e60fad088772e6017658da361bb30c02a24191d06ca6ee9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89429449cb75f8abd67d09f246e03a4f94a31b2a718950a79cba72cef1f57595)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4907e6f3f2e59069cfa2bfceff587895fa4324742e169f027417e60134f3d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95effaf8a5d7b7ad8dc2913f66eaefb703ad9dfc53d340dfd8b5510634bc5cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetLogTable, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetLogTable, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetLogTable, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7df64694de42fb61839df74840252ef8de380ffea6a4c4f3573c7b67d6de2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetMarkdown",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "text": "text",
        "width": "width",
    },
)
class OneDashboardPageWidgetMarkdown:
    def __init__(
        self,
        *,
        column: jsii.Number,
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        text: typing.Optional[builtins.str] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param text: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#text OneDashboard#text}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4a6904314303931a0a073bebfa73c39a938a81fdf7a73bf9ecff8a81b093d9)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if text is not None:
            self._values["text"] = text
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#text OneDashboard#text}.'''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetMarkdown(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetMarkdownList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetMarkdownList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d346dd67500886aa34481e3d852fe559fb963881db385fe9327907d1aecad28)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetMarkdownOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7d75b5f02def0af49f5d03221204464fc6f40a06d49618ee55a0a0aa1315453)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetMarkdownOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41964e1b3c7c5d1ee1693ae44ee0f29f3f61d66df7e2f6429ab5ed4654046df7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7b99e6f3d5e37ce6e02fef76e5a9ae595c68a55f777b417a5396f9cf40144bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ba67d602ca85599a539964c11dbdfb3718f4f36c3eca6f2871a01b618de1281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetMarkdown]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetMarkdown]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetMarkdown]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2baf727b42457805b55d0a52eecc9375719f559a19e4f0f857e601bf9bc15b1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetMarkdownOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetMarkdownOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c5e86ca878b67dad2be8f47b6186fb2fc8f3b93efc81b98541141938c0587f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__072448ee639069c76c7d488a1900abeddf3f4b1a94ad24de6423fdfb460b7efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117f5873e79e46c76c3f879dbdbc170466bfee0a600abf0357cc29af00a30943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a2ec317c7136fa28f7b085b5cc4253893d3099f2d3cd893cc180c651834ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__646fff00e74ac395f992a218332fbe4de3603ee7e2f377bbb4db7bf19c2cc7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b8aab6481189e9f6955ff36c76b8e202e9b6e9810a7616526d91b89424486a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce74b7ca7d5458495d6b6283a7943b3fceaab6b63d363e95af4694d78a334178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2556b7b671ddf2f493ffd04e42a21bfb87f81e981530661aa7aae2cc2bf8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetMarkdown, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetMarkdown, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetMarkdown, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ab3642467e08c1bf8b1eb5f075723e6a9143b4526b3b1939db9180276f8e9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetPie",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "filter_current_dashboard": "filterCurrentDashboard",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "linked_entity_guids": "linkedEntityGuids",
        "width": "width",
    },
)
class OneDashboardPageWidgetPie:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetPieNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param filter_current_dashboard: Use this item to filter the current dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param linked_entity_guids: Related entities. Currently only supports Dashboard entities, but may allow other cases in the future. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f4be3ef8b3adbedc30cf23f721a27f7ed100d6d9247520aecdaa0e9f8caad28)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument filter_current_dashboard", value=filter_current_dashboard, expected_type=type_hints["filter_current_dashboard"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument linked_entity_guids", value=linked_entity_guids, expected_type=type_hints["linked_entity_guids"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if filter_current_dashboard is not None:
            self._values["filter_current_dashboard"] = filter_current_dashboard
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if linked_entity_guids is not None:
            self._values["linked_entity_guids"] = linked_entity_guids
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetPieNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetPieNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_current_dashboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use this item to filter the current dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        '''
        result = self._values.get("filter_current_dashboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def linked_entity_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Related entities. Currently only supports Dashboard entities, but may allow other cases in the future.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        '''
        result = self._values.get("linked_entity_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetPie(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetPieList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetPieList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de4a24de83f3846c19fb67474ce2487f1bed35effdd7ca69e41a23734035725d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetPieOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a52e594e087a3c717344d2795417b3d166574731b8a312dd3842cd6048e4aa4a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetPieOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb749eb27d19032f19691f5de2aceae230c82e33eb6504f00ef622dccbabeb66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9eb0708237add8c980507cdb6169b42ac4c81cd964fb8395c0cf3b3f26fd0e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a17c963640dd5ccc10187741cf1712c2207a98ece8368c133612c14f31e791b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPie]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPie]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPie]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__226a3b713666576c12cb54f7435776aa7e033c0b3c0f74de36fb0a7aa5b5e056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetPieNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetPieNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf8bc34fee0d55fbee5733825bd4b8bdb1e4a6ea87c37c6f111f4aa2d2e30ce)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetPieNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetPieNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetPieNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1534743808bdec658a93bf6f529841ed4e36565db9df52b57c16944073409b05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetPieNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc37352d2111de4790124bcd476ce8e850090dc1cb59bb8ce54a1b6bf5d670c4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetPieNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee8df9a7bb19ffdcd70d169deafe9ad248ea0b61e0e6be2db02be3627bb69774)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffd6b85d1e7c7f6448cc12f955d00646107720b0ab351308e256d942286a48c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d66ba4de97c8dae1fb4f46f317d38f704015ab1d7ac73d053af6d626570dd81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPieNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPieNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPieNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b2339f3d1b3e943630891240068e92a5b991c7eee9a7bc833ddc222fc3c147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetPieNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetPieNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a43108d0e12501cc7fe372217c21216f6bbdeff848a0a7239358bf6c6f4df05b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08aeacd19cec5cf343f97ba2f39da767c21a2e0ec922fc58634672e99f9ed9b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__671ba42472b9942c48d6c19ad593d6956eaf5ebeea85fe995020d82c18ceac21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetPieNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetPieNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetPieNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc2be342c5a20894995b3403e763178ed9ba926ab059a7739d13dd77a1a27da2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetPieOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetPieOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a48569d9875f66ec42ac0c0cb25de11c1d40ea72eb9f4e95cfa0ab49d990fc0d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetPieNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a107b7c9b50595e01744bd22abd61016b03f273135503bbb24453b2925dc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetFilterCurrentDashboard")
    def reset_filter_current_dashboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCurrentDashboard", []))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetLinkedEntityGuids")
    def reset_linked_entity_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedEntityGuids", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetPieNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetPieNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboardInput")
    def filter_current_dashboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterCurrentDashboardInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuidsInput")
    def linked_entity_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linkedEntityGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPieNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPieNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6c5460f0bf46103ff40c84fe9daa81aac23aca47bae53fd8ca2c73a09499b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboard")
    def filter_current_dashboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterCurrentDashboard"))

    @filter_current_dashboard.setter
    def filter_current_dashboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d8e3d6ddf5a358ea55894d780f2de2e6e1ccdc44698e4813ce2739a1f106c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterCurrentDashboard", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18820545cac6ec1141c970ec804d77b7b9701669cc38796ce5d376cada0a683a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__272cc8dfeae4ac1d059d220761d7d21d214726563f7cbd427db17c060e60ef08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuids")
    def linked_entity_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "linkedEntityGuids"))

    @linked_entity_guids.setter
    def linked_entity_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c37e65978ffcb6e8159267d463f46fe71783b999fce441243af6b85e04a27a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedEntityGuids", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ea80004105fac316a41a96e3f1d4fd157caca9d5b64646436182b047b6ad31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6fbd364f5a105fa66cb9d35054b2ab83f70668e0cd379c713f8f428e526a9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458bcdb43dd96ed6febc406e01ad103d00ccf8e2848842da23fdcf3bcc7d2e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetPie, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetPie, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetPie, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa101081971caa0bba52f44f14da9f7f0a0442c39d1f248075e90c01fc8cfce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetStackedBar",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "width": "width",
    },
)
class OneDashboardPageWidgetStackedBar:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetStackedBarNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6752f1dfb839e17794c3fc1984b2624fde4a1900abab3147046c9d149644df0)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetStackedBarNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetStackedBarNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetStackedBar(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetStackedBarList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetStackedBarList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7739749390fcf60819ca29cc89d7bff111cdf9337b53b4baedf7b807ec0dfdba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetStackedBarOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b8da7f7773242a083fe2c3b2a8ac2c1b548cb7ff3732d4e0090ae1fa781d2a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetStackedBarOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb678cbacd34a0b7f7fe1a9985dab6591b73bcd0395fc392145112a02166f090)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1df99e306c62e63dff9a99f2e342c93a560d7ea804dc6e564a1849c349387e58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c870652350c0f8e7d52225b89e44aeb759132cf47e2a309bd218f114428c659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBar]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBar]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBar]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb0ac332891ac39c43f8b85eb6ce9d1833d05adc4a1c63373782b595e04f53e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetStackedBarNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetStackedBarNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675cef10884a25b5ee1a32a128aa3e81dbe8480ff251118aee9e1a53fc5e58e3)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetStackedBarNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetStackedBarNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetStackedBarNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdb13b206502a46776dfd622a3a43ff090a0c05a2260889c977bf3c49418d078)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetStackedBarNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__885616935c40a2feb6fe1152ae3ff238d163c41d97e5e6f2cd05ca305ffd96d1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetStackedBarNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c3c0830921379bb1f256c9d747acbcbb6cd5812c15836e961bd20490294228a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c36f1e8442ed392077525d4e26d3622df3eed7aa1f4d4965cb6a0b736154a7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0aa9acfcdd431338fdc15a61e47121bed77875258d76fde9bc2efda07a94ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBarNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBarNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBarNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba97d3e9f11e6d564cd211dc98c08d55bda758317630adad98e616021f674549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetStackedBarNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetStackedBarNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b1e17a98fc14e079d689b6cd35a7b75ad2a6ea8b31fb536eb7824c4e6565505)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__540db736bddcbd751f778c395122162cd7f0bffdcde421dbbc5acf108246b0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38366a4b73545e631e960d3dcd937673a9c38dec5bea6b071d66f7aa7d6f9676)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a1976160c58b5bafc8a490af099131212199a9b35cbfa3c2e359edc15314bb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetStackedBarOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetStackedBarOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c90e1ed22d4114b53f5d992e667df316c2beb353bae8a3bb4bdcf7a7edd6ba0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4009e92e55ac01950ec924ffabedaabb7ae0de855e2efe2ee18926aea1dd46bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetStackedBarNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetStackedBarNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBarNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBarNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880a8bdf61bd79ab2a03d5fc19525b0c9024a584d4e74ad5553a56c7a6591a67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d85eb623e84b76a9fe9bc3d7d4cc9e3781778c79d57d682ab9c215c4572e9c68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9c539237347fcc20c85b90e3b69e2e80eb3133349bb938589d92fe16735072)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f588099d5a482f85b77a737c70fe98b0809e9dc294fed5c3481d813f73e3ea81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56fbe5d8eefcb3425822fe6f7a739e06ac6042f18b05188ba62f7c1b1f8fdd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0643ef223608f9bf5b09fe2ac8502237fd871fc2fd3c24e4de9b464ffa76174b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetStackedBar, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetStackedBar, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetStackedBar, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ea84a438a7a29412df38aaead8d0f114188e3516a0eae46ec97657f2049a50b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetTable",
    jsii_struct_bases=[],
    name_mapping={
        "column": "column",
        "nrql_query": "nrqlQuery",
        "row": "row",
        "title": "title",
        "filter_current_dashboard": "filterCurrentDashboard",
        "height": "height",
        "ignore_time_range": "ignoreTimeRange",
        "linked_entity_guids": "linkedEntityGuids",
        "width": "width",
    },
)
class OneDashboardPageWidgetTable:
    def __init__(
        self,
        *,
        column: jsii.Number,
        nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardPageWidgetTableNrqlQuery", typing.Dict[builtins.str, typing.Any]]]],
        row: jsii.Number,
        title: builtins.str,
        filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        height: typing.Optional[jsii.Number] = None,
        ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
        width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param column: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        :param row: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.
        :param title: A title for the widget. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param filter_current_dashboard: Use this item to filter the current dashboard. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        :param height: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.
        :param ignore_time_range: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.
        :param linked_entity_guids: Related entities. Currently only supports Dashboard entities, but may allow other cases in the future. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        :param width: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0d83e80b6e042ca608dd188e4fb7a8c39b32a4189c287f49977da72e5dee31)
            check_type(argname="argument column", value=column, expected_type=type_hints["column"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
            check_type(argname="argument row", value=row, expected_type=type_hints["row"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument filter_current_dashboard", value=filter_current_dashboard, expected_type=type_hints["filter_current_dashboard"])
            check_type(argname="argument height", value=height, expected_type=type_hints["height"])
            check_type(argname="argument ignore_time_range", value=ignore_time_range, expected_type=type_hints["ignore_time_range"])
            check_type(argname="argument linked_entity_guids", value=linked_entity_guids, expected_type=type_hints["linked_entity_guids"])
            check_type(argname="argument width", value=width, expected_type=type_hints["width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "column": column,
            "nrql_query": nrql_query,
            "row": row,
            "title": title,
        }
        if filter_current_dashboard is not None:
            self._values["filter_current_dashboard"] = filter_current_dashboard
        if height is not None:
            self._values["height"] = height
        if ignore_time_range is not None:
            self._values["ignore_time_range"] = ignore_time_range
        if linked_entity_guids is not None:
            self._values["linked_entity_guids"] = linked_entity_guids
        if width is not None:
            self._values["width"] = width

    @builtins.property
    def column(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#column OneDashboard#column}.'''
        result = self._values.get("column")
        assert result is not None, "Required property 'column' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def nrql_query(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetTableNrqlQuery"]]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        assert result is not None, "Required property 'nrql_query' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardPageWidgetTableNrqlQuery"]], result)

    @builtins.property
    def row(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#row OneDashboard#row}.'''
        result = self._values.get("row")
        assert result is not None, "Required property 'row' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''A title for the widget.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter_current_dashboard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use this item to filter the current dashboard.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#filter_current_dashboard OneDashboard#filter_current_dashboard}
        '''
        result = self._values.get("filter_current_dashboard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def height(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#height OneDashboard#height}.'''
        result = self._values.get("height")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_time_range(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#ignore_time_range OneDashboard#ignore_time_range}.'''
        result = self._values.get("ignore_time_range")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def linked_entity_guids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Related entities. Currently only supports Dashboard entities, but may allow other cases in the future.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#linked_entity_guids OneDashboard#linked_entity_guids}
        '''
        result = self._values.get("linked_entity_guids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def width(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#width OneDashboard#width}.'''
        result = self._values.get("width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetTable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetTableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetTableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02574d4454dbaef619ecfecb4ccf6190bd9302607082f68353a2e41bb57e366f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardPageWidgetTableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce39f3fe98f3d4e9814def0c1a33984b40f831c11055b7578467140fb9d5c31a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetTableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a158f1356d6465699fa770b7014f12691b594286d63e4a06295940f5aa06bc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad302fa991f646530ac262d2330db29b15c3464efae91000979c9372d71d541c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac332ea9a3809fa2ab65fc9f3f1f2a7477140e1159caac4b76d5bf7f067a57e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55da68ca642ff07e9327bf7be2d97152d8a5aa32cea5b84945fc44aea5d91ea5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetTableNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_id": "accountId"},
)
class OneDashboardPageWidgetTableNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param query: The NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_id: The account id used for the NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9afa7c932bbf9161a7a7a0e2324d970afc058eddff7934ce23c3971040f81593)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def query(self) -> builtins.str:
        '''The NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id used for the NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_id OneDashboard#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardPageWidgetTableNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardPageWidgetTableNrqlQueryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetTableNrqlQueryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__498799cd268a3b287b5cf96fe92b288a513b4a2da6b76aac866192f1ec6517c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "OneDashboardPageWidgetTableNrqlQueryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__446a425303b99fc048a966d559f01c5d5bb538155290b287d0ff87cff5158ef4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardPageWidgetTableNrqlQueryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc480be70acfa273d06bf85dbce7328fb71f79b87ab239e599b08785862a8ef1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3501f231bd1c85e4fc96058972d7593e20244c75c5c5d288af6f88a3aa5ff151)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d783a2d6791b5ea0cd959bd588c45911ac0b87c54f1fcd11888747a020bd771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTableNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTableNrqlQuery]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTableNrqlQuery]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c6d34508347644857189fc9c70932610e371beda89eafabfb720e62d8b1e07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetTableNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetTableNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5361b89f85af50d4a30569d0a9bf6d8255406ef0825a898e8b158facbd283d78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480680d2416b0d2a68a30d032f95c57c1ec3c57fdadffe157ff7cdc2936b3f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e1e3b5c93ecb2f88b2eb94740523206a45d19dca8b8ee198ca4e874d912415)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetTableNrqlQuery, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetTableNrqlQuery, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetTableNrqlQuery, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e8bb4b2decc4557fc3d87c83bb7995b2c0a264c015e28f217abca8012c186b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardPageWidgetTableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardPageWidgetTableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__882201a67bdccd4708c68e0c382af63841d7d8aa66ca37245b529751f1872f7e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetTableNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__408ad95c1b786a83ef249c142aa1746255ec248b8261a9e6cbd1bb2c62d41a6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetFilterCurrentDashboard")
    def reset_filter_current_dashboard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilterCurrentDashboard", []))

    @jsii.member(jsii_name="resetHeight")
    def reset_height(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeight", []))

    @jsii.member(jsii_name="resetIgnoreTimeRange")
    def reset_ignore_time_range(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreTimeRange", []))

    @jsii.member(jsii_name="resetLinkedEntityGuids")
    def reset_linked_entity_guids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLinkedEntityGuids", []))

    @jsii.member(jsii_name="resetWidth")
    def reset_width(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWidth", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardPageWidgetTableNrqlQueryList:
        return typing.cast(OneDashboardPageWidgetTableNrqlQueryList, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="columnInput")
    def column_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "columnInput"))

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboardInput")
    def filter_current_dashboard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "filterCurrentDashboardInput"))

    @builtins.property
    @jsii.member(jsii_name="heightInput")
    def height_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "heightInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRangeInput")
    def ignore_time_range_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuidsInput")
    def linked_entity_guids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "linkedEntityGuidsInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTableNrqlQuery]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTableNrqlQuery]]], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="rowInput")
    def row_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rowInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="widthInput")
    def width_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "widthInput"))

    @builtins.property
    @jsii.member(jsii_name="column")
    def column(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "column"))

    @column.setter
    def column(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46ee3c5609ccacc176610decc594b865b63ddee7ea708c32e3747cd8d746a66f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "column", value)

    @builtins.property
    @jsii.member(jsii_name="filterCurrentDashboard")
    def filter_current_dashboard(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "filterCurrentDashboard"))

    @filter_current_dashboard.setter
    def filter_current_dashboard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb3bc95990a9d17509b391017a7ca36cfc579da08a7bb481aa7141349bf24a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filterCurrentDashboard", value)

    @builtins.property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "height"))

    @height.setter
    def height(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75683962dd9a30edf39ba94860edce0aea4eae429d6d67864270dcd4742c8fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "height", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreTimeRange")
    def ignore_time_range(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreTimeRange"))

    @ignore_time_range.setter
    def ignore_time_range(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6a2586e27f9052b869620594b521df447e8f9a5837acbb16fe5eed20c6b46c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreTimeRange", value)

    @builtins.property
    @jsii.member(jsii_name="linkedEntityGuids")
    def linked_entity_guids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "linkedEntityGuids"))

    @linked_entity_guids.setter
    def linked_entity_guids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d391b7aaeacef1003dca7ec6cb36ebb2e5a445964e27166a65cc99c76ef70535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "linkedEntityGuids", value)

    @builtins.property
    @jsii.member(jsii_name="row")
    def row(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "row"))

    @row.setter
    def row(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541d9e8714d1027ed6bf61b1412046f02794fc5e200cb78c61da461ac130c5ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "row", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94248ff54c05f1f33a9f95d5ff07baa7172d646cdc28ecd1a9cbc4e725937069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "width"))

    @width.setter
    def width(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e7e37886fc7740d0f33d8389324d0ba9c5136f02d081f75b5ce66da77445ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "width", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardPageWidgetTable, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardPageWidgetTable, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardPageWidgetTable, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c4396cc0e7870c78943737b577eceab76f65cf0cb8a5afd74b2ce57f12d1dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariable",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "replacement_strategy": "replacementStrategy",
        "title": "title",
        "type": "type",
        "default_values": "defaultValues",
        "is_multi_selection": "isMultiSelection",
        "item": "item",
        "nrql_query": "nrqlQuery",
    },
)
class OneDashboardVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        replacement_strategy: builtins.str,
        title: builtins.str,
        type: builtins.str,
        default_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_multi_selection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["OneDashboardVariableItem", typing.Dict[builtins.str, typing.Any]]]]] = None,
        nrql_query: typing.Optional[typing.Union["OneDashboardVariableNrqlQuery", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: The variable identifier. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        :param replacement_strategy: Indicates the strategy to apply when replacing a variable in a NRQL query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#replacement_strategy OneDashboard#replacement_strategy}
        :param title: Human-friendly display string for this variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        :param type: Specifies the data type of the variable and where its possible values may come from. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#type OneDashboard#type}
        :param default_values: Default values for this variable. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#default_values OneDashboard#default_values}
        :param is_multi_selection: Indicates whether this variable supports multiple selection or not. Only applies to variables of type NRQL or ENUM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#is_multi_selection OneDashboard#is_multi_selection}
        :param item: item block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#item OneDashboard#item}
        :param nrql_query: nrql_query block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        if isinstance(nrql_query, dict):
            nrql_query = OneDashboardVariableNrqlQuery(**nrql_query)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1968b96825bdfd0e91e71911576bc8adf3dc036af0a58921ac6ad9fe53a79a25)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replacement_strategy", value=replacement_strategy, expected_type=type_hints["replacement_strategy"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument default_values", value=default_values, expected_type=type_hints["default_values"])
            check_type(argname="argument is_multi_selection", value=is_multi_selection, expected_type=type_hints["is_multi_selection"])
            check_type(argname="argument item", value=item, expected_type=type_hints["item"])
            check_type(argname="argument nrql_query", value=nrql_query, expected_type=type_hints["nrql_query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "replacement_strategy": replacement_strategy,
            "title": title,
            "type": type,
        }
        if default_values is not None:
            self._values["default_values"] = default_values
        if is_multi_selection is not None:
            self._values["is_multi_selection"] = is_multi_selection
        if item is not None:
            self._values["item"] = item
        if nrql_query is not None:
            self._values["nrql_query"] = nrql_query

    @builtins.property
    def name(self) -> builtins.str:
        '''The variable identifier.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#name OneDashboard#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replacement_strategy(self) -> builtins.str:
        '''Indicates the strategy to apply when replacing a variable in a NRQL query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#replacement_strategy OneDashboard#replacement_strategy}
        '''
        result = self._values.get("replacement_strategy")
        assert result is not None, "Required property 'replacement_strategy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> builtins.str:
        '''Human-friendly display string for this variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Specifies the data type of the variable and where its possible values may come from.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#type OneDashboard#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Default values for this variable.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#default_values OneDashboard#default_values}
        '''
        result = self._values.get("default_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_multi_selection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether this variable supports multiple selection or not. Only applies to variables of type NRQL or ENUM.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#is_multi_selection OneDashboard#is_multi_selection}
        '''
        result = self._values.get("is_multi_selection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def item(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardVariableItem"]]]:
        '''item block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#item OneDashboard#item}
        '''
        result = self._values.get("item")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["OneDashboardVariableItem"]]], result)

    @builtins.property
    def nrql_query(self) -> typing.Optional["OneDashboardVariableNrqlQuery"]:
        '''nrql_query block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#nrql_query OneDashboard#nrql_query}
        '''
        result = self._values.get("nrql_query")
        return typing.cast(typing.Optional["OneDashboardVariableNrqlQuery"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableItem",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "title": "title"},
)
class OneDashboardVariableItem:
    def __init__(
        self,
        *,
        value: builtins.str,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: A possible variable value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#value OneDashboard#value}
        :param title: A human-friendly display string for this value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c64b88ec3f8bfa78bcee98491b15db8a1a80015a7e55cb0a68a4a9eef671a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def value(self) -> builtins.str:
        '''A possible variable value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#value OneDashboard#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''A human-friendly display string for this value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#title OneDashboard#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardVariableItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardVariableItemList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableItemList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab42c55be078e08fb4c34e3d675767321909300a2d1c70aefaa9c8d339423d6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardVariableItemOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b875f342d0210dd335f9dbf8d8820362a974135eb518010ba23ad22a08b34e14)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardVariableItemOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45434c39664813a8d67f3ebb82aa3ea99f4fdfdbb96f38e3af00f69a7187a13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68b408951e1e79fe27b34038bbb8a8a1321e8c8fd57c87ab4ff8b2898cbb179c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36508e84671a342c97e43c005bd878c4e17fa6a2e78bac06d2e167d68836281c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariableItem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariableItem]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariableItem]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2ce05d1c3c933016335982b1770e0c03e50c90d9b56c86a27b39cec1009dd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardVariableItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27dda56b51e4801d9ca5eca2b5200572fbe199b23bbea6b64ac712d6766cdd79)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__329ef69b70c9b015549d46f7754657600af83678d54a6b795630c7b8159874c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b598cd1f307c0bab7d3c12fc3d3f7ceb4746b64f7826907c4a7254f095859bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardVariableItem, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardVariableItem, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardVariableItem, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba839e5d23d59f3cedb13e3e5d9c450787f78ef26fd677bdccc0eabafbe0aa1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__374ae33ec3310b10a28d36163cf8cacfabfe5a42ab220b55b5ee9e39c279fec4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "OneDashboardVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__013399c814170b817f6e3cb135b1a8330b36d55a632b9100778c357baa6200ef)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("OneDashboardVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc49b0efa512ecd69af3a3e5fa33152c85c9448eef2df5d78401181564a30ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01f66025c6f4e1f38927490d03ce9811a6709ae7490ae208a84ca88c625e07d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f66aec6eccb9cdbac36f05f299876fc211bcfd283c2822f7533a11327e39faf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faee5bc8fa6762e3b08e1a2a12608fb013b3909cc1269620ef8e2eb52350f6ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableNrqlQuery",
    jsii_struct_bases=[],
    name_mapping={"query": "query", "account_ids": "accountIds"},
)
class OneDashboardVariableNrqlQuery:
    def __init__(
        self,
        *,
        query: builtins.str,
        account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param query: NRQL formatted query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_ids: New Relic account ID(s) to issue the query against. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_ids OneDashboard#account_ids}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d285e813593e095ff97a0067e82b0c88047e9ae8043d748fe8eaf2d53eeadbe5)
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
            check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "query": query,
        }
        if account_ids is not None:
            self._values["account_ids"] = account_ids

    @builtins.property
    def query(self) -> builtins.str:
        '''NRQL formatted query.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        '''
        result = self._values.get("query")
        assert result is not None, "Required property 'query' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_ids(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''New Relic account ID(s) to issue the query against.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_ids OneDashboard#account_ids}
        '''
        result = self._values.get("account_ids")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OneDashboardVariableNrqlQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OneDashboardVariableNrqlQueryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableNrqlQueryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d35b6d27305e5e882d833dd0481916828d26f8b8ea3e712c4746b8b80cdf31d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAccountIds")
    def reset_account_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountIds", []))

    @builtins.property
    @jsii.member(jsii_name="accountIdsInput")
    def account_ids_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "accountIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="queryInput")
    def query_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryInput"))

    @builtins.property
    @jsii.member(jsii_name="accountIds")
    def account_ids(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "accountIds"))

    @account_ids.setter
    def account_ids(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398a8abfaf045ade6ce38310b6dfec4ef8b712ca9ae7273a701d773504ae6d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountIds", value)

    @builtins.property
    @jsii.member(jsii_name="query")
    def query(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "query"))

    @query.setter
    def query(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10fc75e5b3cef8dd3556bbb8c1c34646e467c069627b91cd4d8e258102f337f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "query", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[OneDashboardVariableNrqlQuery]:
        return typing.cast(typing.Optional[OneDashboardVariableNrqlQuery], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OneDashboardVariableNrqlQuery],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7ad18d8caca4f2e686554b44699ff32666abc34757d97704163b5ed2bba2069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class OneDashboardVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.oneDashboard.OneDashboardVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__647bb1d5fd9964d9a1d7f0a59f1f53dc23974b94888dc2bfd1286fc3eb3fa03e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putItem")
    def put_item(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardVariableItem, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__199c8ae56b09fe7ce101fa3fa08d98cf82e7734660cef96e35e848215912c934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItem", [value]))

    @jsii.member(jsii_name="putNrqlQuery")
    def put_nrql_query(
        self,
        *,
        query: builtins.str,
        account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param query: NRQL formatted query. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#query OneDashboard#query}
        :param account_ids: New Relic account ID(s) to issue the query against. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/one_dashboard#account_ids OneDashboard#account_ids}
        '''
        value = OneDashboardVariableNrqlQuery(query=query, account_ids=account_ids)

        return typing.cast(None, jsii.invoke(self, "putNrqlQuery", [value]))

    @jsii.member(jsii_name="resetDefaultValues")
    def reset_default_values(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultValues", []))

    @jsii.member(jsii_name="resetIsMultiSelection")
    def reset_is_multi_selection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsMultiSelection", []))

    @jsii.member(jsii_name="resetItem")
    def reset_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItem", []))

    @jsii.member(jsii_name="resetNrqlQuery")
    def reset_nrql_query(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNrqlQuery", []))

    @builtins.property
    @jsii.member(jsii_name="item")
    def item(self) -> OneDashboardVariableItemList:
        return typing.cast(OneDashboardVariableItemList, jsii.get(self, "item"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQuery")
    def nrql_query(self) -> OneDashboardVariableNrqlQueryOutputReference:
        return typing.cast(OneDashboardVariableNrqlQueryOutputReference, jsii.get(self, "nrqlQuery"))

    @builtins.property
    @jsii.member(jsii_name="defaultValuesInput")
    def default_values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultValuesInput"))

    @builtins.property
    @jsii.member(jsii_name="isMultiSelectionInput")
    def is_multi_selection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isMultiSelectionInput"))

    @builtins.property
    @jsii.member(jsii_name="itemInput")
    def item_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariableItem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariableItem]]], jsii.get(self, "itemInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nrqlQueryInput")
    def nrql_query_input(self) -> typing.Optional[OneDashboardVariableNrqlQuery]:
        return typing.cast(typing.Optional[OneDashboardVariableNrqlQuery], jsii.get(self, "nrqlQueryInput"))

    @builtins.property
    @jsii.member(jsii_name="replacementStrategyInput")
    def replacement_strategy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "replacementStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultValues")
    def default_values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultValues"))

    @default_values.setter
    def default_values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b932f814eb527d3f2922af4348cc2ed4534970133c8d1b26dddb6c27ef52d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultValues", value)

    @builtins.property
    @jsii.member(jsii_name="isMultiSelection")
    def is_multi_selection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isMultiSelection"))

    @is_multi_selection.setter
    def is_multi_selection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__991298da4497e9559b48676bd1fa45d3b7730c813f91c7e0d79c77170905af6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isMultiSelection", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dda6e2a2e3e8301136d3cd29775e28536c1bd178be57bd5288f8f1870e86be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="replacementStrategy")
    def replacement_strategy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "replacementStrategy"))

    @replacement_strategy.setter
    def replacement_strategy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe432e783cebe6ab52f4fd93ca6059e33dcc44373422c007a6baaea39ff129f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replacementStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e91f797f13666d025deb8da8a75c1008e7aef914f91f580ffbb67dc55b65438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ac6cac34171e2c55ced2735f57678cfec0bc166c3e0103d8b89d2aa395c78f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OneDashboardVariable, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OneDashboardVariable, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OneDashboardVariable, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d450835486c68dfac33e70d4f958f40f46494ed5bc5beba7c3dcdf9db6aeaf40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OneDashboard",
    "OneDashboardConfig",
    "OneDashboardPage",
    "OneDashboardPageList",
    "OneDashboardPageOutputReference",
    "OneDashboardPageWidgetArea",
    "OneDashboardPageWidgetAreaList",
    "OneDashboardPageWidgetAreaNrqlQuery",
    "OneDashboardPageWidgetAreaNrqlQueryList",
    "OneDashboardPageWidgetAreaNrqlQueryOutputReference",
    "OneDashboardPageWidgetAreaOutputReference",
    "OneDashboardPageWidgetBar",
    "OneDashboardPageWidgetBarList",
    "OneDashboardPageWidgetBarNrqlQuery",
    "OneDashboardPageWidgetBarNrqlQueryList",
    "OneDashboardPageWidgetBarNrqlQueryOutputReference",
    "OneDashboardPageWidgetBarOutputReference",
    "OneDashboardPageWidgetBillboard",
    "OneDashboardPageWidgetBillboardList",
    "OneDashboardPageWidgetBillboardNrqlQuery",
    "OneDashboardPageWidgetBillboardNrqlQueryList",
    "OneDashboardPageWidgetBillboardNrqlQueryOutputReference",
    "OneDashboardPageWidgetBillboardOutputReference",
    "OneDashboardPageWidgetBullet",
    "OneDashboardPageWidgetBulletList",
    "OneDashboardPageWidgetBulletNrqlQuery",
    "OneDashboardPageWidgetBulletNrqlQueryList",
    "OneDashboardPageWidgetBulletNrqlQueryOutputReference",
    "OneDashboardPageWidgetBulletOutputReference",
    "OneDashboardPageWidgetFunnel",
    "OneDashboardPageWidgetFunnelList",
    "OneDashboardPageWidgetFunnelNrqlQuery",
    "OneDashboardPageWidgetFunnelNrqlQueryList",
    "OneDashboardPageWidgetFunnelNrqlQueryOutputReference",
    "OneDashboardPageWidgetFunnelOutputReference",
    "OneDashboardPageWidgetHeatmap",
    "OneDashboardPageWidgetHeatmapList",
    "OneDashboardPageWidgetHeatmapNrqlQuery",
    "OneDashboardPageWidgetHeatmapNrqlQueryList",
    "OneDashboardPageWidgetHeatmapNrqlQueryOutputReference",
    "OneDashboardPageWidgetHeatmapOutputReference",
    "OneDashboardPageWidgetHistogram",
    "OneDashboardPageWidgetHistogramList",
    "OneDashboardPageWidgetHistogramNrqlQuery",
    "OneDashboardPageWidgetHistogramNrqlQueryList",
    "OneDashboardPageWidgetHistogramNrqlQueryOutputReference",
    "OneDashboardPageWidgetHistogramOutputReference",
    "OneDashboardPageWidgetJson",
    "OneDashboardPageWidgetJsonList",
    "OneDashboardPageWidgetJsonNrqlQuery",
    "OneDashboardPageWidgetJsonNrqlQueryList",
    "OneDashboardPageWidgetJsonNrqlQueryOutputReference",
    "OneDashboardPageWidgetJsonOutputReference",
    "OneDashboardPageWidgetLine",
    "OneDashboardPageWidgetLineList",
    "OneDashboardPageWidgetLineNrqlQuery",
    "OneDashboardPageWidgetLineNrqlQueryList",
    "OneDashboardPageWidgetLineNrqlQueryOutputReference",
    "OneDashboardPageWidgetLineOutputReference",
    "OneDashboardPageWidgetLogTable",
    "OneDashboardPageWidgetLogTableList",
    "OneDashboardPageWidgetLogTableNrqlQuery",
    "OneDashboardPageWidgetLogTableNrqlQueryList",
    "OneDashboardPageWidgetLogTableNrqlQueryOutputReference",
    "OneDashboardPageWidgetLogTableOutputReference",
    "OneDashboardPageWidgetMarkdown",
    "OneDashboardPageWidgetMarkdownList",
    "OneDashboardPageWidgetMarkdownOutputReference",
    "OneDashboardPageWidgetPie",
    "OneDashboardPageWidgetPieList",
    "OneDashboardPageWidgetPieNrqlQuery",
    "OneDashboardPageWidgetPieNrqlQueryList",
    "OneDashboardPageWidgetPieNrqlQueryOutputReference",
    "OneDashboardPageWidgetPieOutputReference",
    "OneDashboardPageWidgetStackedBar",
    "OneDashboardPageWidgetStackedBarList",
    "OneDashboardPageWidgetStackedBarNrqlQuery",
    "OneDashboardPageWidgetStackedBarNrqlQueryList",
    "OneDashboardPageWidgetStackedBarNrqlQueryOutputReference",
    "OneDashboardPageWidgetStackedBarOutputReference",
    "OneDashboardPageWidgetTable",
    "OneDashboardPageWidgetTableList",
    "OneDashboardPageWidgetTableNrqlQuery",
    "OneDashboardPageWidgetTableNrqlQueryList",
    "OneDashboardPageWidgetTableNrqlQueryOutputReference",
    "OneDashboardPageWidgetTableOutputReference",
    "OneDashboardVariable",
    "OneDashboardVariableItem",
    "OneDashboardVariableItemList",
    "OneDashboardVariableItemOutputReference",
    "OneDashboardVariableList",
    "OneDashboardVariableNrqlQuery",
    "OneDashboardVariableNrqlQueryOutputReference",
    "OneDashboardVariableOutputReference",
]

publication.publish()

def _typecheckingstub__feca567106b8718efc93d950aad2c0578a8de5ce54cbfc6f44ca17c804c2626f(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    page: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPage, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__80c4803501bb8b54897eae197c2cb79eae7f3709d0d16634d00d600dc23b0f9a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9de57c9e41664179a6133c15816d5cc1f1ca4ee5f82ea1597c3225a775e42ee(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e89aeae913cc56708e3bbbe9107e552e4e5a954bdfd7067b870e5dbcb02b5a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ec2164b43e91f5ad208b6db064916847ef31a81a329fb92d562206cc3cddfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f751be9c0fc528c2067b3d388841a0c0497c913308ec8296501ff22d1254445e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e256d2cd840af74023616f1df3551e739f981c27ffae0dffe75e35e283538fcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2c9555d9ec06b00b525f23399b17b061b23636caf36387a29a9908f2f48904(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf246025deeda1e6a2d2f0ee4748ee6ac41552f5535bd2c9fec6b73660b58ff(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    page: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPage, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[builtins.str] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad90e159424eaeeb508b02cde06a6c3bdd8561b00435df1ce2dd2ebbbbb7fe6(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    widget_area: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetArea, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_bar: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBar, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_billboard: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBillboard, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_bullet: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBullet, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_funnel: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetFunnel, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_heatmap: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHeatmap, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_histogram: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHistogram, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_json: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetJson, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_line: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLine, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_log_table: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLogTable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_markdown: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetMarkdown, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_pie: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetPie, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_stacked_bar: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetStackedBar, typing.Dict[builtins.str, typing.Any]]]]] = None,
    widget_table: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetTable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cff5a67842ce39ee793086a8751ca33e6db073a384983147ac8b5a82a2bf90d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19fafd33a889731bf38d89935767917448bd94db445264feccf9799526b6392c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c4cccd632b3d63b2e46a24a280f42abecf0e2775433501028069f320b8a914(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b557b195645bb7553b9deb9d116599cc8b20fd5bc19022186504ee6c236d9618(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__030b8a998f62bcb54c79ced0a98aa03b55acef12de0acd1f89d97ca232147bd1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ff19f4a9b0e1cc4c0efe0ae026a121e88538f2ef4eeb5c8a4c6d620ee034b5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__812cda7b001a2fdcb6c1a9e9fa043d9092d77ff2c7b9a1583a90d7969348651c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc40807903017bb98d2bc10303e803173880f844245748c8ccc2f53de964066(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetArea, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70dccb11444f8b75235a86f241a576d426cb76ae4b4f99d8dbbd9b31f6d12f4c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBar, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f56c048406405ead03777bf8e7c4211d75e6f41c76ee8d8694d2e96c3ca4277(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBillboard, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777087add7016c4857de95b7f8a53b06aaf674685e0b9f527e90971a4ce52472(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBullet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a865e47824c262809ae0c6eb30214c28fc1a9d4c3dcd4691d3ac5ece4d3423(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetFunnel, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c57fd9012eb439ed8fe92047b0ee43fae8b291d7438f4322813dfceba9d9d5b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHeatmap, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b448a939ecb5fe12b3d9d0a3a51f49ab77b9f9ce03c391ce898f826bcdc2937(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHistogram, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e70f96de5d02450424dda738f11db90e35af6eb3cf1954f739695aba0117a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetJson, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefd6046dab76fe13e484e4ed3aeee6ae36ece945ef8bd2a7de2a25c6f8ea2ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLine, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71ccafb0891025b1e4de88c4a7d4d036065d9b7e843d5ab8cad1cc39678827dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLogTable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85d2e66a6af0d94b94ad2734a4cf09366ea58a431906830f37e9e9851cca8a6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetMarkdown, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__396a554edb1a0ebf81e3c63cd05b160d67ad05f82b56df5907f28aacdc200b6a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetPie, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a66da789f19569d92b64b12b233faf45fd0ec90996eb25237a582345d8157b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetStackedBar, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6795d358808e2ddd9c69ec6409d7210f9d0967310cca777453726303510bd3b2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetTable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8b1deec46dac39726858185173d5ccb5acdc12a0988922bae82e579f334d4b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d0d6310069491de3c098640fd45c8b59928e2a1c55b8ba4ea371fc8cbfe14b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38905a63f7ca2cf0fa26532e7489db78097b0ac33dd4a9c9c1e9d9e26788f7a7(
    value: typing.Optional[typing.Union[OneDashboardPage, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f54147f0484c97291ee89b7cc0b4a467986eff65c7bfade83cb0e27f7d5448(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f57e7a42531872c8b50b58a8f3e4189fdd3bd7ad6b21ed8510103762887d67(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e7e2557492f7e3c22f77282de0fa5fd7a12f3871ea35624a4342fb721aeb629(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__219eea473fe7d0372257d6a8c5a06a26b15cf07893a39fab8931e50b5e5da411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67da9de2ee0461ac9ddcf4923789cc45ca186593aa40d32c157372736a39464c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca2b2110e3751cfa4de2e7db8b5387a82c61e8a91154c25bd074342ba1a21e8e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5f82482d2338f77c052b3f96b9daf2a93e44fa5c13b82d53ed00d0f91145ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetArea]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957a77ef06d2b06a5ed740f10df5fea7f9c08a538f37ef5435446df7ab99fd05(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3700326127ab76a4fe666e375c5b74b367f238b0602323ad988c09e5bc72a686(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4933d6a83022b05b4717e18e4297dcbf055c8b10671423fe4ae50885922de5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c649c70a8ff909456d0de8eccdfc70d69bd3fa230c58100925c5215405f5927c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ef6e7e29772966882d3cc62e8e856abcd16e4e7769ba232a39a026a6554f05(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72df003ff9d45093cbdba688a207d093dd4774cedecbaa105eee9f35eaf2f4bc(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4a2ad5ed1541c1c0fa96d4df410c60218cefa1eabe123d4c6b7af674f77031(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetAreaNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198506a28cc10e1cb203a914fd29564d95f805e118bb241ceac9b6e80110de73(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e62be1affe33864dea41eed3b0c10dbdc3f65ca438c7c50bb012cbf5240f66(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b19eaeb18507cd5eeedce89ef86fdaea7a0cb83533da28562c02f11735f7e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9f6f1ac5d3ec75b2597b6a506f1866c22939fe9ea0f599e9eb2ebdac7c793dc(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34f6d2f11ebffd5380995e337bd9918482bed3f521c0fadee03c5d200694cdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1beb89b4a4773fa3959de85504057e34fe8666bd03e7a623e7cc731ed6a3e2c2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetAreaNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9ec47174de1df60d0e6656643a49fba7d15182277351b06eb5b5474227a63e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b925daa15a3c52ca42453cc7401e423c2ae2a37beb7861f8b523f6d4e4ba4489(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc0c44dbbddbaed7648c0c968649dfcf51b1335ba3bd372805405455eeea437(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2526ff077a49d64dc0133bf9674ac9716540cdd52c84fe0666507f0cc44f61(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2785e9b50ef3975fd112f7847c6b01777127437d126e98bd5a927e93e1004c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2923b233cd6d7378eb5fd31112c2cb1acd6a5917505f9289d22c82e27b2be82(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e8fed6d42099125f481658f092a85657f5a5c1d133caaace195eb11e918897(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetArea, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7fd8f09732c40f5c70b0c3f4f6ccdd6538746442266f32a806a4c3c807c797(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBarNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b5486f560cbe28b41402719068f9150ba0307b2e9e92fcf31f2205686d7b9a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0657dfa99d288047ff79f42ead5444750670c769866c9b74c2ba28d2f9c4a3c8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d5c5fced03c6b0f78e95318b7d7ada3184262de6a9a5340cf9592ad8f056af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb4689f24b1b13343b9023eaa9c0173103f4c86450d4391ed915ff954e468cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abb120db001e855d2ff7b2f885953d2a80565de28b7a26891c5f4a2cf20ab8fd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11be4a4fbc649867e11e91216f90f4c0cfd8cbf394bed19d69c667c49b1ecb49(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBar]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a9443b6c0754224b7df09b9601b83e2dffe0f14164ac765f119d65d6812dd2(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ac5c266eeef75b5b0cd5d5882576e74e14ce248ca9c192d7b2d6719954df06f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1657e5f419f31a9561ac3df55e1af295ad1aca3d91462a72586e7ffb415adb5f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c9d1c5af069284cf3af71764ff14ca5a3839e369484920f04463743c9bce10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e73fdb95acf20e9f7df0bfe45bdff630cf3de9011520f85b9b249f654de9ef4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d8515f55c159fd6cc3d70d3fc78395afcea937334e87367e7bc08746a455f4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__140bf3eeed3bad2af69c6de7632b56b01ede4e0f1fc8486859351322e801b5f9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBarNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f472d68d8ed0e291396f1e4e20c37ec1e178682d900070a8a82d04ae75eef53(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945868a74b0681e0cd2b3cc9316a6c28ee3a852c5936aa321791b11a723670aa(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b48ee21ae3d6865a2b4d284f94f6316f1ca8b24997b8c74a2bec609e44e4d05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443d296956e2a1e1f7b0f64b99e6fab3490408bcdca0c17be288dd59601ae766(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetBarNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f0d3347255e73a5ab0040ae4818356866c1d01e6851264b11d2ae1f209895e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49a042f684f05e397f03acd7d3d2ad9edd4badd08b576eb6e0a9a855f432529(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBarNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c0a295dcaf6f2934705b69e71d6baa4091743148aa2df5c3198e9e334ca27e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a09b0fac3db716b2bba83ee56eefd7ba60d07ac25fc367eada924a2bdfe7d573(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21198abb6340923fa8e662cc2f258e227b8eb3fe7236a02c4bac6220d1d63ea(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd031a028f45f767d27837808315ae8250ec1c7a73bb4f2a0413baad3b55b93c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a54078c351d49bf3f83eda5da11fd9fd1b949b8f33ac6af0bb4919298be6c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e47d5555af8927b028672ab5e440854d2ac9732cb8be92ed10ffe7df75d027(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b3dbb25a65ff1b86cea9d0a720ea6a86ff5aba1a895bc2037775ac6b1f66bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257a41382f8f4cebf3117ea423737cd31517c06887a1adea9895a547ffe78fd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72d03546533b8322f04e13122ff247c06e1fd29ad50251ea45fa8fb01ad4b88f(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetBar, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4519ff1c610e118dde2c95bf8426f5724dfa9398cd0519416b372703ee0f53a6(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    critical: typing.Optional[builtins.str] = None,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    warning: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894fdab0f58338f0b572982508016551d77bf9dea527bdcc9252b74d49d6c05e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46e0c9c70918be2a6b2f97413afa7d53548ba4ffd44f4c28957b419fc720183(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3513ee2b75ba0a7cf72a8d2a3b666263335324ef3ab7ac439d658ecd79f6a5e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50e130bfe66b9e2248172a008b949d1b01b3dae6d5cdfaa3091b0cd847c9392(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c36205dd37c589015f42cc775e72fa5cf6a5b36526e888f03aacb342768dd0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72e79a0b43824b61866cfcdcdd1ef386ae5f13fb9fa13e7fbda439443a483467(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboard]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafa3074e861e1d5ebf2e8c4077b3dfa1f545d4b2db6d102bae2a908189a3598(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48377d1f09f6fa228f0b8a8c06e85d85be44eeacf8f152b24da4f02b4e58c2f3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee644d2f4c7fb4dc3d5c77c8051148e822c03b5ef83ee9b02b93e3e1e31b8c87(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3c47a15a87e0c14f9c702394fab3fc33effc9d1be71d23db9f18545329d317a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f03eefe536ec78a1237cd8ad54fa4af08823da15946d3218a76b4caba9d9f2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__418d6735c96d7f2144d86c144c05e84a9b5ffd3739348b45afce2841a416a1aa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88631c13b2527746d3f58d88744cf32495cbfbf120427d3ca139acc8730ddd33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBillboardNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f1a55f09aafc860275896e0376bf0dbcadd7982bae99a11e13444a5e58ce48a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76a466793b66e28573281916b44fc7d6344b2e8e84f025b8182c639f6772f6b7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4da882a93de44627d05dcfbdfb9d0b3f37a8d1ab73c978d6626d5c22105e7cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0279a8a50903b255714cc3158eeecc6134583afd1b2eec59f9432963da0e01(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b2a58c80eb16a1e50a5ab1bdaba280dfd71696708a83f71e15b5389bf845578(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a296a21633fa7f7b7a4d45fc88a73bb60b7641b013839bba730bb8a68150e5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBillboardNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a18dffa16f429263e7d27b2371285a08dd64bfab2e742f1f690cc46993bb7c0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e139c1d753b5fbe05a725c540362ffcf60a4f4c9efe95e76fbc01cacdc3b7962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0b1875c5ee7f0a0831783325d83299bb4b1489cd4847fad5446a0a5e8bc341(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0de7ab04d21d6f62effbf6aa02e21c5a247caa8642170a1c186fdccccf43a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e4fd9a3bba4caf7de4314341d1309ca69deac272637cdde9d618c5762c228c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6fc0e22620ebe540aedfb24f046292d0c0e3d9f315e858e80a66c993d85a30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9327724f805ffeaacb104c68f13bd5e209426601540f8b764d6ae606736558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc40fb460a2882fbecb1c489b1626d7801f4545dbaa39bf186c99a5ffa7124c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd280d1ba2eb59f0afb44d739c9133da4dc36f41160c491cf27a8aaa06c96411(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetBillboard, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1eddc8ab7bda5dc1856a97b6e9a0daa659f395c405b38d7f1aaed4d210e590f(
    *,
    column: jsii.Number,
    limit: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3852ea534a10337bef8d8d4948320a74e40e6892d8eba9d3e90caf1733e347e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccf70bb55a2d3ddbf1611a392159d3a4f32c3e0bd3ca126acce1dd602ff6b011(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01d19b1a4ada2a2366f02c577516aa90772f1481174f54dcdd73eed3f38eaee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d44eb5d97732f8a43e7e91ac2b25eafb65aa35e3cdc8b5f964908444523aa7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa71dee47c241fb33bd778fe2964ca01d2f63bf794ec2dd8515da2b5e9a10574(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d1466b5ed53a0a827db75cef6c6cacb917349c128cec6893f7fb464bb1134f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBullet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__830407ff9c790892d7f3d865d2e12e4b5e33ea3848217ae530bfcb329328e5e2(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa632382ceb6ac5f9793b4e7f35a9cf5604ef143cee22563ad2f291349f31c6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2234b67d237340a19724a04e952446ace59e80605aae39a64a31074f374cd05f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539dcbd59fa549868ce6af9bca57a114e143e4689f65d7b84d82405966d13559(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf01d7766ccf39888ecf6c6ca8e82cd4abab920d2ec0ce2d576f5cb1f83d8bdf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a0d6fdec01fb5c0864a6d8e345e017cedd7856459d9c5546f8a487f1c362a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8124207fe863c347857484fdf131470697bcf90167e8ff518d174eed9b4bf0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetBulletNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7418bf484b6c56d82111e44b59e4537e944b10eef223caa83ba3c79b4e7c335b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e28b5a7c62256cac6bcea277a72794a992f5e547dc9038ac289e4aa8d94e6827(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__566768ac9cf64270dc0012afdeeb81aed713e2867f448ede93a8e7d28b16e73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ef039acd99a1484a800d026842f309dc2dd7772a344304840c835905c1bccf(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cbc29faf7db3077ad18ed7adef206724bb40a3ec0c0e2635baf803de7c24b0c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91ddd8d69381a842f9e8b16f44cc9c751ad6a3e9cfed50a4047f1233b773177(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetBulletNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__121461dfcf0f6009638d5315e2b760d253ce8e1db8dca3855ac882defed4adf1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebde968b9e629fcdef60488d2d60b8ec38907c96327432783c2fd186c7b98e9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38cb579f1593999e34a2ac80a6f718e6affaefdb53153397b581fb23b2da3dd8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b7850fab8e4d9531df7225e0afff389f82087fc44c66a9afd7396ab056d045(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a50099ed247ebe9901b5b4b4c7ce3fafe5b9bdb09b181131ce7669e48ad8cb0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9734507856a058302b91d644b544a4153903268d88dcdfbf1b0b666cf060fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe19dd3afd9bb3c6ffab99310f4916094d6e197e0d340940bdbdeba3410d6dc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ea5a899a8dee914d61f6586ef998506dee739f05e07b2a761a79515f8c1ae23(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetBullet, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ecd9a6b0fb08de51cb5866fa122f575713c64086df42aff6d60640694311943(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fceba0d6768354f26a811503217927cf9cd31b3bea45ac6d6e160498c9d54c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0f2f6545b1f8feaac3b067774befa68e457cd9399d2642c385c250ca011ba0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5361d9a7ced494aed67622964bcf1f686da82addf31c1a289df6a32043d96e41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde6feea9845fdf87fafb64f8cfffbddffc924b2c6cef3e951b548b06f83d9a1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b6cdb94df3888c22adced4f1661a7add5472b58eaa84d640c8ceb428e7c9c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76637a88105678d2f0c3f437e6dc18564e20d126c46e46b21ebc6fc1eb3f2a9d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnel]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18599d442fc91055a62517eda1609f83a90bff913719ef9f7be06aff0640fa5(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304d58510782c486f012360f9c06311ab9b6f7d832a6a8ba982c00284fa902da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a42fa844c0b2250ee106c9b4c9fed2b4d76a02ca0966047fd3dda9f68f158b59(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e018ca08335cba86810a716eaa08292df209c1fa0abf06f4e4d2d6e8311fdc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ee0c2ea00364fc8e40043b6d96de6918a8d77b54b57fa776aeb946348c9640(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c034c46b8e6f6ab36707ad3e3f44ae6007c429634d3164cc840454c033caeed2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a0a82fae381d175bb094d91cc4289b4899030a57324be951223c2d56f5ea8f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetFunnelNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2083d024a1fea48a05e376d09dbf600ddd0facbf33a12a36d3957057c19a4200(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617570785272fc9cb485f7719e4d7052a00a05781dcfcb092a47f2441fade482(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbca120b6c6f516b2cd2b5c239538dcfd595aef472707099cba7098ea5a48c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d79eb646d91b56c6df7c99c2a364ff4627da7bf21e1075e00317e7b92b39ee20(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7212d0d1203e0b5cf6564bd475e8784e8b82316533aa1c6fb2a4fa1510ffeb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__137909aa4c853fe36b1cd736f01f94150c0ca1c7ce7872604e0f3d73cc821bbe(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetFunnelNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0aa2a7d357a9e1173b0f806439414ad5829fcf17f64d2a4cc971fdea7fa8f0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8342254ebd02fbe1767c7ec5272c45c0e0657e2a8774de30545ed853cd8c463b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24270658967482c61afb5297c564dcc4550cf22a24dc32d514cfa55c1c0459e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d8c46fd94511ab72c2e47bf9c68a68aee4cf05c061644dbe5e5de5a496d566(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed1d12433c0c6ce3e4e934fe86ba5d7181916c9033f9973110babfa31dee7db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b87e22b23df9145d3912e5597245e5d6de128baa82a033f32a03134ab16f4e45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22a4e82cf4c04d694410031fe7806629d618879919776ed89900ff190990c5e(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetFunnel, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a48668e851711da36e9562bf945f2418c3a6c87d91621b6b38cd7de2c3cb5f3(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51caa13b0ebb5bdb86ea44014acc44d3d15ba1ce9bd3d45c9176913accf7d07a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f49a9514adc18db6a887eadaae2bb3210799ea2d37dff953b5ebc00c02b906(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6b9c8c9f6a45cd39eb97b05b41c146b2e533ba170a55cb90f3f5e0111e0d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e42431a8819d7cb334d968d4d03d1f384bf4c4fb29173d6b9cc2e3f1d7960de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f919e8ac7d53e5765149e96db31be15c67c2c9e47ddc09c84c17506728a08e8d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d23626f4696aa43f80dd511ada0bc63dd55cf49f173b155e41ad5a964f24e96(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmap]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48f6ea791b34a1fab69ea90cc7a764d46c48a5859ac6aee2d122e71d1a6e0b49(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e982f44ccdcefa53701b5f47c5822292ebf6544e48b8780914f24b5c81251695(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0872650b35cdbbcd0aef59b5ec366915af24e187dcdb5b3e0546c0220e346138(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b032d7134f4987cc5efe53eaf4ae3ca3080307480f04d63237359af3ef8ee5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f12c7348622730b8456a40e83aa67fbc3c0e3e9244f159f02853dd6e61f1ac1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06789c59c116f26a5c79c03e4de1cb6268d1da8273e0183e9dc3a3a36ef5f50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64491ce37caedf0753c638035eaaead850a5ef3535af87b337563b13cee38395(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHeatmapNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44749baacbf0262c14a862db751c5f78e4c4ff426389a467a66b410680bb331e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a47a015b5eeb328ed06dc15ba5ed4bd5ff30d0e9300233f866e1b21cd8db04(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ede34d867fb31c22914653b4f50ceaead4e29583161ac77e97a6f8531147df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5ec99b27d6ef8cd032b44e314d88089262af84fd7953cb3a6459576557a940(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aee874e2c9d9750dcb6f1716b207575761476123496be60c7baae824b1818f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cb92828002a2e7bf6629157c109bb376b5818eaea46a097ec37a88d5a2c953e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHeatmapNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abd1b40d8a1f78d80eb6fdf923ba5203e87bcee56bd1a35179085f479abebf4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef559e2bb6d62fd16c601730fbd291e8f5c99d289f0892edca0d0f45f27c2e45(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99adce21d444150c4fff8cf2b58731b7762fcd4eb944547f0881621bc76831d3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3532fe23ad894dc35fd8bee4d3cfe470d7a56877b192a7c39d0e6002845620c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cead5768d805a654e389dfe26c11ab254388cc9c981ea7f61e32262290a8b8b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ac7657c875baa52fde7960de56b697b4b03df37f49da61b129b5d5b3e4f9b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6e22bb6432ccfb959a2da6bba3ca2a5659bcb1f2c67df180aeff59ec752627f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec792db211d5952157b01d8d02b1b7c458cbf5f43e1e0032ab41edf563bf6de4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f430c66f13f645b2dfa7fc39df2e05c8e8de8852ed511e6acce23761b52bef1d(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetHeatmap, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b4aa18dfd455e9a25c069343ad099e643e61975ecc01a5a7679dc43460b07a(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdbc753eb485882022e483f950ed5ba3a004e02505bc09d3e24ddf7407a21e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__134d64b2a4e3e32fb17f43e23f113f4e6490778b62e7bdc74c961712e73cbfbd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__551efabbf8b6c3e236c38bcf66f4df5d6892cf5433fadff5e5295c948bcf7885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce31c80552a3e7a4946008044af99b99c58e449494f800349cd5fb51edf24e5a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1abeb843fe9809ef99f6f284fa54e4f2d0f1029dcc1ca070f624b41110ef65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35da2e69f7f8b923ace71d42847ca72cf2f6b4f49c50eb2a2261e60cbfb9e7c6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogram]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0960a9b185a5c7ab276087057011e25a6b3569b169865dc93219771e6db56e0a(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__477f5b48f4fbc6126151ce433af47e1d2b89e6c88fccc9b2e17a80cf9cdd0c24(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abab7167b3b5672991d21c8d78b89291fce3d7735ef11e293c8193b244f56823(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59e280929e547b88de7338a57e9a1dc466856aa357e103ccbf1d73e28d5a9a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4781ea0ba02c72c39a65eeccc6b8907b94845db2d58afa16d818a823b56e85d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0074345df9f11abc8d5c6eb57be30a4497518b450bfe87742be670a11803986b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7fc5e90430d1399f0cf7a3522d237b3f0502068bef3c3db2803fdd6ac1ffbd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetHistogramNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__539b0a13f9d6f024250eb539a23601702c2200b4dade882c6a8a99d8f23cb91c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0aaf10599f0bc10335914ebf8fa7b3e9c322e21fb4d8b1aaa212410c4ba438(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c93e0d6b02564a053feebe4970e6c965ed2788019fed15f03716775cbe98031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6300feb44433e811c485b5f7eee5ddb0c090d4fdea770ceeea15df79479f1ba(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edcd1ca27e962053e4bdfc4e45f2aa19c03849c71c50d7ec6c32d134884d8e17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856797a553b2ebb48d41568daf37e7311f3f2da4efd8f6b5d055f79b9481eee5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetHistogramNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ed59404e17bd667c659646b329bc0226921210927b6730def796b2649eff78(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2937e081bdd8d5494995d827912515ffff9f16c81508d9d64beaed44721f7039(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8cb99b41a4641f1d6bca29eebd410bc7f9bd7cfddc0f3c2cda72a17aa87c79c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f480d4324c25cd6634803148565a5cf47b5d5b07ed308d1e7cc33b6abbde04a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d83f1b001f7b9ba2cf3d4099c0c428df293d34f43ac3ed014ba779b168d8558(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc11d3a37fa43ba0f0aef0156b49987969d239cdfb03e8da2c9ad29c0aed661a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73d2d0888584fab272cc493928e6c0ef0e4cc6ed482adf0146f157b80e9c87c(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetHistogram, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0c7da08740c8d81ea8e144152c334411c5fb54c9d1c704be0d8582e3db7f60(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282760c11198cf171a3fa1e162c3be860a192ed49a5871535666a7f9e97d211b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b8f2a79f64a42fb0d9b4926a963cca9eee62fbc391f28b7d1ef2a231c52e45(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2203d0d6593bd758659857610be4edb5ffcf7e64089cfe7fd42cf12eef303be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df47a0c164cd86551428b2a117ae279a716451ac02cd1598ef5f79b8b724a6a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ac1f4cec76829acf5043ad93e0a36cb87560b0d038f833ad3f9de620e2cf83c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aea7327d7e76db90b1eb66aeea782daf5a6e4e03d5031076d1c439ef65400b9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJson]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b644b5c3d27e0e7c4665fd93b743ac4856e0f6baf4cad80991b9a524dc07258(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70707c438dabb738e093c72dfebba5e5c96f2d04e9450f360b5dace34a770dca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178f1370df3ae1c0b8e4195891306c92ba30664e62a3735c140afabca080420f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ac9c42920567ae5aab8e07ba921286fd99d492545969ffaca52c2b1d18235f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1409374d4ea3cd972ababe9e9ebca4eb06f6cea05dce4ef122323115a7d07d03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c34cd4776caddaa86654a909cd633baa7614efe5fe0790afa9d0b8b480cf9e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c8a408091e46575805940818632949c315ba1d6fdfd61b6f6fb05360c70b47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetJsonNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a236c367885381343585a09804589944a5fbbf0bddb8b3a71329dbb2c73551bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f5f1e863c9bae6199c15a523d48571828b6f85fa52aa98ea6c3d96743eb089(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae172cc5f3c0eda58d199f29e77fba4534ab7b4724c055b14b1747d18b8a264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a401156f408835684fa95f04843a1373d41316a5841c73b90fcd07486887105(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d76b2e18c406bd5291d3d9f9885f2077f67e0c04ad6caa6b271cfb0edc1a8f7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f49a3a167acd4007da90ddd15f6e8676ba5709eba0418eb45bf43cd896f550(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetJsonNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e181007ab327b04f61c91ac379141b30e9c67d2b15d0e638b82bc2c71ff51a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6899733ce2ea2d870c11e3150c0f6a0b477de931492d1e92ab7b956e9949e6d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39930dffa26f369afa3cd1691c85a1ef1543ca75f3748399f21268543f1ea8e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de568b12bda7868542d6003266158171c218b3d630a1d44631ef770283eef3f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ffdffe59db666bc41d1a8520846de54a9249afa98f165087126d5ef0064925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e18ec56b5fa54bff76177bcbbcfae0d07878373cbc87d23d8ec80189fe88154(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65e103e464726157303b7864c547f91698271946ec34779080ebbd11def47af(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetJson, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18149664903820e719a1ae6d88101663f1385b175f6fe3fae3dec3bddd0115b3(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLineNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459b2b8d8365a03ec643ed1618c7a8cebafd7e7ed11180156ddb45b2e6ddc463(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df34111e345276c1f29227917c86afe0a0d03f1fc37c955f4a758569825dc068(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001fdc0128fe3746c02994c4cba36985d02d10a86772fa9758ec4cdac15754f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a16433a8b8de224813eb0e752c65656ae1a443b5743f1cf255b6e99959e4550(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a1365d17c95f03f452afaa47032c128255b1bf2cc86342d5e1948907f1ef38(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7cc17e2c5816452eebf28e5d9b303944c9a6229b91171a23059c9c50b9e1b2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLine]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e04d2773849871dc2fd8ae87adb5ff5bd10960506c1f80c01980b6f125a9aa(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65da24ed376189d012f38cdf2ff1caeb71d2402085fb6608ca4d0ab8243992fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8f3b65ce9d112d1ef61c252ac8a63a03b201ae2999b554c6f9d1d06bc3c5ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088d18ad27f0e50d27cbe55b23ee35ad65c5f38757d1d76f648940cc79e12757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf2c70ded1112dd7e1e6b5121450104b752985743b2421e099a549ea0154398(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e25ac40a8344f5c6c471584d6ba53d810d2aba73978233ec88d27f5049833b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b53c5f2aa89dfef3fe92412a28ec9cefcd2b67d25560522f18c95863002b82(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLineNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629d2eb3fcc088d4ea88a049811b19a56ddb3c870fc54ca98c0e237097831f20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dacd1d1f0c3458b9d9504ed5684080a3500b056904feac7abcefdcc61bd3840(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16579d62ab3b349bb4c1ad35325bc68dd6224d568c9c58fad94df2d734df27c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a87d4f99ee7913e63b2a560fe73be28b480b64eb5072dd7684569c2e3efc2b(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetLineNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c49be1160e85958c7a2a0f6635f47964cfaeb078de9066ff02bd9f059165787(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaf278546e6e79a818a4e82a55a7f3597c58a21e1f50102fd1a8f913a8c2d365(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLineNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ab97ee40e807f6e93c068077ecf1a0eb04316591a6751cecc5b22c0898862c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e5e8713630e8d855bb9f4c21327deb439efab4e64a7b0a8e65fd3ec1900d39(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aebe376b7b245072b3423e251c29d1e3eaa6c880da37ec42947f28b3d1abfc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091d501e7bd3e4067e8260b28f701572d17ace2d4d6ada367821469c9f77a335(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce6c35b1dc673bcbf1f36d593239bd9dbd11a73127c820c1bb21a388f10cf5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd7e243d4dd0ad9374e6173fc592ae3b9d2049a891160fe1831f6313a2926a2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f111ca0289d6f0d2aa217b09e7f698c65d7b1e8045b55dd74ac4409b28c0338(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetLine, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256f0694cbefd9641e4281d2d5f9565b29cd1b64dd7a51e3b5c1fba334c804bb(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb08aae410359b8514f479a7d5180d126a5eba01c6d3d0627c84431f291bc51d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69584cd969523c647b8d5f3b24198a5b88dc85cff40dd0a9db285d4b0577fa3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ac392e9d1b7fd186ef96e14481536686fcab0f6c996b041c6d1b00cbddf8ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1823c49b1f341a237515e35ff39b461da1077ff84d04ccc34d2c33d9b297f947(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee806efccdc8fa45cfe887643a888c30cc71a0624741e9cc4f354fb70ea4d835(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71dbf2a4c3f8246ea08bf1b1e30a3f88582a3db189a42d2e8897dfa324c0bb29(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0faeb7a4013b88c959a6bd72f125b3b0b4610529ba148f3aa09e3c66d1151d6c(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0818cdd4cdcbf5130bdcc236665adce429997fe1aa717241b4f54254bade8f71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__207f02806589225a9a681e9b9f1a5ab4cbf984336974082feda26feecf4baded(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce9fac8908b8071f10d6bd85667b76816f38dc88db04f6247200a22976c2b937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c1b7fdc09c94d22e4c92aff0dad6d289cd596f16d1796a38a9a157542621da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3eca7fdc70000c45639886dcf28c6675acab2671d6fbacd2485d44e0648bbe0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ba9ecad74ed48a93904e7f0dfbd162b497c9593e4e1d904cf1385462fae29a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetLogTableNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2284c8cc0d29a655f31446748a8c654de4d908db461cb8f7e4d0a1efa997e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77703fbf7f6a2ed15b75bec2842dbe6207d06ccb57767882ef983221b852cd76(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c1e59a4b47573c58beea681c7ca7d3c4398303538f881086d8b563edc7ed546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e74ddadf831e7fd049a10a25cde67950862fff34250ce10c02256f0c770de12(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efff0c7a20e4209a519725b3ae5a1cb813a4e8b7aa4db605037cd2877fcfb07c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e19d40157f76867faf82951de958915e4209166cfa1b1f60572b095b70e66da2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetLogTableNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26562561c45104585436cde1af74bba464c09985f5937495a119ba5bfc67fdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715a25e5536e5eddc7a4b3f692b2f3b5242b95fbd508a5ebf5214e32535fe8e1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f72efeac648d382e60fad088772e6017658da361bb30c02a24191d06ca6ee9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89429449cb75f8abd67d09f246e03a4f94a31b2a718950a79cba72cef1f57595(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4907e6f3f2e59069cfa2bfceff587895fa4324742e169f027417e60134f3d1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95effaf8a5d7b7ad8dc2913f66eaefb703ad9dfc53d340dfd8b5510634bc5cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7df64694de42fb61839df74840252ef8de380ffea6a4c4f3573c7b67d6de2d(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetLogTable, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4a6904314303931a0a073bebfa73c39a938a81fdf7a73bf9ecff8a81b093d9(
    *,
    column: jsii.Number,
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    text: typing.Optional[builtins.str] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d346dd67500886aa34481e3d852fe559fb963881db385fe9327907d1aecad28(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7d75b5f02def0af49f5d03221204464fc6f40a06d49618ee55a0a0aa1315453(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41964e1b3c7c5d1ee1693ae44ee0f29f3f61d66df7e2f6429ab5ed4654046df7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b99e6f3d5e37ce6e02fef76e5a9ae595c68a55f777b417a5396f9cf40144bb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba67d602ca85599a539964c11dbdfb3718f4f36c3eca6f2871a01b618de1281(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2baf727b42457805b55d0a52eecc9375719f559a19e4f0f857e601bf9bc15b1d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetMarkdown]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c5e86ca878b67dad2be8f47b6186fb2fc8f3b93efc81b98541141938c0587f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__072448ee639069c76c7d488a1900abeddf3f4b1a94ad24de6423fdfb460b7efc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117f5873e79e46c76c3f879dbdbc170466bfee0a600abf0357cc29af00a30943(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a2ec317c7136fa28f7b085b5cc4253893d3099f2d3cd893cc180c651834ce1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__646fff00e74ac395f992a218332fbe4de3603ee7e2f377bbb4db7bf19c2cc7a5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b8aab6481189e9f6955ff36c76b8e202e9b6e9810a7616526d91b89424486a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce74b7ca7d5458495d6b6283a7943b3fceaab6b63d363e95af4694d78a334178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2556b7b671ddf2f493ffd04e42a21bfb87f81e981530661aa7aae2cc2bf8f0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ab3642467e08c1bf8b1eb5f075723e6a9143b4526b3b1939db9180276f8e9c(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetMarkdown, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4be3ef8b3adbedc30cf23f721a27f7ed100d6d9247520aecdaa0e9f8caad28(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetPieNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de4a24de83f3846c19fb67474ce2487f1bed35effdd7ca69e41a23734035725d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a52e594e087a3c717344d2795417b3d166574731b8a312dd3842cd6048e4aa4a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb749eb27d19032f19691f5de2aceae230c82e33eb6504f00ef622dccbabeb66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9eb0708237add8c980507cdb6169b42ac4c81cd964fb8395c0cf3b3f26fd0e7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17c963640dd5ccc10187741cf1712c2207a98ece8368c133612c14f31e791b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226a3b713666576c12cb54f7435776aa7e033c0b3c0f74de36fb0a7aa5b5e056(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPie]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf8bc34fee0d55fbee5733825bd4b8bdb1e4a6ea87c37c6f111f4aa2d2e30ce(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1534743808bdec658a93bf6f529841ed4e36565db9df52b57c16944073409b05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc37352d2111de4790124bcd476ce8e850090dc1cb59bb8ce54a1b6bf5d670c4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee8df9a7bb19ffdcd70d169deafe9ad248ea0b61e0e6be2db02be3627bb69774(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd6b85d1e7c7f6448cc12f955d00646107720b0ab351308e256d942286a48c1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d66ba4de97c8dae1fb4f46f317d38f704015ab1d7ac73d053af6d626570dd81(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b2339f3d1b3e943630891240068e92a5b991c7eee9a7bc833ddc222fc3c147(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetPieNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43108d0e12501cc7fe372217c21216f6bbdeff848a0a7239358bf6c6f4df05b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08aeacd19cec5cf343f97ba2f39da767c21a2e0ec922fc58634672e99f9ed9b0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__671ba42472b9942c48d6c19ad593d6956eaf5ebeea85fe995020d82c18ceac21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc2be342c5a20894995b3403e763178ed9ba926ab059a7739d13dd77a1a27da2(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetPieNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48569d9875f66ec42ac0c0cb25de11c1d40ea72eb9f4e95cfa0ab49d990fc0d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a107b7c9b50595e01744bd22abd61016b03f273135503bbb24453b2925dc15(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetPieNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6c5460f0bf46103ff40c84fe9daa81aac23aca47bae53fd8ca2c73a09499b22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d8e3d6ddf5a358ea55894d780f2de2e6e1ccdc44698e4813ce2739a1f106c5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18820545cac6ec1141c970ec804d77b7b9701669cc38796ce5d376cada0a683a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__272cc8dfeae4ac1d059d220761d7d21d214726563f7cbd427db17c060e60ef08(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c37e65978ffcb6e8159267d463f46fe71783b999fce441243af6b85e04a27a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ea80004105fac316a41a96e3f1d4fd157caca9d5b64646436182b047b6ad31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6fbd364f5a105fa66cb9d35054b2ab83f70668e0cd379c713f8f428e526a9e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458bcdb43dd96ed6febc406e01ad103d00ccf8e2848842da23fdcf3bcc7d2e84(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa101081971caa0bba52f44f14da9f7f0a0442c39d1f248075e90c01fc8cfce(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetPie, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6752f1dfb839e17794c3fc1984b2624fde4a1900abab3147046c9d149644df0(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7739749390fcf60819ca29cc89d7bff111cdf9337b53b4baedf7b807ec0dfdba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b8da7f7773242a083fe2c3b2a8ac2c1b548cb7ff3732d4e0090ae1fa781d2a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb678cbacd34a0b7f7fe1a9985dab6591b73bcd0395fc392145112a02166f090(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df99e306c62e63dff9a99f2e342c93a560d7ea804dc6e564a1849c349387e58(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c870652350c0f8e7d52225b89e44aeb759132cf47e2a309bd218f114428c659(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb0ac332891ac39c43f8b85eb6ce9d1833d05adc4a1c63373782b595e04f53e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBar]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675cef10884a25b5ee1a32a128aa3e81dbe8480ff251118aee9e1a53fc5e58e3(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb13b206502a46776dfd622a3a43ff090a0c05a2260889c977bf3c49418d078(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__885616935c40a2feb6fe1152ae3ff238d163c41d97e5e6f2cd05ca305ffd96d1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3c0830921379bb1f256c9d747acbcbb6cd5812c15836e961bd20490294228a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c36f1e8442ed392077525d4e26d3622df3eed7aa1f4d4965cb6a0b736154a7d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0aa9acfcdd431338fdc15a61e47121bed77875258d76fde9bc2efda07a94ec0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba97d3e9f11e6d564cd211dc98c08d55bda758317630adad98e616021f674549(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetStackedBarNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b1e17a98fc14e079d689b6cd35a7b75ad2a6ea8b31fb536eb7824c4e6565505(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__540db736bddcbd751f778c395122162cd7f0bffdcde421dbbc5acf108246b0ef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38366a4b73545e631e960d3dcd937673a9c38dec5bea6b071d66f7aa7d6f9676(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1976160c58b5bafc8a490af099131212199a9b35cbfa3c2e359edc15314bb5(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c90e1ed22d4114b53f5d992e667df316c2beb353bae8a3bb4bdcf7a7edd6ba0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4009e92e55ac01950ec924ffabedaabb7ae0de855e2efe2ee18926aea1dd46bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetStackedBarNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880a8bdf61bd79ab2a03d5fc19525b0c9024a584d4e74ad5553a56c7a6591a67(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d85eb623e84b76a9fe9bc3d7d4cc9e3781778c79d57d682ab9c215c4572e9c68(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9c539237347fcc20c85b90e3b69e2e80eb3133349bb938589d92fe16735072(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f588099d5a482f85b77a737c70fe98b0809e9dc294fed5c3481d813f73e3ea81(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56fbe5d8eefcb3425822fe6f7a739e06ac6042f18b05188ba62f7c1b1f8fdd95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0643ef223608f9bf5b09fe2ac8502237fd871fc2fd3c24e4de9b464ffa76174b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ea84a438a7a29412df38aaead8d0f114188e3516a0eae46ec97657f2049a50b(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetStackedBar, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0d83e80b6e042ca608dd188e4fb7a8c39b32a4189c287f49977da72e5dee31(
    *,
    column: jsii.Number,
    nrql_query: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetTableNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
    row: jsii.Number,
    title: builtins.str,
    filter_current_dashboard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    height: typing.Optional[jsii.Number] = None,
    ignore_time_range: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    linked_entity_guids: typing.Optional[typing.Sequence[builtins.str]] = None,
    width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02574d4454dbaef619ecfecb4ccf6190bd9302607082f68353a2e41bb57e366f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce39f3fe98f3d4e9814def0c1a33984b40f831c11055b7578467140fb9d5c31a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a158f1356d6465699fa770b7014f12691b594286d63e4a06295940f5aa06bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad302fa991f646530ac262d2330db29b15c3464efae91000979c9372d71d541c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac332ea9a3809fa2ab65fc9f3f1f2a7477140e1159caac4b76d5bf7f067a57e2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55da68ca642ff07e9327bf7be2d97152d8a5aa32cea5b84945fc44aea5d91ea5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9afa7c932bbf9161a7a7a0e2324d970afc058eddff7934ce23c3971040f81593(
    *,
    query: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498799cd268a3b287b5cf96fe92b288a513b4a2da6b76aac866192f1ec6517c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__446a425303b99fc048a966d559f01c5d5bb538155290b287d0ff87cff5158ef4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc480be70acfa273d06bf85dbce7328fb71f79b87ab239e599b08785862a8ef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3501f231bd1c85e4fc96058972d7593e20244c75c5c5d288af6f88a3aa5ff151(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d783a2d6791b5ea0cd959bd588c45911ac0b87c54f1fcd11888747a020bd771(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c6d34508347644857189fc9c70932610e371beda89eafabfb720e62d8b1e07(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardPageWidgetTableNrqlQuery]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5361b89f85af50d4a30569d0a9bf6d8255406ef0825a898e8b158facbd283d78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480680d2416b0d2a68a30d032f95c57c1ec3c57fdadffe157ff7cdc2936b3f50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e1e3b5c93ecb2f88b2eb94740523206a45d19dca8b8ee198ca4e874d912415(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e8bb4b2decc4557fc3d87c83bb7995b2c0a264c015e28f217abca8012c186b(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetTableNrqlQuery, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882201a67bdccd4708c68e0c382af63841d7d8aa66ca37245b529751f1872f7e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408ad95c1b786a83ef249c142aa1746255ec248b8261a9e6cbd1bb2c62d41a6f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardPageWidgetTableNrqlQuery, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ee3c5609ccacc176610decc594b865b63ddee7ea708c32e3747cd8d746a66f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3bc95990a9d17509b391017a7ca36cfc579da08a7bb481aa7141349bf24a77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75683962dd9a30edf39ba94860edce0aea4eae429d6d67864270dcd4742c8fcb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a2586e27f9052b869620594b521df447e8f9a5837acbb16fe5eed20c6b46c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d391b7aaeacef1003dca7ec6cb36ebb2e5a445964e27166a65cc99c76ef70535(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541d9e8714d1027ed6bf61b1412046f02794fc5e200cb78c61da461ac130c5ab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94248ff54c05f1f33a9f95d5ff07baa7172d646cdc28ecd1a9cbc4e725937069(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e7e37886fc7740d0f33d8389324d0ba9c5136f02d081f75b5ce66da77445ae(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4396cc0e7870c78943737b577eceab76f65cf0cb8a5afd74b2ce57f12d1dd9(
    value: typing.Optional[typing.Union[OneDashboardPageWidgetTable, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1968b96825bdfd0e91e71911576bc8adf3dc036af0a58921ac6ad9fe53a79a25(
    *,
    name: builtins.str,
    replacement_strategy: builtins.str,
    title: builtins.str,
    type: builtins.str,
    default_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_multi_selection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardVariableItem, typing.Dict[builtins.str, typing.Any]]]]] = None,
    nrql_query: typing.Optional[typing.Union[OneDashboardVariableNrqlQuery, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c64b88ec3f8bfa78bcee98491b15db8a1a80015a7e55cb0a68a4a9eef671a2e(
    *,
    value: builtins.str,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab42c55be078e08fb4c34e3d675767321909300a2d1c70aefaa9c8d339423d6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b875f342d0210dd335f9dbf8d8820362a974135eb518010ba23ad22a08b34e14(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45434c39664813a8d67f3ebb82aa3ea99f4fdfdbb96f38e3af00f69a7187a13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68b408951e1e79fe27b34038bbb8a8a1321e8c8fd57c87ab4ff8b2898cbb179c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36508e84671a342c97e43c005bd878c4e17fa6a2e78bac06d2e167d68836281c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2ce05d1c3c933016335982b1770e0c03e50c90d9b56c86a27b39cec1009dd8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariableItem]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27dda56b51e4801d9ca5eca2b5200572fbe199b23bbea6b64ac712d6766cdd79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329ef69b70c9b015549d46f7754657600af83678d54a6b795630c7b8159874c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b598cd1f307c0bab7d3c12fc3d3f7ceb4746b64f7826907c4a7254f095859bf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba839e5d23d59f3cedb13e3e5d9c450787f78ef26fd677bdccc0eabafbe0aa1d(
    value: typing.Optional[typing.Union[OneDashboardVariableItem, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__374ae33ec3310b10a28d36163cf8cacfabfe5a42ab220b55b5ee9e39c279fec4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013399c814170b817f6e3cb135b1a8330b36d55a632b9100778c357baa6200ef(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc49b0efa512ecd69af3a3e5fa33152c85c9448eef2df5d78401181564a30ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01f66025c6f4e1f38927490d03ce9811a6709ae7490ae208a84ca88c625e07d2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66aec6eccb9cdbac36f05f299876fc211bcfd283c2822f7533a11327e39faf9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faee5bc8fa6762e3b08e1a2a12608fb013b3909cc1269620ef8e2eb52350f6ad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[OneDashboardVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d285e813593e095ff97a0067e82b0c88047e9ae8043d748fe8eaf2d53eeadbe5(
    *,
    query: builtins.str,
    account_ids: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d35b6d27305e5e882d833dd0481916828d26f8b8ea3e712c4746b8b80cdf31d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398a8abfaf045ade6ce38310b6dfec4ef8b712ca9ae7273a701d773504ae6d6e(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fc75e5b3cef8dd3556bbb8c1c34646e467c069627b91cd4d8e258102f337f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7ad18d8caca4f2e686554b44699ff32666abc34757d97704163b5ed2bba2069(
    value: typing.Optional[OneDashboardVariableNrqlQuery],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__647bb1d5fd9964d9a1d7f0a59f1f53dc23974b94888dc2bfd1286fc3eb3fa03e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__199c8ae56b09fe7ce101fa3fa08d98cf82e7734660cef96e35e848215912c934(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[OneDashboardVariableItem, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b932f814eb527d3f2922af4348cc2ed4534970133c8d1b26dddb6c27ef52d6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__991298da4497e9559b48676bd1fa45d3b7730c813f91c7e0d79c77170905af6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dda6e2a2e3e8301136d3cd29775e28536c1bd178be57bd5288f8f1870e86be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe432e783cebe6ab52f4fd93ca6059e33dcc44373422c007a6baaea39ff129f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e91f797f13666d025deb8da8a75c1008e7aef914f91f580ffbb67dc55b65438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ac6cac34171e2c55ced2735f57678cfec0bc166c3e0103d8b89d2aa395c78f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d450835486c68dfac33e70d4f958f40f46494ed5bc5beba7c3dcdf9db6aeaf40(
    value: typing.Optional[typing.Union[OneDashboardVariable, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
