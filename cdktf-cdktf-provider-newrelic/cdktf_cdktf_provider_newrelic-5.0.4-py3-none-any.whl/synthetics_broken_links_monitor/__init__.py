'''
# `newrelic_synthetics_broken_links_monitor`

Refer to the Terraform Registory for docs: [`newrelic_synthetics_broken_links_monitor`](https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor).
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


class SyntheticsBrokenLinksMonitor(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsBrokenLinksMonitor.SyntheticsBrokenLinksMonitor",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor newrelic_synthetics_broken_links_monitor}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        period: builtins.str,
        status: builtins.str,
        uri: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        locations_private: typing.Optional[typing.Sequence[builtins.str]] = None,
        locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsBrokenLinksMonitorTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor newrelic_synthetics_broken_links_monitor} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The title of this monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#name SyntheticsBrokenLinksMonitor#name}
        :param period: The interval at which this monitor should run. Valid values are EVERY_MINUTE, EVERY_5_MINUTES, EVERY_10_MINUTES, EVERY_15_MINUTES, EVERY_30_MINUTES, EVERY_HOUR, EVERY_6_HOURS, EVERY_12_HOURS, or EVERY_DAY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#period SyntheticsBrokenLinksMonitor#period}
        :param status: The monitor status (i.e. ENABLED, MUTED, DISABLED). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#status SyntheticsBrokenLinksMonitor#status}
        :param uri: The URI the monitor runs against. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#uri SyntheticsBrokenLinksMonitor#uri}
        :param account_id: ID of the newrelic account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#account_id SyntheticsBrokenLinksMonitor#account_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#id SyntheticsBrokenLinksMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param locations_private: List private location GUIDs for which the monitor will run. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#locations_private SyntheticsBrokenLinksMonitor#locations_private}
        :param locations_public: Publicly available location names in which the monitor will run. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#locations_public SyntheticsBrokenLinksMonitor#locations_public}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#tag SyntheticsBrokenLinksMonitor#tag}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2233e98ff17d2c8083c26d18d3e8339dcb60aa5fe5125e14ef197fd9ec2a2e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SyntheticsBrokenLinksMonitorConfig(
            name=name,
            period=period,
            status=status,
            uri=uri,
            account_id=account_id,
            id=id,
            locations_private=locations_private,
            locations_public=locations_public,
            tag=tag,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTag")
    def put_tag(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsBrokenLinksMonitorTag", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d1c9ee0fda289c0d63c70c792839d33a28ca78d736ca8e1ae40abd2097c22b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTag", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocationsPrivate")
    def reset_locations_private(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationsPrivate", []))

    @jsii.member(jsii_name="resetLocationsPublic")
    def reset_locations_public(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocationsPublic", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

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
    @jsii.member(jsii_name="tag")
    def tag(self) -> "SyntheticsBrokenLinksMonitorTagList":
        return typing.cast("SyntheticsBrokenLinksMonitorTagList", jsii.get(self, "tag"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsPrivateInput")
    def locations_private_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsPrivateInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsPublicInput")
    def locations_public_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsPublicInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="periodInput")
    def period_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "periodInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsBrokenLinksMonitorTag"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsBrokenLinksMonitorTag"]]], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d1a36de68e78e8d401ef03a72de8f0a1d039e19f3195b95616105bce591f8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52afa541fafcf12601e896db37ce732c092e91118431c5657712f6c90c45f402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="locationsPrivate")
    def locations_private(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locationsPrivate"))

    @locations_private.setter
    def locations_private(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d4377377c4a2e9d670f2f776f6b8b256b14362a4a92d7f1b656a7c3191136c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationsPrivate", value)

    @builtins.property
    @jsii.member(jsii_name="locationsPublic")
    def locations_public(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locationsPublic"))

    @locations_public.setter
    def locations_public(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6b7474baa4d08bcae0c97c01168f968d4ef7a5a16d350dea525ccc4147a969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationsPublic", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb09e7308446bc5172c42d1a18e85d9237275c8f07735b5dfb09d3eb7c0c0d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="period")
    def period(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "period"))

    @period.setter
    def period(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb8937aef7efaa17435ef58ae7a0bdef1139ae32b7a275b3ab3191951e259183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "period", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95d98684fbe8edbc701e8b24febb98cfbc7ccbb128e344d380adb7de5aa9bf13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f99733eec19df4d538a9d65e4a8fabe66d1a07433c86ed41939684bc4d2a01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.syntheticsBrokenLinksMonitor.SyntheticsBrokenLinksMonitorConfig",
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
        "period": "period",
        "status": "status",
        "uri": "uri",
        "account_id": "accountId",
        "id": "id",
        "locations_private": "locationsPrivate",
        "locations_public": "locationsPublic",
        "tag": "tag",
    },
)
class SyntheticsBrokenLinksMonitorConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        period: builtins.str,
        status: builtins.str,
        uri: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        locations_private: typing.Optional[typing.Sequence[builtins.str]] = None,
        locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
        tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SyntheticsBrokenLinksMonitorTag", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The title of this monitor. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#name SyntheticsBrokenLinksMonitor#name}
        :param period: The interval at which this monitor should run. Valid values are EVERY_MINUTE, EVERY_5_MINUTES, EVERY_10_MINUTES, EVERY_15_MINUTES, EVERY_30_MINUTES, EVERY_HOUR, EVERY_6_HOURS, EVERY_12_HOURS, or EVERY_DAY. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#period SyntheticsBrokenLinksMonitor#period}
        :param status: The monitor status (i.e. ENABLED, MUTED, DISABLED). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#status SyntheticsBrokenLinksMonitor#status}
        :param uri: The URI the monitor runs against. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#uri SyntheticsBrokenLinksMonitor#uri}
        :param account_id: ID of the newrelic account. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#account_id SyntheticsBrokenLinksMonitor#account_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#id SyntheticsBrokenLinksMonitor#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param locations_private: List private location GUIDs for which the monitor will run. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#locations_private SyntheticsBrokenLinksMonitor#locations_private}
        :param locations_public: Publicly available location names in which the monitor will run. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#locations_public SyntheticsBrokenLinksMonitor#locations_public}
        :param tag: tag block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#tag SyntheticsBrokenLinksMonitor#tag}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfacfc699fbb3711bcb51cf8115ec9a138ada62e4a8c05f6354b9d28f63a81b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument period", value=period, expected_type=type_hints["period"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument locations_private", value=locations_private, expected_type=type_hints["locations_private"])
            check_type(argname="argument locations_public", value=locations_public, expected_type=type_hints["locations_public"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "period": period,
            "status": status,
            "uri": uri,
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
        if locations_private is not None:
            self._values["locations_private"] = locations_private
        if locations_public is not None:
            self._values["locations_public"] = locations_public
        if tag is not None:
            self._values["tag"] = tag

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
        '''The title of this monitor.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#name SyntheticsBrokenLinksMonitor#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def period(self) -> builtins.str:
        '''The interval at which this monitor should run.

        Valid values are EVERY_MINUTE, EVERY_5_MINUTES, EVERY_10_MINUTES, EVERY_15_MINUTES, EVERY_30_MINUTES, EVERY_HOUR, EVERY_6_HOURS, EVERY_12_HOURS, or EVERY_DAY.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#period SyntheticsBrokenLinksMonitor#period}
        '''
        result = self._values.get("period")
        assert result is not None, "Required property 'period' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status(self) -> builtins.str:
        '''The monitor status (i.e. ENABLED, MUTED, DISABLED).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#status SyntheticsBrokenLinksMonitor#status}
        '''
        result = self._values.get("status")
        assert result is not None, "Required property 'status' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''The URI the monitor runs against.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#uri SyntheticsBrokenLinksMonitor#uri}
        '''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''ID of the newrelic account.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#account_id SyntheticsBrokenLinksMonitor#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#id SyntheticsBrokenLinksMonitor#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def locations_private(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List private location GUIDs for which the monitor will run.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#locations_private SyntheticsBrokenLinksMonitor#locations_private}
        '''
        result = self._values.get("locations_private")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def locations_public(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Publicly available location names in which the monitor will run.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#locations_public SyntheticsBrokenLinksMonitor#locations_public}
        '''
        result = self._values.get("locations_public")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tag(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsBrokenLinksMonitorTag"]]]:
        '''tag block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#tag SyntheticsBrokenLinksMonitor#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SyntheticsBrokenLinksMonitorTag"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsBrokenLinksMonitorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.syntheticsBrokenLinksMonitor.SyntheticsBrokenLinksMonitorTag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "values": "values"},
)
class SyntheticsBrokenLinksMonitorTag:
    def __init__(
        self,
        *,
        key: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param key: Name of the tag key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#key SyntheticsBrokenLinksMonitor#key}
        :param values: Values associated with the tag key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#values SyntheticsBrokenLinksMonitor#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304518ca688e90c984178dfa34d1a80a13c3b363f47cf515ce7dc4a1166ae900)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "values": values,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Name of the tag key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#key SyntheticsBrokenLinksMonitor#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Values associated with the tag key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/newrelic/r/synthetics_broken_links_monitor#values SyntheticsBrokenLinksMonitor#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SyntheticsBrokenLinksMonitorTag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SyntheticsBrokenLinksMonitorTagList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsBrokenLinksMonitor.SyntheticsBrokenLinksMonitorTagList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be76fef053d646b621118cc30699890e9bc145aa3bc5649cfb4111f66a502284)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SyntheticsBrokenLinksMonitorTagOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b5e611788d2e7c54ecbe8f14560dccc6c377bdbe21a15d44c35f71fe844360)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SyntheticsBrokenLinksMonitorTagOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d66fc0f66394d893b14042deca7e58800c9afe3929a1e70233aae68648af206)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0900987071aa64d9f5824292f6df5891f33fd2f117028d592871080c2482b9d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__60f05ea96c6345be1ae500b7c14f7a6ee8bf254f78d140f00a2707e3aed45525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsBrokenLinksMonitorTag]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsBrokenLinksMonitorTag]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsBrokenLinksMonitorTag]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abd67cf67dc916a75ad22479f4dba37a6c016091de39168871f5ebb387c0bf93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SyntheticsBrokenLinksMonitorTagOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.syntheticsBrokenLinksMonitor.SyntheticsBrokenLinksMonitorTagOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55bce52c55ece59cac57d210ac09ce33f0f1fa1439a937fbd58de5dfbc125b21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c84bc0d911d1d4510380eee3ad89624b8f61431201d4336ae9c1f7036510de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1372794315bd8a3c21aa62d679f685683fd1aa7b5fb971deec4d571baa03054e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SyntheticsBrokenLinksMonitorTag, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SyntheticsBrokenLinksMonitorTag, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SyntheticsBrokenLinksMonitorTag, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fb7e4e30ab842b51d90b1ae6774e61a51109e348a0717eeafd7e26673efc0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SyntheticsBrokenLinksMonitor",
    "SyntheticsBrokenLinksMonitorConfig",
    "SyntheticsBrokenLinksMonitorTag",
    "SyntheticsBrokenLinksMonitorTagList",
    "SyntheticsBrokenLinksMonitorTagOutputReference",
]

publication.publish()

def _typecheckingstub__e2233e98ff17d2c8083c26d18d3e8339dcb60aa5fe5125e14ef197fd9ec2a2e9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    period: builtins.str,
    status: builtins.str,
    uri: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    locations_private: typing.Optional[typing.Sequence[builtins.str]] = None,
    locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsBrokenLinksMonitorTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__5d1c9ee0fda289c0d63c70c792839d33a28ca78d736ca8e1ae40abd2097c22b8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsBrokenLinksMonitorTag, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13d1a36de68e78e8d401ef03a72de8f0a1d039e19f3195b95616105bce591f8d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52afa541fafcf12601e896db37ce732c092e91118431c5657712f6c90c45f402(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d4377377c4a2e9d670f2f776f6b8b256b14362a4a92d7f1b656a7c3191136c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6b7474baa4d08bcae0c97c01168f968d4ef7a5a16d350dea525ccc4147a969(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb09e7308446bc5172c42d1a18e85d9237275c8f07735b5dfb09d3eb7c0c0d8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb8937aef7efaa17435ef58ae7a0bdef1139ae32b7a275b3ab3191951e259183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d98684fbe8edbc701e8b24febb98cfbc7ccbb128e344d380adb7de5aa9bf13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f99733eec19df4d538a9d65e4a8fabe66d1a07433c86ed41939684bc4d2a01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bfacfc699fbb3711bcb51cf8115ec9a138ada62e4a8c05f6354b9d28f63a81b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    period: builtins.str,
    status: builtins.str,
    uri: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    locations_private: typing.Optional[typing.Sequence[builtins.str]] = None,
    locations_public: typing.Optional[typing.Sequence[builtins.str]] = None,
    tag: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SyntheticsBrokenLinksMonitorTag, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304518ca688e90c984178dfa34d1a80a13c3b363f47cf515ce7dc4a1166ae900(
    *,
    key: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be76fef053d646b621118cc30699890e9bc145aa3bc5649cfb4111f66a502284(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b5e611788d2e7c54ecbe8f14560dccc6c377bdbe21a15d44c35f71fe844360(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d66fc0f66394d893b14042deca7e58800c9afe3929a1e70233aae68648af206(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0900987071aa64d9f5824292f6df5891f33fd2f117028d592871080c2482b9d7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f05ea96c6345be1ae500b7c14f7a6ee8bf254f78d140f00a2707e3aed45525(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abd67cf67dc916a75ad22479f4dba37a6c016091de39168871f5ebb387c0bf93(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SyntheticsBrokenLinksMonitorTag]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bce52c55ece59cac57d210ac09ce33f0f1fa1439a937fbd58de5dfbc125b21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c84bc0d911d1d4510380eee3ad89624b8f61431201d4336ae9c1f7036510de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1372794315bd8a3c21aa62d679f685683fd1aa7b5fb971deec4d571baa03054e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fb7e4e30ab842b51d90b1ae6774e61a51109e348a0717eeafd7e26673efc0d(
    value: typing.Optional[typing.Union[SyntheticsBrokenLinksMonitorTag, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
