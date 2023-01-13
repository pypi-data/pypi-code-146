'''
# `spotinst_multai_target_set`

Refer to the Terraform Registory for docs: [`spotinst_multai_target_set`](https://www.terraform.io/docs/providers/spotinst/r/multai_target_set).
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


class MultaiTargetSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set spotinst_multai_target_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        balancer_id: builtins.str,
        deployment_id: builtins.str,
        health_check: typing.Union["MultaiTargetSetHealthCheck", typing.Dict[builtins.str, typing.Any]],
        protocol: builtins.str,
        weight: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiTargetSetTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set spotinst_multai_target_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param balancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#balancer_id MultaiTargetSet#balancer_id}.
        :param deployment_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#deployment_id MultaiTargetSet#deployment_id}.
        :param health_check: health_check block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#health_check MultaiTargetSet#health_check}
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#protocol MultaiTargetSet#protocol}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#weight MultaiTargetSet#weight}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#id MultaiTargetSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#name MultaiTargetSet#name}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#port MultaiTargetSet#port}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#tags MultaiTargetSet#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d9ea7ddc3719dd65fac29ff79c7455be850295d67a5283695ab88dccdee2f9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MultaiTargetSetConfig(
            balancer_id=balancer_id,
            deployment_id=deployment_id,
            health_check=health_check,
            protocol=protocol,
            weight=weight,
            id=id,
            name=name,
            port=port,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putHealthCheck")
    def put_health_check(
        self,
        *,
        healthy_threshold: jsii.Number,
        interval: jsii.Number,
        path: builtins.str,
        protocol: builtins.str,
        timeout: jsii.Number,
        unhealthy_threshold: jsii.Number,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param healthy_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#healthy_threshold MultaiTargetSet#healthy_threshold}.
        :param interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#interval MultaiTargetSet#interval}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#path MultaiTargetSet#path}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#protocol MultaiTargetSet#protocol}.
        :param timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#timeout MultaiTargetSet#timeout}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#unhealthy_threshold MultaiTargetSet#unhealthy_threshold}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#port MultaiTargetSet#port}.
        '''
        value = MultaiTargetSetHealthCheck(
            healthy_threshold=healthy_threshold,
            interval=interval,
            path=path,
            protocol=protocol,
            timeout=timeout,
            unhealthy_threshold=unhealthy_threshold,
            port=port,
        )

        return typing.cast(None, jsii.invoke(self, "putHealthCheck", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiTargetSetTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd2b4f02dd6a872acb337125d60984d7fe5d2ce2b29591bbae7fb98fcce0bfef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="healthCheck")
    def health_check(self) -> "MultaiTargetSetHealthCheckOutputReference":
        return typing.cast("MultaiTargetSetHealthCheckOutputReference", jsii.get(self, "healthCheck"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "MultaiTargetSetTagsList":
        return typing.cast("MultaiTargetSetTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="balancerIdInput")
    def balancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "balancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deploymentIdInput")
    def deployment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckInput")
    def health_check_input(self) -> typing.Optional["MultaiTargetSetHealthCheck"]:
        return typing.cast(typing.Optional["MultaiTargetSetHealthCheck"], jsii.get(self, "healthCheckInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetSetTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetSetTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="balancerId")
    def balancer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "balancerId"))

    @balancer_id.setter
    def balancer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4060e261b02ab48aaa5735812045e37823e9fabff9bd3876956f6a36df434580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancerId", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentId")
    def deployment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deploymentId"))

    @deployment_id.setter
    def deployment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__330f9bf3e34e86a810a53c563bfbfccbdcab0651d9f4285983c95e23990df609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7693143398448ee50219ce348f9198a2f1ac86259b5b354f5f693f0b52a42bd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bccba75f774d21f5151522f0d953783fa6e77af91439637bf6aaa3e3ecd94c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6380ad433c836c00fea4076df21e6fa37f60095956eef838ca1da2c194e4f0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714b7a701af376f49dad0d6466ba52bb59f91d1f55829c776298dbd7883bf061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07a219354ac019d8a6933d381f1801ab5bf3bf3853c6e129d2b32070cb08d4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "balancer_id": "balancerId",
        "deployment_id": "deploymentId",
        "health_check": "healthCheck",
        "protocol": "protocol",
        "weight": "weight",
        "id": "id",
        "name": "name",
        "port": "port",
        "tags": "tags",
    },
)
class MultaiTargetSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        balancer_id: builtins.str,
        deployment_id: builtins.str,
        health_check: typing.Union["MultaiTargetSetHealthCheck", typing.Dict[builtins.str, typing.Any]],
        protocol: builtins.str,
        weight: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiTargetSetTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param balancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#balancer_id MultaiTargetSet#balancer_id}.
        :param deployment_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#deployment_id MultaiTargetSet#deployment_id}.
        :param health_check: health_check block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#health_check MultaiTargetSet#health_check}
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#protocol MultaiTargetSet#protocol}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#weight MultaiTargetSet#weight}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#id MultaiTargetSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#name MultaiTargetSet#name}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#port MultaiTargetSet#port}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#tags MultaiTargetSet#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(health_check, dict):
            health_check = MultaiTargetSetHealthCheck(**health_check)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83def819c238b6b1ae29aec7e2ba0c1814c17b0c2d72f422840261316f2a7d94)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument balancer_id", value=balancer_id, expected_type=type_hints["balancer_id"])
            check_type(argname="argument deployment_id", value=deployment_id, expected_type=type_hints["deployment_id"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "balancer_id": balancer_id,
            "deployment_id": deployment_id,
            "health_check": health_check,
            "protocol": protocol,
            "weight": weight,
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
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if tags is not None:
            self._values["tags"] = tags

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
    def balancer_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#balancer_id MultaiTargetSet#balancer_id}.'''
        result = self._values.get("balancer_id")
        assert result is not None, "Required property 'balancer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#deployment_id MultaiTargetSet#deployment_id}.'''
        result = self._values.get("deployment_id")
        assert result is not None, "Required property 'deployment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def health_check(self) -> "MultaiTargetSetHealthCheck":
        '''health_check block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#health_check MultaiTargetSet#health_check}
        '''
        result = self._values.get("health_check")
        assert result is not None, "Required property 'health_check' is missing"
        return typing.cast("MultaiTargetSetHealthCheck", result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#protocol MultaiTargetSet#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#weight MultaiTargetSet#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#id MultaiTargetSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#name MultaiTargetSet#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#port MultaiTargetSet#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetSetTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#tags MultaiTargetSet#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetSetTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiTargetSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSetHealthCheck",
    jsii_struct_bases=[],
    name_mapping={
        "healthy_threshold": "healthyThreshold",
        "interval": "interval",
        "path": "path",
        "protocol": "protocol",
        "timeout": "timeout",
        "unhealthy_threshold": "unhealthyThreshold",
        "port": "port",
    },
)
class MultaiTargetSetHealthCheck:
    def __init__(
        self,
        *,
        healthy_threshold: jsii.Number,
        interval: jsii.Number,
        path: builtins.str,
        protocol: builtins.str,
        timeout: jsii.Number,
        unhealthy_threshold: jsii.Number,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param healthy_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#healthy_threshold MultaiTargetSet#healthy_threshold}.
        :param interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#interval MultaiTargetSet#interval}.
        :param path: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#path MultaiTargetSet#path}.
        :param protocol: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#protocol MultaiTargetSet#protocol}.
        :param timeout: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#timeout MultaiTargetSet#timeout}.
        :param unhealthy_threshold: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#unhealthy_threshold MultaiTargetSet#unhealthy_threshold}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#port MultaiTargetSet#port}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f500b98328c3236f7fed7f5ccdf06d0fcbc6009c28154fc859cc28a2a0c25f7)
            check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "healthy_threshold": healthy_threshold,
            "interval": interval,
            "path": path,
            "protocol": protocol,
            "timeout": timeout,
            "unhealthy_threshold": unhealthy_threshold,
        }
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def healthy_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#healthy_threshold MultaiTargetSet#healthy_threshold}.'''
        result = self._values.get("healthy_threshold")
        assert result is not None, "Required property 'healthy_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#interval MultaiTargetSet#interval}.'''
        result = self._values.get("interval")
        assert result is not None, "Required property 'interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#path MultaiTargetSet#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#protocol MultaiTargetSet#protocol}.'''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def timeout(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#timeout MultaiTargetSet#timeout}.'''
        result = self._values.get("timeout")
        assert result is not None, "Required property 'timeout' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def unhealthy_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#unhealthy_threshold MultaiTargetSet#unhealthy_threshold}.'''
        result = self._values.get("unhealthy_threshold")
        assert result is not None, "Required property 'unhealthy_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#port MultaiTargetSet#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiTargetSetHealthCheck(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MultaiTargetSetHealthCheckOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSetHealthCheckOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d59771b63cd870938a197242e133db088fbda250d737991457ab3b4139f4d89)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @builtins.property
    @jsii.member(jsii_name="healthyThresholdInput")
    def healthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "intervalInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolInput")
    def protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocolInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInput")
    def timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="unhealthyThresholdInput")
    def unhealthy_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unhealthyThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="healthyThreshold")
    def healthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthyThreshold"))

    @healthy_threshold.setter
    def healthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355c80fc42f0b5aa050da58f8dd977413c5078f800e2b0ff67d6d4c1c351d1ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthyThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f801af8d640bc28f7b929c54432e4eeb075cca081f3ebe6e1c6bcaa64039d953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae426adc84eb3dfa5e86afaf7fc0dd37b4aeca2544f6d6e6a3c6c5bd9315a6fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f3b46234343ca2cbf771a44900633048b7c25601f4d2c7ce0bcaa1009e354a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bee92169012208918a267d6cafaf5ca1da7eaca3581cfc87289f8062bc7db5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7779961ac251ffc2333108f09b41e81e51e9ea70ea6db982c9707335e6a13d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @builtins.property
    @jsii.member(jsii_name="unhealthyThreshold")
    def unhealthy_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "unhealthyThreshold"))

    @unhealthy_threshold.setter
    def unhealthy_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5450a185f821ef3cf18fac0a9f01456028fc0fb831184f74d154ef40f41dd50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unhealthyThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MultaiTargetSetHealthCheck]:
        return typing.cast(typing.Optional[MultaiTargetSetHealthCheck], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MultaiTargetSetHealthCheck],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3a6cb2be5ff02d866a10db684554883faf9630c6f9c4e93bcca51b136c9c70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSetTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class MultaiTargetSetTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#key MultaiTargetSet#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#value MultaiTargetSet#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae28f69a507448f817916e790473f20d9a1abca39175fcd498946f2027ae394)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#key MultaiTargetSet#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target_set#value MultaiTargetSet#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiTargetSetTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MultaiTargetSetTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSetTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__083be320e00782e67971f2b26f2e0223f0fb3d679bb8931bcf4a1da2449dbf3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MultaiTargetSetTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffe90df8c610a56858bfd65b552b63b9ab2e97aaaa491a4d555ed2d33a6da089)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MultaiTargetSetTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ae64a9df3b779acf03939455f5c67f293b04c19dcd92ec783f9bdfebc643593)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fb31b36fa5c974e8b8485dd45dc1e8994dbcba984799455475239408723ff6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fac9a76c518e04190ef90d9d7f5f0e8d097bbf7ad52ac82160ee80d9e3ccdbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetSetTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetSetTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetSetTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b912224fd351e3593388c91cfca68a8437b767eb22e607c524ba6cb3ab8c1e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MultaiTargetSetTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTargetSet.MultaiTargetSetTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9a7cc0f103f0e8b57405d42b37a997c82776a686159e6417c94dc2d5ce20f52)
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
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff07ba406c9570f7b92ae1e80929804bfd6713b9fb03bfca926c449f682a804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f99bcaafa95dc88a557386ee3dfc81987aeb499592a3425b9e0460c3e702c3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MultaiTargetSetTags, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MultaiTargetSetTags, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MultaiTargetSetTags, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91ccbb841bc9885eb082309bac8a41c7a407c76b0d295f3e6d3f8f5e442f8acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MultaiTargetSet",
    "MultaiTargetSetConfig",
    "MultaiTargetSetHealthCheck",
    "MultaiTargetSetHealthCheckOutputReference",
    "MultaiTargetSetTags",
    "MultaiTargetSetTagsList",
    "MultaiTargetSetTagsOutputReference",
]

publication.publish()

def _typecheckingstub__89d9ea7ddc3719dd65fac29ff79c7455be850295d67a5283695ab88dccdee2f9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    balancer_id: builtins.str,
    deployment_id: builtins.str,
    health_check: typing.Union[MultaiTargetSetHealthCheck, typing.Dict[builtins.str, typing.Any]],
    protocol: builtins.str,
    weight: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiTargetSetTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__dd2b4f02dd6a872acb337125d60984d7fe5d2ce2b29591bbae7fb98fcce0bfef(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiTargetSetTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4060e261b02ab48aaa5735812045e37823e9fabff9bd3876956f6a36df434580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__330f9bf3e34e86a810a53c563bfbfccbdcab0651d9f4285983c95e23990df609(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7693143398448ee50219ce348f9198a2f1ac86259b5b354f5f693f0b52a42bd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bccba75f774d21f5151522f0d953783fa6e77af91439637bf6aaa3e3ecd94c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6380ad433c836c00fea4076df21e6fa37f60095956eef838ca1da2c194e4f0f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714b7a701af376f49dad0d6466ba52bb59f91d1f55829c776298dbd7883bf061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07a219354ac019d8a6933d381f1801ab5bf3bf3853c6e129d2b32070cb08d4d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83def819c238b6b1ae29aec7e2ba0c1814c17b0c2d72f422840261316f2a7d94(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    balancer_id: builtins.str,
    deployment_id: builtins.str,
    health_check: typing.Union[MultaiTargetSetHealthCheck, typing.Dict[builtins.str, typing.Any]],
    protocol: builtins.str,
    weight: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiTargetSetTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f500b98328c3236f7fed7f5ccdf06d0fcbc6009c28154fc859cc28a2a0c25f7(
    *,
    healthy_threshold: jsii.Number,
    interval: jsii.Number,
    path: builtins.str,
    protocol: builtins.str,
    timeout: jsii.Number,
    unhealthy_threshold: jsii.Number,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d59771b63cd870938a197242e133db088fbda250d737991457ab3b4139f4d89(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__355c80fc42f0b5aa050da58f8dd977413c5078f800e2b0ff67d6d4c1c351d1ac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f801af8d640bc28f7b929c54432e4eeb075cca081f3ebe6e1c6bcaa64039d953(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae426adc84eb3dfa5e86afaf7fc0dd37b4aeca2544f6d6e6a3c6c5bd9315a6fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f3b46234343ca2cbf771a44900633048b7c25601f4d2c7ce0bcaa1009e354a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bee92169012208918a267d6cafaf5ca1da7eaca3581cfc87289f8062bc7db5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7779961ac251ffc2333108f09b41e81e51e9ea70ea6db982c9707335e6a13d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5450a185f821ef3cf18fac0a9f01456028fc0fb831184f74d154ef40f41dd50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3a6cb2be5ff02d866a10db684554883faf9630c6f9c4e93bcca51b136c9c70(
    value: typing.Optional[MultaiTargetSetHealthCheck],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae28f69a507448f817916e790473f20d9a1abca39175fcd498946f2027ae394(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__083be320e00782e67971f2b26f2e0223f0fb3d679bb8931bcf4a1da2449dbf3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe90df8c610a56858bfd65b552b63b9ab2e97aaaa491a4d555ed2d33a6da089(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ae64a9df3b779acf03939455f5c67f293b04c19dcd92ec783f9bdfebc643593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb31b36fa5c974e8b8485dd45dc1e8994dbcba984799455475239408723ff6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fac9a76c518e04190ef90d9d7f5f0e8d097bbf7ad52ac82160ee80d9e3ccdbe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b912224fd351e3593388c91cfca68a8437b767eb22e607c524ba6cb3ab8c1e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetSetTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9a7cc0f103f0e8b57405d42b37a997c82776a686159e6417c94dc2d5ce20f52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff07ba406c9570f7b92ae1e80929804bfd6713b9fb03bfca926c449f682a804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f99bcaafa95dc88a557386ee3dfc81987aeb499592a3425b9e0460c3e702c3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ccbb841bc9885eb082309bac8a41c7a407c76b0d295f3e6d3f8f5e442f8acc(
    value: typing.Optional[typing.Union[MultaiTargetSetTags, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
