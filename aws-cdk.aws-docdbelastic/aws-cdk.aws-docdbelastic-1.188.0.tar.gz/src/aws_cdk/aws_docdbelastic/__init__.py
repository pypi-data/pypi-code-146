'''
# AWS::DocDBElastic Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_docdbelastic as docdbelastic
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DocDBElastic construct libraries](https://constructs.dev/search?q=docdbelastic)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DocDBElastic resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DocDBElastic.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DocDBElastic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DocDBElastic.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnCluster(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-docdbelastic.CfnCluster",
):
    '''A CloudFormation ``AWS::DocDBElastic::Cluster``.

    Creates a new Elastic DocumentDB cluster and returns its Cluster structure.

    :cloudformationResource: AWS::DocDBElastic::Cluster
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_docdbelastic as docdbelastic
        
        cfn_cluster = docdbelastic.CfnCluster(self, "MyCfnCluster",
            admin_user_name="adminUserName",
            auth_type="authType",
            cluster_name="clusterName",
            shard_capacity=123,
            shard_count=123,
        
            # the properties below are optional
            admin_user_password="adminUserPassword",
            kms_key_id="kmsKeyId",
            preferred_maintenance_window="preferredMaintenanceWindow",
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_security_group_ids=["vpcSecurityGroupIds"]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        admin_user_name: builtins.str,
        auth_type: builtins.str,
        cluster_name: builtins.str,
        shard_capacity: jsii.Number,
        shard_count: jsii.Number,
        admin_user_password: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::DocDBElastic::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param admin_user_name: The name of the Elastic DocumentDB cluster administrator. *Constraints* : - Must be from 1 to 63 letters or numbers. - The first character must be a letter. - Cannot be a reserved word.
        :param auth_type: The authentication type for the Elastic DocumentDB cluster.
        :param cluster_name: The name of the new Elastic DocumentDB cluster. This parameter is stored as a lowercase string. *Constraints* : - Must contain from 1 to 63 letters, numbers, or hyphens. - The first character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. *Example* : ``my-cluster``
        :param shard_capacity: The capacity of each shard in the new Elastic DocumentDB cluster.
        :param shard_count: The number of shards to create in the new Elastic DocumentDB cluster.
        :param admin_user_password: The password for the Elastic DocumentDB cluster administrator and can contain any printable ASCII characters. *Constraints* : - Must contain from 8 to 100 characters. - Cannot contain a forward slash (/), double quote ("), or the "at" symbol (@). - A valid ``AdminUserName`` entry is also required.
        :param kms_key_id: The KMS key identifier to use to encrypt the new Elastic DocumentDB cluster. The KMS key identifier is the Amazon Resource Name (ARN) for the KMS encryption key. If you are creating a cluster using the same Amazon account that owns this KMS encryption key, you can use the KMS key alias instead of the ARN as the KMS encryption key. If an encryption key is not specified, Elastic DocumentDB uses the default encryption key that KMS creates for your account. Your account has a different default encryption key for each Amazon Region.
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC). *Format* : ``ddd:hh24:mi-ddd:hh24:mi`` *Default* : a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week. *Valid days* : Mon, Tue, Wed, Thu, Fri, Sat, Sun *Constraints* : Minimum 30-minute window.
        :param subnet_ids: The Amazon EC2 subnet IDs for the new Elastic DocumentDB cluster.
        :param tags: The tags to be assigned to the new Elastic DocumentDB cluster.
        :param vpc_security_group_ids: A list of EC2 VPC security groups to associate with the new Elastic DocumentDB cluster.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d09869e83d33dde3438834e19a27cb2521ed431fb0f33aced128f28f5c161352)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnClusterProps(
            admin_user_name=admin_user_name,
            auth_type=auth_type,
            cluster_name=cluster_name,
            shard_capacity=shard_capacity,
            shard_count=shard_count,
            admin_user_password=admin_user_password,
            kms_key_id=kms_key_id,
            preferred_maintenance_window=preferred_maintenance_window,
            subnet_ids=subnet_ids,
            tags=tags,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fd9e04c1c251db0bda31afa1b46700d1478e7a446f32eb31582077f1384601)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6f6f3edfdb19dcfaa8ea4ae6385e93d2bb86b7ea45fb9d74f0eb0e3ab8d0f9)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrClusterArn")
    def attr_cluster_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: ClusterArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrClusterArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags to be assigned to the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="adminUserName")
    def admin_user_name(self) -> builtins.str:
        '''The name of the Elastic DocumentDB cluster administrator.

        *Constraints* :

        - Must be from 1 to 63 letters or numbers.
        - The first character must be a letter.
        - Cannot be a reserved word.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-adminusername
        '''
        return typing.cast(builtins.str, jsii.get(self, "adminUserName"))

    @admin_user_name.setter
    def admin_user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7e3053bc421a76d65a4b9ffa7832d260827511217b01283a6eeeb3505548cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUserName", value)

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> builtins.str:
        '''The authentication type for the Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-authtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d5938c613cd83e026d7acf10ac53cb5fa65e02eb00d555bd77ea579bb74cd1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        '''The name of the new Elastic DocumentDB cluster. This parameter is stored as a lowercase string.

        *Constraints* :

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - The first character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        *Example* : ``my-cluster``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-clustername
        '''
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f9636992459c030c86c2bb1ee357ed551e817c95554e7d229135aab78abd08c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="shardCapacity")
    def shard_capacity(self) -> jsii.Number:
        '''The capacity of each shard in the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-shardcapacity
        '''
        return typing.cast(jsii.Number, jsii.get(self, "shardCapacity"))

    @shard_capacity.setter
    def shard_capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29011e74a85b342a71b0c37479ef2ba8ccb7dc088ba6136ddb98d86cc58d7258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="shardCount")
    def shard_count(self) -> jsii.Number:
        '''The number of shards to create in the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-shardcount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "shardCount"))

    @shard_count.setter
    def shard_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8691613b5b16bf6b507e71e81fddedc7409989e14de3c1ce80499154d598c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shardCount", value)

    @builtins.property
    @jsii.member(jsii_name="adminUserPassword")
    def admin_user_password(self) -> typing.Optional[builtins.str]:
        '''The password for the Elastic DocumentDB cluster administrator and can contain any printable ASCII characters.

        *Constraints* :

        - Must contain from 8 to 100 characters.
        - Cannot contain a forward slash (/), double quote ("), or the "at" symbol (@).
        - A valid ``AdminUserName`` entry is also required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-adminuserpassword
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "adminUserPassword"))

    @admin_user_password.setter
    def admin_user_password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ed37b8be863d62eb9af544d74f2bf844fdb6e509b571fb842342b011ab5672)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminUserPassword", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key identifier to use to encrypt the new Elastic DocumentDB cluster.

        The KMS key identifier is the Amazon Resource Name (ARN) for the KMS encryption key. If you are creating a cluster using the same Amazon account that owns this KMS encryption key, you can use the KMS key alias instead of the ARN as the KMS encryption key.

        If an encryption key is not specified, Elastic DocumentDB uses the default encryption key that KMS creates for your account. Your account has a different default encryption key for each Amazon Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d47a88f2ae29426e3aca810813d5e16dbc73e7c8707d8b2f9f0d99573a944619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

        *Format* : ``ddd:hh24:mi-ddd:hh24:mi``

        *Default* : a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week.

        *Valid days* : Mon, Tue, Wed, Thu, Fri, Sat, Sun

        *Constraints* : Minimum 30-minute window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d3137f60cc0794afa4c1ef8ad74e1c00dc1c6378633a9867f8bfe725349e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon EC2 subnet IDs for the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-subnetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc7a526eb7ff0c8b6ab6b570d356f753ea80a6e6e5f04988ef22a3f9f6c6e885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 VPC security groups to associate with the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-vpcsecuritygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "vpcSecurityGroupIds"))

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8759291919ef87ee55aac5b33efceb3ea43034e51810dad44cc3aca014199ff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcSecurityGroupIds", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-docdbelastic.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_user_name": "adminUserName",
        "auth_type": "authType",
        "cluster_name": "clusterName",
        "shard_capacity": "shardCapacity",
        "shard_count": "shardCount",
        "admin_user_password": "adminUserPassword",
        "kms_key_id": "kmsKeyId",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        admin_user_name: builtins.str,
        auth_type: builtins.str,
        cluster_name: builtins.str,
        shard_capacity: jsii.Number,
        shard_count: jsii.Number,
        admin_user_password: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCluster``.

        :param admin_user_name: The name of the Elastic DocumentDB cluster administrator. *Constraints* : - Must be from 1 to 63 letters or numbers. - The first character must be a letter. - Cannot be a reserved word.
        :param auth_type: The authentication type for the Elastic DocumentDB cluster.
        :param cluster_name: The name of the new Elastic DocumentDB cluster. This parameter is stored as a lowercase string. *Constraints* : - Must contain from 1 to 63 letters, numbers, or hyphens. - The first character must be a letter. - Cannot end with a hyphen or contain two consecutive hyphens. *Example* : ``my-cluster``
        :param shard_capacity: The capacity of each shard in the new Elastic DocumentDB cluster.
        :param shard_count: The number of shards to create in the new Elastic DocumentDB cluster.
        :param admin_user_password: The password for the Elastic DocumentDB cluster administrator and can contain any printable ASCII characters. *Constraints* : - Must contain from 8 to 100 characters. - Cannot contain a forward slash (/), double quote ("), or the "at" symbol (@). - A valid ``AdminUserName`` entry is also required.
        :param kms_key_id: The KMS key identifier to use to encrypt the new Elastic DocumentDB cluster. The KMS key identifier is the Amazon Resource Name (ARN) for the KMS encryption key. If you are creating a cluster using the same Amazon account that owns this KMS encryption key, you can use the KMS key alias instead of the ARN as the KMS encryption key. If an encryption key is not specified, Elastic DocumentDB uses the default encryption key that KMS creates for your account. Your account has a different default encryption key for each Amazon Region.
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC). *Format* : ``ddd:hh24:mi-ddd:hh24:mi`` *Default* : a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week. *Valid days* : Mon, Tue, Wed, Thu, Fri, Sat, Sun *Constraints* : Minimum 30-minute window.
        :param subnet_ids: The Amazon EC2 subnet IDs for the new Elastic DocumentDB cluster.
        :param tags: The tags to be assigned to the new Elastic DocumentDB cluster.
        :param vpc_security_group_ids: A list of EC2 VPC security groups to associate with the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_docdbelastic as docdbelastic
            
            cfn_cluster_props = docdbelastic.CfnClusterProps(
                admin_user_name="adminUserName",
                auth_type="authType",
                cluster_name="clusterName",
                shard_capacity=123,
                shard_count=123,
            
                # the properties below are optional
                admin_user_password="adminUserPassword",
                kms_key_id="kmsKeyId",
                preferred_maintenance_window="preferredMaintenanceWindow",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_security_group_ids=["vpcSecurityGroupIds"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87540fb3c1dd7d8a6f97c44c1c1b2ba4fef89b92d0d01356f876725fa351fa68)
            check_type(argname="argument admin_user_name", value=admin_user_name, expected_type=type_hints["admin_user_name"])
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument shard_capacity", value=shard_capacity, expected_type=type_hints["shard_capacity"])
            check_type(argname="argument shard_count", value=shard_count, expected_type=type_hints["shard_count"])
            check_type(argname="argument admin_user_password", value=admin_user_password, expected_type=type_hints["admin_user_password"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_security_group_ids", value=vpc_security_group_ids, expected_type=type_hints["vpc_security_group_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_user_name": admin_user_name,
            "auth_type": auth_type,
            "cluster_name": cluster_name,
            "shard_capacity": shard_capacity,
            "shard_count": shard_count,
        }
        if admin_user_password is not None:
            self._values["admin_user_password"] = admin_user_password
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def admin_user_name(self) -> builtins.str:
        '''The name of the Elastic DocumentDB cluster administrator.

        *Constraints* :

        - Must be from 1 to 63 letters or numbers.
        - The first character must be a letter.
        - Cannot be a reserved word.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-adminusername
        '''
        result = self._values.get("admin_user_name")
        assert result is not None, "Required property 'admin_user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth_type(self) -> builtins.str:
        '''The authentication type for the Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-authtype
        '''
        result = self._values.get("auth_type")
        assert result is not None, "Required property 'auth_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cluster_name(self) -> builtins.str:
        '''The name of the new Elastic DocumentDB cluster. This parameter is stored as a lowercase string.

        *Constraints* :

        - Must contain from 1 to 63 letters, numbers, or hyphens.
        - The first character must be a letter.
        - Cannot end with a hyphen or contain two consecutive hyphens.

        *Example* : ``my-cluster``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def shard_capacity(self) -> jsii.Number:
        '''The capacity of each shard in the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-shardcapacity
        '''
        result = self._values.get("shard_capacity")
        assert result is not None, "Required property 'shard_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def shard_count(self) -> jsii.Number:
        '''The number of shards to create in the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-shardcount
        '''
        result = self._values.get("shard_count")
        assert result is not None, "Required property 'shard_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def admin_user_password(self) -> typing.Optional[builtins.str]:
        '''The password for the Elastic DocumentDB cluster administrator and can contain any printable ASCII characters.

        *Constraints* :

        - Must contain from 8 to 100 characters.
        - Cannot contain a forward slash (/), double quote ("), or the "at" symbol (@).
        - A valid ``AdminUserName`` entry is also required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-adminuserpassword
        '''
        result = self._values.get("admin_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The KMS key identifier to use to encrypt the new Elastic DocumentDB cluster.

        The KMS key identifier is the Amazon Resource Name (ARN) for the KMS encryption key. If you are creating a cluster using the same Amazon account that owns this KMS encryption key, you can use the KMS key alias instead of the ARN as the KMS encryption key.

        If an encryption key is not specified, Elastic DocumentDB uses the default encryption key that KMS creates for your account. Your account has a different default encryption key for each Amazon Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur, in Universal Coordinated Time (UTC).

        *Format* : ``ddd:hh24:mi-ddd:hh24:mi``

        *Default* : a 30-minute window selected at random from an 8-hour block of time for each AWS Region , occurring on a random day of the week.

        *Valid days* : Mon, Tue, Wed, Thu, Fri, Sat, Sun

        *Constraints* : Minimum 30-minute window.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon EC2 subnet IDs for the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags to be assigned to the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of EC2 VPC security groups to associate with the new Elastic DocumentDB cluster.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-docdbelastic-cluster.html#cfn-docdbelastic-cluster-vpcsecuritygroupids
        '''
        result = self._values.get("vpc_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCluster",
    "CfnClusterProps",
]

publication.publish()

def _typecheckingstub__d09869e83d33dde3438834e19a27cb2521ed431fb0f33aced128f28f5c161352(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    admin_user_name: builtins.str,
    auth_type: builtins.str,
    cluster_name: builtins.str,
    shard_capacity: jsii.Number,
    shard_count: jsii.Number,
    admin_user_password: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fd9e04c1c251db0bda31afa1b46700d1478e7a446f32eb31582077f1384601(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6f6f3edfdb19dcfaa8ea4ae6385e93d2bb86b7ea45fb9d74f0eb0e3ab8d0f9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7e3053bc421a76d65a4b9ffa7832d260827511217b01283a6eeeb3505548cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d5938c613cd83e026d7acf10ac53cb5fa65e02eb00d555bd77ea579bb74cd1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9636992459c030c86c2bb1ee357ed551e817c95554e7d229135aab78abd08c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29011e74a85b342a71b0c37479ef2ba8ccb7dc088ba6136ddb98d86cc58d7258(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8691613b5b16bf6b507e71e81fddedc7409989e14de3c1ce80499154d598c9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ed37b8be863d62eb9af544d74f2bf844fdb6e509b571fb842342b011ab5672(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d47a88f2ae29426e3aca810813d5e16dbc73e7c8707d8b2f9f0d99573a944619(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d3137f60cc0794afa4c1ef8ad74e1c00dc1c6378633a9867f8bfe725349e1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc7a526eb7ff0c8b6ab6b570d356f753ea80a6e6e5f04988ef22a3f9f6c6e885(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8759291919ef87ee55aac5b33efceb3ea43034e51810dad44cc3aca014199ff9(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87540fb3c1dd7d8a6f97c44c1c1b2ba4fef89b92d0d01356f876725fa351fa68(
    *,
    admin_user_name: builtins.str,
    auth_type: builtins.str,
    cluster_name: builtins.str,
    shard_capacity: jsii.Number,
    shard_count: jsii.Number,
    admin_user_password: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
