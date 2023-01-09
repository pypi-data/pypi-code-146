'''
# shady-island

[![Apache 2.0](https://img.shields.io/github/license/libreworks/shady-island)](https://github.com/libreworks/shady-island/blob/main/LICENSE)
[![npm](https://img.shields.io/npm/v/shady-island)](https://www.npmjs.com/package/shady-island)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/libreworks/shady-island/release/main?label=release)](https://github.com/libreworks/shady-island/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/libreworks/shady-island?sort=semver)](https://github.com/libreworks/shady-island/releases)
[![codecov](https://codecov.io/gh/libreworks/shady-island/branch/main/graph/badge.svg?token=OHTRGNTSPO)](https://codecov.io/gh/libreworks/shady-island)

Utilities and constructs for the AWS CDK.

## Features

* Create IPv6 CIDRs and routes for subnets in a VPC with the `CidrContext` construct.
* Set the `AssignIpv6AddressOnCreation` property of subnets in a VPC with the `AssignOnLaunch` construct.
* Properly encrypt a CloudWatch Log group with a KMS key and provision IAM permissions with the `EncryptedLogGroup` construct.
* Represent a deployment tier with the `Tier` class.
* Create a subclass of the `Workload` construct to contain your `Stack`s, and optionally load context values from a JSON file you specify.

## Documentation

* [TypeScript API Reference](https://libreworks.github.io/shady-island/api/API.html)

## The Name

It's a pun. In English, the pronunciation of the acronym *CDK* sounds a bit like the phrase *seedy cay*. A seedy cay might also be called a *shady island*.
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_efs as _aws_cdk_aws_efs_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="shady-island.AssignOnLaunchProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc", "vpc_subnets": "vpcSubnets"},
)
class AssignOnLaunchProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for creating a new {@link AssignOnLaunch}.

        :param vpc: The VPC whose subnets will be configured.
        :param vpc_subnets: Which subnets to assign IPv6 addresses upon ENI creation.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6464fd9d48d82d0db14a3cccbdb92cb250ed4fe6d6bd38b8e06d86417f53f2)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC whose subnets will be configured.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Which subnets to assign IPv6 addresses upon ENI creation.'''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssignOnLaunchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.CidrContextProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "address_pool": "addressPool",
        "assign_address_on_launch": "assignAddressOnLaunch",
        "cidr_block": "cidrBlock",
        "cidr_count": "cidrCount",
    },
)
class CidrContextProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        address_pool: typing.Optional[builtins.str] = None,
        assign_address_on_launch: typing.Optional[builtins.bool] = None,
        cidr_block: typing.Optional[builtins.str] = None,
        cidr_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for creating a new {@link CidrContext}.

        :param vpc: The VPC whose subnets will be configured.
        :param address_pool: The ID of a BYOIP IPv6 address pool from which to allocate the CIDR block. If this parameter is not specified or is undefined, the CIDR block will be provided by AWS.
        :param assign_address_on_launch: Whether this VPC should auto-assign an IPv6 address to launched ENIs. True by default.
        :param cidr_block: An IPv6 CIDR block from the IPv6 address pool to use for this VPC. The {@link EnableIpv6Props#addressPool} attribute is required if this parameter is specified.
        :param cidr_count: Split the CIDRs into this many groups (by default one for each subnet).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050e47d5b52c553cfe8b87e6673a27b8787fd0db2253c4e7b62521814ed5ae1d)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument address_pool", value=address_pool, expected_type=type_hints["address_pool"])
            check_type(argname="argument assign_address_on_launch", value=assign_address_on_launch, expected_type=type_hints["assign_address_on_launch"])
            check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
            check_type(argname="argument cidr_count", value=cidr_count, expected_type=type_hints["cidr_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if address_pool is not None:
            self._values["address_pool"] = address_pool
        if assign_address_on_launch is not None:
            self._values["assign_address_on_launch"] = assign_address_on_launch
        if cidr_block is not None:
            self._values["cidr_block"] = cidr_block
        if cidr_count is not None:
            self._values["cidr_count"] = cidr_count

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC whose subnets will be configured.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def address_pool(self) -> typing.Optional[builtins.str]:
        '''The ID of a BYOIP IPv6 address pool from which to allocate the CIDR block.

        If this parameter is not specified or is undefined, the CIDR block will be
        provided by AWS.
        '''
        result = self._values.get("address_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assign_address_on_launch(self) -> typing.Optional[builtins.bool]:
        '''Whether this VPC should auto-assign an IPv6 address to launched ENIs.

        True by default.
        '''
        result = self._values.get("assign_address_on_launch")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def cidr_block(self) -> typing.Optional[builtins.str]:
        '''An IPv6 CIDR block from the IPv6 address pool to use for this VPC.

        The {@link EnableIpv6Props#addressPool} attribute is required if this
        parameter is specified.
        '''
        result = self._values.get("cidr_block")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cidr_count(self) -> typing.Optional[jsii.Number]:
        '''Split the CIDRs into this many groups (by default one for each subnet).'''
        result = self._values.get("cidr_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CidrContextProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.EncryptedFileSystemProps",
    jsii_struct_bases=[_aws_cdk_aws_efs_ceddda9d.FileSystemProps],
    name_mapping={
        "vpc": "vpc",
        "enable_automatic_backups": "enableAutomaticBackups",
        "encrypted": "encrypted",
        "file_system_name": "fileSystemName",
        "kms_key": "kmsKey",
        "lifecycle_policy": "lifecyclePolicy",
        "out_of_infrequent_access_policy": "outOfInfrequentAccessPolicy",
        "performance_mode": "performanceMode",
        "provisioned_throughput_per_second": "provisionedThroughputPerSecond",
        "removal_policy": "removalPolicy",
        "security_group": "securityGroup",
        "throughput_mode": "throughputMode",
        "vpc_subnets": "vpcSubnets",
    },
)
class EncryptedFileSystemProps(_aws_cdk_aws_efs_ceddda9d.FileSystemProps):
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        enable_automatic_backups: typing.Optional[builtins.bool] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        file_system_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        lifecycle_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.LifecyclePolicy] = None,
        out_of_infrequent_access_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.OutOfInfrequentAccessPolicy] = None,
        performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
        provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Constructor parameters for EncryptedFileSystem.

        The ``encrypted`` argument is ignored.

        :param vpc: VPC to launch the file system in.
        :param enable_automatic_backups: Whether to enable automatic backups for the file system. Default: false
        :param encrypted: Defines if the data at rest in the file system is encrypted or not. Default: - If your application has the '
        :param file_system_name: The file system's name. Default: - CDK generated name
        :param kms_key: The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        :param lifecycle_policy: A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - None. EFS will not transition files to the IA storage class.
        :param out_of_infrequent_access_policy: A policy used by EFS lifecycle management to transition files from Infrequent Access (IA) storage class to primary storage class. Default: - None. EFS will not transition files from IA storage to primary storage.
        :param performance_mode: The performance mode that the file system will operate under. An Amazon EFS file system's performance mode can't be changed after the file system has been created. Updating this property will replace the file system. Default: PerformanceMode.GENERAL_PURPOSE
        :param provisioned_throughput_per_second: Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic
        :param throughput_mode: Enum to mention the throughput mode of the file system. Default: ThroughputMode.BURSTING
        :param vpc_subnets: Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd1576cc635c21f66d4c77cc0746612de310b047b380081961173028162c533)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument enable_automatic_backups", value=enable_automatic_backups, expected_type=type_hints["enable_automatic_backups"])
            check_type(argname="argument encrypted", value=encrypted, expected_type=type_hints["encrypted"])
            check_type(argname="argument file_system_name", value=file_system_name, expected_type=type_hints["file_system_name"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument lifecycle_policy", value=lifecycle_policy, expected_type=type_hints["lifecycle_policy"])
            check_type(argname="argument out_of_infrequent_access_policy", value=out_of_infrequent_access_policy, expected_type=type_hints["out_of_infrequent_access_policy"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument provisioned_throughput_per_second", value=provisioned_throughput_per_second, expected_type=type_hints["provisioned_throughput_per_second"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument throughput_mode", value=throughput_mode, expected_type=type_hints["throughput_mode"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if enable_automatic_backups is not None:
            self._values["enable_automatic_backups"] = enable_automatic_backups
        if encrypted is not None:
            self._values["encrypted"] = encrypted
        if file_system_name is not None:
            self._values["file_system_name"] = file_system_name
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if lifecycle_policy is not None:
            self._values["lifecycle_policy"] = lifecycle_policy
        if out_of_infrequent_access_policy is not None:
            self._values["out_of_infrequent_access_policy"] = out_of_infrequent_access_policy
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if provisioned_throughput_per_second is not None:
            self._values["provisioned_throughput_per_second"] = provisioned_throughput_per_second
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_group is not None:
            self._values["security_group"] = security_group
        if throughput_mode is not None:
            self._values["throughput_mode"] = throughput_mode
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC to launch the file system in.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def enable_automatic_backups(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable automatic backups for the file system.

        :default: false
        '''
        result = self._values.get("enable_automatic_backups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def encrypted(self) -> typing.Optional[builtins.bool]:
        '''Defines if the data at rest in the file system is encrypted or not.

        :default: - If your application has the '

        :aws-cdk: /aws-efs:defaultEncryptionAtRest' feature flag set, the default is true, otherwise, the default is false.
        :link: https://docs.aws.amazon.com/cdk/latest/guide/featureflags.html
        '''
        result = self._values.get("encrypted")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def file_system_name(self) -> typing.Optional[builtins.str]:
        '''The file system's name.

        :default: - CDK generated name
        '''
        result = self._values.get("file_system_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The KMS key used for encryption.

        This is required to encrypt the data at rest if @encrypted is set to true.

        :default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def lifecycle_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.LifecyclePolicy]:
        '''A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class.

        :default: - None. EFS will not transition files to the IA storage class.
        '''
        result = self._values.get("lifecycle_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.LifecyclePolicy], result)

    @builtins.property
    def out_of_infrequent_access_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.OutOfInfrequentAccessPolicy]:
        '''A policy used by EFS lifecycle management to transition files from Infrequent Access (IA) storage class to primary storage class.

        :default: - None. EFS will not transition files from IA storage to primary storage.
        '''
        result = self._values.get("out_of_infrequent_access_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.OutOfInfrequentAccessPolicy], result)

    @builtins.property
    def performance_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode]:
        '''The performance mode that the file system will operate under.

        An Amazon EFS file system's performance mode can't be changed after the file system has been created.
        Updating this property will replace the file system.

        :default: PerformanceMode.GENERAL_PURPOSE
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode], result)

    @builtins.property
    def provisioned_throughput_per_second(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''Provisioned throughput for the file system.

        This is a required property if the throughput mode is set to PROVISIONED.
        Must be at least 1MiB/s.

        :default: - none, errors out
        '''
        result = self._values.get("provisioned_throughput_per_second")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy to apply to the file system.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security Group to assign to this file system.

        :default: - creates new security group which allows all outbound traffic
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def throughput_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode]:
        '''Enum to mention the throughput mode of the file system.

        :default: ThroughputMode.BURSTING
        '''
        result = self._values.get("throughput_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Which subnets to place the mount target in the VPC.

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptedFileSystemProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="shady-island.EncryptedLogGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "encryption_key": "encryptionKey",
        "removal_policy": "removalPolicy",
        "retention": "retention",
    },
)
class EncryptedLogGroupProps:
    def __init__(
        self,
        *,
        log_group_name: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''Constructor properties for EncryptedLogGroup.

        :param log_group_name: Name of the log group. We need a log group name ahead of time because otherwise the key policy would create a cyclical dependency.
        :param encryption_key: The KMS Key to encrypt the log group with. Default: A new KMS key will be created
        :param removal_policy: Whether the key and group should be retained when they are removed from the Stack. Default: RemovalPolicy.RETAIN
        :param retention: How long, in days, the log contents will be retained. Default: RetentionDays.TWO_YEARS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336d3d15e4b6b1d5a3f1d25302a1b6aa54f3525152e85c4efc9022074bbc84ef)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument retention", value=retention, expected_type=type_hints["retention"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_group_name": log_group_name,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if retention is not None:
            self._values["retention"] = retention

    @builtins.property
    def log_group_name(self) -> builtins.str:
        '''Name of the log group.

        We need a log group name ahead of time because otherwise the key policy
        would create a cyclical dependency.
        '''
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The KMS Key to encrypt the log group with.

        :default: A new KMS key will be created
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Whether the key and group should be retained when they are removed from the Stack.

        :default: RemovalPolicy.RETAIN
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def retention(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''How long, in days, the log contents will be retained.

        :default: RetentionDays.TWO_YEARS
        '''
        result = self._values.get("retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncryptedLogGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="shady-island.IAssignOnLaunch")
class IAssignOnLaunch(typing_extensions.Protocol):
    '''Interface for the AssignOnLaunch class.'''

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The IPv6-enabled VPC.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcPlacement")
    def vpc_placement(self) -> _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets:
        '''The chosen subnets for address assignment on ENI launch.'''
        ...


class _IAssignOnLaunchProxy:
    '''Interface for the AssignOnLaunch class.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.IAssignOnLaunch"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The IPv6-enabled VPC.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="vpcPlacement")
    def vpc_placement(self) -> _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets:
        '''The chosen subnets for address assignment on ENI launch.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, jsii.get(self, "vpcPlacement"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAssignOnLaunch).__jsii_proxy_class__ = lambda : _IAssignOnLaunchProxy


@jsii.interface(jsii_type="shady-island.ICidrContext")
class ICidrContext(typing_extensions.Protocol):
    '''Interface for the CidrContext class.'''

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The IPv6-enabled VPC.'''
        ...


class _ICidrContextProxy:
    '''Interface for the CidrContext class.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.ICidrContext"

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The IPv6-enabled VPC.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICidrContext).__jsii_proxy_class__ = lambda : _ICidrContextProxy


@jsii.interface(jsii_type="shady-island.IEncryptedFileSystem")
class IEncryptedFileSystem(_constructs_77d1e7e8.IConstruct, typing_extensions.Protocol):
    '''Interface for EncryptedFileSystem.'''

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''The EFS file system.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The KMS encryption key.'''
        ...


class _IEncryptedFileSystemProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''Interface for EncryptedFileSystem.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.IEncryptedFileSystem"

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''The EFS file system.'''
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IFileSystem, jsii.get(self, "fileSystem"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The KMS encryption key.'''
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "key"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEncryptedFileSystem).__jsii_proxy_class__ = lambda : _IEncryptedFileSystemProxy


@jsii.interface(jsii_type="shady-island.IEncryptedLogGroup")
class IEncryptedLogGroup(typing_extensions.Protocol):
    '''A log group encrypted by a KMS customer managed key.'''

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The KMS encryption key.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group.'''
        ...


class _IEncryptedLogGroupProxy:
    '''A log group encrypted by a KMS customer managed key.'''

    __jsii_type__: typing.ClassVar[str] = "shady-island.IEncryptedLogGroup"

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The KMS encryption key.'''
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group.'''
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, jsii.get(self, "logGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEncryptedLogGroup).__jsii_proxy_class__ = lambda : _IEncryptedLogGroupProxy


@jsii.data_type(
    jsii_type="shady-island.PrioritizedLines",
    jsii_struct_bases=[],
    name_mapping={"lines": "lines", "priority": "priority"},
)
class PrioritizedLines:
    def __init__(
        self,
        *,
        lines: typing.Sequence[builtins.str],
        priority: jsii.Number,
    ) -> None:
        '''A container for lines of a User Data script, sortable by ``priority``.

        :param lines: The command lines.
        :param priority: The priority for this set of commands.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6e48c7b1cd24344a1cdbb27f3f7aea01ec3a2ce2f1bf2ce870bcc01f662aa91)
            check_type(argname="argument lines", value=lines, expected_type=type_hints["lines"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lines": lines,
            "priority": priority,
        }

    @builtins.property
    def lines(self) -> typing.List[builtins.str]:
        '''The command lines.'''
        result = self._values.get("lines")
        assert result is not None, "Required property 'lines' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''The priority for this set of commands.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrioritizedLines(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Tier(metaclass=jsii.JSIIMeta, jsii_type="shady-island.Tier"):
    '''A deployment environment with a specific purpose and audience.

    You can create any Tier you like, but we include those explained by DTAP.

    :see: https://en.wikipedia.org/wiki/Development,_testing,_acceptance_and_production
    '''

    def __init__(self, id: builtins.str, label: builtins.str) -> None:
        '''Creates a new Tier.

        :param id: - The machine-readable identifier for this tier (e.g. prod).
        :param label: - The human-readable label for this tier (e.g. Production).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530a177d1cc816f59517c3e52dceeb99d4c7774e513d4d6bf96e414b10eee80f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
        jsii.create(self.__class__, self, [id, label])

    @jsii.member(jsii_name="parse")
    @builtins.classmethod
    def parse(cls, value: builtins.str) -> "Tier":
        '''Return the deployment tier that corresponds to the provided value.

        Production: "live", "prod", or "production".
        Acceptance: "uat", "stage", "staging", or "acceptance".
        Testing: "qc", "qa", "test", or "testing".
        Development: anything else.

        :param value: - The value to parse, case-insensitive.

        :return: The matching deployment tier, or else ``DEVELOPMENT``.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2f20e1b838706908cb4dc457364ab4d6a3ba246f70b4d648ff5df5ead1e52df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Tier", jsii.sinvoke(cls, "parse", [value]))

    @jsii.member(jsii_name="applyTags")
    def apply_tags(self, construct: _constructs_77d1e7e8.IConstruct) -> None:
        '''Adds the label of this tier as a tag to the provided construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c184966e811a15ee5af7f9b885e27fa53713f5978c027ccfe09f4878a486801)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(None, jsii.invoke(self, "applyTags", [construct]))

    @jsii.member(jsii_name="matches")
    def matches(self, other: "Tier") -> builtins.bool:
        '''Compares this tier to the provided value and tests for equality.

        :param other: - The value to compare.

        :return: Whether the provided value is equal to this tier.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc74e7f1b826ca0249b2f9a045466e09289c315ccc1cc9056778d302475eac52)
            check_type(argname="argument other", value=other, expected_type=type_hints["other"])
        return typing.cast(builtins.bool, jsii.invoke(self, "matches", [other]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ACCEPTANCE")
    def ACCEPTANCE(cls) -> "Tier":
        '''A tier that represents an acceptance environment.'''
        return typing.cast("Tier", jsii.sget(cls, "ACCEPTANCE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEVELOPMENT")
    def DEVELOPMENT(cls) -> "Tier":
        '''A tier that represents a development environment.'''
        return typing.cast("Tier", jsii.sget(cls, "DEVELOPMENT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PRODUCTION")
    def PRODUCTION(cls) -> "Tier":
        '''A tier that represents a production environment.'''
        return typing.cast("Tier", jsii.sget(cls, "PRODUCTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TESTING")
    def TESTING(cls) -> "Tier":
        '''A tier that represents a testing environment.'''
        return typing.cast("Tier", jsii.sget(cls, "TESTING"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''The machine-readable identifier for this tier (e.g. prod).'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        '''The human-readable label for this tier (e.g. Production).'''
        return typing.cast(builtins.str, jsii.get(self, "label"))


class UserDataBuilder(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="shady-island.UserDataBuilder",
):
    '''A utility class to assist with composing instance User Data.

    This class allows multiple observers in code to add lines to the same end
    result UserData without clobbering each other. Just like ``conf.d`` directories
    with priority number prefixes, you can declare the proper execution order of
    your UserData commands without having to add them in that order.
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="forLinux")
    @builtins.classmethod
    def for_linux(
        cls,
        *,
        shebang: typing.Optional[builtins.str] = None,
    ) -> "UserDataBuilder":
        '''Returns a user data builder for GNU/Linux operating systems.

        :param shebang: Shebang for the UserData script. Default: "#!/bin/bash"

        :return: the new builder object
        '''
        options = _aws_cdk_aws_ec2_ceddda9d.LinuxUserDataOptions(shebang=shebang)

        return typing.cast("UserDataBuilder", jsii.sinvoke(cls, "forLinux", [options]))

    @jsii.member(jsii_name="forWindows")
    @builtins.classmethod
    def for_windows(cls) -> "UserDataBuilder":
        '''Returns a user data builder for Windows operating systems.

        :return: the new builder object
        '''
        return typing.cast("UserDataBuilder", jsii.sinvoke(cls, "forWindows", []))

    @jsii.member(jsii_name="addCommands")
    def add_commands(self, *commands: builtins.str) -> None:
        '''Add one or more commands to the user data with a priority of ``0``.

        :param commands: - The lines to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56dc72e2b8d9e69be937435e41fa771eb82b99df61762e67305a1aa7d1a25cd)
            check_type(argname="argument commands", value=commands, expected_type=typing.Tuple[type_hints["commands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addCommands", [*commands]))

    @jsii.member(jsii_name="buildUserData")
    @abc.abstractmethod
    def build_user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''Produces the User Data script with all lines sorted in priority order.

        :return: The assembled User Data
        '''
        ...

    @jsii.member(jsii_name="insertCommands")
    def insert_commands(self, priority: jsii.Number, *commands: builtins.str) -> None:
        '''Add one or more commands to the user data at a specific priority.

        :param priority: - The priority of these lines (lower executes earlier).
        :param commands: - The lines to add.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6114eade1a4b4469c7ffa50dbde1b95b36c5b299d356317bbe384e4caf526133)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument commands", value=commands, expected_type=typing.Tuple[type_hints["commands"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "insertCommands", [priority, *commands]))

    @builtins.property
    @jsii.member(jsii_name="lines")
    def _lines(self) -> typing.List[PrioritizedLines]:
        '''The groups of prioritized command line entries.'''
        return typing.cast(typing.List[PrioritizedLines], jsii.get(self, "lines"))


class _UserDataBuilderProxy(UserDataBuilder):
    @jsii.member(jsii_name="buildUserData")
    def build_user_data(self) -> _aws_cdk_aws_ec2_ceddda9d.UserData:
        '''Produces the User Data script with all lines sorted in priority order.

        :return: The assembled User Data
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.UserData, jsii.invoke(self, "buildUserData", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, UserDataBuilder).__jsii_proxy_class__ = lambda : _UserDataBuilderProxy


class Workload(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.Workload",
):
    '''A collection of Stacks in an Environment representing a deployment Tier.

    Consider deriving a subclass of ``Workload`` and creating your ``Stack`` objects
    within its constructor.

    The difference between this class and a ``Stage`` is that a ``Stage`` is meant to
    be deployed with CDK Pipelines. This class can be used with ``cdk deploy``.
    This class also provides context loading capabilities.

    It is an anti-pattern to provide a ``Workload`` instance as the parent scope to
    the ``aws-cdk-lib.Stack`` constructor. You should either use the
    ``createStack()`` method, create your own sub-class of ``Stack`` and provide a
    ``Workload`` instance as the parent scope, or use the ``import()`` method to
    essentially *import* a ``Stack`` and its constructs into a ``Workload`` without
    changing its scope.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        tier: Tier,
        base_domain_name: typing.Optional[builtins.str] = None,
        context_file: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new Workload.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param tier: The deployment tier.
        :param base_domain_name: The base domain name used to create the FQDN for public resources.
        :param context_file: The filesystem path to a JSON file that contains context values to load. Using this property allows you to load different context values within each instantiated ``Workload``, directly from a file you can check into source control.
        :param env: The AWS environment (account/region) where this stack will be deployed.
        :param workload_name: The machine identifier for this workload. This value will be used to create the ``publicDomainName`` property. By default, the ``stackName`` property used to create ``Stack`` constructs in the ``createStack`` method will begin with this Workload's ``workloadName`` and its ``tier`` separated by hyphens. Consider providing a constant ``workloadName`` value to the superclass constructor in your derived class. Default: - The id passed to the ``Workload`` constructor, but in lowercase
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc677f9592ce3b6c83e0b51756bcbfa8439cf4279d746c77e45e81d3ac83c74)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WorkloadProps(
            tier=tier,
            base_domain_name=base_domain_name,
            context_file=context_file,
            env=env,
            workload_name=workload_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="isWorkload")
    @builtins.classmethod
    def is_workload(cls, x: typing.Any) -> builtins.bool:
        '''Test whether the given construct is a Workload.

        :param x: - The value to test.

        :return: Whether the value is a Workload object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ebb0ba06e254e10fe2379e1883988108104f296135702e61231d2437cee11e)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isWorkload", [x]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: _constructs_77d1e7e8.IConstruct) -> "Workload":
        '''Return the Workload the construct is contained within, fails if there is no workload up the tree.

        :param construct: - The construct whose parent nodes will be searched.

        :return: The Workload containing the construct

        :throws: Error - if none of the construct's parents are a workload
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e27f5fc4333ac0563c57801a0b496252f1fe2f4b9a122724ccfbfec6d7998dbf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast("Workload", jsii.sinvoke(cls, "of", [construct]))

    @jsii.member(jsii_name="createStack")
    def create_stack(
        self,
        id: builtins.str,
        *,
        analytics_reporting: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        stack_name: typing.Optional[builtins.str] = None,
        synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_ceddda9d.Stack:
        '''Adds a stack to the Workload.

        This method will return a ``Stack`` with this Workload as its scope. By
        default, the ``stackName`` property provided to the ``Stack`` will be this
        Workload's ``workloadName``, its ``tier``, and the value of the ``id``
        parameter separated by hyphens, all in lowercase.

        :param id: - The Stack construct id (e.g. "Network").
        :param analytics_reporting: Include runtime versioning information in this Stack. Default: ``analyticsReporting`` setting of containing ``App``, or value of 'aws:cdk:version-reporting' context key
        :param description: A description of the stack. Default: - No description.
        :param env: The AWS environment (account/region) where this stack will be deployed. Set the ``region``/``account`` fields of ``env`` to either a concrete value to select the indicated environment (recommended for production stacks), or to the values of environment variables ``CDK_DEFAULT_REGION``/``CDK_DEFAULT_ACCOUNT`` to let the target environment depend on the AWS credentials/configuration that the CDK CLI is executed under (recommended for development stacks). If the ``Stack`` is instantiated inside a ``Stage``, any undefined ``region``/``account`` fields from ``env`` will default to the same field on the encompassing ``Stage``, if configured there. If either ``region`` or ``account`` are not set nor inherited from ``Stage``, the Stack will be considered "*environment-agnostic*"". Environment-agnostic stacks can be deployed to any environment but may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups such as ``ec2.Vpc.fromLookup`` and will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environment of the containing ``Stage`` if available, otherwise create the stack will be environment-agnostic.
        :param stack_name: Name to deploy the stack with. Default: - Derived from construct path.
        :param synthesizer: Synthesis method to use while deploying this stack. Default: - ``DefaultStackSynthesizer`` if the ``@aws-cdk/core:newStyleStackSynthesis`` feature flag is set, ``LegacyStackSynthesizer`` otherwise.
        :param tags: Stack tags that will be applied to all the taggable resources and the stack itself. Default: {}
        :param termination_protection: Whether to enable termination protection for this stack. Default: false

        Example::

            const exampleDev = new Workload(app, 'Example', {
              tier: Tier.DEVELOPMENT,
              env: { account: '123456789012', region: 'us-east-1' },
            });
            const networkStack = exampleDev.createStack('Network', {});
            assert.strictEqual(networkStack.stackName, 'example-dev-network').
            
            You can override the `env` and `stackName` properties in the `props`
            argument if desired.
            
            The stack will have a `DeploymentTier` tag added, set to the tier label.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9ba1202ef7d254e0e9e1f79faf21a7241261ea59fec1d6b565e8f9c5709830b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_ceddda9d.StackProps(
            analytics_reporting=analytics_reporting,
            description=description,
            env=env,
            stack_name=stack_name,
            synthesizer=synthesizer,
            tags=tags,
            termination_protection=termination_protection,
        )

        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.invoke(self, "createStack", [id, props]))

    @jsii.member(jsii_name="import")
    def import_(self, *stacks: _aws_cdk_ceddda9d.Stack) -> None:
        '''Forces a return value for ``Workload.of`` for one or more ``Stack`` objects.

        Normally, a construct must be within the scope of the ``Workload`` instance,
        such as a construct that is a descendant of a ``Stack`` returned from
        ``createStack()``.

        That means that any ``Stack`` instances you created in your CDK application
        *before* installing the ``shady-island`` library would not be able to be part
        of a ``Workload`` unless you changed the ``scope`` argument of the ``Stack``
        constructor from the ``App`` or ``Stage`` to the desired ``Workload`` instance.
        However, that's bad news for a ``Stack`` that has already been deployed to
        CloudFormation because the resource identifier of persistent child
        constructs (e.g. RDS databases, S3 buckets) would change.

        A successful call to this method will register the provided ``Stack`` objects
        and all their construct descendants as members of that ``Workload`` instance.
        Calling ``Workload.of()`` with any of the provided ``Stack`` objects or their
        descendant constructs will return that ``Workload`` instance.

        If any of the ``Stack`` objects provided to this method already belong to a
        different ``Workload`` object, or whose parent scope is not identical to the
        parent scope of this ``Workload`` (i.e. the ``Stage`` or the ``App``), an error
        will be thrown.

        :param stacks: - The ``Stack`` instances to import to this ``Workload``.

        :throws: {Error} if any of the stacks have a different parent scope
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2eedf91b5d4e25d97e311a1a26f03b3db1e8d5bba809f0a2bd20df11d9bdfb)
            check_type(argname="argument stacks", value=stacks, expected_type=typing.Tuple[type_hints["stacks"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "import", [*stacks]))

    @jsii.member(jsii_name="registerStack")
    def _register_stack(
        self,
        stack: _aws_cdk_ceddda9d.Stack,
    ) -> _aws_cdk_ceddda9d.Stack:
        '''Register the provided ``Stack`` as being part of this ``Workload``.

        :param stack: - The stack to register.

        :return: The provided Stack
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19f32a870d457362c1bd937f00bb736bfc4263b2f555fd93d34c4bf7dd53f7a7)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.invoke(self, "registerStack", [stack]))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[_aws_cdk_ceddda9d.Stack]:
        '''
        :return: The stacks created by invoking ``createStack``
        '''
        return typing.cast(typing.List[_aws_cdk_ceddda9d.Stack], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(self) -> Tier:
        '''The deployment tier.'''
        return typing.cast(Tier, jsii.get(self, "tier"))

    @builtins.property
    @jsii.member(jsii_name="workloadName")
    def workload_name(self) -> builtins.str:
        '''The prefix used in the default ``stackName`` provided to child Stacks.'''
        return typing.cast(builtins.str, jsii.get(self, "workloadName"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''The default account for all resources defined within this workload.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "account"))

    @builtins.property
    @jsii.member(jsii_name="publicDomainName")
    def public_domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name to use for resources that expose public endpoints.

        You can use ``Workload.of(this).publicDomainName`` as the ``zoneName`` of a
        Route 53 hosted zone.

        Any construct that creates public DNS resources (e.g. those of API Gateway,
        Application Load Balancing, CloudFront) can use this property to format
        a FQDN for itself by adding a subdomain.

        :default: - If ``baseDomainName`` was empty, this will be ``undefined``

        Example::

            const app = new App();
            const workload = new Workload(app, "Foobar", {
              tier: Tier.PRODUCTION,
              baseDomainName: 'example.com'
            });
            assert.strictEqual(workload.publicDomainName, 'prod.foobar.example.com');
            const stack = workload.createStack("DNS");
            const hostedZone = new HostedZone(stack, "HostedZone", {
              zoneName: `${workload.publicDomainName}`
            });
            const api = new RestApi(stack, "API", {
              restApiName: "foobar",
              domainName: { domainName: `api.${workload.publicDomainName}` },
            });
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicDomainName"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''The default region for all resources defined within this workload.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))


@jsii.data_type(
    jsii_type="shady-island.WorkloadProps",
    jsii_struct_bases=[],
    name_mapping={
        "tier": "tier",
        "base_domain_name": "baseDomainName",
        "context_file": "contextFile",
        "env": "env",
        "workload_name": "workloadName",
    },
)
class WorkloadProps:
    def __init__(
        self,
        *,
        tier: Tier,
        base_domain_name: typing.Optional[builtins.str] = None,
        context_file: typing.Optional[builtins.str] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        workload_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructor properties for a Workload.

        :param tier: The deployment tier.
        :param base_domain_name: The base domain name used to create the FQDN for public resources.
        :param context_file: The filesystem path to a JSON file that contains context values to load. Using this property allows you to load different context values within each instantiated ``Workload``, directly from a file you can check into source control.
        :param env: The AWS environment (account/region) where this stack will be deployed.
        :param workload_name: The machine identifier for this workload. This value will be used to create the ``publicDomainName`` property. By default, the ``stackName`` property used to create ``Stack`` constructs in the ``createStack`` method will begin with this Workload's ``workloadName`` and its ``tier`` separated by hyphens. Consider providing a constant ``workloadName`` value to the superclass constructor in your derived class. Default: - The id passed to the ``Workload`` constructor, but in lowercase
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d21735e564e0f2e2aaeb9fd18b82adda3268ccc0278f45c2386e1cb3a55271)
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument base_domain_name", value=base_domain_name, expected_type=type_hints["base_domain_name"])
            check_type(argname="argument context_file", value=context_file, expected_type=type_hints["context_file"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument workload_name", value=workload_name, expected_type=type_hints["workload_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "tier": tier,
        }
        if base_domain_name is not None:
            self._values["base_domain_name"] = base_domain_name
        if context_file is not None:
            self._values["context_file"] = context_file
        if env is not None:
            self._values["env"] = env
        if workload_name is not None:
            self._values["workload_name"] = workload_name

    @builtins.property
    def tier(self) -> Tier:
        '''The deployment tier.'''
        result = self._values.get("tier")
        assert result is not None, "Required property 'tier' is missing"
        return typing.cast(Tier, result)

    @builtins.property
    def base_domain_name(self) -> typing.Optional[builtins.str]:
        '''The base domain name used to create the FQDN for public resources.'''
        result = self._values.get("base_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_file(self) -> typing.Optional[builtins.str]:
        '''The filesystem path to a JSON file that contains context values to load.

        Using this property allows you to load different context values within each
        instantiated ``Workload``, directly from a file you can check into source
        control.
        '''
        result = self._values.get("context_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''The AWS environment (account/region) where this stack will be deployed.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def workload_name(self) -> typing.Optional[builtins.str]:
        '''The machine identifier for this workload.

        This value will be used to create the ``publicDomainName`` property.

        By default, the ``stackName`` property used to create ``Stack`` constructs in
        the ``createStack`` method will begin with this Workload's ``workloadName`` and
        its ``tier`` separated by hyphens.

        Consider providing a constant ``workloadName`` value to the superclass
        constructor in your derived class.

        :default: - The id passed to the ``Workload`` constructor, but in lowercase

        Example::

            class MyWorkload extends Workload {
              constructor(scope: Construct, id: string, props: WorkloadProps) {
                super(scope, id, { ...props, workloadName: 'my-workload' });
              }
            }
        '''
        result = self._values.get("workload_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkloadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAssignOnLaunch)
class AssignOnLaunch(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.AssignOnLaunch",
):
    '''Enables the "assignIpv6AddressOnCreation" attribute on selected subnets.

    :see: {@link https://github.com/aws/aws-cdk/issues/5927}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Creates a new BetterVpc.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param vpc: The VPC whose subnets will be configured.
        :param vpc_subnets: Which subnets to assign IPv6 addresses upon ENI creation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef34bf6f916957f913c4aa2b3459686556aaef0c4dde4b4cd1da18bd1bdf38e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = AssignOnLaunchProps(vpc=vpc, vpc_subnets=vpc_subnets)

        jsii.create(self.__class__, self, [scope, id, options])

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The IPv6-enabled VPC.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="vpcPlacement")
    def vpc_placement(self) -> _aws_cdk_aws_ec2_ceddda9d.SelectedSubnets:
        '''The chosen subnets for address assignment on ENI launch.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SelectedSubnets, jsii.get(self, "vpcPlacement"))


@jsii.implements(ICidrContext)
class CidrContext(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.CidrContext",
):
    '''Allocates IPv6 CIDRs and routes for subnets in a VPC.

    :see: {@link https://github.com/aws/aws-cdk/issues/5927}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        address_pool: typing.Optional[builtins.str] = None,
        assign_address_on_launch: typing.Optional[builtins.bool] = None,
        cidr_block: typing.Optional[builtins.str] = None,
        cidr_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Creates a new BetterVpc.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param vpc: The VPC whose subnets will be configured.
        :param address_pool: The ID of a BYOIP IPv6 address pool from which to allocate the CIDR block. If this parameter is not specified or is undefined, the CIDR block will be provided by AWS.
        :param assign_address_on_launch: Whether this VPC should auto-assign an IPv6 address to launched ENIs. True by default.
        :param cidr_block: An IPv6 CIDR block from the IPv6 address pool to use for this VPC. The {@link EnableIpv6Props#addressPool} attribute is required if this parameter is specified.
        :param cidr_count: Split the CIDRs into this many groups (by default one for each subnet).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b0de4a00dc5c9be3f27b4ab96a0dcd78e40528295ed76dce57eec996acc188c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = CidrContextProps(
            vpc=vpc,
            address_pool=address_pool,
            assign_address_on_launch=assign_address_on_launch,
            cidr_block=cidr_block,
            cidr_count=cidr_count,
        )

        jsii.create(self.__class__, self, [scope, id, options])

    @jsii.member(jsii_name="assignPrivateSubnetCidrs")
    def _assign_private_subnet_cidrs(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cidrs: typing.Sequence[builtins.str],
        cidr_block: _aws_cdk_ceddda9d.CfnResource,
    ) -> None:
        '''Override the template;

        set the IPv6 CIDR for private subnets.

        :param vpc: - The VPC of the subnets.
        :param cidrs: - The possible IPv6 CIDRs to assign.
        :param cidr_block: - The CfnVPCCidrBlock the subnets depend on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b002de4531052fe21d5d3510d0331c20a853e0a42c33e19aabc0f4c089723954)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
        return typing.cast(None, jsii.invoke(self, "assignPrivateSubnetCidrs", [vpc, cidrs, cidr_block]))

    @jsii.member(jsii_name="assignPublicSubnetCidrs")
    def _assign_public_subnet_cidrs(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cidrs: typing.Sequence[builtins.str],
        cidr_block: _aws_cdk_ceddda9d.CfnResource,
    ) -> None:
        '''Override the template;

        set the IPv6 CIDR for isolated subnets.

        :param vpc: - The VPC of the subnets.
        :param cidrs: - The possible IPv6 CIDRs to assign.
        :param cidr_block: - The CfnVPCCidrBlock the subnets depend on.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7693f240a70888012a03fe0b6a47ff72168fbb02ae5de987a68ac482cbe1a967)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            check_type(argname="argument cidr_block", value=cidr_block, expected_type=type_hints["cidr_block"])
        return typing.cast(None, jsii.invoke(self, "assignPublicSubnetCidrs", [vpc, cidrs, cidr_block]))

    @jsii.member(jsii_name="validateCidrCount")
    def _validate_cidr_count(
        self,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        cidr_count: typing.Optional[jsii.Number] = None,
    ) -> jsii.Number:
        '''Figure out the minimun required CIDR subnets and the number desired.

        :param vpc: - The VPC.
        :param cidr_count: - Optional. Divide the VPC CIDR into this many subsets.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__824a74b960abc01e0c39abfdf3e11416c999207fb7b170a7c45ff9e6f49b5189)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument cidr_count", value=cidr_count, expected_type=type_hints["cidr_count"])
        return typing.cast(jsii.Number, jsii.invoke(self, "validateCidrCount", [vpc, cidr_count]))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The IPv6-enabled VPC.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


@jsii.implements(IEncryptedFileSystem)
class EncryptedFileSystem(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.EncryptedFileSystem",
):
    '''An EncryptedFileSystem.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        enable_automatic_backups: typing.Optional[builtins.bool] = None,
        encrypted: typing.Optional[builtins.bool] = None,
        file_system_name: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        lifecycle_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.LifecyclePolicy] = None,
        out_of_infrequent_access_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.OutOfInfrequentAccessPolicy] = None,
        performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
        provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Creates a new EncryptedFileSystem.

        :param scope: - The Construct that contains this one.
        :param id: - The identifier of this construct.
        :param vpc: VPC to launch the file system in.
        :param enable_automatic_backups: Whether to enable automatic backups for the file system. Default: false
        :param encrypted: Defines if the data at rest in the file system is encrypted or not. Default: - If your application has the '
        :param file_system_name: The file system's name. Default: - CDK generated name
        :param kms_key: The KMS key used for encryption. This is required to encrypt the data at rest if @encrypted is set to true. Default: - if 'encrypted' is true, the default key for EFS (/aws/elasticfilesystem) is used
        :param lifecycle_policy: A policy used by EFS lifecycle management to transition files to the Infrequent Access (IA) storage class. Default: - None. EFS will not transition files to the IA storage class.
        :param out_of_infrequent_access_policy: A policy used by EFS lifecycle management to transition files from Infrequent Access (IA) storage class to primary storage class. Default: - None. EFS will not transition files from IA storage to primary storage.
        :param performance_mode: The performance mode that the file system will operate under. An Amazon EFS file system's performance mode can't be changed after the file system has been created. Updating this property will replace the file system. Default: PerformanceMode.GENERAL_PURPOSE
        :param provisioned_throughput_per_second: Provisioned throughput for the file system. This is a required property if the throughput mode is set to PROVISIONED. Must be at least 1MiB/s. Default: - none, errors out
        :param removal_policy: The removal policy to apply to the file system. Default: RemovalPolicy.RETAIN
        :param security_group: Security Group to assign to this file system. Default: - creates new security group which allows all outbound traffic
        :param throughput_mode: Enum to mention the throughput mode of the file system. Default: ThroughputMode.BURSTING
        :param vpc_subnets: Which subnets to place the mount target in the VPC. Default: - the Vpc default strategy if not specified
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0265e0783e7671397c96c0da68a8c3724a7f5c6f4f86f1260aca2a10c0d21309)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EncryptedFileSystemProps(
            vpc=vpc,
            enable_automatic_backups=enable_automatic_backups,
            encrypted=encrypted,
            file_system_name=file_system_name,
            kms_key=kms_key,
            lifecycle_policy=lifecycle_policy,
            out_of_infrequent_access_policy=out_of_infrequent_access_policy,
            performance_mode=performance_mode,
            provisioned_throughput_per_second=provisioned_throughput_per_second,
            removal_policy=removal_policy,
            security_group=security_group,
            throughput_mode=throughput_mode,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''The EFS file system.'''
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IFileSystem, jsii.get(self, "fileSystem"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The KMS encryption key.'''
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "key"))


@jsii.implements(IEncryptedLogGroup)
class EncryptedLogGroup(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="shady-island.EncryptedLogGroup",
):
    '''A log group encrypted by a KMS customer managed key.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group_name: builtins.str,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ) -> None:
        '''Creates a new EncryptedLogGroup.

        :param scope: -
        :param id: -
        :param log_group_name: Name of the log group. We need a log group name ahead of time because otherwise the key policy would create a cyclical dependency.
        :param encryption_key: The KMS Key to encrypt the log group with. Default: A new KMS key will be created
        :param removal_policy: Whether the key and group should be retained when they are removed from the Stack. Default: RemovalPolicy.RETAIN
        :param retention: How long, in days, the log contents will be retained. Default: RetentionDays.TWO_YEARS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e62c39421d32db71f8755871011ead455af0c78b5896a1837602bdf3019046)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EncryptedLogGroupProps(
            log_group_name=log_group_name,
            encryption_key=encryption_key,
            removal_policy=removal_policy,
            retention=retention,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''The KMS encryption key.'''
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="logGroup")
    def log_group(self) -> _aws_cdk_aws_logs_ceddda9d.ILogGroup:
        '''The log group.'''
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.ILogGroup, jsii.get(self, "logGroup"))


__all__ = [
    "AssignOnLaunch",
    "AssignOnLaunchProps",
    "CidrContext",
    "CidrContextProps",
    "EncryptedFileSystem",
    "EncryptedFileSystemProps",
    "EncryptedLogGroup",
    "EncryptedLogGroupProps",
    "IAssignOnLaunch",
    "ICidrContext",
    "IEncryptedFileSystem",
    "IEncryptedLogGroup",
    "PrioritizedLines",
    "Tier",
    "UserDataBuilder",
    "Workload",
    "WorkloadProps",
]

publication.publish()

def _typecheckingstub__bf6464fd9d48d82d0db14a3cccbdb92cb250ed4fe6d6bd38b8e06d86417f53f2(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050e47d5b52c553cfe8b87e6673a27b8787fd0db2253c4e7b62521814ed5ae1d(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    address_pool: typing.Optional[builtins.str] = None,
    assign_address_on_launch: typing.Optional[builtins.bool] = None,
    cidr_block: typing.Optional[builtins.str] = None,
    cidr_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd1576cc635c21f66d4c77cc0746612de310b047b380081961173028162c533(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    enable_automatic_backups: typing.Optional[builtins.bool] = None,
    encrypted: typing.Optional[builtins.bool] = None,
    file_system_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    lifecycle_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.LifecyclePolicy] = None,
    out_of_infrequent_access_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.OutOfInfrequentAccessPolicy] = None,
    performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
    provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336d3d15e4b6b1d5a3f1d25302a1b6aa54f3525152e85c4efc9022074bbc84ef(
    *,
    log_group_name: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6e48c7b1cd24344a1cdbb27f3f7aea01ec3a2ce2f1bf2ce870bcc01f662aa91(
    *,
    lines: typing.Sequence[builtins.str],
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530a177d1cc816f59517c3e52dceeb99d4c7774e513d4d6bf96e414b10eee80f(
    id: builtins.str,
    label: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2f20e1b838706908cb4dc457364ab4d6a3ba246f70b4d648ff5df5ead1e52df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c184966e811a15ee5af7f9b885e27fa53713f5978c027ccfe09f4878a486801(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc74e7f1b826ca0249b2f9a045466e09289c315ccc1cc9056778d302475eac52(
    other: Tier,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56dc72e2b8d9e69be937435e41fa771eb82b99df61762e67305a1aa7d1a25cd(
    *commands: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6114eade1a4b4469c7ffa50dbde1b95b36c5b299d356317bbe384e4caf526133(
    priority: jsii.Number,
    *commands: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc677f9592ce3b6c83e0b51756bcbfa8439cf4279d746c77e45e81d3ac83c74(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    tier: Tier,
    base_domain_name: typing.Optional[builtins.str] = None,
    context_file: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ebb0ba06e254e10fe2379e1883988108104f296135702e61231d2437cee11e(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e27f5fc4333ac0563c57801a0b496252f1fe2f4b9a122724ccfbfec6d7998dbf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9ba1202ef7d254e0e9e1f79faf21a7241261ea59fec1d6b565e8f9c5709830b(
    id: builtins.str,
    *,
    analytics_reporting: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    stack_name: typing.Optional[builtins.str] = None,
    synthesizer: typing.Optional[_aws_cdk_ceddda9d.IStackSynthesizer] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2eedf91b5d4e25d97e311a1a26f03b3db1e8d5bba809f0a2bd20df11d9bdfb(
    *stacks: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19f32a870d457362c1bd937f00bb736bfc4263b2f555fd93d34c4bf7dd53f7a7(
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d21735e564e0f2e2aaeb9fd18b82adda3268ccc0278f45c2386e1cb3a55271(
    *,
    tier: Tier,
    base_domain_name: typing.Optional[builtins.str] = None,
    context_file: typing.Optional[builtins.str] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef34bf6f916957f913c4aa2b3459686556aaef0c4dde4b4cd1da18bd1bdf38e1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b0de4a00dc5c9be3f27b4ab96a0dcd78e40528295ed76dce57eec996acc188c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    address_pool: typing.Optional[builtins.str] = None,
    assign_address_on_launch: typing.Optional[builtins.bool] = None,
    cidr_block: typing.Optional[builtins.str] = None,
    cidr_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b002de4531052fe21d5d3510d0331c20a853e0a42c33e19aabc0f4c089723954(
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cidrs: typing.Sequence[builtins.str],
    cidr_block: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7693f240a70888012a03fe0b6a47ff72168fbb02ae5de987a68ac482cbe1a967(
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cidrs: typing.Sequence[builtins.str],
    cidr_block: _aws_cdk_ceddda9d.CfnResource,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__824a74b960abc01e0c39abfdf3e11416c999207fb7b170a7c45ff9e6f49b5189(
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    cidr_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0265e0783e7671397c96c0da68a8c3724a7f5c6f4f86f1260aca2a10c0d21309(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    enable_automatic_backups: typing.Optional[builtins.bool] = None,
    encrypted: typing.Optional[builtins.bool] = None,
    file_system_name: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    lifecycle_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.LifecyclePolicy] = None,
    out_of_infrequent_access_policy: typing.Optional[_aws_cdk_aws_efs_ceddda9d.OutOfInfrequentAccessPolicy] = None,
    performance_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.PerformanceMode] = None,
    provisioned_throughput_per_second: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    throughput_mode: typing.Optional[_aws_cdk_aws_efs_ceddda9d.ThroughputMode] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e62c39421d32db71f8755871011ead455af0c78b5896a1837602bdf3019046(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group_name: builtins.str,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
) -> None:
    """Type checking stubs"""
    pass
