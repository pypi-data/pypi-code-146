'''
# `okta_network_zone`

Refer to the Terraform Registory for docs: [`okta_network_zone`](https://www.terraform.io/docs/providers/okta/r/network_zone).
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


class NetworkZone(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-okta.networkZone.NetworkZone",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/okta/r/network_zone okta_network_zone}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        asns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamic_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamic_proxy_type: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        usage: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/okta/r/network_zone okta_network_zone} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the Network Zone Resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#name NetworkZone#name}
        :param type: Type of the Network Zone - can either be IP or DYNAMIC only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#type NetworkZone#type}
        :param asns: Format of each array value: a string representation of an ASN numeric value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#asns NetworkZone#asns}
        :param dynamic_locations: Array of locations ISO-3166-1(2). Format code: countryCode OR countryCode-regionCode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#dynamic_locations NetworkZone#dynamic_locations}
        :param dynamic_proxy_type: Type of proxy being controlled by this network zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#dynamic_proxy_type NetworkZone#dynamic_proxy_type}
        :param gateways: Array of values in CIDR/range form depending on the way it's been declared (i.e. CIDR will contain /suffix). Please check API docs for examples. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#gateways NetworkZone#gateways}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#id NetworkZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param proxies: Array of values in CIDR/range form depending on the way it's been declared (i.e. CIDR will contain /suffix). Please check API docs for examples. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#proxies NetworkZone#proxies}
        :param usage: Zone's purpose: POLICY or BLOCKLIST. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#usage NetworkZone#usage}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11530994d160981b2ff12be7e07fa86a2d0e05e26901f9551177f473ae3aa0b9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkZoneConfig(
            name=name,
            type=type,
            asns=asns,
            dynamic_locations=dynamic_locations,
            dynamic_proxy_type=dynamic_proxy_type,
            gateways=gateways,
            id=id,
            proxies=proxies,
            usage=usage,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAsns")
    def reset_asns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAsns", []))

    @jsii.member(jsii_name="resetDynamicLocations")
    def reset_dynamic_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicLocations", []))

    @jsii.member(jsii_name="resetDynamicProxyType")
    def reset_dynamic_proxy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicProxyType", []))

    @jsii.member(jsii_name="resetGateways")
    def reset_gateways(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateways", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProxies")
    def reset_proxies(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxies", []))

    @jsii.member(jsii_name="resetUsage")
    def reset_usage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsage", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="asnsInput")
    def asns_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "asnsInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicLocationsInput")
    def dynamic_locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dynamicLocationsInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicProxyTypeInput")
    def dynamic_proxy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dynamicProxyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewaysInput")
    def gateways_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "gatewaysInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="proxiesInput")
    def proxies_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "proxiesInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="usageInput")
    def usage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usageInput"))

    @builtins.property
    @jsii.member(jsii_name="asns")
    def asns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "asns"))

    @asns.setter
    def asns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b490cabc60a9873b4bed4e175a4f1546b6dc00337f7521b02bd61aeb8bdccfcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "asns", value)

    @builtins.property
    @jsii.member(jsii_name="dynamicLocations")
    def dynamic_locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dynamicLocations"))

    @dynamic_locations.setter
    def dynamic_locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d61f8218a24249ab30f2fa9831ca42ab2b86100b9e2946bf6b63b2a148b9fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicLocations", value)

    @builtins.property
    @jsii.member(jsii_name="dynamicProxyType")
    def dynamic_proxy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dynamicProxyType"))

    @dynamic_proxy_type.setter
    def dynamic_proxy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1db6706376ba595736d5c7792f0ecaacc6d2d877dc556698271cb6e49d5faae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dynamicProxyType", value)

    @builtins.property
    @jsii.member(jsii_name="gateways")
    def gateways(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "gateways"))

    @gateways.setter
    def gateways(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a47c0cc99236e26b25e4c096b95797abbac8b31dd9c243d3392f8e958bf02f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateways", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__847a30b2b25ee8f276eb00627e0c5318d89492e3e99401be7e28cc32a13e8b54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa569d25f16d09e307e9f44161a0327ceeec1ec0e4ca85546150018112f4515b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="proxies")
    def proxies(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "proxies"))

    @proxies.setter
    def proxies(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb7a22ce99aee2a7cf8d2770c335e01de80c8429a111e8553638b1acc8f2299)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxies", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5417d0d33a9cca15fcdc732351fc6f541e9abce6f8725b14b9549de363f8fd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="usage")
    def usage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usage"))

    @usage.setter
    def usage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef6c0063ca86f21773581c9fb4955a783b4e76efa66423be139ab9beb627cbf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usage", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-okta.networkZone.NetworkZoneConfig",
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
        "type": "type",
        "asns": "asns",
        "dynamic_locations": "dynamicLocations",
        "dynamic_proxy_type": "dynamicProxyType",
        "gateways": "gateways",
        "id": "id",
        "proxies": "proxies",
        "usage": "usage",
    },
)
class NetworkZoneConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        type: builtins.str,
        asns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamic_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        dynamic_proxy_type: typing.Optional[builtins.str] = None,
        gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
        usage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the Network Zone Resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#name NetworkZone#name}
        :param type: Type of the Network Zone - can either be IP or DYNAMIC only. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#type NetworkZone#type}
        :param asns: Format of each array value: a string representation of an ASN numeric value. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#asns NetworkZone#asns}
        :param dynamic_locations: Array of locations ISO-3166-1(2). Format code: countryCode OR countryCode-regionCode. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#dynamic_locations NetworkZone#dynamic_locations}
        :param dynamic_proxy_type: Type of proxy being controlled by this network zone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#dynamic_proxy_type NetworkZone#dynamic_proxy_type}
        :param gateways: Array of values in CIDR/range form depending on the way it's been declared (i.e. CIDR will contain /suffix). Please check API docs for examples. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#gateways NetworkZone#gateways}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#id NetworkZone#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param proxies: Array of values in CIDR/range form depending on the way it's been declared (i.e. CIDR will contain /suffix). Please check API docs for examples. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#proxies NetworkZone#proxies}
        :param usage: Zone's purpose: POLICY or BLOCKLIST. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#usage NetworkZone#usage}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2748754e7c183f2d4a03aae642879ec9a371357d5ff8aa15ab870b7bfb3efcf8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument asns", value=asns, expected_type=type_hints["asns"])
            check_type(argname="argument dynamic_locations", value=dynamic_locations, expected_type=type_hints["dynamic_locations"])
            check_type(argname="argument dynamic_proxy_type", value=dynamic_proxy_type, expected_type=type_hints["dynamic_proxy_type"])
            check_type(argname="argument gateways", value=gateways, expected_type=type_hints["gateways"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument proxies", value=proxies, expected_type=type_hints["proxies"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if asns is not None:
            self._values["asns"] = asns
        if dynamic_locations is not None:
            self._values["dynamic_locations"] = dynamic_locations
        if dynamic_proxy_type is not None:
            self._values["dynamic_proxy_type"] = dynamic_proxy_type
        if gateways is not None:
            self._values["gateways"] = gateways
        if id is not None:
            self._values["id"] = id
        if proxies is not None:
            self._values["proxies"] = proxies
        if usage is not None:
            self._values["usage"] = usage

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
        '''Name of the Network Zone Resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#name NetworkZone#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of the Network Zone - can either be IP or DYNAMIC only.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#type NetworkZone#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Format of each array value: a string representation of an ASN numeric value.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#asns NetworkZone#asns}
        '''
        result = self._values.get("asns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dynamic_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Array of locations ISO-3166-1(2). Format code: countryCode OR countryCode-regionCode.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#dynamic_locations NetworkZone#dynamic_locations}
        '''
        result = self._values.get("dynamic_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dynamic_proxy_type(self) -> typing.Optional[builtins.str]:
        '''Type of proxy being controlled by this network zone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#dynamic_proxy_type NetworkZone#dynamic_proxy_type}
        '''
        result = self._values.get("dynamic_proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateways(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Array of values in CIDR/range form depending on the way it's been declared (i.e. CIDR will contain /suffix). Please check API docs for examples.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#gateways NetworkZone#gateways}
        '''
        result = self._values.get("gateways")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#id NetworkZone#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Array of values in CIDR/range form depending on the way it's been declared (i.e. CIDR will contain /suffix). Please check API docs for examples.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#proxies NetworkZone#proxies}
        '''
        result = self._values.get("proxies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def usage(self) -> typing.Optional[builtins.str]:
        '''Zone's purpose: POLICY or BLOCKLIST.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/okta/r/network_zone#usage NetworkZone#usage}
        '''
        result = self._values.get("usage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkZoneConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "NetworkZone",
    "NetworkZoneConfig",
]

publication.publish()

def _typecheckingstub__11530994d160981b2ff12be7e07fa86a2d0e05e26901f9551177f473ae3aa0b9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    type: builtins.str,
    asns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dynamic_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    dynamic_proxy_type: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    usage: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b490cabc60a9873b4bed4e175a4f1546b6dc00337f7521b02bd61aeb8bdccfcc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d61f8218a24249ab30f2fa9831ca42ab2b86100b9e2946bf6b63b2a148b9fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1db6706376ba595736d5c7792f0ecaacc6d2d877dc556698271cb6e49d5faae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a47c0cc99236e26b25e4c096b95797abbac8b31dd9c243d3392f8e958bf02f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__847a30b2b25ee8f276eb00627e0c5318d89492e3e99401be7e28cc32a13e8b54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa569d25f16d09e307e9f44161a0327ceeec1ec0e4ca85546150018112f4515b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb7a22ce99aee2a7cf8d2770c335e01de80c8429a111e8553638b1acc8f2299(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5417d0d33a9cca15fcdc732351fc6f541e9abce6f8725b14b9549de363f8fd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef6c0063ca86f21773581c9fb4955a783b4e76efa66423be139ab9beb627cbf7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2748754e7c183f2d4a03aae642879ec9a371357d5ff8aa15ab870b7bfb3efcf8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    type: builtins.str,
    asns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dynamic_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    dynamic_proxy_type: typing.Optional[builtins.str] = None,
    gateways: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    proxies: typing.Optional[typing.Sequence[builtins.str]] = None,
    usage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
