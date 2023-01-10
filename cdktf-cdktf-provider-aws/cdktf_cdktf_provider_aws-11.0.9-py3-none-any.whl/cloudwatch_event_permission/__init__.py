'''
# `aws_cloudwatch_event_permission`

Refer to the Terraform Registory for docs: [`aws_cloudwatch_event_permission`](https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission).
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


class CloudwatchEventPermission(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchEventPermission.CloudwatchEventPermission",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission aws_cloudwatch_event_permission}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        principal: builtins.str,
        statement_id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union["CloudwatchEventPermissionCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission aws_cloudwatch_event_permission} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param principal: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#principal CloudwatchEventPermission#principal}.
        :param statement_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#statement_id CloudwatchEventPermission#statement_id}.
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#action CloudwatchEventPermission#action}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#condition CloudwatchEventPermission#condition}
        :param event_bus_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#event_bus_name CloudwatchEventPermission#event_bus_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#id CloudwatchEventPermission#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d95c2f4b46ff6278bbb74be4df949a6b83c2289b9a4757e598a2a706d16771d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudwatchEventPermissionConfig(
            principal=principal,
            statement_id=statement_id,
            action=action,
            condition=condition,
            event_bus_name=event_bus_name,
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

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        key: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#key CloudwatchEventPermission#key}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#type CloudwatchEventPermission#type}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#value CloudwatchEventPermission#value}.
        '''
        value_ = CloudwatchEventPermissionCondition(key=key, type=type, value=value)

        return typing.cast(None, jsii.invoke(self, "putCondition", [value_]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetEventBusName")
    def reset_event_bus_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventBusName", []))

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
    @jsii.member(jsii_name="condition")
    def condition(self) -> "CloudwatchEventPermissionConditionOutputReference":
        return typing.cast("CloudwatchEventPermissionConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional["CloudwatchEventPermissionCondition"]:
        return typing.cast(typing.Optional["CloudwatchEventPermissionCondition"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="eventBusNameInput")
    def event_bus_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventBusNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="statementIdInput")
    def statement_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statementIdInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f01034f402eaf3bae3a32c3f122dcd59a3ce4696a04a2ccf17d6d41c67212d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="eventBusName")
    def event_bus_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventBusName"))

    @event_bus_name.setter
    def event_bus_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bfc53cad0897f76ef159fb5212548178fdbc5cf489d3416dece49273b7a3d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventBusName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc6ac5910960c8fdc398fb4888d48148e26b1407eafeefc30f4b03e36e4f8da9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd9a74716d679cc9c1d190b67316a91e72edca40491092603bdf66993846678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="statementId")
    def statement_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "statementId"))

    @statement_id.setter
    def statement_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd338b5caa19b126f955a48ef71bc419000f315810b06ba9a43609c5670742ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "statementId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchEventPermission.CloudwatchEventPermissionCondition",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "type": "type", "value": "value"},
)
class CloudwatchEventPermissionCondition:
    def __init__(
        self,
        *,
        key: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#key CloudwatchEventPermission#key}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#type CloudwatchEventPermission#type}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#value CloudwatchEventPermission#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d54cf5fa8a429eed1fc79cb40829134cc070189f788f5f6aed50265a2113167)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "type": type,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#key CloudwatchEventPermission#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#type CloudwatchEventPermission#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#value CloudwatchEventPermission#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchEventPermissionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudwatchEventPermissionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.cloudwatchEventPermission.CloudwatchEventPermissionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b0a4db5aa8e3517d10a35127969641a3cc5882a41e173f659068da6c80855e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e514a7cdca9104f9046df8605e870a8045d42c0f1c0b05de047397ba62b3afe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d205edfa7b3284fd0040be6116b40d514530c89b809885c00ca4853b8f55e236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f420a38cd50c1935bfb55e1611aa9adde04871782f96534ecd5febde4248cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudwatchEventPermissionCondition]:
        return typing.cast(typing.Optional[CloudwatchEventPermissionCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudwatchEventPermissionCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2013a704f082df38614047961b0607118d06206f477d0515bbcd00fa34bd9d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.cloudwatchEventPermission.CloudwatchEventPermissionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "principal": "principal",
        "statement_id": "statementId",
        "action": "action",
        "condition": "condition",
        "event_bus_name": "eventBusName",
        "id": "id",
    },
)
class CloudwatchEventPermissionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        principal: builtins.str,
        statement_id: builtins.str,
        action: typing.Optional[builtins.str] = None,
        condition: typing.Optional[typing.Union[CloudwatchEventPermissionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        event_bus_name: typing.Optional[builtins.str] = None,
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
        :param principal: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#principal CloudwatchEventPermission#principal}.
        :param statement_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#statement_id CloudwatchEventPermission#statement_id}.
        :param action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#action CloudwatchEventPermission#action}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#condition CloudwatchEventPermission#condition}
        :param event_bus_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#event_bus_name CloudwatchEventPermission#event_bus_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#id CloudwatchEventPermission#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = CloudwatchEventPermissionCondition(**condition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c805913becc0f270a4c6c2f656dae9da33b320b89fad595cc5b8a552c8f4f87f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument statement_id", value=statement_id, expected_type=type_hints["statement_id"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument event_bus_name", value=event_bus_name, expected_type=type_hints["event_bus_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal": principal,
            "statement_id": statement_id,
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
        if action is not None:
            self._values["action"] = action
        if condition is not None:
            self._values["condition"] = condition
        if event_bus_name is not None:
            self._values["event_bus_name"] = event_bus_name
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
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#principal CloudwatchEventPermission#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def statement_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#statement_id CloudwatchEventPermission#statement_id}.'''
        result = self._values.get("statement_id")
        assert result is not None, "Required property 'statement_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#action CloudwatchEventPermission#action}.'''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def condition(self) -> typing.Optional[CloudwatchEventPermissionCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#condition CloudwatchEventPermission#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[CloudwatchEventPermissionCondition], result)

    @builtins.property
    def event_bus_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#event_bus_name CloudwatchEventPermission#event_bus_name}.'''
        result = self._values.get("event_bus_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/cloudwatch_event_permission#id CloudwatchEventPermission#id}.

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
        return "CloudwatchEventPermissionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudwatchEventPermission",
    "CloudwatchEventPermissionCondition",
    "CloudwatchEventPermissionConditionOutputReference",
    "CloudwatchEventPermissionConfig",
]

publication.publish()

def _typecheckingstub__3d95c2f4b46ff6278bbb74be4df949a6b83c2289b9a4757e598a2a706d16771d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    principal: builtins.str,
    statement_id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[CloudwatchEventPermissionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bus_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__9f01034f402eaf3bae3a32c3f122dcd59a3ce4696a04a2ccf17d6d41c67212d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bfc53cad0897f76ef159fb5212548178fdbc5cf489d3416dece49273b7a3d99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6ac5910960c8fdc398fb4888d48148e26b1407eafeefc30f4b03e36e4f8da9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd9a74716d679cc9c1d190b67316a91e72edca40491092603bdf66993846678(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd338b5caa19b126f955a48ef71bc419000f315810b06ba9a43609c5670742ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d54cf5fa8a429eed1fc79cb40829134cc070189f788f5f6aed50265a2113167(
    *,
    key: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0a4db5aa8e3517d10a35127969641a3cc5882a41e173f659068da6c80855e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e514a7cdca9104f9046df8605e870a8045d42c0f1c0b05de047397ba62b3afe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d205edfa7b3284fd0040be6116b40d514530c89b809885c00ca4853b8f55e236(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f420a38cd50c1935bfb55e1611aa9adde04871782f96534ecd5febde4248cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2013a704f082df38614047961b0607118d06206f477d0515bbcd00fa34bd9d0(
    value: typing.Optional[CloudwatchEventPermissionCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c805913becc0f270a4c6c2f656dae9da33b320b89fad595cc5b8a552c8f4f87f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    principal: builtins.str,
    statement_id: builtins.str,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[CloudwatchEventPermissionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bus_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
