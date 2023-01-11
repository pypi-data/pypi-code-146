'''
# `data_cloudflare_waf_packages`

Refer to the Terraform Registory for docs: [`data_cloudflare_waf_packages`](https://www.terraform.io/docs/providers/cloudflare/d/waf_packages).
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


class DataCloudflareWafPackages(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackages",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages cloudflare_waf_packages}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        zone_id: builtins.str,
        filter: typing.Optional[typing.Union["DataCloudflareWafPackagesFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages cloudflare_waf_packages} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param zone_id: The zone identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#zone_id DataCloudflareWafPackages#zone_id}
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#filter DataCloudflareWafPackages#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#id DataCloudflareWafPackages#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2db55ffd699af5a78056ba531f9e0fcccc4fb1eb98ce6b0a41eb0ae8b88f5407)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataCloudflareWafPackagesConfig(
            zone_id=zone_id,
            filter=filter,
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

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        *,
        action_mode: typing.Optional[builtins.str] = None,
        detection_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sensitivity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#action_mode DataCloudflareWafPackages#action_mode}.
        :param detection_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#detection_mode DataCloudflareWafPackages#detection_mode}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#name DataCloudflareWafPackages#name}.
        :param sensitivity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#sensitivity DataCloudflareWafPackages#sensitivity}.
        '''
        value = DataCloudflareWafPackagesFilter(
            action_mode=action_mode,
            detection_mode=detection_mode,
            name=name,
            sensitivity=sensitivity,
        )

        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

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
    @jsii.member(jsii_name="filter")
    def filter(self) -> "DataCloudflareWafPackagesFilterOutputReference":
        return typing.cast("DataCloudflareWafPackagesFilterOutputReference", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="packages")
    def packages(self) -> "DataCloudflareWafPackagesPackagesList":
        return typing.cast("DataCloudflareWafPackagesPackagesList", jsii.get(self, "packages"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(self) -> typing.Optional["DataCloudflareWafPackagesFilter"]:
        return typing.cast(typing.Optional["DataCloudflareWafPackagesFilter"], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneIdInput")
    def zone_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10804730112a74303f0aad063fc7afc2ab91090be468a0dd64cab2c118a295e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="zoneId")
    def zone_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneId"))

    @zone_id.setter
    def zone_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d29e4a45b271e98c649dbddaf47f16a118754234000b2b1c81ee9b9596b7c03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackagesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "zone_id": "zoneId",
        "filter": "filter",
        "id": "id",
    },
)
class DataCloudflareWafPackagesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        zone_id: builtins.str,
        filter: typing.Optional[typing.Union["DataCloudflareWafPackagesFilter", typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param zone_id: The zone identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#zone_id DataCloudflareWafPackages#zone_id}
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#filter DataCloudflareWafPackages#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#id DataCloudflareWafPackages#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(filter, dict):
            filter = DataCloudflareWafPackagesFilter(**filter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967db2b3e159c47b61e7085a3f5e3dbce1f51f75c26320af0b9219bbb7998ff7)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument zone_id", value=zone_id, expected_type=type_hints["zone_id"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if filter is not None:
            self._values["filter"] = filter
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
    def zone_id(self) -> builtins.str:
        '''The zone identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#zone_id DataCloudflareWafPackages#zone_id}
        '''
        result = self._values.get("zone_id")
        assert result is not None, "Required property 'zone_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Optional["DataCloudflareWafPackagesFilter"]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#filter DataCloudflareWafPackages#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional["DataCloudflareWafPackagesFilter"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#id DataCloudflareWafPackages#id}.

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
        return "DataCloudflareWafPackagesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackagesFilter",
    jsii_struct_bases=[],
    name_mapping={
        "action_mode": "actionMode",
        "detection_mode": "detectionMode",
        "name": "name",
        "sensitivity": "sensitivity",
    },
)
class DataCloudflareWafPackagesFilter:
    def __init__(
        self,
        *,
        action_mode: typing.Optional[builtins.str] = None,
        detection_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sensitivity: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#action_mode DataCloudflareWafPackages#action_mode}.
        :param detection_mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#detection_mode DataCloudflareWafPackages#detection_mode}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#name DataCloudflareWafPackages#name}.
        :param sensitivity: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#sensitivity DataCloudflareWafPackages#sensitivity}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1cca273aa3d317665d6f1b12970c5b097188f9ad40c4efc1cf94ccbe479374)
            check_type(argname="argument action_mode", value=action_mode, expected_type=type_hints["action_mode"])
            check_type(argname="argument detection_mode", value=detection_mode, expected_type=type_hints["detection_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitivity", value=sensitivity, expected_type=type_hints["sensitivity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_mode is not None:
            self._values["action_mode"] = action_mode
        if detection_mode is not None:
            self._values["detection_mode"] = detection_mode
        if name is not None:
            self._values["name"] = name
        if sensitivity is not None:
            self._values["sensitivity"] = sensitivity

    @builtins.property
    def action_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#action_mode DataCloudflareWafPackages#action_mode}.'''
        result = self._values.get("action_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detection_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#detection_mode DataCloudflareWafPackages#detection_mode}.'''
        result = self._values.get("detection_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#name DataCloudflareWafPackages#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitivity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/d/waf_packages#sensitivity DataCloudflareWafPackages#sensitivity}.'''
        result = self._values.get("sensitivity")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareWafPackagesFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareWafPackagesFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackagesFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ec7466517e14ab381f7fabdb1cd8697c5c95de2ff11eccd090bafebdac6eb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetActionMode")
    def reset_action_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionMode", []))

    @jsii.member(jsii_name="resetDetectionMode")
    def reset_detection_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDetectionMode", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSensitivity")
    def reset_sensitivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitivity", []))

    @builtins.property
    @jsii.member(jsii_name="actionModeInput")
    def action_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="detectionModeInput")
    def detection_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "detectionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitivityInput")
    def sensitivity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sensitivityInput"))

    @builtins.property
    @jsii.member(jsii_name="actionMode")
    def action_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionMode"))

    @action_mode.setter
    def action_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__179751af8a05cb6db29516a24ad1c7b566cf48d9a0947437cb19362951b6e655)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionMode", value)

    @builtins.property
    @jsii.member(jsii_name="detectionMode")
    def detection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detectionMode"))

    @detection_mode.setter
    def detection_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6f1e78b1810842fb5da24ddf498c812cbdc5b5599991dd0419befcbe0c89458)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "detectionMode", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4e4990ea85229a351f7149e866df1c47ffb75daa8b246f3f79929395ff10f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sensitivity")
    def sensitivity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sensitivity"))

    @sensitivity.setter
    def sensitivity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad66300a723a73b39fab27322c782d2de5c59ced219d85cb13b697e8f5a3b95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensitivity", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareWafPackagesFilter]:
        return typing.cast(typing.Optional[DataCloudflareWafPackagesFilter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareWafPackagesFilter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e33dac6cb957373ad63415f76da8bfe5fb774f8a582f72dd9858cdbd8454538a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackagesPackages",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataCloudflareWafPackagesPackages:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCloudflareWafPackagesPackages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataCloudflareWafPackagesPackagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackagesPackagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e379a9a1d899405aea13e56cf85281b191361445079b27aed1e5241783eb9e29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataCloudflareWafPackagesPackagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4058810d0cd54c3eb1d5f1daf9805d93b2ee6c45a58666a747e88af6908f5132)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataCloudflareWafPackagesPackagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320a2065542e1a026d9af2ad0598b9a091973a6f816841f8517c1a055d96606c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1dc92eaee532ba5a229caf6f2f75dc56fb0c1721141b212d6c78bcf48b82b68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1691023e124bf9982d7601f912b5e8e0ff5a60947ef292a8a9d504f5bf86362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataCloudflareWafPackagesPackagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.dataCloudflareWafPackages.DataCloudflareWafPackagesPackagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07aec7ed0e440fa840a8e816ee6b81165b6ce601a79f790cb141e8751e4cff38)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="actionMode")
    def action_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionMode"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="detectionMode")
    def detection_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detectionMode"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sensitivity")
    def sensitivity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sensitivity"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataCloudflareWafPackagesPackages]:
        return typing.cast(typing.Optional[DataCloudflareWafPackagesPackages], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataCloudflareWafPackagesPackages],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a0cd0b5854303fea4efc79115c8c52ab9059fb8784f8f26010edb48034a03f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataCloudflareWafPackages",
    "DataCloudflareWafPackagesConfig",
    "DataCloudflareWafPackagesFilter",
    "DataCloudflareWafPackagesFilterOutputReference",
    "DataCloudflareWafPackagesPackages",
    "DataCloudflareWafPackagesPackagesList",
    "DataCloudflareWafPackagesPackagesOutputReference",
]

publication.publish()

def _typecheckingstub__2db55ffd699af5a78056ba531f9e0fcccc4fb1eb98ce6b0a41eb0ae8b88f5407(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    zone_id: builtins.str,
    filter: typing.Optional[typing.Union[DataCloudflareWafPackagesFilter, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__10804730112a74303f0aad063fc7afc2ab91090be468a0dd64cab2c118a295e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d29e4a45b271e98c649dbddaf47f16a118754234000b2b1c81ee9b9596b7c03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967db2b3e159c47b61e7085a3f5e3dbce1f51f75c26320af0b9219bbb7998ff7(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_id: builtins.str,
    filter: typing.Optional[typing.Union[DataCloudflareWafPackagesFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1cca273aa3d317665d6f1b12970c5b097188f9ad40c4efc1cf94ccbe479374(
    *,
    action_mode: typing.Optional[builtins.str] = None,
    detection_mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sensitivity: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ec7466517e14ab381f7fabdb1cd8697c5c95de2ff11eccd090bafebdac6eb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179751af8a05cb6db29516a24ad1c7b566cf48d9a0947437cb19362951b6e655(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6f1e78b1810842fb5da24ddf498c812cbdc5b5599991dd0419befcbe0c89458(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4e4990ea85229a351f7149e866df1c47ffb75daa8b246f3f79929395ff10f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad66300a723a73b39fab27322c782d2de5c59ced219d85cb13b697e8f5a3b95(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33dac6cb957373ad63415f76da8bfe5fb774f8a582f72dd9858cdbd8454538a(
    value: typing.Optional[DataCloudflareWafPackagesFilter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e379a9a1d899405aea13e56cf85281b191361445079b27aed1e5241783eb9e29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4058810d0cd54c3eb1d5f1daf9805d93b2ee6c45a58666a747e88af6908f5132(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320a2065542e1a026d9af2ad0598b9a091973a6f816841f8517c1a055d96606c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dc92eaee532ba5a229caf6f2f75dc56fb0c1721141b212d6c78bcf48b82b68(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1691023e124bf9982d7601f912b5e8e0ff5a60947ef292a8a9d504f5bf86362(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07aec7ed0e440fa840a8e816ee6b81165b6ce601a79f790cb141e8751e4cff38(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a0cd0b5854303fea4efc79115c8c52ab9059fb8784f8f26010edb48034a03f(
    value: typing.Optional[DataCloudflareWafPackagesPackages],
) -> None:
    """Type checking stubs"""
    pass
