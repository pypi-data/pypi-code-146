'''
# `cloudflare_email_routing_catch_all`

Refer to the Terraform Registory for docs: [`cloudflare_email_routing_catch_all`](https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all).
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


class EmailRoutingCatchAll(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAll",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all cloudflare_email_routing_catch_all}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmailRoutingCatchAllAction", typing.Dict[builtins.str, typing.Any]]]],
        matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmailRoutingCatchAllMatcher", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        zone_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all cloudflare_email_routing_catch_all} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#action EmailRoutingCatchAll#action}
        :param matcher: matcher block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#matcher EmailRoutingCatchAll#matcher}
        :param name: Routing rule name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#name EmailRoutingCatchAll#name}
        :param zone_id: The zone identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#zone_id EmailRoutingCatchAll#zone_id}
        :param enabled: Routing rule status. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#enabled EmailRoutingCatchAll#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#id EmailRoutingCatchAll#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af0cfb556aa3bc70705f28118cbbfbf9f41e80153bd78a1ad1a8c3bdcd42ecf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EmailRoutingCatchAllConfig(
            action=action,
            matcher=matcher,
            name=name,
            zone_id=zone_id,
            enabled=enabled,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmailRoutingCatchAllAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6acc5c36d759c7378533a5c4871270b1fbad57b5d230a3272f8a6871acf970a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putMatcher")
    def put_matcher(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmailRoutingCatchAllMatcher", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8addb56474ff1b8b974c91490e202041eae3bd4fe79f92650188d8966655e0cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatcher", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> "EmailRoutingCatchAllActionList":
        return typing.cast("EmailRoutingCatchAllActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="matcher")
    def matcher(self) -> "EmailRoutingCatchAllMatcherList":
        return typing.cast("EmailRoutingCatchAllMatcherList", jsii.get(self, "matcher"))

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmailRoutingCatchAllAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmailRoutingCatchAllAction"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="matcherInput")
    def matcher_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmailRoutingCatchAllMatcher"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmailRoutingCatchAllMatcher"]]], jsii.get(self, "matcherInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__54ac08c202e773ccad0ff344fd64c26ea89ed533e1e27cb7e413542299c68702)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c465a59d77a60351a818dc40984f4e8d5c8fbfa7d741d1e59983933b17ad802c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__445a4b78e15c0a8464715b53874b81120e7001189a031dd9c7cfd3b8fde2c8a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de878100e2abc9bba06681bf6ff5f3a9360914881b0492bc2403c3cc09ee0490)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllAction",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "value": "value"},
)
class EmailRoutingCatchAllAction:
    def __init__(
        self,
        *,
        type: builtins.str,
        value: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param type: Type of supported action. Available values: ``drop``, ``forward``, ``worker``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#type EmailRoutingCatchAll#type}
        :param value: A list with items in the following form. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#value EmailRoutingCatchAll#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1462a5c5e587dfd9c89ce219774145b7c5f97e3a5d3ac67a124e9438ea37f5)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
            "value": value,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of supported action. Available values: ``drop``, ``forward``, ``worker``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#type EmailRoutingCatchAll#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> typing.List[builtins.str]:
        '''A list with items in the following form.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#value EmailRoutingCatchAll#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailRoutingCatchAllAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmailRoutingCatchAllActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__187a7c739711b5cacaa0f75e77d95cde6d4c18e93b5a8da3eb48fbb1950f2b5d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EmailRoutingCatchAllActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c866be048ad6233a16e9e9cbb17f52ba94ff2a437b365e41141ade2c4ef8d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmailRoutingCatchAllActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56d931ce7df4a215db6f31e65c6b19f1678b1410a41cf00f9961c9408ed9c22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a1629ed7adc6b68de3b98f67c882a98c16798a0a53705b3f4560317ef210f59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e2fa329912f622fe395219a9b1495e539d23bc299865ab02d9375a5bde1457a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf1578d3d022c17e193e6816620cccfc6a25284ab5dc6d523a370332561f364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EmailRoutingCatchAllActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb8b9cfa9fb6cf9b71431ff4139eaccc0305d43ee86698270b8ded4c3ac3e02c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000cdfb63d7267475862baaeb07cac323d24033d7aa645c12a5c41f426715041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))

    @value.setter
    def value(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__902786f22c40822c2c0aff2641ed092a0d04763662df88860a1a07455d5be928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[EmailRoutingCatchAllAction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[EmailRoutingCatchAllAction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[EmailRoutingCatchAllAction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2c31e8f20046b273128c68222da3aef51831e006bcd67a2e6692e02a62ce48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action": "action",
        "matcher": "matcher",
        "name": "name",
        "zone_id": "zoneId",
        "enabled": "enabled",
        "id": "id",
    },
)
class EmailRoutingCatchAllConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllAction, typing.Dict[builtins.str, typing.Any]]]],
        matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EmailRoutingCatchAllMatcher", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        zone_id: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#action EmailRoutingCatchAll#action}
        :param matcher: matcher block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#matcher EmailRoutingCatchAll#matcher}
        :param name: Routing rule name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#name EmailRoutingCatchAll#name}
        :param zone_id: The zone identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#zone_id EmailRoutingCatchAll#zone_id}
        :param enabled: Routing rule status. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#enabled EmailRoutingCatchAll#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#id EmailRoutingCatchAll#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce97b72d40ca7f990f99e24cb33020b68c76327e0c169335c245f8be448d10b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "matcher": matcher,
            "name": name,
            "zone_id": zone_id,
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
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id

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
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllAction]]:
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#action EmailRoutingCatchAll#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllAction]], result)

    @builtins.property
    def matcher(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmailRoutingCatchAllMatcher"]]:
        '''matcher block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#matcher EmailRoutingCatchAll#matcher}
        '''
        result = self._values.get("matcher")
        assert result is not None, "Required property 'matcher' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EmailRoutingCatchAllMatcher"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Routing rule name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#name EmailRoutingCatchAll#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#zone_id EmailRoutingCatchAll#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Routing rule status.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#enabled EmailRoutingCatchAll#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#id EmailRoutingCatchAll#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailRoutingCatchAllConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllMatcher",
    jsii_struct_bases=[],
    name_mapping={"type": "type"},
)
class EmailRoutingCatchAllMatcher:
    def __init__(self, *, type: builtins.str) -> None:
        '''
        :param type: Type of matcher. Available values: ``all``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#type EmailRoutingCatchAll#type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662d06cdd34d845d1095ea61ca050c76d8ef9766866ff0357980e8114df003ab)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of matcher. Available values: ``all``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/email_routing_catch_all#type EmailRoutingCatchAll#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmailRoutingCatchAllMatcher(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EmailRoutingCatchAllMatcherList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllMatcherList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3884c84d07e770063a463b0eb8f32530f274c5302426731c1917ac47217f6f2d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EmailRoutingCatchAllMatcherOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9625140f99d3f0458dc24c875ab34782f157682cbb661e0b8f4929072eb8c3dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EmailRoutingCatchAllMatcherOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26c9c2ca95eb56df858791066a4f5272c56036ff16d0c2dcd8bcc41a0a757f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7774cf652b3c5134a4d8c0590f46e05a3ed1ecf1aa70fb56f8fcffc5647c93fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e03950f1d2e1713b7c0293709de7bc16670a533ffc01bfb43311a1c8ace2a35c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllMatcher]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllMatcher]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllMatcher]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f03cdb108c39a5518a419d091bf0de08b0d18ce7afdec73ec8f46a5504e51af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EmailRoutingCatchAllMatcherOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.emailRoutingCatchAll.EmailRoutingCatchAllMatcherOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c7ea092abd7424a772b638a39b1f6ff4f3c286badb5a0d439ef591038325d4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d90538c77ae73269d5db14566846fc630f0f615a992439b1724951f05eb3d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[EmailRoutingCatchAllMatcher, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[EmailRoutingCatchAllMatcher, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[EmailRoutingCatchAllMatcher, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8346014d1eed3308dc07ae9d9c6a61e0dca5e80fa0fa5d0c1235f894ce07d22e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "EmailRoutingCatchAll",
    "EmailRoutingCatchAllAction",
    "EmailRoutingCatchAllActionList",
    "EmailRoutingCatchAllActionOutputReference",
    "EmailRoutingCatchAllConfig",
    "EmailRoutingCatchAllMatcher",
    "EmailRoutingCatchAllMatcherList",
    "EmailRoutingCatchAllMatcherOutputReference",
]

publication.publish()

def _typecheckingstub__9af0cfb556aa3bc70705f28118cbbfbf9f41e80153bd78a1ad1a8c3bdcd42ecf(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllAction, typing.Dict[builtins.str, typing.Any]]]],
    matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllMatcher, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    zone_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__6acc5c36d759c7378533a5c4871270b1fbad57b5d230a3272f8a6871acf970a7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8addb56474ff1b8b974c91490e202041eae3bd4fe79f92650188d8966655e0cc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllMatcher, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ac08c202e773ccad0ff344fd64c26ea89ed533e1e27cb7e413542299c68702(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c465a59d77a60351a818dc40984f4e8d5c8fbfa7d741d1e59983933b17ad802c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__445a4b78e15c0a8464715b53874b81120e7001189a031dd9c7cfd3b8fde2c8a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de878100e2abc9bba06681bf6ff5f3a9360914881b0492bc2403c3cc09ee0490(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1462a5c5e587dfd9c89ce219774145b7c5f97e3a5d3ac67a124e9438ea37f5(
    *,
    type: builtins.str,
    value: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187a7c739711b5cacaa0f75e77d95cde6d4c18e93b5a8da3eb48fbb1950f2b5d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c866be048ad6233a16e9e9cbb17f52ba94ff2a437b365e41141ade2c4ef8d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56d931ce7df4a215db6f31e65c6b19f1678b1410a41cf00f9961c9408ed9c22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a1629ed7adc6b68de3b98f67c882a98c16798a0a53705b3f4560317ef210f59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e2fa329912f622fe395219a9b1495e539d23bc299865ab02d9375a5bde1457a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf1578d3d022c17e193e6816620cccfc6a25284ab5dc6d523a370332561f364(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8b9cfa9fb6cf9b71431ff4139eaccc0305d43ee86698270b8ded4c3ac3e02c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__000cdfb63d7267475862baaeb07cac323d24033d7aa645c12a5c41f426715041(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__902786f22c40822c2c0aff2641ed092a0d04763662df88860a1a07455d5be928(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2c31e8f20046b273128c68222da3aef51831e006bcd67a2e6692e02a62ce48(
    value: typing.Optional[typing.Union[EmailRoutingCatchAllAction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce97b72d40ca7f990f99e24cb33020b68c76327e0c169335c245f8be448d10b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllAction, typing.Dict[builtins.str, typing.Any]]]],
    matcher: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EmailRoutingCatchAllMatcher, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    zone_id: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662d06cdd34d845d1095ea61ca050c76d8ef9766866ff0357980e8114df003ab(
    *,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3884c84d07e770063a463b0eb8f32530f274c5302426731c1917ac47217f6f2d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9625140f99d3f0458dc24c875ab34782f157682cbb661e0b8f4929072eb8c3dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26c9c2ca95eb56df858791066a4f5272c56036ff16d0c2dcd8bcc41a0a757f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7774cf652b3c5134a4d8c0590f46e05a3ed1ecf1aa70fb56f8fcffc5647c93fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03950f1d2e1713b7c0293709de7bc16670a533ffc01bfb43311a1c8ace2a35c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f03cdb108c39a5518a419d091bf0de08b0d18ce7afdec73ec8f46a5504e51af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EmailRoutingCatchAllMatcher]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c7ea092abd7424a772b638a39b1f6ff4f3c286badb5a0d439ef591038325d4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d90538c77ae73269d5db14566846fc630f0f615a992439b1724951f05eb3d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8346014d1eed3308dc07ae9d9c6a61e0dca5e80fa0fa5d0c1235f894ce07d22e(
    value: typing.Optional[typing.Union[EmailRoutingCatchAllMatcher, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
