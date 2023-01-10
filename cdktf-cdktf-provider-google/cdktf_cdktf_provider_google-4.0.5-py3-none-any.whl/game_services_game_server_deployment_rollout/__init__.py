'''
# `google_game_services_game_server_deployment_rollout`

Refer to the Terraform Registory for docs: [`google_game_services_game_server_deployment_rollout`](https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout).
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


class GameServicesGameServerDeploymentRollout(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRollout",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout google_game_services_game_server_deployment_rollout}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        default_game_server_config: builtins.str,
        deployment_id: builtins.str,
        game_server_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GameServicesGameServerDeploymentRolloutTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout google_game_services_game_server_deployment_rollout} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param default_game_server_config: This field points to the game server config that is applied by default to all realms and clusters. For example,. 'projects/my-project/locations/global/gameServerDeployments/my-game/configs/my-config'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#default_game_server_config GameServicesGameServerDeploymentRollout#default_game_server_config}
        :param deployment_id: The deployment to rollout the new config to. Only 1 rollout must be associated with each deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#deployment_id GameServicesGameServerDeploymentRollout#deployment_id}
        :param game_server_config_overrides: game_server_config_overrides block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#game_server_config_overrides GameServicesGameServerDeploymentRollout#game_server_config_overrides}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#id GameServicesGameServerDeploymentRollout#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#project GameServicesGameServerDeploymentRollout#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#timeouts GameServicesGameServerDeploymentRollout#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16d931b28160b911ad1bf9d5cb920a251c5b5e69f7d72f7994e735b6e3108c14)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GameServicesGameServerDeploymentRolloutConfig(
            default_game_server_config=default_game_server_config,
            deployment_id=deployment_id,
            game_server_config_overrides=game_server_config_overrides,
            id=id,
            project=project,
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

    @jsii.member(jsii_name="putGameServerConfigOverrides")
    def put_game_server_config_overrides(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b569fadfb67be866404a3bfb9f5ce7ca182f66da4f2438168ebbc7d1c92d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGameServerConfigOverrides", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#create GameServicesGameServerDeploymentRollout#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#delete GameServicesGameServerDeploymentRollout#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#update GameServicesGameServerDeploymentRollout#update}.
        '''
        value = GameServicesGameServerDeploymentRolloutTimeouts(
            create=create, delete=delete, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetGameServerConfigOverrides")
    def reset_game_server_config_overrides(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGameServerConfigOverrides", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

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
    @jsii.member(jsii_name="gameServerConfigOverrides")
    def game_server_config_overrides(
        self,
    ) -> "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesList":
        return typing.cast("GameServicesGameServerDeploymentRolloutGameServerConfigOverridesList", jsii.get(self, "gameServerConfigOverrides"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "GameServicesGameServerDeploymentRolloutTimeoutsOutputReference":
        return typing.cast("GameServicesGameServerDeploymentRolloutTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="defaultGameServerConfigInput")
    def default_game_server_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultGameServerConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentIdInput")
    def deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="gameServerConfigOverridesInput")
    def game_server_config_overrides_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides"]]], jsii.get(self, "gameServerConfigOverridesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["GameServicesGameServerDeploymentRolloutTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["GameServicesGameServerDeploymentRolloutTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultGameServerConfig")
    def default_game_server_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultGameServerConfig"))

    @default_game_server_config.setter
    def default_game_server_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4791ca1b2e313f7debfa814feaadd59a7a5dd3a95caa76659ef575952cf4ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultGameServerConfig", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e4b227b8d4e89a5b00f0deadb44042575b63ea57e21fbf0a0de8269574d411c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80eee7d27aa8b00f928985c139d93b91d05be307c2c4a0ffdbb9270ac6574987)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323316f0960893e4f499225ae259824f3a37b48bf76be6839058b166b70a2dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "default_game_server_config": "defaultGameServerConfig",
        "deployment_id": "deploymentId",
        "game_server_config_overrides": "gameServerConfigOverrides",
        "id": "id",
        "project": "project",
        "timeouts": "timeouts",
    },
)
class GameServicesGameServerDeploymentRolloutConfig(
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
        default_game_server_config: builtins.str,
        deployment_id: builtins.str,
        game_server_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["GameServicesGameServerDeploymentRolloutTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param default_game_server_config: This field points to the game server config that is applied by default to all realms and clusters. For example,. 'projects/my-project/locations/global/gameServerDeployments/my-game/configs/my-config'. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#default_game_server_config GameServicesGameServerDeploymentRollout#default_game_server_config}
        :param deployment_id: The deployment to rollout the new config to. Only 1 rollout must be associated with each deployment. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#deployment_id GameServicesGameServerDeploymentRollout#deployment_id}
        :param game_server_config_overrides: game_server_config_overrides block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#game_server_config_overrides GameServicesGameServerDeploymentRollout#game_server_config_overrides}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#id GameServicesGameServerDeploymentRollout#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param project: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#project GameServicesGameServerDeploymentRollout#project}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#timeouts GameServicesGameServerDeploymentRollout#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = GameServicesGameServerDeploymentRolloutTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b34b5c248211332de8f7921f461e16a1bc44045865c6a3975711f03ad9317989)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument default_game_server_config", value=default_game_server_config, expected_type=type_hints["default_game_server_config"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument game_server_config_overrides", value=game_server_config_overrides, expected_type=type_hints["game_server_config_overrides"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_game_server_config": default_game_server_config,
            "deployment_id": deployment_id,
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
        if game_server_config_overrides is not None:
            self._values["game_server_config_overrides"] = game_server_config_overrides
        if id is not None:
            self._values["id"] = id
        if project is not None:
            self._values["project"] = project
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
    def default_game_server_config(self) -> builtins.str:
        '''This field points to the game server config that is applied by default to all realms and clusters. For example,.

        'projects/my-project/locations/global/gameServerDeployments/my-game/configs/my-config'.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#default_game_server_config GameServicesGameServerDeploymentRollout#default_game_server_config}
        '''
        result = self._values.get("default_game_server_config")
        assert result is not None, "Required property 'default_game_server_config' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_id(self) -> builtins.str:
        '''The deployment to rollout the new config to. Only 1 rollout must be associated with each deployment.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#deployment_id GameServicesGameServerDeploymentRollout#deployment_id}
        '''
        result = self._values.get("deployment_id")
        assert result is not None, "Required property 'deployment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def game_server_config_overrides(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides"]]]:
        '''game_server_config_overrides block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#game_server_config_overrides GameServicesGameServerDeploymentRollout#game_server_config_overrides}
        '''
        result = self._values.get("game_server_config_overrides")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GameServicesGameServerDeploymentRolloutGameServerConfigOverrides"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#id GameServicesGameServerDeploymentRollout#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#project GameServicesGameServerDeploymentRollout#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["GameServicesGameServerDeploymentRolloutTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#timeouts GameServicesGameServerDeploymentRollout#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["GameServicesGameServerDeploymentRolloutTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerDeploymentRolloutConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutGameServerConfigOverrides",
    jsii_struct_bases=[],
    name_mapping={
        "config_version": "configVersion",
        "realms_selector": "realmsSelector",
    },
)
class GameServicesGameServerDeploymentRolloutGameServerConfigOverrides:
    def __init__(
        self,
        *,
        config_version: typing.Optional[builtins.str] = None,
        realms_selector: typing.Optional[typing.Union["GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param config_version: Version of the configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#config_version GameServicesGameServerDeploymentRollout#config_version}
        :param realms_selector: realms_selector block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#realms_selector GameServicesGameServerDeploymentRollout#realms_selector}
        '''
        if isinstance(realms_selector, dict):
            realms_selector = GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector(**realms_selector)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38762a3a0585595c3adc9c55629019e6a8b54b937ab2d029600dd8bc978246db)
            check_type(argname="argument config_version", value=config_version, expected_type=type_hints["config_version"])
            check_type(argname="argument realms_selector", value=realms_selector, expected_type=type_hints["realms_selector"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config_version is not None:
            self._values["config_version"] = config_version
        if realms_selector is not None:
            self._values["realms_selector"] = realms_selector

    @builtins.property
    def config_version(self) -> typing.Optional[builtins.str]:
        '''Version of the configuration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#config_version GameServicesGameServerDeploymentRollout#config_version}
        '''
        result = self._values.get("config_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def realms_selector(
        self,
    ) -> typing.Optional["GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector"]:
        '''realms_selector block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#realms_selector GameServicesGameServerDeploymentRollout#realms_selector}
        '''
        result = self._values.get("realms_selector")
        return typing.cast(typing.Optional["GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerDeploymentRolloutGameServerConfigOverrides(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerDeploymentRolloutGameServerConfigOverridesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutGameServerConfigOverridesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f43df497a7d77c2073282477a44204701ed123dce55520e4fd21c67c333491a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d795a941f5d8d65b88e0b9e294862f3c8ded5856b14c32ed5427e335f717e40)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GameServicesGameServerDeploymentRolloutGameServerConfigOverridesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f82121457b585e4a335b7fa660ae8c046e13d464639de0b74242171a6fe522c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9db48a06d73f44c7e2a5eae0787568992bf91b269ef9196a20144cdce39089f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d0b082e5dc329a3b6a25d844b64ead6be1226bc11a25ad0d7876bd29b2a3d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc39df99f562570a29e3e25ead74e69b271af20ca6c8bb598c6217abefd51a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GameServicesGameServerDeploymentRolloutGameServerConfigOverridesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutGameServerConfigOverridesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5df48e9782a12416abc06972f7e00a96d5abc3171298066f74583d25e3eb234a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRealmsSelector")
    def put_realms_selector(
        self,
        *,
        realms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param realms: List of realms to match against. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#realms GameServicesGameServerDeploymentRollout#realms}
        '''
        value = GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector(
            realms=realms
        )

        return typing.cast(None, jsii.invoke(self, "putRealmsSelector", [value]))

    @jsii.member(jsii_name="resetConfigVersion")
    def reset_config_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigVersion", []))

    @jsii.member(jsii_name="resetRealmsSelector")
    def reset_realms_selector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealmsSelector", []))

    @builtins.property
    @jsii.member(jsii_name="realmsSelector")
    def realms_selector(
        self,
    ) -> "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelectorOutputReference":
        return typing.cast("GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelectorOutputReference", jsii.get(self, "realmsSelector"))

    @builtins.property
    @jsii.member(jsii_name="configVersionInput")
    def config_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="realmsSelectorInput")
    def realms_selector_input(
        self,
    ) -> typing.Optional["GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector"]:
        return typing.cast(typing.Optional["GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector"], jsii.get(self, "realmsSelectorInput"))

    @builtins.property
    @jsii.member(jsii_name="configVersion")
    def config_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configVersion"))

    @config_version.setter
    def config_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ebb2e276e50aaf49175a30220bd316069d1244071df8b7b14222601ed578613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configVersion", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9bdd14b6edb308cc11ca1781b5f43db0264047515c8baa9646171ab83527f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector",
    jsii_struct_bases=[],
    name_mapping={"realms": "realms"},
)
class GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector:
    def __init__(
        self,
        *,
        realms: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param realms: List of realms to match against. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#realms GameServicesGameServerDeploymentRollout#realms}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfa91b163bb8dcd7b3524a541494cdbc420f652cf28e9b745997cc5fb118614f)
            check_type(argname="argument realms", value=realms, expected_type=type_hints["realms"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if realms is not None:
            self._values["realms"] = realms

    @builtins.property
    def realms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of realms to match against.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#realms GameServicesGameServerDeploymentRollout#realms}
        '''
        result = self._values.get("realms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d07c696e0f1e3ee8ad3d379216a373c9a5b87b754e25602991d8643b9dbdf98)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRealms")
    def reset_realms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRealms", []))

    @builtins.property
    @jsii.member(jsii_name="realmsInput")
    def realms_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "realmsInput"))

    @builtins.property
    @jsii.member(jsii_name="realms")
    def realms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "realms"))

    @realms.setter
    def realms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ef2c7c10af931c770d20faf9af6d66aaa228f73dbe16578fdcb6553bf78061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "realms", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector]:
        return typing.cast(typing.Optional[GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bf16eff34da27e955df54f22fca9e520cb87f0244a8cab6fb23375b0831b46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class GameServicesGameServerDeploymentRolloutTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#create GameServicesGameServerDeploymentRollout#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#delete GameServicesGameServerDeploymentRollout#delete}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#update GameServicesGameServerDeploymentRollout#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4805da0202e8dab1ce90213b08e50f7fe7fedaf100d52f4e3d5271d92d092f9)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#create GameServicesGameServerDeploymentRollout#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#delete GameServicesGameServerDeploymentRollout#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/google/r/game_services_game_server_deployment_rollout#update GameServicesGameServerDeploymentRollout#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GameServicesGameServerDeploymentRolloutTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GameServicesGameServerDeploymentRolloutTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.gameServicesGameServerDeploymentRollout.GameServicesGameServerDeploymentRolloutTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3ef0d9ff23d0290b4a9fbd93e45fe80758152804d219698b9ab90900379fad0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaab7965dc1a2bc46ffad0131d19e2249bb57402f62f78fe3625946e889e7972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d4659b9e26811ba5485aa59031c80dd0fc64b17c987a05c78b04b73b37ee3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7aaa5be8bf6e843752372b348241828caaa42b904eca6a47f2361dc18bfcfd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af71ab8c8c4010b0bd0a6dd68223cf52915fa0b7e2fa4b9a9fae810bb038ec5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "GameServicesGameServerDeploymentRollout",
    "GameServicesGameServerDeploymentRolloutConfig",
    "GameServicesGameServerDeploymentRolloutGameServerConfigOverrides",
    "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesList",
    "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesOutputReference",
    "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector",
    "GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelectorOutputReference",
    "GameServicesGameServerDeploymentRolloutTimeouts",
    "GameServicesGameServerDeploymentRolloutTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__16d931b28160b911ad1bf9d5cb920a251c5b5e69f7d72f7994e735b6e3108c14(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    default_game_server_config: builtins.str,
    deployment_id: builtins.str,
    game_server_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__72b569fadfb67be866404a3bfb9f5ce7ca182f66da4f2438168ebbc7d1c92d76(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4791ca1b2e313f7debfa814feaadd59a7a5dd3a95caa76659ef575952cf4ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4b227b8d4e89a5b00f0deadb44042575b63ea57e21fbf0a0de8269574d411c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80eee7d27aa8b00f928985c139d93b91d05be307c2c4a0ffdbb9270ac6574987(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323316f0960893e4f499225ae259824f3a37b48bf76be6839058b166b70a2dfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b34b5c248211332de8f7921f461e16a1bc44045865c6a3975711f03ad9317989(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_game_server_config: builtins.str,
    deployment_id: builtins.str,
    game_server_config_overrides: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38762a3a0585595c3adc9c55629019e6a8b54b937ab2d029600dd8bc978246db(
    *,
    config_version: typing.Optional[builtins.str] = None,
    realms_selector: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f43df497a7d77c2073282477a44204701ed123dce55520e4fd21c67c333491a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d795a941f5d8d65b88e0b9e294862f3c8ded5856b14c32ed5427e335f717e40(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f82121457b585e4a335b7fa660ae8c046e13d464639de0b74242171a6fe522c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db48a06d73f44c7e2a5eae0787568992bf91b269ef9196a20144cdce39089f8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0b082e5dc329a3b6a25d844b64ead6be1226bc11a25ad0d7876bd29b2a3d19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc39df99f562570a29e3e25ead74e69b271af20ca6c8bb598c6217abefd51a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df48e9782a12416abc06972f7e00a96d5abc3171298066f74583d25e3eb234a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ebb2e276e50aaf49175a30220bd316069d1244071df8b7b14222601ed578613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9bdd14b6edb308cc11ca1781b5f43db0264047515c8baa9646171ab83527f1(
    value: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutGameServerConfigOverrides, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa91b163bb8dcd7b3524a541494cdbc420f652cf28e9b745997cc5fb118614f(
    *,
    realms: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d07c696e0f1e3ee8ad3d379216a373c9a5b87b754e25602991d8643b9dbdf98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ef2c7c10af931c770d20faf9af6d66aaa228f73dbe16578fdcb6553bf78061(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bf16eff34da27e955df54f22fca9e520cb87f0244a8cab6fb23375b0831b46(
    value: typing.Optional[GameServicesGameServerDeploymentRolloutGameServerConfigOverridesRealmsSelector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4805da0202e8dab1ce90213b08e50f7fe7fedaf100d52f4e3d5271d92d092f9(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ef0d9ff23d0290b4a9fbd93e45fe80758152804d219698b9ab90900379fad0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaab7965dc1a2bc46ffad0131d19e2249bb57402f62f78fe3625946e889e7972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d4659b9e26811ba5485aa59031c80dd0fc64b17c987a05c78b04b73b37ee3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7aaa5be8bf6e843752372b348241828caaa42b904eca6a47f2361dc18bfcfd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af71ab8c8c4010b0bd0a6dd68223cf52915fa0b7e2fa4b9a9fae810bb038ec5f(
    value: typing.Optional[typing.Union[GameServicesGameServerDeploymentRolloutTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
