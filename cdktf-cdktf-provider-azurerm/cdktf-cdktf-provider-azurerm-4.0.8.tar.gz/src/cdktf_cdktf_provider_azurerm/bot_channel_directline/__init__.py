'''
# `azurerm_bot_channel_directline`

Refer to the Terraform Registory for docs: [`azurerm_bot_channel_directline`](https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline).
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


class BotChannelDirectline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectline",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline azurerm_bot_channel_directline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        bot_name: builtins.str,
        location: builtins.str,
        resource_group_name: builtins.str,
        site: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BotChannelDirectlineSite", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BotChannelDirectlineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline azurerm_bot_channel_directline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param bot_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#bot_name BotChannelDirectline#bot_name}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#location BotChannelDirectline#location}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#resource_group_name BotChannelDirectline#resource_group_name}.
        :param site: site block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#site BotChannelDirectline#site}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#id BotChannelDirectline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#timeouts BotChannelDirectline#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85a554247be3636abccb0b50c1ff0b364682b1eba18047e1c079fa82a31f0ed6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BotChannelDirectlineConfig(
            bot_name=bot_name,
            location=location,
            resource_group_name=resource_group_name,
            site=site,
            id=id,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putSite")
    def put_site(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BotChannelDirectlineSite", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9863a90e916a8ba243882c5e45f8c4c59f30d9fcb4a9b5b576f546c1dfc46245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSite", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#create BotChannelDirectline#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#delete BotChannelDirectline#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#read BotChannelDirectline#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#update BotChannelDirectline#update}.
        '''
        value = BotChannelDirectlineTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="site")
    def site(self) -> "BotChannelDirectlineSiteList":
        return typing.cast("BotChannelDirectlineSiteList", jsii.get(self, "site"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BotChannelDirectlineTimeoutsOutputReference":
        return typing.cast("BotChannelDirectlineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="botNameInput")
    def bot_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "botNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="siteInput")
    def site_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BotChannelDirectlineSite"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BotChannelDirectlineSite"]]], jsii.get(self, "siteInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["BotChannelDirectlineTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["BotChannelDirectlineTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="botName")
    def bot_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "botName"))

    @bot_name.setter
    def bot_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ae7adeb335a9fe3a1c77a39c71b42675502686121bdcb034302e0dbf1de94b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "botName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5654eafde6fd249e8753cac3ce185b3da3f18ea4690a31632ccd1fa799c3a150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345738b027ab6a7b097660af2dda931f3741512069e0ab224d25ba7a3c28d985)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f8679ec927562389c518753453bd0a7ae518ad94389e95c7897930ef1865d73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectlineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "bot_name": "botName",
        "location": "location",
        "resource_group_name": "resourceGroupName",
        "site": "site",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class BotChannelDirectlineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        bot_name: builtins.str,
        location: builtins.str,
        resource_group_name: builtins.str,
        site: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["BotChannelDirectlineSite", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["BotChannelDirectlineTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param bot_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#bot_name BotChannelDirectline#bot_name}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#location BotChannelDirectline#location}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#resource_group_name BotChannelDirectline#resource_group_name}.
        :param site: site block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#site BotChannelDirectline#site}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#id BotChannelDirectline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#timeouts BotChannelDirectline#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BotChannelDirectlineTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc9370debbf11dd3214cd0e946b7102a67cfe0a31ab850c18fb2a7c9fabe3184)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument bot_name", value=bot_name, expected_type=type_hints["bot_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument site", value=site, expected_type=type_hints["site"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bot_name": bot_name,
            "location": location,
            "resource_group_name": resource_group_name,
            "site": site,
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
        if id is not None:
            self._values["id"] = id
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def bot_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#bot_name BotChannelDirectline#bot_name}.'''
        result = self._values.get("bot_name")
        assert result is not None, "Required property 'bot_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#location BotChannelDirectline#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#resource_group_name BotChannelDirectline#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BotChannelDirectlineSite"]]:
        '''site block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#site BotChannelDirectline#site}
        '''
        result = self._values.get("site")
        assert result is not None, "Required property 'site' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["BotChannelDirectlineSite"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#id BotChannelDirectline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BotChannelDirectlineTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#timeouts BotChannelDirectline#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BotChannelDirectlineTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BotChannelDirectlineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectlineSite",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "enabled": "enabled",
        "enhanced_authentication_enabled": "enhancedAuthenticationEnabled",
        "trusted_origins": "trustedOrigins",
        "v1_allowed": "v1Allowed",
        "v3_allowed": "v3Allowed",
    },
)
class BotChannelDirectlineSite:
    def __init__(
        self,
        *,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enhanced_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trusted_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        v1_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        v3_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#name BotChannelDirectline#name}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#enabled BotChannelDirectline#enabled}.
        :param enhanced_authentication_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#enhanced_authentication_enabled BotChannelDirectline#enhanced_authentication_enabled}.
        :param trusted_origins: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#trusted_origins BotChannelDirectline#trusted_origins}.
        :param v1_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#v1_allowed BotChannelDirectline#v1_allowed}.
        :param v3_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#v3_allowed BotChannelDirectline#v3_allowed}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3991d622115d672053d64bdbad65aeb59cd1897eb7fb8f47de94794d6c3e44c5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enhanced_authentication_enabled", value=enhanced_authentication_enabled, expected_type=type_hints["enhanced_authentication_enabled"])
            check_type(argname="argument trusted_origins", value=trusted_origins, expected_type=type_hints["trusted_origins"])
            check_type(argname="argument v1_allowed", value=v1_allowed, expected_type=type_hints["v1_allowed"])
            check_type(argname="argument v3_allowed", value=v3_allowed, expected_type=type_hints["v3_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if enhanced_authentication_enabled is not None:
            self._values["enhanced_authentication_enabled"] = enhanced_authentication_enabled
        if trusted_origins is not None:
            self._values["trusted_origins"] = trusted_origins
        if v1_allowed is not None:
            self._values["v1_allowed"] = v1_allowed
        if v3_allowed is not None:
            self._values["v3_allowed"] = v3_allowed

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#name BotChannelDirectline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#enabled BotChannelDirectline#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enhanced_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#enhanced_authentication_enabled BotChannelDirectline#enhanced_authentication_enabled}.'''
        result = self._values.get("enhanced_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trusted_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#trusted_origins BotChannelDirectline#trusted_origins}.'''
        result = self._values.get("trusted_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def v1_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#v1_allowed BotChannelDirectline#v1_allowed}.'''
        result = self._values.get("v1_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def v3_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#v3_allowed BotChannelDirectline#v3_allowed}.'''
        result = self._values.get("v3_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BotChannelDirectlineSite(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BotChannelDirectlineSiteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectlineSiteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5549506c43763493a2dfb274ea263d593a2f7eea79a23492759244bae8e33b64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "BotChannelDirectlineSiteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efca954712edc622015323bc9c5632c86d4f65a24719bcee633f1d4841a29ae0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("BotChannelDirectlineSiteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56182ac5e407e633bcfc462b4f3bdc6d47839d4ca9b5143680a016b73d5a3213)
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
            type_hints = typing.get_type_hints(_typecheckingstub__355d686e82ea6c8d47eb822515d5f32d876bebe7f8beb6671de5d37dbabfd7a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64183f5dbe89857993c39f7fd50820cea17226f7f926167048a2367d64df98f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BotChannelDirectlineSite]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BotChannelDirectlineSite]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BotChannelDirectlineSite]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e9ade17f31db4d43ac6c928f8eefcb39fde1523fb87e65bf1f3a40322e7960)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class BotChannelDirectlineSiteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectlineSiteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bd3ec0ea0d27e65df6b36228eafe6a061311c7e3bce2fe8dde6d310f11a7506)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEnhancedAuthenticationEnabled")
    def reset_enhanced_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnhancedAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetTrustedOrigins")
    def reset_trusted_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedOrigins", []))

    @jsii.member(jsii_name="resetV1Allowed")
    def reset_v1_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetV1Allowed", []))

    @jsii.member(jsii_name="resetV3Allowed")
    def reset_v3_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetV3Allowed", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="key2")
    def key2(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key2"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enhancedAuthenticationEnabledInput")
    def enhanced_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enhancedAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedOriginsInput")
    def trusted_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "trustedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="v1AllowedInput")
    def v1_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "v1AllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="v3AllowedInput")
    def v3_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "v3AllowedInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8b69a99be8c6f4accce73bd8b98e54829ae5bb06ed6b2306a84279cd410cf646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="enhancedAuthenticationEnabled")
    def enhanced_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enhancedAuthenticationEnabled"))

    @enhanced_authentication_enabled.setter
    def enhanced_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa6db477c6aaaa8981a42d1d7a87cad2ef0db9a508d69c71691eb911e413885f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enhancedAuthenticationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da199d0593b1cb7477558d59e573d5d363c95ae125d687bdf98dce9e858dcacb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="trustedOrigins")
    def trusted_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "trustedOrigins"))

    @trusted_origins.setter
    def trusted_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d560e87ec4f25a64281391d72759ae4e5151e03adce61fed01d4934b092100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedOrigins", value)

    @builtins.property
    @jsii.member(jsii_name="v1Allowed")
    def v1_allowed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "v1Allowed"))

    @v1_allowed.setter
    def v1_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d0ec2077eeffd2a47585bc04efe1d7608cb9b0ce83ff046ff02d2b7b3673b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "v1Allowed", value)

    @builtins.property
    @jsii.member(jsii_name="v3Allowed")
    def v3_allowed(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "v3Allowed"))

    @v3_allowed.setter
    def v3_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb20f67dd2614a7b6213a21d1730d65796033066203013caa63834a17f57632)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "v3Allowed", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BotChannelDirectlineSite, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BotChannelDirectlineSite, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BotChannelDirectlineSite, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507371872c7e4098059f86aabc9f37dce350ab315a33b083de12c39d07e789f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectlineTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BotChannelDirectlineTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#create BotChannelDirectline#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#delete BotChannelDirectline#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#read BotChannelDirectline#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#update BotChannelDirectline#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3545fca1e50649361a6af76e8ec0fc885f8562972498433d46de528cc955fc03)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#create BotChannelDirectline#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#delete BotChannelDirectline#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#read BotChannelDirectline#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/bot_channel_directline#update BotChannelDirectline#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BotChannelDirectlineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BotChannelDirectlineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.botChannelDirectline.BotChannelDirectlineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0ead6e5aa7ed4a6779eee4c26847eef691d143ef1d12ea251f635e62532e6a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9ac47c55699b83c5855618926ed5b43f555300fe48cb65ec08d5caebfe3782)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__761e4d577cae6820eefd32ee6ffce4415c61d62cc98be6a40b07470d2b1b9827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4acf90e6f928a8a92a210e90f2b9870045207c2ef222cb0bd21c127de671d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530344403f0c3b31e3fe01de3c18e430d571e97fe2601e43b89febb19539b548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[BotChannelDirectlineTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[BotChannelDirectlineTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[BotChannelDirectlineTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1dc9a70ae569c6d9d20c5eade43bd8e0de4b17a8a0480412d1aa7944420970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "BotChannelDirectline",
    "BotChannelDirectlineConfig",
    "BotChannelDirectlineSite",
    "BotChannelDirectlineSiteList",
    "BotChannelDirectlineSiteOutputReference",
    "BotChannelDirectlineTimeouts",
    "BotChannelDirectlineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__85a554247be3636abccb0b50c1ff0b364682b1eba18047e1c079fa82a31f0ed6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    bot_name: builtins.str,
    location: builtins.str,
    resource_group_name: builtins.str,
    site: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BotChannelDirectlineSite, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BotChannelDirectlineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__9863a90e916a8ba243882c5e45f8c4c59f30d9fcb4a9b5b576f546c1dfc46245(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BotChannelDirectlineSite, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ae7adeb335a9fe3a1c77a39c71b42675502686121bdcb034302e0dbf1de94b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5654eafde6fd249e8753cac3ce185b3da3f18ea4690a31632ccd1fa799c3a150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345738b027ab6a7b097660af2dda931f3741512069e0ab224d25ba7a3c28d985(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f8679ec927562389c518753453bd0a7ae518ad94389e95c7897930ef1865d73(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc9370debbf11dd3214cd0e946b7102a67cfe0a31ab850c18fb2a7c9fabe3184(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    bot_name: builtins.str,
    location: builtins.str,
    resource_group_name: builtins.str,
    site: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[BotChannelDirectlineSite, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[BotChannelDirectlineTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3991d622115d672053d64bdbad65aeb59cd1897eb7fb8f47de94794d6c3e44c5(
    *,
    name: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enhanced_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trusted_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    v1_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    v3_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5549506c43763493a2dfb274ea263d593a2f7eea79a23492759244bae8e33b64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efca954712edc622015323bc9c5632c86d4f65a24719bcee633f1d4841a29ae0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56182ac5e407e633bcfc462b4f3bdc6d47839d4ca9b5143680a016b73d5a3213(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355d686e82ea6c8d47eb822515d5f32d876bebe7f8beb6671de5d37dbabfd7a6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64183f5dbe89857993c39f7fd50820cea17226f7f926167048a2367d64df98f0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e9ade17f31db4d43ac6c928f8eefcb39fde1523fb87e65bf1f3a40322e7960(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[BotChannelDirectlineSite]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd3ec0ea0d27e65df6b36228eafe6a061311c7e3bce2fe8dde6d310f11a7506(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b69a99be8c6f4accce73bd8b98e54829ae5bb06ed6b2306a84279cd410cf646(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6db477c6aaaa8981a42d1d7a87cad2ef0db9a508d69c71691eb911e413885f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da199d0593b1cb7477558d59e573d5d363c95ae125d687bdf98dce9e858dcacb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d560e87ec4f25a64281391d72759ae4e5151e03adce61fed01d4934b092100(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d0ec2077eeffd2a47585bc04efe1d7608cb9b0ce83ff046ff02d2b7b3673b48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb20f67dd2614a7b6213a21d1730d65796033066203013caa63834a17f57632(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507371872c7e4098059f86aabc9f37dce350ab315a33b083de12c39d07e789f1(
    value: typing.Optional[typing.Union[BotChannelDirectlineSite, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3545fca1e50649361a6af76e8ec0fc885f8562972498433d46de528cc955fc03(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ead6e5aa7ed4a6779eee4c26847eef691d143ef1d12ea251f635e62532e6a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9ac47c55699b83c5855618926ed5b43f555300fe48cb65ec08d5caebfe3782(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761e4d577cae6820eefd32ee6ffce4415c61d62cc98be6a40b07470d2b1b9827(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4acf90e6f928a8a92a210e90f2b9870045207c2ef222cb0bd21c127de671d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530344403f0c3b31e3fe01de3c18e430d571e97fe2601e43b89febb19539b548(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1dc9a70ae569c6d9d20c5eade43bd8e0de4b17a8a0480412d1aa7944420970(
    value: typing.Optional[typing.Union[BotChannelDirectlineTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
