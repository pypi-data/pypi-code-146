'''
# `cloudflare_list`

Refer to the Terraform Registory for docs: [`cloudflare_list`](https://www.terraform.io/docs/providers/cloudflare/r/list).
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


class List(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.list.List",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/list cloudflare_list}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ListItem", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/list cloudflare_list} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#account_id List#account_id}
        :param kind: The type of items the list will contain. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#kind List#kind}
        :param name: The name of the list. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#name List#name}
        :param description: An optional description of the list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#description List#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#id List#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param item: item block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#item List#item}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__524e2c7d37ad2ce42909cabda973d9e1d995b7f4970a151dffeb131cd179ffd6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ListConfig(
            account_id=account_id,
            kind=kind,
            name=name,
            description=description,
            id=id,
            item=item,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putItem")
    def put_item(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ListItem", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7865f39503856b6b3d7eb26bdffa13c3a8ea0d8d209975a65bd0752e05a9dc5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putItem", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetItem")
    def reset_item(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetItem", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="item")
    def item(self) -> "ListItemList":
        return typing.cast("ListItemList", jsii.get(self, "item"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="itemInput")
    def item_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItem"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItem"]]], jsii.get(self, "itemInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1752ad885ce059d786e1d5c2e40905e901c71f8b2ce95a352a725536478aa6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb73b30d7da97952fc394c7b0bb3763ed7e889357a79df2bb20df110a0d411b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62b5d6e3148951d93a1d78bfc252a553a02dc13b461d3d413fb928500d5e62e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e570c6b9e9c028fadd0332045d759175a31bc297ee7540c4204ebf9457763d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9541ab37c34cf504c7a69b63e8a45b09565cd1bca6cf72ceb3400909fcacc703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.list.ListConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "kind": "kind",
        "name": "name",
        "description": "description",
        "id": "id",
        "item": "item",
    },
)
class ListConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        kind: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ListItem", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#account_id List#account_id}
        :param kind: The type of items the list will contain. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#kind List#kind}
        :param name: The name of the list. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#name List#name}
        :param description: An optional description of the list. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#description List#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#id List#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param item: item block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#item List#item}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d2b96daec7d5ea9ecd7401f5efcd50ecbf8fbc0ca0176388cfc7a64f79cc5d)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument item", value=item, expected_type=type_hints["item"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "kind": kind,
            "name": name,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if item is not None:
            self._values["item"] = item

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
    def account_id(self) -> builtins.str:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#account_id List#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kind(self) -> builtins.str:
        '''The type of items the list will contain.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#kind List#kind}
        '''
        result = self._values.get("kind")
        assert result is not None, "Required property 'kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the list. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#name List#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description of the list.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#description List#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#id List#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def item(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItem"]]]:
        '''item block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#item List#item}
        '''
        result = self._values.get("item")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItem"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.list.ListItem",
    jsii_struct_bases=[],
    name_mapping={"value": "value", "comment": "comment"},
)
class ListItem:
    def __init__(
        self,
        *,
        value: typing.Union["ListItemValue", typing.Dict[builtins.str, typing.Any]],
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: value block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#value List#value}
        :param comment: An optional comment for the item. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#comment List#comment}
        '''
        if isinstance(value, dict):
            value = ListItemValue(**value)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c3b8ae65ebf3cb8f5abf1ca477c2bbb8fe83d8786789de2757ceaa671bdd27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def value(self) -> "ListItemValue":
        '''value block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#value List#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast("ListItemValue", result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''An optional comment for the item.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#comment List#comment}
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListItem(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ListItemList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.list.ListItemList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df0bdc8714e8db76245283fc2306992db8414ff45c023063c1c09fedc209aec8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ListItemOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77c049d7e35ea34042cb50d7e98ce435ca97212c0f466efcd0ac21fc655e9c77)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ListItemOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__161880ed5621fdfb4e00610824a2a4db682f3827d8a477504f4f0b1250f8b147)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30af621daeeb12c28f3f4b25b1be14accee26f8225a359c8bd961e7b65cf392d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9f8d2f4238a1a0d10a61f6ad76db00f77963a3908d648de677b8405b68d4ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItem]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItem]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItem]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6cafe6f68bc933c463c39ee43a39fe8928cc08dc83e2bd74fc67db674b839b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ListItemOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.list.ListItemOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ebe89251cae633102b3812125449ff884f1588a3d26eaee17eea16d1f62de37)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putValue")
    def put_value(
        self,
        *,
        ip: typing.Optional[builtins.str] = None,
        redirect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ListItemValueRedirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#ip List#ip}.
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#redirect List#redirect}
        '''
        value = ListItemValue(ip=ip, redirect=redirect)

        return typing.cast(None, jsii.invoke(self, "putValue", [value]))

    @jsii.member(jsii_name="resetComment")
    def reset_comment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComment", []))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> "ListItemValueOutputReference":
        return typing.cast("ListItemValueOutputReference", jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="commentInput")
    def comment_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional["ListItemValue"]:
        return typing.cast(typing.Optional["ListItemValue"], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comment"))

    @comment.setter
    def comment(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b89c3a31f121f054d0ec04e2fe0bf36aa5b7cd4a809dabbe9cd66fb687e2804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comment", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ListItem, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ListItem, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ListItem, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc515de7823bbb0f1be1bf8de264162a64b55c3e31e70f277f93ed26cb10321d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.list.ListItemValue",
    jsii_struct_bases=[],
    name_mapping={"ip": "ip", "redirect": "redirect"},
)
class ListItemValue:
    def __init__(
        self,
        *,
        ip: typing.Optional[builtins.str] = None,
        redirect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ListItemValueRedirect", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#ip List#ip}.
        :param redirect: redirect block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#redirect List#redirect}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0489c2de78ec6900534c1ee89b807b7e83603ee13a57ae62019124af81f8cc3)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument redirect", value=redirect, expected_type=type_hints["redirect"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip is not None:
            self._values["ip"] = ip
        if redirect is not None:
            self._values["redirect"] = redirect

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#ip List#ip}.'''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redirect(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItemValueRedirect"]]]:
        '''redirect block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#redirect List#redirect}
        '''
        result = self._values.get("redirect")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItemValueRedirect"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListItemValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ListItemValueOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.list.ListItemValueOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b274676b6750d3955eb2fe7a6e3d8f0ae5c84dfc301e11f92350dde9e7b5ff)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRedirect")
    def put_redirect(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ListItemValueRedirect", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5591c8a3c9c381a8c4d78c5cc273e830bfb377a48160f8ef0ed4d4915ac381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedirect", [value]))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetRedirect")
    def reset_redirect(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedirect", []))

    @builtins.property
    @jsii.member(jsii_name="redirect")
    def redirect(self) -> "ListItemValueRedirectList":
        return typing.cast("ListItemValueRedirectList", jsii.get(self, "redirect"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="redirectInput")
    def redirect_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItemValueRedirect"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ListItemValueRedirect"]]], jsii.get(self, "redirectInput"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ip"))

    @ip.setter
    def ip(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e99d0cc9afe1853ade14f17d60e4edd2af5820c71a7ce3032bb7712972fe835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ip", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ListItemValue]:
        return typing.cast(typing.Optional[ListItemValue], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ListItemValue]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b73c98da069cb3c3e6b9da06ac8f376a9ec776067faa9eb838e52c0f125927)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.list.ListItemValueRedirect",
    jsii_struct_bases=[],
    name_mapping={
        "source_url": "sourceUrl",
        "target_url": "targetUrl",
        "include_subdomains": "includeSubdomains",
        "preserve_path_suffix": "preservePathSuffix",
        "preserve_query_string": "preserveQueryString",
        "status_code": "statusCode",
        "subpath_matching": "subpathMatching",
    },
)
class ListItemValueRedirect:
    def __init__(
        self,
        *,
        source_url: builtins.str,
        target_url: builtins.str,
        include_subdomains: typing.Optional[builtins.str] = None,
        preserve_path_suffix: typing.Optional[builtins.str] = None,
        preserve_query_string: typing.Optional[builtins.str] = None,
        status_code: typing.Optional[jsii.Number] = None,
        subpath_matching: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source_url: The source url of the redirect. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#source_url List#source_url}
        :param target_url: The target url of the redirect. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#target_url List#target_url}
        :param include_subdomains: Whether the redirect also matches subdomains of the source url. Available values: ``disabled``, ``enabled``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#include_subdomains List#include_subdomains}
        :param preserve_path_suffix: Whether to preserve the path suffix when doing subpath matching. Available values: ``disabled``, ``enabled``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#preserve_path_suffix List#preserve_path_suffix}
        :param preserve_query_string: Whether the redirect target url should keep the query string of the request's url. Available values: ``disabled``, ``enabled``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#preserve_query_string List#preserve_query_string}
        :param status_code: The status code to be used when redirecting a request. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#status_code List#status_code}
        :param subpath_matching: Whether the redirect also matches subpaths of the source url. Available values: ``disabled``, ``enabled``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#subpath_matching List#subpath_matching}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4228e9eab1d43fc6b43fbf2a4caea2f11261d295aea15f0b6423fba239893d4)
            check_type(argname="argument source_url", value=source_url, expected_type=type_hints["source_url"])
            check_type(argname="argument target_url", value=target_url, expected_type=type_hints["target_url"])
            check_type(argname="argument include_subdomains", value=include_subdomains, expected_type=type_hints["include_subdomains"])
            check_type(argname="argument preserve_path_suffix", value=preserve_path_suffix, expected_type=type_hints["preserve_path_suffix"])
            check_type(argname="argument preserve_query_string", value=preserve_query_string, expected_type=type_hints["preserve_query_string"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument subpath_matching", value=subpath_matching, expected_type=type_hints["subpath_matching"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_url": source_url,
            "target_url": target_url,
        }
        if include_subdomains is not None:
            self._values["include_subdomains"] = include_subdomains
        if preserve_path_suffix is not None:
            self._values["preserve_path_suffix"] = preserve_path_suffix
        if preserve_query_string is not None:
            self._values["preserve_query_string"] = preserve_query_string
        if status_code is not None:
            self._values["status_code"] = status_code
        if subpath_matching is not None:
            self._values["subpath_matching"] = subpath_matching

    @builtins.property
    def source_url(self) -> builtins.str:
        '''The source url of the redirect.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#source_url List#source_url}
        '''
        result = self._values.get("source_url")
        assert result is not None, "Required property 'source_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_url(self) -> builtins.str:
        '''The target url of the redirect.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#target_url List#target_url}
        '''
        result = self._values.get("target_url")
        assert result is not None, "Required property 'target_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def include_subdomains(self) -> typing.Optional[builtins.str]:
        '''Whether the redirect also matches subdomains of the source url. Available values: ``disabled``, ``enabled``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#include_subdomains List#include_subdomains}
        '''
        result = self._values.get("include_subdomains")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_path_suffix(self) -> typing.Optional[builtins.str]:
        '''Whether to preserve the path suffix when doing subpath matching. Available values: ``disabled``, ``enabled``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#preserve_path_suffix List#preserve_path_suffix}
        '''
        result = self._values.get("preserve_path_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_query_string(self) -> typing.Optional[builtins.str]:
        '''Whether the redirect target url should keep the query string of the request's url. Available values: ``disabled``, ``enabled``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#preserve_query_string List#preserve_query_string}
        '''
        result = self._values.get("preserve_query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status_code(self) -> typing.Optional[jsii.Number]:
        '''The status code to be used when redirecting a request.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#status_code List#status_code}
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def subpath_matching(self) -> typing.Optional[builtins.str]:
        '''Whether the redirect also matches subpaths of the source url. Available values: ``disabled``, ``enabled``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/list#subpath_matching List#subpath_matching}
        '''
        result = self._values.get("subpath_matching")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListItemValueRedirect(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ListItemValueRedirectList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.list.ListItemValueRedirectList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8856d9b1160f827645c75168fe2f90935f1974bf823413256e1628c2de0a2a0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ListItemValueRedirectOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ed979b25069cda1720ad92cddf36d8bbaf63be7d406c1a76e3e8ec5da82d42)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ListItemValueRedirectOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9d6fd928b188aab73256de8da4a57e1a407c324a88d61a88b51af4dcc428fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8507137bf53fe2a354bbafccba4176601ae5f87f0f92b5b45bc12076815983e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56223c270974ccd4dbc583378b6bd0221e2e353b8185ada0a962250336946613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItemValueRedirect]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItemValueRedirect]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItemValueRedirect]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ef9492d891bf7239ba6af760597cfaa8d8f704ce3abe8c168bcb71ea7089a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ListItemValueRedirectOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.list.ListItemValueRedirectOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fdecbc3b2cceaad9e76d79d2bffd13736d12a58bfbab67fdd153f545bf6086b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIncludeSubdomains")
    def reset_include_subdomains(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeSubdomains", []))

    @jsii.member(jsii_name="resetPreservePathSuffix")
    def reset_preserve_path_suffix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreservePathSuffix", []))

    @jsii.member(jsii_name="resetPreserveQueryString")
    def reset_preserve_query_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveQueryString", []))

    @jsii.member(jsii_name="resetStatusCode")
    def reset_status_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatusCode", []))

    @jsii.member(jsii_name="resetSubpathMatching")
    def reset_subpath_matching(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubpathMatching", []))

    @builtins.property
    @jsii.member(jsii_name="includeSubdomainsInput")
    def include_subdomains_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "includeSubdomainsInput"))

    @builtins.property
    @jsii.member(jsii_name="preservePathSuffixInput")
    def preserve_path_suffix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preservePathSuffixInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveQueryStringInput")
    def preserve_query_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preserveQueryStringInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceUrlInput")
    def source_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="statusCodeInput")
    def status_code_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "statusCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="subpathMatchingInput")
    def subpath_matching_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subpathMatchingInput"))

    @builtins.property
    @jsii.member(jsii_name="targetUrlInput")
    def target_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="includeSubdomains")
    def include_subdomains(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "includeSubdomains"))

    @include_subdomains.setter
    def include_subdomains(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7a25dd3e0f133c2d9b5a4371bc19d26495b5f9558e7f64b3a9b27c58bdfb752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeSubdomains", value)

    @builtins.property
    @jsii.member(jsii_name="preservePathSuffix")
    def preserve_path_suffix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preservePathSuffix"))

    @preserve_path_suffix.setter
    def preserve_path_suffix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c2de0f3a324a129cb430906e0e94e9e48ff26ee548347ecfc103501485a337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preservePathSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="preserveQueryString")
    def preserve_query_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "preserveQueryString"))

    @preserve_query_string.setter
    def preserve_query_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cccfb310107212fb2324ed9bc45bf11b7d07a225a899c06370ff7686af3b867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveQueryString", value)

    @builtins.property
    @jsii.member(jsii_name="sourceUrl")
    def source_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceUrl"))

    @source_url.setter
    def source_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8639f0a3caa56b8fdab8020abef27c1b48b2f5e0ee2a295407383050c430e873)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceUrl", value)

    @builtins.property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "statusCode"))

    @status_code.setter
    def status_code(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050262338910f697af90fae54eb8d98d8dd97fee63a5b98b05c6d09b465b969f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statusCode", value)

    @builtins.property
    @jsii.member(jsii_name="subpathMatching")
    def subpath_matching(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subpathMatching"))

    @subpath_matching.setter
    def subpath_matching(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41f2a09b60e0152490aea7530f3f6ee0938914b8474c4d2907ca6ef5b0211fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subpathMatching", value)

    @builtins.property
    @jsii.member(jsii_name="targetUrl")
    def target_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetUrl"))

    @target_url.setter
    def target_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc17b54f062404650f59825f9e48485dd39a5c57dba6f81fe42ce92a9485fafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetUrl", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ListItemValueRedirect, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ListItemValueRedirect, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ListItemValueRedirect, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d372208ca5079e6e8d49646deeacbbcbd485835e0383ea2f00607e887092291)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "List",
    "ListConfig",
    "ListItem",
    "ListItemList",
    "ListItemOutputReference",
    "ListItemValue",
    "ListItemValueOutputReference",
    "ListItemValueRedirect",
    "ListItemValueRedirectList",
    "ListItemValueRedirectOutputReference",
]

publication.publish()

def _typecheckingstub__524e2c7d37ad2ce42909cabda973d9e1d995b7f4970a151dffeb131cd179ffd6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ListItem, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__7865f39503856b6b3d7eb26bdffa13c3a8ea0d8d209975a65bd0752e05a9dc5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ListItem, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1752ad885ce059d786e1d5c2e40905e901c71f8b2ce95a352a725536478aa6bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb73b30d7da97952fc394c7b0bb3763ed7e889357a79df2bb20df110a0d411b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b5d6e3148951d93a1d78bfc252a553a02dc13b461d3d413fb928500d5e62e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e570c6b9e9c028fadd0332045d759175a31bc297ee7540c4204ebf9457763d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9541ab37c34cf504c7a69b63e8a45b09565cd1bca6cf72ceb3400909fcacc703(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d2b96daec7d5ea9ecd7401f5efcd50ecbf8fbc0ca0176388cfc7a64f79cc5d(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    kind: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    item: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ListItem, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c3b8ae65ebf3cb8f5abf1ca477c2bbb8fe83d8786789de2757ceaa671bdd27(
    *,
    value: typing.Union[ListItemValue, typing.Dict[builtins.str, typing.Any]],
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0bdc8714e8db76245283fc2306992db8414ff45c023063c1c09fedc209aec8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77c049d7e35ea34042cb50d7e98ce435ca97212c0f466efcd0ac21fc655e9c77(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__161880ed5621fdfb4e00610824a2a4db682f3827d8a477504f4f0b1250f8b147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30af621daeeb12c28f3f4b25b1be14accee26f8225a359c8bd961e7b65cf392d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f8d2f4238a1a0d10a61f6ad76db00f77963a3908d648de677b8405b68d4ebf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6cafe6f68bc933c463c39ee43a39fe8928cc08dc83e2bd74fc67db674b839b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItem]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebe89251cae633102b3812125449ff884f1588a3d26eaee17eea16d1f62de37(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b89c3a31f121f054d0ec04e2fe0bf36aa5b7cd4a809dabbe9cd66fb687e2804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc515de7823bbb0f1be1bf8de264162a64b55c3e31e70f277f93ed26cb10321d(
    value: typing.Optional[typing.Union[ListItem, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0489c2de78ec6900534c1ee89b807b7e83603ee13a57ae62019124af81f8cc3(
    *,
    ip: typing.Optional[builtins.str] = None,
    redirect: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ListItemValueRedirect, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b274676b6750d3955eb2fe7a6e3d8f0ae5c84dfc301e11f92350dde9e7b5ff(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5591c8a3c9c381a8c4d78c5cc273e830bfb377a48160f8ef0ed4d4915ac381(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ListItemValueRedirect, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e99d0cc9afe1853ade14f17d60e4edd2af5820c71a7ce3032bb7712972fe835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b73c98da069cb3c3e6b9da06ac8f376a9ec776067faa9eb838e52c0f125927(
    value: typing.Optional[ListItemValue],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4228e9eab1d43fc6b43fbf2a4caea2f11261d295aea15f0b6423fba239893d4(
    *,
    source_url: builtins.str,
    target_url: builtins.str,
    include_subdomains: typing.Optional[builtins.str] = None,
    preserve_path_suffix: typing.Optional[builtins.str] = None,
    preserve_query_string: typing.Optional[builtins.str] = None,
    status_code: typing.Optional[jsii.Number] = None,
    subpath_matching: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8856d9b1160f827645c75168fe2f90935f1974bf823413256e1628c2de0a2a0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ed979b25069cda1720ad92cddf36d8bbaf63be7d406c1a76e3e8ec5da82d42(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9d6fd928b188aab73256de8da4a57e1a407c324a88d61a88b51af4dcc428fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8507137bf53fe2a354bbafccba4176601ae5f87f0f92b5b45bc12076815983e9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56223c270974ccd4dbc583378b6bd0221e2e353b8185ada0a962250336946613(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef9492d891bf7239ba6af760597cfaa8d8f704ce3abe8c168bcb71ea7089a74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ListItemValueRedirect]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fdecbc3b2cceaad9e76d79d2bffd13736d12a58bfbab67fdd153f545bf6086b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7a25dd3e0f133c2d9b5a4371bc19d26495b5f9558e7f64b3a9b27c58bdfb752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c2de0f3a324a129cb430906e0e94e9e48ff26ee548347ecfc103501485a337(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cccfb310107212fb2324ed9bc45bf11b7d07a225a899c06370ff7686af3b867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8639f0a3caa56b8fdab8020abef27c1b48b2f5e0ee2a295407383050c430e873(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050262338910f697af90fae54eb8d98d8dd97fee63a5b98b05c6d09b465b969f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41f2a09b60e0152490aea7530f3f6ee0938914b8474c4d2907ca6ef5b0211fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc17b54f062404650f59825f9e48485dd39a5c57dba6f81fe42ce92a9485fafa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d372208ca5079e6e8d49646deeacbbcbd485835e0383ea2f00607e887092291(
    value: typing.Optional[typing.Union[ListItemValueRedirect, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
