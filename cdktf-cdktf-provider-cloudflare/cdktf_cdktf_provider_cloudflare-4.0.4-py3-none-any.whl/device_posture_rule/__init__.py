'''
# `cloudflare_device_posture_rule`

Refer to the Terraform Registory for docs: [`cloudflare_device_posture_rule`](https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule).
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


class DevicePostureRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule cloudflare_device_posture_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule cloudflare_device_posture_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#account_id DevicePostureRule#account_id}
        :param type: The device posture rule type. Available values: ``serial_number``, ``file``, ``application``, ``gateway``, ``warp``, ``domain_joined``, ``os_version``, ``disk_encryption``, ``firewall``, ``workspace_one``, ``unique_client_id``, ``crowdstrike_s2s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#type DevicePostureRule#type}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#description DevicePostureRule#description}.
        :param expiration: Expire posture results after the specified amount of time. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#expiration DevicePostureRule#expiration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#id DevicePostureRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input: input block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#input DevicePostureRule#input}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#match DevicePostureRule#match}
        :param name: Name of the device posture rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#name DevicePostureRule#name}
        :param schedule: Tells the client when to run the device posture check. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#schedule DevicePostureRule#schedule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494f8f43c04817278220af714151722da52fb36b0bd580bd1d619b7d97cbb1af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DevicePostureRuleConfig(
            account_id=account_id,
            type=type,
            description=description,
            expiration=expiration,
            id=id,
            input=input,
            match=match,
            name=name,
            schedule=schedule,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putInput")
    def put_input(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInput", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc988f0d9ae7d1d4202d73f8b30e897c9672ab2dc71b4f472b2aeefb48e18ee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInput", [value]))

    @jsii.member(jsii_name="putMatch")
    def put_match(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleMatch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba2261b3b5e73ce9692241d0cb3f3d3f3b31045f11fe96109d78a473da3dc0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMatch", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExpiration")
    def reset_expiration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpiration", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInput")
    def reset_input(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInput", []))

    @jsii.member(jsii_name="resetMatch")
    def reset_match(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMatch", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="input")
    def input(self) -> "DevicePostureRuleInputList":
        return typing.cast("DevicePostureRuleInputList", jsii.get(self, "input"))

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(self) -> "DevicePostureRuleMatchList":
        return typing.cast("DevicePostureRuleMatchList", jsii.get(self, "match"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="expirationInput")
    def expiration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expirationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputInput")
    def input_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]], jsii.get(self, "inputInput"))

    @builtins.property
    @jsii.member(jsii_name="matchInput")
    def match_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]], jsii.get(self, "matchInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113a65c63dbb9fa728571d146a4c14fdd5a75f1386fe8a44aa0f0e02b8225dba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0384b2fbd09b72376b01b1fcd8bf095bfee99348a8763bc669e50bd919666331)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="expiration")
    def expiration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expiration"))

    @expiration.setter
    def expiration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef2c09ecd134b16867e2569200742966cdc1bb38389214a813498e0d1fc04b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expiration", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dd37e21c027196f9aad5dc1310fc7ef1ce3332c3be23df3cfca8856dbe0b9f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d595444183bfd85332545bc1adb550a16d317e738ff4d2a0b8949e6e36117b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schedule"))

    @schedule.setter
    def schedule(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57114897a71f5585126106626c5d177c2f2c2574406ebaa1afd0ced8e1b1f472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25988da3b1a31806454122c26a530282600cd866dcc7f5fc0a75dba99778a40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleConfig",
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
        "type": "type",
        "description": "description",
        "expiration": "expiration",
        "id": "id",
        "input": "input",
        "match": "match",
        "name": "name",
        "schedule": "schedule",
    },
)
class DevicePostureRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        expiration: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleInput", typing.Dict[builtins.str, typing.Any]]]]] = None,
        match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureRuleMatch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#account_id DevicePostureRule#account_id}
        :param type: The device posture rule type. Available values: ``serial_number``, ``file``, ``application``, ``gateway``, ``warp``, ``domain_joined``, ``os_version``, ``disk_encryption``, ``firewall``, ``workspace_one``, ``unique_client_id``, ``crowdstrike_s2s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#type DevicePostureRule#type}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#description DevicePostureRule#description}.
        :param expiration: Expire posture results after the specified amount of time. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#expiration DevicePostureRule#expiration}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#id DevicePostureRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input: input block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#input DevicePostureRule#input}
        :param match: match block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#match DevicePostureRule#match}
        :param name: Name of the device posture rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#name DevicePostureRule#name}
        :param schedule: Tells the client when to run the device posture check. Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#schedule DevicePostureRule#schedule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa817da09a38468daa126847f27e850ad6afc1a4888ce613898f3cf9d30b4fb4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument expiration", value=expiration, expected_type=type_hints["expiration"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "type": type,
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
        if expiration is not None:
            self._values["expiration"] = expiration
        if id is not None:
            self._values["id"] = id
        if input is not None:
            self._values["input"] = input
        if match is not None:
            self._values["match"] = match
        if name is not None:
            self._values["name"] = name
        if schedule is not None:
            self._values["schedule"] = schedule

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#account_id DevicePostureRule#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The device posture rule type. Available values: ``serial_number``, ``file``, ``application``, ``gateway``, ``warp``, ``domain_joined``, ``os_version``, ``disk_encryption``, ``firewall``, ``workspace_one``, ``unique_client_id``, ``crowdstrike_s2s``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#type DevicePostureRule#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#description DevicePostureRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expiration(self) -> typing.Optional[builtins.str]:
        '''Expire posture results after the specified amount of time.

        Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#expiration DevicePostureRule#expiration}
        '''
        result = self._values.get("expiration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#id DevicePostureRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]]:
        '''input block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#input DevicePostureRule#input}
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleInput"]]], result)

    @builtins.property
    def match(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]]:
        '''match block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#match DevicePostureRule#match}
        '''
        result = self._values.get("match")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureRuleMatch"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the device posture rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#name DevicePostureRule#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional[builtins.str]:
        '''Tells the client when to run the device posture check.

        Must be in the format ``1h`` or ``30m``. Valid units are ``h`` and ``m``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#schedule DevicePostureRule#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInput",
    jsii_struct_bases=[],
    name_mapping={
        "compliance_status": "complianceStatus",
        "connection_id": "connectionId",
        "domain": "domain",
        "enabled": "enabled",
        "exists": "exists",
        "id": "id",
        "operator": "operator",
        "os": "os",
        "os_distro_name": "osDistroName",
        "os_distro_revision": "osDistroRevision",
        "overall": "overall",
        "path": "path",
        "require_all": "requireAll",
        "running": "running",
        "sensor_config": "sensorConfig",
        "sha256": "sha256",
        "thumbprint": "thumbprint",
        "version": "version",
        "version_operator": "versionOperator",
    },
)
class DevicePostureRuleInput:
    def __init__(
        self,
        *,
        compliance_status: typing.Optional[builtins.str] = None,
        connection_id: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        operator: typing.Optional[builtins.str] = None,
        os: typing.Optional[builtins.str] = None,
        os_distro_name: typing.Optional[builtins.str] = None,
        os_distro_revision: typing.Optional[builtins.str] = None,
        overall: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        require_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        running: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sensor_config: typing.Optional[builtins.str] = None,
        sha256: typing.Optional[builtins.str] = None,
        thumbprint: typing.Optional[builtins.str] = None,
        version: typing.Optional[builtins.str] = None,
        version_operator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param compliance_status: The workspace one device compliance status. Available values: ``compliant``, ``noncompliant``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#compliance_status DevicePostureRule#compliance_status}
        :param connection_id: The workspace one connection id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#connection_id DevicePostureRule#connection_id}
        :param domain: The domain that the client must join. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#domain DevicePostureRule#domain}
        :param enabled: True if the firewall must be enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#enabled DevicePostureRule#enabled}
        :param exists: Checks if the file should exist. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#exists DevicePostureRule#exists}
        :param id: The Teams List id. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#id DevicePostureRule#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param operator: The version comparison operator. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#operator DevicePostureRule#operator}
        :param os: OS signal score from Crowdstrike. Value must be between 1 and 100. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#os DevicePostureRule#os}
        :param os_distro_name: The operating system excluding version information. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#os_distro_name DevicePostureRule#os_distro_name}
        :param os_distro_revision: The operating system version excluding OS name information or release name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#os_distro_revision DevicePostureRule#os_distro_revision}
        :param overall: Overall ZTA score from Crowdstrike. Value must be between 1 and 100. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#overall DevicePostureRule#overall}
        :param path: The path to the file. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#path DevicePostureRule#path}
        :param require_all: True if all drives must be encrypted. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#require_all DevicePostureRule#require_all}
        :param running: Checks if the application should be running. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#running DevicePostureRule#running}
        :param sensor_config: Sensor signal score from Crowdstrike. Value must be between 1 and 100. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#sensor_config DevicePostureRule#sensor_config}
        :param sha256: The sha256 hash of the file. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#sha256 DevicePostureRule#sha256}
        :param thumbprint: The thumbprint of the file certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#thumbprint DevicePostureRule#thumbprint}
        :param version: The operating system semantic version. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#version DevicePostureRule#version}
        :param version_operator: The version comparison operator for crowdstrike. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#version_operator DevicePostureRule#version_operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5189d7ffb5c296d0a8d0cf95c7694928856e6a6a5e5a63551b29645ddcdcf7)
            check_type(argname="argument compliance_status", value=compliance_status, expected_type=type_hints["compliance_status"])
            check_type(argname="argument connection_id", value=connection_id, expected_type=type_hints["connection_id"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exists", value=exists, expected_type=type_hints["exists"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument os", value=os, expected_type=type_hints["os"])
            check_type(argname="argument os_distro_name", value=os_distro_name, expected_type=type_hints["os_distro_name"])
            check_type(argname="argument os_distro_revision", value=os_distro_revision, expected_type=type_hints["os_distro_revision"])
            check_type(argname="argument overall", value=overall, expected_type=type_hints["overall"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument require_all", value=require_all, expected_type=type_hints["require_all"])
            check_type(argname="argument running", value=running, expected_type=type_hints["running"])
            check_type(argname="argument sensor_config", value=sensor_config, expected_type=type_hints["sensor_config"])
            check_type(argname="argument sha256", value=sha256, expected_type=type_hints["sha256"])
            check_type(argname="argument thumbprint", value=thumbprint, expected_type=type_hints["thumbprint"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument version_operator", value=version_operator, expected_type=type_hints["version_operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compliance_status is not None:
            self._values["compliance_status"] = compliance_status
        if connection_id is not None:
            self._values["connection_id"] = connection_id
        if domain is not None:
            self._values["domain"] = domain
        if enabled is not None:
            self._values["enabled"] = enabled
        if exists is not None:
            self._values["exists"] = exists
        if id is not None:
            self._values["id"] = id
        if operator is not None:
            self._values["operator"] = operator
        if os is not None:
            self._values["os"] = os
        if os_distro_name is not None:
            self._values["os_distro_name"] = os_distro_name
        if os_distro_revision is not None:
            self._values["os_distro_revision"] = os_distro_revision
        if overall is not None:
            self._values["overall"] = overall
        if path is not None:
            self._values["path"] = path
        if require_all is not None:
            self._values["require_all"] = require_all
        if running is not None:
            self._values["running"] = running
        if sensor_config is not None:
            self._values["sensor_config"] = sensor_config
        if sha256 is not None:
            self._values["sha256"] = sha256
        if thumbprint is not None:
            self._values["thumbprint"] = thumbprint
        if version is not None:
            self._values["version"] = version
        if version_operator is not None:
            self._values["version_operator"] = version_operator

    @builtins.property
    def compliance_status(self) -> typing.Optional[builtins.str]:
        '''The workspace one device compliance status. Available values: ``compliant``, ``noncompliant``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#compliance_status DevicePostureRule#compliance_status}
        '''
        result = self._values.get("compliance_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_id(self) -> typing.Optional[builtins.str]:
        '''The workspace one connection id.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#connection_id DevicePostureRule#connection_id}
        '''
        result = self._values.get("connection_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain that the client must join.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#domain DevicePostureRule#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if the firewall must be enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#enabled DevicePostureRule#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def exists(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Checks if the file should exist.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#exists DevicePostureRule#exists}
        '''
        result = self._values.get("exists")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''The Teams List id.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#id DevicePostureRule#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''The version comparison operator. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#operator DevicePostureRule#operator}
        '''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os(self) -> typing.Optional[builtins.str]:
        '''OS signal score from Crowdstrike. Value must be between 1 and 100.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#os DevicePostureRule#os}
        '''
        result = self._values.get("os")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_distro_name(self) -> typing.Optional[builtins.str]:
        '''The operating system excluding version information.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#os_distro_name DevicePostureRule#os_distro_name}
        '''
        result = self._values.get("os_distro_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def os_distro_revision(self) -> typing.Optional[builtins.str]:
        '''The operating system version excluding OS name information or release name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#os_distro_revision DevicePostureRule#os_distro_revision}
        '''
        result = self._values.get("os_distro_revision")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def overall(self) -> typing.Optional[builtins.str]:
        '''Overall ZTA score from Crowdstrike. Value must be between 1 and 100.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#overall DevicePostureRule#overall}
        '''
        result = self._values.get("overall")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the file.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#path DevicePostureRule#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''True if all drives must be encrypted.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#require_all DevicePostureRule#require_all}
        '''
        result = self._values.get("require_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def running(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Checks if the application should be running.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#running DevicePostureRule#running}
        '''
        result = self._values.get("running")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sensor_config(self) -> typing.Optional[builtins.str]:
        '''Sensor signal score from Crowdstrike. Value must be between 1 and 100.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#sensor_config DevicePostureRule#sensor_config}
        '''
        result = self._values.get("sensor_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sha256(self) -> typing.Optional[builtins.str]:
        '''The sha256 hash of the file.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#sha256 DevicePostureRule#sha256}
        '''
        result = self._values.get("sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def thumbprint(self) -> typing.Optional[builtins.str]:
        '''The thumbprint of the file certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#thumbprint DevicePostureRule#thumbprint}
        '''
        result = self._values.get("thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The operating system semantic version.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#version DevicePostureRule#version}
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_operator(self) -> typing.Optional[builtins.str]:
        '''The version comparison operator for crowdstrike. Available values: ``>``, ``>=``, ``<``, ``<=``, ``==``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#version_operator DevicePostureRule#version_operator}
        '''
        result = self._values.get("version_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleInput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevicePostureRuleInputList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__49aeee82282cc7fbe77ebc8dcabc3e352d6a4510e0e064712ce0010d08d5dfab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DevicePostureRuleInputOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be3cb79c7906e646ce5a0e40c63fefb6f93f5b3434b4977130fab76ceb38d233)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DevicePostureRuleInputOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b0b4f1db1869a08dae27417ed72ca3eee21a30df7c4106a17f841c80e517e8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e225b7db827ae8c40479108e4844e7dd1976f6035121d709452836ff9db0849)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ca76c9518c3f0f8b0c7514171764de7c05bcd7638b1b7805526411dc5e6971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d348b03b9860dd93f49a9101b4d06f94ff5f7e962cff18ecfa2a2cfd19be85f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DevicePostureRuleInputOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleInputOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed93bd050f27ea05e0f30cae92cacd3cb8f4fddd33a31e4c8741ffa057f9e71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetComplianceStatus")
    def reset_compliance_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComplianceStatus", []))

    @jsii.member(jsii_name="resetConnectionId")
    def reset_connection_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionId", []))

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetExists")
    def reset_exists(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExists", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetOs")
    def reset_os(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOs", []))

    @jsii.member(jsii_name="resetOsDistroName")
    def reset_os_distro_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDistroName", []))

    @jsii.member(jsii_name="resetOsDistroRevision")
    def reset_os_distro_revision(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOsDistroRevision", []))

    @jsii.member(jsii_name="resetOverall")
    def reset_overall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOverall", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetRequireAll")
    def reset_require_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAll", []))

    @jsii.member(jsii_name="resetRunning")
    def reset_running(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunning", []))

    @jsii.member(jsii_name="resetSensorConfig")
    def reset_sensor_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensorConfig", []))

    @jsii.member(jsii_name="resetSha256")
    def reset_sha256(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSha256", []))

    @jsii.member(jsii_name="resetThumbprint")
    def reset_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThumbprint", []))

    @jsii.member(jsii_name="resetVersion")
    def reset_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersion", []))

    @jsii.member(jsii_name="resetVersionOperator")
    def reset_version_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionOperator", []))

    @builtins.property
    @jsii.member(jsii_name="complianceStatusInput")
    def compliance_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "complianceStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionIdInput")
    def connection_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="existsInput")
    def exists_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "existsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="osDistroNameInput")
    def os_distro_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDistroNameInput"))

    @builtins.property
    @jsii.member(jsii_name="osDistroRevisionInput")
    def os_distro_revision_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osDistroRevisionInput"))

    @builtins.property
    @jsii.member(jsii_name="osInput")
    def os_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "osInput"))

    @builtins.property
    @jsii.member(jsii_name="overallInput")
    def overall_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "overallInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="requireAllInput")
    def require_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAllInput"))

    @builtins.property
    @jsii.member(jsii_name="runningInput")
    def running_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runningInput"))

    @builtins.property
    @jsii.member(jsii_name="sensorConfigInput")
    def sensor_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sensorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256Input")
    def sha256_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256Input"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintInput")
    def thumbprint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="versionOperatorInput")
    def version_operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionOperatorInput"))

    @builtins.property
    @jsii.member(jsii_name="complianceStatus")
    def compliance_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "complianceStatus"))

    @compliance_status.setter
    def compliance_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f81cc928b1d5f9597a05f475e68cd848be72b30b30adbfc45a0d768003734c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "complianceStatus", value)

    @builtins.property
    @jsii.member(jsii_name="connectionId")
    def connection_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionId"))

    @connection_id.setter
    def connection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b586981fb5b45c04c00ec31700c84899177a0208ba1b5d6380b4b33524e22f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionId", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e36d2c5e54475a0832f73fa60448356c84a5ced07d50635ae443993626b20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__69f168ad98553b54bd5d9d8150fca49faf5b08239be6f7a230e702b18e6bbe65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="exists")
    def exists(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "exists"))

    @exists.setter
    def exists(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8d5e4f9d35e29de4802aba8b03bd4f60dc1ed4a9eb126725e2c8746ce01ea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "exists", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f421d222cda3b11c807139fb4186b08eaad7151a5233e2871e5927e9e5f99d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a14d3372b1fe23805d144a4325d2d61ba72054a3298093f6669d89f5835a64f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="os")
    def os(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "os"))

    @os.setter
    def os(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d1d1360468ae8c277360c714f2aa92e37a210c4f5e6ff0727d87491d74752d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "os", value)

    @builtins.property
    @jsii.member(jsii_name="osDistroName")
    def os_distro_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDistroName"))

    @os_distro_name.setter
    def os_distro_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64df9cef991ed7bdc5396cc281da832305d71b6b9e04856a0b57409b9248ec51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDistroName", value)

    @builtins.property
    @jsii.member(jsii_name="osDistroRevision")
    def os_distro_revision(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "osDistroRevision"))

    @os_distro_revision.setter
    def os_distro_revision(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8820de5a9bc2c9e0278fae6211aef505917b986253507997b00373ceb60042d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "osDistroRevision", value)

    @builtins.property
    @jsii.member(jsii_name="overall")
    def overall(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "overall"))

    @overall.setter
    def overall(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4cfae7d06316d2a4b7cba6105edcafc75add1cd1d2814fc64020ba0a226405f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "overall", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95538f57139ff2073f888f959e913df262826ba63fff9ec127f8407bc93444de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="requireAll")
    def require_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAll"))

    @require_all.setter
    def require_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eda1f64d8ac088442d401cd0c18dca35ea9e5484efac7df84315e494366cad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAll", value)

    @builtins.property
    @jsii.member(jsii_name="running")
    def running(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "running"))

    @running.setter
    def running(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab0e2534a655fda0582b2ac117cb03f137d05edbc0358b6e3fd95967720bc6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "running", value)

    @builtins.property
    @jsii.member(jsii_name="sensorConfig")
    def sensor_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sensorConfig"))

    @sensor_config.setter
    def sensor_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3f4ea1dc29e979604856b82d0698e51b816c23dca277c802cbe2e27e5e9252)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensorConfig", value)

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @sha256.setter
    def sha256(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e301519b0f3c25d96c0d2657988dbc37b52e73b37b96176b2c57caefe79841d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256", value)

    @builtins.property
    @jsii.member(jsii_name="thumbprint")
    def thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thumbprint"))

    @thumbprint.setter
    def thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f6ee2a79ed3673cf1258e8580d0447504ded7048b074cd960d5040b7a707c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprint", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16470c2b91bd05726d3678e5e288ee8313a17f8946d49b9f9b52f4f0bad3d59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value)

    @builtins.property
    @jsii.member(jsii_name="versionOperator")
    def version_operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionOperator"))

    @version_operator.setter
    def version_operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43d08fba0d50dfb9f96049786176f5ccf1442140a1a52ce6692897861dae0bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionOperator", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DevicePostureRuleInput, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DevicePostureRuleInput, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DevicePostureRuleInput, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5df1763055034b69fdc812d5d10828d2a4d0805754ba0f47c3cb1a7c672d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleMatch",
    jsii_struct_bases=[],
    name_mapping={"platform": "platform"},
)
class DevicePostureRuleMatch:
    def __init__(self, *, platform: typing.Optional[builtins.str] = None) -> None:
        '''
        :param platform: The platform of the device. Available values: ``windows``, ``mac``, ``linux``, ``android``, ``ios``, ``chromeos``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#platform DevicePostureRule#platform}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbfc29af90f1985dc6f5c7186dd463794fe056488a7dc1bf660c7f04f0ec3d32)
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if platform is not None:
            self._values["platform"] = platform

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform of the device. Available values: ``windows``, ``mac``, ``linux``, ``android``, ``ios``, ``chromeos``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_rule#platform DevicePostureRule#platform}
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureRuleMatch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevicePostureRuleMatchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleMatchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3627b13043be2a5afc4695f646ca3e323ea9483bf4794bc16fb5e51331448fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DevicePostureRuleMatchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f88b77c2037a61eb21fe29e3f27c94a664f20de53f14f224723cffdb5555be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DevicePostureRuleMatchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35c089de7932e476602bc098ae47e356e9f5860cd84cdeaed5d8b90279890342)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73133f30821f3fa4d55af9ea1928e47a5663a0ce3f98a2f5e19aebaaf2f11e7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41936c2d40d357169dbcd5260a434318660774f2b29c29da3288e5af12be7577)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e77ac11684684b9bb72b872e9c6380ece7c4e758295a4fee695bdca8b3b31dad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DevicePostureRuleMatchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureRule.DevicePostureRuleMatchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f89d1d0345ad7a762ea9be4a49982bb7dc401c76a39774a03c10a6f112df0ed7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPlatform")
    def reset_platform(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlatform", []))

    @builtins.property
    @jsii.member(jsii_name="platformInput")
    def platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformInput"))

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e944670d3e86a9bd0b9cd68438e0fd6bcf06add90ade5e9a23fc4e96d82c02f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DevicePostureRuleMatch, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DevicePostureRuleMatch, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DevicePostureRuleMatch, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117ce4a84081f4816f7794c78d75cdb0c7a36cabd16de31e3e3356208cd319a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DevicePostureRule",
    "DevicePostureRuleConfig",
    "DevicePostureRuleInput",
    "DevicePostureRuleInputList",
    "DevicePostureRuleInputOutputReference",
    "DevicePostureRuleMatch",
    "DevicePostureRuleMatchList",
    "DevicePostureRuleMatchOutputReference",
]

publication.publish()

def _typecheckingstub__494f8f43c04817278220af714151722da52fb36b0bd580bd1d619b7d97cbb1af(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__fc988f0d9ae7d1d4202d73f8b30e897c9672ab2dc71b4f472b2aeefb48e18ee1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInput, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba2261b3b5e73ce9692241d0cb3f3d3f3b31045f11fe96109d78a473da3dc0a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleMatch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113a65c63dbb9fa728571d146a4c14fdd5a75f1386fe8a44aa0f0e02b8225dba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0384b2fbd09b72376b01b1fcd8bf095bfee99348a8763bc669e50bd919666331(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef2c09ecd134b16867e2569200742966cdc1bb38389214a813498e0d1fc04b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dd37e21c027196f9aad5dc1310fc7ef1ce3332c3be23df3cfca8856dbe0b9f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d595444183bfd85332545bc1adb550a16d317e738ff4d2a0b8949e6e36117b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57114897a71f5585126106626c5d177c2f2c2574406ebaa1afd0ced8e1b1f472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25988da3b1a31806454122c26a530282600cd866dcc7f5fc0a75dba99778a40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa817da09a38468daa126847f27e850ad6afc1a4888ce613898f3cf9d30b4fb4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    expiration: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    input: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleInput, typing.Dict[builtins.str, typing.Any]]]]] = None,
    match: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureRuleMatch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5189d7ffb5c296d0a8d0cf95c7694928856e6a6a5e5a63551b29645ddcdcf7(
    *,
    compliance_status: typing.Optional[builtins.str] = None,
    connection_id: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    exists: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    operator: typing.Optional[builtins.str] = None,
    os: typing.Optional[builtins.str] = None,
    os_distro_name: typing.Optional[builtins.str] = None,
    os_distro_revision: typing.Optional[builtins.str] = None,
    overall: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    require_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    running: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sensor_config: typing.Optional[builtins.str] = None,
    sha256: typing.Optional[builtins.str] = None,
    thumbprint: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
    version_operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49aeee82282cc7fbe77ebc8dcabc3e352d6a4510e0e064712ce0010d08d5dfab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be3cb79c7906e646ce5a0e40c63fefb6f93f5b3434b4977130fab76ceb38d233(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0b4f1db1869a08dae27417ed72ca3eee21a30df7c4106a17f841c80e517e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e225b7db827ae8c40479108e4844e7dd1976f6035121d709452836ff9db0849(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ca76c9518c3f0f8b0c7514171764de7c05bcd7638b1b7805526411dc5e6971(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d348b03b9860dd93f49a9101b4d06f94ff5f7e962cff18ecfa2a2cfd19be85f3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleInput]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed93bd050f27ea05e0f30cae92cacd3cb8f4fddd33a31e4c8741ffa057f9e71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f81cc928b1d5f9597a05f475e68cd848be72b30b30adbfc45a0d768003734c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b586981fb5b45c04c00ec31700c84899177a0208ba1b5d6380b4b33524e22f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e36d2c5e54475a0832f73fa60448356c84a5ced07d50635ae443993626b20e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69f168ad98553b54bd5d9d8150fca49faf5b08239be6f7a230e702b18e6bbe65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8d5e4f9d35e29de4802aba8b03bd4f60dc1ed4a9eb126725e2c8746ce01ea1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f421d222cda3b11c807139fb4186b08eaad7151a5233e2871e5927e9e5f99d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a14d3372b1fe23805d144a4325d2d61ba72054a3298093f6669d89f5835a64f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d1d1360468ae8c277360c714f2aa92e37a210c4f5e6ff0727d87491d74752d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64df9cef991ed7bdc5396cc281da832305d71b6b9e04856a0b57409b9248ec51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8820de5a9bc2c9e0278fae6211aef505917b986253507997b00373ceb60042d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4cfae7d06316d2a4b7cba6105edcafc75add1cd1d2814fc64020ba0a226405f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95538f57139ff2073f888f959e913df262826ba63fff9ec127f8407bc93444de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eda1f64d8ac088442d401cd0c18dca35ea9e5484efac7df84315e494366cad8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab0e2534a655fda0582b2ac117cb03f137d05edbc0358b6e3fd95967720bc6f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3f4ea1dc29e979604856b82d0698e51b816c23dca277c802cbe2e27e5e9252(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e301519b0f3c25d96c0d2657988dbc37b52e73b37b96176b2c57caefe79841d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f6ee2a79ed3673cf1258e8580d0447504ded7048b074cd960d5040b7a707c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16470c2b91bd05726d3678e5e288ee8313a17f8946d49b9f9b52f4f0bad3d59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43d08fba0d50dfb9f96049786176f5ccf1442140a1a52ce6692897861dae0bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5df1763055034b69fdc812d5d10828d2a4d0805754ba0f47c3cb1a7c672d86(
    value: typing.Optional[typing.Union[DevicePostureRuleInput, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbfc29af90f1985dc6f5c7186dd463794fe056488a7dc1bf660c7f04f0ec3d32(
    *,
    platform: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3627b13043be2a5afc4695f646ca3e323ea9483bf4794bc16fb5e51331448fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f88b77c2037a61eb21fe29e3f27c94a664f20de53f14f224723cffdb5555be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35c089de7932e476602bc098ae47e356e9f5860cd84cdeaed5d8b90279890342(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73133f30821f3fa4d55af9ea1928e47a5663a0ce3f98a2f5e19aebaaf2f11e7e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41936c2d40d357169dbcd5260a434318660774f2b29c29da3288e5af12be7577(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e77ac11684684b9bb72b872e9c6380ece7c4e758295a4fee695bdca8b3b31dad(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureRuleMatch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89d1d0345ad7a762ea9be4a49982bb7dc401c76a39774a03c10a6f112df0ed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e944670d3e86a9bd0b9cd68438e0fd6bcf06add90ade5e9a23fc4e96d82c02f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117ce4a84081f4816f7794c78d75cdb0c7a36cabd16de31e3e3356208cd319a1(
    value: typing.Optional[typing.Union[DevicePostureRuleMatch, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
