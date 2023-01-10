'''
# `google_game_services_game_server_config`

Refer to the Terraform Registory for docs: [`google_game_services_game_server_config`](https://www.terraform.io/docs/providers/google/r/game_services_game_server_config).
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


class GameServicesGameServerConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config google_game_services_game_server_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        config_id: builtins.str,
        deployment_id: builtins.str,
        fleet_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigFleetConfigs", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config google_game_services_game_server_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param config_id: A unique id for the deployment config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#config_id GameServicesGameServerConfig#config_id}
        :param deployment_id: A unique id for the deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#deployment_id GameServicesGameServerConfig#deployment_id}
        :param fleet_configs: fleet_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_configs GameServicesGameServerConfig#fleet_configs}
        :param description: The description of the game server config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#description GameServicesGameServerConfig#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#id GameServicesGameServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this game server config. Each label is a key-value pair. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        :param location: Location of the Deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#location GameServicesGameServerConfig#location}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#project GameServicesGameServerConfig#project}.
        :param scaling_configs: scaling_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#scaling_configs GameServicesGameServerConfig#scaling_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#timeouts GameServicesGameServerConfig#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d30415c3aadfe275499db8019d8fcddc361b32a7f6359cb1db83611d904dd6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GameServicesGameServerConfigConfig(
            config_id=config_id,
            deployment_id=deployment_id,
            fleet_configs=fleet_configs,
            description=description,
            id=id,
            labels=labels,
            location=location,
            project=project,
            scaling_configs=scaling_configs,
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

    @jsii.member(jsii_name="putFleetConfigs")
    def put_fleet_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigFleetConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da997db7f2d80f04ca35dcb6d91237191d9a8587e2e569ceb40ebd2e427ca9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFleetConfigs", [value]))

    @jsii.member(jsii_name="putScalingConfigs")
    def put_scaling_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a512022d158b61dd27a8712bebace4d5fb17e87e03655dbb044c3b93afd3096e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScalingConfigs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#create GameServicesGameServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#delete GameServicesGameServerConfig#delete}.
        '''
        value = GameServicesGameServerConfigTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetLocation")
    def reset_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocation", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetScalingConfigs")
    def reset_scaling_configs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScalingConfigs", []))

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
    @jsii.member(jsii_name="fleetConfigs")
    def fleet_configs(self) -> "GameServicesGameServerConfigFleetConfigsList":
        return typing.cast("GameServicesGameServerConfigFleetConfigsList", jsii.get(self, "fleetConfigs"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigs")
    def scaling_configs(self) -> "GameServicesGameServerConfigScalingConfigsList":
        return typing.cast("GameServicesGameServerConfigScalingConfigsList", jsii.get(self, "scalingConfigs"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "GameServicesGameServerConfigTimeoutsOutputReference":
        return typing.cast("GameServicesGameServerConfigTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="configIdInput")
    def config_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentIdInput")
    def deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetConfigsInput")
    def fleet_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]]], jsii.get(self, "fleetConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="scalingConfigsInput")
    def scaling_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]], jsii.get(self, "scalingConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="configId")
    def config_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configId"))

    @config_id.setter
    def config_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fd4b31c199ba5633f43ed02dea09c8c6d4024ed8c7ffc438b4eaad4d1d820a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configId", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__454415b9b8ae3b34ce2a4919d8bd003b4465a4d214a6071caccff7a0931b89ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a461237a67b97d95380101e31bd4677593441680f5507874e9427968be8fcf64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432969f149ec11da2b997cab6d348da540b4e359c86ef9c12b84f8a9905c3a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbe1aefb3719f17a9925c22b047e696b12e28ad57b3cf95469df6ffd7e751cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd9fdde47231e6652562d5044fc13d88bc88bc89db5c1f6aa326250f9a71beee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c0b6907380fb51ab8c00b7b391c43a162f2d635ce802ba6d2b8ad550b83b98d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "config_id": "configId",
        "deployment_id": "deploymentId",
        "fleet_configs": "fleetConfigs",
        "description": "description",
        "id": "id",
        "labels": "labels",
        "location": "location",
        "project": "project",
        "scaling_configs": "scalingConfigs",
        "timeouts": "timeouts",
    },
)
class GameServicesGameServerConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config_id: builtins.str,
        deployment_id: builtins.str,
        fleet_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigFleetConfigs", typing.Dict[builtins.str, typing.Any]]]],
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        location: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        scaling_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigs", typing.Dict[builtins.str, typing.Any]]]]] = None,
        timeouts: typing.Optional[typing.Union["GameServicesGameServerConfigTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param config_id: A unique id for the deployment config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#config_id GameServicesGameServerConfig#config_id}
        :param deployment_id: A unique id for the deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#deployment_id GameServicesGameServerConfig#deployment_id}
        :param fleet_configs: fleet_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_configs GameServicesGameServerConfig#fleet_configs}
        :param description: The description of the game server config. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#description GameServicesGameServerConfig#description}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#id GameServicesGameServerConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: The labels associated with this game server config. Each label is a key-value pair. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        :param location: Location of the Deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#location GameServicesGameServerConfig#location}
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#project GameServicesGameServerConfig#project}.
        :param scaling_configs: scaling_configs block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#scaling_configs GameServicesGameServerConfig#scaling_configs}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#timeouts GameServicesGameServerConfig#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GameServicesGameServerConfigTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23737af42c8625c021728d37a94069341fece78311b71a45c407fc7d21e1bdb1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument config_id", value=config_id, expected_type=type_hints["config_id"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument fleet_configs", value=fleet_configs, expected_type=type_hints["fleet_configs"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument scaling_configs", value=scaling_configs, expected_type=type_hints["scaling_configs"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_id": config_id,
            "deployment_id": deployment_id,
            "fleet_configs": fleet_configs,
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
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if location is not None:
            self._values["location"] = location
        if project is not None:
            self._values["project"] = project
        if scaling_configs is not None:
            self._values["scaling_configs"] = scaling_configs
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
    def config_id(self) -> builtins.str:
        '''A unique id for the deployment config.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#config_id GameServicesGameServerConfig#config_id}
        '''
        result = self._values.get("config_id")
        assert result is not None, "Required property 'config_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_id(self) -> builtins.str:
        '''A unique id for the deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#deployment_id GameServicesGameServerConfig#deployment_id}
        '''
        result = self._values.get("deployment_id")
        assert result is not None, "Required property 'deployment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fleet_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]]:
        '''fleet_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_configs GameServicesGameServerConfig#fleet_configs}
        '''
        result = self._values.get("fleet_configs")
        assert result is not None, "Required property 'fleet_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigFleetConfigs"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the game server config.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#description GameServicesGameServerConfig#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#id GameServicesGameServerConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The labels associated with this game server config. Each label is a key-value pair.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def location(self) -> typing.Optional[builtins.str]:
        '''Location of the Deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#location GameServicesGameServerConfig#location}
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#project GameServicesGameServerConfig#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configs(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]]:
        '''scaling_configs block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#scaling_configs GameServicesGameServerConfig#scaling_configs}
        '''
        result = self._values.get("scaling_configs")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigs"]]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["GameServicesGameServerConfigTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#timeouts GameServicesGameServerConfig#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GameServicesGameServerConfigTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigFleetConfigs",
    jsii_struct_bases=[],
    name_mapping={"fleet_spec": "fleetSpec", "name": "name"},
)
class GameServicesGameServerConfigFleetConfigs:
    def __init__(
        self,
        *,
        fleet_spec: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param fleet_spec: The fleet spec, which is sent to Agones to configure fleet. The spec can be passed as inline json but it is recommended to use a file reference instead. File references can contain the json or yaml format of the fleet spec. Eg: fleet_spec = jsonencode(yamldecode(file("fleet_configs.yaml"))) fleet_spec = file("fleet_configs.json") The format of the spec can be found : 'https://agones.dev/site/docs/reference/fleet/'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_spec GameServicesGameServerConfig#fleet_spec}
        :param name: The name of the FleetConfig. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912f71778548e3db67d8f0f1d51fa5faef863808bd1c7446484b9faf0fa8eab7)
            check_type(argname="argument fleet_spec", value=fleet_spec, expected_type=type_hints["fleet_spec"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fleet_spec": fleet_spec,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def fleet_spec(self) -> builtins.str:
        '''The fleet spec, which is sent to Agones to configure fleet.

        The spec can be passed as inline json but it is recommended to use a file reference
        instead. File references can contain the json or yaml format of the fleet spec. Eg:

        fleet_spec = jsonencode(yamldecode(file("fleet_configs.yaml")))
        fleet_spec = file("fleet_configs.json")

        The format of the spec can be found :
        'https://agones.dev/site/docs/reference/fleet/'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_spec GameServicesGameServerConfig#fleet_spec}
        '''
        result = self._values.get("fleet_spec")
        assert result is not None, "Required property 'fleet_spec' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the FleetConfig.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigFleetConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigFleetConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigFleetConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1751cd1e68cf0f27bb3a0be287d3466f2c1994f6e39153b1b5bea2a6a17b4d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GameServicesGameServerConfigFleetConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d97eecb481575cc495f91f09f9fbcaa2d530b96cb3e91e098b29e01900940c3e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigFleetConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686121e3cb7e71a778bfd4167ce830384b1b9fd8bc485552aebb285b7912fa3e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f0f018ed4bff6596b005a1d85a854ccec7083a766c6635da362ed5393b33ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__618aa433968e14843f7751915998b2126b1d4ded989b29cdb4c5e5d4611bd305)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa46056f4d91ae20212e5c024b598bfc3b486efb579011755417c5971e6326f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigFleetConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigFleetConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02fef1b4fee085753454a8d7895905df5255e48b56dc4cb73db1424d58a40e2c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @builtins.property
    @jsii.member(jsii_name="fleetSpecInput")
    def fleet_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetSpec")
    def fleet_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetSpec"))

    @fleet_spec.setter
    def fleet_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e36b2b9ef309d946e8defcd35ef5a04086a2490fc858fed1a894d270e57372a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetSpec", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad661d903aad99535c4d9ca1e1095f96a6bd6382756a52f9b4f633937489582)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4246b2eaab9f2d9849c71d076edb307d2d65a4875435e4fc2dfba6b7997440e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "fleet_autoscaler_spec": "fleetAutoscalerSpec",
        "name": "name",
        "schedules": "schedules",
        "selectors": "selectors",
    },
)
class GameServicesGameServerConfigScalingConfigs:
    def __init__(
        self,
        *,
        fleet_autoscaler_spec: builtins.str,
        name: builtins.str,
        schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSchedules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSelectors", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param fleet_autoscaler_spec: Fleet autoscaler spec, which is sent to Agones. Example spec can be found : https://agones.dev/site/docs/reference/fleetautoscaler/. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_autoscaler_spec GameServicesGameServerConfig#fleet_autoscaler_spec}
        :param name: The name of the ScalingConfig. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        :param schedules: schedules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#schedules GameServicesGameServerConfig#schedules}
        :param selectors: selectors block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#selectors GameServicesGameServerConfig#selectors}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__404257c9c0bb7a27e198c78410450b7b56d0640153d8e7de2698332ea393224b)
            check_type(argname="argument fleet_autoscaler_spec", value=fleet_autoscaler_spec, expected_type=type_hints["fleet_autoscaler_spec"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedules", value=schedules, expected_type=type_hints["schedules"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fleet_autoscaler_spec": fleet_autoscaler_spec,
            "name": name,
        }
        if schedules is not None:
            self._values["schedules"] = schedules
        if selectors is not None:
            self._values["selectors"] = selectors

    @builtins.property
    def fleet_autoscaler_spec(self) -> builtins.str:
        '''Fleet autoscaler spec, which is sent to Agones. Example spec can be found : https://agones.dev/site/docs/reference/fleetautoscaler/.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#fleet_autoscaler_spec GameServicesGameServerConfig#fleet_autoscaler_spec}
        '''
        result = self._values.get("fleet_autoscaler_spec")
        assert result is not None, "Required property 'fleet_autoscaler_spec' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the ScalingConfig.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#name GameServicesGameServerConfig#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]]:
        '''schedules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#schedules GameServicesGameServerConfig#schedules}
        '''
        result = self._values.get("schedules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]], result)

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]]:
        '''selectors block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#selectors GameServicesGameServerConfig#selectors}
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigScalingConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigScalingConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ca34144919362442e6862a8efb90cebfda21be06e3eb8c68b4403e8f654aa02)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GameServicesGameServerConfigScalingConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c59f6ef9d6f51fe9b24dffc2bb3568be4d4c16491ababe8a97035ad23d3038)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigScalingConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d551fe1971af3e90708b6383063e069dfa044f6898195c7b9bb873410cbdbc8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1516888ff4646067f58662a94e06635ce5e531aafa1cc97bab3ff23246cf5eb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__576c1c2cee006958f6d25d24f653a238c186a44a872a4dac9ad15b86d5fa4116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e98a5842eb27f25500f25b2e6e9af578c263cf348ebb7bbfe0f32e2e38c037a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigScalingConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda4f0fc05c771d273cdc8058abe5015f3dfa4f9b5ad4cb977a4ee660bd86a25)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSchedules")
    def put_schedules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSchedules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdbec448ce1e8f508f1c2be3085ad7f6d54508460580296971cdf1495ae97bba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSchedules", [value]))

    @jsii.member(jsii_name="putSelectors")
    def put_selectors(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerConfigScalingConfigsSelectors", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__383756848487b7a8728b8283e7b57c1643c16352adb7e8a9252e27dbc0688ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSelectors", [value]))

    @jsii.member(jsii_name="resetSchedules")
    def reset_schedules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedules", []))

    @jsii.member(jsii_name="resetSelectors")
    def reset_selectors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelectors", []))

    @builtins.property
    @jsii.member(jsii_name="schedules")
    def schedules(self) -> "GameServicesGameServerConfigScalingConfigsSchedulesList":
        return typing.cast("GameServicesGameServerConfigScalingConfigsSchedulesList", jsii.get(self, "schedules"))

    @builtins.property
    @jsii.member(jsii_name="selectors")
    def selectors(self) -> "GameServicesGameServerConfigScalingConfigsSelectorsList":
        return typing.cast("GameServicesGameServerConfigScalingConfigsSelectorsList", jsii.get(self, "selectors"))

    @builtins.property
    @jsii.member(jsii_name="fleetAutoscalerSpecInput")
    def fleet_autoscaler_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fleetAutoscalerSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="schedulesInput")
    def schedules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSchedules"]]], jsii.get(self, "schedulesInput"))

    @builtins.property
    @jsii.member(jsii_name="selectorsInput")
    def selectors_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerConfigScalingConfigsSelectors"]]], jsii.get(self, "selectorsInput"))

    @builtins.property
    @jsii.member(jsii_name="fleetAutoscalerSpec")
    def fleet_autoscaler_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fleetAutoscalerSpec"))

    @fleet_autoscaler_spec.setter
    def fleet_autoscaler_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0bef63bcbc6331b1261938fdef2c2b5484a27d2f5fc36bfe0b45a258399a534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fleetAutoscalerSpec", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d92c15ccd5420ab2c34ddf3d9df9d8d156219c513040f11b6abacd6258062db8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1567b7d68570f41b1441f9f0428aa93da47bbb0dc4bdaf693473c98056e6b81e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSchedules",
    jsii_struct_bases=[],
    name_mapping={
        "cron_job_duration": "cronJobDuration",
        "cron_spec": "cronSpec",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class GameServicesGameServerConfigScalingConfigsSchedules:
    def __init__(
        self,
        *,
        cron_job_duration: typing.Optional[builtins.str] = None,
        cron_spec: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cron_job_duration: The duration for the cron job event. The duration of the event is effective after the cron job's start time. A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_job_duration GameServicesGameServerConfig#cron_job_duration}
        :param cron_spec: The cron definition of the scheduled event. See https://en.wikipedia.org/wiki/Cron. Cron spec specifies the local time as defined by the realm. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_spec GameServicesGameServerConfig#cron_spec}
        :param end_time: The end time of the event. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#end_time GameServicesGameServerConfig#end_time}
        :param start_time: The start time of the event. A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z". Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#start_time GameServicesGameServerConfig#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fbd3f60ff951d25bfff200e1ef76f8dfb6b191f551ea2479acd0b07e5de9f1)
            check_type(argname="argument cron_job_duration", value=cron_job_duration, expected_type=type_hints["cron_job_duration"])
            check_type(argname="argument cron_spec", value=cron_spec, expected_type=type_hints["cron_spec"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_job_duration is not None:
            self._values["cron_job_duration"] = cron_job_duration
        if cron_spec is not None:
            self._values["cron_spec"] = cron_spec
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def cron_job_duration(self) -> typing.Optional[builtins.str]:
        '''The duration for the cron job event. The duration of the event is effective after the cron job's start time.

        A duration in seconds with up to nine fractional digits, terminated by 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_job_duration GameServicesGameServerConfig#cron_job_duration}
        '''
        result = self._values.get("cron_job_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cron_spec(self) -> typing.Optional[builtins.str]:
        '''The cron definition of the scheduled event. See https://en.wikipedia.org/wiki/Cron. Cron spec specifies the local time as defined by the realm.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#cron_spec GameServicesGameServerConfig#cron_spec}
        '''
        result = self._values.get("cron_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The end time of the event.

        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#end_time GameServicesGameServerConfig#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The start time of the event.

        A timestamp in RFC3339 UTC "Zulu" format, accurate to nanoseconds. Example: "2014-10-02T15:01:23.045123456Z".

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#start_time GameServicesGameServerConfig#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigScalingConfigsSchedules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigScalingConfigsSchedulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSchedulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72dcf50229964381910c6f744ca1cbefcb646360ecde53d2a2f57b0dc064937c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GameServicesGameServerConfigScalingConfigsSchedulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823cd1e2f231f112261ef94e8bfc1b21aee050338454ed3366903e83416c9f64)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigScalingConfigsSchedulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b8913f30e4a2b80fcdc57798a1d818d7b2ee17bb0e27379b32ef6c36bd6a7b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d51149633ef16a6b02f58504b10ff9454451bedce3f855b4c52465b6e6a78fda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d87d10252b057c26de135b54d946d501612ab99bde9cd37abe26b65fcfa057a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b651ac6c740f90654e67a12ba04b0f0b9adfe0813a8c83ffaeac1770c670a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigScalingConfigsSchedulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSchedulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8e19ed48d178ab0b4b1014dff2b91da15a2ee7cf4fe61106b0712aca94c2148)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCronJobDuration")
    def reset_cron_job_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronJobDuration", []))

    @jsii.member(jsii_name="resetCronSpec")
    def reset_cron_spec(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronSpec", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="cronJobDurationInput")
    def cron_job_duration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronJobDurationInput"))

    @builtins.property
    @jsii.member(jsii_name="cronSpecInput")
    def cron_spec_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronSpecInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="cronJobDuration")
    def cron_job_duration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronJobDuration"))

    @cron_job_duration.setter
    def cron_job_duration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1d10f521dca4c2d0c95807235d216888b391299d3f2e76aa3a31aa44de1b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronJobDuration", value)

    @builtins.property
    @jsii.member(jsii_name="cronSpec")
    def cron_spec(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronSpec"))

    @cron_spec.setter
    def cron_spec(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171aa8a04d8ee3ffdd4ad9034ccbc49f0241cacc4140821f5fd6c14569985171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronSpec", value)

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f966f778a58c411be52ccc342590251c3a7373857fbc1be7928b35881908b34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value)

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772ef0d116c483d3ae6e83bd5017fe2e11a9bc920ffdc0c95c44836237c45078)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa757cf4a95e4aebd2f246174c4d92f129c9200d55abcaa16f2f986a52b372c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSelectors",
    jsii_struct_bases=[],
    name_mapping={"labels": "labels"},
)
class GameServicesGameServerConfigScalingConfigsSelectors:
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param labels: Set of labels to group by. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b0c47cf56f39dddf2ccb2d6190c8faf0d021cb628b69eefe434030589ad8407)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Set of labels to group by.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#labels GameServicesGameServerConfig#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigScalingConfigsSelectors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigScalingConfigsSelectorsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSelectorsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced593db51ac79b30d20cc43b27291f1ecee6713a74398729c7319d87731ab05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GameServicesGameServerConfigScalingConfigsSelectorsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d224e44db3545fe9273fbdfd9a504d010b5a709118969730ecb125d97ed17b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerConfigScalingConfigsSelectorsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076e26033b0b828033e12b728b3d8e0c3baa71e76cd21992a57ecd9e86ac2411)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a75990b3996fc95659d471515867862134d1db17652cde4173a178b910bad857)
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
            type_hints = typing.get_type_hints(_typecheckingstub__945c785345c1d407d9d6314a84290c5802234d214790894fa51f536b97c46081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f901e5eeb6c9c769093d644344f0952cd6877b718f988cdc72a88a7f266d0920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerConfigScalingConfigsSelectorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigScalingConfigsSelectorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3215842100bff3993ee8766cdf35bdbb5f745b6a40484d0dafb1eb10bcb836)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164768e31257d2cc390805fb37576af6171521d2cbeed36ac610b55be3d884bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eecd89782c4046cfb1d420c3dab03ff7235dc772766a06f53e810fd15cd61f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class GameServicesGameServerConfigTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#create GameServicesGameServerConfig#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#delete GameServicesGameServerConfig#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78831315b63946dd009cfd7c688cb6f3de8c98ecbb58445478ba6de38a184feb)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#create GameServicesGameServerConfig#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_config#delete GameServicesGameServerConfig#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerConfigTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerConfigTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerConfig.GameServicesGameServerConfigTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__93c4250537b50343fb456857c5975c85093b040aa4cab305403db418f65d020d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cfeb850ea44ff0640235730bc28bca57307c338bc84764dad3100aed69e5793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__147d3936ee363475bea86797916fae9b3bd1cf8c177013d0d93d425053e67bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a8fc269220a9ef4a6f3cbfd693a376a6cb32da886c96793b340558afc18e75c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GameServicesGameServerConfig",
    "GameServicesGameServerConfigConfig",
    "GameServicesGameServerConfigFleetConfigs",
    "GameServicesGameServerConfigFleetConfigsList",
    "GameServicesGameServerConfigFleetConfigsOutputReference",
    "GameServicesGameServerConfigScalingConfigs",
    "GameServicesGameServerConfigScalingConfigsList",
    "GameServicesGameServerConfigScalingConfigsOutputReference",
    "GameServicesGameServerConfigScalingConfigsSchedules",
    "GameServicesGameServerConfigScalingConfigsSchedulesList",
    "GameServicesGameServerConfigScalingConfigsSchedulesOutputReference",
    "GameServicesGameServerConfigScalingConfigsSelectors",
    "GameServicesGameServerConfigScalingConfigsSelectorsList",
    "GameServicesGameServerConfigScalingConfigsSelectorsOutputReference",
    "GameServicesGameServerConfigTimeouts",
    "GameServicesGameServerConfigTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c3d30415c3aadfe275499db8019d8fcddc361b32a7f6359cb1db83611d904dd6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    config_id: builtins.str,
    deployment_id: builtins.str,
    fleet_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigFleetConfigs, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__da997db7f2d80f04ca35dcb6d91237191d9a8587e2e569ceb40ebd2e427ca9f8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigFleetConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a512022d158b61dd27a8712bebace4d5fb17e87e03655dbb044c3b93afd3096e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fd4b31c199ba5633f43ed02dea09c8c6d4024ed8c7ffc438b4eaad4d1d820a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__454415b9b8ae3b34ce2a4919d8bd003b4465a4d214a6071caccff7a0931b89ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a461237a67b97d95380101e31bd4677593441680f5507874e9427968be8fcf64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432969f149ec11da2b997cab6d348da540b4e359c86ef9c12b84f8a9905c3a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbe1aefb3719f17a9925c22b047e696b12e28ad57b3cf95469df6ffd7e751cec(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd9fdde47231e6652562d5044fc13d88bc88bc89db5c1f6aa326250f9a71beee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c0b6907380fb51ab8c00b7b391c43a162f2d635ce802ba6d2b8ad550b83b98d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23737af42c8625c021728d37a94069341fece78311b71a45c407fc7d21e1bdb1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config_id: builtins.str,
    deployment_id: builtins.str,
    fleet_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigFleetConfigs, typing.Dict[builtins.str, typing.Any]]]],
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    location: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    scaling_configs: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigs, typing.Dict[builtins.str, typing.Any]]]]] = None,
    timeouts: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912f71778548e3db67d8f0f1d51fa5faef863808bd1c7446484b9faf0fa8eab7(
    *,
    fleet_spec: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1751cd1e68cf0f27bb3a0be287d3466f2c1994f6e39153b1b5bea2a6a17b4d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d97eecb481575cc495f91f09f9fbcaa2d530b96cb3e91e098b29e01900940c3e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686121e3cb7e71a778bfd4167ce830384b1b9fd8bc485552aebb285b7912fa3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f0f018ed4bff6596b005a1d85a854ccec7083a766c6635da362ed5393b33ec(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618aa433968e14843f7751915998b2126b1d4ded989b29cdb4c5e5d4611bd305(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa46056f4d91ae20212e5c024b598bfc3b486efb579011755417c5971e6326f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigFleetConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02fef1b4fee085753454a8d7895905df5255e48b56dc4cb73db1424d58a40e2c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36b2b9ef309d946e8defcd35ef5a04086a2490fc858fed1a894d270e57372a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad661d903aad99535c4d9ca1e1095f96a6bd6382756a52f9b4f633937489582(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4246b2eaab9f2d9849c71d076edb307d2d65a4875435e4fc2dfba6b7997440e0(
    value: typing.Optional[typing.Union[GameServicesGameServerConfigFleetConfigs, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__404257c9c0bb7a27e198c78410450b7b56d0640153d8e7de2698332ea393224b(
    *,
    fleet_autoscaler_spec: builtins.str,
    name: builtins.str,
    schedules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    selectors: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca34144919362442e6862a8efb90cebfda21be06e3eb8c68b4403e8f654aa02(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c59f6ef9d6f51fe9b24dffc2bb3568be4d4c16491ababe8a97035ad23d3038(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d551fe1971af3e90708b6383063e069dfa044f6898195c7b9bb873410cbdbc8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1516888ff4646067f58662a94e06635ce5e531aafa1cc97bab3ff23246cf5eb0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__576c1c2cee006958f6d25d24f653a238c186a44a872a4dac9ad15b86d5fa4116(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e98a5842eb27f25500f25b2e6e9af578c263cf348ebb7bbfe0f32e2e38c037a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda4f0fc05c771d273cdc8058abe5015f3dfa4f9b5ad4cb977a4ee660bd86a25(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdbec448ce1e8f508f1c2be3085ad7f6d54508460580296971cdf1495ae97bba(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__383756848487b7a8728b8283e7b57c1643c16352adb7e8a9252e27dbc0688ce1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0bef63bcbc6331b1261938fdef2c2b5484a27d2f5fc36bfe0b45a258399a534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d92c15ccd5420ab2c34ddf3d9df9d8d156219c513040f11b6abacd6258062db8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1567b7d68570f41b1441f9f0428aa93da47bbb0dc4bdaf693473c98056e6b81e(
    value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigs, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fbd3f60ff951d25bfff200e1ef76f8dfb6b191f551ea2479acd0b07e5de9f1(
    *,
    cron_job_duration: typing.Optional[builtins.str] = None,
    cron_spec: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72dcf50229964381910c6f744ca1cbefcb646360ecde53d2a2f57b0dc064937c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823cd1e2f231f112261ef94e8bfc1b21aee050338454ed3366903e83416c9f64(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b8913f30e4a2b80fcdc57798a1d818d7b2ee17bb0e27379b32ef6c36bd6a7b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51149633ef16a6b02f58504b10ff9454451bedce3f855b4c52465b6e6a78fda(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d87d10252b057c26de135b54d946d501612ab99bde9cd37abe26b65fcfa057a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b651ac6c740f90654e67a12ba04b0f0b9adfe0813a8c83ffaeac1770c670a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSchedules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e19ed48d178ab0b4b1014dff2b91da15a2ee7cf4fe61106b0712aca94c2148(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1d10f521dca4c2d0c95807235d216888b391299d3f2e76aa3a31aa44de1b02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171aa8a04d8ee3ffdd4ad9034ccbc49f0241cacc4140821f5fd6c14569985171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f966f778a58c411be52ccc342590251c3a7373857fbc1be7928b35881908b34(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772ef0d116c483d3ae6e83bd5017fe2e11a9bc920ffdc0c95c44836237c45078(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa757cf4a95e4aebd2f246174c4d92f129c9200d55abcaa16f2f986a52b372c8(
    value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSchedules, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0c47cf56f39dddf2ccb2d6190c8faf0d021cb628b69eefe434030589ad8407(
    *,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced593db51ac79b30d20cc43b27291f1ecee6713a74398729c7319d87731ab05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d224e44db3545fe9273fbdfd9a504d010b5a709118969730ecb125d97ed17b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076e26033b0b828033e12b728b3d8e0c3baa71e76cd21992a57ecd9e86ac2411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a75990b3996fc95659d471515867862134d1db17652cde4173a178b910bad857(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__945c785345c1d407d9d6314a84290c5802234d214790894fa51f536b97c46081(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f901e5eeb6c9c769093d644344f0952cd6877b718f988cdc72a88a7f266d0920(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerConfigScalingConfigsSelectors]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3215842100bff3993ee8766cdf35bdbb5f745b6a40484d0dafb1eb10bcb836(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164768e31257d2cc390805fb37576af6171521d2cbeed36ac610b55be3d884bc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eecd89782c4046cfb1d420c3dab03ff7235dc772766a06f53e810fd15cd61f9c(
    value: typing.Optional[typing.Union[GameServicesGameServerConfigScalingConfigsSelectors, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78831315b63946dd009cfd7c688cb6f3de8c98ecbb58445478ba6de38a184feb(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c4250537b50343fb456857c5975c85093b040aa4cab305403db418f65d020d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfeb850ea44ff0640235730bc28bca57307c338bc84764dad3100aed69e5793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__147d3936ee363475bea86797916fae9b3bd1cf8c177013d0d93d425053e67bc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a8fc269220a9ef4a6f3cbfd693a376a6cb32da886c96793b340558afc18e75c(
    value: typing.Optional[typing.Union[GameServicesGameServerConfigTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
