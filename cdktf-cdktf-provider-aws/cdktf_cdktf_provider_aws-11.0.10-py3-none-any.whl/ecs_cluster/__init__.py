'''
# `aws_ecs_cluster`

Refer to the Terraform Registory for docs: [`aws_ecs_cluster`](https://www.terraform.io/docs/providers/aws/r/ecs_cluster).
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


class EcsCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsCluster",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster aws_ecs_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        capacity_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[typing.Union["EcsClusterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        default_capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsClusterDefaultCapacityProviderStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        service_connect_defaults: typing.Optional[typing.Union["EcsClusterServiceConnectDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsClusterSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster aws_ecs_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#name EcsCluster#name}.
        :param capacity_providers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#capacity_providers EcsCluster#capacity_providers}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#configuration EcsCluster#configuration}
        :param default_capacity_provider_strategy: default_capacity_provider_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#default_capacity_provider_strategy EcsCluster#default_capacity_provider_strategy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#id EcsCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_connect_defaults: service_connect_defaults block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#service_connect_defaults EcsCluster#service_connect_defaults}
        :param setting: setting block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#setting EcsCluster#setting}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#tags EcsCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#tags_all EcsCluster#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a69934a4d3fa136a2fa15e2e4aadfffc786ffe043e8414e25b124c1abd6fe99b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EcsClusterConfig(
            name=name,
            capacity_providers=capacity_providers,
            configuration=configuration,
            default_capacity_provider_strategy=default_capacity_provider_strategy,
            id=id,
            service_connect_defaults=service_connect_defaults,
            setting=setting,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putConfiguration")
    def put_configuration(
        self,
        *,
        execute_command_configuration: typing.Optional[typing.Union["EcsClusterConfigurationExecuteCommandConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execute_command_configuration: execute_command_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#execute_command_configuration EcsCluster#execute_command_configuration}
        '''
        value = EcsClusterConfiguration(
            execute_command_configuration=execute_command_configuration
        )

        return typing.cast(None, jsii.invoke(self, "putConfiguration", [value]))

    @jsii.member(jsii_name="putDefaultCapacityProviderStrategy")
    def put_default_capacity_provider_strategy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsClusterDefaultCapacityProviderStrategy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__000da76224c60569cd245e728889c1f3108ab54d2fe02cbd2a667dece5acc36b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultCapacityProviderStrategy", [value]))

    @jsii.member(jsii_name="putServiceConnectDefaults")
    def put_service_connect_defaults(self, *, namespace: builtins.str) -> None:
        '''
        :param namespace: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#namespace EcsCluster#namespace}.
        '''
        value = EcsClusterServiceConnectDefaults(namespace=namespace)

        return typing.cast(None, jsii.invoke(self, "putServiceConnectDefaults", [value]))

    @jsii.member(jsii_name="putSetting")
    def put_setting(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsClusterSetting", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c4b1080fe2d917a9388769a8dc7e87a8b6ebb45378f941c9174c428e0c5e609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetting", [value]))

    @jsii.member(jsii_name="resetCapacityProviders")
    def reset_capacity_providers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCapacityProviders", []))

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetDefaultCapacityProviderStrategy")
    def reset_default_capacity_provider_strategy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultCapacityProviderStrategy", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetServiceConnectDefaults")
    def reset_service_connect_defaults(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceConnectDefaults", []))

    @jsii.member(jsii_name="resetSetting")
    def reset_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetting", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> "EcsClusterConfigurationOutputReference":
        return typing.cast("EcsClusterConfigurationOutputReference", jsii.get(self, "configuration"))

    @builtins.property
    @jsii.member(jsii_name="defaultCapacityProviderStrategy")
    def default_capacity_provider_strategy(
        self,
    ) -> "EcsClusterDefaultCapacityProviderStrategyList":
        return typing.cast("EcsClusterDefaultCapacityProviderStrategyList", jsii.get(self, "defaultCapacityProviderStrategy"))

    @builtins.property
    @jsii.member(jsii_name="serviceConnectDefaults")
    def service_connect_defaults(
        self,
    ) -> "EcsClusterServiceConnectDefaultsOutputReference":
        return typing.cast("EcsClusterServiceConnectDefaultsOutputReference", jsii.get(self, "serviceConnectDefaults"))

    @builtins.property
    @jsii.member(jsii_name="setting")
    def setting(self) -> "EcsClusterSettingList":
        return typing.cast("EcsClusterSettingList", jsii.get(self, "setting"))

    @builtins.property
    @jsii.member(jsii_name="capacityProvidersInput")
    def capacity_providers_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "capacityProvidersInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(self) -> typing.Optional["EcsClusterConfiguration"]:
        return typing.cast(typing.Optional["EcsClusterConfiguration"], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultCapacityProviderStrategyInput")
    def default_capacity_provider_strategy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterDefaultCapacityProviderStrategy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterDefaultCapacityProviderStrategy"]]], jsii.get(self, "defaultCapacityProviderStrategyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceConnectDefaultsInput")
    def service_connect_defaults_input(
        self,
    ) -> typing.Optional["EcsClusterServiceConnectDefaults"]:
        return typing.cast(typing.Optional["EcsClusterServiceConnectDefaults"], jsii.get(self, "serviceConnectDefaultsInput"))

    @builtins.property
    @jsii.member(jsii_name="settingInput")
    def setting_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterSetting"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterSetting"]]], jsii.get(self, "settingInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviders")
    def capacity_providers(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "capacityProviders"))

    @capacity_providers.setter
    def capacity_providers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e12f6bf40e869cac6a4f17bdc2a403840d5338b283fb2166bf9633233423586c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityProviders", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19ad8e3b0fe31796b0e978b4900408ba68994845bab26ade580e7f79ebd0e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9068e44be0b8377554eda776b2720844b8c3eb95c65ba62cc11ea31cdc42329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5106b358b0c64b32d1f333fe8e2db1cce78f038858c0b3028e04bc2f98ab628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23725d025a65c8078a85f317e45f21da7bc5da13c20f08c52e2df3bbb26b4249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfig",
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
        "capacity_providers": "capacityProviders",
        "configuration": "configuration",
        "default_capacity_provider_strategy": "defaultCapacityProviderStrategy",
        "id": "id",
        "service_connect_defaults": "serviceConnectDefaults",
        "setting": "setting",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class EcsClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        capacity_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
        configuration: typing.Optional[typing.Union["EcsClusterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        default_capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsClusterDefaultCapacityProviderStrategy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        service_connect_defaults: typing.Optional[typing.Union["EcsClusterServiceConnectDefaults", typing.Dict[builtins.str, typing.Any]]] = None,
        setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EcsClusterSetting", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#name EcsCluster#name}.
        :param capacity_providers: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#capacity_providers EcsCluster#capacity_providers}.
        :param configuration: configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#configuration EcsCluster#configuration}
        :param default_capacity_provider_strategy: default_capacity_provider_strategy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#default_capacity_provider_strategy EcsCluster#default_capacity_provider_strategy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#id EcsCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param service_connect_defaults: service_connect_defaults block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#service_connect_defaults EcsCluster#service_connect_defaults}
        :param setting: setting block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#setting EcsCluster#setting}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#tags EcsCluster#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#tags_all EcsCluster#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(configuration, dict):
            configuration = EcsClusterConfiguration(**configuration)
        if isinstance(service_connect_defaults, dict):
            service_connect_defaults = EcsClusterServiceConnectDefaults(**service_connect_defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f475f9d1a32ba909c7863c7f94a7670836b710c2f0b13fa511dcf196c1e22c9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument capacity_providers", value=capacity_providers, expected_type=type_hints["capacity_providers"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument default_capacity_provider_strategy", value=default_capacity_provider_strategy, expected_type=type_hints["default_capacity_provider_strategy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service_connect_defaults", value=service_connect_defaults, expected_type=type_hints["service_connect_defaults"])
            check_type(argname="argument setting", value=setting, expected_type=type_hints["setting"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
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
        if capacity_providers is not None:
            self._values["capacity_providers"] = capacity_providers
        if configuration is not None:
            self._values["configuration"] = configuration
        if default_capacity_provider_strategy is not None:
            self._values["default_capacity_provider_strategy"] = default_capacity_provider_strategy
        if id is not None:
            self._values["id"] = id
        if service_connect_defaults is not None:
            self._values["service_connect_defaults"] = service_connect_defaults
        if setting is not None:
            self._values["setting"] = setting
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#name EcsCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def capacity_providers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#capacity_providers EcsCluster#capacity_providers}.'''
        result = self._values.get("capacity_providers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def configuration(self) -> typing.Optional["EcsClusterConfiguration"]:
        '''configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#configuration EcsCluster#configuration}
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional["EcsClusterConfiguration"], result)

    @builtins.property
    def default_capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterDefaultCapacityProviderStrategy"]]]:
        '''default_capacity_provider_strategy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#default_capacity_provider_strategy EcsCluster#default_capacity_provider_strategy}
        '''
        result = self._values.get("default_capacity_provider_strategy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterDefaultCapacityProviderStrategy"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#id EcsCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_connect_defaults(
        self,
    ) -> typing.Optional["EcsClusterServiceConnectDefaults"]:
        '''service_connect_defaults block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#service_connect_defaults EcsCluster#service_connect_defaults}
        '''
        result = self._values.get("service_connect_defaults")
        return typing.cast(typing.Optional["EcsClusterServiceConnectDefaults"], result)

    @builtins.property
    def setting(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterSetting"]]]:
        '''setting block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#setting EcsCluster#setting}
        '''
        result = self._values.get("setting")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EcsClusterSetting"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#tags EcsCluster#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#tags_all EcsCluster#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"execute_command_configuration": "executeCommandConfiguration"},
)
class EcsClusterConfiguration:
    def __init__(
        self,
        *,
        execute_command_configuration: typing.Optional[typing.Union["EcsClusterConfigurationExecuteCommandConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param execute_command_configuration: execute_command_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#execute_command_configuration EcsCluster#execute_command_configuration}
        '''
        if isinstance(execute_command_configuration, dict):
            execute_command_configuration = EcsClusterConfigurationExecuteCommandConfiguration(**execute_command_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a036fbd26b7391416ed3160a630b820f4d7540fae6b0a110c34399e6f516324)
            check_type(argname="argument execute_command_configuration", value=execute_command_configuration, expected_type=type_hints["execute_command_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execute_command_configuration is not None:
            self._values["execute_command_configuration"] = execute_command_configuration

    @builtins.property
    def execute_command_configuration(
        self,
    ) -> typing.Optional["EcsClusterConfigurationExecuteCommandConfiguration"]:
        '''execute_command_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#execute_command_configuration EcsCluster#execute_command_configuration}
        '''
        result = self._values.get("execute_command_configuration")
        return typing.cast(typing.Optional["EcsClusterConfigurationExecuteCommandConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfigurationExecuteCommandConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "kms_key_id": "kmsKeyId",
        "log_configuration": "logConfiguration",
        "logging": "logging",
    },
)
class EcsClusterConfigurationExecuteCommandConfiguration:
    def __init__(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union["EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#kms_key_id EcsCluster#kms_key_id}.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#log_configuration EcsCluster#log_configuration}
        :param logging: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#logging EcsCluster#logging}.
        '''
        if isinstance(log_configuration, dict):
            log_configuration = EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration(**log_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b987ee60039f258da9688482891bdedfbcb3410c3ceb76ad9f3af433e1f5b19e)
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if logging is not None:
            self._values["logging"] = logging

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#kms_key_id EcsCluster#kms_key_id}.'''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional["EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration"]:
        '''log_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#log_configuration EcsCluster#log_configuration}
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional["EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration"], result)

    @builtins.property
    def logging(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#logging EcsCluster#logging}.'''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterConfigurationExecuteCommandConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_encryption_enabled": "cloudWatchEncryptionEnabled",
        "cloud_watch_log_group_name": "cloudWatchLogGroupName",
        "s3_bucket_encryption_enabled": "s3BucketEncryptionEnabled",
        "s3_bucket_name": "s3BucketName",
        "s3_key_prefix": "s3KeyPrefix",
    },
)
class EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration:
    def __init__(
        self,
        *,
        cloud_watch_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
        s3_bucket_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_watch_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#cloud_watch_encryption_enabled EcsCluster#cloud_watch_encryption_enabled}.
        :param cloud_watch_log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#cloud_watch_log_group_name EcsCluster#cloud_watch_log_group_name}.
        :param s3_bucket_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_bucket_encryption_enabled EcsCluster#s3_bucket_encryption_enabled}.
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_bucket_name EcsCluster#s3_bucket_name}.
        :param s3_key_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_key_prefix EcsCluster#s3_key_prefix}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f8a39c29e10463c963e904ba43349a8ca8584c35948ee8102ea571dc4cc9254)
            check_type(argname="argument cloud_watch_encryption_enabled", value=cloud_watch_encryption_enabled, expected_type=type_hints["cloud_watch_encryption_enabled"])
            check_type(argname="argument cloud_watch_log_group_name", value=cloud_watch_log_group_name, expected_type=type_hints["cloud_watch_log_group_name"])
            check_type(argname="argument s3_bucket_encryption_enabled", value=s3_bucket_encryption_enabled, expected_type=type_hints["s3_bucket_encryption_enabled"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_encryption_enabled is not None:
            self._values["cloud_watch_encryption_enabled"] = cloud_watch_encryption_enabled
        if cloud_watch_log_group_name is not None:
            self._values["cloud_watch_log_group_name"] = cloud_watch_log_group_name
        if s3_bucket_encryption_enabled is not None:
            self._values["s3_bucket_encryption_enabled"] = s3_bucket_encryption_enabled
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix

    @builtins.property
    def cloud_watch_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#cloud_watch_encryption_enabled EcsCluster#cloud_watch_encryption_enabled}.'''
        result = self._values.get("cloud_watch_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cloud_watch_log_group_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#cloud_watch_log_group_name EcsCluster#cloud_watch_log_group_name}.'''
        result = self._values.get("cloud_watch_log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket_encryption_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_bucket_encryption_enabled EcsCluster#s3_bucket_encryption_enabled}.'''
        result = self._values.get("s3_bucket_encryption_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_bucket_name EcsCluster#s3_bucket_name}.'''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_key_prefix EcsCluster#s3_key_prefix}.'''
        result = self._values.get("s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsClusterConfigurationExecuteCommandConfigurationLogConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfigurationExecuteCommandConfigurationLogConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48999b44ad9a7a19ec8e405700c582ac83873990aa94e9c649ca7439534b6fac)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCloudWatchEncryptionEnabled")
    def reset_cloud_watch_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchEncryptionEnabled", []))

    @jsii.member(jsii_name="resetCloudWatchLogGroupName")
    def reset_cloud_watch_log_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudWatchLogGroupName", []))

    @jsii.member(jsii_name="resetS3BucketEncryptionEnabled")
    def reset_s3_bucket_encryption_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BucketEncryptionEnabled", []))

    @jsii.member(jsii_name="resetS3BucketName")
    def reset_s3_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3BucketName", []))

    @jsii.member(jsii_name="resetS3KeyPrefix")
    def reset_s3_key_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetS3KeyPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchEncryptionEnabledInput")
    def cloud_watch_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudWatchEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupNameInput")
    def cloud_watch_log_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudWatchLogGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketEncryptionEnabledInput")
    def s3_bucket_encryption_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "s3BucketEncryptionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="s3BucketNameInput")
    def s3_bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3BucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="s3KeyPrefixInput")
    def s3_key_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "s3KeyPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchEncryptionEnabled")
    def cloud_watch_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "cloudWatchEncryptionEnabled"))

    @cloud_watch_encryption_enabled.setter
    def cloud_watch_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a2efc11193ccfb3f92c369cd2dba123786595638eec5d171dfbfa42cb0e029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="cloudWatchLogGroupName")
    def cloud_watch_log_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudWatchLogGroupName"))

    @cloud_watch_log_group_name.setter
    def cloud_watch_log_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1016280ece611d715b3a115d3e64793321e7dd72e379421e5e2b0a099f16d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudWatchLogGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketEncryptionEnabled")
    def s3_bucket_encryption_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "s3BucketEncryptionEnabled"))

    @s3_bucket_encryption_enabled.setter
    def s3_bucket_encryption_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7998f20a1d26792896cdbca46562ee7edb34e6c2e3547f5ab48b73f5b83706f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketEncryptionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3BucketName"))

    @s3_bucket_name.setter
    def s3_bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebeb7305a183d79514deb2da112ff386fc11a8daedfd72f85eb78cb8e8804bc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3BucketName", value)

    @builtins.property
    @jsii.member(jsii_name="s3KeyPrefix")
    def s3_key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "s3KeyPrefix"))

    @s3_key_prefix.setter
    def s3_key_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58e9e2f4d2894a4d542ac6027b5f6be778799ca69aa790bf2697334fcfd6855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3KeyPrefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration]:
        return typing.cast(typing.Optional[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e8640cf08fa7af26a23ad9ae835c1bb6ec49ef092f77bee150f7307cfc76cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EcsClusterConfigurationExecuteCommandConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfigurationExecuteCommandConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29e40c7057a8cd0f591a18d1ca8ac254104c9a175ca4cbc432f90ff0fed9c46a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putLogConfiguration")
    def put_log_configuration(
        self,
        *,
        cloud_watch_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
        s3_bucket_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_watch_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#cloud_watch_encryption_enabled EcsCluster#cloud_watch_encryption_enabled}.
        :param cloud_watch_log_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#cloud_watch_log_group_name EcsCluster#cloud_watch_log_group_name}.
        :param s3_bucket_encryption_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_bucket_encryption_enabled EcsCluster#s3_bucket_encryption_enabled}.
        :param s3_bucket_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_bucket_name EcsCluster#s3_bucket_name}.
        :param s3_key_prefix: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#s3_key_prefix EcsCluster#s3_key_prefix}.
        '''
        value = EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration(
            cloud_watch_encryption_enabled=cloud_watch_encryption_enabled,
            cloud_watch_log_group_name=cloud_watch_log_group_name,
            s3_bucket_encryption_enabled=s3_bucket_encryption_enabled,
            s3_bucket_name=s3_bucket_name,
            s3_key_prefix=s3_key_prefix,
        )

        return typing.cast(None, jsii.invoke(self, "putLogConfiguration", [value]))

    @jsii.member(jsii_name="resetKmsKeyId")
    def reset_kms_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKmsKeyId", []))

    @jsii.member(jsii_name="resetLogConfiguration")
    def reset_log_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogConfiguration", []))

    @jsii.member(jsii_name="resetLogging")
    def reset_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogging", []))

    @builtins.property
    @jsii.member(jsii_name="logConfiguration")
    def log_configuration(
        self,
    ) -> EcsClusterConfigurationExecuteCommandConfigurationLogConfigurationOutputReference:
        return typing.cast(EcsClusterConfigurationExecuteCommandConfigurationLogConfigurationOutputReference, jsii.get(self, "logConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyIdInput")
    def kms_key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logConfigurationInput")
    def log_configuration_input(
        self,
    ) -> typing.Optional[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration]:
        return typing.cast(typing.Optional[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration], jsii.get(self, "logConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingInput")
    def logging_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingInput"))

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b590fb089a87ca3eb0475defbcd96d0e5028d85c78c16bd3fcfe51e11292e576)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logging"))

    @logging.setter
    def logging(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8641554ec0f7d4c900f48ec3a3d136c3ff19dd93937908dc1342e994ca64e84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logging", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EcsClusterConfigurationExecuteCommandConfiguration]:
        return typing.cast(typing.Optional[EcsClusterConfigurationExecuteCommandConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsClusterConfigurationExecuteCommandConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635d0ceb486f9fcc293bc6150d98294da1219c45910afb8be764294da25e363a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EcsClusterConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__19598a018cf3f4f90d278e0355178882c98c5a0edd2027ebe77ed0fe0f72f1db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExecuteCommandConfiguration")
    def put_execute_command_configuration(
        self,
        *,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_configuration: typing.Optional[typing.Union[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        logging: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param kms_key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#kms_key_id EcsCluster#kms_key_id}.
        :param log_configuration: log_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#log_configuration EcsCluster#log_configuration}
        :param logging: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#logging EcsCluster#logging}.
        '''
        value = EcsClusterConfigurationExecuteCommandConfiguration(
            kms_key_id=kms_key_id, log_configuration=log_configuration, logging=logging
        )

        return typing.cast(None, jsii.invoke(self, "putExecuteCommandConfiguration", [value]))

    @jsii.member(jsii_name="resetExecuteCommandConfiguration")
    def reset_execute_command_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecuteCommandConfiguration", []))

    @builtins.property
    @jsii.member(jsii_name="executeCommandConfiguration")
    def execute_command_configuration(
        self,
    ) -> EcsClusterConfigurationExecuteCommandConfigurationOutputReference:
        return typing.cast(EcsClusterConfigurationExecuteCommandConfigurationOutputReference, jsii.get(self, "executeCommandConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="executeCommandConfigurationInput")
    def execute_command_configuration_input(
        self,
    ) -> typing.Optional[EcsClusterConfigurationExecuteCommandConfiguration]:
        return typing.cast(typing.Optional[EcsClusterConfigurationExecuteCommandConfiguration], jsii.get(self, "executeCommandConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EcsClusterConfiguration]:
        return typing.cast(typing.Optional[EcsClusterConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[EcsClusterConfiguration]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e1ee26ffa070b2eefae9e8a010915a98454567cb7d8825b426e568593368ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterDefaultCapacityProviderStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_provider": "capacityProvider",
        "base": "base",
        "weight": "weight",
    },
)
class EcsClusterDefaultCapacityProviderStrategy:
    def __init__(
        self,
        *,
        capacity_provider: builtins.str,
        base: typing.Optional[jsii.Number] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param capacity_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#capacity_provider EcsCluster#capacity_provider}.
        :param base: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#base EcsCluster#base}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#weight EcsCluster#weight}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcd2c128f8e907cbde58efe770af10aaf6804654867b164df2ec5732c4913356)
            check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
            check_type(argname="argument base", value=base, expected_type=type_hints["base"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity_provider": capacity_provider,
        }
        if base is not None:
            self._values["base"] = base
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def capacity_provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#capacity_provider EcsCluster#capacity_provider}.'''
        result = self._values.get("capacity_provider")
        assert result is not None, "Required property 'capacity_provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def base(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#base EcsCluster#base}.'''
        result = self._values.get("base")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#weight EcsCluster#weight}.'''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterDefaultCapacityProviderStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsClusterDefaultCapacityProviderStrategyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterDefaultCapacityProviderStrategyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5c60bfff24df9589844818f0d6d4a999f0664e69874d2646d5108a62fe6ff94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EcsClusterDefaultCapacityProviderStrategyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739c680fe07a772c57d8222cccf90e187ba5c8f62bd4a528b89b15178b9119be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EcsClusterDefaultCapacityProviderStrategyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c9dd0a9ed6ed1675506d0dc1290592077f45df8d9bef3500f306ccf9f7ae06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2ef341f5898b27693d29898e77896922df526e39a117d2fad5c8437caf2186a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f5947559dafe7c2e3cacee7bda41d2b27c50de4160b5a9cc7959cbb867e96a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterDefaultCapacityProviderStrategy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterDefaultCapacityProviderStrategy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterDefaultCapacityProviderStrategy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36e9e568c0f2146a45604486047c95ce73077e3c148d251dd08b4c756cc7e046)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EcsClusterDefaultCapacityProviderStrategyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterDefaultCapacityProviderStrategyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a55f66f41c01bb93ee0caa21e0e2e4632b952b3f5c3c67f935e9647d56ed2e6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetBase")
    def reset_base(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="baseInput")
    def base_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "baseInput"))

    @builtins.property
    @jsii.member(jsii_name="capacityProviderInput")
    def capacity_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "capacityProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="base")
    def base(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "base"))

    @base.setter
    def base(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb3d307d08cc110946aa10890f3a9e108f1dbf55ca52c13def47a512212dba0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "base", value)

    @builtins.property
    @jsii.member(jsii_name="capacityProvider")
    def capacity_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "capacityProvider"))

    @capacity_provider.setter
    def capacity_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b56588a7c9669bf56efd11cb00bd60f00c75390eb8a35268e57e445faec0b06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacityProvider", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d21b2429b88b2cf289693968c432afdfae154c68504629a6b51b3ff139f2d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[EcsClusterDefaultCapacityProviderStrategy, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[EcsClusterDefaultCapacityProviderStrategy, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[EcsClusterDefaultCapacityProviderStrategy, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca443e12f02c4c07224079323b900e338c8961a007c53d21fcdadefea7251be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterServiceConnectDefaults",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace"},
)
class EcsClusterServiceConnectDefaults:
    def __init__(self, *, namespace: builtins.str) -> None:
        '''
        :param namespace: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#namespace EcsCluster#namespace}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88a3fa5d76f9e4afc0b6c3d59d7808c08ef273f94562674f0cbe51d4f9988ce2)
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace": namespace,
        }

    @builtins.property
    def namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#namespace EcsCluster#namespace}.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterServiceConnectDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsClusterServiceConnectDefaultsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterServiceConnectDefaultsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__24294f15d971722bd79f273be2dbe155601c1d322c7c47ceeaf03245e5c2d91f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ddbd184b40bfdab02bfec25cfeeecc86f2a18f0245459c007ee14ca7ca8ca5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EcsClusterServiceConnectDefaults]:
        return typing.cast(typing.Optional[EcsClusterServiceConnectDefaults], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EcsClusterServiceConnectDefaults],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bd4ad395ff7e3aad8bf13d5b93aaa1735f8c63cf7fae657bc5bbfb04eab20d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterSetting",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class EcsClusterSetting:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#name EcsCluster#name}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#value EcsCluster#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a07b74e7de57588ff279eff826570d0e8ef9edba438807c50c98729a3c905e1f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#name EcsCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ecs_cluster#value EcsCluster#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsClusterSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsClusterSettingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterSettingList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9018dfe031d7ff47fae331462ce3c6f2529a5187e7ac4dcc314c4b2b1ee0181d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EcsClusterSettingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f791bb0117ebf2a3201f4e238d20bed2b3122750f1445b378fc0eae611b96b1f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EcsClusterSettingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c319a500700cdab3d17b4c9975b9700db786183b0133f0a303cb219ac46aea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f06b9ca2dd392b229eaced435308d7b9cab73ec8f65a8a0f14c82b72ab4ff50f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__600e3d37a290fbd9c67f614b937d8e68e46e0440c8f0ed4e984485bc607098ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterSetting]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterSetting]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterSetting]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eefbc3459fdc8a9aaf8b5bac9f16cdafeba522ac1ee65497a86d36c07d23ea97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class EcsClusterSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ecsCluster.EcsClusterSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__791a7938883c627fe8392c756189ffdbb52abbbe16ff0315ea134d7ab3356390)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82489dc869ddd9642b1cca0c53cc97850ad2b27ed3a58488bf2f3260ee3ffecb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773207f76dd3ddcdf1e4ce4cc975e6c7266a03f09568a6374cdc74aa7b30d8d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[EcsClusterSetting, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[EcsClusterSetting, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[EcsClusterSetting, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e652b054829a770194b7d929924cfeab4803283b3ca4b744fa0d5ae505ab552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "EcsCluster",
    "EcsClusterConfig",
    "EcsClusterConfiguration",
    "EcsClusterConfigurationExecuteCommandConfiguration",
    "EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration",
    "EcsClusterConfigurationExecuteCommandConfigurationLogConfigurationOutputReference",
    "EcsClusterConfigurationExecuteCommandConfigurationOutputReference",
    "EcsClusterConfigurationOutputReference",
    "EcsClusterDefaultCapacityProviderStrategy",
    "EcsClusterDefaultCapacityProviderStrategyList",
    "EcsClusterDefaultCapacityProviderStrategyOutputReference",
    "EcsClusterServiceConnectDefaults",
    "EcsClusterServiceConnectDefaultsOutputReference",
    "EcsClusterSetting",
    "EcsClusterSettingList",
    "EcsClusterSettingOutputReference",
]

publication.publish()

def _typecheckingstub__a69934a4d3fa136a2fa15e2e4aadfffc786ffe043e8414e25b124c1abd6fe99b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    capacity_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[typing.Union[EcsClusterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    default_capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsClusterDefaultCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    service_connect_defaults: typing.Optional[typing.Union[EcsClusterServiceConnectDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsClusterSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__000da76224c60569cd245e728889c1f3108ab54d2fe02cbd2a667dece5acc36b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsClusterDefaultCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4b1080fe2d917a9388769a8dc7e87a8b6ebb45378f941c9174c428e0c5e609(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsClusterSetting, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12f6bf40e869cac6a4f17bdc2a403840d5338b283fb2166bf9633233423586c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19ad8e3b0fe31796b0e978b4900408ba68994845bab26ade580e7f79ebd0e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9068e44be0b8377554eda776b2720844b8c3eb95c65ba62cc11ea31cdc42329(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5106b358b0c64b32d1f333fe8e2db1cce78f038858c0b3028e04bc2f98ab628(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23725d025a65c8078a85f317e45f21da7bc5da13c20f08c52e2df3bbb26b4249(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f475f9d1a32ba909c7863c7f94a7670836b710c2f0b13fa511dcf196c1e22c9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    capacity_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    configuration: typing.Optional[typing.Union[EcsClusterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    default_capacity_provider_strategy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsClusterDefaultCapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    service_connect_defaults: typing.Optional[typing.Union[EcsClusterServiceConnectDefaults, typing.Dict[builtins.str, typing.Any]]] = None,
    setting: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EcsClusterSetting, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a036fbd26b7391416ed3160a630b820f4d7540fae6b0a110c34399e6f516324(
    *,
    execute_command_configuration: typing.Optional[typing.Union[EcsClusterConfigurationExecuteCommandConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b987ee60039f258da9688482891bdedfbcb3410c3ceb76ad9f3af433e1f5b19e(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_configuration: typing.Optional[typing.Union[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    logging: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f8a39c29e10463c963e904ba43349a8ca8584c35948ee8102ea571dc4cc9254(
    *,
    cloud_watch_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
    s3_bucket_encryption_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48999b44ad9a7a19ec8e405700c582ac83873990aa94e9c649ca7439534b6fac(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a2efc11193ccfb3f92c369cd2dba123786595638eec5d171dfbfa42cb0e029(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1016280ece611d715b3a115d3e64793321e7dd72e379421e5e2b0a099f16d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7998f20a1d26792896cdbca46562ee7edb34e6c2e3547f5ab48b73f5b83706f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebeb7305a183d79514deb2da112ff386fc11a8daedfd72f85eb78cb8e8804bc1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58e9e2f4d2894a4d542ac6027b5f6be778799ca69aa790bf2697334fcfd6855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e8640cf08fa7af26a23ad9ae835c1bb6ec49ef092f77bee150f7307cfc76cb(
    value: typing.Optional[EcsClusterConfigurationExecuteCommandConfigurationLogConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e40c7057a8cd0f591a18d1ca8ac254104c9a175ca4cbc432f90ff0fed9c46a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b590fb089a87ca3eb0475defbcd96d0e5028d85c78c16bd3fcfe51e11292e576(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8641554ec0f7d4c900f48ec3a3d136c3ff19dd93937908dc1342e994ca64e84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635d0ceb486f9fcc293bc6150d98294da1219c45910afb8be764294da25e363a(
    value: typing.Optional[EcsClusterConfigurationExecuteCommandConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19598a018cf3f4f90d278e0355178882c98c5a0edd2027ebe77ed0fe0f72f1db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e1ee26ffa070b2eefae9e8a010915a98454567cb7d8825b426e568593368ec(
    value: typing.Optional[EcsClusterConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcd2c128f8e907cbde58efe770af10aaf6804654867b164df2ec5732c4913356(
    *,
    capacity_provider: builtins.str,
    base: typing.Optional[jsii.Number] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c60bfff24df9589844818f0d6d4a999f0664e69874d2646d5108a62fe6ff94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739c680fe07a772c57d8222cccf90e187ba5c8f62bd4a528b89b15178b9119be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c9dd0a9ed6ed1675506d0dc1290592077f45df8d9bef3500f306ccf9f7ae06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ef341f5898b27693d29898e77896922df526e39a117d2fad5c8437caf2186a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5947559dafe7c2e3cacee7bda41d2b27c50de4160b5a9cc7959cbb867e96a5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36e9e568c0f2146a45604486047c95ce73077e3c148d251dd08b4c756cc7e046(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterDefaultCapacityProviderStrategy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55f66f41c01bb93ee0caa21e0e2e4632b952b3f5c3c67f935e9647d56ed2e6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb3d307d08cc110946aa10890f3a9e108f1dbf55ca52c13def47a512212dba0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b56588a7c9669bf56efd11cb00bd60f00c75390eb8a35268e57e445faec0b06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d21b2429b88b2cf289693968c432afdfae154c68504629a6b51b3ff139f2d7b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca443e12f02c4c07224079323b900e338c8961a007c53d21fcdadefea7251be(
    value: typing.Optional[typing.Union[EcsClusterDefaultCapacityProviderStrategy, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a3fa5d76f9e4afc0b6c3d59d7808c08ef273f94562674f0cbe51d4f9988ce2(
    *,
    namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24294f15d971722bd79f273be2dbe155601c1d322c7c47ceeaf03245e5c2d91f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddbd184b40bfdab02bfec25cfeeecc86f2a18f0245459c007ee14ca7ca8ca5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bd4ad395ff7e3aad8bf13d5b93aaa1735f8c63cf7fae657bc5bbfb04eab20d3(
    value: typing.Optional[EcsClusterServiceConnectDefaults],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a07b74e7de57588ff279eff826570d0e8ef9edba438807c50c98729a3c905e1f(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9018dfe031d7ff47fae331462ce3c6f2529a5187e7ac4dcc314c4b2b1ee0181d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f791bb0117ebf2a3201f4e238d20bed2b3122750f1445b378fc0eae611b96b1f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c319a500700cdab3d17b4c9975b9700db786183b0133f0a303cb219ac46aea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06b9ca2dd392b229eaced435308d7b9cab73ec8f65a8a0f14c82b72ab4ff50f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600e3d37a290fbd9c67f614b937d8e68e46e0440c8f0ed4e984485bc607098ce(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eefbc3459fdc8a9aaf8b5bac9f16cdafeba522ac1ee65497a86d36c07d23ea97(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EcsClusterSetting]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791a7938883c627fe8392c756189ffdbb52abbbe16ff0315ea134d7ab3356390(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82489dc869ddd9642b1cca0c53cc97850ad2b27ed3a58488bf2f3260ee3ffecb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773207f76dd3ddcdf1e4ce4cc975e6c7266a03f09568a6374cdc74aa7b30d8d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e652b054829a770194b7d929924cfeab4803283b3ca4b744fa0d5ae505ab552(
    value: typing.Optional[typing.Union[EcsClusterSetting, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
