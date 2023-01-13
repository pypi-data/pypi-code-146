'''
# `spotinst_multai_target`

Refer to the Terraform Registory for docs: [`spotinst_multai_target`](https://www.terraform.io/docs/providers/spotinst/r/multai_target).
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


class MultaiTarget(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTarget.MultaiTarget",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target spotinst_multai_target}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        balancer_id: builtins.str,
        host: builtins.str,
        target_set_id: builtins.str,
        weight: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiTargetTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target spotinst_multai_target} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param balancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#balancer_id MultaiTarget#balancer_id}.
        :param host: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#host MultaiTarget#host}.
        :param target_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#target_set_id MultaiTarget#target_set_id}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#weight MultaiTarget#weight}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#id MultaiTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#name MultaiTarget#name}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#port MultaiTarget#port}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#tags MultaiTarget#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d38e3f33c3073f3ca9bf8eafc2cc02cc36bce6f69c9be6b30d5b79466fd394c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MultaiTargetConfig(
            balancer_id=balancer_id,
            host=host,
            target_set_id=target_set_id,
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

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiTargetTags", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df9ccb520f9797485f97f85237dab6029d3443d2727f4878e561ead2c4b15150)
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
    @jsii.member(jsii_name="tags")
    def tags(self) -> "MultaiTargetTagsList":
        return typing.cast("MultaiTargetTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="balancerIdInput")
    def balancer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "balancerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

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
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetTags"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetTags"]]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetSetIdInput")
    def target_set_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetSetIdInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__874a63f0148f50e8fb6a61e3e60500ccb5e95dcb40c0ea61d9d72f8134b42378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "balancerId", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ef7ebf7a75b0f49fcff7cebae90ed8b166e61b9462ddbd7e2a79886753cd66a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d3c065c0b3fcf8fbd8e9e3794fe26828f891cb7835c74aec3a80de6f6224d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d9de9d35d5940f2fb4c06faef8a4cb1cbc3e8b5b22da8928c0e57c28396f068)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c315d04a427b2a3f0ca9afc7508c34530c325a46e022699d75ba05a914b2fe4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="targetSetId")
    def target_set_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetSetId"))

    @target_set_id.setter
    def target_set_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55567e6868e0dc59357b2b6cc9e39eae0959749d256115a0e618350c27b8b193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetSetId", value)

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27ec9d4aa0b56dbe4f177e53540a503c46b854be1e9e919653704c70eb4fc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiTarget.MultaiTargetConfig",
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
        "host": "host",
        "target_set_id": "targetSetId",
        "weight": "weight",
        "id": "id",
        "name": "name",
        "port": "port",
        "tags": "tags",
    },
)
class MultaiTargetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        host: builtins.str,
        target_set_id: builtins.str,
        weight: jsii.Number,
        id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MultaiTargetTags", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param balancer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#balancer_id MultaiTarget#balancer_id}.
        :param host: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#host MultaiTarget#host}.
        :param target_set_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#target_set_id MultaiTarget#target_set_id}.
        :param weight: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#weight MultaiTarget#weight}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#id MultaiTarget#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#name MultaiTarget#name}.
        :param port: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#port MultaiTarget#port}.
        :param tags: tags block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#tags MultaiTarget#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9aad428c5526088cbc820ead09b71b8cf0b6e18203228fafea85d7d6f03715a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument balancer_id", value=balancer_id, expected_type=type_hints["balancer_id"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument target_set_id", value=target_set_id, expected_type=type_hints["target_set_id"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "balancer_id": balancer_id,
            "host": host,
            "target_set_id": target_set_id,
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#balancer_id MultaiTarget#balancer_id}.'''
        result = self._values.get("balancer_id")
        assert result is not None, "Required property 'balancer_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#host MultaiTarget#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_set_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#target_set_id MultaiTarget#target_set_id}.'''
        result = self._values.get("target_set_id")
        assert result is not None, "Required property 'target_set_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#weight MultaiTarget#weight}.'''
        result = self._values.get("weight")
        assert result is not None, "Required property 'weight' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#id MultaiTarget#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#name MultaiTarget#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#port MultaiTarget#port}.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetTags"]]]:
        '''tags block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#tags MultaiTarget#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MultaiTargetTags"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-spotinst.multaiTarget.MultaiTargetTags",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class MultaiTargetTags:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#key MultaiTarget#key}.
        :param value: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#value MultaiTarget#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7aecf7c3b2517e5ea6d91786986907eb5f1b402219f815474ee41360562c2f)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#key MultaiTarget#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/spotinst/r/multai_target#value MultaiTarget#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultaiTargetTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MultaiTargetTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTarget.MultaiTargetTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ed2a4f26321ce60bf2b0f5de9ac23aa95a7c8ff406d20f2320ce57d62dcd100)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MultaiTargetTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb6986126b720a3576ccae14415e837ee55eaec5be63d69e1c36c9fb6fc684be)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MultaiTargetTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ffb1ea916545fe7c51455d2440034a0c94c9b17484d524ff2bf6dd29a29f921)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dafc6fc4a10804a5b01cf5c92c7f335fbc51dabc2ef4ad1dd5212f6e12d24a57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e16fe71fd806ee8f4cca75b2ac10d977c8719dce0456d56122484a77bbab7d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetTags]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetTags]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetTags]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97c334f6651d89cf1930085822084f73eb652218d240948ac20549893be667f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MultaiTargetTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-spotinst.multaiTarget.MultaiTargetTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af01d3a3bcdf103a550df9698408032151c193f7f0bbc85642489204a661151c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e882558eea3136a6bbc12ece9152cee4cab4e4f6d198ee606d190dfc380d8947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d27055a898a387268d6062f187239d06851e025fa2eb5dbb0678c046d4079a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MultaiTargetTags, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MultaiTargetTags, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MultaiTargetTags, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cbbdd177cf3f7e256fbf94eacfeba9446840e9c126c2699bee01f889c3bd8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MultaiTarget",
    "MultaiTargetConfig",
    "MultaiTargetTags",
    "MultaiTargetTagsList",
    "MultaiTargetTagsOutputReference",
]

publication.publish()

def _typecheckingstub__1d38e3f33c3073f3ca9bf8eafc2cc02cc36bce6f69c9be6b30d5b79466fd394c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    balancer_id: builtins.str,
    host: builtins.str,
    target_set_id: builtins.str,
    weight: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiTargetTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__df9ccb520f9797485f97f85237dab6029d3443d2727f4878e561ead2c4b15150(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiTargetTags, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874a63f0148f50e8fb6a61e3e60500ccb5e95dcb40c0ea61d9d72f8134b42378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef7ebf7a75b0f49fcff7cebae90ed8b166e61b9462ddbd7e2a79886753cd66a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d3c065c0b3fcf8fbd8e9e3794fe26828f891cb7835c74aec3a80de6f6224d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d9de9d35d5940f2fb4c06faef8a4cb1cbc3e8b5b22da8928c0e57c28396f068(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c315d04a427b2a3f0ca9afc7508c34530c325a46e022699d75ba05a914b2fe4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55567e6868e0dc59357b2b6cc9e39eae0959749d256115a0e618350c27b8b193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27ec9d4aa0b56dbe4f177e53540a503c46b854be1e9e919653704c70eb4fc6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9aad428c5526088cbc820ead09b71b8cf0b6e18203228fafea85d7d6f03715a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    balancer_id: builtins.str,
    host: builtins.str,
    target_set_id: builtins.str,
    weight: jsii.Number,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MultaiTargetTags, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7aecf7c3b2517e5ea6d91786986907eb5f1b402219f815474ee41360562c2f(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed2a4f26321ce60bf2b0f5de9ac23aa95a7c8ff406d20f2320ce57d62dcd100(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6986126b720a3576ccae14415e837ee55eaec5be63d69e1c36c9fb6fc684be(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffb1ea916545fe7c51455d2440034a0c94c9b17484d524ff2bf6dd29a29f921(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dafc6fc4a10804a5b01cf5c92c7f335fbc51dabc2ef4ad1dd5212f6e12d24a57(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e16fe71fd806ee8f4cca75b2ac10d977c8719dce0456d56122484a77bbab7d9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97c334f6651d89cf1930085822084f73eb652218d240948ac20549893be667f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MultaiTargetTags]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af01d3a3bcdf103a550df9698408032151c193f7f0bbc85642489204a661151c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e882558eea3136a6bbc12ece9152cee4cab4e4f6d198ee606d190dfc380d8947(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d27055a898a387268d6062f187239d06851e025fa2eb5dbb0678c046d4079a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cbbdd177cf3f7e256fbf94eacfeba9446840e9c126c2699bee01f889c3bd8f(
    value: typing.Optional[typing.Union[MultaiTargetTags, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
