'''
# `azurerm_iot_time_series_insights_event_source_eventhub`

Refer to the Terraform Registory for docs: [`azurerm_iot_time_series_insights_event_source_eventhub`](https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub).
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


class IotTimeSeriesInsightsEventSourceEventhub(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsEventSourceEventhub.IotTimeSeriesInsightsEventSourceEventhub",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub azurerm_iot_time_series_insights_event_source_eventhub}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        consumer_group_name: builtins.str,
        environment_id: builtins.str,
        eventhub_name: builtins.str,
        event_source_resource_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        namespace_name: builtins.str,
        shared_access_key: builtins.str,
        shared_access_key_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["IotTimeSeriesInsightsEventSourceEventhubTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timestamp_property_name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub azurerm_iot_time_series_insights_event_source_eventhub} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param consumer_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#consumer_group_name IotTimeSeriesInsightsEventSourceEventhub#consumer_group_name}.
        :param environment_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#environment_id IotTimeSeriesInsightsEventSourceEventhub#environment_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#eventhub_name IotTimeSeriesInsightsEventSourceEventhub#eventhub_name}.
        :param event_source_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#event_source_resource_id IotTimeSeriesInsightsEventSourceEventhub#event_source_resource_id}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#location IotTimeSeriesInsightsEventSourceEventhub#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#name IotTimeSeriesInsightsEventSourceEventhub#name}.
        :param namespace_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#namespace_name IotTimeSeriesInsightsEventSourceEventhub#namespace_name}.
        :param shared_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#shared_access_key IotTimeSeriesInsightsEventSourceEventhub#shared_access_key}.
        :param shared_access_key_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#shared_access_key_name IotTimeSeriesInsightsEventSourceEventhub#shared_access_key_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#id IotTimeSeriesInsightsEventSourceEventhub#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#tags IotTimeSeriesInsightsEventSourceEventhub#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#timeouts IotTimeSeriesInsightsEventSourceEventhub#timeouts}
        :param timestamp_property_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#timestamp_property_name IotTimeSeriesInsightsEventSourceEventhub#timestamp_property_name}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__296b982e4e4abea0c54139b23582363750c399e1d7dd9c15caa0fea6eeae3fbc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotTimeSeriesInsightsEventSourceEventhubConfig(
            consumer_group_name=consumer_group_name,
            environment_id=environment_id,
            eventhub_name=eventhub_name,
            event_source_resource_id=event_source_resource_id,
            location=location,
            name=name,
            namespace_name=namespace_name,
            shared_access_key=shared_access_key,
            shared_access_key_name=shared_access_key_name,
            id=id,
            tags=tags,
            timeouts=timeouts,
            timestamp_property_name=timestamp_property_name,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#create IotTimeSeriesInsightsEventSourceEventhub#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#delete IotTimeSeriesInsightsEventSourceEventhub#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#read IotTimeSeriesInsightsEventSourceEventhub#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#update IotTimeSeriesInsightsEventSourceEventhub#update}.
        '''
        value = IotTimeSeriesInsightsEventSourceEventhubTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTimestampPropertyName")
    def reset_timestamp_property_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimestampPropertyName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "IotTimeSeriesInsightsEventSourceEventhubTimeoutsOutputReference":
        return typing.cast("IotTimeSeriesInsightsEventSourceEventhubTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupNameInput")
    def consumer_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentIdInput")
    def environment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubNameInput")
    def eventhub_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventSourceResourceIdInput")
    def event_source_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventSourceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceNameInput")
    def namespace_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedAccessKeyInput")
    def shared_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedAccessKeyNameInput")
    def shared_access_key_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sharedAccessKeyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["IotTimeSeriesInsightsEventSourceEventhubTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["IotTimeSeriesInsightsEventSourceEventhubTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="timestampPropertyNameInput")
    def timestamp_property_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timestampPropertyNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerGroupName")
    def consumer_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerGroupName"))

    @consumer_group_name.setter
    def consumer_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7b871e9cf1aadf0df66ed7f1137d20da5ff51670ce7cc505e50739e38ef41cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @environment_id.setter
    def environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1273f3d7862c5cb29d2d893948f7c6cfd69e6846ab04aeec588c0c43cc37170a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentId", value)

    @builtins.property
    @jsii.member(jsii_name="eventhubName")
    def eventhub_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubName"))

    @eventhub_name.setter
    def eventhub_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09008e2dae4182e3ba7d7423a8a08736795cbc2e188e0d6d7a4d7e7f1e04baad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubName", value)

    @builtins.property
    @jsii.member(jsii_name="eventSourceResourceId")
    def event_source_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventSourceResourceId"))

    @event_source_resource_id.setter
    def event_source_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cabd269eb9aeb44ec16c0f1793505fd6e58c735bd7a4171f8053971749bcd97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventSourceResourceId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a442435375805298f8d606ab06472df89d25463450e5b07d6460a8b0e08fd11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ce219bce79e86c95684837f88c0076d42f2555e2bf8e5285a02f3f99221eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1308e81e5dffd68d7f13bfc5073756a6ab64376403157f7353fcb9087dc082f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @namespace_name.setter
    def namespace_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fc3e22e0acb0240987b3047ec0b2529bad9a9920fdc753815377e0afb41c133)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceName", value)

    @builtins.property
    @jsii.member(jsii_name="sharedAccessKey")
    def shared_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedAccessKey"))

    @shared_access_key.setter
    def shared_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4c343fdccde7decc12d22995f1ae36be7ede5498217aabe34dccc614b25c7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedAccessKey", value)

    @builtins.property
    @jsii.member(jsii_name="sharedAccessKeyName")
    def shared_access_key_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sharedAccessKeyName"))

    @shared_access_key_name.setter
    def shared_access_key_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b57093132ad8775f0e1dd71e70c70e704e752abfb4ec9a1c624a5da2785a937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedAccessKeyName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fdc8e662e6fede79a3e09048f8fc0a7a8da8391a2799c12ab00576d2b1b18b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="timestampPropertyName")
    def timestamp_property_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timestampPropertyName"))

    @timestamp_property_name.setter
    def timestamp_property_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b42627cbc584334abfd4275122b9366e8b696ecd5a87935b4c4424666d71a3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timestampPropertyName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsEventSourceEventhub.IotTimeSeriesInsightsEventSourceEventhubConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "consumer_group_name": "consumerGroupName",
        "environment_id": "environmentId",
        "eventhub_name": "eventhubName",
        "event_source_resource_id": "eventSourceResourceId",
        "location": "location",
        "name": "name",
        "namespace_name": "namespaceName",
        "shared_access_key": "sharedAccessKey",
        "shared_access_key_name": "sharedAccessKeyName",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
        "timestamp_property_name": "timestampPropertyName",
    },
)
class IotTimeSeriesInsightsEventSourceEventhubConfig(
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
        consumer_group_name: builtins.str,
        environment_id: builtins.str,
        eventhub_name: builtins.str,
        event_source_resource_id: builtins.str,
        location: builtins.str,
        name: builtins.str,
        namespace_name: builtins.str,
        shared_access_key: builtins.str,
        shared_access_key_name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["IotTimeSeriesInsightsEventSourceEventhubTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        timestamp_property_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param consumer_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#consumer_group_name IotTimeSeriesInsightsEventSourceEventhub#consumer_group_name}.
        :param environment_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#environment_id IotTimeSeriesInsightsEventSourceEventhub#environment_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#eventhub_name IotTimeSeriesInsightsEventSourceEventhub#eventhub_name}.
        :param event_source_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#event_source_resource_id IotTimeSeriesInsightsEventSourceEventhub#event_source_resource_id}.
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#location IotTimeSeriesInsightsEventSourceEventhub#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#name IotTimeSeriesInsightsEventSourceEventhub#name}.
        :param namespace_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#namespace_name IotTimeSeriesInsightsEventSourceEventhub#namespace_name}.
        :param shared_access_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#shared_access_key IotTimeSeriesInsightsEventSourceEventhub#shared_access_key}.
        :param shared_access_key_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#shared_access_key_name IotTimeSeriesInsightsEventSourceEventhub#shared_access_key_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#id IotTimeSeriesInsightsEventSourceEventhub#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#tags IotTimeSeriesInsightsEventSourceEventhub#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#timeouts IotTimeSeriesInsightsEventSourceEventhub#timeouts}
        :param timestamp_property_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#timestamp_property_name IotTimeSeriesInsightsEventSourceEventhub#timestamp_property_name}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = IotTimeSeriesInsightsEventSourceEventhubTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9894961f3010ebbce54fa0e18f544aa43fcb627f34c73175e9dace185e7ad4be)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument consumer_group_name", value=consumer_group_name, expected_type=type_hints["consumer_group_name"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument event_source_resource_id", value=event_source_resource_id, expected_type=type_hints["event_source_resource_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument shared_access_key", value=shared_access_key, expected_type=type_hints["shared_access_key"])
            check_type(argname="argument shared_access_key_name", value=shared_access_key_name, expected_type=type_hints["shared_access_key_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument timestamp_property_name", value=timestamp_property_name, expected_type=type_hints["timestamp_property_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_group_name": consumer_group_name,
            "environment_id": environment_id,
            "eventhub_name": eventhub_name,
            "event_source_resource_id": event_source_resource_id,
            "location": location,
            "name": name,
            "namespace_name": namespace_name,
            "shared_access_key": shared_access_key,
            "shared_access_key_name": shared_access_key_name,
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
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if timestamp_property_name is not None:
            self._values["timestamp_property_name"] = timestamp_property_name

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
    def consumer_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#consumer_group_name IotTimeSeriesInsightsEventSourceEventhub#consumer_group_name}.'''
        result = self._values.get("consumer_group_name")
        assert result is not None, "Required property 'consumer_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#environment_id IotTimeSeriesInsightsEventSourceEventhub#environment_id}.'''
        result = self._values.get("environment_id")
        assert result is not None, "Required property 'environment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#eventhub_name IotTimeSeriesInsightsEventSourceEventhub#eventhub_name}.'''
        result = self._values.get("eventhub_name")
        assert result is not None, "Required property 'eventhub_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_source_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#event_source_resource_id IotTimeSeriesInsightsEventSourceEventhub#event_source_resource_id}.'''
        result = self._values.get("event_source_resource_id")
        assert result is not None, "Required property 'event_source_resource_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#location IotTimeSeriesInsightsEventSourceEventhub#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#name IotTimeSeriesInsightsEventSourceEventhub#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#namespace_name IotTimeSeriesInsightsEventSourceEventhub#namespace_name}.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shared_access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#shared_access_key IotTimeSeriesInsightsEventSourceEventhub#shared_access_key}.'''
        result = self._values.get("shared_access_key")
        assert result is not None, "Required property 'shared_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shared_access_key_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#shared_access_key_name IotTimeSeriesInsightsEventSourceEventhub#shared_access_key_name}.'''
        result = self._values.get("shared_access_key_name")
        assert result is not None, "Required property 'shared_access_key_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#id IotTimeSeriesInsightsEventSourceEventhub#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#tags IotTimeSeriesInsightsEventSourceEventhub#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["IotTimeSeriesInsightsEventSourceEventhubTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#timeouts IotTimeSeriesInsightsEventSourceEventhub#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IotTimeSeriesInsightsEventSourceEventhubTimeouts"], result)

    @builtins.property
    def timestamp_property_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#timestamp_property_name IotTimeSeriesInsightsEventSourceEventhub#timestamp_property_name}.'''
        result = self._values.get("timestamp_property_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTimeSeriesInsightsEventSourceEventhubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsEventSourceEventhub.IotTimeSeriesInsightsEventSourceEventhubTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class IotTimeSeriesInsightsEventSourceEventhubTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#create IotTimeSeriesInsightsEventSourceEventhub#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#delete IotTimeSeriesInsightsEventSourceEventhub#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#read IotTimeSeriesInsightsEventSourceEventhub#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#update IotTimeSeriesInsightsEventSourceEventhub#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f60a8a52e99cac0bee1e85ba2b00d78a64bb16d9d77ece0f61295bd08c69b90f)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#create IotTimeSeriesInsightsEventSourceEventhub#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#delete IotTimeSeriesInsightsEventSourceEventhub#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#read IotTimeSeriesInsightsEventSourceEventhub#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/iot_time_series_insights_event_source_eventhub#update IotTimeSeriesInsightsEventSourceEventhub#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotTimeSeriesInsightsEventSourceEventhubTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotTimeSeriesInsightsEventSourceEventhubTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotTimeSeriesInsightsEventSourceEventhub.IotTimeSeriesInsightsEventSourceEventhubTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__634e91df169294d0599f0bacdd3be1c991c9cfde8edf5af6113e5922a6aa731a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03f9c9ee1fab6194b42550ca72c64f1ce3b4030a00aa19fb4e4603d8f0391d07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bcd3072d5d7a32ad018c8edcb2f5829f1677eae17216fc7d23084d4fff3ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fd6270e8e1f75e2a8c2078a9bf47cea1a44804822a9e8ddd573c260f8766e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70b6f177e7125a1d974d0f030d50ca2ed3a7c9332f5367f4a23fed15afb658d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[IotTimeSeriesInsightsEventSourceEventhubTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[IotTimeSeriesInsightsEventSourceEventhubTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[IotTimeSeriesInsightsEventSourceEventhubTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bd5f4637ce2297d5821ffd33273897495544ee36e726577b8ff22f7dc71a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "IotTimeSeriesInsightsEventSourceEventhub",
    "IotTimeSeriesInsightsEventSourceEventhubConfig",
    "IotTimeSeriesInsightsEventSourceEventhubTimeouts",
    "IotTimeSeriesInsightsEventSourceEventhubTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__296b982e4e4abea0c54139b23582363750c399e1d7dd9c15caa0fea6eeae3fbc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    consumer_group_name: builtins.str,
    environment_id: builtins.str,
    eventhub_name: builtins.str,
    event_source_resource_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    namespace_name: builtins.str,
    shared_access_key: builtins.str,
    shared_access_key_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[IotTimeSeriesInsightsEventSourceEventhubTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timestamp_property_name: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d7b871e9cf1aadf0df66ed7f1137d20da5ff51670ce7cc505e50739e38ef41cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1273f3d7862c5cb29d2d893948f7c6cfd69e6846ab04aeec588c0c43cc37170a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09008e2dae4182e3ba7d7423a8a08736795cbc2e188e0d6d7a4d7e7f1e04baad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cabd269eb9aeb44ec16c0f1793505fd6e58c735bd7a4171f8053971749bcd97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a442435375805298f8d606ab06472df89d25463450e5b07d6460a8b0e08fd11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ce219bce79e86c95684837f88c0076d42f2555e2bf8e5285a02f3f99221eb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1308e81e5dffd68d7f13bfc5073756a6ab64376403157f7353fcb9087dc082f6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc3e22e0acb0240987b3047ec0b2529bad9a9920fdc753815377e0afb41c133(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4c343fdccde7decc12d22995f1ae36be7ede5498217aabe34dccc614b25c7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b57093132ad8775f0e1dd71e70c70e704e752abfb4ec9a1c624a5da2785a937(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fdc8e662e6fede79a3e09048f8fc0a7a8da8391a2799c12ab00576d2b1b18b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b42627cbc584334abfd4275122b9366e8b696ecd5a87935b4c4424666d71a3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9894961f3010ebbce54fa0e18f544aa43fcb627f34c73175e9dace185e7ad4be(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    consumer_group_name: builtins.str,
    environment_id: builtins.str,
    eventhub_name: builtins.str,
    event_source_resource_id: builtins.str,
    location: builtins.str,
    name: builtins.str,
    namespace_name: builtins.str,
    shared_access_key: builtins.str,
    shared_access_key_name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[IotTimeSeriesInsightsEventSourceEventhubTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    timestamp_property_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f60a8a52e99cac0bee1e85ba2b00d78a64bb16d9d77ece0f61295bd08c69b90f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__634e91df169294d0599f0bacdd3be1c991c9cfde8edf5af6113e5922a6aa731a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03f9c9ee1fab6194b42550ca72c64f1ce3b4030a00aa19fb4e4603d8f0391d07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bcd3072d5d7a32ad018c8edcb2f5829f1677eae17216fc7d23084d4fff3ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fd6270e8e1f75e2a8c2078a9bf47cea1a44804822a9e8ddd573c260f8766e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70b6f177e7125a1d974d0f030d50ca2ed3a7c9332f5367f4a23fed15afb658d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bd5f4637ce2297d5821ffd33273897495544ee36e726577b8ff22f7dc71a38(
    value: typing.Optional[typing.Union[IotTimeSeriesInsightsEventSourceEventhubTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
