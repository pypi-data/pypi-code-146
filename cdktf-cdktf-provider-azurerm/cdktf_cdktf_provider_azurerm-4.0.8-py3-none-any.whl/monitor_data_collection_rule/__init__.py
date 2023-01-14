'''
# `azurerm_monitor_data_collection_rule`

Refer to the Terraform Registory for docs: [`azurerm_monitor_data_collection_rule`](https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule).
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


class MonitorDataCollectionRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRule",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule azurerm_monitor_data_collection_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataFlow", typing.Dict[builtins.str, typing.Any]]]],
        destinations: typing.Union["MonitorDataCollectionRuleDestinations", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        data_sources: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorDataCollectionRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule azurerm_monitor_data_collection_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_flow: data_flow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#data_flow MonitorDataCollectionRule#data_flow}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#location MonitorDataCollectionRule#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#resource_group_name MonitorDataCollectionRule#resource_group_name}.
        :param data_sources: data_sources block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#data_sources MonitorDataCollectionRule#data_sources}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#description MonitorDataCollectionRule#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#id MonitorDataCollectionRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kind: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#kind MonitorDataCollectionRule#kind}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#tags MonitorDataCollectionRule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#timeouts MonitorDataCollectionRule#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7453666e1a553395226393741cd1fa7f278ea729f9b208c8d82957365dd73fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorDataCollectionRuleConfig(
            data_flow=data_flow,
            destinations=destinations,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            data_sources=data_sources,
            description=description,
            id=id,
            kind=kind,
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

    @jsii.member(jsii_name="putDataFlow")
    def put_data_flow(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataFlow", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e11e8053e4d4689ad66e11c5b3b4857dd939bf1bc46f7fd9a24c4a7ce5e81a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDataFlow", [value]))

    @jsii.member(jsii_name="putDataSources")
    def put_data_sources(
        self,
        *,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        performance_counter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPerformanceCounter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        syslog: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesSyslog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_event_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsEventLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param extension: extension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension MonitorDataCollectionRule#extension}
        :param performance_counter: performance_counter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#performance_counter MonitorDataCollectionRule#performance_counter}
        :param syslog: syslog block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#syslog MonitorDataCollectionRule#syslog}
        :param windows_event_log: windows_event_log block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#windows_event_log MonitorDataCollectionRule#windows_event_log}
        '''
        value = MonitorDataCollectionRuleDataSources(
            extension=extension,
            performance_counter=performance_counter,
            syslog=syslog,
            windows_event_log=windows_event_log,
        )

        return typing.cast(None, jsii.invoke(self, "putDataSources", [value]))

    @jsii.member(jsii_name="putDestinations")
    def put_destinations(
        self,
        *,
        azure_monitor_metrics: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        log_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsLogAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_monitor_metrics: azure_monitor_metrics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#azure_monitor_metrics MonitorDataCollectionRule#azure_monitor_metrics}
        :param log_analytics: log_analytics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#log_analytics MonitorDataCollectionRule#log_analytics}
        '''
        value = MonitorDataCollectionRuleDestinations(
            azure_monitor_metrics=azure_monitor_metrics, log_analytics=log_analytics
        )

        return typing.cast(None, jsii.invoke(self, "putDestinations", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#create MonitorDataCollectionRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#delete MonitorDataCollectionRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#read MonitorDataCollectionRule#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#update MonitorDataCollectionRule#update}.
        '''
        value = MonitorDataCollectionRuleTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDataSources")
    def reset_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDataSources", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetKind")
    def reset_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKind", []))

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
    @jsii.member(jsii_name="dataFlow")
    def data_flow(self) -> "MonitorDataCollectionRuleDataFlowList":
        return typing.cast("MonitorDataCollectionRuleDataFlowList", jsii.get(self, "dataFlow"))

    @builtins.property
    @jsii.member(jsii_name="dataSources")
    def data_sources(self) -> "MonitorDataCollectionRuleDataSourcesOutputReference":
        return typing.cast("MonitorDataCollectionRuleDataSourcesOutputReference", jsii.get(self, "dataSources"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> "MonitorDataCollectionRuleDestinationsOutputReference":
        return typing.cast("MonitorDataCollectionRuleDestinationsOutputReference", jsii.get(self, "destinations"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorDataCollectionRuleTimeoutsOutputReference":
        return typing.cast("MonitorDataCollectionRuleTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="dataFlowInput")
    def data_flow_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]]], jsii.get(self, "dataFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourcesInput")
    def data_sources_input(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDataSources"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSources"], jsii.get(self, "dataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDestinations"]:
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDestinations"], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="kindInput")
    def kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kindInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitorDataCollectionRuleTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitorDataCollectionRuleTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0a394bb8b6e37d91805fa59e4acaf2d079e0d607c424ce7ee9c94e1d8b7eef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd1a633d39cc0d112f1c664f1c447859aab147a85e4c0b444cf173e02a713773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @kind.setter
    def kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__275a728f2a5ab4f192ac57947b946bd499a44adaa22a59fed67db05e8add50df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kind", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b2ebce16a93e815816f1d44e9db356f927eeee9cbe385ce08fe43cd9deccb68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38fb73cf03f998dbc2489f0dda204889060e754510687c2747824cfd3dbb408)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5f01dbf2f883c2a932ccfd3de2a8ac4ae393089c4ea1d2dc518f89a95f885f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a015c242f541883e7d693f89c1e1d38d3a9ab49dd92619dbb1ce3d833530265b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_flow": "dataFlow",
        "destinations": "destinations",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "data_sources": "dataSources",
        "description": "description",
        "id": "id",
        "kind": "kind",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorDataCollectionRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataFlow", typing.Dict[builtins.str, typing.Any]]]],
        destinations: typing.Union["MonitorDataCollectionRuleDestinations", typing.Dict[builtins.str, typing.Any]],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        data_sources: typing.Optional[typing.Union["MonitorDataCollectionRuleDataSources", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        kind: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorDataCollectionRuleTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_flow: data_flow block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#data_flow MonitorDataCollectionRule#data_flow}
        :param destinations: destinations block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}
        :param location: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#location MonitorDataCollectionRule#location}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#resource_group_name MonitorDataCollectionRule#resource_group_name}.
        :param data_sources: data_sources block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#data_sources MonitorDataCollectionRule#data_sources}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#description MonitorDataCollectionRule#description}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#id MonitorDataCollectionRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param kind: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#kind MonitorDataCollectionRule#kind}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#tags MonitorDataCollectionRule#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#timeouts MonitorDataCollectionRule#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(destinations, dict):
            destinations = MonitorDataCollectionRuleDestinations(**destinations)
        if isinstance(data_sources, dict):
            data_sources = MonitorDataCollectionRuleDataSources(**data_sources)
        if isinstance(timeouts, dict):
            timeouts = MonitorDataCollectionRuleTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa2466c780fe932563ee1fdec3e948f3932866f264f4758aa6e61dfaf01b721)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_flow", value=data_flow, expected_type=type_hints["data_flow"])
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument data_sources", value=data_sources, expected_type=type_hints["data_sources"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument kind", value=kind, expected_type=type_hints["kind"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_flow": data_flow,
            "destinations": destinations,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if data_sources is not None:
            self._values["data_sources"] = data_sources
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if kind is not None:
            self._values["kind"] = kind
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
    def data_flow(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]]:
        '''data_flow block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#data_flow MonitorDataCollectionRule#data_flow}
        '''
        result = self._values.get("data_flow")
        assert result is not None, "Required property 'data_flow' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataFlow"]], result)

    @builtins.property
    def destinations(self) -> "MonitorDataCollectionRuleDestinations":
        '''destinations block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}
        '''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast("MonitorDataCollectionRuleDestinations", result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#location MonitorDataCollectionRule#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#resource_group_name MonitorDataCollectionRule#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_sources(self) -> typing.Optional["MonitorDataCollectionRuleDataSources"]:
        '''data_sources block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#data_sources MonitorDataCollectionRule#data_sources}
        '''
        result = self._values.get("data_sources")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDataSources"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#description MonitorDataCollectionRule#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#id MonitorDataCollectionRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kind(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#kind MonitorDataCollectionRule#kind}.'''
        result = self._values.get("kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#tags MonitorDataCollectionRule#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorDataCollectionRuleTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#timeouts MonitorDataCollectionRule#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataFlow",
    jsii_struct_bases=[],
    name_mapping={"destinations": "destinations", "streams": "streams"},
)
class MonitorDataCollectionRuleDataFlow:
    def __init__(
        self,
        *,
        destinations: typing.Sequence[builtins.str],
        streams: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param destinations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}.
        :param streams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31534c94d7dd3dad441dc0a88e1e01b345b0d2771935ed98ae8cfa810007c1b8)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destinations": destinations,
            "streams": streams,
        }

    @builtins.property
    def destinations(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#destinations MonitorDataCollectionRule#destinations}.'''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataFlow(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataFlowList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataFlowList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3b7467ac66c79abb788f4f177613cc038be6bd3bef457292cad4d50c9d2ac4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataFlowOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e28001bae8dde55b09ebc93d72573d086b3471678ab9376fb58397279361854)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataFlowOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3fe99a37a74266ffbc7c65e477f17d6b2ae1c0d94b6fe073fc14a8ac979493)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e37357f493fd96feb93ab04c9ba3ffd21760d46f8a20df9eea4700415bccd5ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16f8b837a7f0ac2ccc598e8656dc844340d6afc00202328badf53b48cf1d29ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19211c8f99e693e17a52ce672f2aaafaa796160841818044805dec48626ccd3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDataFlowOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataFlowOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3d0559b2a7af7e3c93c11f6ce5dd64fc74b4cce670ea17392f5d6adc9f9777)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="destinationsInput")
    def destinations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "destinationsInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="destinations")
    def destinations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "destinations"))

    @destinations.setter
    def destinations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c3ab541bab6e813a141e98046559a185a3117aac7618ac05955f43018ca51f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinations", value)

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d5cdf55d1808ceeb0ade162c05658ac355c00259c0977a978a8ed2acb2942c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleDataFlow, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleDataFlow, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataFlow, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ae601d4a96b61b1e90db264045b452e77a95599c2b7b7c10185d848b2b2a32e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSources",
    jsii_struct_bases=[],
    name_mapping={
        "extension": "extension",
        "performance_counter": "performanceCounter",
        "syslog": "syslog",
        "windows_event_log": "windowsEventLog",
    },
)
class MonitorDataCollectionRuleDataSources:
    def __init__(
        self,
        *,
        extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesExtension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        performance_counter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPerformanceCounter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        syslog: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesSyslog", typing.Dict[builtins.str, typing.Any]]]]] = None,
        windows_event_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsEventLog", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param extension: extension block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension MonitorDataCollectionRule#extension}
        :param performance_counter: performance_counter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#performance_counter MonitorDataCollectionRule#performance_counter}
        :param syslog: syslog block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#syslog MonitorDataCollectionRule#syslog}
        :param windows_event_log: windows_event_log block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#windows_event_log MonitorDataCollectionRule#windows_event_log}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c3daef060c1ba14b60de26ea3644ccaf37e883eede9cf3152594ac4b91630e)
            check_type(argname="argument extension", value=extension, expected_type=type_hints["extension"])
            check_type(argname="argument performance_counter", value=performance_counter, expected_type=type_hints["performance_counter"])
            check_type(argname="argument syslog", value=syslog, expected_type=type_hints["syslog"])
            check_type(argname="argument windows_event_log", value=windows_event_log, expected_type=type_hints["windows_event_log"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if extension is not None:
            self._values["extension"] = extension
        if performance_counter is not None:
            self._values["performance_counter"] = performance_counter
        if syslog is not None:
            self._values["syslog"] = syslog
        if windows_event_log is not None:
            self._values["windows_event_log"] = windows_event_log

    @builtins.property
    def extension(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesExtension"]]]:
        '''extension block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension MonitorDataCollectionRule#extension}
        '''
        result = self._values.get("extension")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesExtension"]]], result)

    @builtins.property
    def performance_counter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]]:
        '''performance_counter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#performance_counter MonitorDataCollectionRule#performance_counter}
        '''
        result = self._values.get("performance_counter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]], result)

    @builtins.property
    def syslog(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]]:
        '''syslog block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#syslog MonitorDataCollectionRule#syslog}
        '''
        result = self._values.get("syslog")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]], result)

    @builtins.property
    def windows_event_log(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]]:
        '''windows_event_log block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#windows_event_log MonitorDataCollectionRule#windows_event_log}
        '''
        result = self._values.get("windows_event_log")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesExtension",
    jsii_struct_bases=[],
    name_mapping={
        "extension_name": "extensionName",
        "name": "name",
        "streams": "streams",
        "extension_json": "extensionJson",
        "input_data_sources": "inputDataSources",
    },
)
class MonitorDataCollectionRuleDataSourcesExtension:
    def __init__(
        self,
        *,
        extension_name: builtins.str,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        extension_json: typing.Optional[builtins.str] = None,
        input_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param extension_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension_name MonitorDataCollectionRule#extension_name}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param extension_json: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension_json MonitorDataCollectionRule#extension_json}.
        :param input_data_sources: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#input_data_sources MonitorDataCollectionRule#input_data_sources}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880b7ad1e3b0bd0ba7e0151d7e7567c5d08b9cbdfc6d38d39417b12702a3368f)
            check_type(argname="argument extension_name", value=extension_name, expected_type=type_hints["extension_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument extension_json", value=extension_json, expected_type=type_hints["extension_json"])
            check_type(argname="argument input_data_sources", value=input_data_sources, expected_type=type_hints["input_data_sources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "extension_name": extension_name,
            "name": name,
            "streams": streams,
        }
        if extension_json is not None:
            self._values["extension_json"] = extension_json
        if input_data_sources is not None:
            self._values["input_data_sources"] = input_data_sources

    @builtins.property
    def extension_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension_name MonitorDataCollectionRule#extension_name}.'''
        result = self._values.get("extension_name")
        assert result is not None, "Required property 'extension_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def extension_json(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#extension_json MonitorDataCollectionRule#extension_json}.'''
        result = self._values.get("extension_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_data_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#input_data_sources MonitorDataCollectionRule#input_data_sources}.'''
        result = self._values.get("input_data_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesExtensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesExtensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__183fae162e87e634b2a1f5afe600ebc7173826d68e760e51ee37419023830866)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesExtensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbd9f8ba2db26388671009239773467b9df840eb192aafbb15e32fbe6db5486)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesExtensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7a9b8afdc59c99c73eafd4d2819580128b0f70cb88281820ff12e4121c0895d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fa733b18a6e5102f40d47e6d9254aff9099cc2b95d7877810da5756c5f56b9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__185756c2250710bef82bf9ac7c9bb9b2cc4e16b791ea9d93bac1f29419126d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0cd819b7de080bf03920306efacdd1aefc760d5024ea31242786ee123aa0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDataSourcesExtensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesExtensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d52a47c60ab98c9c983f79ffe99470d98b01f78d2b3c72d7de6fdff9efd14a6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetExtensionJson")
    def reset_extension_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtensionJson", []))

    @jsii.member(jsii_name="resetInputDataSources")
    def reset_input_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputDataSources", []))

    @builtins.property
    @jsii.member(jsii_name="extensionJsonInput")
    def extension_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionNameInput")
    def extension_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "extensionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="inputDataSourcesInput")
    def input_data_sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="extensionJson")
    def extension_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensionJson"))

    @extension_json.setter
    def extension_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae6e2ea2650bca6797764421dc9064fed839bc8a152f80c6c282e07160d96b1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionJson", value)

    @builtins.property
    @jsii.member(jsii_name="extensionName")
    def extension_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "extensionName"))

    @extension_name.setter
    def extension_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90ad2b40420efecf2dd706280bf4eec18f806932690a7cee0d59f7995555fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "extensionName", value)

    @builtins.property
    @jsii.member(jsii_name="inputDataSources")
    def input_data_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputDataSources"))

    @input_data_sources.setter
    def input_data_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d043607978efb77412109d01c1589c0f4a02ce12d95b0d4be2879dc7ab7d6d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputDataSources", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35680830854aa39deac9d18cbfa14a1eb36b0479ff3535f70a2040634b7feac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00efb2fbf8068731a29e8ab7f73f72aecd0787c4401f1cae08f2ee5e2c1e50d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c7afc49a4e77c572bcb5390bd01ce235841f959207e50382bcb1962e0b8e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDataSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2effe2f8c570d9473506ca26fa08538e9686d88823968e25280314ce036abb49)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExtension")
    def put_extension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0a89278e0341b256e9f9cc8e1d9d492bc0e448d8018ca9d7cb9088b0251dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtension", [value]))

    @jsii.member(jsii_name="putPerformanceCounter")
    def put_performance_counter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesPerformanceCounter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b0b23419be8886df574a3538f0029ecb4dc28798e8cf2988355ce62ea204452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPerformanceCounter", [value]))

    @jsii.member(jsii_name="putSyslog")
    def put_syslog(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesSyslog", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b4fc0a3e1e4514bdc017ec8e53c7c1d6b3f0d0fd2a867d9635198eeb9a9979)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSyslog", [value]))

    @jsii.member(jsii_name="putWindowsEventLog")
    def put_windows_event_log(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDataSourcesWindowsEventLog", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__678e2a6c50a509255b32cdb494db7c92fc40cca514d78b7b7865700b097015e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWindowsEventLog", [value]))

    @jsii.member(jsii_name="resetExtension")
    def reset_extension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtension", []))

    @jsii.member(jsii_name="resetPerformanceCounter")
    def reset_performance_counter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPerformanceCounter", []))

    @jsii.member(jsii_name="resetSyslog")
    def reset_syslog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSyslog", []))

    @jsii.member(jsii_name="resetWindowsEventLog")
    def reset_windows_event_log(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowsEventLog", []))

    @builtins.property
    @jsii.member(jsii_name="extension")
    def extension(self) -> MonitorDataCollectionRuleDataSourcesExtensionList:
        return typing.cast(MonitorDataCollectionRuleDataSourcesExtensionList, jsii.get(self, "extension"))

    @builtins.property
    @jsii.member(jsii_name="performanceCounter")
    def performance_counter(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesPerformanceCounterList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesPerformanceCounterList", jsii.get(self, "performanceCounter"))

    @builtins.property
    @jsii.member(jsii_name="syslog")
    def syslog(self) -> "MonitorDataCollectionRuleDataSourcesSyslogList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesSyslogList", jsii.get(self, "syslog"))

    @builtins.property
    @jsii.member(jsii_name="windowsEventLog")
    def windows_event_log(
        self,
    ) -> "MonitorDataCollectionRuleDataSourcesWindowsEventLogList":
        return typing.cast("MonitorDataCollectionRuleDataSourcesWindowsEventLogList", jsii.get(self, "windowsEventLog"))

    @builtins.property
    @jsii.member(jsii_name="extensionInput")
    def extension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]], jsii.get(self, "extensionInput"))

    @builtins.property
    @jsii.member(jsii_name="performanceCounterInput")
    def performance_counter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesPerformanceCounter"]]], jsii.get(self, "performanceCounterInput"))

    @builtins.property
    @jsii.member(jsii_name="syslogInput")
    def syslog_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesSyslog"]]], jsii.get(self, "syslogInput"))

    @builtins.property
    @jsii.member(jsii_name="windowsEventLogInput")
    def windows_event_log_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDataSourcesWindowsEventLog"]]], jsii.get(self, "windowsEventLogInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDataCollectionRuleDataSources]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDataSources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDataSources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9fcfd914b9be386362f91e5d399a648425be687b5559c9d4e9dbf6d3ca17c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPerformanceCounter",
    jsii_struct_bases=[],
    name_mapping={
        "counter_specifiers": "counterSpecifiers",
        "name": "name",
        "sampling_frequency_in_seconds": "samplingFrequencyInSeconds",
        "streams": "streams",
    },
)
class MonitorDataCollectionRuleDataSourcesPerformanceCounter:
    def __init__(
        self,
        *,
        counter_specifiers: typing.Sequence[builtins.str],
        name: builtins.str,
        sampling_frequency_in_seconds: jsii.Number,
        streams: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param counter_specifiers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#counter_specifiers MonitorDataCollectionRule#counter_specifiers}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param sampling_frequency_in_seconds: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#sampling_frequency_in_seconds MonitorDataCollectionRule#sampling_frequency_in_seconds}.
        :param streams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78ba1f5d9613309985657fe5930e78b29ab6382c52d1effa76c6bbec356ed669)
            check_type(argname="argument counter_specifiers", value=counter_specifiers, expected_type=type_hints["counter_specifiers"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sampling_frequency_in_seconds", value=sampling_frequency_in_seconds, expected_type=type_hints["sampling_frequency_in_seconds"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "counter_specifiers": counter_specifiers,
            "name": name,
            "sampling_frequency_in_seconds": sampling_frequency_in_seconds,
            "streams": streams,
        }

    @builtins.property
    def counter_specifiers(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#counter_specifiers MonitorDataCollectionRule#counter_specifiers}.'''
        result = self._values.get("counter_specifiers")
        assert result is not None, "Required property 'counter_specifiers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sampling_frequency_in_seconds(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#sampling_frequency_in_seconds MonitorDataCollectionRule#sampling_frequency_in_seconds}.'''
        result = self._values.get("sampling_frequency_in_seconds")
        assert result is not None, "Required property 'sampling_frequency_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesPerformanceCounter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesPerformanceCounterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPerformanceCounterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e176ba6c348b43592700cf73b905e40b6e43c0ec8716e5c3463fc730347ae7a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3df5f8db59d7a70d216f8b9d09242dea4d008534d6c676b32f5c9082c4a5e52)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a46ef8e935b7375dc66288bcbfa68000ba20431c33565aa6ab0db1ac11d5247b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a50725eb29f40423111863c87f0fd76d5a138203d80f1f44cd8b71d14aaa5010)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afd547505ac563cc2877a062839063bffca99801d395a2c457198379b0a157e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da162700eecd9b67119ff4ba6574311c9cbf7617dde1c9306c4a761f93a5d923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba48b3032f1fbdbec9520c26c08f837f3499f3787aad32081ac6bf7d9c0a1bf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="counterSpecifiersInput")
    def counter_specifiers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "counterSpecifiersInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="samplingFrequencyInSecondsInput")
    def sampling_frequency_in_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "samplingFrequencyInSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="counterSpecifiers")
    def counter_specifiers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "counterSpecifiers"))

    @counter_specifiers.setter
    def counter_specifiers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__019fc55d291fdf6ed53eabcdfe5a735e7cfe4e23b2bc2205f2076a530231696c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "counterSpecifiers", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44685a243f0dd09810e08799a3cb881340919bfdab2f5963000a5fefa414a0de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="samplingFrequencyInSeconds")
    def sampling_frequency_in_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "samplingFrequencyInSeconds"))

    @sampling_frequency_in_seconds.setter
    def sampling_frequency_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e296f08e7386d1e845462f452383c1b5701615f2293becda6436199586af13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samplingFrequencyInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0a02f98829b60720def8c2570ddc43664284f7ec78b53b572f0f27c587664c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b102ff800cdee7e14415df5d29642221721ec2b922472f59e0ae5a26a074e62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesSyslog",
    jsii_struct_bases=[],
    name_mapping={
        "facility_names": "facilityNames",
        "log_levels": "logLevels",
        "name": "name",
        "streams": "streams",
    },
)
class MonitorDataCollectionRuleDataSourcesSyslog:
    def __init__(
        self,
        *,
        facility_names: typing.Sequence[builtins.str],
        log_levels: typing.Sequence[builtins.str],
        name: builtins.str,
        streams: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param facility_names: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#facility_names MonitorDataCollectionRule#facility_names}.
        :param log_levels: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#log_levels MonitorDataCollectionRule#log_levels}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9883e1ae6a4738a241f2d58c530f77392ebf28f4f8bcff16cbb35b180a87dd)
            check_type(argname="argument facility_names", value=facility_names, expected_type=type_hints["facility_names"])
            check_type(argname="argument log_levels", value=log_levels, expected_type=type_hints["log_levels"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "facility_names": facility_names,
            "log_levels": log_levels,
            "name": name,
        }
        if streams is not None:
            self._values["streams"] = streams

    @builtins.property
    def facility_names(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#facility_names MonitorDataCollectionRule#facility_names}.'''
        result = self._values.get("facility_names")
        assert result is not None, "Required property 'facility_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def log_levels(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#log_levels MonitorDataCollectionRule#log_levels}.'''
        result = self._values.get("log_levels")
        assert result is not None, "Required property 'log_levels' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesSyslog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesSyslogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesSyslogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8e065d90d2fec3a359cfa493fc108b40bb648980f2a7a10d7c41adcb8e342a2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesSyslogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775dd5444548e5ad93924f6b6bdb06546a96458eac1dff78ce4ffef60980db18)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesSyslogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b2257aad83009eff725de5a48a53bb4b36eb3f0fd2d008e6341c5caa217967)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b22a5544aea02741f55941d849ef70b86928957d176407217cf1c05e2b4ad316)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac12af89411ebf126eaa86d93b12437625c0c61c2ef2ed78715fa965e45867a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf58e26d2249e71249170f53fc2737e098ad5207f6a76257b72d373a24f8862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDataSourcesSyslogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesSyslogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9395de1dc772496048a16e5720bf172b0429024a22a8780da6d5625c4edffa3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetStreams")
    def reset_streams(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreams", []))

    @builtins.property
    @jsii.member(jsii_name="facilityNamesInput")
    def facility_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "facilityNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelsInput")
    def log_levels_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "logLevelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="facilityNames")
    def facility_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "facilityNames"))

    @facility_names.setter
    def facility_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a710f9efe877b8c08037c0a7688d0c185fa2ad66c1420e68d86ebf9afee7e9f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "facilityNames", value)

    @builtins.property
    @jsii.member(jsii_name="logLevels")
    def log_levels(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "logLevels"))

    @log_levels.setter
    def log_levels(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95687c2eec80398767496ad3cfa55696d9ea87e6425d0ed7691355e0ed6bc47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500fe805d28c61fcaacebf17058d8f615e949ced6a6cc55dfd9917bc41b9f381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c1cb242acfb5b9e07424d7ab71d87206676b08fd6ca1cc668c9daec918a93b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca36002b57f3acbd64630f68149f68bcde0363e4baa21d3592020407ece77b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsEventLog",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "streams": "streams",
        "x_path_queries": "xPathQueries",
    },
)
class MonitorDataCollectionRuleDataSourcesWindowsEventLog:
    def __init__(
        self,
        *,
        name: builtins.str,
        streams: typing.Sequence[builtins.str],
        x_path_queries: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param streams: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.
        :param x_path_queries: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#x_path_queries MonitorDataCollectionRule#x_path_queries}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b557f77d1831e36056c552a32db43c0d6da5fda2d3231c835178e51abd7925a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument streams", value=streams, expected_type=type_hints["streams"])
            check_type(argname="argument x_path_queries", value=x_path_queries, expected_type=type_hints["x_path_queries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "streams": streams,
            "x_path_queries": x_path_queries,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def streams(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#streams MonitorDataCollectionRule#streams}.'''
        result = self._values.get("streams")
        assert result is not None, "Required property 'streams' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def x_path_queries(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#x_path_queries MonitorDataCollectionRule#x_path_queries}.'''
        result = self._values.get("x_path_queries")
        assert result is not None, "Required property 'x_path_queries' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDataSourcesWindowsEventLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDataSourcesWindowsEventLogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsEventLogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec9a50ff2a5020e44702ba3ecf596a9339a8dc48b6fc4695018929d907f21f9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a625a4a1a6a1cf68036a2cbbc33e3af075a67ab10696572e1d5fa4cc84c1052)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9fa611d7edce38fd55b9b978596d636a49acd5037a6e226b599532c8e369b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b27f75a278932276e72a3aefedcb4483e91634cebdcafff23762203e82469f8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84602f9219b96030b27dc26be68b3a66a004f24f7d1062ee5316a73753202e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8313d3809cc603a18a5c92cfb56366a1df14d027b50ea1a55acc65608409efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f0fb0e4b94355c0f9c3eb1acbc8271d1cffec0637dbbdc4546a4b2cf757e007)
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
    @jsii.member(jsii_name="streamsInput")
    def streams_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "streamsInput"))

    @builtins.property
    @jsii.member(jsii_name="xPathQueriesInput")
    def x_path_queries_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xPathQueriesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e59ed61ddbff58dc840808382b8ddf1c2892676c422e0c949d21370e3de0a920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="streams")
    def streams(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "streams"))

    @streams.setter
    def streams(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e3a8eae68c25d444877c414cc6abda9d2d5cf268f00cc01e386619a37507e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streams", value)

    @builtins.property
    @jsii.member(jsii_name="xPathQueries")
    def x_path_queries(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xPathQueries"))

    @x_path_queries.setter
    def x_path_queries(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f23cebcc2b2a793c46d90f5a53dbe34f3c4549cbee36bab023a947623238222)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xPathQueries", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41b0f67435549f47faad1238a8cd36c0a9404a47a886965b566e4967ba1a389c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinations",
    jsii_struct_bases=[],
    name_mapping={
        "azure_monitor_metrics": "azureMonitorMetrics",
        "log_analytics": "logAnalytics",
    },
)
class MonitorDataCollectionRuleDestinations:
    def __init__(
        self,
        *,
        azure_monitor_metrics: typing.Optional[typing.Union["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics", typing.Dict[builtins.str, typing.Any]]] = None,
        log_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorDataCollectionRuleDestinationsLogAnalytics", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param azure_monitor_metrics: azure_monitor_metrics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#azure_monitor_metrics MonitorDataCollectionRule#azure_monitor_metrics}
        :param log_analytics: log_analytics block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#log_analytics MonitorDataCollectionRule#log_analytics}
        '''
        if isinstance(azure_monitor_metrics, dict):
            azure_monitor_metrics = MonitorDataCollectionRuleDestinationsAzureMonitorMetrics(**azure_monitor_metrics)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91129a3b8459f9f9277e633acd1c0cba03afca8b282196aba60a2ffea57b91a8)
            check_type(argname="argument azure_monitor_metrics", value=azure_monitor_metrics, expected_type=type_hints["azure_monitor_metrics"])
            check_type(argname="argument log_analytics", value=log_analytics, expected_type=type_hints["log_analytics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if azure_monitor_metrics is not None:
            self._values["azure_monitor_metrics"] = azure_monitor_metrics
        if log_analytics is not None:
            self._values["log_analytics"] = log_analytics

    @builtins.property
    def azure_monitor_metrics(
        self,
    ) -> typing.Optional["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics"]:
        '''azure_monitor_metrics block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#azure_monitor_metrics MonitorDataCollectionRule#azure_monitor_metrics}
        '''
        result = self._values.get("azure_monitor_metrics")
        return typing.cast(typing.Optional["MonitorDataCollectionRuleDestinationsAzureMonitorMetrics"], result)

    @builtins.property
    def log_analytics(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsLogAnalytics"]]]:
        '''log_analytics block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#log_analytics MonitorDataCollectionRule#log_analytics}
        '''
        result = self._values.get("log_analytics")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorDataCollectionRuleDestinationsLogAnalytics"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsAzureMonitorMetrics",
    jsii_struct_bases=[],
    name_mapping={"name": "name"},
)
class MonitorDataCollectionRuleDestinationsAzureMonitorMetrics:
    def __init__(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ecd0556ab897ecc2bca1b5401b8dbd4d672f663daadc537150dba8b8f4fb70)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsAzureMonitorMetrics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9057f9db833800d87a63b1df8170af107ad8c20affb98d66be4da94182eb044a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4a0a0ceb07c7ec885a3ac5d79b0833b8caa3d739dd8be4eecf59962a9c29a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd026bc0ea172c4e759b319b66699e7648ed57e390d431db5a417465a0b767a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsLogAnalytics",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "workspace_resource_id": "workspaceResourceId"},
)
class MonitorDataCollectionRuleDestinationsLogAnalytics:
    def __init__(
        self,
        *,
        name: builtins.str,
        workspace_resource_id: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        :param workspace_resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#workspace_resource_id MonitorDataCollectionRule#workspace_resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__251443bc66028e9ec47bb10d9c703e7b79fd9cb49a3de69a82c29a7adf08508d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument workspace_resource_id", value=workspace_resource_id, expected_type=type_hints["workspace_resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "workspace_resource_id": workspace_resource_id,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workspace_resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#workspace_resource_id MonitorDataCollectionRule#workspace_resource_id}.'''
        result = self._values.get("workspace_resource_id")
        assert result is not None, "Required property 'workspace_resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleDestinationsLogAnalytics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleDestinationsLogAnalyticsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsLogAnalyticsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b910654ddfca9e344e8141acb1abb600e90077de18e9650337a717855d8d624)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63e8cb24e7b3a3be4c78abe3061cb2287e98ba7aa0554fcc0bc3e3ad43b25a50)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731f1b46222b14adf5de13fc4bd639cb53277f8c38ae139bf3c633796136e89a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3a9bd5eb5e4e75e12f759e050b6048ec228cbdb3328abf91ef53311f1ce2c44)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9f959ef7c4c4d4bd72b60c4d4bd883b10c7bb28a6131fe871b7626b4963e14b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__616fd31921bf88f0d3165cee51b4f976c64c556905fe55727a70ccf6ad9a45bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d98f91803fead56e4f1ba854b066930a45e6c7e6e91b8502163107c55ac6e11)
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
    @jsii.member(jsii_name="workspaceResourceIdInput")
    def workspace_resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceResourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1ccb4def4da1177ca948eefc1199d7f4cd2ea3886594f89878527bc679f01f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="workspaceResourceId")
    def workspace_resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceResourceId"))

    @workspace_resource_id.setter
    def workspace_resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dea27ca99d63e43e6b0aa930b3ebbf5767b9ec3af80e50e6ea7f25059c0014b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceResourceId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818948068c75dcae789dd04d74629d38a8c8c7d00b4382e6015b7fd035227055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorDataCollectionRuleDestinationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleDestinationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c782f684d157afde64540324f5f82e0b0f863ad3b1dc23c61fd2fcc72643d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAzureMonitorMetrics")
    def put_azure_monitor_metrics(self, *, name: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#name MonitorDataCollectionRule#name}.
        '''
        value = MonitorDataCollectionRuleDestinationsAzureMonitorMetrics(name=name)

        return typing.cast(None, jsii.invoke(self, "putAzureMonitorMetrics", [value]))

    @jsii.member(jsii_name="putLogAnalytics")
    def put_log_analytics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b415fe73dab62431fb7a05f0e71fec2d04de47a0db07fa94d8980ccc2497326e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLogAnalytics", [value]))

    @jsii.member(jsii_name="resetAzureMonitorMetrics")
    def reset_azure_monitor_metrics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureMonitorMetrics", []))

    @jsii.member(jsii_name="resetLogAnalytics")
    def reset_log_analytics(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalytics", []))

    @builtins.property
    @jsii.member(jsii_name="azureMonitorMetrics")
    def azure_monitor_metrics(
        self,
    ) -> MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference:
        return typing.cast(MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference, jsii.get(self, "azureMonitorMetrics"))

    @builtins.property
    @jsii.member(jsii_name="logAnalytics")
    def log_analytics(self) -> MonitorDataCollectionRuleDestinationsLogAnalyticsList:
        return typing.cast(MonitorDataCollectionRuleDestinationsLogAnalyticsList, jsii.get(self, "logAnalytics"))

    @builtins.property
    @jsii.member(jsii_name="azureMonitorMetricsInput")
    def azure_monitor_metrics_input(
        self,
    ) -> typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics], jsii.get(self, "azureMonitorMetricsInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsInput")
    def log_analytics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]], jsii.get(self, "logAnalyticsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorDataCollectionRuleDestinations]:
        return typing.cast(typing.Optional[MonitorDataCollectionRuleDestinations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorDataCollectionRuleDestinations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e09f04e010ada32c12dc4384179d3061aaa449ccbbbf9e0972c668346135b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorDataCollectionRuleTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#create MonitorDataCollectionRule#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#delete MonitorDataCollectionRule#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#read MonitorDataCollectionRule#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#update MonitorDataCollectionRule#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f613481b34a9e84eaf7bdfe27afa2f209b9c0450d6f6da0e76bf9978064eb832)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#create MonitorDataCollectionRule#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#delete MonitorDataCollectionRule#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#read MonitorDataCollectionRule#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_data_collection_rule#update MonitorDataCollectionRule#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorDataCollectionRuleTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorDataCollectionRuleTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorDataCollectionRule.MonitorDataCollectionRuleTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__748230ce1aa460add2b88e74b7b34e8e75cfb571cddd317414f030d656e633be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__623c9190f2692ff5b8c50f4dc7846c8ae43654b019829ffe7ce7255adebbe281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__944eaa692cd5bc0f47db9e7de9ee30c53758ecdb4de0dbb2324c765bc500ed3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b21271d37530314d8a2a14fd460cbcf4ce1910df9dd7a122aa1902c42e21872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74dc6e72b4d4da7518e8afb87a7b1a96223dfeaf3705c734a9179cba1db15e4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff96d5437c456f564ff126f6b28b77cc57c6bb67a074dd8c94acac244b1d4bde)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitorDataCollectionRule",
    "MonitorDataCollectionRuleConfig",
    "MonitorDataCollectionRuleDataFlow",
    "MonitorDataCollectionRuleDataFlowList",
    "MonitorDataCollectionRuleDataFlowOutputReference",
    "MonitorDataCollectionRuleDataSources",
    "MonitorDataCollectionRuleDataSourcesExtension",
    "MonitorDataCollectionRuleDataSourcesExtensionList",
    "MonitorDataCollectionRuleDataSourcesExtensionOutputReference",
    "MonitorDataCollectionRuleDataSourcesOutputReference",
    "MonitorDataCollectionRuleDataSourcesPerformanceCounter",
    "MonitorDataCollectionRuleDataSourcesPerformanceCounterList",
    "MonitorDataCollectionRuleDataSourcesPerformanceCounterOutputReference",
    "MonitorDataCollectionRuleDataSourcesSyslog",
    "MonitorDataCollectionRuleDataSourcesSyslogList",
    "MonitorDataCollectionRuleDataSourcesSyslogOutputReference",
    "MonitorDataCollectionRuleDataSourcesWindowsEventLog",
    "MonitorDataCollectionRuleDataSourcesWindowsEventLogList",
    "MonitorDataCollectionRuleDataSourcesWindowsEventLogOutputReference",
    "MonitorDataCollectionRuleDestinations",
    "MonitorDataCollectionRuleDestinationsAzureMonitorMetrics",
    "MonitorDataCollectionRuleDestinationsAzureMonitorMetricsOutputReference",
    "MonitorDataCollectionRuleDestinationsLogAnalytics",
    "MonitorDataCollectionRuleDestinationsLogAnalyticsList",
    "MonitorDataCollectionRuleDestinationsLogAnalyticsOutputReference",
    "MonitorDataCollectionRuleDestinationsOutputReference",
    "MonitorDataCollectionRuleTimeouts",
    "MonitorDataCollectionRuleTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c7453666e1a553395226393741cd1fa7f278ea729f9b208c8d82957365dd73fe(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataFlow, typing.Dict[builtins.str, typing.Any]]]],
    destinations: typing.Union[MonitorDataCollectionRuleDestinations, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    data_sources: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__6e11e8053e4d4689ad66e11c5b3b4857dd939bf1bc46f7fd9a24c4a7ce5e81a3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataFlow, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a394bb8b6e37d91805fa59e4acaf2d079e0d607c424ce7ee9c94e1d8b7eef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd1a633d39cc0d112f1c664f1c447859aab147a85e4c0b444cf173e02a713773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__275a728f2a5ab4f192ac57947b946bd499a44adaa22a59fed67db05e8add50df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b2ebce16a93e815816f1d44e9db356f927eeee9cbe385ce08fe43cd9deccb68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38fb73cf03f998dbc2489f0dda204889060e754510687c2747824cfd3dbb408(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5f01dbf2f883c2a932ccfd3de2a8ac4ae393089c4ea1d2dc518f89a95f885f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a015c242f541883e7d693f89c1e1d38d3a9ab49dd92619dbb1ce3d833530265b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa2466c780fe932563ee1fdec3e948f3932866f264f4758aa6e61dfaf01b721(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_flow: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataFlow, typing.Dict[builtins.str, typing.Any]]]],
    destinations: typing.Union[MonitorDataCollectionRuleDestinations, typing.Dict[builtins.str, typing.Any]],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    data_sources: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSources, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    kind: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31534c94d7dd3dad441dc0a88e1e01b345b0d2771935ed98ae8cfa810007c1b8(
    *,
    destinations: typing.Sequence[builtins.str],
    streams: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b7467ac66c79abb788f4f177613cc038be6bd3bef457292cad4d50c9d2ac4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e28001bae8dde55b09ebc93d72573d086b3471678ab9376fb58397279361854(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3fe99a37a74266ffbc7c65e477f17d6b2ae1c0d94b6fe073fc14a8ac979493(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37357f493fd96feb93ab04c9ba3ffd21760d46f8a20df9eea4700415bccd5ff(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f8b837a7f0ac2ccc598e8656dc844340d6afc00202328badf53b48cf1d29ea(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19211c8f99e693e17a52ce672f2aaafaa796160841818044805dec48626ccd3a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataFlow]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3d0559b2a7af7e3c93c11f6ce5dd64fc74b4cce670ea17392f5d6adc9f9777(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c3ab541bab6e813a141e98046559a185a3117aac7618ac05955f43018ca51f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d5cdf55d1808ceeb0ade162c05658ac355c00259c0977a978a8ed2acb2942c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ae601d4a96b61b1e90db264045b452e77a95599c2b7b7c10185d848b2b2a32e(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataFlow, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c3daef060c1ba14b60de26ea3644ccaf37e883eede9cf3152594ac4b91630e(
    *,
    extension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    performance_counter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    syslog: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, typing.Dict[builtins.str, typing.Any]]]]] = None,
    windows_event_log: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880b7ad1e3b0bd0ba7e0151d7e7567c5d08b9cbdfc6d38d39417b12702a3368f(
    *,
    extension_name: builtins.str,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    extension_json: typing.Optional[builtins.str] = None,
    input_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183fae162e87e634b2a1f5afe600ebc7173826d68e760e51ee37419023830866(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbd9f8ba2db26388671009239773467b9df840eb192aafbb15e32fbe6db5486(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7a9b8afdc59c99c73eafd4d2819580128b0f70cb88281820ff12e4121c0895d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa733b18a6e5102f40d47e6d9254aff9099cc2b95d7877810da5756c5f56b9f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185756c2250710bef82bf9ac7c9bb9b2cc4e16b791ea9d93bac1f29419126d06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0cd819b7de080bf03920306efacdd1aefc760d5024ea31242786ee123aa0f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesExtension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d52a47c60ab98c9c983f79ffe99470d98b01f78d2b3c72d7de6fdff9efd14a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae6e2ea2650bca6797764421dc9064fed839bc8a152f80c6c282e07160d96b1b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90ad2b40420efecf2dd706280bf4eec18f806932690a7cee0d59f7995555fa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d043607978efb77412109d01c1589c0f4a02ce12d95b0d4be2879dc7ab7d6d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35680830854aa39deac9d18cbfa14a1eb36b0479ff3535f70a2040634b7feac2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00efb2fbf8068731a29e8ab7f73f72aecd0787c4401f1cae08f2ee5e2c1e50d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c7afc49a4e77c572bcb5390bd01ce235841f959207e50382bcb1962e0b8e04(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2effe2f8c570d9473506ca26fa08538e9686d88823968e25280314ce036abb49(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0a89278e0341b256e9f9cc8e1d9d492bc0e448d8018ca9d7cb9088b0251dd6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesExtension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b0b23419be8886df574a3538f0029ecb4dc28798e8cf2988355ce62ea204452(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b4fc0a3e1e4514bdc017ec8e53c7c1d6b3f0d0fd2a867d9635198eeb9a9979(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678e2a6c50a509255b32cdb494db7c92fc40cca514d78b7b7865700b097015e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9fcfd914b9be386362f91e5d399a648425be687b5559c9d4e9dbf6d3ca17c9(
    value: typing.Optional[MonitorDataCollectionRuleDataSources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ba1f5d9613309985657fe5930e78b29ab6382c52d1effa76c6bbec356ed669(
    *,
    counter_specifiers: typing.Sequence[builtins.str],
    name: builtins.str,
    sampling_frequency_in_seconds: jsii.Number,
    streams: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e176ba6c348b43592700cf73b905e40b6e43c0ec8716e5c3463fc730347ae7a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3df5f8db59d7a70d216f8b9d09242dea4d008534d6c676b32f5c9082c4a5e52(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a46ef8e935b7375dc66288bcbfa68000ba20431c33565aa6ab0db1ac11d5247b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a50725eb29f40423111863c87f0fd76d5a138203d80f1f44cd8b71d14aaa5010(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd547505ac563cc2877a062839063bffca99801d395a2c457198379b0a157e7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da162700eecd9b67119ff4ba6574311c9cbf7617dde1c9306c4a761f93a5d923(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesPerformanceCounter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba48b3032f1fbdbec9520c26c08f837f3499f3787aad32081ac6bf7d9c0a1bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__019fc55d291fdf6ed53eabcdfe5a735e7cfe4e23b2bc2205f2076a530231696c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44685a243f0dd09810e08799a3cb881340919bfdab2f5963000a5fefa414a0de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e296f08e7386d1e845462f452383c1b5701615f2293becda6436199586af13(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0a02f98829b60720def8c2570ddc43664284f7ec78b53b572f0f27c587664c0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b102ff800cdee7e14415df5d29642221721ec2b922472f59e0ae5a26a074e62(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesPerformanceCounter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9883e1ae6a4738a241f2d58c530f77392ebf28f4f8bcff16cbb35b180a87dd(
    *,
    facility_names: typing.Sequence[builtins.str],
    log_levels: typing.Sequence[builtins.str],
    name: builtins.str,
    streams: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e065d90d2fec3a359cfa493fc108b40bb648980f2a7a10d7c41adcb8e342a2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775dd5444548e5ad93924f6b6bdb06546a96458eac1dff78ce4ffef60980db18(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b2257aad83009eff725de5a48a53bb4b36eb3f0fd2d008e6341c5caa217967(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22a5544aea02741f55941d849ef70b86928957d176407217cf1c05e2b4ad316(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac12af89411ebf126eaa86d93b12437625c0c61c2ef2ed78715fa965e45867a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf58e26d2249e71249170f53fc2737e098ad5207f6a76257b72d373a24f8862(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesSyslog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9395de1dc772496048a16e5720bf172b0429024a22a8780da6d5625c4edffa3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a710f9efe877b8c08037c0a7688d0c185fa2ad66c1420e68d86ebf9afee7e9f6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95687c2eec80398767496ad3cfa55696d9ea87e6425d0ed7691355e0ed6bc47(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500fe805d28c61fcaacebf17058d8f615e949ced6a6cc55dfd9917bc41b9f381(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c1cb242acfb5b9e07424d7ab71d87206676b08fd6ca1cc668c9daec918a93b7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca36002b57f3acbd64630f68149f68bcde0363e4baa21d3592020407ece77b90(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesSyslog, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b557f77d1831e36056c552a32db43c0d6da5fda2d3231c835178e51abd7925a(
    *,
    name: builtins.str,
    streams: typing.Sequence[builtins.str],
    x_path_queries: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9a50ff2a5020e44702ba3ecf596a9339a8dc48b6fc4695018929d907f21f9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a625a4a1a6a1cf68036a2cbbc33e3af075a67ab10696572e1d5fa4cc84c1052(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9fa611d7edce38fd55b9b978596d636a49acd5037a6e226b599532c8e369b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b27f75a278932276e72a3aefedcb4483e91634cebdcafff23762203e82469f8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84602f9219b96030b27dc26be68b3a66a004f24f7d1062ee5316a73753202e8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8313d3809cc603a18a5c92cfb56366a1df14d027b50ea1a55acc65608409efe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDataSourcesWindowsEventLog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f0fb0e4b94355c0f9c3eb1acbc8271d1cffec0637dbbdc4546a4b2cf757e007(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59ed61ddbff58dc840808382b8ddf1c2892676c422e0c949d21370e3de0a920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4e3a8eae68c25d444877c414cc6abda9d2d5cf268f00cc01e386619a37507e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f23cebcc2b2a793c46d90f5a53dbe34f3c4549cbee36bab023a947623238222(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b0f67435549f47faad1238a8cd36c0a9404a47a886965b566e4967ba1a389c(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleDataSourcesWindowsEventLog, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91129a3b8459f9f9277e633acd1c0cba03afca8b282196aba60a2ffea57b91a8(
    *,
    azure_monitor_metrics: typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics, typing.Dict[builtins.str, typing.Any]]] = None,
    log_analytics: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ecd0556ab897ecc2bca1b5401b8dbd4d672f663daadc537150dba8b8f4fb70(
    *,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9057f9db833800d87a63b1df8170af107ad8c20affb98d66be4da94182eb044a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a0a0ceb07c7ec885a3ac5d79b0833b8caa3d739dd8be4eecf59962a9c29a10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd026bc0ea172c4e759b319b66699e7648ed57e390d431db5a417465a0b767a1(
    value: typing.Optional[MonitorDataCollectionRuleDestinationsAzureMonitorMetrics],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__251443bc66028e9ec47bb10d9c703e7b79fd9cb49a3de69a82c29a7adf08508d(
    *,
    name: builtins.str,
    workspace_resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b910654ddfca9e344e8141acb1abb600e90077de18e9650337a717855d8d624(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63e8cb24e7b3a3be4c78abe3061cb2287e98ba7aa0554fcc0bc3e3ad43b25a50(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731f1b46222b14adf5de13fc4bd639cb53277f8c38ae139bf3c633796136e89a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a9bd5eb5e4e75e12f759e050b6048ec228cbdb3328abf91ef53311f1ce2c44(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f959ef7c4c4d4bd72b60c4d4bd883b10c7bb28a6131fe871b7626b4963e14b0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__616fd31921bf88f0d3165cee51b4f976c64c556905fe55727a70ccf6ad9a45bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorDataCollectionRuleDestinationsLogAnalytics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d98f91803fead56e4f1ba854b066930a45e6c7e6e91b8502163107c55ac6e11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1ccb4def4da1177ca948eefc1199d7f4cd2ea3886594f89878527bc679f01f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dea27ca99d63e43e6b0aa930b3ebbf5767b9ec3af80e50e6ea7f25059c0014b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818948068c75dcae789dd04d74629d38a8c8c7d00b4382e6015b7fd035227055(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c782f684d157afde64540324f5f82e0b0f863ad3b1dc23c61fd2fcc72643d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b415fe73dab62431fb7a05f0e71fec2d04de47a0db07fa94d8980ccc2497326e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorDataCollectionRuleDestinationsLogAnalytics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e09f04e010ada32c12dc4384179d3061aaa449ccbbbf9e0972c668346135b13(
    value: typing.Optional[MonitorDataCollectionRuleDestinations],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f613481b34a9e84eaf7bdfe27afa2f209b9c0450d6f6da0e76bf9978064eb832(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__748230ce1aa460add2b88e74b7b34e8e75cfb571cddd317414f030d656e633be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__623c9190f2692ff5b8c50f4dc7846c8ae43654b019829ffe7ce7255adebbe281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944eaa692cd5bc0f47db9e7de9ee30c53758ecdb4de0dbb2324c765bc500ed3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b21271d37530314d8a2a14fd460cbcf4ce1910df9dd7a122aa1902c42e21872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74dc6e72b4d4da7518e8afb87a7b1a96223dfeaf3705c734a9179cba1db15e4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff96d5437c456f564ff126f6b28b77cc57c6bb67a074dd8c94acac244b1d4bde(
    value: typing.Optional[typing.Union[MonitorDataCollectionRuleTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
