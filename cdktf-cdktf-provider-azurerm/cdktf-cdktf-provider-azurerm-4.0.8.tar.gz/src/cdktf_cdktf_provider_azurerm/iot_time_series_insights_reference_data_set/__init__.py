'''
# `azurerm_iot_time_series_insights_reference_data_set`

Refer to the Terraform Registory for docs: [`azurerm_iot_time_series_insights_reference_data_set`](https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set).
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


class IotTimeSeriesInsightsReferenceDataSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set azurerm_iot_time_series_insights_reference_data_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key_property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTimeSeriesInsightsReferenceDataSetKeyProperty", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        time_series_insights_environment_id: builtins.str,
        data_string_comparison_behavior: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["IotTimeSeriesInsightsReferenceDataSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set azurerm_iot_time_series_insights_reference_data_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key_property: key_property block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#key_property IotTimeSeriesInsightsReferenceDataSet#key_property}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#location IotTimeSeriesInsightsReferenceDataSet#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#name IotTimeSeriesInsightsReferenceDataSet#name}.
        :param time_series_insights_environment_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#time_series_insights_environment_id IotTimeSeriesInsightsReferenceDataSet#time_series_insights_environment_id}.
        :param data_string_comparison_behavior: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#data_string_comparison_behavior IotTimeSeriesInsightsReferenceDataSet#data_string_comparison_behavior}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#id IotTimeSeriesInsightsReferenceDataSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#tags IotTimeSeriesInsightsReferenceDataSet#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#timeouts IotTimeSeriesInsightsReferenceDataSet#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f83ff8fb9539e4531edb7df68353db4555bab778301d5f9dd59c6e6ead41212)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotTimeSeriesInsightsReferenceDataSetConfig(
            key_property=key_property,
            location=location,
            name=name,
            time_series_insights_environment_id=time_series_insights_environment_id,
            data_string_comparison_behavior=data_string_comparison_behavior,
            id=id,
            tags=tags,
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

    @jsii.member(jsii_name="putKeyProperty")
    def put_key_property(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTimeSeriesInsightsReferenceDataSetKeyProperty", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541977c480ad8b41c7b152e2ec490efcd23be04275e426b05b11bef4418cb951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKeyProperty", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#create IotTimeSeriesInsightsReferenceDataSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#delete IotTimeSeriesInsightsReferenceDataSet#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#read IotTimeSeriesInsightsReferenceDataSet#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#update IotTimeSeriesInsightsReferenceDataSet#update}.
        '''
        value = IotTimeSeriesInsightsReferenceDataSetTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataStringComparisonBehavior")
    def reset_data_string_comparison_behavior(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataStringComparisonBehavior", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

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
    @jsii.member(jsii_name="keyProperty")
    def key_property(self) -> "IotTimeSeriesInsightsReferenceDataSetKeyPropertyList":
        return typing.cast("IotTimeSeriesInsightsReferenceDataSetKeyPropertyList", jsii.get(self, "keyProperty"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "IotTimeSeriesInsightsReferenceDataSetTimeoutsOutputReference":
        return typing.cast("IotTimeSeriesInsightsReferenceDataSetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataStringComparisonBehaviorInput")
    def data_string_comparison_behavior_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dataStringComparisonBehaviorInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyPropertyInput")
    def key_property_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTimeSeriesInsightsReferenceDataSetKeyProperty"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTimeSeriesInsightsReferenceDataSetKeyProperty"]]], jsii.get(self, "keyPropertyInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["IotTimeSeriesInsightsReferenceDataSetTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["IotTimeSeriesInsightsReferenceDataSetTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeSeriesInsightsEnvironmentIdInput")
    def time_series_insights_environment_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeSeriesInsightsEnvironmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataStringComparisonBehavior")
    def data_string_comparison_behavior(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dataStringComparisonBehavior"))

    @data_string_comparison_behavior.setter
    def data_string_comparison_behavior(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bde357c3e833b85b4bab88f6d0e4d768b8d8d6445af95459630dd9237149c01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataStringComparisonBehavior", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fccd3d09c598e79a7739c0a4ea22264c01d431b5d2cc9240cabf17e30c3c297d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e975582cbcbf767b6a131bffcb67348154753b4a3530ef932852a2486175393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d9ed3e1f26191c5bdccfcf61423fe494e55d99092a11f8b5199ad5e5bb4f8a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a269f42662437a7adc4b85e1a2c72037f667c2f3b02d56dc9f45bc0f9a56cb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="timeSeriesInsightsEnvironmentId")
    def time_series_insights_environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeSeriesInsightsEnvironmentId"))

    @time_series_insights_environment_id.setter
    def time_series_insights_environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f64dd63a22942fc46b11bfae99cd7222360c44ab0ba9f7b446bd1acc59b101)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeSeriesInsightsEnvironmentId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key_property": "keyProperty",
        "location": "location",
        "name": "name",
        "time_series_insights_environment_id": "timeSeriesInsightsEnvironmentId",
        "data_string_comparison_behavior": "dataStringComparisonBehavior",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class IotTimeSeriesInsightsReferenceDataSetConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        key_property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotTimeSeriesInsightsReferenceDataSetKeyProperty", typing.Dict[builtins.str, typing.Any]]]],
        location: builtins.str,
        name: builtins.str,
        time_series_insights_environment_id: builtins.str,
        data_string_comparison_behavior: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["IotTimeSeriesInsightsReferenceDataSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key_property: key_property block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#key_property IotTimeSeriesInsightsReferenceDataSet#key_property}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#location IotTimeSeriesInsightsReferenceDataSet#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#name IotTimeSeriesInsightsReferenceDataSet#name}.
        :param time_series_insights_environment_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#time_series_insights_environment_id IotTimeSeriesInsightsReferenceDataSet#time_series_insights_environment_id}.
        :param data_string_comparison_behavior: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#data_string_comparison_behavior IotTimeSeriesInsightsReferenceDataSet#data_string_comparison_behavior}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#id IotTimeSeriesInsightsReferenceDataSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#tags IotTimeSeriesInsightsReferenceDataSet#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#timeouts IotTimeSeriesInsightsReferenceDataSet#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = IotTimeSeriesInsightsReferenceDataSetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8908e0241afe3b8fb136f53ebea839318b2c61229eb1f0c72d594dd5808e77be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key_property", value=key_property, expected_type=type_hints["key_property"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument time_series_insights_environment_id", value=time_series_insights_environment_id, expected_type=type_hints["time_series_insights_environment_id"])
            check_type(argname="argument data_string_comparison_behavior", value=data_string_comparison_behavior, expected_type=type_hints["data_string_comparison_behavior"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_property": key_property,
            "location": location,
            "name": name,
            "time_series_insights_environment_id": time_series_insights_environment_id,
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
        if data_string_comparison_behavior is not None:
            self._values["data_string_comparison_behavior"] = data_string_comparison_behavior
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags
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
    def key_property(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTimeSeriesInsightsReferenceDataSetKeyProperty"]]:
        '''key_property block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#key_property IotTimeSeriesInsightsReferenceDataSet#key_property}
        '''
        result = self._values.get("key_property")
        assert result is not None, "Required property 'key_property' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotTimeSeriesInsightsReferenceDataSetKeyProperty"]], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#location IotTimeSeriesInsightsReferenceDataSet#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#name IotTimeSeriesInsightsReferenceDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def time_series_insights_environment_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#time_series_insights_environment_id IotTimeSeriesInsightsReferenceDataSet#time_series_insights_environment_id}.'''
        result = self._values.get("time_series_insights_environment_id")
        assert result is not None, "Required property 'time_series_insights_environment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_string_comparison_behavior(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#data_string_comparison_behavior IotTimeSeriesInsightsReferenceDataSet#data_string_comparison_behavior}.'''
        result = self._values.get("data_string_comparison_behavior")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#id IotTimeSeriesInsightsReferenceDataSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#tags IotTimeSeriesInsightsReferenceDataSet#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["IotTimeSeriesInsightsReferenceDataSetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#timeouts IotTimeSeriesInsightsReferenceDataSet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IotTimeSeriesInsightsReferenceDataSetTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTimeSeriesInsightsReferenceDataSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSetKeyProperty",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type"},
)
class IotTimeSeriesInsightsReferenceDataSetKeyProperty:
    def __init__(self, *, name: builtins.str, type: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#name IotTimeSeriesInsightsReferenceDataSet#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#type IotTimeSeriesInsightsReferenceDataSet#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e2779cb3bad7fc0e44fbc956d3ba0f0d6fcfadf6daaba868c4ecfb5e8fea6f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#name IotTimeSeriesInsightsReferenceDataSet#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#type IotTimeSeriesInsightsReferenceDataSet#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTimeSeriesInsightsReferenceDataSetKeyProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTimeSeriesInsightsReferenceDataSetKeyPropertyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSetKeyPropertyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__606390ff72f19b3accfbf1b57330c52edf1e87fde6ec99c30cea43b88762b969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotTimeSeriesInsightsReferenceDataSetKeyPropertyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb6e792373e22456d5d1fc7a4988ceaed92bba68dc245a93f06411d2f0c85e6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotTimeSeriesInsightsReferenceDataSetKeyPropertyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86466f2586cc4232adbfd2c04f5e5be8245eef5d876867065faf11a3d40ca9f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ff7a6b6d97892f890471dbdf4e0551b6ccaf32f4dd139326b1207e4fe6393f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcd1342c74c9ff3848ed43114fd93dd2e6baf1e94d4db4ca6e579bb613a64bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTimeSeriesInsightsReferenceDataSetKeyProperty]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTimeSeriesInsightsReferenceDataSetKeyProperty]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTimeSeriesInsightsReferenceDataSetKeyProperty]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbe35a8ed5b15a711f9a19e859cd6150d2690577e0c0bfecfb5c07e8baf91e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class IotTimeSeriesInsightsReferenceDataSetKeyPropertyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSetKeyPropertyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b4490be6dc9c50bdfe4b3d3ad0fd2403744c69e7383b821cdd2959c5b93232c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d46c3580940232000dde6b202c55978173d2d08c30c76161d9185cdfaba9a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c13afbeefbc940e294cff51d1ecc8b8479916d8c610d02e37f30eca453c1b9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574e79b859889adc9184a869a5256fae0fe16c68e2e317fc07a52e8a16e94089)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSetTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class IotTimeSeriesInsightsReferenceDataSetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#create IotTimeSeriesInsightsReferenceDataSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#delete IotTimeSeriesInsightsReferenceDataSet#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#read IotTimeSeriesInsightsReferenceDataSet#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#update IotTimeSeriesInsightsReferenceDataSet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22241550c300b50a349fc8b4c742c93ed0033d044344ad7f67760905c2892e02)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#create IotTimeSeriesInsightsReferenceDataSet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#delete IotTimeSeriesInsightsReferenceDataSet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#read IotTimeSeriesInsightsReferenceDataSet#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_reference_data_set#update IotTimeSeriesInsightsReferenceDataSet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTimeSeriesInsightsReferenceDataSetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTimeSeriesInsightsReferenceDataSetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsReferenceDataSet.IotTimeSeriesInsightsReferenceDataSetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c498c031550ca77d50f1916966c1db5fde1f9ed1f876d8b2a72dda85c23ca10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b5433fcbfd5890e9b2cbd3f1551c15584a916e42a6d30ab26565cce9ed00067)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19767d896928b18ad29588cd0dc3fc56ce1e8ba2aa0602747d87bb76ab6ea835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648b1b0ffddad58bd63ee1d59619864b7851f7d840c60ae0bf126fcf5a2ca498)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281833f80ecc0b479fa70bb2228abfb0273623bd9bafc738e5d3b8cf0fa036d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20022870d13d5ed2fe543956928e014088c7706c7e793e299fffc88542f53567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "IotTimeSeriesInsightsReferenceDataSet",
    "IotTimeSeriesInsightsReferenceDataSetConfig",
    "IotTimeSeriesInsightsReferenceDataSetKeyProperty",
    "IotTimeSeriesInsightsReferenceDataSetKeyPropertyList",
    "IotTimeSeriesInsightsReferenceDataSetKeyPropertyOutputReference",
    "IotTimeSeriesInsightsReferenceDataSetTimeouts",
    "IotTimeSeriesInsightsReferenceDataSetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__3f83ff8fb9539e4531edb7df68353db4555bab778301d5f9dd59c6e6ead41212(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key_property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    time_series_insights_environment_id: builtins.str,
    data_string_comparison_behavior: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__541977c480ad8b41c7b152e2ec490efcd23be04275e426b05b11bef4418cb951(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bde357c3e833b85b4bab88f6d0e4d768b8d8d6445af95459630dd9237149c01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fccd3d09c598e79a7739c0a4ea22264c01d431b5d2cc9240cabf17e30c3c297d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e975582cbcbf767b6a131bffcb67348154753b4a3530ef932852a2486175393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d9ed3e1f26191c5bdccfcf61423fe494e55d99092a11f8b5199ad5e5bb4f8a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a269f42662437a7adc4b85e1a2c72037f667c2f3b02d56dc9f45bc0f9a56cb7a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f64dd63a22942fc46b11bfae99cd7222360c44ab0ba9f7b446bd1acc59b101(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8908e0241afe3b8fb136f53ebea839318b2c61229eb1f0c72d594dd5808e77be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key_property: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, typing.Dict[builtins.str, typing.Any]]]],
    location: builtins.str,
    name: builtins.str,
    time_series_insights_environment_id: builtins.str,
    data_string_comparison_behavior: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e2779cb3bad7fc0e44fbc956d3ba0f0d6fcfadf6daaba868c4ecfb5e8fea6f(
    *,
    name: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606390ff72f19b3accfbf1b57330c52edf1e87fde6ec99c30cea43b88762b969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb6e792373e22456d5d1fc7a4988ceaed92bba68dc245a93f06411d2f0c85e6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86466f2586cc4232adbfd2c04f5e5be8245eef5d876867065faf11a3d40ca9f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ff7a6b6d97892f890471dbdf4e0551b6ccaf32f4dd139326b1207e4fe6393f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd1342c74c9ff3848ed43114fd93dd2e6baf1e94d4db4ca6e579bb613a64bc8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbe35a8ed5b15a711f9a19e859cd6150d2690577e0c0bfecfb5c07e8baf91e0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotTimeSeriesInsightsReferenceDataSetKeyProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4490be6dc9c50bdfe4b3d3ad0fd2403744c69e7383b821cdd2959c5b93232c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d46c3580940232000dde6b202c55978173d2d08c30c76161d9185cdfaba9a5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c13afbeefbc940e294cff51d1ecc8b8479916d8c610d02e37f30eca453c1b9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574e79b859889adc9184a869a5256fae0fe16c68e2e317fc07a52e8a16e94089(
    value: typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetKeyProperty, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22241550c300b50a349fc8b4c742c93ed0033d044344ad7f67760905c2892e02(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c498c031550ca77d50f1916966c1db5fde1f9ed1f876d8b2a72dda85c23ca10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5433fcbfd5890e9b2cbd3f1551c15584a916e42a6d30ab26565cce9ed00067(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19767d896928b18ad29588cd0dc3fc56ce1e8ba2aa0602747d87bb76ab6ea835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648b1b0ffddad58bd63ee1d59619864b7851f7d840c60ae0bf126fcf5a2ca498(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281833f80ecc0b479fa70bb2228abfb0273623bd9bafc738e5d3b8cf0fa036d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20022870d13d5ed2fe543956928e014088c7706c7e793e299fffc88542f53567(
    value: typing.Optional[typing.Union[IotTimeSeriesInsightsReferenceDataSetTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
