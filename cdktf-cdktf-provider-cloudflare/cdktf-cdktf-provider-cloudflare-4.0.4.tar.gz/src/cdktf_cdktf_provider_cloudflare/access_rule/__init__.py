'''
# `cloudflare_access_rule`

Refer to the Terraform Registory for docs: [`cloudflare_access_rule`](https://www.terraform.io/docs/providers/cloudflare/r/access_rule).
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


class AccessRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessRule.AccessRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule cloudflare_access_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        configuration: typing.Union["AccessRuleConfiguration", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule cloudflare_access_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#configuration AccessRule#configuration}
        :param mode: The action to apply to a matched request. Available values: ``block``, ``challenge``, ``whitelist``, ``js_challenge``, ``managed_challenge``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#mode AccessRule#mode}
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#account_id AccessRule#account_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#id AccessRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: A personal note about the rule. Typically used as a reminder or explanation for the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#notes AccessRule#notes}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#zone_id AccessRule#zone_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1077ddacbc0bb08e1b5d3168fcb95c249badd1966fda88a4a8f78c89f27fbef9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessRuleConfig(
            configuration=configuration,
            mode=mode,
            account_id=account_id,
            id=id,
            notes=notes,
            zone_id=zone_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(self, *, target: builtins.str, value: builtins.str) -> None:
        '''
        :param target: The request property to target. Available values: ``ip``, ``ip6``, ``ip_range``, ``asn``, ``country``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#target AccessRule#target}
        :param value: The value to target. Depends on target's type. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#value AccessRule#value}
        '''
        value_ = AccessRuleConfiguration(target=target, value=value)

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value_]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotes")
    def reset_notes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotes", []))

    @jsii.member(jsii_name="resetZoneId")
    def reset_zone_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "AccessRuleConfigurationOutputReference":
        return typing.cast("AccessRuleConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["AccessRuleConfiguration"]:
        return typing.cast(typing.Optional["AccessRuleConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="notesInput")
    def notes_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notesInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58edbd2c8ed64dd74112d5a6180345c8fc8be03622bdb42fca4a8c59e2eb50b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806abb4d6130be6e8bb41d8535dde6e9a7506ee37df30236d85c6721151faa03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb0aaa75621abdb1bf750185ffe478b07f6ce33585eeb513c923f031906f104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="notes")
    def notes(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notes"))

    @notes.setter
    def notes(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__809718b30a45abd6356d638fc44bac7393603e002b6ed8cca65d037294625077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notes", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c48cd785596a64c43f7f417ea39c51a53d7b004265a3ecd836e2638d06de867)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessRule.AccessRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "configuration": "configuration",
        "mode": "mode",
        "account_id": "accountId",
        "id": "id",
        "notes": "notes",
        "zone_id": "zoneId",
    },
)
class AccessRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        configuration: typing.Union["AccessRuleConfiguration", typing.Dict[builtins.str, typing.Any]],
        mode: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notes: typing.Optional[builtins.str] = None,
        zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#configuration AccessRule#configuration}
        :param mode: The action to apply to a matched request. Available values: ``block``, ``challenge``, ``whitelist``, ``js_challenge``, ``managed_challenge``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#mode AccessRule#mode}
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#account_id AccessRule#account_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#id AccessRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notes: A personal note about the rule. Typically used as a reminder or explanation for the rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#notes AccessRule#notes}
        :param zone_id: The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#zone_id AccessRule#zone_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = AccessRuleConfiguration(**configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94625c91121e0016a1d16ae59cb9aa215f7c9a797779bdcb6aec30b716109faa)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notes", value=notes, expected_type=type_hints["notes"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
            "mode": mode,
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
        if id is not None:
            self._values["id"] = id
        if notes is not None:
            self._values["notes"] = notes
        if zone_id is not None:
            self._values["zone_id"] = zone_id

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
    def configuration(self) -> "AccessRuleConfiguration":
        '''configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#configuration AccessRule#configuration}
        '''
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("AccessRuleConfiguration", result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''The action to apply to a matched request. Available values: ``block``, ``challenge``, ``whitelist``, ``js_challenge``, ``managed_challenge``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#mode AccessRule#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#account_id AccessRule#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#id AccessRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notes(self) -> typing.Optional[builtins.str]:
        '''A personal note about the rule. Typically used as a reminder or explanation for the rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#notes AccessRule#notes}
        '''
        result = self._values.get("notes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zone_id(self) -> typing.Optional[builtins.str]:
        '''The zone identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#zone_id AccessRule#zone_id}
        '''
        result = self._values.get("zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.accessRule.AccessRuleConfiguration",
    jsii_struct_bases=[],
    name_mapping={"target": "target", "value": "value"},
)
class AccessRuleConfiguration:
    def __init__(self, *, target: builtins.str, value: builtins.str) -> None:
        '''
        :param target: The request property to target. Available values: ``ip``, ``ip6``, ``ip_range``, ``asn``, ``country``. **Modifying this attribute will force creation of a new resource.** Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#target AccessRule#target}
        :param value: The value to target. Depends on target's type. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#value AccessRule#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00f6aea14342a2e618e6e1295525269b246bc321e7ebf80e22c6e9975862bd4)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
            "value": value,
        }

    @builtins.property
    def target(self) -> builtins.str:
        '''The request property to target.

        Available values: ``ip``, ``ip6``, ``ip_range``, ``asn``, ``country``. **Modifying this attribute will force creation of a new resource.**

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#target AccessRule#target}
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The value to target. Depends on target's type. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/access_rule#value AccessRule#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessRuleConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessRuleConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.accessRule.AccessRuleConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9911051ccc4f125a0721098b294e5c7328a197f2e992957b30af90c528a1d0f0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a375300b1c14e407ed8c7cb9c4222cecd410878854f749796ab743644babc42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6119730d96c6433affb46d597fcc11c8a7a9bd768669cc58bea1ffee9c999834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AccessRuleConfiguration]:
        return typing.cast(typing.Optional[AccessRuleConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AccessRuleConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e760f6d675695a5f7ae5fa94e1a41759e1d27dfe9ca65c8e56051a7ddc99bd37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AccessRule",
    "AccessRuleConfig",
    "AccessRuleConfiguration",
    "AccessRuleConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__1077ddacbc0bb08e1b5d3168fcb95c249badd1966fda88a4a8f78c89f27fbef9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    configuration: typing.Union[AccessRuleConfiguration, typing.Dict[builtins.str, typing.Any]],
    mode: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__58edbd2c8ed64dd74112d5a6180345c8fc8be03622bdb42fca4a8c59e2eb50b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806abb4d6130be6e8bb41d8535dde6e9a7506ee37df30236d85c6721151faa03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb0aaa75621abdb1bf750185ffe478b07f6ce33585eeb513c923f031906f104(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__809718b30a45abd6356d638fc44bac7393603e002b6ed8cca65d037294625077(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c48cd785596a64c43f7f417ea39c51a53d7b004265a3ecd836e2638d06de867(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94625c91121e0016a1d16ae59cb9aa215f7c9a797779bdcb6aec30b716109faa(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    configuration: typing.Union[AccessRuleConfiguration, typing.Dict[builtins.str, typing.Any]],
    mode: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notes: typing.Optional[builtins.str] = None,
    zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00f6aea14342a2e618e6e1295525269b246bc321e7ebf80e22c6e9975862bd4(
    *,
    target: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9911051ccc4f125a0721098b294e5c7328a197f2e992957b30af90c528a1d0f0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a375300b1c14e407ed8c7cb9c4222cecd410878854f749796ab743644babc42a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6119730d96c6433affb46d597fcc11c8a7a9bd768669cc58bea1ffee9c999834(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e760f6d675695a5f7ae5fa94e1a41759e1d27dfe9ca65c8e56051a7ddc99bd37(
    value: typing.Optional[AccessRuleConfiguration],
) -> None:
    """Type checking stubs"""
    pass
