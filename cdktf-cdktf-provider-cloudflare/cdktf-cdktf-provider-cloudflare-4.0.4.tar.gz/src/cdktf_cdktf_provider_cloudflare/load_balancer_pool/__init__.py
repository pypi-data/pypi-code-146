'''
# `cloudflare_load_balancer_pool`

Refer to the Terraform Registory for docs: [`cloudflare_load_balancer_pool`](https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool).
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


class LoadBalancerPool(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPool",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool cloudflare_load_balancer_pool}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        origins: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOrigins", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[builtins.str] = None,
        check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        latitude: typing.Optional[jsii.Number] = None,
        load_shedding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolLoadShedding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        longitude: typing.Optional[jsii.Number] = None,
        minimum_origins: typing.Optional[jsii.Number] = None,
        monitor: typing.Optional[builtins.str] = None,
        notification_email: typing.Optional[builtins.str] = None,
        origin_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOriginSteering", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool cloudflare_load_balancer_pool} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#name LoadBalancerPool#name}.
        :param origins: origins block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#origins LoadBalancerPool#origins}
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#account_id LoadBalancerPool#account_id}
        :param check_regions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#check_regions LoadBalancerPool#check_regions}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#description LoadBalancerPool#description}.
        :param enabled: Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#enabled LoadBalancerPool#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#id LoadBalancerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param latitude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#latitude LoadBalancerPool#latitude}.
        :param load_shedding: load_shedding block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#load_shedding LoadBalancerPool#load_shedding}
        :param longitude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#longitude LoadBalancerPool#longitude}.
        :param minimum_origins: Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#minimum_origins LoadBalancerPool#minimum_origins}
        :param monitor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#monitor LoadBalancerPool#monitor}.
        :param notification_email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#notification_email LoadBalancerPool#notification_email}.
        :param origin_steering: origin_steering block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#origin_steering LoadBalancerPool#origin_steering}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3b552a4bb4fcad5284c6e7ceae7509e70e4b0d04ba7128f3442cfb122a502e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LoadBalancerPoolConfig(
            name=name,
            origins=origins,
            account_id=account_id,
            check_regions=check_regions,
            description=description,
            enabled=enabled,
            id=id,
            latitude=latitude,
            load_shedding=load_shedding,
            longitude=longitude,
            minimum_origins=minimum_origins,
            monitor=monitor,
            notification_email=notification_email,
            origin_steering=origin_steering,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putLoadShedding")
    def put_load_shedding(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolLoadShedding", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb698d5327f764aa8acbc19db7c6239bc170eae2d63a8c4a1e120a8991ad587)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLoadShedding", [value]))

    @jsii.member(jsii_name="putOrigins")
    def put_origins(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOrigins", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c121b925d3abbb25d2118b367ce0380dff98fa541f5975eed6a6c6fb0cb8408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOrigins", [value]))

    @jsii.member(jsii_name="putOriginSteering")
    def put_origin_steering(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOriginSteering", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db71962bb7581afd4195c4dd862c210f2059f88fd530b209ef3263d64e04d6cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOriginSteering", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetCheckRegions")
    def reset_check_regions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCheckRegions", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLatitude")
    def reset_latitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLatitude", []))

    @jsii.member(jsii_name="resetLoadShedding")
    def reset_load_shedding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadShedding", []))

    @jsii.member(jsii_name="resetLongitude")
    def reset_longitude(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLongitude", []))

    @jsii.member(jsii_name="resetMinimumOrigins")
    def reset_minimum_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumOrigins", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetNotificationEmail")
    def reset_notification_email(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationEmail", []))

    @jsii.member(jsii_name="resetOriginSteering")
    def reset_origin_steering(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginSteering", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="createdOn")
    def created_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdOn"))

    @builtins.property
    @jsii.member(jsii_name="loadShedding")
    def load_shedding(self) -> "LoadBalancerPoolLoadSheddingList":
        return typing.cast("LoadBalancerPoolLoadSheddingList", jsii.get(self, "loadShedding"))

    @builtins.property
    @jsii.member(jsii_name="modifiedOn")
    def modified_on(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modifiedOn"))

    @builtins.property
    @jsii.member(jsii_name="origins")
    def origins(self) -> "LoadBalancerPoolOriginsList":
        return typing.cast("LoadBalancerPoolOriginsList", jsii.get(self, "origins"))

    @builtins.property
    @jsii.member(jsii_name="originSteering")
    def origin_steering(self) -> "LoadBalancerPoolOriginSteeringList":
        return typing.cast("LoadBalancerPoolOriginSteeringList", jsii.get(self, "originSteering"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="checkRegionsInput")
    def check_regions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "checkRegionsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

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
    @jsii.member(jsii_name="latitudeInput")
    def latitude_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "latitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="loadSheddingInput")
    def load_shedding_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolLoadShedding"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolLoadShedding"]]], jsii.get(self, "loadSheddingInput"))

    @builtins.property
    @jsii.member(jsii_name="longitudeInput")
    def longitude_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "longitudeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumOriginsInput")
    def minimum_origins_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationEmailInput")
    def notification_email_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "notificationEmailInput"))

    @builtins.property
    @jsii.member(jsii_name="originsInput")
    def origins_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOrigins"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOrigins"]]], jsii.get(self, "originsInput"))

    @builtins.property
    @jsii.member(jsii_name="originSteeringInput")
    def origin_steering_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOriginSteering"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOriginSteering"]]], jsii.get(self, "originSteeringInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7655c428291295f13b8a8549a5b31763c437d4aa3caa50e2004124d8f279ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="checkRegions")
    def check_regions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "checkRegions"))

    @check_regions.setter
    def check_regions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df46dadbc869b69bf00a93133d03ab47a6c4d110af26188392c7e686ea5d20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "checkRegions", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b2946ee1610ea56c64dcaaf5a28d0a9f99200b04c7eb60a1fb911664745339)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__54fc7e2c8f0ae31a734fad756123843b3b67b2d43b2bb601d2bfc407b6b818fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4b655124a353dd413890541cecc905b50d2d3ed9ccd28cbdc4a8ff3af2f6a72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="latitude")
    def latitude(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "latitude"))

    @latitude.setter
    def latitude(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22267cc88a52d94ca349e2203675b062f62d8fca908e7efb3e19b1e65233223a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latitude", value)

    @builtins.property
    @jsii.member(jsii_name="longitude")
    def longitude(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "longitude"))

    @longitude.setter
    def longitude(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b68c5ed8f3ff9288b85c250a4bc5a9a367c37e24f429991ba75ce5810775d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "longitude", value)

    @builtins.property
    @jsii.member(jsii_name="minimumOrigins")
    def minimum_origins(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumOrigins"))

    @minimum_origins.setter
    def minimum_origins(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680cc5b0e6ad8f2c57288213ada1b7416958798bbd10111e259890ee254cec7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumOrigins", value)

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "monitor"))

    @monitor.setter
    def monitor(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0021e9e6ab33a6755e73e21dd3835cdd1f3e4d1df975065652d7e5e5d970c6af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitor", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__279398a20e435d18cba92073a866ee24e2823f892776ceef2a64e19cbdc257dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="notificationEmail")
    def notification_email(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "notificationEmail"))

    @notification_email.setter
    def notification_email(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68707b6b4521f1ad052dd7715e9b7a481d169aa0e312c7aaaddcd27fcb8bd41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationEmail", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolConfig",
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
        "origins": "origins",
        "account_id": "accountId",
        "check_regions": "checkRegions",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "latitude": "latitude",
        "load_shedding": "loadShedding",
        "longitude": "longitude",
        "minimum_origins": "minimumOrigins",
        "monitor": "monitor",
        "notification_email": "notificationEmail",
        "origin_steering": "originSteering",
    },
)
class LoadBalancerPoolConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        origins: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOrigins", typing.Dict[builtins.str, typing.Any]]]],
        account_id: typing.Optional[builtins.str] = None,
        check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        latitude: typing.Optional[jsii.Number] = None,
        load_shedding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolLoadShedding", typing.Dict[builtins.str, typing.Any]]]]] = None,
        longitude: typing.Optional[jsii.Number] = None,
        minimum_origins: typing.Optional[jsii.Number] = None,
        monitor: typing.Optional[builtins.str] = None,
        notification_email: typing.Optional[builtins.str] = None,
        origin_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOriginSteering", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#name LoadBalancerPool#name}.
        :param origins: origins block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#origins LoadBalancerPool#origins}
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#account_id LoadBalancerPool#account_id}
        :param check_regions: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#check_regions LoadBalancerPool#check_regions}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#description LoadBalancerPool#description}.
        :param enabled: Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#enabled LoadBalancerPool#enabled}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#id LoadBalancerPool#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param latitude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#latitude LoadBalancerPool#latitude}.
        :param load_shedding: load_shedding block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#load_shedding LoadBalancerPool#load_shedding}
        :param longitude: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#longitude LoadBalancerPool#longitude}.
        :param minimum_origins: Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#minimum_origins LoadBalancerPool#minimum_origins}
        :param monitor: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#monitor LoadBalancerPool#monitor}.
        :param notification_email: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#notification_email LoadBalancerPool#notification_email}.
        :param origin_steering: origin_steering block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#origin_steering LoadBalancerPool#origin_steering}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692be5c2b081be7d23745f651c1b30e04c41009d4b1d5588cec705f651d298f9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument origins", value=origins, expected_type=type_hints["origins"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument check_regions", value=check_regions, expected_type=type_hints["check_regions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
            check_type(argname="argument load_shedding", value=load_shedding, expected_type=type_hints["load_shedding"])
            check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            check_type(argname="argument minimum_origins", value=minimum_origins, expected_type=type_hints["minimum_origins"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument notification_email", value=notification_email, expected_type=type_hints["notification_email"])
            check_type(argname="argument origin_steering", value=origin_steering, expected_type=type_hints["origin_steering"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "origins": origins,
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
        if check_regions is not None:
            self._values["check_regions"] = check_regions
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if latitude is not None:
            self._values["latitude"] = latitude
        if load_shedding is not None:
            self._values["load_shedding"] = load_shedding
        if longitude is not None:
            self._values["longitude"] = longitude
        if minimum_origins is not None:
            self._values["minimum_origins"] = minimum_origins
        if monitor is not None:
            self._values["monitor"] = monitor
        if notification_email is not None:
            self._values["notification_email"] = notification_email
        if origin_steering is not None:
            self._values["origin_steering"] = origin_steering

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#name LoadBalancerPool#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origins(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOrigins"]]:
        '''origins block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#origins LoadBalancerPool#origins}
        '''
        result = self._values.get("origins")
        assert result is not None, "Required property 'origins' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOrigins"]], result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#account_id LoadBalancerPool#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#check_regions LoadBalancerPool#check_regions}.'''
        result = self._values.get("check_regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#description LoadBalancerPool#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#enabled LoadBalancerPool#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#id LoadBalancerPool#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def latitude(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#latitude LoadBalancerPool#latitude}.'''
        result = self._values.get("latitude")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def load_shedding(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolLoadShedding"]]]:
        '''load_shedding block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#load_shedding LoadBalancerPool#load_shedding}
        '''
        result = self._values.get("load_shedding")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolLoadShedding"]]], result)

    @builtins.property
    def longitude(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#longitude LoadBalancerPool#longitude}.'''
        result = self._values.get("longitude")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_origins(self) -> typing.Optional[jsii.Number]:
        '''Defaults to ``1``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#minimum_origins LoadBalancerPool#minimum_origins}
        '''
        result = self._values.get("minimum_origins")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def monitor(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#monitor LoadBalancerPool#monitor}.'''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_email(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#notification_email LoadBalancerPool#notification_email}.'''
        result = self._values.get("notification_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin_steering(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOriginSteering"]]]:
        '''origin_steering block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#origin_steering LoadBalancerPool#origin_steering}
        '''
        result = self._values.get("origin_steering")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOriginSteering"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerPoolConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolLoadShedding",
    jsii_struct_bases=[],
    name_mapping={
        "default_percent": "defaultPercent",
        "default_policy": "defaultPolicy",
        "session_percent": "sessionPercent",
        "session_policy": "sessionPolicy",
    },
)
class LoadBalancerPoolLoadShedding:
    def __init__(
        self,
        *,
        default_percent: typing.Optional[jsii.Number] = None,
        default_policy: typing.Optional[builtins.str] = None,
        session_percent: typing.Optional[jsii.Number] = None,
        session_policy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_percent: Percent of traffic to shed 0 - 100. Defaults to ``0``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#default_percent LoadBalancerPool#default_percent}
        :param default_policy: Method of shedding traffic. Available values: ``, ``hash``, ``random``. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#default_policy LoadBalancerPool#default_policy}
        :param session_percent: Percent of session traffic to shed 0 - 100. Defaults to ``0``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#session_percent LoadBalancerPool#session_percent}
        :param session_policy: Method of shedding traffic. Available values: ``, ``hash``. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#session_policy LoadBalancerPool#session_policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715bb646fc17ccd60bd6a750e5f890dfa8638411709d825bbab4a7257d205450)
            check_type(argname="argument default_percent", value=default_percent, expected_type=type_hints["default_percent"])
            check_type(argname="argument default_policy", value=default_policy, expected_type=type_hints["default_policy"])
            check_type(argname="argument session_percent", value=session_percent, expected_type=type_hints["session_percent"])
            check_type(argname="argument session_policy", value=session_policy, expected_type=type_hints["session_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_percent is not None:
            self._values["default_percent"] = default_percent
        if default_policy is not None:
            self._values["default_policy"] = default_policy
        if session_percent is not None:
            self._values["session_percent"] = session_percent
        if session_policy is not None:
            self._values["session_policy"] = session_policy

    @builtins.property
    def default_percent(self) -> typing.Optional[jsii.Number]:
        '''Percent of traffic to shed 0 - 100. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#default_percent LoadBalancerPool#default_percent}
        '''
        result = self._values.get("default_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def default_policy(self) -> typing.Optional[builtins.str]:
        '''Method of shedding traffic. Available values: ``, ``hash``, ``random``. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#default_policy LoadBalancerPool#default_policy}
        '''
        result = self._values.get("default_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_percent(self) -> typing.Optional[jsii.Number]:
        '''Percent of session traffic to shed 0 - 100. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#session_percent LoadBalancerPool#session_percent}
        '''
        result = self._values.get("session_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def session_policy(self) -> typing.Optional[builtins.str]:
        '''Method of shedding traffic. Available values: ``, ``hash``. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#session_policy LoadBalancerPool#session_policy}
        '''
        result = self._values.get("session_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerPoolLoadShedding(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerPoolLoadSheddingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolLoadSheddingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7a64679becf4602f7a9d17aeb124b847022bd3f94d7016a87cf678778ca8003)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerPoolLoadSheddingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c7965fab3b789e9a2462a6765e8877cabd3c67bc2871d11306d24948e53021)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerPoolLoadSheddingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe405b331a975b79032fd9be595e59d4da03d346297656a977becdc08e7abd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9eb82eca207607e2682cc5c69a32fee1d66acbd9863472787df33c965b08ea9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7db4e09553ca92f520d18639c6dd0e74b744593abc404e54a70c4d4217a6895c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolLoadShedding]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolLoadShedding]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolLoadShedding]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f856f44f41aafa523c0a312baa4169f4348387fdb53239ad691c53a30af182)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerPoolLoadSheddingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolLoadSheddingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__216363376007d395389870494823e1b7ea92cc0e6909469dd60dcf0c590f8b9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefaultPercent")
    def reset_default_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPercent", []))

    @jsii.member(jsii_name="resetDefaultPolicy")
    def reset_default_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultPolicy", []))

    @jsii.member(jsii_name="resetSessionPercent")
    def reset_session_percent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionPercent", []))

    @jsii.member(jsii_name="resetSessionPolicy")
    def reset_session_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSessionPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="defaultPercentInput")
    def default_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPolicyInput")
    def default_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionPercentInput")
    def session_percent_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sessionPercentInput"))

    @builtins.property
    @jsii.member(jsii_name="sessionPolicyInput")
    def session_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sessionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultPercent")
    def default_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultPercent"))

    @default_percent.setter
    def default_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f687fc7787be4b00c893df736871340a1cfa4c8754f5395541bad06c11092c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPercent", value)

    @builtins.property
    @jsii.member(jsii_name="defaultPolicy")
    def default_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultPolicy"))

    @default_policy.setter
    def default_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6ac1cc657cb03727e9475fe58f521ad724f021e9a686ab395c3ce5e172c260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="sessionPercent")
    def session_percent(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sessionPercent"))

    @session_percent.setter
    def session_percent(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0eda545ddbf8d12c6b5fa423f48997ddd255ddb77ba59b1b3ea6684578af6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionPercent", value)

    @builtins.property
    @jsii.member(jsii_name="sessionPolicy")
    def session_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sessionPolicy"))

    @session_policy.setter
    def session_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f300582bfd2527b41f89748513f616ca3f392344544f7fac53380c18b70a7ab2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sessionPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerPoolLoadShedding, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerPoolLoadShedding, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerPoolLoadShedding, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdb48881143b7edfa84451d97f301d404fa8b4787eafb1bab0f5ca773ee75ddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginSteering",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy"},
)
class LoadBalancerPoolOriginSteering:
    def __init__(self, *, policy: typing.Optional[builtins.str] = None) -> None:
        '''
        :param policy: Origin steering policy to be used. Available values: ``, ``hash``, ``random``. Defaults to ``random``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#policy LoadBalancerPool#policy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c72c8eb26ee3b133606b600532da2142af1e8f1791717295c41c7778ed236dc)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''Origin steering policy to be used. Available values: ``, ``hash``, ``random``. Defaults to ``random``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#policy LoadBalancerPool#policy}
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerPoolOriginSteering(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerPoolOriginSteeringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginSteeringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e37cac542d2c0d8023b630a49613447cee327de6a2d93a5a5f8b4afb84123b0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LoadBalancerPoolOriginSteeringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36bf8d8edaea7512ea0e6fcbb93b528b90eaf1bcc8fa8da333cafa8cf2613f8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerPoolOriginSteeringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a775b01a7c5aee3259d0b6edb6bc39fc4506afed8cda6bc22a4f8a5624a23221)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f967d84c76bc6a5398f0523da40d143bba5fc6509400acbecdc8825a1160ec0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c49af827c230ee4784cf965d658dcc102e6bd45838598becf36148597e0f3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginSteering]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginSteering]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginSteering]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5283355cf4009e494c115d36faf79b693665a6f82e6b1b7424fbd0ea3691e4c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerPoolOriginSteeringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginSteeringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d75ba71413daca192bad8a16102726dda08fd5a033408ea85dbd3fe05d383f62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPolicy")
    def reset_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="policyInput")
    def policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyInput"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e0a410d1ebd8ccc9fb5aa24f64a14f7b813c0e25e637b4c0b727e3df2ae1c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerPoolOriginSteering, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerPoolOriginSteering, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerPoolOriginSteering, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221251a3706dee0b19d8623c6786f866e55a00ef603e10c85185b5aa9d9b0766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOrigins",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "name": "name",
        "enabled": "enabled",
        "header": "header",
        "weight": "weight",
    },
)
class LoadBalancerPoolOrigins:
    def __init__(
        self,
        *,
        address: builtins.str,
        name: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LoadBalancerPoolOriginsHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param address: The IP address (IPv4 or IPv6) of the origin, or the publicly addressable hostname. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#address LoadBalancerPool#address}
        :param name: A human-identifiable name for the origin. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#name LoadBalancerPool#name}
        :param enabled: Whether this origin is enabled. Disabled origins will not receive traffic and are excluded from health checks. Defaults to ``true``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#enabled LoadBalancerPool#enabled}
        :param header: header block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#header LoadBalancerPool#header}
        :param weight: The weight (0.01 - 1.00) of this origin, relative to other origins in the pool. Equal values mean equal weighting. A weight of 0 means traffic will not be sent to this origin, but health is still checked. Defaults to ``1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#weight LoadBalancerPool#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fa2420bd66ef218996632a7196f195d33fe95eaa8e0c6af6e1a3921395cd41b)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "address": address,
            "name": name,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if header is not None:
            self._values["header"] = header
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def address(self) -> builtins.str:
        '''The IP address (IPv4 or IPv6) of the origin, or the publicly addressable hostname.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#address LoadBalancerPool#address}
        '''
        result = self._values.get("address")
        assert result is not None, "Required property 'address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A human-identifiable name for the origin.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#name LoadBalancerPool#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether this origin is enabled.

        Disabled origins will not receive traffic and are excluded from health checks. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#enabled LoadBalancerPool#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOriginsHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#header LoadBalancerPool#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LoadBalancerPoolOriginsHeader"]]], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''The weight (0.01 - 1.00) of this origin, relative to other origins in the pool. Equal values mean equal weighting. A weight of 0 means traffic will not be sent to this origin, but health is still checked. Defaults to ``1``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#weight LoadBalancerPool#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerPoolOrigins(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginsHeader",
    jsii_struct_bases=[],
    name_mapping={"header": "header", "values": "values"},
)
class LoadBalancerPoolOriginsHeader:
    def __init__(
        self,
        *,
        header: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param header: HTTP Header name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#header LoadBalancerPool#header}
        :param values: Values for the HTTP headers. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#values LoadBalancerPool#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__341602971ceb0c2249b031606eb62902eaca9fb381b7141e848415dfb8c2272c)
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header": header,
            "values": values,
        }

    @builtins.property
    def header(self) -> builtins.str:
        '''HTTP Header name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#header LoadBalancerPool#header}
        '''
        result = self._values.get("header")
        assert result is not None, "Required property 'header' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Values for the HTTP headers.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/load_balancer_pool#values LoadBalancerPool#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerPoolOriginsHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LoadBalancerPoolOriginsHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginsHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5b4ebbc0c3f2532c821eabee90180e42f2c7fcf8291601e6a20030620f5a29d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerPoolOriginsHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa88864fe0f82d9b1e4ed5b3d2402fcc5799222b4394b3d418e4ede77fd53845)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerPoolOriginsHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__576f3f27feb32cdbcc4c17b3df48a5341e86a968f5796ada05b596611c1f5298)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84397d53386cc12dfb4dec0bb20fab4841d095026300e1abb1fa9b417b4cdb18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c788866d2a47b164782f2545d834e6940adebb1a45d70b4aac52b84e1e81f20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginsHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginsHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginsHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097ed63f0844c27e11c564f88a54c373b4cbba00e0099e93f3c62c1303178a21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerPoolOriginsHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginsHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52e430333cb1cccb5662d819056cf5ebb3fce0ccb0db3b2b07da7e7f71f85192)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "header"))

    @header.setter
    def header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7f6b313a5364665508788f08405ab8528ca407810894866fcf7613a92f981cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "header", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e627bb12094bb715a2b55d6577bd9869b7e5e0f951da3b7aa0a11e2c55ce29b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerPoolOriginsHeader, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerPoolOriginsHeader, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerPoolOriginsHeader, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa25a684f7465ec5a3d108a975bfc1719f9ac2a525d86c74a7decdd33332c34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerPoolOriginsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b89cf595bdc66572070fd0ac3bf46db245adb30c940ea9e23b30c31f8800297)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "LoadBalancerPoolOriginsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075031e82b917393d5ec53c8833bb3d0decd5c9cad76d85a9296c225edba8bb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LoadBalancerPoolOriginsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efa4d8c3ec1c3cf331ccb9c7bba7c4777bef5c9114d5204e6794d1e373b5cf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8327a70d3f6860970bf1f55b0b1391f066771a7136faf4bf0f2da27e8de0f555)
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
            type_hints = typing.get_type_hints(_typecheckingstub__677d4893c66570f3d5813e097d63866c7203c4cf298e77c84aa1eace2800ba65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOrigins]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOrigins]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOrigins]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b301155d9d8ac8030420756216d87f19d458db58ba95091b2e4b6a83198eef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class LoadBalancerPoolOriginsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.loadBalancerPool.LoadBalancerPoolOriginsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea9a95c81bf62ddf8299ca0c8e3f3c110498404b905b5c61881b66c681dd3911)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOriginsHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce839b3789d0a70a4e6838eeaba26a406e354dd20f5236f4d21a2895d13e253e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(self) -> LoadBalancerPoolOriginsHeaderList:
        return typing.cast(LoadBalancerPoolOriginsHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginsHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginsHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e93178082349f1ff50ea8227dcf6d8c732258853a13c0ba3749d774b7032a19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__9ecd93a4e787115ed3f52bb1be6341f9f785c557638452028f00ee74407650a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a5fc1fbede8d1b9fd8b05a385a204d60c667f10fa373c9de7f857524991c55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c070f1d9d759410d13a999a3aec55880a13d209243be37c7988ed2809a29fc4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[LoadBalancerPoolOrigins, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[LoadBalancerPoolOrigins, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[LoadBalancerPoolOrigins, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afdb8a3dba053cd228e17329b27bc8a62a0a971ba48bc8b3364ff9c690cee09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "LoadBalancerPool",
    "LoadBalancerPoolConfig",
    "LoadBalancerPoolLoadShedding",
    "LoadBalancerPoolLoadSheddingList",
    "LoadBalancerPoolLoadSheddingOutputReference",
    "LoadBalancerPoolOriginSteering",
    "LoadBalancerPoolOriginSteeringList",
    "LoadBalancerPoolOriginSteeringOutputReference",
    "LoadBalancerPoolOrigins",
    "LoadBalancerPoolOriginsHeader",
    "LoadBalancerPoolOriginsHeaderList",
    "LoadBalancerPoolOriginsHeaderOutputReference",
    "LoadBalancerPoolOriginsList",
    "LoadBalancerPoolOriginsOutputReference",
]

publication.publish()

def _typecheckingstub__0b3b552a4bb4fcad5284c6e7ceae7509e70e4b0d04ba7128f3442cfb122a502e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    origins: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOrigins, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[builtins.str] = None,
    check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    latitude: typing.Optional[jsii.Number] = None,
    load_shedding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolLoadShedding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    longitude: typing.Optional[jsii.Number] = None,
    minimum_origins: typing.Optional[jsii.Number] = None,
    monitor: typing.Optional[builtins.str] = None,
    notification_email: typing.Optional[builtins.str] = None,
    origin_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOriginSteering, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__3cb698d5327f764aa8acbc19db7c6239bc170eae2d63a8c4a1e120a8991ad587(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolLoadShedding, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c121b925d3abbb25d2118b367ce0380dff98fa541f5975eed6a6c6fb0cb8408(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOrigins, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db71962bb7581afd4195c4dd862c210f2059f88fd530b209ef3263d64e04d6cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOriginSteering, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7655c428291295f13b8a8549a5b31763c437d4aa3caa50e2004124d8f279ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df46dadbc869b69bf00a93133d03ab47a6c4d110af26188392c7e686ea5d20e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b2946ee1610ea56c64dcaaf5a28d0a9f99200b04c7eb60a1fb911664745339(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fc7e2c8f0ae31a734fad756123843b3b67b2d43b2bb601d2bfc407b6b818fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4b655124a353dd413890541cecc905b50d2d3ed9ccd28cbdc4a8ff3af2f6a72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22267cc88a52d94ca349e2203675b062f62d8fca908e7efb3e19b1e65233223a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b68c5ed8f3ff9288b85c250a4bc5a9a367c37e24f429991ba75ce5810775d5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680cc5b0e6ad8f2c57288213ada1b7416958798bbd10111e259890ee254cec7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0021e9e6ab33a6755e73e21dd3835cdd1f3e4d1df975065652d7e5e5d970c6af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279398a20e435d18cba92073a866ee24e2823f892776ceef2a64e19cbdc257dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68707b6b4521f1ad052dd7715e9b7a481d169aa0e312c7aaaddcd27fcb8bd41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692be5c2b081be7d23745f651c1b30e04c41009d4b1d5588cec705f651d298f9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    origins: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOrigins, typing.Dict[builtins.str, typing.Any]]]],
    account_id: typing.Optional[builtins.str] = None,
    check_regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    latitude: typing.Optional[jsii.Number] = None,
    load_shedding: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolLoadShedding, typing.Dict[builtins.str, typing.Any]]]]] = None,
    longitude: typing.Optional[jsii.Number] = None,
    minimum_origins: typing.Optional[jsii.Number] = None,
    monitor: typing.Optional[builtins.str] = None,
    notification_email: typing.Optional[builtins.str] = None,
    origin_steering: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOriginSteering, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715bb646fc17ccd60bd6a750e5f890dfa8638411709d825bbab4a7257d205450(
    *,
    default_percent: typing.Optional[jsii.Number] = None,
    default_policy: typing.Optional[builtins.str] = None,
    session_percent: typing.Optional[jsii.Number] = None,
    session_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a64679becf4602f7a9d17aeb124b847022bd3f94d7016a87cf678778ca8003(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c7965fab3b789e9a2462a6765e8877cabd3c67bc2871d11306d24948e53021(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe405b331a975b79032fd9be595e59d4da03d346297656a977becdc08e7abd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb82eca207607e2682cc5c69a32fee1d66acbd9863472787df33c965b08ea9b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db4e09553ca92f520d18639c6dd0e74b744593abc404e54a70c4d4217a6895c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f856f44f41aafa523c0a312baa4169f4348387fdb53239ad691c53a30af182(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolLoadShedding]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__216363376007d395389870494823e1b7ea92cc0e6909469dd60dcf0c590f8b9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f687fc7787be4b00c893df736871340a1cfa4c8754f5395541bad06c11092c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6ac1cc657cb03727e9475fe58f521ad724f021e9a686ab395c3ce5e172c260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0eda545ddbf8d12c6b5fa423f48997ddd255ddb77ba59b1b3ea6684578af6d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f300582bfd2527b41f89748513f616ca3f392344544f7fac53380c18b70a7ab2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdb48881143b7edfa84451d97f301d404fa8b4787eafb1bab0f5ca773ee75ddd(
    value: typing.Optional[typing.Union[LoadBalancerPoolLoadShedding, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c72c8eb26ee3b133606b600532da2142af1e8f1791717295c41c7778ed236dc(
    *,
    policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e37cac542d2c0d8023b630a49613447cee327de6a2d93a5a5f8b4afb84123b0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36bf8d8edaea7512ea0e6fcbb93b528b90eaf1bcc8fa8da333cafa8cf2613f8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a775b01a7c5aee3259d0b6edb6bc39fc4506afed8cda6bc22a4f8a5624a23221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f967d84c76bc6a5398f0523da40d143bba5fc6509400acbecdc8825a1160ec0c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c49af827c230ee4784cf965d658dcc102e6bd45838598becf36148597e0f3d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5283355cf4009e494c115d36faf79b693665a6f82e6b1b7424fbd0ea3691e4c8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginSteering]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75ba71413daca192bad8a16102726dda08fd5a033408ea85dbd3fe05d383f62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e0a410d1ebd8ccc9fb5aa24f64a14f7b813c0e25e637b4c0b727e3df2ae1c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221251a3706dee0b19d8623c6786f866e55a00ef603e10c85185b5aa9d9b0766(
    value: typing.Optional[typing.Union[LoadBalancerPoolOriginSteering, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fa2420bd66ef218996632a7196f195d33fe95eaa8e0c6af6e1a3921395cd41b(
    *,
    address: builtins.str,
    name: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOriginsHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__341602971ceb0c2249b031606eb62902eaca9fb381b7141e848415dfb8c2272c(
    *,
    header: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b4ebbc0c3f2532c821eabee90180e42f2c7fcf8291601e6a20030620f5a29d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa88864fe0f82d9b1e4ed5b3d2402fcc5799222b4394b3d418e4ede77fd53845(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576f3f27feb32cdbcc4c17b3df48a5341e86a968f5796ada05b596611c1f5298(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84397d53386cc12dfb4dec0bb20fab4841d095026300e1abb1fa9b417b4cdb18(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c788866d2a47b164782f2545d834e6940adebb1a45d70b4aac52b84e1e81f20f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097ed63f0844c27e11c564f88a54c373b4cbba00e0099e93f3c62c1303178a21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOriginsHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e430333cb1cccb5662d819056cf5ebb3fce0ccb0db3b2b07da7e7f71f85192(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f6b313a5364665508788f08405ab8528ca407810894866fcf7613a92f981cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e627bb12094bb715a2b55d6577bd9869b7e5e0f951da3b7aa0a11e2c55ce29b1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa25a684f7465ec5a3d108a975bfc1719f9ac2a525d86c74a7decdd33332c34b(
    value: typing.Optional[typing.Union[LoadBalancerPoolOriginsHeader, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b89cf595bdc66572070fd0ac3bf46db245adb30c940ea9e23b30c31f8800297(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075031e82b917393d5ec53c8833bb3d0decd5c9cad76d85a9296c225edba8bb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efa4d8c3ec1c3cf331ccb9c7bba7c4777bef5c9114d5204e6794d1e373b5cf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8327a70d3f6860970bf1f55b0b1391f066771a7136faf4bf0f2da27e8de0f555(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677d4893c66570f3d5813e097d63866c7203c4cf298e77c84aa1eace2800ba65(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b301155d9d8ac8030420756216d87f19d458db58ba95091b2e4b6a83198eef2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LoadBalancerPoolOrigins]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea9a95c81bf62ddf8299ca0c8e3f3c110498404b905b5c61881b66c681dd3911(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce839b3789d0a70a4e6838eeaba26a406e354dd20f5236f4d21a2895d13e253e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LoadBalancerPoolOriginsHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e93178082349f1ff50ea8227dcf6d8c732258853a13c0ba3749d774b7032a19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ecd93a4e787115ed3f52bb1be6341f9f785c557638452028f00ee74407650a8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a5fc1fbede8d1b9fd8b05a385a204d60c667f10fa373c9de7f857524991c55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c070f1d9d759410d13a999a3aec55880a13d209243be37c7988ed2809a29fc4b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afdb8a3dba053cd228e17329b27bc8a62a0a971ba48bc8b3364ff9c690cee09(
    value: typing.Optional[typing.Union[LoadBalancerPoolOrigins, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
