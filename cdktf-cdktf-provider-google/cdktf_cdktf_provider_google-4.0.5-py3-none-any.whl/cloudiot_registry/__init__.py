'''
# `google_cloudiot_registry`

Refer to the Terraform Registory for docs: [`google_cloudiot_registry`](https://www.terraform.io/docs/providers/google/r/cloudiot_registry).
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


class CloudiotRegistry(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistry",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry google_cloudiot_registry}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudiotRegistryCredentials", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudiotRegistryEventNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        mqtt_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state_notification_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CloudiotRegistryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry google_cloudiot_registry} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: A unique name for the resource, required by device registry. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#name CloudiotRegistry#name}
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#credentials CloudiotRegistry#credentials}
        :param event_notification_configs: event_notification_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#event_notification_configs CloudiotRegistry#event_notification_configs}
        :param http_config: Activate or deactivate HTTP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#http_config CloudiotRegistry#http_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#id CloudiotRegistry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_level: The default logging verbosity for activity from devices in this registry. Specifies which events should be written to logs. For example, if the LogLevel is ERROR, only events that terminate in errors will be logged. LogLevel is inclusive; enabling INFO logging will also enable ERROR logging. Default value: "NONE" Possible values: ["NONE", "ERROR", "INFO", "DEBUG"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#log_level CloudiotRegistry#log_level}
        :param mqtt_config: Activate or deactivate MQTT. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#mqtt_config CloudiotRegistry#mqtt_config}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#project CloudiotRegistry#project}.
        :param region: The region in which the created registry should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#region CloudiotRegistry#region}
        :param state_notification_config: A PubSub topic to publish device state updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#state_notification_config CloudiotRegistry#state_notification_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#timeouts CloudiotRegistry#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72820b479bf7786f4b42aa71a21103ba5f0f6371645759a2056d3c812d51183a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudiotRegistryConfig(
            name=name,
            credentials=credentials,
            event_notification_configs=event_notification_configs,
            http_config=http_config,
            id=id,
            log_level=log_level,
            mqtt_config=mqtt_config,
            project=project,
            region=region,
            state_notification_config=state_notification_config,
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

    @jsii.member(jsii_name="putCredentials")
    def put_credentials(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudiotRegistryCredentials", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__174f9a04f8ca2fcd013488d9083f235a24b89779fbc9f6e3b23d5e60e150d398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCredentials", [value]))

    @jsii.member(jsii_name="putEventNotificationConfigs")
    def put_event_notification_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudiotRegistryEventNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e627adf354125cd5e2f1eef548e9a08dc1b3a6050c1f24cbf6abe8d74d24d298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventNotificationConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#create CloudiotRegistry#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#delete CloudiotRegistry#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#update CloudiotRegistry#update}.
        '''
        value = CloudiotRegistryTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCredentials")
    def reset_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCredentials", []))

    @jsii.member(jsii_name="resetEventNotificationConfigs")
    def reset_event_notification_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventNotificationConfigs", []))

    @jsii.member(jsii_name="resetHttpConfig")
    def reset_http_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogLevel")
    def reset_log_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogLevel", []))

    @jsii.member(jsii_name="resetMqttConfig")
    def reset_mqtt_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMqttConfig", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStateNotificationConfig")
    def reset_state_notification_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStateNotificationConfig", []))

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
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> "CloudiotRegistryCredentialsList":
        return typing.cast("CloudiotRegistryCredentialsList", jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="eventNotificationConfigs")
    def event_notification_configs(
        self,
    ) -> "CloudiotRegistryEventNotificationConfigsList":
        return typing.cast("CloudiotRegistryEventNotificationConfigsList", jsii.get(self, "eventNotificationConfigs"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "CloudiotRegistryTimeoutsOutputReference":
        return typing.cast("CloudiotRegistryTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="credentialsInput")
    def credentials_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryCredentials"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryCredentials"]]], jsii.get(self, "credentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventNotificationConfigsInput")
    def event_notification_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryEventNotificationConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryEventNotificationConfigs"]]], jsii.get(self, "eventNotificationConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpConfigInput")
    def http_config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "httpConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logLevelInput")
    def log_level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logLevelInput"))

    @builtins.property
    @jsii.member(jsii_name="mqttConfigInput")
    def mqtt_config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "mqttConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="stateNotificationConfigInput")
    def state_notification_config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "stateNotificationConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["CloudiotRegistryTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["CloudiotRegistryTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="httpConfig")
    def http_config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "httpConfig"))

    @http_config.setter
    def http_config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dacde5045954722148bf1858f12a820e2843d1575be59f3a02bf9e75148c798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpConfig", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa6a6881270814a1c46ec101f16d8ae7d50d6ef7a81cb065ba23afa8769ace1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="logLevel")
    def log_level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logLevel"))

    @log_level.setter
    def log_level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16716bcd48cbbc59b0675081e7f62de8763cc4425da5b5bdc97d9fa31bcfd89e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logLevel", value)

    @builtins.property
    @jsii.member(jsii_name="mqttConfig")
    def mqtt_config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "mqttConfig"))

    @mqtt_config.setter
    def mqtt_config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__039c82b02148410b7d72fcdc8ef3ba1f0433a36c5377067323490d75e7b35d0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mqttConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1feca3803312ce6f59317d34446f854c5859a9ba556522c130844ace63a269aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c87d5891c9da38a84ad98cf224de673678e2530062ad13bc1b76aafe66e598c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbb14c93040a57629df7d74ce72abcae30f06fd27c6dcb02d0db95e27a3b84a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="stateNotificationConfig")
    def state_notification_config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "stateNotificationConfig"))

    @state_notification_config.setter
    def state_notification_config(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72085a3f7bf3684141b730b4eda376ec1d8022e127f901a6700f36da732fc687)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateNotificationConfig", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryConfig",
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
        "credentials": "credentials",
        "event_notification_configs": "eventNotificationConfigs",
        "http_config": "httpConfig",
        "id": "id",
        "log_level": "logLevel",
        "mqtt_config": "mqttConfig",
        "project": "project",
        "region": "region",
        "state_notification_config": "stateNotificationConfig",
        "timeouts": "timeouts",
    },
)
class CloudiotRegistryConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudiotRegistryCredentials", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudiotRegistryEventNotificationConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        http_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_level: typing.Optional[builtins.str] = None,
        mqtt_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        project: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        state_notification_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["CloudiotRegistryTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: A unique name for the resource, required by device registry. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#name CloudiotRegistry#name}
        :param credentials: credentials block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#credentials CloudiotRegistry#credentials}
        :param event_notification_configs: event_notification_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#event_notification_configs CloudiotRegistry#event_notification_configs}
        :param http_config: Activate or deactivate HTTP. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#http_config CloudiotRegistry#http_config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#id CloudiotRegistry#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_level: The default logging verbosity for activity from devices in this registry. Specifies which events should be written to logs. For example, if the LogLevel is ERROR, only events that terminate in errors will be logged. LogLevel is inclusive; enabling INFO logging will also enable ERROR logging. Default value: "NONE" Possible values: ["NONE", "ERROR", "INFO", "DEBUG"] Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#log_level CloudiotRegistry#log_level}
        :param mqtt_config: Activate or deactivate MQTT. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#mqtt_config CloudiotRegistry#mqtt_config}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#project CloudiotRegistry#project}.
        :param region: The region in which the created registry should reside. If it is not provided, the provider region is used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#region CloudiotRegistry#region}
        :param state_notification_config: A PubSub topic to publish device state updates. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#state_notification_config CloudiotRegistry#state_notification_config}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#timeouts CloudiotRegistry#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = CloudiotRegistryTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2b797d57c816533946c0ab566d35c2323d99d2582a9463ba9039b9047e70bd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument event_notification_configs", value=event_notification_configs, expected_type=type_hints["event_notification_configs"])
            check_type(argname="argument http_config", value=http_config, expected_type=type_hints["http_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument mqtt_config", value=mqtt_config, expected_type=type_hints["mqtt_config"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument state_notification_config", value=state_notification_config, expected_type=type_hints["state_notification_config"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
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
        if credentials is not None:
            self._values["credentials"] = credentials
        if event_notification_configs is not None:
            self._values["event_notification_configs"] = event_notification_configs
        if http_config is not None:
            self._values["http_config"] = http_config
        if id is not None:
            self._values["id"] = id
        if log_level is not None:
            self._values["log_level"] = log_level
        if mqtt_config is not None:
            self._values["mqtt_config"] = mqtt_config
        if project is not None:
            self._values["project"] = project
        if region is not None:
            self._values["region"] = region
        if state_notification_config is not None:
            self._values["state_notification_config"] = state_notification_config
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
    def name(self) -> builtins.str:
        '''A unique name for the resource, required by device registry.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#name CloudiotRegistry#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryCredentials"]]]:
        '''credentials block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#credentials CloudiotRegistry#credentials}
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryCredentials"]]], result)

    @builtins.property
    def event_notification_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryEventNotificationConfigs"]]]:
        '''event_notification_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#event_notification_configs CloudiotRegistry#event_notification_configs}
        '''
        result = self._values.get("event_notification_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudiotRegistryEventNotificationConfigs"]]], result)

    @builtins.property
    def http_config(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Activate or deactivate HTTP.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#http_config CloudiotRegistry#http_config}
        '''
        result = self._values.get("http_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#id CloudiotRegistry#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_level(self) -> typing.Optional[builtins.str]:
        '''The default logging verbosity for activity from devices in this registry.

        Specifies which events should be written to logs. For
        example, if the LogLevel is ERROR, only events that terminate in
        errors will be logged. LogLevel is inclusive; enabling INFO logging
        will also enable ERROR logging. Default value: "NONE" Possible values: ["NONE", "ERROR", "INFO", "DEBUG"]

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#log_level CloudiotRegistry#log_level}
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mqtt_config(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Activate or deactivate MQTT.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#mqtt_config CloudiotRegistry#mqtt_config}
        '''
        result = self._values.get("mqtt_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#project CloudiotRegistry#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The region in which the created registry should reside. If it is not provided, the provider region is used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#region CloudiotRegistry#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state_notification_config(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A PubSub topic to publish device state updates.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#state_notification_config CloudiotRegistry#state_notification_config}
        '''
        result = self._values.get("state_notification_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["CloudiotRegistryTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#timeouts CloudiotRegistry#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["CloudiotRegistryTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudiotRegistryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryCredentials",
    jsii_struct_bases=[],
    name_mapping={"public_key_certificate": "publicKeyCertificate"},
)
class CloudiotRegistryCredentials:
    def __init__(
        self,
        *,
        public_key_certificate: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param public_key_certificate: A public key certificate format and data. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#public_key_certificate CloudiotRegistry#public_key_certificate}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c5812ad14f1ec1a4bec8c709f15b92227e7a5f73c13ae95e8a2757fe6030cc)
            check_type(argname="argument public_key_certificate", value=public_key_certificate, expected_type=type_hints["public_key_certificate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key_certificate": public_key_certificate,
        }

    @builtins.property
    def public_key_certificate(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''A public key certificate format and data.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#public_key_certificate CloudiotRegistry#public_key_certificate}
        '''
        result = self._values.get("public_key_certificate")
        assert result is not None, "Required property 'public_key_certificate' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudiotRegistryCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudiotRegistryCredentialsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryCredentialsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8593e3577de4f169941439ef2b416d1cdc941f88067b8e7c3acb1eb639362aea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CloudiotRegistryCredentialsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2860aca50840f8d4a7f41330553f58cc327dfebbedd4cdb87c7660194421c9cb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudiotRegistryCredentialsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282c6fde62ce4ab908e7a28ca5b27e0beb04250565b7599be041c70b2a3267b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dd38f921272b24f4e9c68a0fdad52132872d64cffba2ad50ec854f03c0337ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c276123bd2959e3d96bfb2d4d14105f512636280276a25e7e33dadaac0cd7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryCredentials]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryCredentials]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryCredentials]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321a89e6d46f000a45c314e0d332cb5ae19b6b0a1a13f68de873babb745728d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CloudiotRegistryCredentialsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryCredentialsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f4874445a8b93b13f67770e4ec6f0a2631613389cb799959bee366a574a69c8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="publicKeyCertificateInput")
    def public_key_certificate_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "publicKeyCertificateInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyCertificate")
    def public_key_certificate(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "publicKeyCertificate"))

    @public_key_certificate.setter
    def public_key_certificate(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__490aa13f5c0d7b35b60633f6f35c95d6f861fbd2e90f595edf878b21b81c415e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyCertificate", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudiotRegistryCredentials, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudiotRegistryCredentials, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudiotRegistryCredentials, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd391558013415e3c1eae34c55c433c54f659cdfe24fa232d2151acee65e4da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryEventNotificationConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "pubsub_topic_name": "pubsubTopicName",
        "subfolder_matches": "subfolderMatches",
    },
)
class CloudiotRegistryEventNotificationConfigs:
    def __init__(
        self,
        *,
        pubsub_topic_name: builtins.str,
        subfolder_matches: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param pubsub_topic_name: PubSub topic name to publish device events. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#pubsub_topic_name CloudiotRegistry#pubsub_topic_name}
        :param subfolder_matches: If the subfolder name matches this string exactly, this configuration will be used. The string must not include the leading '/' character. If empty, all strings are matched. Empty value can only be used for the last 'event_notification_configs' item. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#subfolder_matches CloudiotRegistry#subfolder_matches}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa6516375babf72f4237d30d7bcda91e0ecea5d5d106da304e2f706ba00349e)
            check_type(argname="argument pubsub_topic_name", value=pubsub_topic_name, expected_type=type_hints["pubsub_topic_name"])
            check_type(argname="argument subfolder_matches", value=subfolder_matches, expected_type=type_hints["subfolder_matches"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pubsub_topic_name": pubsub_topic_name,
        }
        if subfolder_matches is not None:
            self._values["subfolder_matches"] = subfolder_matches

    @builtins.property
    def pubsub_topic_name(self) -> builtins.str:
        '''PubSub topic name to publish device events.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#pubsub_topic_name CloudiotRegistry#pubsub_topic_name}
        '''
        result = self._values.get("pubsub_topic_name")
        assert result is not None, "Required property 'pubsub_topic_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subfolder_matches(self) -> typing.Optional[builtins.str]:
        '''If the subfolder name matches this string exactly, this configuration will be used.

        The string must not include the
        leading '/' character. If empty, all strings are matched. Empty
        value can only be used for the last 'event_notification_configs'
        item.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#subfolder_matches CloudiotRegistry#subfolder_matches}
        '''
        result = self._values.get("subfolder_matches")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudiotRegistryEventNotificationConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudiotRegistryEventNotificationConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryEventNotificationConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a0b0d41495d72841792cf4bc27b74e15bb4124416a581cfbd32ee61b6572c46)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudiotRegistryEventNotificationConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73ab78d4d0a9f27df953e51d1fb6e28cd89146d76bb6381cce02fe923f73ad43)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudiotRegistryEventNotificationConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74111da4583f02b0263a87c45dc5f56f39135bd9b66c3b91df99f9fdaa81030b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9894f3f5180123f085c2ab507c62fa6e885e0685ae8742c72d2dc738a2cfd7fd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db61b1092adc9ea5978795afe666d8aca7d2bb5828babb15fdf8c76d1cfda83e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryEventNotificationConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryEventNotificationConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryEventNotificationConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40904fc318a0fa829d521fc4206a0d8fad011df854289bba68a00e14c2c68ebe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CloudiotRegistryEventNotificationConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryEventNotificationConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a87a49c02ed96544f8bdf82728ebe73b2b16af4f265cf6dfa5e3ba927d233861)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSubfolderMatches")
    def reset_subfolder_matches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubfolderMatches", []))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicNameInput")
    def pubsub_topic_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pubsubTopicNameInput"))

    @builtins.property
    @jsii.member(jsii_name="subfolderMatchesInput")
    def subfolder_matches_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subfolderMatchesInput"))

    @builtins.property
    @jsii.member(jsii_name="pubsubTopicName")
    def pubsub_topic_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pubsubTopicName"))

    @pubsub_topic_name.setter
    def pubsub_topic_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d37a9ae68c12e9f8da65d6f206191019ffc0f86e7aa9812b16da38be6722b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pubsubTopicName", value)

    @builtins.property
    @jsii.member(jsii_name="subfolderMatches")
    def subfolder_matches(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subfolderMatches"))

    @subfolder_matches.setter
    def subfolder_matches(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e9a854db80bc332ef86b36ad0ff4c59d79bccfc1a99d416be781290c947c21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subfolderMatches", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudiotRegistryEventNotificationConfigs, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudiotRegistryEventNotificationConfigs, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudiotRegistryEventNotificationConfigs, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20c8a106aff21bdeb0f5d40b3dc129c5e0d835498138817e655baa8bb551f840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class CloudiotRegistryTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#create CloudiotRegistry#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#delete CloudiotRegistry#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#update CloudiotRegistry#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4e81a255c13e9e89abbd3d744dbe77c0dde360da1e53f7fec9eed3e6eaed7c1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#create CloudiotRegistry#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#delete CloudiotRegistry#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/cloudiot_registry#update CloudiotRegistry#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudiotRegistryTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudiotRegistryTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.cloudiotRegistry.CloudiotRegistryTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f99dfedfcb6aa9dde0a2d296daf62a86e83b5806717ca97adeaba6cbab44aea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e8254b7f335bc1481ddf7eaa1b7275d26800269c0ada8aa3577ada4fdf96fcf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd334ec2768769edd4909e2902a2534278755a9b0bd9318973ab87db6d1b33a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e56ac8a14240ca9faf0462e98b53709530f34b076f3b5ce1562c5855c11b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[CloudiotRegistryTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[CloudiotRegistryTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[CloudiotRegistryTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676a87148056fc22772e2f9541da55c226a6c3ce9ecf99499c364c518b2e1eb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "CloudiotRegistry",
    "CloudiotRegistryConfig",
    "CloudiotRegistryCredentials",
    "CloudiotRegistryCredentialsList",
    "CloudiotRegistryCredentialsOutputReference",
    "CloudiotRegistryEventNotificationConfigs",
    "CloudiotRegistryEventNotificationConfigsList",
    "CloudiotRegistryEventNotificationConfigsOutputReference",
    "CloudiotRegistryTimeouts",
    "CloudiotRegistryTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__72820b479bf7786f4b42aa71a21103ba5f0f6371645759a2056d3c812d51183a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudiotRegistryCredentials, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudiotRegistryEventNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mqtt_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state_notification_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CloudiotRegistryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__174f9a04f8ca2fcd013488d9083f235a24b89779fbc9f6e3b23d5e60e150d398(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudiotRegistryCredentials, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e627adf354125cd5e2f1eef548e9a08dc1b3a6050c1f24cbf6abe8d74d24d298(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudiotRegistryEventNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dacde5045954722148bf1858f12a820e2843d1575be59f3a02bf9e75148c798(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa6a6881270814a1c46ec101f16d8ae7d50d6ef7a81cb065ba23afa8769ace1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16716bcd48cbbc59b0675081e7f62de8763cc4425da5b5bdc97d9fa31bcfd89e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039c82b02148410b7d72fcdc8ef3ba1f0433a36c5377067323490d75e7b35d0a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1feca3803312ce6f59317d34446f854c5859a9ba556522c130844ace63a269aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c87d5891c9da38a84ad98cf224de673678e2530062ad13bc1b76aafe66e598c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbb14c93040a57629df7d74ce72abcae30f06fd27c6dcb02d0db95e27a3b84a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72085a3f7bf3684141b730b4eda376ec1d8022e127f901a6700f36da732fc687(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2b797d57c816533946c0ab566d35c2323d99d2582a9463ba9039b9047e70bd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    credentials: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudiotRegistryCredentials, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_notification_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudiotRegistryEventNotificationConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    http_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_level: typing.Optional[builtins.str] = None,
    mqtt_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    project: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    state_notification_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[CloudiotRegistryTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c5812ad14f1ec1a4bec8c709f15b92227e7a5f73c13ae95e8a2757fe6030cc(
    *,
    public_key_certificate: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8593e3577de4f169941439ef2b416d1cdc941f88067b8e7c3acb1eb639362aea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2860aca50840f8d4a7f41330553f58cc327dfebbedd4cdb87c7660194421c9cb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282c6fde62ce4ab908e7a28ca5b27e0beb04250565b7599be041c70b2a3267b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd38f921272b24f4e9c68a0fdad52132872d64cffba2ad50ec854f03c0337ae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c276123bd2959e3d96bfb2d4d14105f512636280276a25e7e33dadaac0cd7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321a89e6d46f000a45c314e0d332cb5ae19b6b0a1a13f68de873babb745728d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryCredentials]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f4874445a8b93b13f67770e4ec6f0a2631613389cb799959bee366a574a69c8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490aa13f5c0d7b35b60633f6f35c95d6f861fbd2e90f595edf878b21b81c415e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd391558013415e3c1eae34c55c433c54f659cdfe24fa232d2151acee65e4da1(
    value: typing.Optional[typing.Union[CloudiotRegistryCredentials, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa6516375babf72f4237d30d7bcda91e0ecea5d5d106da304e2f706ba00349e(
    *,
    pubsub_topic_name: builtins.str,
    subfolder_matches: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0b0d41495d72841792cf4bc27b74e15bb4124416a581cfbd32ee61b6572c46(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ab78d4d0a9f27df953e51d1fb6e28cd89146d76bb6381cce02fe923f73ad43(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74111da4583f02b0263a87c45dc5f56f39135bd9b66c3b91df99f9fdaa81030b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9894f3f5180123f085c2ab507c62fa6e885e0685ae8742c72d2dc738a2cfd7fd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db61b1092adc9ea5978795afe666d8aca7d2bb5828babb15fdf8c76d1cfda83e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40904fc318a0fa829d521fc4206a0d8fad011df854289bba68a00e14c2c68ebe(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudiotRegistryEventNotificationConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87a49c02ed96544f8bdf82728ebe73b2b16af4f265cf6dfa5e3ba927d233861(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d37a9ae68c12e9f8da65d6f206191019ffc0f86e7aa9812b16da38be6722b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e9a854db80bc332ef86b36ad0ff4c59d79bccfc1a99d416be781290c947c21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20c8a106aff21bdeb0f5d40b3dc129c5e0d835498138817e655baa8bb551f840(
    value: typing.Optional[typing.Union[CloudiotRegistryEventNotificationConfigs, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4e81a255c13e9e89abbd3d744dbe77c0dde360da1e53f7fec9eed3e6eaed7c1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f99dfedfcb6aa9dde0a2d296daf62a86e83b5806717ca97adeaba6cbab44aea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8254b7f335bc1481ddf7eaa1b7275d26800269c0ada8aa3577ada4fdf96fcf3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd334ec2768769edd4909e2902a2534278755a9b0bd9318973ab87db6d1b33a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e56ac8a14240ca9faf0462e98b53709530f34b076f3b5ce1562c5855c11b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676a87148056fc22772e2f9541da55c226a6c3ce9ecf99499c364c518b2e1eb4(
    value: typing.Optional[typing.Union[CloudiotRegistryTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
