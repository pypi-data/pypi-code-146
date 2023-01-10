'''
# `aws_ec2_host`

Refer to the Terraform Registory for docs: [`aws_ec2_host`](https://www.terraform.io/docs/providers/aws/r/ec2_host).
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


class Ec2Host(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2Host.Ec2Host",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/ec2_host aws_ec2_host}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        auto_placement: typing.Optional[builtins.str] = None,
        host_recovery: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_family: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
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
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/ec2_host aws_ec2_host} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#availability_zone Ec2Host#availability_zone}.
        :param auto_placement: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#auto_placement Ec2Host#auto_placement}.
        :param host_recovery: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#host_recovery Ec2Host#host_recovery}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#id Ec2Host#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_family: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#instance_family Ec2Host#instance_family}.
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#instance_type Ec2Host#instance_type}.
        :param outpost_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#outpost_arn Ec2Host#outpost_arn}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#tags Ec2Host#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#tags_all Ec2Host#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10c83591f50749563bee3a0f789c08b3a9ff6dd37db0eebc4ff73ff9762325bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Ec2HostConfig(
            availability_zone=availability_zone,
            auto_placement=auto_placement,
            host_recovery=host_recovery,
            id=id,
            instance_family=instance_family,
            instance_type=instance_type,
            outpost_arn=outpost_arn,
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

    @jsii.member(jsii_name="resetAutoPlacement")
    def reset_auto_placement(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoPlacement", []))

    @jsii.member(jsii_name="resetHostRecovery")
    def reset_host_recovery(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostRecovery", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceFamily")
    def reset_instance_family(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceFamily", []))

    @jsii.member(jsii_name="resetInstanceType")
    def reset_instance_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceType", []))

    @jsii.member(jsii_name="resetOutpostArn")
    def reset_outpost_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutpostArn", []))

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
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @builtins.property
    @jsii.member(jsii_name="autoPlacementInput")
    def auto_placement_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoPlacementInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="hostRecoveryInput")
    def host_recovery_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostRecoveryInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceFamilyInput")
    def instance_family_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceFamilyInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="outpostArnInput")
    def outpost_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outpostArnInput"))

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
    @jsii.member(jsii_name="autoPlacement")
    def auto_placement(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoPlacement"))

    @auto_placement.setter
    def auto_placement(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b9ad547cf9ee3874b0196243feaaf3165a09fac8c35c5b543122ec7c59257c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoPlacement", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e75286fa628ab0567200132078c2e09a6eeddc22e59f99a22de260cf62401c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="hostRecovery")
    def host_recovery(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostRecovery"))

    @host_recovery.setter
    def host_recovery(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc44c068da38f6f71a5b78330691aca9c8c7d5999b095033137cb1f6554c6607)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostRecovery", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1fb6c31ea89994a97bba80dc37c9c05f41d696da69a7e20eb842fc36bcae38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceFamily")
    def instance_family(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceFamily"))

    @instance_family.setter
    def instance_family(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b226b4624dbfd693ffc0f69399681965b81e9c265f57c198033f5989ddd45e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceFamily", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9087d4408157a904867606ae636b99d6ee5ad2c421f341a292b7fac822d664d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="outpostArn")
    def outpost_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outpostArn"))

    @outpost_arn.setter
    def outpost_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77b8f56ab7d64ec06f79d86f01aedcaa86525d704a20f76d2f4b156caff84ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d63aacda88346f655cd7d0ec30466cd50b4a3ee3f91dc1c179db15180d1047c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__649510691acddbaeaf08375ddd887f72889f7f9f4963d89ef9af3914c2eeb5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2Host.Ec2HostConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "availability_zone": "availabilityZone",
        "auto_placement": "autoPlacement",
        "host_recovery": "hostRecovery",
        "id": "id",
        "instance_family": "instanceFamily",
        "instance_type": "instanceType",
        "outpost_arn": "outpostArn",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class Ec2HostConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        availability_zone: builtins.str,
        auto_placement: typing.Optional[builtins.str] = None,
        host_recovery: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        instance_family: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
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
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#availability_zone Ec2Host#availability_zone}.
        :param auto_placement: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#auto_placement Ec2Host#auto_placement}.
        :param host_recovery: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#host_recovery Ec2Host#host_recovery}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#id Ec2Host#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_family: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#instance_family Ec2Host#instance_family}.
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#instance_type Ec2Host#instance_type}.
        :param outpost_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#outpost_arn Ec2Host#outpost_arn}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#tags Ec2Host#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#tags_all Ec2Host#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b4c1cbb2608b0f74fcbf2b1fe6c4531f4fec121089b6e474e4f9f2114c01a2)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument auto_placement", value=auto_placement, expected_type=type_hints["auto_placement"])
            check_type(argname="argument host_recovery", value=host_recovery, expected_type=type_hints["host_recovery"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_family", value=instance_family, expected_type=type_hints["instance_family"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument outpost_arn", value=outpost_arn, expected_type=type_hints["outpost_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
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
        if auto_placement is not None:
            self._values["auto_placement"] = auto_placement
        if host_recovery is not None:
            self._values["host_recovery"] = host_recovery
        if id is not None:
            self._values["id"] = id
        if instance_family is not None:
            self._values["instance_family"] = instance_family
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if outpost_arn is not None:
            self._values["outpost_arn"] = outpost_arn
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
    def availability_zone(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#availability_zone Ec2Host#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_placement(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#auto_placement Ec2Host#auto_placement}.'''
        result = self._values.get("auto_placement")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_recovery(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#host_recovery Ec2Host#host_recovery}.'''
        result = self._values.get("host_recovery")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#id Ec2Host#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_family(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#instance_family Ec2Host#instance_family}.'''
        result = self._values.get("instance_family")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#instance_type Ec2Host#instance_type}.'''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outpost_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#outpost_arn Ec2Host#outpost_arn}.'''
        result = self._values.get("outpost_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#tags Ec2Host#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_host#tags_all Ec2Host#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2HostConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ec2Host",
    "Ec2HostConfig",
]

publication.publish()

def _typecheckingstub__10c83591f50749563bee3a0f789c08b3a9ff6dd37db0eebc4ff73ff9762325bc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    auto_placement: typing.Optional[builtins.str] = None,
    host_recovery: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_family: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b7b9ad547cf9ee3874b0196243feaaf3165a09fac8c35c5b543122ec7c59257c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e75286fa628ab0567200132078c2e09a6eeddc22e59f99a22de260cf62401c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc44c068da38f6f71a5b78330691aca9c8c7d5999b095033137cb1f6554c6607(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1fb6c31ea89994a97bba80dc37c9c05f41d696da69a7e20eb842fc36bcae38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b226b4624dbfd693ffc0f69399681965b81e9c265f57c198033f5989ddd45e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9087d4408157a904867606ae636b99d6ee5ad2c421f341a292b7fac822d664d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77b8f56ab7d64ec06f79d86f01aedcaa86525d704a20f76d2f4b156caff84ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d63aacda88346f655cd7d0ec30466cd50b4a3ee3f91dc1c179db15180d1047c0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__649510691acddbaeaf08375ddd887f72889f7f9f4963d89ef9af3914c2eeb5f4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b4c1cbb2608b0f74fcbf2b1fe6c4531f4fec121089b6e474e4f9f2114c01a2(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    auto_placement: typing.Optional[builtins.str] = None,
    host_recovery: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    instance_family: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
