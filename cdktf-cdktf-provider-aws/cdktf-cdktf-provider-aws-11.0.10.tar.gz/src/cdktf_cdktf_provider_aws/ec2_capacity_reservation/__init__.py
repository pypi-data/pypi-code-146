'''
# `aws_ec2_capacity_reservation`

Refer to the Terraform Registory for docs: [`aws_ec2_capacity_reservation`](https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation).
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


class Ec2CapacityReservation(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.ec2CapacityReservation.Ec2CapacityReservation",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation aws_ec2_capacity_reservation}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        availability_zone: builtins.str,
        instance_count: jsii.Number,
        instance_platform: builtins.str,
        instance_type: builtins.str,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_date: typing.Optional[builtins.str] = None,
        end_date_type: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_match_criteria: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        placement_group_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenancy: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation aws_ec2_capacity_reservation} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#availability_zone Ec2CapacityReservation#availability_zone}.
        :param instance_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_count Ec2CapacityReservation#instance_count}.
        :param instance_platform: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_platform Ec2CapacityReservation#instance_platform}.
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_type Ec2CapacityReservation#instance_type}.
        :param ebs_optimized: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#ebs_optimized Ec2CapacityReservation#ebs_optimized}.
        :param end_date: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#end_date Ec2CapacityReservation#end_date}.
        :param end_date_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#end_date_type Ec2CapacityReservation#end_date_type}.
        :param ephemeral_storage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#ephemeral_storage Ec2CapacityReservation#ephemeral_storage}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#id Ec2CapacityReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_match_criteria: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_match_criteria Ec2CapacityReservation#instance_match_criteria}.
        :param outpost_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#outpost_arn Ec2CapacityReservation#outpost_arn}.
        :param placement_group_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#placement_group_arn Ec2CapacityReservation#placement_group_arn}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tags Ec2CapacityReservation#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tags_all Ec2CapacityReservation#tags_all}.
        :param tenancy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tenancy Ec2CapacityReservation#tenancy}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c579005cbf27264fd48aafbd8ff3566c13f79083ea8f22be57b9f039f907f7d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = Ec2CapacityReservationConfig(
            availability_zone=availability_zone,
            instance_count=instance_count,
            instance_platform=instance_platform,
            instance_type=instance_type,
            ebs_optimized=ebs_optimized,
            end_date=end_date,
            end_date_type=end_date_type,
            ephemeral_storage=ephemeral_storage,
            id=id,
            instance_match_criteria=instance_match_criteria,
            outpost_arn=outpost_arn,
            placement_group_arn=placement_group_arn,
            tags=tags,
            tags_all=tags_all,
            tenancy=tenancy,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetEbsOptimized")
    def reset_ebs_optimized(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsOptimized", []))

    @jsii.member(jsii_name="resetEndDate")
    def reset_end_date(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDate", []))

    @jsii.member(jsii_name="resetEndDateType")
    def reset_end_date_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndDateType", []))

    @jsii.member(jsii_name="resetEphemeralStorage")
    def reset_ephemeral_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEphemeralStorage", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInstanceMatchCriteria")
    def reset_instance_match_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceMatchCriteria", []))

    @jsii.member(jsii_name="resetOutpostArn")
    def reset_outpost_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutpostArn", []))

    @jsii.member(jsii_name="resetPlacementGroupArn")
    def reset_placement_group_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlacementGroupArn", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTenancy")
    def reset_tenancy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTenancy", []))

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
    @jsii.member(jsii_name="availabilityZoneInput")
    def availability_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsOptimizedInput")
    def ebs_optimized_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ebsOptimizedInput"))

    @builtins.property
    @jsii.member(jsii_name="endDateInput")
    def end_date_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateInput"))

    @builtins.property
    @jsii.member(jsii_name="endDateTypeInput")
    def end_date_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageInput")
    def ephemeral_storage_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ephemeralStorageInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceMatchCriteriaInput")
    def instance_match_criteria_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceMatchCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="instancePlatformInput")
    def instance_platform_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instancePlatformInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypeInput")
    def instance_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="outpostArnInput")
    def outpost_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outpostArnInput"))

    @builtins.property
    @jsii.member(jsii_name="placementGroupArnInput")
    def placement_group_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "placementGroupArnInput"))

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
    @jsii.member(jsii_name="tenancyInput")
    def tenancy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenancyInput"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a638c32abed963c8f02601e83aa2312623c9cb76247409f345223c105b95afaf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="ebsOptimized")
    def ebs_optimized(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ebsOptimized"))

    @ebs_optimized.setter
    def ebs_optimized(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86b221c979e5c11b349f7dbe9869235fe91aa6e8492cb89a00d69f918d67bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsOptimized", value)

    @builtins.property
    @jsii.member(jsii_name="endDate")
    def end_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDate"))

    @end_date.setter
    def end_date(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__070b94e13cacc1814e73a0f90bd138cd5c67ca7748c920da050a13d24409f58e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDate", value)

    @builtins.property
    @jsii.member(jsii_name="endDateType")
    def end_date_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDateType"))

    @end_date_type.setter
    def end_date_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23695fa3afdb96c2605ac9626f6bfa62f66b3fb6b2a791215bc6b9931b48bd5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDateType", value)

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorage")
    def ephemeral_storage(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ephemeralStorage"))

    @ephemeral_storage.setter
    def ephemeral_storage(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa5d8ed4bab8b5a53c514660f1c4826fb2f9e579b9debca08a36972d19dca6f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ephemeralStorage", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908e45ef081d587ea502b507676bbd79a1b26c60cb9def53c42740baf1e956b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0988b690d96f7d850adb6d5e387962006dbaa45d96010c184e403169eb0a5a2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value)

    @builtins.property
    @jsii.member(jsii_name="instanceMatchCriteria")
    def instance_match_criteria(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceMatchCriteria"))

    @instance_match_criteria.setter
    def instance_match_criteria(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be17006c853b583791d64de73952eb1ea7f71c462e5827d95b15618318973813)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceMatchCriteria", value)

    @builtins.property
    @jsii.member(jsii_name="instancePlatform")
    def instance_platform(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instancePlatform"))

    @instance_platform.setter
    def instance_platform(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35a1c9c948eee2a59b2bf6f6cdc247f600286ed1fac3b101062456ba627a6264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instancePlatform", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f99da39b0bcdf9ea41fa59a8615d3ef302e7d1004216301696bc7875eaad4f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="outpostArn")
    def outpost_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outpostArn"))

    @outpost_arn.setter
    def outpost_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe34580c4392e821a0e3e9c698e0eab25b072af81b27286b8a3079fb6632bd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostArn", value)

    @builtins.property
    @jsii.member(jsii_name="placementGroupArn")
    def placement_group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "placementGroupArn"))

    @placement_group_arn.setter
    def placement_group_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552c4d8af2697414cd7f7fdf27c6f2d6c94c2f9ab031ab5f2b615d6c312fbb20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "placementGroupArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03489b24ca9f1f4e716a415bdc2aa7ee776f80f82aabeabe73f301cddd440509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5ee0922ae291cfdd1743255bc5ad5e5c165488dd7759d6a9bc4a8ee1661b20c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="tenancy")
    def tenancy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenancy"))

    @tenancy.setter
    def tenancy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc2f7e61dc0c72a05cff93e46e60236d03d7df19f1db346b585972e2fb016a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenancy", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.ec2CapacityReservation.Ec2CapacityReservationConfig",
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
        "instance_count": "instanceCount",
        "instance_platform": "instancePlatform",
        "instance_type": "instanceType",
        "ebs_optimized": "ebsOptimized",
        "end_date": "endDate",
        "end_date_type": "endDateType",
        "ephemeral_storage": "ephemeralStorage",
        "id": "id",
        "instance_match_criteria": "instanceMatchCriteria",
        "outpost_arn": "outpostArn",
        "placement_group_arn": "placementGroupArn",
        "tags": "tags",
        "tags_all": "tagsAll",
        "tenancy": "tenancy",
    },
)
class Ec2CapacityReservationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        instance_count: jsii.Number,
        instance_platform: builtins.str,
        instance_type: builtins.str,
        ebs_optimized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        end_date: typing.Optional[builtins.str] = None,
        end_date_type: typing.Optional[builtins.str] = None,
        ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        instance_match_criteria: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        placement_group_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tenancy: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param availability_zone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#availability_zone Ec2CapacityReservation#availability_zone}.
        :param instance_count: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_count Ec2CapacityReservation#instance_count}.
        :param instance_platform: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_platform Ec2CapacityReservation#instance_platform}.
        :param instance_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_type Ec2CapacityReservation#instance_type}.
        :param ebs_optimized: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#ebs_optimized Ec2CapacityReservation#ebs_optimized}.
        :param end_date: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#end_date Ec2CapacityReservation#end_date}.
        :param end_date_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#end_date_type Ec2CapacityReservation#end_date_type}.
        :param ephemeral_storage: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#ephemeral_storage Ec2CapacityReservation#ephemeral_storage}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#id Ec2CapacityReservation#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param instance_match_criteria: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_match_criteria Ec2CapacityReservation#instance_match_criteria}.
        :param outpost_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#outpost_arn Ec2CapacityReservation#outpost_arn}.
        :param placement_group_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#placement_group_arn Ec2CapacityReservation#placement_group_arn}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tags Ec2CapacityReservation#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tags_all Ec2CapacityReservation#tags_all}.
        :param tenancy: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tenancy Ec2CapacityReservation#tenancy}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83eae8610036a816e4d559260b641f5c5960cf0db966d797877954c5821abef)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
            check_type(argname="argument instance_platform", value=instance_platform, expected_type=type_hints["instance_platform"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument ebs_optimized", value=ebs_optimized, expected_type=type_hints["ebs_optimized"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument end_date_type", value=end_date_type, expected_type=type_hints["end_date_type"])
            check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument instance_match_criteria", value=instance_match_criteria, expected_type=type_hints["instance_match_criteria"])
            check_type(argname="argument outpost_arn", value=outpost_arn, expected_type=type_hints["outpost_arn"])
            check_type(argname="argument placement_group_arn", value=placement_group_arn, expected_type=type_hints["placement_group_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument tenancy", value=tenancy, expected_type=type_hints["tenancy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "availability_zone": availability_zone,
            "instance_count": instance_count,
            "instance_platform": instance_platform,
            "instance_type": instance_type,
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
        if ebs_optimized is not None:
            self._values["ebs_optimized"] = ebs_optimized
        if end_date is not None:
            self._values["end_date"] = end_date
        if end_date_type is not None:
            self._values["end_date_type"] = end_date_type
        if ephemeral_storage is not None:
            self._values["ephemeral_storage"] = ephemeral_storage
        if id is not None:
            self._values["id"] = id
        if instance_match_criteria is not None:
            self._values["instance_match_criteria"] = instance_match_criteria
        if outpost_arn is not None:
            self._values["outpost_arn"] = outpost_arn
        if placement_group_arn is not None:
            self._values["placement_group_arn"] = placement_group_arn
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if tenancy is not None:
            self._values["tenancy"] = tenancy

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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#availability_zone Ec2CapacityReservation#availability_zone}.'''
        result = self._values.get("availability_zone")
        assert result is not None, "Required property 'availability_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_count Ec2CapacityReservation#instance_count}.'''
        result = self._values.get("instance_count")
        assert result is not None, "Required property 'instance_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def instance_platform(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_platform Ec2CapacityReservation#instance_platform}.'''
        result = self._values.get("instance_platform")
        assert result is not None, "Required property 'instance_platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_type Ec2CapacityReservation#instance_type}.'''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ebs_optimized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#ebs_optimized Ec2CapacityReservation#ebs_optimized}.'''
        result = self._values.get("ebs_optimized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#end_date Ec2CapacityReservation#end_date}.'''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_date_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#end_date_type Ec2CapacityReservation#end_date_type}.'''
        result = self._values.get("end_date_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ephemeral_storage(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#ephemeral_storage Ec2CapacityReservation#ephemeral_storage}.'''
        result = self._values.get("ephemeral_storage")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#id Ec2CapacityReservation#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_match_criteria(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#instance_match_criteria Ec2CapacityReservation#instance_match_criteria}.'''
        result = self._values.get("instance_match_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outpost_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#outpost_arn Ec2CapacityReservation#outpost_arn}.'''
        result = self._values.get("outpost_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def placement_group_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#placement_group_arn Ec2CapacityReservation#placement_group_arn}.'''
        result = self._values.get("placement_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tags Ec2CapacityReservation#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tags_all Ec2CapacityReservation#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tenancy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/ec2_capacity_reservation#tenancy Ec2CapacityReservation#tenancy}.'''
        result = self._values.get("tenancy")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2CapacityReservationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ec2CapacityReservation",
    "Ec2CapacityReservationConfig",
]

publication.publish()

def _typecheckingstub__2c579005cbf27264fd48aafbd8ff3566c13f79083ea8f22be57b9f039f907f7d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    availability_zone: builtins.str,
    instance_count: jsii.Number,
    instance_platform: builtins.str,
    instance_type: builtins.str,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_date: typing.Optional[builtins.str] = None,
    end_date_type: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_match_criteria: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    placement_group_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenancy: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a638c32abed963c8f02601e83aa2312623c9cb76247409f345223c105b95afaf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86b221c979e5c11b349f7dbe9869235fe91aa6e8492cb89a00d69f918d67bfe(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__070b94e13cacc1814e73a0f90bd138cd5c67ca7748c920da050a13d24409f58e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23695fa3afdb96c2605ac9626f6bfa62f66b3fb6b2a791215bc6b9931b48bd5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa5d8ed4bab8b5a53c514660f1c4826fb2f9e579b9debca08a36972d19dca6f3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908e45ef081d587ea502b507676bbd79a1b26c60cb9def53c42740baf1e956b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0988b690d96f7d850adb6d5e387962006dbaa45d96010c184e403169eb0a5a2f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be17006c853b583791d64de73952eb1ea7f71c462e5827d95b15618318973813(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35a1c9c948eee2a59b2bf6f6cdc247f600286ed1fac3b101062456ba627a6264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f99da39b0bcdf9ea41fa59a8615d3ef302e7d1004216301696bc7875eaad4f18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe34580c4392e821a0e3e9c698e0eab25b072af81b27286b8a3079fb6632bd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552c4d8af2697414cd7f7fdf27c6f2d6c94c2f9ab031ab5f2b615d6c312fbb20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03489b24ca9f1f4e716a415bdc2aa7ee776f80f82aabeabe73f301cddd440509(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ee0922ae291cfdd1743255bc5ad5e5c165488dd7759d6a9bc4a8ee1661b20c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc2f7e61dc0c72a05cff93e46e60236d03d7df19f1db346b585972e2fb016a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83eae8610036a816e4d559260b641f5c5960cf0db966d797877954c5821abef(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    availability_zone: builtins.str,
    instance_count: jsii.Number,
    instance_platform: builtins.str,
    instance_type: builtins.str,
    ebs_optimized: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    end_date: typing.Optional[builtins.str] = None,
    end_date_type: typing.Optional[builtins.str] = None,
    ephemeral_storage: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    instance_match_criteria: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    placement_group_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tenancy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
