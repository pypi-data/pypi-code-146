'''
# `data_aws_vpc_peering_connection`

Refer to the Terraform Registory for docs: [`data_aws_vpc_peering_connection`](https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection).
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


class DataAwsVpcPeeringConnection(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnection",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection aws_vpc_peering_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cidr_block: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsVpcPeeringConnectionFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        peer_cidr_block: typing.Optional[builtins.str] = None,
        peer_owner_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
        peer_vpc_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DataAwsVpcPeeringConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection aws_vpc_peering_connection} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cidr_block: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#cidr_block DataAwsVpcPeeringConnection#cidr_block}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#filter DataAwsVpcPeeringConnection#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#id DataAwsVpcPeeringConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#owner_id DataAwsVpcPeeringConnection#owner_id}.
        :param peer_cidr_block: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_cidr_block DataAwsVpcPeeringConnection#peer_cidr_block}.
        :param peer_owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_owner_id DataAwsVpcPeeringConnection#peer_owner_id}.
        :param peer_region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_region DataAwsVpcPeeringConnection#peer_region}.
        :param peer_vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_vpc_id DataAwsVpcPeeringConnection#peer_vpc_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#region DataAwsVpcPeeringConnection#region}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#status DataAwsVpcPeeringConnection#status}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#tags DataAwsVpcPeeringConnection#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#timeouts DataAwsVpcPeeringConnection#timeouts}
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#vpc_id DataAwsVpcPeeringConnection#vpc_id}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961fdd8f90331188ecff5d232adcd43441b574742f26c64244041d99ea450a47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataAwsVpcPeeringConnectionConfig(
            cidr_block=cidr_block,
            filter=filter,
            id=id,
            owner_id=owner_id,
            peer_cidr_block=peer_cidr_block,
            peer_owner_id=peer_owner_id,
            peer_region=peer_region,
            peer_vpc_id=peer_vpc_id,
            region=region,
            status=status,
            tags=tags,
            timeouts=timeouts,
            vpc_id=vpc_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putFilter")
    def put_filter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsVpcPeeringConnectionFilter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b32d117ebc2cb0a51f12b183b67e8ae0560970bd0df39ab424cf31185ec9e4f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilter", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#read DataAwsVpcPeeringConnection#read}.
        '''
        value = DataAwsVpcPeeringConnectionTimeouts(read=read)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCidrBlock")
    def reset_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCidrBlock", []))

    @jsii.member(jsii_name="resetFilter")
    def reset_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilter", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOwnerId")
    def reset_owner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOwnerId", []))

    @jsii.member(jsii_name="resetPeerCidrBlock")
    def reset_peer_cidr_block(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerCidrBlock", []))

    @jsii.member(jsii_name="resetPeerOwnerId")
    def reset_peer_owner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerOwnerId", []))

    @jsii.member(jsii_name="resetPeerRegion")
    def reset_peer_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerRegion", []))

    @jsii.member(jsii_name="resetPeerVpcId")
    def reset_peer_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPeerVpcId", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVpcId")
    def reset_vpc_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVpcId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accepter")
    def accepter(self) -> _cdktf_9a9027ec.BooleanMap:
        return typing.cast(_cdktf_9a9027ec.BooleanMap, jsii.get(self, "accepter"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlockSet")
    def cidr_block_set(self) -> "DataAwsVpcPeeringConnectionCidrBlockSetList":
        return typing.cast("DataAwsVpcPeeringConnectionCidrBlockSetList", jsii.get(self, "cidrBlockSet"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> "DataAwsVpcPeeringConnectionFilterList":
        return typing.cast("DataAwsVpcPeeringConnectionFilterList", jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="peerCidrBlockSet")
    def peer_cidr_block_set(self) -> "DataAwsVpcPeeringConnectionPeerCidrBlockSetList":
        return typing.cast("DataAwsVpcPeeringConnectionPeerCidrBlockSetList", jsii.get(self, "peerCidrBlockSet"))

    @builtins.property
    @jsii.member(jsii_name="requester")
    def requester(self) -> _cdktf_9a9027ec.BooleanMap:
        return typing.cast(_cdktf_9a9027ec.BooleanMap, jsii.get(self, "requester"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DataAwsVpcPeeringConnectionTimeoutsOutputReference":
        return typing.cast("DataAwsVpcPeeringConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlockInput")
    def cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="filterInput")
    def filter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsVpcPeeringConnectionFilter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsVpcPeeringConnectionFilter"]]], jsii.get(self, "filterInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerIdInput")
    def owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerCidrBlockInput")
    def peer_cidr_block_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerCidrBlockInput"))

    @builtins.property
    @jsii.member(jsii_name="peerOwnerIdInput")
    def peer_owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerOwnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="peerRegionInput")
    def peer_region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerRegionInput"))

    @builtins.property
    @jsii.member(jsii_name="peerVpcIdInput")
    def peer_vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "peerVpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["DataAwsVpcPeeringConnectionTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["DataAwsVpcPeeringConnectionTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidrBlock"))

    @cidr_block.setter
    def cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d11be95f7b20baaa296f2b35febda97549e3d3cfc6ee0d68e951938e4f0ac68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrBlock", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__772820e03c483e0abe866ec8cc93533b4d2b738713fdc59d7dd2721c875f919d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @owner_id.setter
    def owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f49a517c65138ef4e82df63ed48b0cf13cb9b9b312a6be1055eee573953b6ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerId", value)

    @builtins.property
    @jsii.member(jsii_name="peerCidrBlock")
    def peer_cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerCidrBlock"))

    @peer_cidr_block.setter
    def peer_cidr_block(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3fd66b8527d5a9b502df94af55d1e494f642ba6c495e5be2fbb787af6aa7885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerCidrBlock", value)

    @builtins.property
    @jsii.member(jsii_name="peerOwnerId")
    def peer_owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerOwnerId"))

    @peer_owner_id.setter
    def peer_owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26d219e9c0122d4cbd13c38c5e37319ccc86dcd39d38accfdb562f4a5139183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerOwnerId", value)

    @builtins.property
    @jsii.member(jsii_name="peerRegion")
    def peer_region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerRegion"))

    @peer_region.setter
    def peer_region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5232786f3649aa6112300aa67b789d3cb876c6863f82c94b434055a7129b6a50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerRegion", value)

    @builtins.property
    @jsii.member(jsii_name="peerVpcId")
    def peer_vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "peerVpcId"))

    @peer_vpc_id.setter
    def peer_vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b031ca2c4113893a9be66ccb210d7aac8138429ec0f01b44ba32cb88b5fb312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "peerVpcId", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b187d30aeea5e9bba270c344c18437e1aa7b4b2c813181caf881770575fd0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ecc967d10113cda8bf5cd57e3d9bb75d6e58b932a59128c174b19ccea0f9e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa8fad4d872b27ec045ebc929eabee6781c0817bb829009b75179f645817add7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde0c2232bcef3700af0db9880e0087cefbd03adf20e025425e0444cb81fccae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionCidrBlockSet",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsVpcPeeringConnectionCidrBlockSet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsVpcPeeringConnectionCidrBlockSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsVpcPeeringConnectionCidrBlockSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionCidrBlockSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14e4c20c10693c65ac1e450850246b7b78f95cb5650723701ee370b9de78373a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsVpcPeeringConnectionCidrBlockSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070b829cd85fd9928b99d4e6a605087e6bfb07a404e88debc0e6cc78afde74ca)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsVpcPeeringConnectionCidrBlockSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd5b4f42705fe7a6b41205393d8c1944f699c5515e5ed6c6f55da07b658dc02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4902ce0f375e29ec388c27b32aef6bcb3fd832c8bf78b2f295d450b2fe36f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b500509db177630f079b9406216c723e1003f1aed6ee3a59bbbf7803cd83b91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsVpcPeeringConnectionCidrBlockSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionCidrBlockSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8582188076a6ce8fba37542b408d5b52d9730df2d00a19539f8d47a5762cdcf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAwsVpcPeeringConnectionCidrBlockSet]:
        return typing.cast(typing.Optional[DataAwsVpcPeeringConnectionCidrBlockSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsVpcPeeringConnectionCidrBlockSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afbc62513936a7e650b3d5b0408d005eb92254b3cba9ef25a48dde9ae3cda8f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cidr_block": "cidrBlock",
        "filter": "filter",
        "id": "id",
        "owner_id": "ownerId",
        "peer_cidr_block": "peerCidrBlock",
        "peer_owner_id": "peerOwnerId",
        "peer_region": "peerRegion",
        "peer_vpc_id": "peerVpcId",
        "region": "region",
        "status": "status",
        "tags": "tags",
        "timeouts": "timeouts",
        "vpc_id": "vpcId",
    },
)
class DataAwsVpcPeeringConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cidr_block: typing.Optional[builtins.str] = None,
        filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataAwsVpcPeeringConnectionFilter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        owner_id: typing.Optional[builtins.str] = None,
        peer_cidr_block: typing.Optional[builtins.str] = None,
        peer_owner_id: typing.Optional[builtins.str] = None,
        peer_region: typing.Optional[builtins.str] = None,
        peer_vpc_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DataAwsVpcPeeringConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cidr_block: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#cidr_block DataAwsVpcPeeringConnection#cidr_block}.
        :param filter: filter block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#filter DataAwsVpcPeeringConnection#filter}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#id DataAwsVpcPeeringConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#owner_id DataAwsVpcPeeringConnection#owner_id}.
        :param peer_cidr_block: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_cidr_block DataAwsVpcPeeringConnection#peer_cidr_block}.
        :param peer_owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_owner_id DataAwsVpcPeeringConnection#peer_owner_id}.
        :param peer_region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_region DataAwsVpcPeeringConnection#peer_region}.
        :param peer_vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_vpc_id DataAwsVpcPeeringConnection#peer_vpc_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#region DataAwsVpcPeeringConnection#region}.
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#status DataAwsVpcPeeringConnection#status}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#tags DataAwsVpcPeeringConnection#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#timeouts DataAwsVpcPeeringConnection#timeouts}
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#vpc_id DataAwsVpcPeeringConnection#vpc_id}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DataAwsVpcPeeringConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11c456d8a0445ae5bbbcd4182f0f64e368a347f8f1b1cb934b17d6a7f432573)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument peer_cidr_block", value=peer_cidr_block, expected_type=type_hints["peer_cidr_block"])
            check_type(argname="argument peer_owner_id", value=peer_owner_id, expected_type=type_hints["peer_owner_id"])
            check_type(argname="argument peer_region", value=peer_region, expected_type=type_hints["peer_region"])
            check_type(argname="argument peer_vpc_id", value=peer_vpc_id, expected_type=type_hints["peer_vpc_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if cidr_block is not None:
            self._values["cidr_block"] = cidr_block
        if filter is not None:
            self._values["filter"] = filter
        if id is not None:
            self._values["id"] = id
        if owner_id is not None:
            self._values["owner_id"] = owner_id
        if peer_cidr_block is not None:
            self._values["peer_cidr_block"] = peer_cidr_block
        if peer_owner_id is not None:
            self._values["peer_owner_id"] = peer_owner_id
        if peer_region is not None:
            self._values["peer_region"] = peer_region
        if peer_vpc_id is not None:
            self._values["peer_vpc_id"] = peer_vpc_id
        if region is not None:
            self._values["region"] = region
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

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
    def cidr_block(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#cidr_block DataAwsVpcPeeringConnection#cidr_block}.'''
        result = self._values.get("cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsVpcPeeringConnectionFilter"]]]:
        '''filter block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#filter DataAwsVpcPeeringConnection#filter}
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataAwsVpcPeeringConnectionFilter"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#id DataAwsVpcPeeringConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owner_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#owner_id DataAwsVpcPeeringConnection#owner_id}.'''
        result = self._values.get("owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_cidr_block(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_cidr_block DataAwsVpcPeeringConnection#peer_cidr_block}.'''
        result = self._values.get("peer_cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_owner_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_owner_id DataAwsVpcPeeringConnection#peer_owner_id}.'''
        result = self._values.get("peer_owner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_region DataAwsVpcPeeringConnection#peer_region}.'''
        result = self._values.get("peer_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peer_vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#peer_vpc_id DataAwsVpcPeeringConnection#peer_vpc_id}.'''
        result = self._values.get("peer_vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#region DataAwsVpcPeeringConnection#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#status DataAwsVpcPeeringConnection#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#tags DataAwsVpcPeeringConnection#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DataAwsVpcPeeringConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#timeouts DataAwsVpcPeeringConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DataAwsVpcPeeringConnectionTimeouts"], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#vpc_id DataAwsVpcPeeringConnection#vpc_id}.'''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsVpcPeeringConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionFilter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class DataAwsVpcPeeringConnectionFilter:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#name DataAwsVpcPeeringConnection#name}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#values DataAwsVpcPeeringConnection#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e774ee3423578ebdfd6d87a8b213d3e547ac832aaaca9013b2e99ad4a78d0684)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#name DataAwsVpcPeeringConnection#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#values DataAwsVpcPeeringConnection#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsVpcPeeringConnectionFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsVpcPeeringConnectionFilterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionFilterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f86765f71fafb5c96380627fbf30826efd59dcdc9d538a72a85cb7c4bfbd8b10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsVpcPeeringConnectionFilterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b01121e6c0e8f05c51967eb6f5a022e6f319074de65877a7e7f637b64207a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsVpcPeeringConnectionFilterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b3bd3b976ea14b763a6b5eaf75b0afb9dd3b3da708973dfd7c579bd57b210e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c316edbe0c1ebaf9c2bc3fdcf2f6a305e1500fb9743155f241de438236470d8b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f7280453965c3651a7fcf96dffcb9db7ca57d7b74ff35fe10ec8d60ac9e58df7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsVpcPeeringConnectionFilter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsVpcPeeringConnectionFilter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsVpcPeeringConnectionFilter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__095a7808fda0e52b9d2f393d0f23d2e8ed0a287e7a644e554c0c96f07d1c62b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataAwsVpcPeeringConnectionFilterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionFilterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2796611b64480f63c0e8a15d9dddf36cefcccfd0754594e1394015bda5db4027)
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
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__706b62410f013ed2eaacdaca5fe8b510ae2aa42a21379ed14a2efffd57085859)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35762abd04c094a6fb3b9fed380bdec72e8e4d4c3441363e5bba70ddd25a6dfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsVpcPeeringConnectionFilter, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsVpcPeeringConnectionFilter, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsVpcPeeringConnectionFilter, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659bf80f1972dd31462d27aa27998c0cc0123f930376c82c6e991df111281405)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionPeerCidrBlockSet",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataAwsVpcPeeringConnectionPeerCidrBlockSet:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsVpcPeeringConnectionPeerCidrBlockSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsVpcPeeringConnectionPeerCidrBlockSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionPeerCidrBlockSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d43bd2f1e9424c2762f6be90e81c2b0eb0298f18b2cfb2dfb2dae00a2282f76)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataAwsVpcPeeringConnectionPeerCidrBlockSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff927905e2191d3a03d3bf79495fc5025168453e0806c489bc788696975d752a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataAwsVpcPeeringConnectionPeerCidrBlockSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fdcf456a63f213dee4b79607d7bd1603f80ab4cf8308292e4f956354f2aa595)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fae7c78e355b815a03b3c2a82ca03831cb4b512da6f90ad4e58fba03a1906937)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50b9e5f5e66fa6a2dde961c128780d8cdcc6db1790e7b8bec61295afb27d031b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataAwsVpcPeeringConnectionPeerCidrBlockSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionPeerCidrBlockSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4929ef28bd659a18e9861269ea409183087dc0ebcd67e88ab5cdaaf4055d3d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cidrBlock")
    def cidr_block(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cidrBlock"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataAwsVpcPeeringConnectionPeerCidrBlockSet]:
        return typing.cast(typing.Optional[DataAwsVpcPeeringConnectionPeerCidrBlockSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataAwsVpcPeeringConnectionPeerCidrBlockSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f534450f6e5fd55a7145c5e20196cec1fd217c6e97e40aa6294c1e09e8fca0b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"read": "read"},
)
class DataAwsVpcPeeringConnectionTimeouts:
    def __init__(self, *, read: typing.Optional[builtins.str] = None) -> None:
        '''
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#read DataAwsVpcPeeringConnection#read}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08c5cf8e695b5910f7f271c1c81a33703e25021d1c2172723f609cc61627788d)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/d/vpc_peering_connection#read DataAwsVpcPeeringConnection#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataAwsVpcPeeringConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataAwsVpcPeeringConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.dataAwsVpcPeeringConnection.DataAwsVpcPeeringConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78963b66f2aa600e93e15ab4947486830aa5cecec8f172de2c6e8d9dee8d2e4c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c455f06ddf975d2517f70e4d5d1e0433c5c82169ca11f4cfd0832804ef7fae9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataAwsVpcPeeringConnectionTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataAwsVpcPeeringConnectionTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataAwsVpcPeeringConnectionTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8d4ee0e8c999675b1cd6ccaa97922910250b58bd66b262817de23a2166212c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataAwsVpcPeeringConnection",
    "DataAwsVpcPeeringConnectionCidrBlockSet",
    "DataAwsVpcPeeringConnectionCidrBlockSetList",
    "DataAwsVpcPeeringConnectionCidrBlockSetOutputReference",
    "DataAwsVpcPeeringConnectionConfig",
    "DataAwsVpcPeeringConnectionFilter",
    "DataAwsVpcPeeringConnectionFilterList",
    "DataAwsVpcPeeringConnectionFilterOutputReference",
    "DataAwsVpcPeeringConnectionPeerCidrBlockSet",
    "DataAwsVpcPeeringConnectionPeerCidrBlockSetList",
    "DataAwsVpcPeeringConnectionPeerCidrBlockSetOutputReference",
    "DataAwsVpcPeeringConnectionTimeouts",
    "DataAwsVpcPeeringConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__961fdd8f90331188ecff5d232adcd43441b574742f26c64244041d99ea450a47(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cidr_block: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsVpcPeeringConnectionFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    peer_cidr_block: typing.Optional[builtins.str] = None,
    peer_owner_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
    peer_vpc_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DataAwsVpcPeeringConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b32d117ebc2cb0a51f12b183b67e8ae0560970bd0df39ab424cf31185ec9e4f0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsVpcPeeringConnectionFilter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d11be95f7b20baaa296f2b35febda97549e3d3cfc6ee0d68e951938e4f0ac68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__772820e03c483e0abe866ec8cc93533b4d2b738713fdc59d7dd2721c875f919d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f49a517c65138ef4e82df63ed48b0cf13cb9b9b312a6be1055eee573953b6ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3fd66b8527d5a9b502df94af55d1e494f642ba6c495e5be2fbb787af6aa7885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26d219e9c0122d4cbd13c38c5e37319ccc86dcd39d38accfdb562f4a5139183(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5232786f3649aa6112300aa67b789d3cb876c6863f82c94b434055a7129b6a50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b031ca2c4113893a9be66ccb210d7aac8138429ec0f01b44ba32cb88b5fb312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b187d30aeea5e9bba270c344c18437e1aa7b4b2c813181caf881770575fd0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ecc967d10113cda8bf5cd57e3d9bb75d6e58b932a59128c174b19ccea0f9e69(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa8fad4d872b27ec045ebc929eabee6781c0817bb829009b75179f645817add7(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde0c2232bcef3700af0db9880e0087cefbd03adf20e025425e0444cb81fccae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14e4c20c10693c65ac1e450850246b7b78f95cb5650723701ee370b9de78373a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070b829cd85fd9928b99d4e6a605087e6bfb07a404e88debc0e6cc78afde74ca(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd5b4f42705fe7a6b41205393d8c1944f699c5515e5ed6c6f55da07b658dc02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4902ce0f375e29ec388c27b32aef6bcb3fd832c8bf78b2f295d450b2fe36f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b500509db177630f079b9406216c723e1003f1aed6ee3a59bbbf7803cd83b91(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8582188076a6ce8fba37542b408d5b52d9730df2d00a19539f8d47a5762cdcf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afbc62513936a7e650b3d5b0408d005eb92254b3cba9ef25a48dde9ae3cda8f1(
    value: typing.Optional[DataAwsVpcPeeringConnectionCidrBlockSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11c456d8a0445ae5bbbcd4182f0f64e368a347f8f1b1cb934b17d6a7f432573(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cidr_block: typing.Optional[builtins.str] = None,
    filter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataAwsVpcPeeringConnectionFilter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    owner_id: typing.Optional[builtins.str] = None,
    peer_cidr_block: typing.Optional[builtins.str] = None,
    peer_owner_id: typing.Optional[builtins.str] = None,
    peer_region: typing.Optional[builtins.str] = None,
    peer_vpc_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DataAwsVpcPeeringConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e774ee3423578ebdfd6d87a8b213d3e547ac832aaaca9013b2e99ad4a78d0684(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86765f71fafb5c96380627fbf30826efd59dcdc9d538a72a85cb7c4bfbd8b10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b01121e6c0e8f05c51967eb6f5a022e6f319074de65877a7e7f637b64207a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b3bd3b976ea14b763a6b5eaf75b0afb9dd3b3da708973dfd7c579bd57b210e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c316edbe0c1ebaf9c2bc3fdcf2f6a305e1500fb9743155f241de438236470d8b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7280453965c3651a7fcf96dffcb9db7ca57d7b74ff35fe10ec8d60ac9e58df7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095a7808fda0e52b9d2f393d0f23d2e8ed0a287e7a644e554c0c96f07d1c62b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataAwsVpcPeeringConnectionFilter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2796611b64480f63c0e8a15d9dddf36cefcccfd0754594e1394015bda5db4027(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__706b62410f013ed2eaacdaca5fe8b510ae2aa42a21379ed14a2efffd57085859(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35762abd04c094a6fb3b9fed380bdec72e8e4d4c3441363e5bba70ddd25a6dfe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659bf80f1972dd31462d27aa27998c0cc0123f930376c82c6e991df111281405(
    value: typing.Optional[typing.Union[DataAwsVpcPeeringConnectionFilter, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d43bd2f1e9424c2762f6be90e81c2b0eb0298f18b2cfb2dfb2dae00a2282f76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff927905e2191d3a03d3bf79495fc5025168453e0806c489bc788696975d752a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fdcf456a63f213dee4b79607d7bd1603f80ab4cf8308292e4f956354f2aa595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae7c78e355b815a03b3c2a82ca03831cb4b512da6f90ad4e58fba03a1906937(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b9e5f5e66fa6a2dde961c128780d8cdcc6db1790e7b8bec61295afb27d031b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4929ef28bd659a18e9861269ea409183087dc0ebcd67e88ab5cdaaf4055d3d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f534450f6e5fd55a7145c5e20196cec1fd217c6e97e40aa6294c1e09e8fca0b9(
    value: typing.Optional[DataAwsVpcPeeringConnectionPeerCidrBlockSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c5cf8e695b5910f7f271c1c81a33703e25021d1c2172723f609cc61627788d(
    *,
    read: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78963b66f2aa600e93e15ab4947486830aa5cecec8f172de2c6e8d9dee8d2e4c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c455f06ddf975d2517f70e4d5d1e0433c5c82169ca11f4cfd0832804ef7fae9b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8d4ee0e8c999675b1cd6ccaa97922910250b58bd66b262817de23a2166212c(
    value: typing.Optional[typing.Union[DataAwsVpcPeeringConnectionTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
